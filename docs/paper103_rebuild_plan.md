# Paper 103 Rebuild Plan: Sensor Failure Compositionality

Started: 2026-06-14 23:34:00 +0100

## Goal

Rebuild Paper 103 from a template archive into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is that a robot can model when individual sensor failures compose predictably and when combined failures create catastrophic, non-additive policy errors.

## Claimed Mechanism

The proposed method, `proposed_sensor_failure_composition_model`, maintains a compositional failure graph over:

- vision dropout/blur/miscalibration;
- tactile dead zones and saturation;
- proprioceptive bias;
- force-torque drift;
- depth holes and scale error;
- language/instruction grounding noise;
- cross-modal disagreement patterns.

It should predict and mitigate higher-order failure interactions rather than treating each sensor failure independently.

## Benchmark To Build

Create a RAM-light executable benchmark with aggregate metrics rather than full trajectory storage. The benchmark will cover:

- 5 tasks: grasp selection, insertion/alignment, deformable object handling, mobile manipulation near obstacles, and tool-use contact control.
- 7 failure families: vision-only, tactile-only, proprioception-only, force-torque-only, depth-only, language-grounding-only, and compositional multi-sensor interaction.
- 5 splits: nominal, single-sensor shift, paired-sensor shift, delayed sensor recovery, and combined stress.
- 9 methods: nominal multimodal policy, sensor dropout augmentation, independent fault detectors, ensemble uncertainty gating, conformal sensor reliability filter, Bayesian sensor-fusion monitor, robust single-worst-sensor policy, proposed compositional failure model, and oracle failure-aware policy.
- 7 random seeds with independent task/family episodes.

## Evidence Requirements

The rebuild must produce:

- Task success, safety violation, damage, fault-detection F1, interaction-detection F1, false isolation rate, recovery latency, cost, and regret.
- Per-task/per-family breakdowns.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over multi-sensor interaction intensity.
- Ablations for pairwise interaction edges, temporal recovery memory, cross-modal disagreement, conformal gating, and recovery action selection.
- Failure cases explaining where compositional modeling is unnecessary, late, or dominated by robust single-sensor baselines.
- Figures and LaTeX tables generated from CSVs.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined-stress success by a meaningful margin.
- Reduces safety violations or damage rather than only improving fault diagnostics.
- Improves interaction-detection F1 or recovery latency over independent fault detectors.
- Wins paired seed comparisons against the strongest baseline.
- Survives core ablations: removing interaction edges, cross-modal disagreement, temporal recovery memory, conformal gating, or recovery action selection must not match the full method.
- States clearly that real robot/external benchmark validation is still missing.

Otherwise mark `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Replace the shared probability script with a paper-specific sensor-failure-compositionality benchmark.
2. Generate metrics, seed metrics, per-task/per-family tables, pairwise tests, stress sweep, ablations, failure cases, figures, and LaTeX tables.
3. Update repository docs to reflect the actual terminal gate.
4. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative archive report.
5. Compile and copy only `103.pdf` to `C:/Users/wangz/Downloads/103.pdf`.
6. Verify finite CSVs, py_compile, LaTeX log, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized or aggregate group simulation and write summary tables directly. Keep all seeds, tasks, families, methods, stress levels, ablations, and failure cases; do not reduce experimental coverage to save memory.
