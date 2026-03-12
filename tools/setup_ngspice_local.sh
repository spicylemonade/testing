#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
pkg_dir="$repo_root/.tools/ngspice/pkg"
extract_dir="$repo_root/.tools/ngspice/extracted"
deb_path="$pkg_dir/ngspice_39.3+ds-1_amd64.deb"
deb_url="https://deb.debian.org/debian/pool/main/n/ngspice/ngspice_39.3+ds-1_amd64.deb"

mkdir -p "$pkg_dir"
if [[ ! -f "$deb_path" ]]; then
  curl -L --fail -o "$deb_path" "$deb_url"
fi

rm -rf "$extract_dir"
mkdir -p "$extract_dir"
dpkg-deb -x "$deb_path" "$extract_dir"

"$extract_dir/usr/bin/ngspice" -v
