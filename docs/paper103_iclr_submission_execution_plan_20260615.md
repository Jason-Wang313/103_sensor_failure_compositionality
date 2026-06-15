# Paper 103 ICLR Submission-Readiness Execution Plan

Started: 2026-06-15 16:03:29 +0100

## Objective

Re-audit Paper 103 end to end under the continuation standard before moving to Paper 104. The paper can remain `STRONG_REVISE` only if the rerun evidence reproduces the claimed local gains and survives the success, safety, diagnostic, paired-seed, stress, and ablation gates. It still must not be labeled ICLR-main-ready without real robot or independent high-fidelity benchmark validation.

## Current State

- Repo: `103_sensor_failure_compositionality`
- Prior terminal decision: `STRONG_REVISE`
- Prior hardening version: `v4`
- Canonical PDF target: `C:/Users/wangz/Downloads/103.pdf`
- GitHub: `https://github.com/Jason-Wang313/103_sensor_failure_compositionality`
- Prior strongest non-oracle baseline: `bayesian_sensor_fusion_monitor`
- Prior combined-stress evidence: proposed success about `0.607 +/- 0.006` vs `0.544 +/- 0.006` for the strongest non-oracle baseline.
- Known readiness blocker: no real robot, external high-fidelity simulator, trained learned-baseline, or external benchmark validation.

## Evidence Gates

Keep `STRONG_REVISE` only if all local gates pass on a clean rerun:

1. `python -m py_compile src/run_experiment.py` succeeds.
2. `python src/run_experiment.py` regenerates all result CSVs, tables, and figures from source.
3. CSV outputs are finite, nonempty, and cover the declared design: 5 tasks, 7 sensor-failure families, 5 splits, 9 methods, 7 seeds, stress sweep, ablations, and failure cases.
4. `proposed_sensor_failure_composition_model` beats the strongest non-oracle baseline on combined-stress success by a meaningful margin.
5. The proposed method improves safety violation or damage rather than only improving diagnostics.
6. The proposed method improves interaction-detection F1 or recovery latency over independent fault detectors.
7. Paired seed statistics support the claim against the strongest baseline.
8. Core ablations remain below the full method.
9. Stress sweep does not reveal collapse at high multi-sensor interaction intensity.
10. The paper, README, and audit docs state the actual decision honestly, including missing real robot/external validation.
11. The PDF builds cleanly and is copied only to `C:/Users/wangz/Downloads/103.pdf`.
12. No `103.pdf` is placed on the visible Desktop.
13. The child repo is committed, pushed, clean, and public.
14. Root ledgers are updated only after child repo and PDF checks pass.

If any core local gate fails, downgrade to `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Re-run the Paper 103 benchmark from source with controlled thread env vars.
2. Audit coverage, strongest baseline, pairwise statistics, ablations, stress sweep, diagnostics, and failure cases directly from regenerated CSVs.
3. Decide honestly:
   - `STRONG_REVISE` if all local evidence gates pass, while still marking ICLR-main-ready as `no`.
   - `KILL_ARCHIVE` if the local success/safety/diagnostic/ablation evidence fails.
4. Update child docs to v4.1 with exact rerun evidence.
5. Update `paper/main.tex` only to match the verified evidence; do not inflate claims.
6. Rebuild LaTeX, scan logs, copy `103.pdf` to Downloads, hash it, and verify Desktop exclusion.
7. Commit and push the child repo; verify local/remote SHA match and public GitHub visibility.
8. Update the root reports through Paper 103.

## Expected Outcome Before Rerun

The expected outcome is likely `STRONG_REVISE`, because the existing v4 evidence shows a meaningful local gain over `bayesian_sensor_fusion_monitor` and supportive ablations. That expectation is not a conclusion; the rerun decides.
