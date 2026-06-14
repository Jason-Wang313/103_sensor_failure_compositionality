# Hostile Reviewer Response

Paper: 103 Sensor Failure Compositionality

## Strongest Technical Threats

- Sensor dropout and masked-modality training already target policies that survive missing sensors.
- Multimodal manipulation-failure detectors such as FINO-Net already detect failures from robot sensory streams.
- Conformal and uncertainty-aware robot safety methods already calibrate alarms under uncertainty.
- Multi-modal tactile and autonomous-driving sensor-fusion systems already show robust behavior under missing or degraded modalities.

## ICLR Main Response

The v4 rebuild narrows the novelty boundary to compositional failure interactions: cases where single-sensor robustness or independent fault detectors cannot explain the combined failure. The local benchmark supports that boundary: proposed combined-stress success is `0.607 +/- 0.006` versus `0.544 +/- 0.006` for the strongest non-oracle baseline, with lower safety violation and damage.

## Remaining Hostile Review

A hostile reviewer would still be correct to reject a main-track submission today. The evidence is local and synthetic; the baselines are executable diagnostic models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator evidence.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation and implemented learned baselines.
