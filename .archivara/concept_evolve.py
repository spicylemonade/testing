#!/usr/bin/env python3
"""ConceptEvolve: concept-tree exploration via Codex child agents.

Sub-agents do the real work — researching, thinking, and writing files
directly using their tools (bash, read, write, websearch, webfetch,
semantic_scholar).  Python just launches them and post-processes the
filesystem artifacts they leave behind.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = SCRIPT_DIR.parent / "results" / "concept_evolve"
TREE_DIR = RESULTS_DIR / "tree"
DEBUG_DIR = RESULTS_DIR / ".debug"
STATE_DIR = RESULTS_DIR / ".state"
ACTIVE_RUN_STATE_FILE = STATE_DIR / "active_run.json"
OPENCODE_LOG_DIR = Path.home() / ".local" / "share" / "opencode" / "log"
DEFAULT_CODEX_MODEL = "gpt-5.4"
CODEX_MODEL = os.environ.get(
    "CONCEPT_EVOLVE_MODEL", os.environ.get("CODEX_MODEL", os.environ.get("OPENCODE_MODEL", DEFAULT_CODEX_MODEL))
)
if "/" in CODEX_MODEL:
    CODEX_MODEL = CODEX_MODEL.split("/", 1)[1]
CODEX_REASONING_EFFORT = str(
    os.environ.get("CODEX_REASONING_EFFORT", os.environ.get("OPENCODE_REASONING_EFFORT", "high"))
).strip().lower()
if CODEX_REASONING_EFFORT == "xhigh":
    CODEX_REASONING_EFFORT = "high"
if CODEX_REASONING_EFFORT not in {"minimal", "low", "medium", "high"}:
    CODEX_REASONING_EFFORT = "high"
CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))

# Legacy OpenCode settings retained for quick rollback.
OPEN_CODE_MODEL_REF = f"openai/{CODEX_MODEL}"
OPEN_CODE_AGENT = os.environ.get("CONCEPT_EVOLVE_AGENT", "build")
EVOLVE_LOCK_FILE = RESULTS_DIR / ".evolve.lock"
EVOLVE_CACHE_TTL_SECONDS = int(os.environ.get("CONCEPT_EVOLVE_CACHE_TTL_SECONDS", "7200"))
CHILD_LOOP_EXIT_CODE = 86
CHILD_STEP_CHURN_LIMIT = max(
    200, int(os.environ.get("CONCEPT_EVOLVE_STEP_CHURN_LIMIT", "480") or "480")
)
CHILD_EXISTING_ARTIFACT_STEP_CHURN_LIMIT = max(
    80,
    int(
        os.environ.get(
            "CONCEPT_EVOLVE_EXISTING_ARTIFACT_STEP_CHURN_LIMIT",
            "160",
        )
        or "160"
    ),
)
CHILD_POLL_INTERVAL_SECONDS = max(
    0.5, float(os.environ.get("CONCEPT_EVOLVE_POLL_INTERVAL_SECONDS", "1.5") or "1.5")
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(value: str) -> str:
    lowered = (value or "").strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return cleaned or "concept"


def _normalize_topic(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip()).lower()


def _debug_log(filename: str, content: str):
    try:
        DEBUG_DIR.mkdir(parents=True, exist_ok=True)
        (DEBUG_DIR / filename).write_text(content[:500_000])
    except Exception:
        pass


def _compact_text(value: str, limit: int = 200) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())[:limit]


def _prepare_codex_cli():
    CODEX_HOME.mkdir(parents=True, exist_ok=True)
    agents_dir = CODEX_HOME / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    role_files = {
        "explorer.toml": "\n".join(
            [
                f'model = "{CODEX_MODEL}"',
                'model_reasoning_effort = "medium"',
                'sandbox_mode = "read-only"',
                'developer_instructions = """Stay in exploration mode. Read code, inspect artifacts, use web search when needed, and return concrete evidence. Avoid editing files unless the parent agent explicitly asks for it."""',
                "",
            ]
        ),
        "worker.toml": "\n".join(
            [
                f'model = "{CODEX_MODEL}"',
                'model_reasoning_effort = "medium"',
                'sandbox_mode = "workspace-write"',
                'developer_instructions = """Own a narrow implementation or experiment task. Make the smallest defensible change, keep scope tight, and return the exact files and evidence you produced."""',
                "",
            ]
        ),
        "monitor.toml": "\n".join(
            [
                f'model = "{CODEX_MODEL}"',
                'model_reasoning_effort = "medium"',
                'sandbox_mode = "read-only"',
                'developer_instructions = """Specialize in waiting, polling, and summarizing long-running commands or workflows. Do not start unrelated work."""',
                "",
            ]
        ),
        "integrator.toml": "\n".join(
            [
                f'model = "{CODEX_MODEL}"',
                'model_reasoning_effort = "high"',
                'sandbox_mode = "workspace-write"',
                'developer_instructions = """Integrate multiple specialist outputs into one concise decision. Do not restart broad searches when synthesis is the real task."""',
                "",
            ]
        ),
    }
    for filename, contents in role_files.items():
        (agents_dir / filename).write_text(contents)
    config_path = CODEX_HOME / "config.toml"
    config_path.write_text(
        "\n".join(
            [
                f'model = "{CODEX_MODEL}"',
                'approval_policy = "never"',
                'sandbox_mode = "danger-full-access"',
                f'model_reasoning_effort = "{CODEX_REASONING_EFFORT}"',
                'web_search = "live"',
                "",
                "[features]",
                "multi_agent = true",
                "",
                "[agents]",
                "max_threads = 6",
                "max_depth = 1",
                "job_max_runtime_seconds = 1800",
                "",
                '[agents.explorer]',
                'description = "Read-only codebase and literature explorer."',
                'config_file = "agents/explorer.toml"',
                "",
                '[agents.worker]',
                'description = "Execution-focused worker for narrow implementation or experiment tasks."',
                'config_file = "agents/worker.toml"',
                "",
                '[agents.monitor]',
                'description = "Long-running command and polling monitor."',
                'config_file = "agents/monitor.toml"',
                "",
                '[agents.integrator]',
                'description = "Synthesis role that consolidates specialist outputs."',
                'config_file = "agents/integrator.toml"',
                "",
                "[shell_environment_policy]",
                'inherit = "all"',
                "",
                "[history]",
                'persistence = "none"',
                "",
            ]
        )
    )
    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for Codex child runs")
    login_env = {**os.environ, "CODEX_HOME": str(CODEX_HOME)}
    login_errors = []
    login_attempts = [
        (["codex", "login", "--with-api-key"], api_key + "\n"),
        (["codex", "login", "--api-key", api_key], None),
    ]
    for login_cmd, login_input in login_attempts:
        login = subprocess.run(
            login_cmd,
            env=login_env,
            input=login_input,
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR),
        )
        if login.returncode == 0:
            return
        login_errors.append(
            f"{' '.join(login_cmd)} :: {(login.stdout or '')[-200:]} {(login.stderr or '')[-200:]}"
        )
    raise RuntimeError(
        "Codex login failed: " + " || ".join(login_errors)
    )


# ---------------------------------------------------------------------------
# Sub-agent runner
# ---------------------------------------------------------------------------

def _run_sub_agent(
    prompt: str,
    *,
    name: str,
    command: str,
    fingerprint: str,
    topic: str,
    watched_paths: List[Path],
) -> int:
    """Launch a Codex child agent and wait for it to finish.

    The sub-agent is expected to do its work by writing files via its own
    tools (bash, read, write, edit, etc.). We watch its target artifacts and
    internal step stream so duplicate/no-progress loops can be cut
    off without relying on wall-clock timeouts.

    Returns the process exit code (0 = success).
    """
    _prepare_codex_cli()
    env = os.environ.copy()
    env["CODEX_HOME"] = str(CODEX_HOME)
    env["CODEX_MODEL"] = CODEX_MODEL
    env["CODEX_REASONING_EFFORT"] = CODEX_REASONING_EFFORT
    cmd = [
        "codex",
        "exec",
        "--json",
        "--color",
        "never",
        "--model",
        CODEX_MODEL,
        "-C",
        str(SCRIPT_DIR.parent),
        "-c",
        f'model_reasoning_effort="{CODEX_REASONING_EFFORT}"',
        "-c",
        'shell_environment_policy.inherit="all"',
        "-c",
        'web_search="live"',
        (
            f"ROLE: {OPEN_CODE_AGENT}\n"
            "You are a Codex child agent launched by ConceptEvolve.\n"
            "Codex multi-agent is enabled with explorer, worker, monitor, and integrator roles.\n"
            "If the task clearly parallelizes, you may use one child-agent layer and then synthesize the result yourself.\n"
            "Work only on the requested concept task and write the requested artifacts.\n\n"
            + prompt
        ),
    ]
    started_at = _now()
    snapshot = _artifact_snapshot(watched_paths)
    existing_artifact = any(meta.get("exists") for meta in snapshot.values())
    churn_limit = (
        CHILD_EXISTING_ARTIFACT_STEP_CHURN_LIMIT
        if existing_artifact
        else CHILD_STEP_CHURN_LIMIT
    )

    _debug_log(f"{name}_cmd.txt", " ".join(cmd))
    _debug_log(
        f"{name}_env.txt",
        "\n".join(
            f"{k}=<set:{len(v)}>" for k, v in sorted(env.items())
            if k.startswith(("OPEN", "CODEX", "CONCEPT", "ANTHROPIC", "CLAUDE", "GEMINI", "GOOGLE"))
        ),
    )

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(SCRIPT_DIR),
            env=env,
            bufsize=1,
        )
    except FileNotFoundError:
        _debug_log(f"{name}_error.txt", "codex binary not found")
        _write_run_state(
            command,
            fingerprint,
            {
                "status": "failed",
                "name": name,
                "topic": topic,
                "started_at": started_at,
                "updated_at": _now(),
                "note": "codex binary not found",
                "target_artifacts": [_relative_path(path) for path in watched_paths],
            },
        )
        return 1
    except Exception as exc:
        _debug_log(f"{name}_error.txt", str(exc))
        _write_run_state(
            command,
            fingerprint,
            {
                "status": "failed",
                "name": name,
                "topic": topic,
                "started_at": started_at,
                "updated_at": _now(),
                "note": _compact_text(str(exc), 220),
                "target_artifacts": [_relative_path(path) for path in watched_paths],
            },
        )
        return 1

    if process.stdout is None:
        if process.poll() is None:
            process.kill()
        _debug_log(f"{name}_error.txt", "codex stdout pipe missing")
        _write_run_state(
            command,
            fingerprint,
            {
                "status": "failed",
                "name": name,
                "topic": topic,
                "pid": process.pid,
                "started_at": started_at,
                "updated_at": _now(),
                "note": "codex stdout pipe missing",
                "target_artifacts": [_relative_path(path) for path in watched_paths],
            },
        )
        return 1

    _set_nonblocking(process.stdout)
    stdout_lines: List[str] = []
    last_step = 0
    stalled_step_events = 0
    progress_counter = 0
    last_log_line = ""
    changed_paths: List[str] = []
    churn_reason = ""
    target_artifacts = [_relative_path(path) for path in watched_paths]
    last_output_excerpt = ""

    _write_run_state(
        command,
        fingerprint,
        {
            "status": "running",
            "name": name,
            "topic": topic,
            "pid": process.pid,
            "started_at": started_at,
            "updated_at": started_at,
            "target_artifacts": target_artifacts,
            "artifact_snapshot": snapshot,
            "progress_counter": progress_counter,
            "last_step": last_step,
            "stalled_step_events": stalled_step_events,
            "stalled_step_limit": churn_limit,
            "existing_artifact": existing_artifact,
            "note": "child started",
        },
    )

    def _codex_step_info(text_line: str) -> tuple[int, str]:
        try:
            event = json.loads(text_line)
        except Exception:
            return 0, text_line
        payload = event.get("msg") if isinstance(event, dict) and isinstance(event.get("msg"), dict) else event
        if not isinstance(payload, dict):
            return 0, text_line
        event_type = str(payload.get("type", ""))
        thread_label = (
            payload.get("source_thread_label")
            or payload.get("thread_label")
            or payload.get("agent_type")
            or ""
        )

        def _decorate(message: str) -> str:
            if not message:
                return message
            if thread_label:
                return f"[agent:{thread_label}] {message}"
            return message

        if event_type in {"task_started", "agent_reasoning_section_break"}:
            return 1, _decorate(event_type)
        if event_type == "agent_reasoning":
            return 1, _decorate(_compact_text(str(payload.get("text", "")), 220))
        if event_type == "agent_message":
            return 1, _decorate(_compact_text(str(payload.get("message", "")), 220))
        if event_type == "exec_command_begin":
            command_bits = payload.get("command")
            rendered = " ".join(command_bits) if isinstance(command_bits, list) else str(command_bits or "")
            return 1, _decorate(_compact_text(rendered, 220))
        if event_type == "exec_command_end":
            rendered = (
                payload.get("formatted_output")
                or payload.get("aggregated_output")
                or payload.get("stdout")
                or payload.get("stderr")
                or ""
            )
            return 1, _decorate(_compact_text(str(rendered), 220))
        return 0, _decorate(_compact_text(text_line, 220))

    while True:
        step_delta = 0
        try:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                text_line = line.rstrip()
                stdout_lines.append(text_line)
                if text_line:
                    delta, excerpt = _codex_step_info(text_line)
                    step_delta += delta
                    if excerpt:
                        last_log_line = excerpt
                        last_output_excerpt = excerpt
        except (IOError, BlockingIOError):
            pass
        except UnicodeDecodeError as exc:
            _debug_log(f"{name}_decode_error.txt", str(exc))

        last_step += step_delta

        current_snapshot = _artifact_snapshot(watched_paths)
        changed_paths = _changed_snapshot_paths(snapshot, current_snapshot)
        if changed_paths:
            snapshot = current_snapshot
            progress_counter += 1
            stalled_step_events = 0
        elif step_delta > 0:
            stalled_step_events += step_delta

        _write_run_state(
            command,
            fingerprint,
            {
                "status": "running",
                "name": name,
                "topic": topic,
                "pid": process.pid,
                "started_at": started_at,
                "updated_at": _now(),
                "target_artifacts": target_artifacts,
                "artifact_snapshot": snapshot,
                "changed_paths": changed_paths[:8],
                "progress_counter": progress_counter,
                "last_step": last_step,
                "stalled_step_events": stalled_step_events,
                "stalled_step_limit": churn_limit,
                "existing_artifact": existing_artifact,
                "codex_log": "",
                "last_log_line": last_log_line,
                "last_output_excerpt": last_output_excerpt,
            },
        )

        if last_step > 0 and stalled_step_events >= churn_limit:
            churn_reason = (
                "step churn detected after "
                f"{stalled_step_events} internal steps without new target artifact deltas"
            )
            _debug_log(f"{name}_error.txt", churn_reason)
            _write_run_state(
                command,
                fingerprint,
                {
                    "status": "loop_detected",
                    "name": name,
                    "topic": topic,
                    "pid": process.pid,
                    "started_at": started_at,
                    "updated_at": _now(),
                    "target_artifacts": target_artifacts,
                    "artifact_snapshot": snapshot,
                    "changed_paths": changed_paths[:8],
                    "progress_counter": progress_counter,
                    "last_step": last_step,
                    "stalled_step_events": stalled_step_events,
                    "stalled_step_limit": churn_limit,
                    "existing_artifact": existing_artifact,
                    "codex_log": "",
                    "last_log_line": last_log_line,
                    "last_output_excerpt": last_output_excerpt,
                    "note": churn_reason,
                },
            )
            if process.poll() is None:
                process.kill()
            break

        if process.poll() is not None:
            break

        time.sleep(CHILD_POLL_INTERVAL_SECONDS)

    try:
        remaining = process.stdout.read()
        if remaining:
            for line in remaining.splitlines():
                text_line = line.rstrip()
                stdout_lines.append(text_line)
                if text_line:
                    last_output_excerpt = _compact_text(text_line, 220)
    except Exception:
        pass

    process.wait()
    final_snapshot = _artifact_snapshot(watched_paths)
    final_code = CHILD_LOOP_EXIT_CODE if churn_reason else process.returncode
    final_status = "completed" if final_code == 0 else "failed"
    if churn_reason:
        final_status = "loop_detected"

    _write_run_state(
        command,
        fingerprint,
        {
            "status": final_status,
            "name": name,
            "topic": topic,
            "pid": process.pid,
            "started_at": started_at,
            "finished_at": _now(),
            "updated_at": _now(),
            "target_artifacts": target_artifacts,
            "artifact_snapshot": final_snapshot,
            "progress_counter": progress_counter,
            "last_step": last_step,
            "stalled_step_events": stalled_step_events,
            "stalled_step_limit": churn_limit,
            "existing_artifact": existing_artifact,
            "codex_log": "",
            "last_log_line": last_log_line,
            "last_output_excerpt": last_output_excerpt,
            "return_code": final_code,
            "note": churn_reason or f"child exited with code {process.returncode}",
        },
    )
    _debug_log(f"{name}_stdout.txt", "\n".join(stdout_lines)[:200_000])
    _debug_log(f"{name}_rc.txt", str(final_code))
    return final_code


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def _write_json(path: Path, payload: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _hash_file(path: Path) -> str:
    if not path.exists():
        return ""
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
    except Exception:
        return ""
    return digest.hexdigest()


def _relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(SCRIPT_DIR.parent))
    except Exception:
        return str(path)


def _operation_context_paths(command: str) -> List[Path]:
    repo_root = SCRIPT_DIR.parent
    base = [
        repo_root / "results/research_context.md",
        repo_root / "results/literature/prior_art_watchlist.md",
        repo_root / "results/literature/prior_art_gap.md",
        repo_root / "results/literature/semantic_scholar_manifest.json",
        repo_root / "results/swarm/director_brief.md",
        repo_root / "results/swarm/hypotheses.json",
        repo_root / "results/swarm/tool_plan.md",
        repo_root / "results/swarm/falsifier.md",
    ]
    extras = {
        "probe": [
            RESULTS_DIR / "concept_cards.json",
            RESULTS_DIR / "semantic_bridge.json",
            RESULTS_DIR / "steering_directions.json",
            repo_root / "results/verification/verification_summary.md",
        ],
        "reframe": [
            RESULTS_DIR / "probe_result.json",
            RESULTS_DIR / "concept_delta.md",
            repo_root / "results/verification/verification_summary.md",
        ],
        "iterate": [
            RESULTS_DIR / "probe_result.json",
            RESULTS_DIR / "reframings.json",
            RESULTS_DIR / "concept_delta.json",
            RESULTS_DIR / "recurrent_state.json",
            repo_root / "results/verification/novelty_report.md",
            repo_root / "results/verification/benchmark_report.md",
            repo_root / "results/verification/citation_audit.md",
            repo_root / "results/verification/verification_summary.md",
        ],
    }
    ordered: List[Path] = []
    seen: set[str] = set()
    for path in base + extras.get(command, []):
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        ordered.append(path)
    return ordered


def _build_operation_fingerprint(command: str, topic: str) -> tuple[str, Dict[str, Any]]:
    payload = {
        "command": command,
        "topic": _normalize_topic(topic),
        "context": [
            {
                "path": _relative_path(path),
                "exists": path.exists(),
                "sha256": _hash_file(path),
            }
            for path in _operation_context_paths(command)
        ],
    }
    fingerprint = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return fingerprint, payload


def _operation_lock_path(command: str, fingerprint: str) -> Path:
    return STATE_DIR / f".{command}_{fingerprint}.lock"


def _operation_state_path(command: str, fingerprint: str) -> Path:
    return STATE_DIR / f"{command}_{fingerprint}.json"


def _write_run_state(command: str, fingerprint: str, payload: Dict[str, Any]):
    state = {"command": command, "fingerprint": fingerprint, **payload}
    _write_json(_operation_state_path(command, fingerprint), state)
    _write_json(STATE_DIR / f"{command}_latest.json", state)
    _write_json(STATE_DIR / "latest_run.json", state)
    _write_json(ACTIVE_RUN_STATE_FILE, state)


def _operation_lock(command: str, fingerprint: str):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    lock_fp = _operation_lock_path(command, fingerprint).open("w")
    fcntl.flock(lock_fp.fileno(), fcntl.LOCK_EX)
    return lock_fp


def _artifact_snapshot(paths: List[Path]) -> Dict[str, Dict[str, Any]]:
    snapshot: Dict[str, Dict[str, Any]] = {}
    for path in paths:
        key = _relative_path(path)
        try:
            stat = path.stat()
            snapshot[key] = {
                "exists": True,
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        except FileNotFoundError:
            snapshot[key] = {"exists": False, "size": 0, "mtime_ns": 0}
    return snapshot


def _changed_snapshot_paths(
    previous: Dict[str, Dict[str, Any]],
    current: Dict[str, Dict[str, Any]],
) -> List[str]:
    changed: List[str] = []
    for key, meta in current.items():
        if previous.get(key) != meta:
            changed.append(key)
    return changed


def _list_opencode_logs() -> List[Path]:
    if not OPENCODE_LOG_DIR.exists():
        return []
    try:
        return sorted(OPENCODE_LOG_DIR.glob("*.log"), key=lambda path: path.stat().st_mtime, reverse=True)
    except Exception:
        return []


def _discover_child_log(known_logs: set[str], started_at: float) -> Path | None:
    new_candidates: List[tuple[float, Path]] = []
    recent_candidates: List[tuple[float, Path]] = []
    for path in _list_opencode_logs():
        try:
            mtime = path.stat().st_mtime
        except FileNotFoundError:
            continue
        if str(path) not in known_logs:
            new_candidates.append((mtime, path))
        if mtime >= started_at - 2:
            recent_candidates.append((mtime, path))
    candidates = new_candidates or recent_candidates
    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])[1]


_STEP_PATTERN = re.compile(r"session\.prompt step=(\d+)")


def _read_log_step_delta(
    log_path: Path,
    offset: int,
    last_step: int,
) -> tuple[int, int, int, str]:
    if not log_path.exists():
        return offset, last_step, 0, ""
    try:
        size = log_path.stat().st_size
        if size < offset:
            offset = 0
        with log_path.open("r", encoding="utf-8", errors="ignore") as handle:
            handle.seek(offset)
            chunk = handle.read()
            new_offset = handle.tell()
    except Exception:
        return offset, last_step, 0, ""

    max_step = last_step
    step_delta = 0
    last_excerpt = ""
    for raw in chunk.splitlines():
        line = raw.strip()
        if not line:
            continue
        last_excerpt = line
        match = _STEP_PATTERN.search(line)
        if not match:
            continue
        step_value = int(match.group(1))
        if step_value > max_step:
            step_delta += step_value - max_step
            max_step = step_value
    return new_offset, max_step, step_delta, _compact_text(last_excerpt, 220)


def _set_nonblocking(pipe):
    fd = pipe.fileno()
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


def _json_candidates(text: str) -> List[str]:
    candidates: List[str] = []
    stripped = text.strip()
    if stripped:
        candidates.append(stripped)
    for block in re.findall(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL):
        block = block.strip()
        if block:
            candidates.append(block)
    starts = [i for i, c in enumerate(text) if c in "[{"]
    for start in starts:
        stack: list[str] = []
        for i in range(start, len(text)):
            c = text[i]
            if c in "[{":
                stack.append(c)
            elif c in "]}":
                if not stack:
                    break
                stack.pop()
                if not stack:
                    candidates.append(text[start : i + 1])
                    break
    return candidates


def _read_json(path: Path) -> Any:
    """Read a JSON file, tolerating markdown fences or leading/trailing text."""
    if not path.exists():
        return None
    text = path.read_text()
    for block in _json_candidates(text):
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            continue
    return None


def _is_fresh_timestamp(value: Any, max_age_seconds: int) -> bool:
    if not isinstance(value, str) or max_age_seconds <= 0:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return False
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - parsed).total_seconds()
    return age <= max_age_seconds


def _load_cached_evolve(topic: str) -> Dict[str, Any] | None:
    result = _read_json(RESULTS_DIR / "evolve_results.json")
    cards = _read_json(RESULTS_DIR / "concept_cards.json")
    if not isinstance(result, dict):
        return None
    if _normalize_topic(result.get("topic", "")) != _normalize_topic(topic):
        return None
    if not isinstance(cards, list) or not cards:
        return None
    if not _is_fresh_timestamp(result.get("timestamp"), EVOLVE_CACHE_TTL_SECONDS):
        return None

    cached = dict(result)
    cached["status"] = "cached"
    cached["cache_hit"] = True
    cached["cached_at"] = _now()
    cached["cache_ttl_seconds"] = EVOLVE_CACHE_TTL_SECONDS
    return cached


def _safe_list(value: Any) -> List[Dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def _problem_matches(current: Any, expected: str) -> bool:
    return _normalize_topic(str(current or "")) == _normalize_topic(expected)


def _load_cached_probe(problem: str, fingerprint: str) -> Dict[str, Any] | None:
    payload = _read_json(RESULTS_DIR / "probe_result.json")
    if not isinstance(payload, dict):
        return None
    if not _problem_matches(payload.get("sub_problem") or payload.get("problem"), problem):
        return None
    if payload.get("input_fingerprint") != fingerprint:
        return None
    directions = payload.get("steering_directions")
    if not isinstance(directions, list) or not directions:
        return None
    cached = dict(payload)
    cached["status"] = "cached"
    cached["cache_hit"] = True
    cached["cached_at"] = _now()
    return cached


def _load_cached_reframe(problem: str, fingerprint: str) -> Dict[str, Any] | None:
    payload = _read_json(RESULTS_DIR / "reframings.json")
    framings: list = []
    if isinstance(payload, dict):
        if not _problem_matches(payload.get("problem"), problem):
            return None
        if payload.get("input_fingerprint") != fingerprint:
            return None
        framings = payload.get("framings", [])
    elif isinstance(payload, list):
        return None
    if not isinstance(framings, list) or not framings:
        return None
    return {
        "problem": problem,
        "framings": framings,
        "timestamp": payload.get("timestamp") if isinstance(payload, dict) else _now(),
        "input_fingerprint": fingerprint,
        "status": "cached",
        "cache_hit": True,
        "cached_at": _now(),
    }


def _load_cached_iterate(problem: str, fingerprint: str) -> Dict[str, Any] | None:
    recurrent_state = _read_json(RESULTS_DIR / "recurrent_state.json")
    candidates = _read_json(RESULTS_DIR / "bridge_candidates.json")
    concept_delta = _read_json(RESULTS_DIR / "concept_delta.json")
    if not isinstance(recurrent_state, dict):
        return None
    if not _problem_matches(recurrent_state.get("focus"), problem):
        return None
    if recurrent_state.get("input_fingerprint") != fingerprint:
        return None
    if not isinstance(candidates, list) or not candidates:
        return None
    if not isinstance(concept_delta, dict):
        concept_delta = {
            "promoted_bridges": [],
            "retired_bridges": [],
        }
    return {
        "problem": problem,
        "iteration_count": int(recurrent_state.get("iteration_count", 0) or 0),
        "champion_bridge": recurrent_state.get("champion_bridge"),
        "promoted_bridges": len(concept_delta.get("promoted_bridges") or []),
        "retired_bridges": len(concept_delta.get("retired_bridges") or []),
        "timestamp": recurrent_state.get("timestamp") or _now(),
        "input_fingerprint": fingerprint,
        "status": "cached",
        "cache_hit": True,
        "cached_at": _now(),
    }


def _record_cache_hit(
    command: str,
    fingerprint: str,
    topic: str,
    artifact_paths: List[Path],
    note: str,
):
    _write_run_state(
        command,
        fingerprint,
        {
            "status": "cache_hit",
            "topic": topic,
            "updated_at": _now(),
            "target_artifacts": [_relative_path(path) for path in artifact_paths],
            "note": note,
        },
    )


def _with_loop_recovery_guidance(prompt: str, artifact_path: Path) -> str:
    return (
        prompt
        + f"""

