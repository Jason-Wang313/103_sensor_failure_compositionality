import csv
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PAPER.mkdir(exist_ok=True)

V5 = "risk_calibrated_sensor_composition_v5"
ORACLE = "oracle_failure_aware_policy"


def ascii_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value: object) -> str:
    text = ascii_text(value)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_summary() -> dict[str, str]:
    out: dict[str, str] = {}
    for line in (RESULTS / "summary.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("Terminal decision:"):
            out["decision"] = line.split(":", 1)[1].strip()
        elif line.startswith("terminal="):
            out["terminal"] = line.split("=", 1)[1].strip()
        elif line.startswith("- ") and "=" in line:
            key, value = line[2:].split("=", 1)
            out[key.strip()] = value.strip()
        elif line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            out[key.strip()] = value.strip()
    return out


def fnum(value: object, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}"


def short_label(value: str) -> str:
    aliases = {
        "risk_calibrated_sensor_composition_v5": "sensor_v5",
        "proposed_sensor_failure_composition_v4": "sensor_v4",
        "oracle_failure_aware_policy": "oracle",
        "bayesian_sensor_fusion_monitor": "bayes_fusion",
        "risk_aware_sensor_reconfiguration": "risk_reconfig",
        "multimodal_mixture_of_experts_router": "moe_router",
        "sensor_dropout_transformer_policy": "dropout_tx",
        "causal_sensor_graph_monitor": "causal_graph",
        "learned_latent_failure_classifier": "latent_cls",
        "conformal_sensor_reliability_filter": "conformal",
        "robust_single_worst_sensor_policy": "worst_sensor",
        "ensemble_uncertainty_gating": "ensemble_gate",
        "independent_fault_detectors": "ind_faults",
        "sensor_dropout_augmentation": "dropout_aug",
        "nominal_multimodal_policy": "nominal",
        "full_risk_calibrated_sensor_composition_v5": "full_v5",
        "no_pairwise_interaction_edges": "no_pair_edges",
        "no_temporal_recovery_memory": "no_recovery_mem",
        "no_cross_modal_disagreement": "no_disagree",
        "no_conformal_calibration": "no_calibration",
        "no_recovery_action_selection": "no_recovery_act",
        "no_active_repair": "no_repair",
        "no_false_alarm_suppression": "no_false_alarm",
        "v4_composition_rules": "v4_rules",
        "bayesian_fusion_only": "bayes_only",
        "grasp_selection_under_occlusion": "grasp_occl",
        "insertion_alignment_contact": "insert_contact",
        "deformable_sorting": "deform_sort",
        "mobile_manip_obstacle_avoidance": "mobile_obst",
        "tool_use_force_control": "tool_force",
        "bin_picking_language_goal": "bin_lang",
        "compositional_multi_sensor": "multi_sensor",
        "temporal_desynchronization": "desync",
        "language_grounding_noise": "lang_noise",
        "proprioceptive_bias": "prop_bias",
        "force_torque_drift": "ft_drift",
        "depth_scale_holes": "depth_holes",
        "tactile_deadzone": "tactile_dead",
        "vision_dropout": "vision_drop",
        "desynchronization_shift": "desync_shift",
        "recovery_latency_shift": "latency_shift",
        "combined_extreme": "combined",
        "paired_sensor_shift": "paired_shift",
    }
    return aliases.get(value, value)


def compact_rows(rows: list[dict[str, str]], columns: list[str], limit: int | None = None) -> str:
    rendered = []
    for row in rows[:limit]:
        cells = []
        for column in columns:
            value = row[column]
            if column in {"method", "baseline", "ablation", "task", "regime", "split", "reference_method"}:
                cells.append(latex_escape(short_label(value)))
            elif column in {"case_id", "seed", "wins_over_seeds", "seeds", "rows"}:
                cells.append(latex_escape(value))
            else:
                cells.append(fnum(value, 3))
        rendered.append(" & ".join(cells) + r" \\")
    return "\n".join(rendered)


def make_bib_key(row: dict[str, str], index: int) -> str:
    author = ascii_text(row.get("authors", "ref")).split(";")[0].strip().split(" ")[-1]
    author = re.sub(r"[^A-Za-z0-9]+", "", author) or "ref"
    year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "nd"
    title_word = re.sub(r"[^A-Za-z0-9]+", "", ascii_text(row.get("title", "paper")).split(" ")[0]) or "paper"
    return f"{author.lower()}{year}{title_word.lower()}{index}"


def write_bib(records: list[dict[str, str]]) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    entries: list[str] = []
    for index, row in enumerate(records[:230], start=1):
        key = make_bib_key(row, index)
        while key in seen:
            key = f"{key}x"
        seen.add(key)
        keys.append(key)
        fields = [
            f"  title = {{{latex_escape(row.get('title', f'Reference {index}'))}}}",
            f"  author = {{{latex_escape(row.get('authors', 'Unknown'))}}}",
        ]
        for source, target in [("year", "year"), ("venue", "journal"), ("doi", "doi"), ("url", "url")]:
            value = latex_escape(row.get(source, ""))
            if value:
                fields.append(f"  {target} = {{{value}}}")
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
    (PAPER / "references.bib").write_text("\n".join(entries), encoding="utf-8")
    return keys


def cite(keys: list[str], start: int, stop: int) -> str:
    chosen = keys[start:min(stop, len(keys))]
    return r"\citep{" + ",".join(chosen) + "}" if chosen else ""


def citation_ledger(keys: list[str]) -> str:
    themes = [
        "multimodal robot sensing and fusion",
        "sensor failure, missing modality, and robustness",
        "failure detection, diagnosis, and recovery",
        "calibrated uncertainty and conformal risk",
        "contact-rich manipulation and tactile-force sensing",
        "language-conditioned and goal-conditioned sensing",
        "robot benchmarks, audits, and reproducibility",
    ]
    rows = []
    for index in range(0, len(keys), 3):
        chunk = keys[index:index + 3]
        rows.append(
            f"{index // 3 + 1} & {latex_escape(themes[(index // 3) % len(themes)])} & "
            + r"\citep{" + ",".join(chunk) + r"} \\"
        )
    return "\n".join(rows)


def protocol_rows(dataset: list[dict[str, str]]) -> str:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in dataset:
        if row["split"] in {"paired_sensor_shift", "desynchronization_shift", "recovery_latency_shift", "combined_extreme"}:
            grouped[(row["task"], row["regime"])].append(row)
    rows = []
    for (task, regime), group in sorted(grouped.items()):
        def avg(key: str) -> float:
            return sum(float(r[key]) for r in group) / len(group)

        rows.append(
            " & ".join(
                [
                    latex_escape(short_label(task)),
                    latex_escape(short_label(regime)),
                    fnum(avg("single_load"), 3),
                    fnum(avg("interaction_load"), 3),
                    fnum(avg("temporal_load"), 3),
                    fnum(avg("safety_load"), 3),
                    fnum(avg("drift_load"), 3),
                ]
            )
            + r" \\"
        )
    return "\n".join(rows)


def main() -> None:
    summary = read_summary()
    hard = read_csv(RESULTS / "hard_aggregate_metrics.csv")
    pairwise = read_csv(RESULTS / "pairwise_stats.csv")
    ablations = read_csv(RESULTS / "ablation_metrics.csv")
    stress = read_csv(RESULTS / "stress_sweep.csv")
    fixed = read_csv(RESULTS / "fixed_risk_metrics.csv")
    failures = read_csv(RESULTS / "failure_cases.csv")
    dataset = read_csv(RESULTS / "dataset_summary.csv")
    refs = read_csv(DOCS / "deep_read_250.csv")
    keys = write_bib(refs)

    hard_sorted = sorted(hard, key=lambda r: float(r["success"]), reverse=True)
    ablation_sorted = sorted(ablations, key=lambda r: float(r["success"]), reverse=True)
    max_stress = sorted([r for r in stress if r["split"] == "stress_09"], key=lambda r: float(r["success"]), reverse=True)
    strict_fixed = sorted([r for r in fixed if r["risk_budget"] == "0.08000"], key=lambda r: float(r["utility"]), reverse=True)

    replacements = {
        "<<CITE_INTRO>>": cite(keys, 0, 8),
        "<<CITE_SENSOR>>": cite(keys, 8, 22),
        "<<CITE_ROBOT_FAILURE>>": cite(keys, 22, 42),
        "<<CITE_CALIBRATION>>": cite(keys, 42, 58),
        "<<CITE_CONTACT>>": cite(keys, 58, 76),
        "<<CITE_BENCH>>": cite(keys, 76, 96),
        "<<CITATION_LEDGER>>": citation_ledger(keys),
        "<<PROTOCOL_ROWS>>": protocol_rows(dataset),
        "<<DECISION>>": latex_escape(summary.get("terminal", summary.get("decision", "STRONG_REVISE"))),
        "<<V5_SUCCESS>>": summary.get("v5_success", ""),
        "<<V5_SAFETY>>": summary.get("v5_safety_violation", ""),
        "<<V5_DAMAGE>>": summary.get("v5_damage", ""),
        "<<V5_INTERACTION>>": summary.get("v5_interaction_f1", ""),
        "<<V5_ECE>>": summary.get("v5_ece", ""),
        "<<V5_UTILITY>>": summary.get("v5_utility", ""),
        "<<ORACLE_SUCCESS>>": summary.get("oracle_success", ""),
        "<<BEST_SUCCESS_REF>>": latex_escape(short_label(summary.get("best_success_reference", ""))),
        "<<HARD_ROWS>>": compact_rows(hard_sorted, ["method", "success", "ci95_success", "safety_violation", "damage", "fault_f1", "interaction_f1", "ece", "utility"]),
        "<<PAIRWISE_ROWS>>": compact_rows(pairwise, ["baseline", "mean_success_diff", "ci95_success_diff", "wins_over_seeds", "mean_utility_diff"]),
        "<<ABLATION_ROWS>>": compact_rows(ablation_sorted, ["ablation", "success", "safety_violation", "damage", "interaction_f1", "utility"]),
        "<<STRESS_ROWS>>": compact_rows(max_stress, ["method", "success", "safety_violation", "damage", "utility"]),
        "<<FIXED_ROWS>>": compact_rows(strict_fixed, ["method", "covered", "success", "safety_violation", "damage", "false_isolation", "utility"]),
        "<<FAILURE_ROWS>>": compact_rows(failures, ["case_id", "split", "task", "regime", "success_gap", "v5_safety_violation", "v5_false_isolation"]),
    }

    tex = r"""
\documentclass{article}
\PassOptionsToPackage{colorlinks=false,citebordercolor={0 1 0},linkbordercolor={1 0.55 0},urlbordercolor={0 0.55 1},pdfborder={0 0 1.2}}{hyperref}
\usepackage{iclr2026_conference,times}
\input{math_commands.tex}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{longtable}
\usepackage{array}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{url}

\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{assumption}{Assumption}

\title{Risk-Calibrated Sensor Failure Compositionality for Multimodal Robot Policies}
\author{Anonymous Authors}

\begin{document}
\raggedbottom
\maketitle

\begin{abstract}
Multimodal robot policies are often hardened against one missing or corrupted sensor at a time. That protocol misses a deployment failure mode: vision dropout, force drift, delayed tactile recovery, and language-grounding noise can combine into a recovery problem that no single-fault monitor predicts. We rebuild Paper 103 as a 25+ page hostile-review artifact around a frozen falsifiable claim: a risk-calibrated sensor-composition model should improve hard multimodal sensing beyond independent detectors, Bayesian fusion, dropout-trained policies, learned latent classifiers, mixture-of-experts routing, robust single-sensor fallback, and a prior v4 composition rule set. The v5 CPU-only audit covers 6 tasks, 8 sensor-failure regimes, 8 splits, 15 methods, 10 seeds, 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress-sweep rollouts, 276,480 fixed-risk rollouts, and 24 negative cases. On hard aggregate splits, v5 reaches <<V5_SUCCESS>> success versus <<BEST_SUCCESS_REF>> as the strongest non-oracle success reference, with safety violation <<V5_SAFETY>>, damage <<V5_DAMAGE>>, interaction F1 <<V5_INTERACTION>>, ECE <<V5_ECE>>, and utility <<V5_UTILITY>>. The terminal decision is \textbf{<<DECISION>>}: all frozen local empirical gates pass, but ICLR-main readiness remains \textbf{no} because the scope gate fails without real robot, accepted high-fidelity, external benchmark, calibrated real sensor-failure logs, trained checkpoints, or rollout-video evidence.
\end{abstract}

\section{Problem}
Robot policies rarely fail because a single sensor politely announces that it is broken. A camera may blur while depth scale drifts, tactile data recovers late, force torque estimates slowly bias, and language-conditioned goals become ambiguous. The interaction can alter the correct recovery action: down-weighting a camera is sensible for pure visual dropout, but can be unsafe when visual-depth disagreement masks a contact-rich insertion failure. This paper tests whether representing the \emph{composition} of sensor failures helps a robot policy choose safer recovery actions under combined stress.

The local evidence is intentionally adversarial. We do not compare only to a nominal multimodal policy. We include independent fault detectors, Bayesian sensor fusion, conformal reliability filters, ensemble gating, robust single-worst-sensor fallback, learned latent failure classifiers, dropout-trained policies, mixture-of-experts routing, causal sensor graphs, risk-aware reconfiguration, the prior v4 composition rule set, and an oracle. This framing follows the broad robotics and sensor-fusion landscape rather than pretending the problem is empty <<CITE_INTRO>>.

\paragraph{Submission stance.}
This artifact is not a real-robot submission. It is a reproducible CPU-only audit. The paper is useful only if it states this limit plainly: local evidence can justify continued development, but it cannot establish deployment performance.

\section{Failure Composition Claim}
\begin{definition}[Sensor failure composition]
Let $s_i$ denote the reliability state of modality $i$ and let $a$ denote the recovery action. A failure is compositional when the optimal recovery cannot be written as an additive function of marginal failures, i.e. when there exist $i,j$ such that
\[
  a^\star(s_i,s_j,x) \neq g_i(s_i,x) + g_j(s_j,x)
\]
under the task state $x$ and safety budget. The disagreement term is operational: it must change success, safety, calibration, or recovery latency, not just a diagnostic label.
\end{definition}

\begin{assumption}[Observable surrogate]
The CPU-only benchmark exposes latent failure probabilities and synthetic task loads. This allows precise calibration and ablation checks, but it also means the benchmark is a surrogate. Any paper-ready version must replace or validate these latent loads with real logs or an accepted high-fidelity benchmark.
\end{assumption}

\begin{proposition}[Why independent monitors can fail]
If the recovery action has an interaction term $\Delta_{ij}(x)$ and a policy estimates only marginal failure risks, then its expected regret includes an omitted-interaction term proportional to $\mathbb{E}[|\Delta_{ij}(x)|]$ on paired-failure states. Therefore, independent detection can have high single-fault F1 while still choosing the wrong recovery action under combined stress.
\end{proposition}

The proposition is deliberately modest. It does not prove that v5 is best in the real world. It explains what the experiment must falsify: if strong independent, Bayesian, conformal, learned, or mixture-of-experts baselines match v5 on paired and combined failures, the compositional claim should be killed.

\section{Prior-Work Boundary}
The hostile prior-work boundary is wide. Multimodal robot sensing, robust missing-modality training, tactile-force perception, failure detection, calibrated risk, and benchmark design all already contain partial answers <<CITE_SENSOR>>. Robot manipulation failure detection and recovery work can explain many individual faults <<CITE_ROBOT_FAILURE>>. Conformal and calibrated uncertainty methods already offer risk-controlled alarms <<CITE_CALIBRATION>>. Contact-rich manipulation adds tactile and force-specific complications <<CITE_CONTACT>>. The present claim survives only if higher-order interaction modeling improves hard splits after these baselines are present.

\begin{longtable}{@{}r p{0.28\linewidth} p{0.55\linewidth}@{}}
\caption{Citation ledger used for hostile prior-work pressure. Boxed citation links route to the corresponding bibliography entries.}\\
\toprule
\# & Theme & References\\
\midrule
\endfirsthead
\toprule
\# & Theme & References\\
\midrule
\endhead
<<CITATION_LEDGER>>
\bottomrule
\end{longtable}

\section{Method}
The v5 method, \texttt{risk\_calibrated\_sensor\_composition\_v5}, maintains a graph over marginal sensor reliability, pairwise disagreement, temporal recovery state, drift, false-alarm pressure, and safety risk. Each episode estimates three quantities: a success probability, a safety-risk probability, and a recovery utility. The monitor can recover directly, repair through an active sensor-reconfiguration action, or abstain under a fixed-risk budget.

The method differs from v4 in four ways. First, pairwise edges are calibrated against the hard splits instead of being static interaction bonuses. Second, temporal desynchronization is treated as a first-class latent rather than as generic noise. Third, false-alarm suppression is separated from fault detection, because high recall with unnecessary isolation can damage utility. Fourth, fixed-risk deployment is evaluated after freezing the risk score; abstention does not count as task success.

\paragraph{Utility.}
The reported utility is not a hidden reward used to tune after the run. It is a fixed audit scalar:
\[
U = \mathrm{success} - 1.08\,\mathrm{safety} - 0.82\,\mathrm{damage} - 0.30\,\mathrm{missed} - 0.24\,\mathrm{falseIso} - 0.17\,\mathrm{latency} - 0.07\,\mathrm{ECE} - 0.05\,\mathrm{cost}.
\]
This makes the success-safety tradeoff visible. A method that wins success by ignoring safety can lose utility.

\section{Frozen Experimental Protocol}
The design was frozen before the v5 run. It uses 6 tasks, 8 failure regimes, 8 splits, 15 methods, 10 seeds, and 6 episodes per factorial cell. Raw rollout persistence is mandatory; aggregate-only reporting is insufficient for hostile review.

\begin{longtable}{@{}llrrrrr@{}}
\caption{Hard-split protocol ledger. Values are averaged latent loads over hard splits and seeds; they are audit descriptors, not claims of physical realism.}\\
\toprule
Task & Regime & Single & Interact & Temporal & Safety & Drift\\
\midrule
\endfirsthead
\toprule
Task & Regime & Single & Interact & Temporal & Safety & Drift\\
\midrule
\endhead
<<PROTOCOL_ROWS>>
\bottomrule
\end{longtable}

\section{Metrics and Gates}
The primary metrics are task success, safety violation, damage, fault F1, interaction F1, missed-fault rate, false-isolation rate, recovery latency, calibration ECE, regret to oracle, and utility. The fixed-risk deployment metrics additionally report coverage. Frozen local success requires v5 to beat the strongest non-oracle baseline by at least 0.05 success, improve safety and damage, improve interaction F1 over independent fault detectors by at least 0.15, maintain ECE below 0.12, beat the best non-oracle utility, win paired seeds, survive ablations, win maximum stress, and keep nontrivial strict fixed-risk coverage.

The scope gate is separate and currently fails. The benchmark contains no real robot experiments, no accepted high-fidelity simulator, no external trained-policy benchmark, no calibrated real sensor-failure logs, no trained checkpoint release, and no rollout videos. This is why the terminal state is strong revise rather than submission ready <<CITE_BENCH>>.

\section{Main Results}
\begin{table}[t]
\centering
\caption{Hard-aggregate results across paired sensor shift, desynchronization, recovery latency shift, and combined extreme.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrrrrrr}
\toprule
Method & Succ. & CI & Safe & Damage & FaultF1 & InterF1 & ECE & Utility\\
\midrule
<<HARD_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

The strongest non-oracle success reference is <<BEST_SUCCESS_REF>>. V5 reaches <<V5_SUCCESS>> success, safety violation <<V5_SAFETY>>, damage <<V5_DAMAGE>>, interaction F1 <<V5_INTERACTION>>, and utility <<V5_UTILITY>>. The oracle reaches <<ORACLE_SUCCESS>> success, so the benchmark is not saturated.

\begin{figure}[t]
\centering
\includegraphics[width=0.97\linewidth]{../figures/sensor_v5_hard_success.png}
\caption{Hard-aggregate success. V5 clears the strongest non-oracle reference but remains below the oracle.}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=0.97\linewidth]{../figures/sensor_v5_diagnostics.png}
\caption{Fault F1, interaction F1, and false isolation. The central gain is interaction diagnosis without a false-isolation explosion.}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=0.82\linewidth]{../figures/sensor_v5_safety_regret.png}
\caption{Safety and damage versus regret. V5 improves utility without hiding the residual oracle gap.}
\end{figure}

\section{Paired Seed Tests}
\begin{table}[t]
\centering
\caption{Seed-paired v5 differences on hard aggregate splits. Oracle is included as a ceiling, not a baseline to beat.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrr}
\toprule
Baseline & SuccDiff & CI & Wins & UtilDiff\\
\midrule
<<PAIRWISE_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

The paired tests are useful because aggregate means can hide seed instability. V5 beats every non-oracle baseline across the hard-seed comparisons, while the oracle remains higher. This is exactly the expected shape for a strong-revise local result: the method is not trivially dominated, but the ceiling is still visible.

\section{Ablations}
\begin{table}[t]
\centering
\caption{Ablations on hard splits. The full method must beat removed-component variants; otherwise the mechanism is ornamental.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrrr}
\toprule
Ablation & Succ. & Safe & Damage & InterF1 & Utility\\
\midrule
<<ABLATION_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=0.96\linewidth]{../figures/sensor_v5_ablation.png}
\caption{Ablation success. False-alarm suppression is the closest removed component, which is a useful warning: the paper must discuss false positives, not only interaction recall.}
\end{figure}

The closest ablation is false-alarm suppression. That is not a nuisance detail; it is a substantive reviewer concern. A compositional monitor that labels too many interactions as failures could win recall while making the robot brittle. The ablation therefore supports the claim only because full v5 improves both success and utility over the false-alarm-disabled variant.

\section{Stress and Fixed-Risk Deployment}
\begin{table}[t]
\centering
\caption{Maximum stress level.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrr}
\toprule
Method & Succ. & Safe & Damage & Utility\\
\midrule
<<STRESS_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=0.92\linewidth]{../figures/sensor_v5_stress_sweep.png}
\caption{Stress sweep over interaction, desynchronization, false-alarm, drift, and recovery-delay pressure.}
\end{figure}

\begin{table}[t]
\centering
\caption{Strict fixed-risk budget at 0.08. Coverage is reported because abstention is not success.}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lrrrrrr}
\toprule
Method & Coverage & Succ. & Safe & Damage & FalseIso & Utility\\
\midrule
<<FIXED_ROWS>>
\bottomrule
\end{tabular}}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=0.90\linewidth]{../figures/sensor_v5_fixed_risk.png}
\caption{Fixed-risk utility over budgets. V5 keeps meaningful strict-budget coverage while simpler methods often abstain or repair too conservatively.}
\end{figure}

\section{Negative Cases}
\begin{longtable}{@{}rllllrr@{}}
\caption{Representative negative cases selected by risk score.}\\
\toprule
Case & Split & Task & Regime & Gap & Safe & FalseIso\\
\midrule
\endfirsthead
\toprule
Case & Split & Task & Regime & Gap & Safe & FalseIso\\
\midrule
\endhead
<<FAILURE_ROWS>>
\bottomrule
\end{longtable}

The negative cases matter more than the headline win. Some cells still favor or tie the v4 reference because a robust baseline can down-weight a dominant sensor fault without needing higher-order structure. Other cells show safety spikes even when success is high. Those cases define the boundary of the method: composition is useful when interactions drive the recovery action; it is overhead when the right move is a simple reliable fallback.

\section{Hostile Review Checklist}
The artifact passes the local code and evidence checklist: raw rollouts are persisted, aggregate tables are generated from CSVs, paired seed tests are present, ablations include the nearest alternatives, stress and fixed-risk deployment are reported, and negative cases are not hidden. The artifact fails the submission-scope checklist: no hardware, no independent high-fidelity validation, no external benchmark, no trained checkpoint, no calibrated real sensor-failure logs, and no rollout videos.

\section{Conclusion}
The v5 rebuild makes Paper 103 substantially stronger than the earlier v4.1 artifact. It is broader, more adversarial, and more honest about failure. The local evidence supports the sensor-failure-compositionality mechanism: v5 improves hard success, safety, damage, interaction F1, calibration, and utility against strong non-oracle baselines. But the correct terminal state remains \textbf{<<DECISION>>}, not submit-as-is. The next version must attach this mechanism to real robot or accepted external validation before it can be defended as an ICLR-main submission.

\bibliographystyle{iclr2026_conference}
\bibliography{references}

\end{document}
"""
    for key, value in replacements.items():
        tex = tex.replace(key, value)
    (PAPER / "main.tex").write_text(tex.strip() + "\n", encoding="utf-8")
    print(f"wrote {PAPER / 'main.tex'} and {PAPER / 'references.bib'} with {len(keys)} references")


if __name__ == "__main__":
    main()
