# Final Audit

1. Chosen thesis: robots should model when individual sensor failures compose benignly and when combined failures create non-additive policy collapse.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v4.1.
4. Evidence: 5 tasks x 7 sensor-failure families x 5 splits x 9 methods, 7 seeds, 84 episodes/group.
5. Strongest non-oracle baseline: `bayesian_sensor_fusion_monitor`.
6. Main result: proposed combined-stress success `0.6071 +/- 0.0055` vs strongest non-oracle `0.5441 +/- 0.0064`.
7. Safety result: proposed safety violation `0.1960` and damage `0.1342` vs baseline `0.2345` and `0.1594`.
8. Diagnostic result: proposed interaction F1 `0.5596` vs independent detector `0.2675`; recovery latency `0.6202` vs `0.8596`.
9. Ablation result: full model `0.6082 +/- 0.0091`; best removed component `minus_conformal_gating` at `0.5876 +/- 0.0030`.
10. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
11. Exact Downloads PDF path: `C:/Users/wangz/Downloads/103.pdf`.
12. GitHub URL: https://github.com/Jason-Wang313/103_sensor_failure_compositionality
13. Confirmation: no visible Desktop copy was requested or made.
14. Continuation log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/103_sensor_failure_compositionality_continuation_rerun_20260615.log`.
