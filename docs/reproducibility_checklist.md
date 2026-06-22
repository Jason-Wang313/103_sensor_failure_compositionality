# Reproducibility Checklist

## Reproduces Locally

- [x] `python -m py_compile src/run_experiment.py scripts/generate_manuscript.py scripts/validate_submission_artifacts.py`
- [x] `python src/run_experiment.py`
- [x] `python scripts/generate_manuscript.py`
- [x] `results/dataset_summary.csv`
- [x] `results/rollouts.csv`
- [x] `results/main_group_metrics.csv`
- [x] `results/main_seed_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/hard_aggregate_seed_metrics.csv`
- [x] `results/hard_aggregate_metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/ablation_rollouts.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/stress_sweep_raw.csv`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/fixed_risk_raw.csv`
- [x] `results/fixed_risk_seed_metrics.csv`
- [x] `results/fixed_risk_metrics.csv`
- [x] `results/fixed_risk_pairwise_stats.csv`
- [x] `results/failure_cases.csv`
- [x] `figures/sensor_v5_hard_success.png`
- [x] `figures/sensor_v5_diagnostics.png`
- [x] `figures/sensor_v5_safety_regret.png`
- [x] `figures/sensor_v5_stress_sweep.png`
- [x] `figures/sensor_v5_ablation.png`
- [x] `figures/sensor_v5_fixed_risk.png`
- [x] `paper/main.tex`
- [x] Canonical PDF: `C:/Users/wangz/Downloads/103.pdf`
- [x] `python scripts/validate_submission_artifacts.py`

## Does Not Yet Reproduce

- [ ] Real robot results.
- [ ] Independent high-fidelity simulator runs.
- [ ] Trained policy checkpoints.
- [ ] Real deployment videos.

This repository reproduces a v5 strong-revise evidence package, not a finished ICLR-main submission.
