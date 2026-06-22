# Hostile Reviewer Response

Paper: 103 Sensor Failure Compositionality

## Strongest Technical Threats

- Sensor dropout and masked-modality training already target policies that survive missing sensors.
- Multimodal manipulation-failure detectors already detect failures from robot sensory streams.
- Conformal and uncertainty-aware robot safety methods already calibrate alarms under uncertainty.
- Multimodal tactile, force, and autonomous-driving sensor-fusion systems already show robust behavior under missing or degraded modalities.
- A robust v4 composition rule set is a strong internal baseline and could make v5 look incremental if v5 does not clear hard ablations.

## ICLR Main Response

The v5 rebuild narrows the novelty boundary to compositional failure interactions: cases where single-sensor robustness, independent fault detectors, Bayesian fusion, dropout training, learned latent classifiers, mixture-of-experts routing, and v4 composition rules cannot explain the combined failure. The local benchmark supports that boundary: `risk_calibrated_sensor_composition_v5` reaches hard-aggregate success `0.79262 +/- 0.01063` versus `0.69948 +/- 0.00846` for the strongest non-oracle success reference, with lower safety violation `0.13785`, lower damage `0.05868`, interaction F1 `0.68394`, ECE `0.00206`, and utility `0.47673`.

## Remaining Hostile Review

A hostile reviewer would still be correct to reject a main-track submission today. The evidence is local and synthetic; the baselines are executable diagnostic models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator evidence.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation, calibrated real sensor-failure logs, trained checkpoints, rollout videos, and implemented learned baselines.
