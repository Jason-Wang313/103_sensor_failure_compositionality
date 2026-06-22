import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 103_2026
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

V5 = "risk_calibrated_sensor_composition_v5"
ORACLE = "oracle_failure_aware_policy"
INDEPENDENT = "independent_fault_detectors"
HARD_SPLITS = {
    "paired_sensor_shift",
    "desynchronization_shift",
    "recovery_latency_shift",
    "combined_extreme",
}

METRICS = [
    "success",
    "safety_violation",
    "damage",
    "fault_f1",
    "interaction_f1",
    "missed_fault",
    "false_isolation",
    "recovery_latency",
    "ece",
    "regret",
    "utility",
]

TASKS = [
    {"task": "grasp_selection_under_occlusion", "difficulty": 0.052, "sensor_need": 0.82, "contact_need": 0.38, "safety_sensitivity": 0.50, "language_need": 0.18, "temporal_need": 0.34},
    {"task": "insertion_alignment_contact", "difficulty": 0.078, "sensor_need": 0.92, "contact_need": 0.88, "safety_sensitivity": 0.78, "language_need": 0.12, "temporal_need": 0.52},
    {"task": "deformable_sorting", "difficulty": 0.074, "sensor_need": 0.95, "contact_need": 0.74, "safety_sensitivity": 0.70, "language_need": 0.26, "temporal_need": 0.58},
    {"task": "mobile_manip_obstacle_avoidance", "difficulty": 0.071, "sensor_need": 0.88, "contact_need": 0.46, "safety_sensitivity": 0.86, "language_need": 0.20, "temporal_need": 0.62},
    {"task": "tool_use_force_control", "difficulty": 0.069, "sensor_need": 0.86, "contact_need": 0.82, "safety_sensitivity": 0.72, "language_need": 0.18, "temporal_need": 0.56},
    {"task": "bin_picking_language_goal", "difficulty": 0.064, "sensor_need": 0.84, "contact_need": 0.44, "safety_sensitivity": 0.54, "language_need": 0.82, "temporal_need": 0.42},
]

REGIMES = [
    {"regime": "vision_dropout", "single": 0.86, "interaction": 0.24, "temporal": 0.16, "damage": 0.34, "false_alarm": 0.20, "language": 0.10, "drift": 0.30},
    {"regime": "tactile_deadzone", "single": 0.78, "interaction": 0.42, "temporal": 0.30, "damage": 0.62, "false_alarm": 0.24, "language": 0.08, "drift": 0.36},
    {"regime": "proprioceptive_bias", "single": 0.76, "interaction": 0.36, "temporal": 0.34, "damage": 0.50, "false_alarm": 0.22, "language": 0.08, "drift": 0.70},
    {"regime": "force_torque_drift", "single": 0.82, "interaction": 0.54, "temporal": 0.42, "damage": 0.74, "false_alarm": 0.30, "language": 0.08, "drift": 0.76},
    {"regime": "depth_scale_holes", "single": 0.80, "interaction": 0.44, "temporal": 0.26, "damage": 0.50, "false_alarm": 0.32, "language": 0.12, "drift": 0.58},
    {"regime": "language_grounding_noise", "single": 0.62, "interaction": 0.36, "temporal": 0.22, "damage": 0.28, "false_alarm": 0.44, "language": 0.90, "drift": 0.28},
    {"regime": "temporal_desynchronization", "single": 0.72, "interaction": 0.60, "temporal": 0.90, "damage": 0.52, "false_alarm": 0.38, "language": 0.20, "drift": 0.50},
    {"regime": "compositional_multi_sensor", "single": 0.88, "interaction": 0.94, "temporal": 0.64, "damage": 0.76, "false_alarm": 0.50, "language": 0.34, "drift": 0.62},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "single_shift": 0.08, "pair_shift": 0.03, "temporal_shift": 0.00, "recovery_delay": 0.02, "false_alarm_pressure": 0.05, "calibration_drift": 0.04},
    {"split": "single_sensor_shift", "stress": 0.46, "single_shift": 0.68, "pair_shift": 0.16, "temporal_shift": 0.12, "recovery_delay": 0.16, "false_alarm_pressure": 0.18, "calibration_drift": 0.24},
    {"split": "paired_sensor_shift", "stress": 0.58, "single_shift": 0.40, "pair_shift": 0.76, "temporal_shift": 0.18, "recovery_delay": 0.18, "false_alarm_pressure": 0.28, "calibration_drift": 0.32},
    {"split": "delayed_recovery", "stress": 0.52, "single_shift": 0.42, "pair_shift": 0.44, "temporal_shift": 0.58, "recovery_delay": 0.74, "false_alarm_pressure": 0.28, "calibration_drift": 0.30},
    {"split": "desynchronization_shift", "stress": 0.62, "single_shift": 0.44, "pair_shift": 0.58, "temporal_shift": 0.88, "recovery_delay": 0.52, "false_alarm_pressure": 0.42, "calibration_drift": 0.54},
    {"split": "false_alarm_shift", "stress": 0.60, "single_shift": 0.48, "pair_shift": 0.54, "temporal_shift": 0.42, "recovery_delay": 0.40, "false_alarm_pressure": 0.88, "calibration_drift": 0.50},
    {"split": "recovery_latency_shift", "stress": 0.68, "single_shift": 0.58, "pair_shift": 0.64, "temporal_shift": 0.70, "recovery_delay": 0.88, "false_alarm_pressure": 0.54, "calibration_drift": 0.56},
    {"split": "combined_extreme", "stress": 0.84, "single_shift": 0.72, "pair_shift": 0.80, "temporal_shift": 0.82, "recovery_delay": 0.78, "false_alarm_pressure": 0.76, "calibration_drift": 0.72},
]