LOOP RECOVERY:
- A previous ConceptEvolve attempt repeated internal steps without changing `{_relative_path(artifact_path)}`.
- Reuse local literature/context artifacts instead of restarting the same discovery path.
- Do NOT repeat the same broad web or Semantic Scholar search if the manifest already covers it.
- Write or update `{_relative_path(artifact_path)}` directly with the best current synthesis and any uncertainty notes.
"""
    )


# ---------------------------------------------------------------------------
# Post-processing helpers (mechanical graph ops after sub-agent finishes)
# ---------------------------------------------------------------------------

def _adjacency_from_bridge(bridge: Dict[str, Any]) -> Dict[str, List[str]]:
    adjacency: Dict[str, List[str]] = defaultdict(list)
    for edge in bridge.get("edges", []) if isinstance(bridge, dict) else []:
        if not isinstance(edge, dict):
            continue
        src = edge.get("source") or edge.get("from")
        dst = edge.get("target") or edge.get("to")
        if isinstance(src, str) and isinstance(dst, str):
            adjacency[src].append(dst)
    return dict(adjacency)


def _walk_paths(adjacency: Dict[str, List[str]], depth: int = 4, width: int = 4) -> List[List[str]]:
    paths: List[List[str]] = []

    def dfs(node: str, path: List[str], remaining: int):
        if remaining <= 0:
            paths.append(path[:])
            return
        children = adjacency.get(node, [])[:width]
        if not children:
            paths.append(path[:])
            return
        for nxt in children:
            if nxt in path:
                continue
            dfs(nxt, path + [nxt], remaining - 1)

    for root in sorted(adjacency.keys())[:25]:
        dfs(root, [root], depth)
    return paths


def _ensure_concept_folders(topic: str, cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Safety net: create any concept folders the sub-agent missed."""
    TREE_DIR.mkdir(parents=True, exist_ok=True)
    index: List[Dict[str, Any]] = []

    for idx, card in enumerate(cards, start=1):
        name = card.get("symbolic_name") or card.get("name") or f"concept_{idx:03d}"
        slug = _slug(name)
        concept_dir = TREE_DIR / f"{idx:03d}_{slug}"
        concept_dir.mkdir(parents=True, exist_ok=True)

        if not (concept_dir / "concept.json").exists():
            card.setdefault("symbolic_name", name)
            card.setdefault("generated_at", _now())
            card.setdefault("project_folder", str(concept_dir.relative_to(RESULTS_DIR.parent)))
            _write_json(concept_dir / "concept.json", card)

        if not (concept_dir / "README.md").exists():
            domains = card.get("domains") or []
            readme = [
                f"# Concept: {name}",
                "",
                f"- Topic Context: {topic}",
                f"- Domains: {', '.join(domains) if isinstance(domains, list) else ''}",
                "",
                "## Implementation Backlog",
                "- [ ] Define minimal executable artifact for this concept.",
                "- [ ] Connect this concept to at least one sibling concept in the bridge graph.",
                "- [ ] Document how this differs from the closest prior-art paper.",
                "- [ ] Add measurable experiment and result file under this folder.",
            ]
            (concept_dir / "README.md").write_text("\n".join(readme))

        index.append({
            "id": name,
            "slug": slug,
            "folder": str(concept_dir),
            "domains": card.get("domains") or [],
        })

    return index


