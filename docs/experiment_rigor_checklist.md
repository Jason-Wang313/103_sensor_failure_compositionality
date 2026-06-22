# Experiment Rigor Checklist

## v5 Local Evidence

- [x] Paper-specific sensor-failure-compositionality benchmark.
- [x] 6 robot task families.
- [x] 8 sensor-failure regimes.
- [x] 8 distribution/stress splits.
- [x] 15 methods including oracle and strong non-oracle baselines.
- [x] 10 random seeds.
- [x] Raw main rollout persistence: 345,600 rows.
- [x] Confidence intervals.
- [x] Pairwise seed comparisons.
- [x] Safety, damage, fault-F1, interaction-F1, missed-fault, false-isolation, latency, ECE, regret, and utility metrics.
- [x] Ablations for pairwise edges, recovery memory, disagreement, calibration, recovery action selection, active repair, false-alarm suppression, v4 rules, and Bayesian fusion.
- [x] Stress sweep over interaction, desynchronization, false-alarm, drift, and recovery-delay pressure.
- [x] Fixed-risk deployment budgets with coverage.
- [x] Failure-case table with 24 negative cases.
- [x] Generated figures and LaTeX tables.
- [x] 2026-06-22 full rerun from source.
- [x] 29-page validated PDF with bright boxed citations.

## Remaining ICLR-Main Gaps

- [ ] Real-robot validation.
- [ ] Independent high-fidelity simulator benchmark.
- [ ] Implemented learned model checkpoints.
- [ ] Implemented real competing baselines.
- [ ] External benchmark comparison.
- [ ] Deployment videos or qualitative rollouts.

Decision: strong-revise. The local evidence is serious enough to continue, but not enough to submit.
