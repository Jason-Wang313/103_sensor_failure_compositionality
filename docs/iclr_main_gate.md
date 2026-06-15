# ICLR Main Gate

Paper: 103 sensor_failure_compositionality

Previous v3 decision: KILL_ARCHIVE

v4.1 gate verdict: STRONG_REVISE

Evidence digest: 5 tasks x 7 failure families x 5 splits x 9 methods x 7 seeds x 84 episodes/group.

Gate outcomes:

- Success gate: pass. Proposed combined-stress success exceeds the strongest non-oracle baseline by `0.0631 +/- 0.0088`.
- Safety gate: pass. Safety violation and damage are lower than the strongest non-oracle baseline by `0.0385` and `0.0253`.
- Diagnostic gate: pass. Interaction F1 improves by `0.2921` over independent fault detectors and latency improves by `0.2394`.
- Pairwise gate: pass. Proposed beats the strongest non-oracle baseline in `7/7` seeds.
- Ablation gate: pass. The full model beats the best removed-component ablation by `0.0206`.
- Continuation rerun gate: pass.

Terminal decision: STRONG_REVISE.

Submission status: not ICLR-main-ready until real robot or independent high-fidelity validation is added.