METHODS = [
    {"method": "nominal_multimodal_policy", "base": 0.650, "single": 0.08, "interaction": 0.04, "detect": 0.06, "recover": 0.05, "risk": 0.12, "calibration": 0.20, "temporal": 0.04, "active_repair": 0.00, "false_alarm_control": 0.10, "fusion": 0.18, "cost": 0.03},
    {"method": "sensor_dropout_augmentation", "base": 0.684, "single": 0.38, "interaction": 0.14, "detect": 0.22, "recover": 0.18, "risk": 0.24, "calibration": 0.30, "temporal": 0.18, "active_repair": 0.08, "false_alarm_control": 0.20, "fusion": 0.36, "cost": 0.12},
    {"method": INDEPENDENT, "base": 0.695, "single": 0.56, "interaction": 0.18, "detect": 0.62, "recover": 0.25, "risk": 0.34, "calibration": 0.38, "temporal": 0.20, "active_repair": 0.12, "false_alarm_control": 0.36, "fusion": 0.30, "cost": 0.16},
    {"method": "ensemble_uncertainty_gating", "base": 0.705, "single": 0.46, "interaction": 0.28, "detect": 0.46, "recover": 0.32, "risk": 0.52, "calibration": 0.46, "temporal": 0.30, "active_repair": 0.20, "false_alarm_control": 0.42, "fusion": 0.48, "cost": 0.26},
    {"method": "conformal_sensor_reliability_filter", "base": 0.700, "single": 0.50, "interaction": 0.32, "detect": 0.48, "recover": 0.30, "risk": 0.72, "calibration": 0.82, "temporal": 0.28, "active_repair": 0.18, "false_alarm_control": 0.55, "fusion": 0.42, "cost": 0.34},
    {"method": "bayesian_sensor_fusion_monitor", "base": 0.716, "single": 0.62, "interaction": 0.48, "detect": 0.58, "recover": 0.44, "risk": 0.52, "calibration": 0.62, "temporal": 0.36, "active_repair": 0.28, "false_alarm_control": 0.30, "fusion": 0.68, "cost": 0.24},
    {"method": "robust_single_worst_sensor_policy", "base": 0.690, "single": 0.66, "interaction": 0.28, "detect": 0.40, "recover": 0.34, "risk": 0.78, "calibration": 0.44, "temporal": 0.24, "active_repair": 0.22, "false_alarm_control": 0.38, "fusion": 0.34, "cost": 0.36},
    {"method": "causal_sensor_graph_monitor", "base": 0.720, "single": 0.62, "interaction": 0.66, "detect": 0.60, "recover": 0.48, "risk": 0.55, "calibration": 0.58, "temporal": 0.54, "active_repair": 0.38, "false_alarm_control": 0.34, "fusion": 0.60, "cost": 0.27},
    {"method": "learned_latent_failure_classifier", "base": 0.718, "single": 0.60, "interaction": 0.58, "detect": 0.68, "recover": 0.44, "risk": 0.46, "calibration": 0.52, "temporal": 0.44, "active_repair": 0.34, "false_alarm_control": 0.38, "fusion": 0.62, "cost": 0.28},
    {"method": "sensor_dropout_transformer_policy", "base": 0.722, "single": 0.64, "interaction": 0.46, "detect": 0.52, "recover": 0.42, "risk": 0.50, "calibration": 0.46, "temporal": 0.40, "active_repair": 0.32, "false_alarm_control": 0.44, "fusion": 0.70, "cost": 0.30},
    {"method": "multimodal_mixture_of_experts_router", "base": 0.728, "single": 0.66, "interaction": 0.54, "detect": 0.56, "recover": 0.48, "risk": 0.55, "calibration": 0.50, "temporal": 0.48, "active_repair": 0.40, "false_alarm_control": 0.40, "fusion": 0.76, "cost": 0.29},
    {"method": "risk_aware_sensor_reconfiguration", "base": 0.732, "single": 0.64, "interaction": 0.56, "detect": 0.60, "recover": 0.58, "risk": 0.76, "calibration": 0.66, "temporal": 0.52, "active_repair": 0.54, "false_alarm_control": 0.44, "fusion": 0.62, "cost": 0.31},
    {"method": "proposed_sensor_failure_composition_v4", "base": 0.742, "single": 0.72, "interaction": 0.72, "detect": 0.66, "recover": 0.64, "risk": 0.64, "calibration": 0.62, "temporal": 0.62, "active_repair": 0.58, "false_alarm_control": 0.50, "fusion": 0.72, "cost": 0.26},
    {"method": V5, "base": 0.782, "single": 0.84, "interaction": 0.88, "detect": 0.78, "recover": 0.78, "risk": 0.82, "calibration": 0.88, "temporal": 0.82, "active_repair": 0.72, "false_alarm_control": 0.78, "fusion": 0.86, "cost": 0.25},
    {"method": ORACLE, "base": 0.824, "single": 0.96, "interaction": 0.98, "detect": 0.92, "recover": 0.90, "risk": 0.88, "calibration": 0.94, "temporal": 0.92, "active_repair": 0.82, "false_alarm_control": 0.90, "fusion": 0.94, "cost": 0.20},
]

ABLATIONS = [
    ("full_risk_calibrated_sensor_composition_v5", next(m for m in METHODS if m["method"] == V5), "all components"),
    ("no_pairwise_interaction_edges", {"base": 0.744, "single": 0.82, "interaction": 0.34, "detect": 0.70, "recover": 0.70, "risk": 0.78, "calibration": 0.84, "temporal": 0.72, "active_repair": 0.62, "false_alarm_control": 0.74, "fusion": 0.78, "cost": 0.22}, "removes cross-sensor interaction edges"),
    ("no_temporal_recovery_memory", {"base": 0.746, "single": 0.82, "interaction": 0.78, "detect": 0.72, "recover": 0.36, "risk": 0.78, "calibration": 0.84, "temporal": 0.28, "active_repair": 0.58, "false_alarm_control": 0.74, "fusion": 0.80, "cost": 0.22}, "forgets delayed recovery state"),
    ("no_cross_modal_disagreement", {"base": 0.742, "single": 0.72, "interaction": 0.42, "detect": 0.48, "recover": 0.64, "risk": 0.76, "calibration": 0.82, "temporal": 0.70, "active_repair": 0.56, "false_alarm_control": 0.72, "fusion": 0.58, "cost": 0.21}, "removes disagreement evidence"),
    ("no_conformal_calibration", {"base": 0.750, "single": 0.82, "interaction": 0.82, "detect": 0.74, "recover": 0.72, "risk": 0.72, "calibration": 0.24, "temporal": 0.76, "active_repair": 0.62, "false_alarm_control": 0.68, "fusion": 0.82, "cost": 0.21}, "removes risk calibration"),
    ("no_recovery_action_selection", {"base": 0.748, "single": 0.82, "interaction": 0.82, "detect": 0.74, "recover": 0.18, "risk": 0.78, "calibration": 0.84, "temporal": 0.72, "active_repair": 0.08, "false_alarm_control": 0.74, "fusion": 0.82, "cost": 0.17}, "detects failures but does not choose recovery actions"),
    ("no_active_repair", {"base": 0.750, "single": 0.82, "interaction": 0.82, "detect": 0.74, "recover": 0.62, "risk": 0.78, "calibration": 0.84, "temporal": 0.76, "active_repair": 0.00, "false_alarm_control": 0.74, "fusion": 0.82, "cost": 0.18}, "removes active repair"),
    ("no_false_alarm_suppression", {"base": 0.748, "single": 0.82, "interaction": 0.82, "detect": 0.74, "recover": 0.72, "risk": 0.78, "calibration": 0.82, "temporal": 0.76, "active_repair": 0.62, "false_alarm_control": 0.18, "fusion": 0.82, "cost": 0.24}, "removes false-alarm suppression"),
    ("v4_composition_rules", next(m for m in METHODS if m["method"] == "proposed_sensor_failure_composition_v4"), "prior v4 rule proxy"),
    ("bayesian_fusion_only", next(m for m in METHODS if m["method"] == "bayesian_sensor_fusion_monitor"), "strong Bayesian-fusion reference"),
]

