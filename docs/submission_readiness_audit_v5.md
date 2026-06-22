# Submission Readiness Audit v5

Audit date: 2026-06-22 14:55:00 +08:00

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

## Commands Executed

- `python -m py_compile src/run_experiment.py scripts/generate_manuscript.py scripts/validate_submission_artifacts.py`
- `python src/run_experiment.py`
- `python scripts/generate_manuscript.py`
- `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`
- `python scripts/validate_submission_artifacts.py`

## Regenerated Evidence Coverage

- `dataset_summary.csv`: 3,840 rows.
- `rollouts.csv`: 345,600 rows.
- `main_group_metrics.csv`: 57,600 rows.
- `main_seed_metrics.csv`: 150 rows.
- `metrics.csv`: 120 rows.
- `hard_aggregate_seed_metrics.csv`: 150 rows.
- `hard_aggregate_metrics.csv`: 15 rows.
- `pairwise_stats.csv`: 14 rows.
- `ablation_rollouts.csv`: 115,200 rows.
- `ablation_seed_metrics.csv`: 100 rows.
- `ablation_metrics.csv`: 10 rows.
- `stress_sweep_raw.csv`: 288,000 rows.
- `stress_sweep_seed_metrics.csv`: 1,000 rows.
- `stress_sweep.csv`: 100 rows.
- `fixed_risk_raw.csv`: 276,480 rows.
- `fixed_risk_seed_metrics.csv`: 480 rows.
- `fixed_risk_metrics.csv`: 48 rows.
- `fixed_risk_pairwise_stats.csv`: 44 rows.
- `failure_cases.csv`: 24 rows.

## Main Gate Evidence

Strongest non-oracle success baseline: `proposed_sensor_failure_composition_v4`.

Hard-aggregate metrics:

- V5 success: `0.79262 +/- 0.01063`.
- Strongest non-oracle success: `0.69948 +/- 0.00846`.
- V5 safety violation: `0.13785`.
- V5 damage: `0.05868`.
- V5 interaction F1: `0.68394`.
- V5 ECE: `0.00206`.
- V5 utility: `0.47673`.
- Oracle success: `0.88273`.

## Terminal Decision

Keep `STRONG_REVISE`. All frozen local empirical gates pass, but this is not ICLR-main-ready without real robot, accepted high-fidelity simulator, implemented learned-baseline, external benchmark, calibrated sensor-failure log, trained-checkpoint, or rollout-video evidence.

## PDF Verification

- Canonical PDF: `C:/Users/wangz/Downloads/103.pdf`.
- Pages: 29.
- SHA256: `D63730CDB03544C6ABF6F5453B41C91A472CE94EBDBF964D841F215EB7319E83`.
- Desktop copy: absent.
- Repo-local numbered PDF: absent.
- LaTeX/BibTeX scan: no unresolved citation or rerun warnings in the final logs.
- Visual PDF QA: pages 1, 2, 8, and 29 rendered and inspected.
