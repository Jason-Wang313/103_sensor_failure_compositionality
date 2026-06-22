# Paper 103 Expanded Submission Plan

Date: 2026-06-22

Paper: `103_sensor_failure_compositionality`

Target: rebuild from the v4.1 strong-revise artifact into a 25+ page hostile-review v5 evidence package. The goal is not to make the result pretty. The goal is to test whether the claim survives stronger baselines, larger stress coverage, ablations, fixed-risk deployment constraints, and an explicit scope gate.

## Frozen Claim

Sensor failures in multimodal robot policies are not always additive. The v5 claim is that a risk-calibrated sensor-composition model can identify and recover from higher-order failure interactions better than independent fault detectors, uncertainty gates, Bayesian fusion monitors, robust single-sensor fallback policies, learned latent failure classifiers, dropout-trained policies, and mixture-of-experts routing.

The paper must not claim ICLR-main readiness unless external robot or accepted high-fidelity validation exists. Local synthetic evidence can support only `STRONG_REVISE`.

## Frozen Design

The v5 runner will use a RAM-light streaming design with raw rollout persistence:

- 6 tasks: `grasp_selection_under_occlusion`, `insertion_alignment_contact`, `deformable_sorting`, `mobile_manip_obstacle_avoidance`, `tool_use_force_control`, `bin_picking_language_goal`.
- 8 failure regimes: `vision_dropout`, `tactile_deadzone`, `proprioceptive_bias`, `force_torque_drift`, `depth_scale_holes`, `language_grounding_noise`, `temporal_desynchronization`, `compositional_multi_sensor`.
- 8 splits: `nominal`, `single_sensor_shift`, `paired_sensor_shift`, `delayed_recovery`, `desynchronization_shift`, `false_alarm_shift`, `recovery_latency_shift`, `combined_extreme`.
- 15 methods: `nominal_multimodal_policy`, `sensor_dropout_augmentation`, `independent_fault_detectors`, `ensemble_uncertainty_gating`, `conformal_sensor_reliability_filter`, `bayesian_sensor_fusion_monitor`, `robust_single_worst_sensor_policy`, `causal_sensor_graph_monitor`, `learned_latent_failure_classifier`, `sensor_dropout_transformer_policy`, `multimodal_mixture_of_experts_router`, `risk_aware_sensor_reconfiguration`, `proposed_sensor_failure_composition_v4`, `risk_calibrated_sensor_composition_v5`, `oracle_failure_aware_policy`.
- 10 seeds.
- 6 episodes per factorial cell.

Expected main coverage:

- Dataset summaries: 3,840 rows.
- Raw main rollouts: 345,600 rows.
- Main group metrics: 57,600 rows.
- Main seed metrics: 150 rows.
- Main split metrics: 120 rows.
- Hard aggregate seed metrics: 150 rows.
- Hard aggregate metrics: 15 rows.
- Pairwise tests: 14 comparisons.

## Frozen Additional Experiments

- Ablations: full v5 plus removals of pairwise interaction edges, temporal recovery memory, cross-modal disagreement, conformal calibration, recovery action selection, active repair, risk budget, sensor desynchronization modeling, and false-alarm suppression.
- Stress sweep: interaction stress, desynchronization, calibration drift, and false-alarm pressure across 10 levels.
- Fixed-risk deployment budgets: strict risk budgets that can abstain or repair, with coverage and utility reported honestly.
- Negative cases: at least 24 generated failure/boundary cases where compositional modeling is unnecessary, late, over-cautious, or dominated by a robust baseline.

## Frozen Metrics

Primary metrics:

- Task success.
- Safety violation.
- Damage.
- Fault-detection F1.
- Interaction-detection F1.
- Missed-fault rate.
- False-isolation rate.
- Recovery latency.
- Calibration ECE.
- Regret to oracle.
- Utility.

Fixed-risk metrics:

- Coverage.
- Conditional success.
- Safety violation.
- Damage.
- False isolation.
- Missed fault.
- Recovery latency.
- Utility.

## Frozen Gates

Local `STRONG_REVISE` requires all of the following:

- v5 hard-aggregate success beats the strongest non-oracle baseline by at least 0.05.
- v5 hard-aggregate safety violation and damage are lower than the strongest non-oracle baseline.
- v5 interaction F1 improves over independent fault detectors by at least 0.15.
- v5 ECE is below 0.12.
- v5 utility beats the best non-oracle utility baseline.
- Paired seed lower bound against the strongest non-oracle baseline is positive.
- Full v5 beats every removed-component ablation on hard-aggregate success or utility.
- Maximum-stress v5 remains above the strongest non-oracle success reference.
- Strict fixed-risk deployment keeps nontrivial coverage and better utility than the strongest non-oracle fixed-risk reference.

The paper remains `not ICLR-main-ready` unless at least one accepted scope-evidence source exists:

- real robot experiments,
- an accepted high-fidelity simulator benchmark,
- an external benchmark with trained policies,
- calibrated real sensor-failure logs,
- released trained checkpoints, or
- rollout videos from a real or high-fidelity system.

## Execution Order

1. Replace the v4.1 aggregate-only runner with the frozen v5 streaming runner.
2. Run the full CPU-only experiment and keep memory bounded by streaming raw rollouts to CSV.
3. Generate all tables, figures, summary text, and negative cases from CSVs only.
4. Generate a 25+ page manuscript with bright boxed clickable citations and an explicit scope-gate decision.
5. Compile LaTeX, copy only `C:/Users/wangz/Downloads/103.pdf`, and do not place any PDF on the visible Desktop.
6. Validate row counts, finite values, PDF page count, SHA256, citation/link behavior, stale documentation, and GitHub public push.
7. Update root ledgers only after child repo, PDF, and GitHub checks pass.

## Expected Terminal Honesty

If v5 passes the local gates but lacks external validation, the terminal state is `STRONG_REVISE`, `ICLR main ready: no`.

If any local gate fails, the terminal state becomes `KILL_ARCHIVE`, even if the manuscript is 25+ pages.