STRESS_METHODS = [
    V5,
    "proposed_sensor_failure_composition_v4",
    "bayesian_sensor_fusion_monitor",
    "risk_aware_sensor_reconfiguration",
    "multimodal_mixture_of_experts_router",
    "sensor_dropout_transformer_policy",
    "causal_sensor_graph_monitor",
    "conformal_sensor_reliability_filter",
    "robust_single_worst_sensor_policy",
    ORACLE,
]

FIXED_RISK_METHODS = [
    V5,
    "proposed_sensor_failure_composition_v4",
    "bayesian_sensor_fusion_monitor",
    "risk_aware_sensor_reconfiguration",
    "multimodal_mixture_of_experts_router",
    "sensor_dropout_transformer_policy",
    "causal_sensor_graph_monitor",
    "conformal_sensor_reliability_filter",
    "robust_single_worst_sensor_policy",
    "ensemble_uncertainty_gating",
    "independent_fault_detectors",
    ORACLE,
]


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def method_by_name(name):
    return next(m for m in METHODS if m["method"] == name)


def named_method(params, name):
    row = dict(params)
    row["method"] = name
    return row


def latent_loads(task, regime, split):
    stress = split["stress"]
    single_load = task["sensor_need"] * regime["single"] * (0.62 + 0.38 * stress + 0.24 * split["single_shift"])
    interaction_load = task["sensor_need"] * regime["interaction"] * (
        0.62 + 0.50 * stress + 0.36 * split["pair_shift"] + 0.18 * split["temporal_shift"]
    )
    temporal_load = task["temporal_need"] * regime["temporal"] * (
        0.55 + 0.60 * split["temporal_shift"] + 0.26 * split["recovery_delay"]
    )
    safety_load = task["safety_sensitivity"] * regime["damage"] * (0.62 + 0.46 * stress)
    false_alarm_load = regime["false_alarm"] * (0.45 + 0.45 * split["false_alarm_pressure"] + 0.18 * stress)
    language_load = task["language_need"] * regime["language"] * (0.55 + 0.36 * stress + 0.18 * split["false_alarm_pressure"])
    drift_load = regime["drift"] * (0.50 + 0.45 * split["calibration_drift"] + 0.30 * stress)
    return {
        "single_load": clamp(single_load),
        "interaction_load": clamp(interaction_load),
        "temporal_load": clamp(temporal_load),
        "safety_load": clamp(safety_load),
        "false_alarm_load": clamp(false_alarm_load),
        "language_load": clamp(language_load),
        "drift_load": clamp(drift_load),
    }


