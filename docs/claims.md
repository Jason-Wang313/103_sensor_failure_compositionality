# Claims

- Mechanism claim: combined sensor failures can create non-additive robot-policy errors that are not captured by independent single-sensor fault models.
- Method claim: a risk-calibrated compositional failure graph over sensors, cross-modal disagreement, temporal desynchronization, drift, false-alarm pressure, and recovery actions can identify and recover from higher-order failure interactions.
- Evidence claim: in the v5 local rerun, `risk_calibrated_sensor_composition_v5` reaches hard-aggregate success `0.79262 +/- 0.01063` versus `0.69948 +/- 0.00846` for the strongest non-oracle success reference.
- Safety claim: v5 reduces safety violation to `0.13785` and damage to `0.05868` on the hard aggregate.
- Diagnostic claim: v5 reaches interaction F1 `0.68394`, missed-fault rate `0.09913`, false-isolation rate `0.00530`, and ECE `0.00206`.
- Scope claim: the evidence supports a strong-revise decision only; it does not establish real-robot deployment performance.
- Unsupported claim explicitly avoided: no claim of ICLR-main readiness or state-of-the-art robot performance.