# ---------------------------------------------------------------------------
# Prompts — the sub-agent gets real instructions, not a JSON template
# ---------------------------------------------------------------------------

_EVOLVE_PROMPT = """You are a cross-domain concept architect with access to websearch, webfetch, semantic_scholar, bash, read, write, and edit tools.

PROBLEM: {topic}

YOUR MISSION: Research this problem across multiple domains, generate cross-domain concept cards, and write all results to disk.

CONTEXT FIRST:
- If they exist, read `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/novelty_guard.json`, and `results/literature/semantic_scholar_manifest.json` before doing new research.
- Avoid repeating broad searches or concept ideas that are already documented in those files.
- Use the prior-art watchlist to identify what is already known, then search for bridges that move beyond it.

STEP 1 — RESEARCH
Use websearch and webfetch to find real papers, techniques, and approaches relevant to this problem from at least 3 different domains. Use semantic_scholar to find academic papers.
- Start with semantic_scholar search/graph on the main problem.
- Then use citations/references/recommend to branch into adjacent-but-not-identical work.
- Prefer connections that the current watchlist or manifest has not already saturated.
- Ground your concepts in real work, but do not just restate a known paper with new wording.

STEP 2 — GENERATE CONCEPT CARDS
Create at least 10 concept cards that bridge different domains. Each card should have:
- symbolic_name (snake_case)
- description (2-3 sentences)
- domains (2+ domain strings)
- mathematical_formalization (LaTeX or pseudo-math)
- analogical_connections (cross-domain analogies)
- implementation_hypothesis (concrete algorithm/code sketch)
- experiment_seed (how to test this)
- closest_prior_art (1-3 papers with title/paperId)
- novelty_claim (what is new vs. the closest prior art)
- differentiation (why this is not just a reimplementation of an existing paper)
- folder_plan (files/folders to create)

STEP 3 — BUILD SEMANTIC BRIDGE
Create a graph connecting your concepts:
- nodes: [{{"id": "concept_name", "domain": "domain"}}]
- edges: [{{"source": "a", "target": "b", "relation": "how they connect"}}]
- bridge_chains: paths through the graph that cross domain boundaries

STEP 4 — INTROSPECT
Generate:
- associations: free-association expansions
- blind_spots: what you might be missing
- anomaly_results: what happens when you inject unexpected constraints

STEP 5 — STEERING DIRECTIONS
Produce at least 3 steering directions, each with:
- direction, rationale, first_step, expected_signal

STEP 6 — WRITE FILES
Use bash (mkdir -p) and write tools to create:

{results_dir}/concept_cards.json         — JSON array of concept cards
{results_dir}/semantic_bridge.json       — JSON object with nodes, edges, bridge_chains
{results_dir}/introspection.json         — JSON object with associations, blind_spots, anomaly_results
{results_dir}/steering_directions.json   — JSON array of steering direction objects

For EACH concept card, create a folder under {tree_dir}/ named NNN_slug (e.g. 001_information_bottleneck/) containing:
  - concept.json   (the card data)
  - README.md      (topic context + implementation backlog)
  - literature.json (papers found via semantic_scholar or websearch — array of objects)

All JSON files must be valid JSON. No markdown fences inside .json files.
Create directories before writing files: mkdir -p {results_dir} {tree_dir}
"""

