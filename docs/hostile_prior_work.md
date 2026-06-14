# Hostile Prior Work

The closest threats are not generic robot-learning papers; they are methods that already make multimodal policies robust to missing sensors, detect robot failures, calibrate safety alarms, or fuse contact/perception modalities under degradation.

- Sensor Dropout trains multimodal policies to handle partial sensor failure.
- Simple masked-modality training improves sensorimotor policies under sensory failures.
- FINO-Net detects and classifies manipulation failures from multimodal robot data.
- Conformal prediction methods provide calibrated safety or uncertainty alarms in robotics.
- PolyTouch shows that stronger multimodal tactile hardware and tactile-diffusion policies improve contact-rich manipulation.
- MoME-style expert fusion in autonomous driving targets robust sensor fusion under adverse camera/LiDAR failures.

The v4 novelty boundary is therefore narrow: Paper 103 is not "add dropout" or "add uncertainty." It must show that representing cross-sensor failure interactions changes recovery decisions when combined sensor failures are worse than their single-failure parts.

Current evidence supports this boundary locally, but real robot or independent high-fidelity validation remains required.
