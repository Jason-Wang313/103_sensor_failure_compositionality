# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Added seven-seed synthetic metrics, stronger baselines, ablations, stress tests, and negative cases.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied stricter ICLR-main-conference standard.
- Marked the existing artifact `KILL_ARCHIVE` because the local evidence was template-like and underpowered.

## v4 - Paper-Specific Evidence Rebuild

- Added `docs/paper103_rebuild_plan.md`.
- Replaced the runner with a sensor-failure-compositionality benchmark.
- Generated fresh metrics, per-task/per-family tables, pairwise tests, ablations, stress sweeps, failure cases, figures, and LaTeX tables.
- Removed obsolete v3 outputs from the runner.
- Rewrote the paper as a strong-revise evidence report with honest limitations.
- Terminal decision: STRONG_REVISE.

## v4.1 - Continuation Re-Audit

- Added `docs/paper103_iclr_submission_execution_plan_20260615.md`.
- Recompiled `src/run_experiment.py` and regenerated the benchmark from source.
- Verified CSV coverage, strongest-baseline gate, pairwise seed statistics, stress sweep, ablations, failure cases, PDF rebuild path, and no-Desktop artifact rule.
- Terminal decision remains STRONG_REVISE because local evidence passes all gates, but ICLR-main readiness remains `no` without real robot or external high-fidelity validation.

## v5 - Expanded-Standard Submission Rebuild

- Added `docs/paper103_expanded_submission_plan_20260622.md`.
- Replaced the v4.1 aggregate-only runner with a streaming v5 runner.
- Expanded coverage to 6 tasks, 8 sensor-failure regimes, 8 splits, 15 methods, 10 seeds, 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts, and 24 negative cases.
- Added generated manuscript and artifact validator scripts.
- Generated a 29-page PDF with bright boxed clickable citations and 230 bibliography entries.
- Terminal decision remains STRONG_REVISE because all local empirical gates pass, but ICLR-main readiness remains `no` without real robot or external validation evidence.