_PROBE_PROMPT = """You are a concept probing agent with access to websearch, webfetch, semantic_scholar, bash, read, write, and edit tools.

BOTTLENECK TO PROBE: {problem}

YOUR MISSION: Perform a deep concept probe on this specific bottleneck. Research it, think about it from multiple angles, and write your analysis to disk.

CONTEXT FIRST:
- If present, read `results/research_context.md`, `results/literature/prior_art_watchlist.md`, and `results/literature/semantic_scholar_manifest.json`.
- Reuse promising seed papers from the manifest instead of blindly repeating earlier searches.

STEP 1 — RESEARCH
Use websearch and semantic_scholar to find relevant work on this bottleneck. Look for solutions from adjacent fields.
- Prefer citations/references/recommend paths from papers already identified as close prior art.
- Explicitly target underexplored connections, not just the most obvious neighboring paper.

STEP 2 — ANALYZE
Generate:
- associations: free-association expansions from this bottleneck
- forced_bridges: objects with "from", "to", "mechanism" — force connections to distant domains
- anomaly_results: what happens under unusual constraints
- steering_directions: objects with "direction", "rationale", "first_step", "expected_signal"
- validation_checks: how to verify each direction works

STEP 3 — WRITE RESULTS
Write a single file:
{results_dir}/probe_result.json

The file must be valid JSON with keys: associations, forced_bridges, anomaly_results, steering_directions, validation_checks.
Create the directory first: mkdir -p {results_dir}
"""

