# 103 Sensor Failure Compositionality

Submission-hardening version: v5-expanded

Terminal decision: STRONG_REVISE for ICLR main conference.

The expanded evidence package tests whether sensor failures compose predictably or produce non-additive collapse in multimodal robot policies. The 2026-06-22 v5 rebuild supports the local mechanism under a much larger hostile-review protocol, but the paper is still not ICLR-main-ready because it lacks real-robot, accepted high-fidelity, external benchmark, calibrated real sensor-failure log, trained-checkpoint, or rollout-video evidence.

## Evidence Snapshot

- Benchmark: 6 tasks x 8 sensor-failure regimes x 8 splits x 15 methods.
- Repeats: 10 seeds, 6 episodes per task/regime/split/method/seed cell.
- Main rollouts: 345,600 raw rows.
- Additional rollouts: 115,200 ablation rows, 288,000 stress rows, 276,480 fixed-risk rows.
- Strongest non-oracle success baseline: `proposed_sensor_failure_composition_v4`.
- v5 hard success: `0.79262 +/- 0.01063` vs `0.69948 +/- 0.00846` for the strongest non-oracle success reference.
- Safety: v5 violation `0.13785`, damage `0.05868`.
- Diagnostics: v5 interaction F1 `0.68394`, missed-fault rate `0.09913`, false-isolation rate `0.00530`, ECE `0.00206`.
- Utility: v5 `0.47673` vs `0.25851` for the strongest non-oracle utility reference.
- Strict fixed-risk v5: coverage `0.54896`, success `0.42153`, safety `0.02222`, damage `0.00833`, utility `0.23085`.
- Terminal gate: `STRONG_REVISE`, not submit-as-is.
- Canonical PDF: `C:/Users/wangz/Downloads/103.pdf`, 29 pages, SHA256 `D63730CDB03544C6ABF6F5453B41C91A472CE94EBDBF964D841F215EB7319E83`.

## Reproduce

```powershell
python -m py_compile src\run_experiment.py scripts\generate_manuscript.py scripts\validate_submission_artifacts.py
python src\run_experiment.py
python scripts\generate_manuscript.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf -Destination C:\Users\wangz\Downloads\103.pdf -Force
cd ..
python scripts\validate_submission_artifacts.py
```

Do not copy `103.pdf` to the visible Desktop.
