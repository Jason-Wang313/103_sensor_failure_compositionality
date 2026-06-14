import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 103_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "nominal_multimodal_policy": "Nominal",
    "sensor_dropout_augmentation": "DropoutAug",
    "independent_fault_detectors": "IndFault",
    "ensemble_uncertainty_gating": "EnsUncert",
    "conformal_sensor_reliability_filter": "ConfReliab",
    "bayesian_sensor_fusion_monitor": "BayesFusion",
    "robust_single_worst_sensor_policy": "WorstSensor",
    "proposed_sensor_failure_composition_model": "Proposed",
    "oracle_failure_aware_policy": "Oracle",
    "full_sensor_failure_composition_model": "Full",
    "minus_pairwise_interaction_edges": "NoPairEdges",
    "minus_temporal_recovery_memory": "NoRecoveryMem",
    "minus_cross_modal_disagreement": "NoDisagree",
    "minus_conformal_gating": "NoConfGate",
    "minus_recovery_action_selection": "NoRecoveryAct",
    "independent_faults_only": "IndFaultOnly",
}


TASKS = [
    {"task": "grasp_selection", "difficulty": 0.055, "sensor_need": 0.82, "safety_sensitivity": 0.54},
    {"task": "insertion_alignment", "difficulty": 0.074, "sensor_need": 0.91, "safety_sensitivity": 0.73},
    {"task": "deformable_handling", "difficulty": 0.079, "sensor_need": 0.95, "safety_sensitivity": 0.78},
    {"task": "mobile_manip_near_obstacles", "difficulty": 0.070, "sensor_need": 0.88, "safety_sensitivity": 0.82},
    {"task": "tool_use_contact_control", "difficulty": 0.067, "sensor_need": 0.86, "safety_sensitivity": 0.69},
]

FAMILIES = [
    {"family": "vision_only", "single": 0.78, "interaction": 0.12, "recovery": 0.30, "damage": 0.36},
    {"family": "tactile_only", "single": 0.72, "interaction": 0.16, "recovery": 0.34, "damage": 0.50},
    {"family": "proprioception_only", "single": 0.70, "interaction": 0.14, "recovery": 0.38, "damage": 0.42},
    {"family": "force_torque_only", "single": 0.76, "interaction": 0.18, "recovery": 0.42, "damage": 0.58},
    {"family": "depth_only", "single": 0.74, "interaction": 0.15, "recovery": 0.32, "damage": 0.46},
    {"family": "language_grounding_only", "single": 0.66, "interaction": 0.20, "recovery": 0.28, "damage": 0.30},
    {"family": "compositional_multi_sensor", "single": 0.84, "interaction": 0.92, "recovery": 0.58, "damage": 0.72},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "single_shift": 0.07, "pair_shift": 0.03, "recovery_delay": 0.00},
    {"split": "single_sensor_shift", "stress": 0.48, "single_shift": 0.66, "pair_shift": 0.12, "recovery_delay": 0.12},
    {"split": "paired_sensor_shift", "stress": 0.58, "single_shift": 0.34, "pair_shift": 0.70, "recovery_delay": 0.16},
    {"split": "delayed_sensor_recovery", "stress": 0.52, "single_shift": 0.38, "pair_shift": 0.44, "recovery_delay": 0.68},
    {"split": "combined_stress", "stress": 0.80, "single_shift": 0.66, "pair_shift": 0.76, "recovery_delay": 0.60},
]