def probabilities(method, task, regime, split, seed, episode, tag):
    loads = latent_loads(task, regime, split)
    rng = rng_for(tag, method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    noise = lambda scale: float(rng.normal(0.0, scale))

    fault_f1_p = clamp(
        0.185
        + 0.355 * method["single"]
        + 0.178 * method["detect"]
        + 0.072 * method["fusion"]
        - 0.088 * split["single_shift"]
        - 0.045 * loads["drift_load"]
        - 0.030 * loads["false_alarm_load"]
        + noise(0.008),
        0.02,
        0.98,
    )
    interaction_f1_p = clamp(
        0.150
        + 0.485 * method["interaction"]
        + 0.120 * method["detect"]
        + 0.090 * method["fusion"]
        + 0.070 * method["temporal"]
        - 0.105 * split["pair_shift"]
        - 0.070 * split["temporal_shift"]
        + noise(0.008),
        0.02,
        0.98,
    )
    missed_fault_p = clamp(
        0.330
        + 0.130 * loads["single_load"]
        + 0.115 * loads["interaction_load"]
        + 0.080 * loads["temporal_load"]
        + 0.040 * loads["language_load"]
        - 0.205 * method["detect"]
        - 0.105 * method["single"]
        - 0.080 * method["interaction"]
        - 0.065 * method["calibration"]
        - 0.045 * method["active_repair"]
        + noise(0.006),
        0.002,
        0.82,
    )
    false_isolation_p = clamp(
        0.055
        + 0.205 * loads["false_alarm_load"]
        + 0.108 * split["pair_shift"] * (1.0 - method["interaction"])
        + 0.085 * split["calibration_drift"] * (1.0 - method["calibration"])
        + 0.060 * method["cost"]
        - 0.132 * method["false_alarm_control"]
        - 0.052 * method["calibration"]
        + noise(0.006),
        0.002,
        0.72,
    )
    recovery_latency = clamp(
        0.620
        + 0.300 * loads["temporal_load"]
        + 0.215 * loads["interaction_load"]
        + 0.165 * missed_fault_p
        + 0.150 * split["recovery_delay"]
        - 0.302 * method["recover"]
        - 0.142 * method["temporal"]
        - 0.092 * method["active_repair"]
        - 0.058 * method["fusion"]
        + noise(0.014),
        0.02,
        1.55,
    )
    safety_violation_p = clamp(
        0.040
        + 0.170 * loads["single_load"]
        + 0.190 * loads["interaction_load"]
        + 0.095 * loads["safety_load"]
        + 0.075 * missed_fault_p
        + 0.042 * false_isolation_p
        - 0.100 * method["risk"]
        - 0.042 * method["recover"]
        - 0.032 * method["calibration"]
        - 0.024 * method["fusion"]
        + noise(0.005),
        0.002,
        0.68,
    )
    damage_p = clamp(
        0.022
        + 0.390 * safety_violation_p
        + 0.075 * loads["safety_load"]
        + 0.042 * recovery_latency
        - 0.055 * method["risk"]
        - 0.018 * method["recover"]
        + noise(0.005),
        0.001,
        0.56,
    )
    ece_p = clamp(
        0.100
        + 0.080 * split["stress"]
        + 0.072 * loads["drift_load"]
        + 0.050 * loads["false_alarm_load"]
        - 0.210 * method["calibration"]
        - 0.038 * method["fusion"]
        - 0.030 * method["active_repair"]
        + noise(0.004),
        0.002,
        0.60,
    )
    success_p = clamp(
        method["base"]
        - task["difficulty"]
        - 0.045 * split["stress"]
        - 0.034 * split["single_shift"]
        - 0.048 * split["pair_shift"]
        - 0.036 * split["temporal_shift"]
        - 0.025 * split["false_alarm_pressure"]
        - 0.030 * split["calibration_drift"]
        + 0.102 * method["single"] * loads["single_load"]
        + 0.150 * method["interaction"] * loads["interaction_load"]
        + 0.064 * method["detect"] * (loads["single_load"] + loads["interaction_load"])
        + 0.076 * method["recover"] * loads["temporal_load"]
        + 0.055 * method["risk"] * loads["safety_load"]
        + 0.050 * method["temporal"] * loads["temporal_load"]
        + 0.040 * method["fusion"] * (loads["single_load"] + loads["interaction_load"]) / 2.0
        + 0.034 * method["active_repair"] * (loads["interaction_load"] + loads["temporal_load"]) / 2.0
        - 0.096 * missed_fault_p
        - 0.098 * safety_violation_p
        - 0.084 * damage_p
        - 0.054 * false_isolation_p
        - 0.036 * recovery_latency
        - 0.022 * method["cost"] * split["stress"]
        + noise(0.010),
        0.02,
        0.98,
    )
    predicted_safety_risk = clamp(
        safety_violation_p
        + 0.055 * (1.0 - method["calibration"])
        + 0.030 * loads["drift_load"]
        + 0.020 * loads["false_alarm_load"]
        - 0.040 * method["risk"]
        - 0.032 * method["active_repair"] * method["calibration"]
        + noise(0.004),
        0.0,
        1.0,
    )
    if method["method"] == ORACLE:
        oracle_success_p = success_p
    else:
        oracle_success_p = probabilities(method_by_name(ORACLE), task, regime, split, seed, episode, tag + "_oracle")[0]
    regret = clamp(oracle_success_p - success_p, -0.10, 1.0)
    utility_p = (
        success_p
        - 1.08 * safety_violation_p
        - 0.82 * damage_p
        - 0.30 * missed_fault_p
        - 0.24 * false_isolation_p
        - 0.17 * recovery_latency
        - 0.070 * ece_p
        - 0.050 * method["cost"]
    )
    return (
        success_p,
        safety_violation_p,
        damage_p,
        fault_f1_p,
        interaction_f1_p,
        missed_fault_p,
        false_isolation_p,
        recovery_latency,
        ece_p,
        regret,
        utility_p,
        predicted_safety_risk,
    )


def simulate_episode(method, task, regime, split, seed, episode, tag):
    (
        success_p,
        safety_p,
        damage_p,
        fault_f1_p,
        interaction_f1_p,
        missed_p,
        false_p,
        latency,
        ece_p,
        regret,
        _utility_p,
        predicted_risk,
    ) = probabilities(method, task, regime, split, seed, episode, tag)
    rng = rng_for("draw", tag, method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    success = int(rng.random() < success_p)
    safety = int(rng.random() < safety_p)
    damage = int(rng.random() < damage_p)
    fault_f1 = int(rng.random() < fault_f1_p)
    interaction_f1 = int(rng.random() < interaction_f1_p)
    missed_fault = int(rng.random() < missed_p)
    false_isolation = int(rng.random() < false_p)
    # The simulator has access to its latent Bernoulli probability, so the
    # per-cell calibration residual is the proper local ECE proxy. Comparing a
    # probability to one Bernoulli draw would be absolute prediction error, not
    # calibration error.
    ece = ece_p
    utility = (
        success
        - 1.08 * safety
        - 0.82 * damage
        - 0.30 * missed_fault
        - 0.24 * false_isolation
        - 0.17 * latency
        - 0.070 * ece
        - 0.050 * method["cost"]
    )
    return {
        "method": method["method"],
        "split": split["split"],
        "task": task["task"],
        "regime": regime["regime"],
        "seed": seed,
        "episode": episode,
        "success": success,
        "safety_violation": safety,
        "damage": damage,
        "fault_f1": fault_f1,
        "interaction_f1": interaction_f1,
        "missed_fault": missed_fault,
        "false_isolation": false_isolation,
        "recovery_latency": latency,
        "ece": ece,
        "regret": regret,
        "utility": utility,
        "predicted_safety_risk": predicted_risk,
        "success_probability": success_p,
    }


def mean(values):
    values = list(values)
    return float(np.mean(values)) if values else 0.0


def ci95(values):
    arr = np.asarray(list(values), dtype=float)
    if len(arr) < 2:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / math.sqrt(len(arr)))


def rounded_row(row):
    out = {}
    for key, value in row.items():
        out[key] = f"{value:.5f}" if isinstance(value, float) else value
    return out


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rounded_row(row) for row in rows)


def aggregate(rows, keys, metrics):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[k] for k in keys)].append(row)
    out = []
    for key, group in sorted(grouped.items()):
        record = dict(zip(keys, key))
        record["rows"] = len(group)
        for metric in metrics:
            vals = [float(r[metric]) for r in group]
            record[metric] = mean(vals)
            record[f"ci95_{metric}"] = ci95(vals)
        out.append(record)
    return out


def summarize_episode_group(rows, identity):
    record = dict(identity)
    record["episodes"] = len(rows)
    for metric in METRICS:
        record[metric] = mean(float(row[metric]) for row in rows)
    record["predicted_safety_risk"] = mean(float(row["predicted_safety_risk"]) for row in rows)
    record["success_probability"] = mean(float(row["success_probability"]) for row in rows)
    return record


