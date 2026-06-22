# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The 2026-06-22 v5 rerun provides a larger paper-specific local benchmark, strong synthetic baselines, raw rollout persistence, ablations, paired seed comparisons, stress sweeps, fixed-risk deployment budgets, failure cases, finite CSV artifacts, generated figures/tables, a 29-page PDF, and bright boxed clickable citations. The evidence supports the local mechanism: on hard aggregate splits, `risk_calibrated_sensor_composition_v5` reaches `0.79262 +/- 0.01063` success versus `0.69948 +/- 0.00846` for `proposed_sensor_failure_composition_v4`, the strongest non-oracle success reference.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, external benchmark evidence, calibrated real sensor-failure logs, trained checkpoints, and rollout videos.
