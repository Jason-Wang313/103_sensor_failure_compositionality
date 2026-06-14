# Literature Map

Paper: 103 sensor_failure_compositionality

Field box: robust multimodal robot learning under sensor degradation.

Thesis: model the composition of sensor failures, not only the marginal reliability of each sensor.

## Crowded Clusters

- Sensor dropout and modality masking for robust sensorimotor policies.
- Multimodal robot manipulation failure detection and anomaly detection.
- Conformal, Bayesian, and ensemble uncertainty monitoring for safe intervention.
- Tactile/vision/proprioception fusion for contact-rich manipulation.
- Autonomous-driving sensor fusion under camera/LiDAR degradation.

## Boundary

The paper's boundary is higher-order failure interaction. A single-sensor dropout method may learn marginal robustness; an independent detector may identify a broken modality; a Bayesian monitor may gate uncertainty. The proposed mechanism asks whether two or more individually survivable failures interact into a different recovery problem.

## Local Evidence

The v4 benchmark supports the boundary under combined stress: proposed success is `0.607 +/- 0.006` versus `0.544 +/- 0.006` for the strongest non-oracle baseline, and interaction F1 improves from `0.267` for independent fault detectors to `0.560`.

## Remaining Gap

The literature boundary is credible enough for strong revise, but not for submission. The next version needs external robot/high-fidelity experiments and implemented learned baselines.