def dataset_summary():
    rows = []
    for split in SPLITS:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    rows.append(
                        {
                            "split": split["split"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "stress": split["stress"],
                            **latent_loads(task, regime, split),
                        }
                    )
    return rows


def run_rollout_table(path, methods, splits, tasks, regimes, seeds, episodes, tag, extra_identity=None):
    extra_identity = extra_identity or {}
    group_rows = []
    fieldnames = [
        *extra_identity.keys(),
        "method",
        "split",
        "task",
        "regime",
        "seed",
        "episode",
        "success",
        "safety_violation",
        "damage",
        "fault_f1",
        "interaction_f1",
        "missed_fault",
        "false_isolation",
        "recovery_latency",
        "ece",
        "regret",
        "utility",
        "predicted_safety_risk",
        "success_probability",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for method in methods:
            for split in splits:
                for task in tasks:
                    for regime in regimes:
                        for seed in seeds:
                            episode_rows = []
                            for episode in range(episodes):
                                row = simulate_episode(method, task, regime, split, seed, episode, tag)
                                if extra_identity:
                                    row = {**extra_identity, **row}
                                writer.writerow(rounded_row(row))
                                episode_rows.append(row)
                            identity = {
                                **extra_identity,
                                "method": method["method"],
                                "split": split["split"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                            }
                            group_rows.append(summarize_episode_group(episode_rows, identity))
    return group_rows


def main_evidence():
    group_rows = run_rollout_table(
        RESULTS / "rollouts.csv",
        METHODS,
        SPLITS,
        TASKS,
        REGIMES,
        SEEDS,
        EPISODES_PER_CELL,
        "main",
    )
    hard_groups = [row for row in group_rows if row["split"] in HARD_SPLITS]
    main_seed = aggregate(hard_groups, ["method", "seed"], METRICS)
    hard_metrics = aggregate(main_seed, ["method"], METRICS)
    metrics = aggregate(group_rows, ["method", "split"], METRICS)
    return group_rows, main_seed, hard_metrics, metrics


def pairwise_stats(seed_metrics):
    v5 = {row["seed"]: row for row in seed_metrics if row["method"] == V5}
    rows = []
    for method in sorted({row["method"] for row in seed_metrics}):
        if method == V5:
            continue
        peer = {row["seed"]: row for row in seed_metrics if row["method"] == method}
        diffs = [float(v5[seed]["success"]) - float(peer[seed]["success"]) for seed in SEEDS]
        utility_diffs = [float(v5[seed]["utility"]) - float(peer[seed]["utility"]) for seed in SEEDS]
        rows.append(
            {
                "comparison": f"{V5}_vs_{method}",
                "baseline": method,
                "mean_success_diff": mean(diffs),
                "ci95_success_diff": ci95(diffs),
                "mean_utility_diff": mean(utility_diffs),
                "ci95_utility_diff": ci95(utility_diffs),
                "wins_over_seeds": sum(1 for diff in diffs if diff > 0),
                "utility_wins_over_seeds": sum(1 for diff in utility_diffs if diff > 0),
                "seeds": len(SEEDS),
                "decision": "v5_better" if mean(diffs) > 0 and sum(1 for diff in diffs if diff > 0) >= 8 else "not_decisive",
            }
        )
    return rows


def ablation_evidence():
    methods = [named_method(params, name) for name, params, _ in ABLATIONS]
    hard_splits = [split for split in SPLITS if split["split"] in HARD_SPLITS]
    group_rows = run_rollout_table(
        RESULTS / "ablation_rollouts.csv",
        methods,
        hard_splits,
        TASKS,
        REGIMES,
        SEEDS,
        EPISODES_PER_CELL,
        "ablation",
    )
    for row in group_rows:
        row["ablation"] = row.pop("method")
    seed_rows = aggregate(group_rows, ["ablation", "seed"], METRICS)
    metrics = aggregate(seed_rows, ["ablation"], METRICS)
    notes = {name: note for name, _, note in ABLATIONS}
    for row in metrics:
        row["interpretation"] = notes[row["ablation"]]
    return group_rows, seed_rows, metrics


def stress_splits():
    splits = []
    for idx, level in enumerate(np.linspace(0.0, 1.0, 10)):
        splits.append(
            {
                "split": f"stress_{idx:02d}",
                "stress": float(level),
                "single_shift": 0.10 + 0.62 * float(level),
                "pair_shift": 0.08 + 0.78 * float(level),
                "temporal_shift": 0.08 + 0.78 * float(level),
                "recovery_delay": 0.08 + 0.72 * float(level),
                "false_alarm_pressure": 0.10 + 0.78 * float(level),
                "calibration_drift": 0.08 + 0.72 * float(level),
            }
        )
    return splits


def stress_evidence():
    methods = [method_by_name(name) for name in STRESS_METHODS]
    group_rows = run_rollout_table(
        RESULTS / "stress_sweep_raw.csv",
        methods,
        stress_splits(),
        TASKS,
        REGIMES,
        SEEDS,
        EPISODES_PER_CELL,
        "stress",
    )
    for row in group_rows:
        row["stress_level"] = float(row["split"].split("_")[1]) / 9.0
    seed_rows = aggregate(group_rows, ["method", "split", "stress_level", "seed"], METRICS)
    metrics = aggregate(seed_rows, ["method", "split", "stress_level"], METRICS)
    return group_rows, seed_rows, metrics


def fixed_risk_evidence():
    methods = [method_by_name(name) for name in FIXED_RISK_METHODS]
    splits = [split for split in SPLITS if split["split"] in {"recovery_latency_shift", "combined_extreme"}]
    budgets = [0.08, 0.12, 0.16, 0.20]
    raw_rows = []
    fieldnames = [
        "risk_budget",
        "covered",
        "safe_repair",
        "method",
        "split",
        "task",
        "regime",
        "seed",
        "episode",
        *METRICS,
        "predicted_safety_risk",
    ]
    with (RESULTS / "fixed_risk_raw.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for budget in budgets:
            for method in methods:
                for split in splits:
                    for task in TASKS:
                        for regime in REGIMES:
                            for seed in SEEDS:
                                for episode in range(EPISODES_PER_CELL):
                                    row = simulate_episode(method, task, regime, split, seed, episode, f"fixed_{budget}")
                                    direct = row["predicted_safety_risk"] <= budget or method["method"] == ORACLE
                                    repair_probability = clamp(
                                        method["active_repair"] * method["recover"] * method["calibration"] * method["false_alarm_control"],
                                        0.0,
                                        0.86,
                                    )
                                    repair_rng = rng_for("fixed_repair", budget, method["method"], split["split"], task["task"], regime["regime"], seed, episode)
                                    safe_repair = int((not direct) and repair_rng.random() < repair_probability)
                                    covered = int(direct or safe_repair)
                                    fixed = dict(row)
                                    if safe_repair:
                                        fixed["safety_violation"] = 0.0
                                        fixed["damage"] = 0.0
                                        fixed["false_isolation"] = 1.0
                                        fixed["recovery_latency"] = min(1.55, float(fixed["recovery_latency"]) + 0.42)
                                        fixed["ece"] = abs(float(fixed["predicted_safety_risk"]) - float(fixed["safety_violation"]))
                                        fixed["utility"] = (
                                            float(fixed["success"])
                                            - 1.08 * float(fixed["safety_violation"])
                                            - 0.82 * float(fixed["damage"])
                                            - 0.30 * float(fixed["missed_fault"])
                                            - 0.24 * float(fixed["false_isolation"])
                                            - 0.17 * float(fixed["recovery_latency"])
                                            - 0.070 * float(fixed["ece"])
                                            - 0.050 * method["cost"]
                                        )
                                    fixed_row = {
                                        "risk_budget": budget,
                                        "covered": covered,
                                        "safe_repair": safe_repair,
                                        "method": fixed["method"],
                                        "split": fixed["split"],
                                        "task": fixed["task"],
                                        "regime": fixed["regime"],
                                        "seed": fixed["seed"],
                                        "episode": fixed["episode"],
                                    }
                                    for metric in METRICS:
                                        fixed_row[metric] = float(fixed[metric]) if covered else 0.0
                                    fixed_row["predicted_safety_risk"] = fixed["predicted_safety_risk"]
                                    writer.writerow(rounded_row(fixed_row))
                                    raw_rows.append(fixed_row)
    seed_rows = aggregate(raw_rows, ["method", "risk_budget", "seed"], [*METRICS, "covered"])
    metrics = aggregate(seed_rows, ["method", "risk_budget"], [*METRICS, "covered"])
    v5 = {(row["risk_budget"], row["seed"]): row for row in seed_rows if row["method"] == V5}
    pairwise = []
    for method in sorted({row["method"] for row in seed_rows}):
        if method == V5:
            continue
        for budget in budgets:
            peer = {(row["risk_budget"], row["seed"]): row for row in seed_rows if row["method"] == method and row["risk_budget"] == budget}
            diffs = [float(v5[(budget, seed)]["utility"]) - float(peer[(budget, seed)]["utility"]) for seed in SEEDS]
            pairwise.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "mean_utility_diff": mean(diffs),
                    "ci95_utility_diff": ci95(diffs),
                    "wins_over_seeds": sum(1 for diff in diffs if diff > 0),
                    "seeds": len(SEEDS),
                }
            )
    return raw_rows, seed_rows, metrics, pairwise


def failure_cases(group_rows, hard_metrics):
    best_ref = max([row for row in hard_metrics if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["success"]))["method"]
    ref_lookup = {
        (row["split"], row["task"], row["regime"], row["seed"]): row
        for row in group_rows
        if row["method"] == best_ref and row["split"] in HARD_SPLITS
    }
    cases = []
    for row in group_rows:
        if row["method"] != V5 or row["split"] not in HARD_SPLITS:
            continue
        ref = ref_lookup[(row["split"], row["task"], row["regime"], row["seed"])]
        success_gap = float(row["success"]) - float(ref["success"])
        risk_score = (
            -success_gap
            + float(row["safety_violation"])
            + float(row["damage"])
            + 0.40 * float(row["false_isolation"])
            + 0.30 * float(row["missed_fault"])
            + 0.20 * float(row["recovery_latency"])
        )
        cases.append((risk_score, success_gap, row, ref))
    cases.sort(reverse=True, key=lambda item: item[0])
    out = []
    for idx, (risk_score, success_gap, row, ref) in enumerate(cases[:24], start=1):
        out.append(
            {
                "case_id": idx,
                "split": row["split"],
                "task": row["task"],
                "regime": row["regime"],
                "seed": row["seed"],
                "v5_success": row["success"],
                "reference_method": best_ref,
                "reference_success": ref["success"],
                "success_gap": success_gap,
                "v5_safety_violation": row["safety_violation"],
                "v5_damage": row["damage"],
                "v5_false_isolation": row["false_isolation"],
                "v5_missed_fault": row["missed_fault"],
                "risk_score": risk_score,
                "lesson": "composition helps least when a robust baseline can down-weight the dominant sensor fault without modeling higher-order interactions",
            }
        )
    return out


def latex_escape(value):
    return str(value).replace("_", "\\_")


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\resizebox{\\linewidth}{!}{%\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                if isinstance(value, (float, int)) and key not in {"rows", "case_id", "seed", "wins_over_seeds"}:
                    values.append(f"{float(value):.3f}")
                else:
                    values.append(latex_escape(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table}\n")


def make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    hard = sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True)
    methods = [row["method"] for row in hard]
    x = np.arange(len(methods))
    colors = ["#8aa1b1"] * len(methods)
    for idx, name in enumerate(methods):
        if name == V5:
            colors[idx] = "#c76f2b"
        elif name == ORACLE:
            colors[idx] = "#264653"

    plt.figure(figsize=(13.0, 5.8))
    plt.bar(x, [float(row["success"]) for row in hard], yerr=[float(row["ci95_success"]) for row in hard], color=colors, capsize=3)
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Hard-aggregate success")
    plt.title("Sensor failure compositionality hard aggregate")
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_v5_hard_success.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.6, 5.8))
    for row in hard:
        marker, size, color = "o", 58, "#7f8c8d"
        if row["method"] == V5:
            marker, size, color = "*", 180, "#c76f2b"
        if row["method"] == ORACLE:
            marker, size, color = "D", 84, "#264653"
        plt.scatter(float(row["safety_violation"]) + float(row["damage"]), float(row["regret"]), marker=marker, s=size, color=color, label=row["method"])
    plt.xlabel("Safety violation + damage")
    plt.ylabel("Regret to oracle")
    plt.title("Safety/damage versus regret")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_v5_safety_regret.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12.5, 5.8))
    width = 0.24
    plt.bar(x - width, [float(row["fault_f1"]) for row in hard], width=width, color="#2a9d8f", label="fault F1")
    plt.bar(x, [float(row["interaction_f1"]) for row in hard], width=width, color="#e76f51", label="interaction F1")
    plt.bar(x + width, [float(row["false_isolation"]) for row in hard], width=width, color="#457b9d", label="false isolation")
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Rate")
    plt.title("Hard-regime diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_v5_diagnostics.png", dpi=180)
    plt.close()

    stress_keep = {V5, "proposed_sensor_failure_composition_v4", "bayesian_sensor_fusion_monitor", "risk_aware_sensor_reconfiguration", "conformal_sensor_reliability_filter", ORACLE}
    plt.figure(figsize=(9.2, 5.8))
    for method in sorted({row["method"] for row in stress_metrics}):
        if method not in stress_keep:
            continue
        series = sorted([row for row in stress_metrics if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in series], [float(row["success"]) for row in series], marker="o", label=method)
    plt.xlabel("Sensor-interaction stress")
    plt.ylabel("Success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_v5_stress_sweep.png", dpi=180)
    plt.close()

    abls = sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True)
    labels = [row["ablation"] for row in abls]
    ax = np.arange(len(labels))
    plt.figure(figsize=(12.0, 5.8))
    plt.bar(ax, [float(row["success"]) for row in abls], yerr=[float(row["ci95_success"]) for row in abls], color=["#c76f2b" if label.startswith("full_") else "#9aa6b2" for label in labels], capsize=3)
    plt.xticks(ax, labels, rotation=35, ha="right")
    plt.ylabel("Hard-aggregate success")
    plt.title("Sensor failure compositionality ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_v5_ablation.png", dpi=180)
    plt.close()

    fixed_keep = {V5, "proposed_sensor_failure_composition_v4", "bayesian_sensor_fusion_monitor", "risk_aware_sensor_reconfiguration", ORACLE}
    plt.figure(figsize=(8.8, 5.8))
    for method in sorted({row["method"] for row in fixed_metrics}):
        if method not in fixed_keep:
            continue
        series = sorted([row for row in fixed_metrics if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot([float(row["risk_budget"]) for row in series], [float(row["utility"]) for row in series], marker="o", label=method)
    plt.xlabel("Safety-risk budget")
    plt.ylabel("Utility")
    plt.title("Fixed-risk utility")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_v5_fixed_risk.png", dpi=180)
    plt.close()


def table_outputs(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures):
    latex_table(
        RESULTS / "hard_aggregate_table.tex",
        sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True),
        [
            ("method", "Method"),
            ("success", "Succ."),
            ("safety_violation", "SafeViol."),
            ("damage", "Damage"),
            ("interaction_f1", "InterF1"),
            ("ece", "ECE"),
            ("utility", "Util."),
        ],
        "Hard-aggregate sensor-failure results.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "SuccDiff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
            ("mean_utility_diff", "UtilDiff"),
        ],
        "Seed-paired v5 differences on hard aggregate splits.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("success", "Succ."),
            ("safety_violation", "SafeViol."),
            ("damage", "Damage"),
            ("interaction_f1", "InterF1"),
            ("utility", "Util."),
        ],
        "Ablations of risk-calibrated sensor failure composition.",
    )
    max_stress = [row for row in stress_metrics if row["split"] == "stress_09"]
    latex_table(
        RESULTS / "stress_table.tex",
        sorted(max_stress, key=lambda row: float(row["success"]), reverse=True),
        [
            ("method", "Method"),
            ("success", "Succ."),
            ("safety_violation", "SafeViol."),
            ("damage", "Damage"),
            ("utility", "Util."),
        ],
        "Maximum-stress sensor-failure results.",
    )
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.08) < 1e-9]
    latex_table(
        RESULTS / "fixed_risk_table.tex",
        sorted(strict, key=lambda row: float(row["utility"]), reverse=True),
        [
            ("method", "Method"),
            ("covered", "Coverage"),
            ("success", "Succ."),
            ("safety_violation", "SafeViol."),
            ("damage", "Damage"),
            ("utility", "Util."),
        ],
        "Strict fixed-risk sensor-failure results.",
    )
    latex_table(
        RESULTS / "negative_cases_table.tex",
        failures[:10],
        [
            ("case_id", "Case"),
            ("split", "Split"),
            ("task", "Task"),
            ("regime", "Regime"),
            ("success_gap", "Gap"),
            ("v5_false_isolation", "FalseIso"),
        ],
        "Representative negative cases.",
    )


def decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics):
    hard_by_method = {row["method"]: row for row in hard_metrics}
    v5 = hard_by_method[V5]
    independent = hard_by_method[INDEPENDENT]
    non_oracle = [row for row in hard_metrics if row["method"] not in {V5, ORACLE}]
    best_success = max(non_oracle, key=lambda row: float(row["success"]))
    best_utility = max(non_oracle, key=lambda row: float(row["utility"]))
    success_gate = float(v5["success"]) - float(best_success["success"]) >= 0.050
    safety_gate = float(v5["safety_violation"]) < float(best_success["safety_violation"])
    damage_gate = float(v5["damage"]) < float(best_success["damage"])
    diagnostic_gate = float(v5["interaction_f1"]) - float(independent["interaction_f1"]) >= 0.150
    calibration_gate = float(v5["ece"]) <= 0.120 and float(v5["ece"]) < float(best_success["ece"])
    utility_gate = float(v5["utility"]) > float(best_utility["utility"])
    pairwise_gate = all(
        row["baseline"] == ORACLE or (float(row["mean_success_diff"]) > 0 and int(row["wins_over_seeds"]) >= 8)
        for row in pairwise
    )
    full = next(row for row in ablation_metrics if row["ablation"] == "full_risk_calibrated_sensor_composition_v5")
    removed = [row for row in ablation_metrics if row["ablation"] != full["ablation"]]
    best_removed_success = max(removed, key=lambda row: float(row["success"]))
    best_removed_utility = max(removed, key=lambda row: float(row["utility"]))
    ablation_gate = (
        float(full["success"]) - float(best_removed_success["success"]) >= 0.030
        or float(full["utility"]) - float(best_removed_utility["utility"]) >= 0.050
    )
    max_stress = [row for row in stress_metrics if row["split"] == "stress_09"]
    v5_stress = next(row for row in max_stress if row["method"] == V5)
    stress_ref = max([row for row in max_stress if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["success"]))
    stress_gate = float(v5_stress["success"]) - float(stress_ref["success"]) >= 0.030
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.08) < 1e-9]
    v5_fixed = next(row for row in strict if row["method"] == V5)
    fixed_ref = max([row for row in strict if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["utility"]))
    fixed_risk_gate = float(v5_fixed["covered"]) >= 0.500 and float(v5_fixed["utility"]) > float(fixed_ref["utility"])
    scope_gate = False
    gates = {
        "success_gate": success_gate,
        "safety_gate": safety_gate,
        "damage_gate": damage_gate,
        "diagnostic_gate": diagnostic_gate,
        "calibration_gate": calibration_gate,
        "utility_gate": utility_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "stress_gate": stress_gate,
        "fixed_risk_gate": fixed_risk_gate,
        "scope_gate": scope_gate,
        "best_success_reference": best_success["method"],
        "best_utility_reference": best_utility["method"],
        "best_removed_success_ablation": best_removed_success["ablation"],
        "best_removed_utility_ablation": best_removed_utility["ablation"],
        "max_stress_reference": stress_ref["method"],
        "fixed_risk_reference": fixed_ref["method"],
    }
    local_pass = all(value is True for key, value in gates.items() if key.endswith("_gate") and key != "scope_gate")
    terminal = "STRONG_REVISE" if local_pass and not scope_gate else "KILL_ARCHIVE"
    return terminal, gates


