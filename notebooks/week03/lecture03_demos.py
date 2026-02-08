# lecture03_demos.py
# =============================================================================
# AI-Enabled Informatics for Engineers — Week 03 Demos (Lecture 03)
#
# PURPOSE (for students)
#   This file is a *single runnable demo script* that supports Lecture 03.
#   Lecture 03 is about data + informatics: dataset quality, schema, provenance,
#   synthetic data, and building “analysis-ready” artifacts you can trust.
#
#   You will generate:
#     - A realistic synthetic tabular dataset (with intentional issues)
#     - A simple “data dictionary” / schema report
#     - Data quality diagnostics (missingness, outliers, correlations)
#     - A cleaned “analysis-ready” dataset
#     - A synthetic text dataset (short feedback strings) + basic NLP features
#     - Plots and CSVs that map to the lecture sections
#
# OUTPUTS (written to --out_dir, default: artifacts/)
#   artifacts/
#     01_raw_tabular.csv
#     02_schema_report.txt
#     03_quality_summary.json
#     04_missingness_by_column.csv
#     05_outlier_rows.csv
#     06_clean_tabular.csv
#     07_text_feedback.csv
#     08_text_features.csv
#     plot_missingness.png
#     plot_correlation.png
#     plot_value_distributions.png
#     plot_text_top_terms.png
#
# =============================================================================
# HOW TO RUN (Google Colab — recommended)
#
# IMPORTANT: In Colab you clone the *repo root*, not a subfolder URL.
#
# 1) In Colab, run a cell like this (replace with your repo URL):
#
#    !git clone https://github.com/<ORG>/<REPO>.git
#    %cd <REPO>/notebooks/week03
#    !pip -q install pandas numpy matplotlib scikit-learn
#    !python lecture03_demos.py --out_dir artifacts --show_plots 1
#
# 2) After it runs, open the artifacts/ folder in the left Colab file browser.
#
# =============================================================================
# HOW TO RUN (Local)
#   cd notebooks/week03
#   python -m venv .venv
#   # Windows: .venv\Scripts\activate
#   # Mac/Linux: source .venv/bin/activate
#   pip install pandas numpy matplotlib scikit-learn
#   python lecture03_demos.py --out_dir artifacts --show_plots 1
#
# =============================================================================
# WHY THIS MATTERS (Lecture 03 linkage)
#   Informatics is about making data *usable, interpretable, and trustworthy*.
#   AI is powerful, but “garbage in → garbage out” is still undefeated.
#   The goal this week is to show that:
#     - Schema + meaning (not just files) is an engineering responsibility
#     - Synthetic data can be a safe, fast stand-in for prototyping
#     - Quality checks should be repeatable, automated, and visible
#
# =============================================================================
# TROUBLESHOOTING (Colab)
#   If it fails, it’s usually one of these:
#     - You didn’t cd into the correct folder (week03)
#     - Dependencies not installed: re-run pip install
#     - Filename mismatch: ensure this file is named EXACTLY lecture03_demos.py
#
# =============================================================================

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

# Matplotlib: use a non-interactive backend-safe approach for notebook/Colab
import matplotlib
matplotlib.use("Agg")  # safe in Colab and headless environments
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer


# -----------------------------------------------------------------------------
# Small utilities
# -----------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_fig(path: str, show_plots: bool) -> None:
    """Save a figure; optionally display when running interactively."""
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    if show_plots:
        # In Colab, Agg won't auto-display; this still works in many setups.
        # Students can open the PNGs from artifacts/ regardless.
        try:
            from IPython.display import display
            display(plt.gcf())
        except Exception:
            pass
    plt.close()