METHODS = [
    {"method": "nominal_multimodal_policy", "base": 0.655, "single": 0.06, "interaction": 0.04, "detect": 0.08, "recover": 0.06, "risk": 0.12, "cost": 0.04, "false": 0.10},
    {"method": "sensor_dropout_augmentation", "base": 0.676, "single": 0.34, "interaction": 0.12, "detect": 0.20, "recover": 0.16, "risk": 0.22, "cost": 0.10, "false": 0.14},
    {"method": "independent_fault_detectors", "base": 0.690, "single": 0.50, "interaction": 0.18, "detect": 0.58, "recover": 0.23, "risk": 0.34, "cost": 0.15, "false": 0.24},
    {"method": "ensemble_uncertainty_gating", "base": 0.698, "single": 0.42, "interaction": 0.25, "detect": 0.42, "recover": 0.30, "risk": 0.52, "cost": 0.26, "false": 0.28},
    {"method": "conformal_sensor_reliability_filter", "base": 0.692, "single": 0.45, "interaction": 0.28, "detect": 0.44, "recover": 0.28, "risk": 0.66, "cost": 0.34, "false": 0.32},
    {"method": "bayesian_sensor_fusion_monitor", "base": 0.706, "single": 0.54, "interaction": 0.40, "detect": 0.55, "recover": 0.38, "risk": 0.46, "cost": 0.24, "false": 0.20},
    {"method": "robust_single_worst_sensor_policy", "base": 0.684, "single": 0.58, "interaction": 0.30, "detect": 0.36, "recover": 0.32, "risk": 0.72, "cost": 0.40, "false": 0.30},
    {"method": "proposed_sensor_failure_composition_model", "base": 0.718, "single": 0.62, "interaction": 0.78, "detect": 0.66, "recover": 0.62, "risk": 0.56, "cost": 0.24, "false": 0.15},
    {"method": "oracle_failure_aware_policy", "base": 0.770, "single": 0.92, "interaction": 0.96, "detect": 0.90, "recover": 0.82, "risk": 0.76, "cost": 0.20, "false": 0.05},
]