def write_summary(row_counts, hard_metrics, ablation_metrics, fixed_metrics, gates, terminal):
    hard = sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True)
    v5 = next(row for row in hard if row["method"] == V5)
    oracle = next(row for row in hard if row["method"] == ORACLE)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 103: sensor_failure_compositionality expanded v5 evidence audit\n")
        handle.write(f"Terminal decision: {terminal}\n")
        handle.write("ICLR main ready: no\n")
        handle.write("Design: 6 tasks x 8 sensor-failure regimes x 8 splits x 15 methods, 10 seeds, 6 episodes per seed/task/regime/split/method cell.\n")
        handle.write("Claim under test: risk-calibrated sensor failure composition should improve hard multimodal robot sensing beyond independent detectors, Bayesian fusion, learned latent classifiers, dropout-trained policies, mixture-of-experts routing, and robust single-sensor fallback.\n\n")
        handle.write("Row counts:\n")
        for key in sorted(row_counts):
            handle.write(f"- {key}: {row_counts[key]}\n")
        handle.write("\nHard-aggregate evidence:\n")
        for row in hard:
            handle.write(
                f"- {row['method']}: success={float(row['success']):.5f} +/- {float(row['ci95_success']):.5f}, "
                f"safety={float(row['safety_violation']):.5f}, damage={float(row['damage']):.5f}, "
                f"fault_f1={float(row['fault_f1']):.5f}, interaction_f1={float(row['interaction_f1']):.5f}, "
                f"missed={float(row['missed_fault']):.5f}, false_iso={float(row['false_isolation']):.5f}, "
                f"latency={float(row['recovery_latency']):.5f}, ece={float(row['ece']):.5f}, "
                f"regret={float(row['regret']):.5f}, utility={float(row['utility']):.5f}\n"
            )
        handle.write("\nReference winners:\n")
        for key in [
            "best_success_reference",
            "best_utility_reference",
            "best_removed_success_ablation",
            "best_removed_utility_ablation",
            "max_stress_reference",
            "fixed_risk_reference",
        ]:
            handle.write(f"- {key}={gates[key]}\n")
        handle.write(f"- v5_success={float(v5['success']):.5f}\n")
        handle.write(f"- v5_safety_violation={float(v5['safety_violation']):.5f}\n")
        handle.write(f"- v5_damage={float(v5['damage']):.5f}\n")
        handle.write(f"- v5_fault_f1={float(v5['fault_f1']):.5f}\n")
        handle.write(f"- v5_interaction_f1={float(v5['interaction_f1']):.5f}\n")
        handle.write(f"- v5_missed_fault={float(v5['missed_fault']):.5f}\n")
        handle.write(f"- v5_false_isolation={float(v5['false_isolation']):.5f}\n")
        handle.write(f"- v5_recovery_latency={float(v5['recovery_latency']):.5f}\n")
        handle.write(f"- v5_ece={float(v5['ece']):.5f}\n")
        handle.write(f"- v5_regret={float(v5['regret']):.5f}\n")
        handle.write(f"- v5_utility={float(v5['utility']):.5f}\n")
        handle.write(f"- oracle_success={float(oracle['success']):.5f}\n\n")
        handle.write("Gate outcomes:\n")
        for key, value in gates.items():
            if key.endswith("_gate"):
                handle.write(f"- {key}: {value}\n")
        handle.write("\nTerminal rationale:\n")
        if terminal == "STRONG_REVISE":
            handle.write("- all frozen local empirical gates pass; terminal state remains STRONG_REVISE only because scope/external-validation evidence is missing\n")
        else:
            handle.write("- at least one frozen local empirical gate fails; terminal state remains KILL_ARCHIVE\n")
        handle.write("- scope gate fails because no real robot study, accepted high-fidelity benchmark, external multimodal-sensing benchmark, calibrated real sensor-failure logs, trained checkpoints, or rollout videos exist\n\n")
        handle.write("Ablation summary:\n")
        for row in sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True):
            handle.write(
                f"- {row['ablation']}: success={float(row['success']):.5f}, safety={float(row['safety_violation']):.5f}, "
                f"damage={float(row['damage']):.5f}, interaction_f1={float(row['interaction_f1']):.5f}, "
                f"utility={float(row['utility']):.5f}, note={row['interpretation']}\n"
            )
        strict = next(row for row in fixed_metrics if row["method"] == V5 and abs(float(row["risk_budget"]) - 0.08) < 1e-9)
        handle.write(
            f"\nFixed-risk strict v5: coverage={float(strict['covered']):.5f}, success={float(strict['success']):.5f}, "
            f"safety={float(strict['safety_violation']):.5f}, damage={float(strict['damage']):.5f}, "
            f"false_iso={float(strict['false_isolation']):.5f}, utility={float(strict['utility']):.5f}\n"
        )
        handle.write("\nNo human-subject, hardware, or external high-fidelity validation is claimed; this is a local CPU-only executable surrogate audit.\n")
        handle.write(f"terminal={terminal}\n")


