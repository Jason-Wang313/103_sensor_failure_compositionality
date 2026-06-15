# Submission Readiness Audit v4.1

Audit date: 2026-06-15 16:09:46 +0100

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

## Commands Executed

- `python -m py_compile src/run_experiment.py`
- `python src/run_experiment.py`

Continuation rerun log:

- `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/103_sensor_failure_compositionality_continuation_rerun_20260615.log`

## Regenerated Evidence Coverage

- `metrics.csv`: 45 rows.
- `per_task_family_metrics.csv`: 1575 rows.
- `seed_task_family_metrics.csv`: 11025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_family_seed_metrics.csv`: 1715 rows.
- `stress_sweep.csv`: 54 rows.
- `stress_sweep_seed_metrics.csv`: 378 rows.
- `failure_cases.csv`: 8 rows.

Coverage remained the declared design: 5 tasks, 7 sensor-failure families, 5 splits, 9 methods, and 7 seeds.

## Main Gate Evidence

Strongest non-oracle baseline: `bayesian_sensor_fusion_monitor`.

Combined-stress metrics:

- Proposed success: `0.6071 +/- 0.0055`.
- Strongest baseline success: `0.5441 +/- 0.0064`.
- Success margin: `+0.0631 +/- 0.0088`.
- Proposed safety violation: `0.1960` vs `0.2345` baseline.
- Proposed damage: `0.1342` vs `0.1594` baseline.
- Proposed interaction F1: `0.5596` vs `0.3705` baseline.
- Proposed recovery latency: `0.6202` vs `0.7665` baseline.
- Proposed regret to oracle: `0.1297` vs `0.1928` baseline.

Paired seed comparison against `bayesian_sensor_fusion_monitor`:

- Success difference: `0.0631 +/- 0.0088`.
- Wins: `7/7`.

## Ablation Gate

- Full method success: `0.6082 +/- 0.0091`.
- Best removed-component ablation: `minus_conformal_gating`.
- Best removed-component success: `0.5876 +/- 0.0030`.
- Ablation margin: `+0.0206`.

The ablation gate passes locally, but the margin is still narrow enough that external validation is required before submission.

## Stress Sweep

The proposed method remains above the strongest non-oracle baseline across the generated multi-sensor interaction stress sweep. At maximum stress level `1.0`, proposed success is `0.5987 +/- 0.0084` vs `0.5281 +/- 0.0054` for `bayesian_sensor_fusion_monitor`, with lower violation and damage.

## Terminal Decision

Keep `STRONG_REVISE`. The local evidence supports the sensor-failure-compositionality mechanism, but this is not ICLR-main-ready without real robot, external high-fidelity simulator, implemented learned-baseline, or external benchmark evidence.

## PDF Verification

- Canonical PDF: `C:/Users/wangz/Downloads/103.pdf`.
- SHA256: `F37A503FD776D95D59C71C6CD3A70C48B14539BDB2A6CACE426C141281B6606E`.
- Size: `694313` bytes.
- Desktop copy: absent.
- LaTeX/BibTeX scan: no actionable warnings; only harmless `rerunfilecheck` package text and BibTeX built-in statistics appeared.
