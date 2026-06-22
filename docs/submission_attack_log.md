# Submission Attack Log

Paper: 103 sensor_failure_compositionality

This v5 pass re-audits the paper-specific local evidence package. The result is `STRONG_REVISE`, not submit-as-is.

## Attack 1: The result could be sensor dropout under a new name.

Response: The benchmark includes both `sensor_dropout_augmentation` and `sensor_dropout_transformer_policy`. On the hard aggregate, they reach success `0.44852` and `0.59002`, below v5 at `0.79262`.

## Attack 2: Independent fault detectors may be enough.

Response: `independent_fault_detectors` reaches success `0.51372` and interaction F1 `0.23125`; v5 reaches success `0.79262` and interaction F1 `0.68394`.

## Attack 3: Bayesian fusion may already capture cross-sensor structure.

Response: `bayesian_sensor_fusion_monitor` reaches success `0.60677`, safety violation `0.21406`, damage `0.12083`, and utility `0.05099`. V5 reaches success `0.79262`, safety violation `0.13785`, damage `0.05868`, and utility `0.47673`.

## Attack 4: The v4 composition rule set may already solve the problem.

Response: `proposed_sensor_failure_composition_v4` is the strongest non-oracle success reference at `0.69948 +/- 0.00846`. V5 improves hard success by `0.09314`, reduces safety violation and damage, and improves utility from `0.25851` to `0.47673`.

## Attack 5: The method may trade success for safety.

Response: V5 improves both success and safety relative to the strongest non-oracle reference: safety violation is `0.13785` versus `0.18047`, and damage is `0.05868` versus `0.09010`.

## Attack 6: A single component may carry the whole result.

Response: The closest removed-component ablation is `no_false_alarm_suppression` at success `0.73863` and utility `0.36739`, below full v5 at success `0.79089` and utility `0.47612`. Removing pairwise interaction edges drops interaction F1 to `0.39887`; removing cross-modal disagreement drops interaction F1 to `0.40234`.

## Attack 7: The claimed mechanism may fail under high interaction intensity.

Response: At maximum stress, v5 reaches success `0.76389`, above the strongest non-oracle reference `0.65972`, while the oracle remains higher at `0.86597`.

## Attack 8: Fixed-risk deployment may collapse.

Response: Strict fixed-risk v5 coverage is `0.54896`, success is `0.42153`, safety violation is `0.02222`, damage is `0.00833`, and utility is `0.23085`. Coverage is reported because abstention is not counted as success.

## Attack 9: The evaluation is still not real robotics evidence.

Response: Correct. The terminal decision is `STRONG_REVISE`, not ICLR-ready. The manuscript explicitly states that real robot or independent high-fidelity simulator validation is required before submission.

## Attack 10: Can this be submitted now?

Response: No. The correct action is strong revise with external robot/high-fidelity experiments, calibrated real sensor-failure logs, trained checkpoints, rollout videos, and implemented learned baselines.