def main():
    for stale in RESULTS.glob("*.csv"):
        stale.unlink()
    for stale in RESULTS.glob("*.tex"):
        stale.unlink()
    for stale in FIGURES.glob("sensor*.png"):
        stale.unlink()

    ds = dataset_summary()
    write_csv(RESULTS / "dataset_summary.csv", ds)

    group_rows, main_seed, hard_metrics, metrics = main_evidence()
    pairwise = pairwise_stats(main_seed)
    ablation_groups, ablation_seed, ablation_metrics = ablation_evidence()
    stress_raw, stress_seed, stress_metrics = stress_evidence()
    fixed_raw, fixed_seed, fixed_metrics, fixed_pairwise = fixed_risk_evidence()
    failures = failure_cases(group_rows, hard_metrics)
    terminal, gates = decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics)

    write_csv(RESULTS / "main_group_metrics.csv", group_rows)
    write_csv(RESULTS / "main_seed_metrics.csv", main_seed)
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", main_seed)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "pairwise_stats.csv", pairwise)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed)
    write_csv(RESULTS / "stress_sweep.csv", stress_metrics)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", fixed_seed)
    write_csv(RESULTS / "fixed_risk_metrics.csv", fixed_metrics)
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", fixed_pairwise)
    write_csv(RESULTS / "failure_cases.csv", failures)

    table_outputs(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures)
    make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)

    row_counts = {
        "dataset_summary_rows": len(ds),
        "main_rollout_rows": 345600,
        "main_group_rows": len(group_rows),
        "main_seed_metric_rows": len(main_seed),
        "main_metric_rows": len(metrics),
        "hard_seed_rows": len(main_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "ablation_rollout_rows": 115200,
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablation_metrics),
        "stress_rollout_rows": 288000,
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_metrics),
        "fixed_risk_rows": len(fixed_raw),
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_metrics),
        "fixed_risk_pairwise_rows": len(fixed_pairwise),
        "failure_case_rows": len(failures),
    }
    write_summary(row_counts, hard_metrics, ablation_metrics, fixed_metrics, gates, terminal)
    print(f"terminal={terminal}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
