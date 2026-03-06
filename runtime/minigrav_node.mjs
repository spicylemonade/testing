#!/usr/bin/env node

import fs from "node:fs"
import path from "node:path"
import process from "node:process"

function loadScenario(filePath) {
  const payload = JSON.parse(fs.readFileSync(filePath, "utf8"))
  const dt = Number(payload.dt)
  const steps = payload.steps ? Number(payload.steps) : Math.round(Number(payload.duration) / dt)
  return {
    scenario_id: payload.scenario_id,
    dt,
    steps,
    gravitational_constant: Number(payload.gravitational_constant),
    ids: payload.bodies.map((body) => body.id),
    masses: payload.bodies.map((body) => Number(body.mass)),
    radii: payload.bodies.map((body) => Number(body.radius || 0)),
    positions: payload.bodies.map((body) => body.position.map(Number)),
    velocities: payload.bodies.map((body) => body.velocity.map(Number)),
  }
}

function cloneMatrix(matrix) {
  return matrix.map((row) => row.slice())
}

function computeForces(state, gravitationalConstant) {
  const n = state.ids.length
  const accelerations = Array.from({ length: n }, () => [0, 0, 0])
  let potential = 0
  let minDistance = Number.POSITIVE_INFINITY
  for (let i = 0; i < n - 1; i += 1) {
    for (let j = i + 1; j < n; j += 1) {
      const dx = state.positions[j][0] - state.positions[i][0]
      const dy = state.positions[j][1] - state.positions[i][1]
      const dz = state.positions[j][2] - state.positions[i][2]
      const distSq = dx * dx + dy * dy + dz * dz
      minDistance = Math.min(minDistance, Math.sqrt(distSq))
      const invDist = 1 / Math.sqrt(distSq)
      const invDistCubed = invDist / distSq
      const scale = gravitationalConstant * invDistCubed
      accelerations[i][0] += state.masses[j] * dx * scale
      accelerations[i][1] += state.masses[j] * dy * scale
      accelerations[i][2] += state.masses[j] * dz * scale
      accelerations[j][0] -= state.masses[i] * dx * scale
      accelerations[j][1] -= state.masses[i] * dy * scale
      accelerations[j][2] -= state.masses[i] * dz * scale
      potential -= gravitationalConstant * state.masses[i] * state.masses[j] * invDist
    }
  }
  return { accelerations, potential, minDistance }
}

function invariants(state, forceReport) {
  let kinetic = 0
  let lx = 0
  let ly = 0
  let lz = 0
  let comX = 0
  let comY = 0
  let comZ = 0
  let comVx = 0
  let comVy = 0
  let comVz = 0
  let totalMass = 0
  for (let i = 0; i < state.ids.length; i += 1) {
    const m = state.masses[i]
    const [x, y, z] = state.positions[i]
    const [vx, vy, vz] = state.velocities[i]
    kinetic += 0.5 * m * (vx * vx + vy * vy + vz * vz)
    lx += m * (y * vz - z * vy)
    ly += m * (z * vx - x * vz)
    lz += m * (x * vy - y * vx)
    comX += m * x
    comY += m * y
    comZ += m * z
    comVx += m * vx
    comVy += m * vy
    comVz += m * vz
    totalMass += m
  }
  return {
    totalEnergy: kinetic + forceReport.potential,
    angularMomentumNorm: Math.sqrt(lx * lx + ly * ly + lz * lz),
    centerOfMass: [comX / totalMass, comY / totalMass, comZ / totalMass],
    centerOfMassVelocity: [comVx / totalMass, comVy / totalMass, comVz / totalMass],
  }
}

function relativeError(value, reference) {
  const scale = Math.max(Math.abs(reference), 1e-12)
  return Math.abs(value - reference) / scale
}

function stepLeapfrog(state, dt, gravitationalConstant) {
  const startForce = computeForces(state, gravitationalConstant)
  const halfVelocity = state.velocities.map((vector, index) => [
    vector[0] + 0.5 * dt * startForce.accelerations[index][0],
    vector[1] + 0.5 * dt * startForce.accelerations[index][1],
    vector[2] + 0.5 * dt * startForce.accelerations[index][2],
  ])
  const driftedPositions = state.positions.map((vector, index) => [
    vector[0] + dt * halfVelocity[index][0],
    vector[1] + dt * halfVelocity[index][1],
    vector[2] + dt * halfVelocity[index][2],
  ])
  const driftedState = { ...state, positions: driftedPositions, velocities: halfVelocity }
  const endForce = computeForces(driftedState, gravitationalConstant)
  const nextVelocities = halfVelocity.map((vector, index) => [
    vector[0] + 0.5 * dt * endForce.accelerations[index][0],
    vector[1] + 0.5 * dt * endForce.accelerations[index][1],
    vector[2] + 0.5 * dt * endForce.accelerations[index][2],
  ])
  return {
    state: { ...state, positions: driftedPositions, velocities: nextVelocities },
    force: endForce,
  }
}

function runScenario(config, sampleEvery) {
  let state = {
    ids: config.ids.slice(),
    masses: config.masses.slice(),
    radii: config.radii.slice(),
    positions: cloneMatrix(config.positions),
    velocities: cloneMatrix(config.velocities),
  }
  let force = computeForces(state, config.gravitational_constant)
  const initial = invariants(state, force)
  const diagnostics = []
  const startedAt = performance.now()
  for (let step = 0; step <= config.steps; step += 1) {
    if (step % sampleEvery === 0 || step === config.steps) {
      const snapshot = invariants(state, force)
      diagnostics.push({
        time: step * config.dt,
        positions: cloneMatrix(state.positions),
        velocities: cloneMatrix(state.velocities),
        energy_rel_drift: relativeError(snapshot.totalEnergy, initial.totalEnergy),
        angular_momentum_rel_drift: relativeError(snapshot.angularMomentumNorm, initial.angularMomentumNorm),
        center_of_mass_abs_drift: Math.hypot(
          snapshot.centerOfMass[0] - initial.centerOfMass[0],
          snapshot.centerOfMass[1] - initial.centerOfMass[1],
          snapshot.centerOfMass[2] - initial.centerOfMass[2]
        ),
      })
    }
    if (step === config.steps) {
      break
    }
    const next = stepLeapfrog(state, config.dt, config.gravitational_constant)
    state = next.state
    force = next.force
  }
  const runtimeSeconds = (performance.now() - startedAt) / 1000
  return {
    metadata: {
      scenario_id: config.scenario_id,
      dt: config.dt,
      integrator: "node_leapfrog_kdk",
      runtime_seconds: runtimeSeconds,
    },
    diagnostics,
  }
}

const scenarioPath = process.argv[2]
const outPath = process.argv[3]
const sampleEvery = Number(process.argv[4] || 1)
if (!scenarioPath || !outPath) {
  console.error("usage: node runtime/minigrav_node.mjs <scenario.json> <output.json> [sampleEvery]")
  process.exit(1)
}

const config = loadScenario(path.resolve(scenarioPath))
const result = runScenario(config, sampleEvery)
fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true })
fs.writeFileSync(path.resolve(outPath), JSON.stringify(result, null, 2) + "\n")
