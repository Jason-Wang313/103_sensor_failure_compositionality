# 103 Sensor Failure Compositionality

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for ICLR main conference.

The rebuilt evidence package tests whether sensor failures compose predictably or produce non-additive collapse in multimodal robot policies. The 2026-06-15 continuation rerun supports the mechanism, but the paper is not yet ICLR-main-ready because it still lacks real-robot or independent high-fidelity simulator validation.

## Evidence Snapshot

- Benchmark: 5 tasks x 7 sensor-failure families x 5 splits x 9 methods.
- Repeats: 7 seeds, 84 episodes per task/family/split/method group.
- Strongest non-oracle baseline: `bayesian_sensor_fusion_monitor`.
- Continuation rerun: `python -m py_compile src/run_experiment.py` and `python src/run_experiment.py` passed on 2026-06-15.
- Combined-stress success: proposed `0.6071 +/- 0.0055`, strongest non-oracle `0.5441 +/- 0.0064`.
- Safety: proposed violation `0.1960` vs `0.2345`, damage `0.1342` vs `0.1594`.
- Interaction diagnostics: proposed interaction F1 `0.5596` vs independent detectors `0.2675`.
- Pairwise seeds: proposed beats strongest non-oracle baseline in `7/7` seeds.
- Terminal gate: `STRONG_REVISE`, not submit-as-is.

## Reproduce

```powershell
python -m py_compile src\run_experiment.py
python src\run_experiment.py
```

Key outputs are in `results/` and `figures/`.

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/103.pdf`
