# ICLR Main Gate

Paper: 103 sensor_failure_compositionality

Previous v4.1 decision: STRONG_REVISE

v5 gate verdict: STRONG_REVISE

Evidence digest: 6 tasks x 8 sensor-failure regimes x 8 splits x 15 methods x 10 seeds x 6 episodes/cell.

Gate outcomes:

- Success gate: pass. V5 hard-aggregate success exceeds the strongest non-oracle baseline by `0.09314`.
- Safety gate: pass. V5 safety violation `0.13785` is below the strongest non-oracle reference `0.18047`.
- Damage gate: pass. V5 damage `0.05868` is below the strongest non-oracle reference `0.09010`.
- Diagnostic gate: pass. V5 interaction F1 `0.68394` improves over independent fault detectors `0.23125`.
- Calibration gate: pass. V5 ECE is `0.00206`.
- Utility gate: pass. V5 utility is `0.47673`.
- Pairwise gate: pass. V5 beats every non-oracle baseline in paired hard-seed comparisons.
- Ablation gate: pass. Full v5 beats the closest removed-component variant.
- Stress gate: pass. V5 remains above the strongest non-oracle reference at maximum stress.
- Fixed-risk gate: pass. Strict fixed-risk v5 coverage is `0.54896` and utility is `0.23085`.
- Scope gate: fail. No real robot, accepted high-fidelity benchmark, external multimodal-sensing benchmark, calibrated real sensor-failure logs, trained checkpoints, or rollout videos exist.

Terminal decision: STRONG_REVISE.

Submission status: not ICLR-main-ready until external validation is added.
