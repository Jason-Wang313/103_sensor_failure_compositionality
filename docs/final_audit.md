# Final Audit

1. Chosen thesis: robots should model when individual sensor failures compose benignly and when combined failures create non-additive policy collapse.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v5-expanded.
4. Evidence: 6 tasks x 8 sensor-failure regimes x 8 splits x 15 methods, 10 seeds, 6 episodes per cell.
5. Raw evidence: 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts, 24 negative cases.
6. Strongest non-oracle success baseline: `proposed_sensor_failure_composition_v4`.
7. Main result: v5 hard success `0.79262 +/- 0.01063` vs strongest non-oracle `0.69948 +/- 0.00846`.
8. Safety result: v5 safety violation `0.13785` and damage `0.05868`.
9. Diagnostic result: v5 interaction F1 `0.68394`, missed-fault rate `0.09913`, false-isolation rate `0.00530`, ECE `0.00206`.
10. Utility result: v5 utility `0.47673` vs `0.25851` for the strongest non-oracle reference.
11. Fixed-risk result: strict v5 coverage `0.54896`, success `0.42153`, safety `0.02222`, damage `0.00833`, utility `0.23085`.
12. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
13. Exact Downloads PDF path: `C:/Users/wangz/Downloads/103.pdf`.
14. Final PDF: 29 pages, SHA256 `D63730CDB03544C6ABF6F5453B41C91A472CE94EBDBF964D841F215EB7319E83`.
15. GitHub URL: https://github.com/Jason-Wang313/103_sensor_failure_compositionality
16. Confirmation: no visible Desktop copy was requested or made.
