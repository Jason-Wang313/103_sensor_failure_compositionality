# Final Audit

1. Chosen thesis: robots should model when individual sensor failures compose benignly and when combined failures create non-additive policy collapse.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v4.
4. Evidence: 5 tasks x 7 sensor-failure families x 5 splits x 9 methods, 7 seeds, 84 episodes/group.
5. Strongest non-oracle baseline: `bayesian_sensor_fusion_monitor`.
6. Main result: proposed combined-stress success `0.607 +/- 0.006` vs strongest non-oracle `0.544 +/- 0.006`.
7. Safety result: proposed safety violation `0.196` and damage `0.134` vs baseline `0.235` and `0.159`.
8. Diagnostic result: proposed interaction F1 `0.560` vs independent detector `0.267`; recovery latency `0.620` vs `0.860`.
9. Ablation result: full model `0.608 +/- 0.009`; best removed component `minus_conformal_gating` at `0.588 +/- 0.003`.
10. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
11. Exact Downloads PDF path: `C:/Users/wangz/Downloads/103.pdf`.
12. GitHub URL: https://github.com/Jason-Wang313/103_sensor_failure_compositionality
13. Confirmation: no visible Desktop copy was requested or made.