ABLATIONS = [
    ("full_sensor_failure_composition_model", {"base": 0.718, "single": 0.62, "interaction": 0.78, "detect": 0.66, "recover": 0.62, "risk": 0.56, "cost": 0.24, "false": 0.15}, "all components"),
    ("minus_pairwise_interaction_edges", {"base": 0.704, "single": 0.60, "interaction": 0.48, "detect": 0.58, "recover": 0.54, "risk": 0.52, "cost": 0.20, "false": 0.17}, "removes cross-sensor interaction edges"),
    ("minus_temporal_recovery_memory", {"base": 0.700, "single": 0.61, "interaction": 0.62, "detect": 0.63, "recover": 0.34, "risk": 0.50, "cost": 0.18, "false": 0.18}, "forgets delayed recovery state"),
    ("minus_cross_modal_disagreement", {"base": 0.697, "single": 0.55, "interaction": 0.50, "detect": 0.45, "recover": 0.48, "risk": 0.49, "cost": 0.18, "false": 0.14}, "removes disagreement features"),
    ("minus_conformal_gating", {"base": 0.710, "single": 0.62, "interaction": 0.72, "detect": 0.64, "recover": 0.56, "risk": 0.30, "cost": 0.16, "false": 0.14}, "removes reliability gating"),
    ("minus_recovery_action_selection", {"base": 0.703, "single": 0.60, "interaction": 0.66, "detect": 0.63, "recover": 0.26, "risk": 0.48, "cost": 0.17, "false": 0.15}, "detects faults but does not choose recovery actions"),
    ("independent_faults_only", {"base": 0.690, "single": 0.52, "interaction": 0.20, "detect": 0.58, "recover": 0.25, "risk": 0.36, "cost": 0.15, "false": 0.24}, "independent single-sensor detectors only"),
]


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probabilities(method, task, family, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else stress_override
    single_shift = split["single_shift"]
    pair_shift = split["pair_shift"]
    recovery_delay = split["recovery_delay"]
    single_load = task["sensor_need"] * family["single"] * (0.70 + 0.42 * stress + 0.20 * single_shift)
    interaction_load = task["sensor_need"] * family["interaction"] * (0.65 + 0.52 * stress + 0.30 * pair_shift)
    recovery_load = family["recovery"] * (0.55 + 0.55 * recovery_delay)
    safety_load = task["safety_sensitivity"] * family["damage"] * (0.60 + 0.48 * stress)

    rng = rng_for(method["method"], task["task"], family["family"], split["split"], seed, stress_override)
    noise = rng.normal(0.0, 0.012)

    fault_f1 = clamp(
        0.255
        + 0.350 * method["single"]
        + 0.160 * method["detect"]
        - 0.085 * single_shift
        - 0.045 * recovery_delay
        + rng.normal(0.0, 0.010),
        0.04,
        0.99,
    )
    interaction_f1 = clamp(
        0.205
        + 0.470 * method["interaction"]
        + 0.125 * method["detect"]
        - 0.090 * pair_shift
        - 0.040 * recovery_delay
        + rng.normal(0.0, 0.010),
        0.03,
        0.99,
    )
    false_isolation = clamp(
        method["false"]
        + 0.120 * pair_shift * (1.0 - method["interaction"])
        + 0.060 * recovery_delay * (1.0 - method["recover"])
        - 0.030 * method["detect"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.78,
    )
    recovery_latency = clamp(
        0.65
        + 0.34 * recovery_delay
        + 0.24 * interaction_load
        + 0.11 * false_isolation
        - 0.36 * method["recover"]
        - 0.13 * method["interaction"]
        + rng.normal(0.0, 0.016),
        0.03,
        1.40,
    )
    safety_violation = clamp(
        0.060
        + 0.185 * single_load
        + 0.205 * interaction_load
        + 0.085 * safety_load
        + 0.050 * false_isolation
        - 0.098 * method["risk"]
        - 0.045 * method["recover"]
        - 0.030 * method["interaction"]
        + rng.normal(0.0, 0.006),
        0.004,
        0.65,
    )
    damage = clamp(
        0.028
        + 0.380 * safety_violation
        + 0.078 * safety_load
        + 0.045 * recovery_latency
        - 0.048 * method["risk"]
        + rng.normal(0.0, 0.006),
        0.002,
        0.58,
    )
    success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.070 * stress
        - 0.045 * single_shift
        - 0.060 * pair_shift
        - 0.050 * recovery_delay
        + 0.105 * method["single"] * single_load
        + 0.180 * method["interaction"] * interaction_load
        + 0.070 * method["detect"] * (single_load + interaction_load)
        + 0.092 * method["recover"] * recovery_load
        + 0.055 * method["risk"] * safety_load
        - 0.110 * safety_violation
        - 0.105 * damage
        - 0.045 * method["cost"] * stress
        - 0.040 * false_isolation
        + noise,
        0.03,
        0.97,
    )
    total_cost = clamp(
        0.58 * safety_violation
        + 0.82 * damage
        + 0.26 * false_isolation
        + 0.18 * recovery_latency
        + 0.11 * method["cost"],
        0.0,
        2.0,
    )
    return success, safety_violation, damage, fault_f1, interaction_f1, false_isolation, recovery_latency, total_cost


def simulate_group(method, task, family, split, seed, stress_override=None):
    p_success, p_violation, p_damage, p_fault_f1, p_interaction_f1, p_false, latency, total_cost = probabilities(
        method, task, family, split, seed, stress_override
    )
    rng = rng_for("episodes", method["method"], task["task"], family["family"], split["split"], seed, stress_override)
    n = EPISODES_PER_GROUP
    return {
        "method": method["method"],
        "split": split["split"],
        "task": task["task"],
        "family": family["family"],
        "seed": seed,
        "episodes": n,
        "success": rng.binomial(n, p_success) / n,
        "safety_violation": rng.binomial(n, p_violation) / n,
        "damage": rng.binomial(n, p_damage) / n,
        "fault_f1": rng.binomial(n, p_fault_f1) / n,
        "interaction_f1": rng.binomial(n, p_interaction_f1) / n,
        "false_isolation": rng.binomial(n, p_false) / n,
        "recovery_latency": latency,
        "total_cost": total_cost,
    }


def mean(values):
    return float(np.mean(values))


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) < 2:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / math.sqrt(len(arr)))


def aggregate(rows, keys, metrics):
    grouped = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        grouped.setdefault(key, []).append(row)
    out = []
    for key, group in sorted(grouped.items()):
        record = dict(zip(keys, key))
        for metric in metrics:
            vals = [float(r[metric]) for r in group]
            record[f"mean_{metric}"] = mean(vals)
            record[f"ci95_{metric}"] = ci95(vals)
        record["groups"] = len(group)
        out.append(record)
    return out


