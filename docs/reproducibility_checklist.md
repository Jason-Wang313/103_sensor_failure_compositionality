# Reproducibility Checklist

## Reproduces Locally

- [x] `python -m py_compile src/run_experiment.py`
- [x] `python src/run_experiment.py`
- [x] `results/seed_task_family_metrics.csv`
- [x] `results/per_task_family_metrics.csv`
- [x] `results/seed_split_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/ablation_task_family_seed_metrics.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/failure_cases.csv`
- [x] `figures/sensor_failure_combined_success.png`
- [x] `figures/sensor_failure_diagnostics.png`
- [x] `figures/sensor_failure_safety_regret.png`
- [x] `figures/sensor_failure_stress_sweep.png`
- [x] `figures/sensor_failure_ablation.png`
- [x] `paper/main.tex`
- [x] Canonical PDF: `C:/Users/wangz/Downloads/103.pdf`

## Does Not Yet Reproduce

- [ ] Real robot results.
- [ ] Independent high-fidelity simulator runs.
- [ ] Trained policy checkpoints.
- [ ] Real deployment videos.

This repository reproduces a v4.1 strong-revise evidence package, not a finished ICLR-main submission.
The 2026-06-15 v4.1 continuation rerun recompiled and regenerated the same evidence package from source; log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/103_sensor_failure_compositionality_continuation_rerun_20260615.log`.
