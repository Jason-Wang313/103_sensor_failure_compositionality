# Claims

- Mechanism claim: combined sensor failures can create non-additive robot-policy errors that are not captured by independent single-sensor fault models.
- Method claim: a compositional failure graph over sensors and cross-modal disagreements can identify and recover from higher-order failure interactions.
- Evidence claim: in the v4.1 local rerun, the proposed model beats the strongest non-oracle baseline by `0.0631 +/- 0.0088` combined-stress success and wins `7/7` paired seeds.
- Safety claim: the proposed model lowers safety violation (`0.1960` vs `0.2345`) and damage (`0.1342` vs `0.1594`) relative to the strongest non-oracle baseline.
- Scope claim: the evidence supports a strong-revise decision only; it does not establish real-robot deployment performance.
- Unsupported claim explicitly avoided: no claim of ICLR-main readiness or state-of-the-art robot performance.
