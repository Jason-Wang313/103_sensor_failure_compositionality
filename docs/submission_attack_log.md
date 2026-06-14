# Submission Attack Log

Paper: 103 sensor_failure_compositionality

This v4 pass rebuilds the archive into a paper-specific local evidence package. The result is `STRONG_REVISE`, not submit-as-is.

## Attack 1: The result could be sensor dropout under a new name.

Response: The benchmark includes a `sensor_dropout_augmentation` baseline. Under combined stress, it reaches `0.438 +/- 0.006` success, far below the proposed `0.607 +/- 0.006`.

## Attack 2: Independent fault detectors may be enough.

Response: `independent_fault_detectors` reaches `0.502 +/- 0.006` success and interaction F1 `0.267`; proposed reaches `0.607 +/- 0.006` and interaction F1 `0.560`.

## Attack 3: Bayesian fusion may already capture cross-sensor structure.

Response: `bayesian_sensor_fusion_monitor` is the strongest non-oracle baseline at `0.544 +/- 0.006`. Proposed improves combined-stress success by `0.063 +/- 0.009` and wins `7/7` paired seeds.

## Attack 4: The method may trade success for safety.

Response: Proposed has lower safety violation (`0.196` vs `0.235`) and lower damage (`0.134` vs `0.159`) than the strongest non-oracle baseline.

## Attack 5: A single component may carry the whole result.

Response: The best removed-component ablation is `minus_conformal_gating` at `0.588 +/- 0.003`, still below the full model at `0.608 +/- 0.009`. Removing pairwise edges drops interaction F1 to `0.414`; removing cross-modal disagreement drops it to `0.403`.

## Attack 6: The claimed mechanism may fail under high interaction intensity.

Response: The stress sweep is included in `results/stress_sweep.csv` and `figures/sensor_failure_stress_sweep.png`. Proposed remains above non-oracle baselines across the generated multi-sensor interaction stress sweep, while the oracle remains higher.

## Attack 7: The evaluation is still not real robotics evidence.

Response: Correct. The terminal decision is `STRONG_REVISE`, not ICLR-ready. The manuscript explicitly states that real robot or independent high-fidelity simulator validation is required before submission.

## Attack 8: Tables and figures could be stale from v3.

Response: The v4 runner deletes obsolete v3 files (`raw_seed_metrics.csv`, `negative_cases.csv`, and `figures/stress_curve_data.csv`) before generating the new outputs. Current CSVs passed a finite-value audit.

## Attack 9: The benchmark might be too narrow.

Response: The local benchmark spans 5 tasks, 7 failure families, 5 splits, 9 methods, 7 seeds, and 84 episodes/group. This is adequate for a strong-revise local evidence package but not enough to replace external validation.

## Attack 10: Can this be submitted now?

Response: No. The correct action is strong revise with external robot/high-fidelity experiments and implemented learned baselines.