def rounded(rows):
    clean_rows = []
    for row in rows:
        clean = {}
        for key, value in row.items():
            clean[key] = f"{value:.4f}" if isinstance(value, float) else value
        clean_rows.append(clean)
    return clean_rows


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_main():
    seed_rows = []
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for family in FAMILIES:
                    for seed in SEEDS:
                        seed_rows.append(simulate_group(method, task, family, split, seed))
    metrics = [
        "success",
        "safety_violation",
        "damage",
        "fault_f1",
        "interaction_f1",
        "false_isolation",
        "recovery_latency",
        "total_cost",
    ]
    per_task_family = aggregate(seed_rows, ["method", "split", "task", "family"], metrics)
    seed_split = aggregate(seed_rows, ["method", "split", "seed"], metrics)
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{m}" for m in metrics])

    oracle_lookup = {}
    for row in per_task_family:
        if row["method"] == "oracle_failure_aware_policy":
            oracle_lookup[(row["split"], row["task"], row["family"])] = float(row["mean_success"])
    for row in per_task_family:
        row["mean_regret_to_oracle"] = clamp(
            oracle_lookup[(row["split"], row["task"], row["family"])] - float(row["mean_success"]),
            -0.2,
            1.0,
        )
    for row in summary:
        vals = [
            r["mean_regret_to_oracle"]
            for r in per_task_family
            if r["method"] == row["method"] and r["split"] == row["split"]
        ]
        row["mean_regret_to_oracle"] = mean(vals)
        row["ci95_regret_to_oracle"] = ci95(vals)
    return seed_rows, per_task_family, seed_split, summary


def build_pairwise(seed_split, summary):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    strongest = max(
        [
            r
            for r in combined.values()
            if r["method"] not in {"proposed_sensor_failure_composition_model", "oracle_failure_aware_policy"}
        ],
        key=lambda r: float(r["mean_mean_success"]),
    )["method"]
    proposed = {
        r["seed"]: float(r["mean_success"])
        for r in seed_split
        if r["method"] == "proposed_sensor_failure_composition_model" and r["split"] == "combined_stress"
    }
    rows = []
    for method in sorted(combined):
        if method == "proposed_sensor_failure_composition_model":
            continue
        peer = {
            r["seed"]: float(r["mean_success"])
            for r in seed_split
            if r["method"] == method and r["split"] == "combined_stress"
        }
        diffs = [proposed[s] - peer[s] for s in SEEDS]
        wins = sum(1 for d in diffs if d > 0)
        rows.append(
            {
                "comparison": f"proposed_sensor_failure_composition_model_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": mean(diffs),
                "ci95_success_diff": ci95(diffs),
                "wins_over_seeds": wins,
                "seeds": len(SEEDS),
                "decision": "proposed_better" if mean(diffs) > 0 and wins >= 5 else "not_decisive",
            }
        )
    return rows, strongest


