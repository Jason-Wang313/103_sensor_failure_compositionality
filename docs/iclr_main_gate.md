# ICLR Main Gate

Paper: 103 sensor_failure_compositionality

Previous v3 decision: KILL_ARCHIVE

v4 gate verdict: STRONG_REVISE

Evidence digest: 5 tasks x 7 failure families x 5 splits x 9 methods x 7 seeds x 84 episodes/group.

Gate outcomes:

- Success gate: pass. Proposed combined-stress success exceeds the strongest non-oracle baseline by `0.063`.
- Safety gate: pass. Safety violation and damage are lower than the strongest non-oracle baseline.
- Diagnostic gate: pass. Interaction F1 improves by `0.292` over independent fault detectors and latency improves by `0.239`.
- Pairwise gate: pass. Proposed beats the strongest non-oracle baseline in `7/7` seeds.
- Ablation gate: pass. The full model beats the best removed-component ablation by `0.0206`.

Terminal decision: STRONG_REVISE.

Submission status: not ICLR-main-ready until real robot or independent high-fidelity validation is added.