_REFRAME_PROMPT = """You are a domain-reframing agent with access to websearch, webfetch, semantic_scholar, bash, read, write, and edit tools.

PROBLEM TO REFRAME: {problem}

YOUR MISSION: Reframe this problem in at least 8 distinct domains. Research each domain to make the reframings concrete, then write results to disk.

CONTEXT FIRST:
- If present, read `results/research_context.md`, `results/literature/prior_art_watchlist.md`, and `results/literature/semantic_scholar_manifest.json`.
- Push toward domains that are underrepresented in the existing literature snapshot instead of staying near the obvious core domain.

For each reframing, include:
- domain
- reframing (how this problem looks in that domain)
- key_insight (what the domain reveals)
- suggested_technique (a concrete technique from that domain)
- mapping_back (how the technique maps back to the original problem)
- candidate_folder_name (snake_case folder name for this framing)

Use websearch to ground each reframing in real techniques from that domain.

Write a single file:
{results_dir}/reframings.json

The file must contain a JSON object with keys "problem" (string) and "framings" (array of reframing objects).
Create the directory first: mkdir -p {results_dir}
"""

_ITERATE_PROMPT = """You are a recurrent creativity agent with access to websearch, webfetch, semantic_scholar, bash, read, write, and edit tools.

FOCUS PROBLEM: {problem}

YOUR MISSION: update the concept search using the latest validation feedback so weak bridges are retired and strong bridges are promoted.

READ FIRST IF PRESENT:
- `results/research_context.md`
- `results/concept_evolve/evolve_results.json`
- `results/concept_evolve/probe_result.json`
- `results/concept_evolve/reframings.json`
- `results/swarm/falsifier.md`
- `results/verification/novelty_report.md`
- `results/verification/benchmark_report.md`
- `results/verification/citation_audit.md`

STEP 1 — FEEDBACK DIGEST
Summarize the strongest negative signals from the falsifier / verifier artifacts.

STEP 2 — BRIDGE RE-RANKING
Produce bridge_candidates as an array of objects with:
- bridge
- novelty_signal
- validation_plan
- risk
- promotion_decision  (promote / hold / retire)

STEP 3 — DELTA
Write `concept_delta.json` with keys:
- focus
- promoted_bridges
- retired_bridges
- next_experiments
- feedback_used

STEP 4 — RECURRENT STATE
Write `recurrent_state.json` with keys:
- focus
- champion_bridge
- iteration_notes
- feedback_digest

STEP 5 — FILES
Write these files under {results_dir}:
- bridge_candidates.json
- concept_delta.json
- recurrent_state.json

All JSON must be valid JSON. Create directories first: mkdir -p {results_dir}
"""