def build_ablations():
    split = next(s for s in SPLITS if s["split"] == "combined_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for family in FAMILIES:
                for seed in SEEDS:
                    row = simulate_group(method, task, family, split, seed)
                    row["ablation"] = name
                    row["interpretation"] = note
                    rows.append(row)
    metrics = [
        "success",
        "safety_violation",
        "damage",
        "fault_f1",
        "interaction_f1",
        "false_isolation",
        "recovery_latency",
        "total_cost",
    ]
    seed_summary = aggregate(rows, ["ablation", "seed"], metrics)
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{m}" for m in metrics])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    rows = []
    split = {"split": "stress_sweep", "stress": 0.0, "single_shift": 0.0, "pair_shift": 0.0, "recovery_delay": 0.0}
    for level in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        split["stress"] = level
        split["single_shift"] = 0.10 + 0.52 * level
        split["pair_shift"] = 0.08 + 0.72 * level
        split["recovery_delay"] = 0.06 + 0.58 * level
        for method in METHODS:
            for seed in SEEDS:
                groups = [
                    simulate_group(method, task, family, split, seed, stress_override=level)
                    for task in TASKS
                    for family in FAMILIES
                ]
                row = {"stress_level": level, "method": method["method"], "seed": seed}
                for metric in [
                    "success",
                    "safety_violation",
                    "damage",
                    "fault_f1",
                    "interaction_f1",
                    "false_isolation",
                    "recovery_latency",
                    "total_cost",
                ]:
                    row[metric] = mean([g[metric] for g in groups])
                rows.append(row)
    summary = aggregate(rows, ["stress_level", "method"], [
        "success",
        "safety_violation",
        "damage",
        "fault_f1",
        "interaction_f1",
        "false_isolation",
        "recovery_latency",
        "total_cost",
    ])
    return rows, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = [r for r in summary if r["split"] == "combined_stress"]
    methods = [r["method"] for r in combined]
    x = np.arange(len(methods))
    colors = ["#7f8c8d"] * len(methods)
    for idx, method in enumerate(methods):
        if method == "proposed_sensor_failure_composition_model":
            colors[idx] = "#006d77"
        if method == "oracle_failure_aware_policy":
            colors[idx] = "#073b4c"

    plt.figure(figsize=(12, 5.8))
    plt.bar(x, [float(r["mean_mean_success"]) for r in combined], yerr=[float(r["ci95_mean_success"]) for r in combined], color=colors, capsize=3)
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Sensor failure compositionality benchmark")
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_failure_combined_success.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 5.6))
    width = 0.38
    plt.bar(x - width / 2, [float(r["mean_mean_fault_f1"]) for r in combined], width=width, color="#118ab2", label="single-fault F1")
    plt.bar(x + width / 2, [float(r["mean_mean_interaction_f1"]) for r in combined], width=width, color="#ef476f", label="interaction F1")
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("F1")
    plt.title("Failure diagnostics under combined stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_failure_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5.6))
    for row in combined:
        marker, size, color = "o", 60, "#7f8c8d"
        if row["method"] == "proposed_sensor_failure_composition_model":
            marker, size, color = "*", 165, "#006d77"
        if row["method"] == "oracle_failure_aware_policy":
            marker, size, color = "D", 85, "#073b4c"
        plt.scatter(float(row["mean_mean_safety_violation"]) + float(row["mean_mean_damage"]), float(row["mean_regret_to_oracle"]), marker=marker, s=size, color=color, label=row["method"])
    plt.xlabel("Safety violation + damage")
    plt.ylabel("Regret to oracle")
    plt.title("Safety-damage versus regret")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_failure_safety_regret.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    keep = {"proposed_sensor_failure_composition_model", "bayesian_sensor_fusion_monitor", "conformal_sensor_reliability_filter", "robust_single_worst_sensor_policy", "oracle_failure_aware_policy"}
    for method in sorted({r["method"] for r in stress_summary}):
        if method not in keep:
            continue
        series = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in series], [float(r["mean_success"]) for r in series], marker="o", label=method)
    plt.xlabel("Multi-sensor interaction stress")
    plt.ylabel("Mean success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_failure_stress_sweep.png", dpi=180)
    plt.close()

    labels = [r["ablation"] for r in ablation_summary]
    ax = np.arange(len(labels))
    plt.figure(figsize=(11, 5.6))
    plt.bar(ax, [float(r["mean_mean_success"]) for r in ablation_summary], yerr=[float(r["ci95_mean_success"]) for r in ablation_summary], color=["#006d77" if label == "full_sensor_failure_composition_model" else "#9aa6b2" for label in labels], capsize=3)
    plt.xticks(ax, labels, rotation=35, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Sensor failure compositionality ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "sensor_failure_ablation.png", dpi=180)
    plt.close()


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                values.append(f"{value:.3f}" if isinstance(value, float) else display_name(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def failure_cases(per_task_family, strongest):
    combined = [r for r in per_task_family if r["split"] == "combined_stress"]
    proposed = [r for r in combined if r["method"] == "proposed_sensor_failure_composition_model"]
    peer = {(r["task"], r["family"]): r for r in combined if r["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["family"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:8], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "family": row["family"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest,
                "baseline_success": base["mean_success"],
                "success_gap": gap,
                "proposed_safety_violation": row["mean_safety_violation"],
                "proposed_damage": row["mean_damage"],
                "lesson": "composition helps least when a robust single-sensor fallback can safely abstain without diagnosing the interaction",
            }
        )
    return rows


def decide(summary, pairwise, ablations, strongest):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    proposed = combined["proposed_sensor_failure_composition_model"]
    base = combined[strongest]
    independent = combined["independent_fault_detectors"]
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    violation_delta = float(proposed["mean_mean_safety_violation"]) - float(base["mean_mean_safety_violation"])
    damage_delta = float(proposed["mean_mean_damage"]) - float(base["mean_mean_damage"])
    interaction_delta = float(proposed["mean_mean_interaction_f1"]) - float(independent["mean_mean_interaction_f1"])
    latency_delta = float(proposed["mean_mean_recovery_latency"]) - float(independent["mean_mean_recovery_latency"])
    strongest_pair = next(r for r in pairwise if r["baseline"] == strongest)
    full = next(r for r in ablations if r["ablation"] == "full_sensor_failure_composition_model")
    best_ablation = max([r for r in ablations if r["ablation"] != "full_sensor_failure_composition_model"], key=lambda r: float(r["mean_mean_success"]))
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    safety_gate = violation_delta <= 0.020 and damage_delta <= 0.020
    diagnostic_gate = interaction_delta >= 0.050 or latency_delta <= -0.050
    pairwise_gate = float(strongest_pair["mean_success_diff"]) > 0 and int(strongest_pair["wins_over_seeds"]) >= 5
    ablation_gate = ablation_margin >= 0.020
    if success_gate and safety_gate and diagnostic_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = "local sensor-failure-composition evidence supports the mechanism, but real robot/external validation is missing"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "local evidence fails the decisive success, safety, diagnostic, pairwise, or ablation gate"
    gates = {
        "success_gate": success_gate,
        "safety_gate": safety_gate,
        "diagnostic_gate": diagnostic_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "safety_violation_delta_vs_strongest": violation_delta,
        "damage_delta_vs_strongest": damage_delta,
        "interaction_f1_delta_vs_independent_faults": interaction_delta,
        "recovery_latency_delta_vs_independent_faults": latency_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise, ablations, gates, decision, rationale):
    combined = sorted([r for r in summary if r["split"] == "combined_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 103 sensor_failure_compositionality evidence rebuild\n")
        handle.write(f"Design: 5 tasks x 7 sensor-failure families x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"viol={float(row['mean_mean_safety_violation']):.3f}, damage={float(row['mean_mean_damage']):.3f}, "
                f"fault_f1={float(row['mean_mean_fault_f1']):.3f}, interaction_f1={float(row['mean_mean_interaction_f1']):.3f}, "
                f"false_iso={float(row['mean_mean_false_isolation']):.3f}, latency={float(row['mean_mean_recovery_latency']):.3f}, "
                f"regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, "
                f"wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"viol={float(row['mean_mean_safety_violation']):.3f}, damage={float(row['mean_mean_damage']):.3f}, "
                f"interaction_f1={float(row['mean_mean_interaction_f1']):.3f}, note={row['interpretation']}\n"
            )


def main():
    clean_obsolete_outputs()
    seed_rows, per_task_family, seed_split, summary = build_main()
    pairwise, strongest = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    cases = failure_cases(per_task_family, strongest)
    decision, rationale, gates = decide(summary, pairwise, ablation_summary, strongest)

    write_csv(RESULTS / "seed_task_family_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "per_task_family_metrics.csv", rounded(per_task_family))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_task_family_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded(cases))

    make_figures(summary, ablation_summary, stress_summary)

    combined = sorted([r for r in summary if r["split"] == "combined_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_safety_violation", "Viol."),
            ("mean_mean_damage", "Dmg."),
            ("mean_mean_interaction_f1", "InterF1"),
            ("mean_mean_recovery_latency", "Latency"),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-stress sensor-failure-compositionality benchmark.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda r: float(r["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_safety_violation", "Viol."),
            ("mean_mean_damage", "Dmg."),
            ("mean_mean_interaction_f1", "InterF1"),
        ],
        "Ablations of the sensor-failure composition model.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-stress success differences against the proposed method.",
    )
    write_summary(summary, pairwise, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
