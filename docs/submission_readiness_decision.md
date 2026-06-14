# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v4 rebuild provides a paper-specific local benchmark, strong synthetic baselines, ablations, pairwise seed comparisons, stress sweeps, failure cases, finite CSV artifacts, and generated figures/tables. The evidence supports the mechanism: on combined stress, the proposed sensor-failure composition model reaches `0.607 +/- 0.006` success versus `0.544 +/- 0.006` for the strongest non-oracle baseline, with lower safety violation and damage rates.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, and external benchmark evidence.
