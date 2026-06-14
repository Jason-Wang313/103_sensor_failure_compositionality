# 103 Sensor Failure Compositionality

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for ICLR main conference.

The rebuilt evidence package tests whether sensor failures compose predictably or produce non-additive collapse in multimodal robot policies. The local benchmark supports the mechanism, but the paper is not yet ICLR-main-ready because it still lacks real-robot or independent high-fidelity simulator validation.

## Evidence Snapshot

- Benchmark: 5 tasks x 7 sensor-failure families x 5 splits x 9 methods.
- Repeats: 7 seeds, 84 episodes per task/family/split/method group.
- Strongest non-oracle baseline: `bayesian_sensor_fusion_monitor`.
- Combined-stress success: proposed `0.607 +/- 0.006`, strongest non-oracle `0.544 +/- 0.006`.
- Safety: proposed violation `0.196` vs `0.235`, damage `0.134` vs `0.159`.
- Interaction diagnostics: proposed interaction F1 `0.560` vs independent detectors `0.267`.
- Pairwise seeds: proposed beats strongest non-oracle baseline in `7/7` seeds.
- Terminal gate: `STRONG_REVISE`, not submit-as-is.

## Reproduce

```powershell
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
