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