# ---------------------------------------------------------------------------
# Public commands
# ---------------------------------------------------------------------------

def evolve(topic: str) -> Dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    cached = _load_cached_evolve(topic)
    if cached:
        print("CONCEPT EVOLUTION CACHE HIT")
        print(f"- Topic: {cached.get('topic', topic)}")
        print(f"- Reusing recent results (ttl={EVOLVE_CACHE_TTL_SECONDS}s)")
        return cached

    lock_fp = EVOLVE_LOCK_FILE.open("w")
    try:
        try:
            fcntl.flock(lock_fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            cached_while_busy = _load_cached_evolve(topic)
            if cached_while_busy:
                print("CONCEPT EVOLUTION CACHE HIT (while lock busy)")
                return cached_while_busy
            raise RuntimeError(
                "ConceptEvolve evolve already running for this workspace; skipping duplicate run"
            ) from exc

        cached_after_lock = _load_cached_evolve(topic)
        if cached_after_lock:
            print("CONCEPT EVOLUTION CACHE HIT (after lock)")
            return cached_after_lock

        prompt = _EVOLVE_PROMPT.format(
            topic=topic,
            results_dir=str(RESULTS_DIR),
            tree_dir=str(TREE_DIR),
        )
        watched_paths = [
            RESULTS_DIR / "concept_cards.json",
            RESULTS_DIR / "semantic_bridge.json",
            RESULTS_DIR / "introspection.json",
            RESULTS_DIR / "steering_directions.json",
        ]

        cards: list = []
        for attempt in range(1, 3):
            print(f"[ConceptEvolve] Sub-agent evolve attempt {attempt} for: {topic[:120]}")
            rc = _run_sub_agent(
                prompt,
                name=f"concept_evolve_a{attempt}",
                command="evolve",
                fingerprint=hashlib.sha256(_normalize_topic(topic).encode("utf-8")).hexdigest(),
                topic=topic,
                watched_paths=watched_paths,
            )
            _debug_log(f"evolve_a{attempt}_rc.txt", str(rc))

            raw_cards = _read_json(RESULTS_DIR / "concept_cards.json")
            cards = _safe_list(raw_cards)
            if cards:
                break
            print(f"[ConceptEvolve] Attempt {attempt}: no concept_cards.json produced (rc={rc})")

        if not cards:
            print("[ConceptEvolve] WARNING: sub-agent did not produce concept_cards.json")

        bridge = _read_json(RESULTS_DIR / "semantic_bridge.json")
        if not isinstance(bridge, dict):
            bridge = {}
        introspection = _read_json(RESULTS_DIR / "introspection.json")
        if not isinstance(introspection, dict):
            introspection = {}
        steering = _read_json(RESULTS_DIR / "steering_directions.json")
        if not isinstance(steering, list):
            steering = []

        index = _ensure_concept_folders(topic, cards)
        adjacency = _adjacency_from_bridge(bridge)
        paths = _walk_paths(adjacency, depth=4, width=4)

        _write_json(TREE_DIR / "index.json", index)
        _write_json(TREE_DIR / "adjacency.json", adjacency)
        _write_json(TREE_DIR / "walk_paths.json", paths)

        result = {
            "topic": topic,
            "timestamp": _now(),
            "status": "completed",
            "n_concepts": len(cards),
            "n_graph_nodes": len(bridge.get("nodes", [])) if isinstance(bridge.get("nodes"), list) else 0,
            "n_graph_edges": len(bridge.get("edges", [])) if isinstance(bridge.get("edges"), list) else 0,
            "n_steering_directions": len(steering),
            "tree": {
                "concept_folder_count": len(index),
                "walk_path_count": len(paths),
                "edge_count": sum(len(v) for v in adjacency.values()),
            },
        }
        _write_json(RESULTS_DIR / "evolve_results.json", result)

        summary_lines = [
            "CONCEPT EVOLUTION COMPLETE",
            f"- Concepts: {result['n_concepts']}",
            f"- Bridge nodes: {result['n_graph_nodes']}",
            f"- Bridge edges: {result['n_graph_edges']}",
            f"- Concept folders: {len(index)}",
            f"- Walk paths: {len(paths)}",
            "",
            "Top steering directions:",
        ]
        for item in steering[:5]:
            if isinstance(item, dict):
                summary_lines.append(f"- {item.get('direction', '')[:180]}")

        (RESULTS_DIR / "summary.txt").write_text("\n".join(summary_lines))
        print("\n".join(summary_lines))
        return result
    finally:
        try:
            fcntl.flock(lock_fp.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        lock_fp.close()


def probe(problem: str) -> Dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    fingerprint, fingerprint_context = _build_operation_fingerprint("probe", problem)
    artifact_path = RESULTS_DIR / "probe_result.json"
    cached = _load_cached_probe(problem, fingerprint)
    if cached:
        _record_cache_hit(
            "probe",
            fingerprint,
            problem,
            [artifact_path],
            "reused matching probe_result.json",
        )
        print(f"[ConceptEvolve] Reusing cached probe for: {problem[:120]}")
        return cached

    lock_fp = _operation_lock("probe", fingerprint)
    try:
        cached = _load_cached_probe(problem, fingerprint)
        if cached:
            _record_cache_hit(
                "probe",
                fingerprint,
                problem,
                [artifact_path],
                "reused probe_result.json after waiting for matching run",
            )
            print(f"[ConceptEvolve] Reusing cached probe for: {problem[:120]}")
            return cached

        prompt = _PROBE_PROMPT.format(problem=problem, results_dir=str(RESULTS_DIR))
        recovery_prompt = _with_loop_recovery_guidance(prompt, artifact_path)

        print(f"[ConceptEvolve] Starting probe for: {problem[:120]}")
        use_recovery_prompt = False
        for attempt in range(1, 3):
            print(f"[ConceptEvolve] Sub-agent probe attempt {attempt}")
            rc = _run_sub_agent(
                recovery_prompt if use_recovery_prompt else prompt,
                name=f"concept_probe_a{attempt}",
                command="probe",
                fingerprint=fingerprint,
                topic=problem,
                watched_paths=[artifact_path],
            )
            parsed = _read_json(artifact_path)
            if isinstance(parsed, dict) and parsed.get("steering_directions"):
                break
            print(f"[ConceptEvolve] Attempt {attempt}: no probe_result.json produced (rc={rc})")
            if rc == CHILD_LOOP_EXIT_CODE:
                use_recovery_prompt = True

        parsed = _read_json(artifact_path)
        if not isinstance(parsed, dict):
            parsed = {"parse_error": True}

        parsed["sub_problem"] = problem
        parsed["input_fingerprint"] = fingerprint
        parsed["input_context"] = fingerprint_context
        parsed["timestamp"] = _now()
        _write_json(artifact_path, parsed)
    finally:
        try:
            fcntl.flock(lock_fp.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        lock_fp.close()

    summary = []
    for item in (parsed.get("steering_directions") or [])[:5]:
        if isinstance(item, dict):
            summary.append(f"- {item.get('direction', '')}")
    if summary:
        print("STEERING DIRECTIONS")
        print("\n".join(summary))
    return parsed


def reframe(problem: str) -> Dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    fingerprint, fingerprint_context = _build_operation_fingerprint("reframe", problem)
    artifact_path = RESULTS_DIR / "reframings.json"
    cached = _load_cached_reframe(problem, fingerprint)
    if cached:
        _record_cache_hit(
            "reframe",
            fingerprint,
            problem,
            [artifact_path],
            "reused matching reframings.json",
        )
        print(f"[ConceptEvolve] Reusing cached reframings for: {problem[:120]}")
        return cached

    lock_fp = _operation_lock("reframe", fingerprint)
    try:
        cached = _load_cached_reframe(problem, fingerprint)
        if cached:
            _record_cache_hit(
                "reframe",
                fingerprint,
                problem,
                [artifact_path],
                "reused reframings.json after waiting for matching run",
            )
            print(f"[ConceptEvolve] Reusing cached reframings for: {problem[:120]}")
            return cached

        prompt = _REFRAME_PROMPT.format(problem=problem, results_dir=str(RESULTS_DIR))
        recovery_prompt = _with_loop_recovery_guidance(prompt, artifact_path)

        print(f"[ConceptEvolve] Starting reframe for: {problem[:120]}")
        framings: list = []
        use_recovery_prompt = False
        for attempt in range(1, 3):
            print(f"[ConceptEvolve] Sub-agent reframe attempt {attempt}")
            rc = _run_sub_agent(
                recovery_prompt if use_recovery_prompt else prompt,
                name=f"concept_reframe_a{attempt}",
                command="reframe",
                fingerprint=fingerprint,
                topic=problem,
                watched_paths=[artifact_path],
            )
            payload = _read_json(artifact_path)
            if isinstance(payload, dict):
                framings = payload.get("framings", [])
            elif isinstance(payload, list):
                framings = payload
            if framings:
                break
            print(f"[ConceptEvolve] Attempt {attempt}: no reframings.json produced (rc={rc})")
            if rc == CHILD_LOOP_EXIT_CODE:
                use_recovery_prompt = True

        result = {
            "problem": problem,
            "framings": framings,
            "timestamp": _now(),
            "input_fingerprint": fingerprint,
            "input_context": fingerprint_context,
        }
        _write_json(artifact_path, result)
        print(f"Generated {len(framings)} reframings")
        return result
    finally:
        try:
            fcntl.flock(lock_fp.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        lock_fp.close()


def iterate(problem: str) -> Dict[str, Any]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    fingerprint, fingerprint_context = _build_operation_fingerprint("iterate", problem)
    artifact_path = RESULTS_DIR / "bridge_candidates.json"
    cached = _load_cached_iterate(problem, fingerprint)
    if cached:
        _record_cache_hit(
            "iterate",
            fingerprint,
            problem,
            [artifact_path, RESULTS_DIR / "recurrent_state.json"],
            "reused matching iterate feedback state",
        )
        print(f"[ConceptEvolve] Reusing cached iteration for: {problem[:120]}")
        print(json.dumps(cached, indent=2))
        return cached

    lock_fp = _operation_lock("iterate", fingerprint)
    try:
        cached = _load_cached_iterate(problem, fingerprint)
        if cached:
            _record_cache_hit(
                "iterate",
                fingerprint,
                problem,
                [artifact_path, RESULTS_DIR / "recurrent_state.json"],
                "reused iterate feedback state after waiting for matching run",
            )
            print(f"[ConceptEvolve] Reusing cached iteration for: {problem[:120]}")
            print(json.dumps(cached, indent=2))
            return cached

        prompt = _ITERATE_PROMPT.format(problem=problem, results_dir=str(RESULTS_DIR))
        recovery_prompt = _with_loop_recovery_guidance(prompt, artifact_path)

        print(f"[ConceptEvolve] Starting recurrent iteration for: {problem[:120]}")
        candidates: list = []
        use_recovery_prompt = False
        for attempt in range(1, 3):
            print(f"[ConceptEvolve] Sub-agent iterate attempt {attempt}")
            rc = _run_sub_agent(
                recovery_prompt if use_recovery_prompt else prompt,
                name=f"concept_iterate_a{attempt}",
                command="iterate",
                fingerprint=fingerprint,
                topic=problem,
                watched_paths=[artifact_path, RESULTS_DIR / "concept_delta.json"],
            )
            payload = _read_json(artifact_path)
            if isinstance(payload, list) and payload:
                candidates = payload
                break
            print(f"[ConceptEvolve] Attempt {attempt}: no bridge_candidates.json produced (rc={rc})")
            if rc == CHILD_LOOP_EXIT_CODE:
                use_recovery_prompt = True

        recurrent_state = _read_json(RESULTS_DIR / "recurrent_state.json")
        if not isinstance(recurrent_state, dict):
            recurrent_state = {}
        concept_delta = _read_json(RESULTS_DIR / "concept_delta.json")
        if not isinstance(concept_delta, dict):
            concept_delta = {
                "focus": problem,
                "promoted_bridges": [],
                "retired_bridges": [],
                "next_experiments": [],
                "feedback_used": [],
            }

        prior_iterations = int(recurrent_state.get("iteration_count", 0) or 0)
        champion = recurrent_state.get("champion_bridge")
        if not champion and candidates:
            champion = candidates[0].get("bridge")

        feedback_material = json.dumps(
            {
                "problem": problem,
                "candidates": candidates[:5],
                "delta": concept_delta,
            },
            sort_keys=True,
        )
        recurrent_state.update(
            {
                "focus": problem,
                "iteration_count": prior_iterations + 1,
                "champion_bridge": champion,
                "last_feedback_hash": hashlib.sha256(feedback_material.encode("utf-8")).hexdigest(),
                "input_fingerprint": fingerprint,
                "input_context": fingerprint_context,
                "timestamp": _now(),
            }
        )
        _write_json(RESULTS_DIR / "recurrent_state.json", recurrent_state)
        _write_json(RESULTS_DIR / "concept_delta.json", concept_delta)

        summary = {
            "problem": problem,
            "iteration_count": recurrent_state["iteration_count"],
            "champion_bridge": recurrent_state.get("champion_bridge"),
            "promoted_bridges": len(concept_delta.get("promoted_bridges") or []),
            "retired_bridges": len(concept_delta.get("retired_bridges") or []),
            "timestamp": _now(),
            "input_fingerprint": fingerprint,
        }
        print(json.dumps(summary, indent=2))
        return summary
    finally:
        try:
            fcntl.flock(lock_fp.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        lock_fp.close()


def walk(seed: str | None, depth: int) -> Dict[str, Any]:
    walk_file = TREE_DIR / "walk_paths.json"
    index_file = TREE_DIR / "index.json"
    if not walk_file.exists():
        raise RuntimeError("No walk paths found. Run 'evolve' first.")

    paths = json.loads(walk_file.read_text())
    index = json.loads(index_file.read_text()) if index_file.exists() else []
    if not isinstance(paths, list):
        paths = []

    filtered = []
    for path in paths:
        if not isinstance(path, list):
            continue
        if seed and not any(seed.lower() in str(node).lower() for node in path):
            continue
        filtered.append(path[: max(1, depth + 1)])

    payload = {
        "timestamp": _now(),
        "seed": seed,
        "depth": depth,
        "total_paths": len(paths),
        "selected_paths": len(filtered),
        "paths": filtered[:80],
        "concept_index_size": len(index) if isinstance(index, list) else 0,
    }
    _write_json(RESULTS_DIR / "walk_session.json", payload)

    print(f"Selected {payload['selected_paths']} concept paths (from {payload['total_paths']} total)")
    for p in payload["paths"][:10]:
        print(" -> ".join(str(x) for x in p))
    return payload


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="ConceptEvolve - concept tree generation and traversal for research projects."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    evolve_p = sub.add_parser("evolve")
    evolve_p.add_argument("topic", nargs="+")

    probe_p = sub.add_parser("probe")
    probe_p.add_argument("problem", nargs="+")

    reframe_p = sub.add_parser("reframe")
    reframe_p.add_argument("problem", nargs="+")

    iterate_p = sub.add_parser("iterate")
    iterate_p.add_argument("problem", nargs="+")

    walk_p = sub.add_parser("walk")
    walk_p.add_argument("--seed", default=None)
    walk_p.add_argument("--depth", type=int, default=4)

    args = parser.parse_args()
    try:
        if args.cmd == "evolve":
            evolve(" ".join(args.topic))
        elif args.cmd == "probe":
            probe(" ".join(args.problem))
        elif args.cmd == "reframe":
            reframe(" ".join(args.problem))
        elif args.cmd == "iterate":
            iterate(" ".join(args.problem))
        elif args.cmd == "walk":
            walk(args.seed, max(1, min(args.depth, 8)))
        return 0
    except Exception as exc:
        print(f"ConceptEvolve error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Usage: concept_evolve.py <evolve|probe|reframe|iterate|walk> "topic or problem"')
        sys.exit(1)
    sys.exit(main())