def write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def write_json(path: str, obj: Dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


# -----------------------------------------------------------------------------
# Demo 1: Generate a realistic synthetic TABULAR dataset (with intentional issues)
# -----------------------------------------------------------------------------

@dataclass
class TabularConfig:
    n: int = 4000
    seed: int = 42


def generate_tabular(cfg: TabularConfig) -> pd.DataFrame:
    """
    Creates a synthetic dataset meant to resemble operational/engineering data.
    You can imagine this as: tickets, incidents, device telemetry summaries,
    or quality-control measurements.

    Intentional issues injected (on purpose, to practice informatics):
      - missing values in a critical field
      - outliers in a numeric field
      - inconsistent category label (typo)
    """
    rng = np.random.default_rng(cfg.seed)

    # Categorical “source” could be region, unit, product line, etc.
    source = rng.choice(["alpha", "bravo", "charlie"], size=cfg.n, p=[0.55, 0.30, 0.15])

    # A “week” feature to hint at time windows and drift analysis later
    week = rng.integers(1, 13, size=cfg.n)

    # Continuous measures
    load = rng.normal(loc=0.0, scale=1.0, size=cfg.n) + (week - 6) * 0.08  # slight trend
    latency_ms = rng.lognormal(mean=4.2, sigma=0.35, size=cfg.n)  # positive skew

    # A bounded score
    quality_score = np.clip(rng.normal(loc=0.75, scale=0.12, size=cfg.n), 0.0, 1.0)

    # Risk-ish label derived from a rule (not “truth”, but a plausible toy process)
    # Higher load + higher latency + lower quality → higher risk
    logits = 0.9 * load + 0.012 * (latency_ms - latency_ms.mean()) - 2.0 * (quality_score - 0.7)
    prob = 1 / (1 + np.exp(-logits))
    risk_flag = rng.binomial(1, p=np.clip(prob * 0.65, 0, 1), size=cfg.n)  # mild imbalance

    df = pd.DataFrame(
        {
            "source": source,
            "week": week,
            "load": load.astype(float),
            "latency_ms": latency_ms.astype(float),
            "quality_score": quality_score.astype(float),
            "risk_flag": risk_flag.astype(int),
        }
    )

    # --- Inject intentional issues ---
    # Missingness in latency_ms (simulate sensor dropouts)
    miss_idx = rng.choice(cfg.n, size=int(cfg.n * 0.015), replace=False)
    df.loc[miss_idx, "latency_ms"] = np.nan

    # Outliers in latency_ms (simulate rare extreme incidents)
    out_idx = rng.choice(cfg.n, size=int(cfg.n * 0.004), replace=False)
    df.loc[out_idx, "latency_ms"] = df.loc[out_idx, "latency_ms"] * rng.uniform(4, 8, size=len(out_idx))

    # Category typo (simulate data entry inconsistency)
    typo_idx = rng.choice(cfg.n, size=int(cfg.n * 0.002), replace=False)
    df.loc[typo_idx, "source"] = "charliee"  # typo on purpose

    return df


# -----------------------------------------------------------------------------
# Demo 2: Schema/Data Dictionary report (lightweight, lecture-friendly)
# -----------------------------------------------------------------------------

def schema_report(df: pd.DataFrame) -> str:
    """
    A simple data dictionary: column types, missingness, ranges, and categories.
    This is informatics: turning “data” into “understood data”.
    """
    lines: List[str] = []
    lines.append("SCHEMA + DATA DICTIONARY REPORT (Lecture 03)")
    lines.append(f"Generated: {now_iso()}")
    lines.append(f"Rows: {len(df):,}")
    lines.append("")

    for col in df.columns:
        s = df[col]
        lines.append(f"Column: {col}")
        lines.append(f"  dtype: {s.dtype}")
        lines.append(f"  missing: {int(s.isna().sum())} ({(s.isna().mean()*100):.2f}%)")

        if pd.api.types.is_numeric_dtype(s):
            lines.append(f"  min/max: {np.nanmin(s):.4g} / {np.nanmax(s):.4g}")
            lines.append(f"  mean/std: {np.nanmean(s):.4g} / {np.nanstd(s):.4g}")
        else:
            # show top categories
            vc = s.value_counts(dropna=False).head(8)
            lines.append("  top values:")
            for k, v in vc.items():
                lines.append(f"    - {repr(k)}: {v}")

        lines.append("")

    # quick “risk framing” reminder (ties to informatics and later evaluation/monitoring)
    lines.append("NOTES (why you care):")
    lines.append("- Missingness can bias metrics and training; document your handling policy.")
    lines.append("- Category typos create silent fragmentation (two buckets that should be one).")
    lines.append("- Outliers can dominate averages; always inspect distributions.")
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Demo 3: Data quality diagnostics (missingness, outliers, correlation)
# -----------------------------------------------------------------------------

def summarize_quality(df: pd.DataFrame) -> Tuple[Dict, pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      - a dict quality summary
      - missingness table
      - outlier rows table (simple z-score approach on numeric cols)
    """
    summary: Dict = {
        "generated_utc": now_iso(),
        "rows": int(len(df)),
        "columns": list(df.columns),
    }

    missing = (
        df.isna().mean()
        .rename("missing_rate")
        .to_frame()
        .sort_values("missing_rate", ascending=False)
        .reset_index()
        .rename(columns={"index": "column"})
    )

    summary["missing_rate_by_column"] = {
        row["column"]: float(row["missing_rate"]) for _, row in missing.iterrows()
    }

    # Outliers: z-score on numeric columns (robust enough for a teaching demo)
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    outlier_mask = np.zeros(len(df), dtype=bool)

    for c in num_cols:
        s = df[c].to_numpy(dtype=float)
        mu = np.nanmean(s)
        sd = np.nanstd(s) + 1e-9
        z = (s - mu) / sd
        outlier_mask |= (np.abs(z) > 4.5)  # stricter threshold: “rare extremes”

    outliers = df.loc[outlier_mask].copy()
    summary["outlier_rows_detected"] = int(len(outliers))

    return summary, missing, outliers


def plot_missingness(missing_df: pd.DataFrame, out_path: str, show_plots: bool) -> None:
    plt.figure()
    plt.bar(missing_df["column"], missing_df["missing_rate"])
    plt.title("Missingness by Column (Lecture 03)")
    plt.xlabel("Column")
    plt.ylabel("Missing rate")
    plt.xticks(rotation=30, ha="right")
    save_fig(out_path, show_plots)


def plot_correlation(df: pd.DataFrame, out_path: str, show_plots: bool) -> None:
    num_df = df.select_dtypes(include=[np.number]).copy()
    corr = num_df.corr(numeric_only=True)
    plt.figure()
    plt.imshow(corr)
    plt.title("Numeric Feature Correlation (Lecture 03)")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=30, ha="right")
    plt.yticks(range(len(corr.columns)), corr.columns)
    for (i, j), v in np.ndenumerate(corr.to_numpy()):
        plt.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8)
    save_fig(out_path, show_plots)


def plot_distributions(df: pd.DataFrame, out_path: str, show_plots: bool) -> None:
    """
    A single figure with multiple histograms is often done via subplots.
    BUT: you asked earlier to avoid subplots when charting *for the user* via python tool.
    Here, we're generating a single PNG for students. Subplots are reasonable and common.
    """
    num_cols = ["load", "latency_ms", "quality_score"]
    plt.figure(figsize=(10, 3))
    for i, c in enumerate(num_cols, 1):
        plt.subplot(1, 3, i)
        plt.hist(df[c].dropna().to_numpy(), bins=30)
        plt.title(c)
    plt.suptitle("Value Distributions (Lecture 03)")
    save_fig(out_path, show_plots)


# -----------------------------------------------------------------------------
# Demo 4: Cleaning policy (explicit, repeatable)
# -----------------------------------------------------------------------------

def clean_tabular(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning is a POLICY decision. We make it explicit for students:

    Policy:
      1) Fix known category typos:
         - "charliee" -> "charlie"
      2) Handle missing latency:
         - Impute with median per source (simple, transparent baseline)
      3) Handle extreme outliers in latency:
         - Winsorize (cap) at 99.5 percentile
    """
    out = df.copy()

    # 1) Category normalization
    out["source"] = out["source"].replace({"charliee": "charlie"})

    # 2) Impute missing latency by median per source
    out["latency_ms"] = out.groupby("source")["latency_ms"].transform(
        lambda s: s.fillna(s.median())
    )

    # 3) Cap extreme outliers (winsorize)
    cap = out["latency_ms"].quantile(0.995)
    out["latency_ms"] = out["latency_ms"].clip(upper=float(cap))

    return out


# -----------------------------------------------------------------------------
# Demo 5: Synthetic TEXT data + basic NLP features (informatics meets AI)
# -----------------------------------------------------------------------------

TEXT_TEMPLATES = [
    "Latency spikes when load is high",
    "System feels slow after update",
    "Quality improved this week",
    "Too many false alarms in monitoring",
    "Dashboard is helpful but confusing",
    "Needs clearer documentation",
    "Data seems incomplete for {source}",
    "Model output is hard to interpret",
    "Great performance in segment {source}",
    "Unexpected errors when traffic shifts",
]

TEXT_LABELS = [
    "performance",
    "reliability",
    "usability",
    "data_quality",
    "explainability",
]


def generate_text_feedback(df_clean: pd.DataFrame, seed: int) -> pd.DataFrame:
    """
    Create small synthetic “feedback” rows aligned to the tabular dataset.
    We attach feedback to source + week to show how informatics metadata matters.
    """
    rng = np.random.default_rng(seed)
    n = min(len(df_clean), 1200)  # keep it manageable
    sample = df_clean.sample(n=n, random_state=seed).reset_index(drop=True)

    texts = []
    topics = []
    for _, row in sample.iterrows():
        template = rng.choice(TEXT_TEMPLATES)
        txt = template.format(source=row["source"])
        # Add mild variation
        if rng.random() < 0.35:
            txt += f" (week {int(row['week'])})"
        texts.append(txt)

        # Topic heuristic: ties to lecture point that labels can be engineered/heuristic early
        if "Latency" in txt or "slow" in txt:
            topics.append("performance")
        elif "false alarms" in txt or "errors" in txt:
            topics.append("reliability")
        elif "confusing" in txt or "documentation" in txt:
            topics.append("usability")
        elif "incomplete" in txt:
            topics.append("data_quality")
        else:
            topics.append("explainability")

    feedback = pd.DataFrame(
        {
            "source": sample["source"],
            "week": sample["week"],
            "feedback_text": texts,
            "topic_label": topics,
        }
    )
    return feedback


def text_features(feedback: pd.DataFrame, out_dir: str, show_plots: bool) -> pd.DataFrame:
    """
    Build simple NLP features: term counts (bag-of-words).
    This is a deliberate “Week 03” approach: start simple before embeddings/transformers.
    """
    vec = CountVectorizer(stop_words="english", max_features=30)
    X = vec.fit_transform(feedback["feedback_text"])
    terms = vec.get_feature_names_out()

    feats = pd.DataFrame(X.toarray(), columns=[f"term_{t}" for t in terms])
    feats.insert(0, "topic_label", feedback["topic_label"].values)

    # Plot top terms overall
    counts = np.asarray(X.sum(axis=0)).ravel()
    order = np.argsort(counts)[::-1]
    top_terms = terms[order][:15]
    top_counts = counts[order][:15]

    plt.figure()
    plt.bar(top_terms, top_counts)
    plt.title("Top Terms in Synthetic Feedback (Lecture 03)")
    plt.xlabel("Term")
    plt.ylabel("Count")
    plt.xticks(rotation=35, ha="right")
    save_fig(os.path.join(out_dir, "plot_text_top_terms.png"), show_plots)

    return feats


# -----------------------------------------------------------------------------
# Main runner
# -----------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", type=str, default="artifacts")
    ap.add_argument("--show_plots", type=int, default=0)
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    out_dir = args.out_dir
    show_plots = bool(args.show_plots)
    ensure_dir(out_dir)

    print("\n=== Lecture 03 Demos: Data + Informatics (Week 03) ===")
    print(f"Output directory: {out_dir}")
    print("If you are in Colab, open the artifacts/ folder after the run.\n")

    # -------------------------------------------------------------------------
    # DEMO 1: Generate raw tabular data
    # -------------------------------------------------------------------------
    print("[DEMO 1] Generating synthetic tabular dataset (with intentional issues)...")
    raw = generate_tabular(TabularConfig(n=args.n, seed=args.seed))
    raw_path = os.path.join(out_dir, "01_raw_tabular.csv")
    raw.to_csv(raw_path, index=False)
    print(f"  Saved: {raw_path}")

    # -------------------------------------------------------------------------
    # DEMO 2: Create schema/data dictionary report
    # -------------------------------------------------------------------------
    print("[DEMO 2] Writing schema + data dictionary report...")
    report = schema_report(raw)
    report_path = os.path.join(out_dir, "02_schema_report.txt")
    write_text(report_path, report)
    print(f"  Saved: {report_path}")

    # -------------------------------------------------------------------------
    # DEMO 3: Data quality diagnostics
    # -------------------------------------------------------------------------
    print("[DEMO 3] Running quality diagnostics (missingness, outliers, correlation)...")
    summary, missing_tbl, outliers_tbl = summarize_quality(raw)

    summary_path = os.path.join(out_dir, "03_quality_summary.json")
    write_json(summary_path, summary)
    print(f"  Saved: {summary_path}")

    miss_path = os.path.join(out_dir, "04_missingness_by_column.csv")
    missing_tbl.to_csv(miss_path, index=False)
    print(f"  Saved: {miss_path}")

    out_path = os.path.join(out_dir, "05_outlier_rows.csv")
    outliers_tbl.to_csv(out_path, index=False)
    print(f"  Saved: {out_path}")

    plot_missingness(missing_tbl, os.path.join(out_dir, "plot_missingness.png"), show_plots)
    plot_correlation(raw, os.path.join(out_dir, "plot_correlation.png"), show_plots)
    plot_distributions(raw, os.path.join(out_dir, "plot_value_distributions.png"), show_plots)
    print("  Saved plots: plot_missingness.png, plot_correlation.png, plot_value_distributions.png")

    # -------------------------------------------------------------------------
    # DEMO 4: Cleaning policy → analysis-ready dataset
    # -------------------------------------------------------------------------
    print("[DEMO 4] Cleaning dataset (explicit policy: normalize categories, impute, cap)...")
    clean = clean_tabular(raw)
    clean_path = os.path.join(out_dir, "06_clean_tabular.csv")
    clean.to_csv(clean_path, index=False)
    print(f"  Saved: {clean_path}")

    # -------------------------------------------------------------------------
    # DEMO 5: Synthetic text feedback + basic NLP features
    # -------------------------------------------------------------------------
    print("[DEMO 5] Generating synthetic text feedback + extracting simple NLP features...")
    feedback = generate_text_feedback(clean, seed=args.seed)
    fb_path = os.path.join(out_dir, "07_text_feedback.csv")
    feedback.to_csv(fb_path, index=False)
    print(f"  Saved: {fb_path}")

    feats = text_features(feedback, out_dir=out_dir, show_plots=show_plots)
    feats_path = os.path.join(out_dir, "08_text_features.csv")
    feats.to_csv(feats_path, index=False)
    print(f"  Saved: {feats_path}")

    # -------------------------------------------------------------------------
    # Student reflection prompts (kept inside file by request)
    # -------------------------------------------------------------------------
    reflection = []
    reflection.append("STUDENT NOTES + INSIGHTS (Lecture 03)")
    reflection.append(f"Generated: {now_iso()}")
    reflection.append("")
    reflection.append("1) What did the schema report reveal?")
    reflection.append("   - Which field(s) had missing values? Would that matter for downstream analysis?")
    reflection.append("")
    reflection.append("2) What is an example of 'semantic' data quality (not just type/format)?")
    reflection.append("   - Example: category typo 'charliee' silently creates a new bucket.")
    reflection.append("")
    reflection.append("3) Compare cleaning strategies:")
    reflection.append("   - Why choose median imputation by group (source) instead of global mean?")
    reflection.append("   - Why cap outliers instead of deleting rows?")
    reflection.append("")
    reflection.append("4) How does the text demo connect to informatics?")
    reflection.append("   - The 'topic_label' is a simple heuristic label—good enough for prototyping.")
    reflection.append("   - Next steps later in the course: embeddings, clustering, transformers.")
    reflection.append("")
    reflection.append("5) Practical takeaway:")
    reflection.append("   - If you can’t explain how your dataset was produced and cleaned,")
    reflection.append("     you can’t defend any model built on top of it.")
    reflection.append("")

    notes_path = os.path.join(out_dir, "STUDENT_NOTES.txt")
    write_text(notes_path, "\n".join(reflection))
    print(f"\nSaved student reflection prompts: {notes_path}")

    print("\n=== DONE ===")
    print("Open artifacts/ and review:")
    print(" - 02_schema_report.txt (data dictionary)")
    print(" - 03_quality_summary.json (quick stats)")
    print(" - plot_*.png (visualizations)")
    print(" - 06_clean_tabular.csv (analysis-ready dataset)")
    print(" - 07_text_feedback.csv + 08_text_features.csv (text + NLP features)\n")


if __name__ == "__main__":
    main()
