# Paper 103 Terminal Audit

Date: 2026-06-15 16:09:46 +0100

Terminal decision: STRONG_REVISE

ICLR main ready: NO

## Verification Summary

The continuation rerun regenerated the full Paper 103 benchmark from source. The run completed with `terminal_decision=STRONG_REVISE` and `strongest_non_oracle_baseline=bayesian_sensor_fusion_monitor`.

The regenerated evidence supports the local mechanism:

- Success gate passed: proposed reached `0.6071 +/- 0.0055` combined-stress success vs `0.5441 +/- 0.0064` for `bayesian_sensor_fusion_monitor`.
- Safety gate passed: safety violation improved from `0.2345` to `0.1960`, and damage improved from `0.1594` to `0.1342`.
- Diagnostic gate passed: interaction F1 improved from `0.2675` for independent detectors to `0.5596`; recovery latency improved from `0.8596` to `0.6202`.
- Pairwise seed gate passed: `+0.0631 +/- 0.0088` with `7/7` seed wins over the strongest baseline.
- Ablation gate passed: best removed component `minus_conformal_gating` reached `0.5876` vs `0.6082` for full.
- Stress gate passed: at maximum stress level `1.0`, proposed success is `0.5987` vs `0.5281` for the strongest baseline.
- External validation gate failed: no real robot, independent high-fidelity simulator, trained learned-baseline, or external benchmark evidence is present.

## Artifact Rules

- Canonical PDF target: `C:/Users/wangz/Downloads/103.pdf`.
- Final PDF SHA256: `F37A503FD776D95D59C71C6CD3A70C48B14539BDB2A6CACE426C141281B6606E`.
- No visible Desktop PDF is permitted.
- Root ledgers must keep ICLR-main-ready as `no`.

## Final Action

Retain as a strong-revise evidence package. Do not submit this version to ICLR main.
