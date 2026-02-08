# lecture03_demos.py
# AI-Enabled Informatics for Engineers — Lecture 03
# Dataset Engineering + Informatics Reliability Demo
# Aligned to Chip Huyen Chapter 8

import argparse
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def maybe_show(show_plots: bool) -> None:
    """
    In Colab/Jupyter, plt.show() will render inline.
    We keep it optional so scripts can run headless in CI/Azure too.
    """
    if show_plots:
        plt.show()


# -------------------------------------------------------------------
# DEMO 1 — Synthetic dataset with intentional problems
# -------------------------------------------------------------------
def generate_data(n: int = 3000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "source": rng.choice(["alpha", "bravo", "charlie"], size=n),
        "week": rng.integers(1, 13, size=n),
        "load": rng.normal(0, 1, size=n),
        "latency_ms": rng.lognormal(4.2, 0.35, size=n),
        "quality_score": np.clip(rng.normal(0.75, 0.12, size=n), 0, 1)
    })

    # derived label: risk_flag (synthetic but structured)
    logits = (
        df["load"] * 0.8
        + (df["latency_ms"] - df["latency_ms"].mean()) * 0.01
        - (df["quality_score"] - 0.7) * 2
    )
    prob = 1 / (1 + np.exp(-logits))
    df["risk_flag"] = rng.binomial(1, np.clip(prob * 0.6, 0, 1))

    # Inject problems (realistic "messiness")
    df.loc[rng.choice(n, int(n * 0.02), replace=False), "latency_ms"] = np.nan          # missing
    df.loc[rng.choice(n, int(n * 0.005), replace=False), "latency_ms"] *= 6            # outliers
    df.loc[rng.choice(n, int(n * 0.003), replace=False), "source"] = "charliee"        # typo category

    return df


# -------------------------------------------------------------------
# DEMO 2 — Schema report (data dictionary starter)
# -------------------------------------------------------------------
def schema_report(df: pd.DataFrame, path: str) -> None:
    lines = []
    for c in df.columns:
        s = df[c]
        lines.append(f"{c} | dtype={s.dtype} | missing={s.isna().mean():.2%}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# -------------------------------------------------------------------
# DEMO 3 — Quality diagnostics + visualizations
# -------------------------------------------------------------------
def quality_plots(df: pd.DataFrame, out_dir: str, show_plots: bool) -> None:
    # Missingness
    missing = df.isna().mean().sort_values(ascending=False)
    ax = missing.plot(kind="bar", title="Missingness by Column")
    ax.set_ylabel("Fraction missing")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/missingness.png", dpi=160)
    maybe_show(show_plots)
    plt.close()

    # Correlation (numeric only)
    num = df.select_dtypes(include=[np.number])
    corr = num.corr(numeric_only=True)
    plt.imshow(corr, aspect="auto")
    plt.title("Correlation (numeric columns)")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.index)), corr.index)
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f"{out_dir}/correlation.png", dpi=160)
    maybe_show(show_plots)
    plt.close()

    # Latency distribution (raw)
    plt.hist(df["latency_ms"].dropna(), bins=60)
    plt.title("Latency Distribution (raw)")
    plt.xlabel("latency_ms")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/latency_hist_raw.png", dpi=160)
    maybe_show(show_plots)
    plt.close()


# -------------------------------------------------------------------
# DEMO 4 — Cleaning policy (explicit, reproducible)
# -------------------------------------------------------------------
def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Policy 1: normalize category typos
    df["source"] = df["source"].replace({"charliee": "charlie"})

    # Policy 2: impute missing latency by group median (keeps group behavior)
    df["latency_ms"] = df.groupby("source")["latency_ms"].transform(lambda s: s.fillna(s.median()))

    # Policy 3: cap extreme outliers at high quantile (robustness)
    cap = df["latency_ms"].quantile(0.995)
    df["latency_ms"] = df["latency_ms"].clip(upper=cap)

    return df


def cleaning_plots(raw_df: pd.DataFrame, clean_df: pd.DataFrame, out_dir: str, show_plots: bool) -> None:
    # Compare latency histograms pre/post cleaning
    plt.hist(raw_df["latency_ms"].dropna(), bins=60, alpha=0.7, label="raw")
    plt.hist(clean_df["latency_ms"].dropna(), bins=60, alpha=0.7, label="clean")
    plt.title("Latency Distribution: raw vs clean")
    plt.xlabel("latency_ms")
    plt.ylabel("count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out_dir}/latency_hist_raw_vs_clean.png", dpi=160)
    maybe_show(show_plots)
    plt.close()


# -------------------------------------------------------------------
# DEMO 5 — Synthetic text + NLP features (simple, explainable)
# -------------------------------------------------------------------
def text_demo(df: pd.DataFrame, out_dir: str, show_plots: bool) -> None:
    texts = [
        "Latency spike in system",
        "Model output confusing",
        "Performance improved after patch",
        "Data incomplete for source",
        "Too many false alarms from rules"
    ]

    # attach text "feedback" to sampled rows
    sample = df.sample(500, random_state=0).reset_index(drop=True)
    feedback = pd.DataFrame({
        "source": sample["source"],
        "week": sample["week"],
        "risk_flag": sample["risk_flag"],
        "text": np.random.choice(texts, len(sample))
    })

    vec = CountVectorizer(stop_words="english")
    X = vec.fit_transform(feedback["text"])

    counts = np.asarray(X.sum(axis=0)).ravel()
    terms = vec.get_feature_names_out()

    # Simple visualization: term frequency
    plt.bar(terms, counts)
    plt.title("Term Frequency (synthetic feedback)")
    plt.xlabel("term")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/text_terms.png", dpi=160)
    maybe_show(show_plots)
    plt.close()

    feedback.to_csv(f"{out_dir}/text_feedback.csv", index=False)


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
def main(out_dir: str, show_plots: bool, n: int, seed: int) -> None:
    ensure_dir(out_dir)

    # Generate + save raw
    raw_df = generate_data(n=n, seed=seed)
    raw_df.to_csv(f"{out_dir}/raw.csv", index=False)

    # Schema + quality diagnostics
    schema_report(raw_df, f"{out_dir}/schema.txt")
    quality_plots(raw_df, out_dir, show_plots)

    # Clean + save
    clean_df = clean(raw_df)
    clean_df.to_csv(f"{out_dir}/clean.csv", index=False)
    cleaning_plots(raw_df, clean_df, out_dir, show_plots)

    # Text demo
    text_demo(clean_df, out_dir, show_plots)

    print("\n✅ Lecture 03 demo complete.")
    print(f"Artifacts written to: {out_dir}/")
    print("Key outputs:")
    print("  - raw.csv, clean.csv, schema.txt")
    print("  - missingness.png, correlation.png, latency_hist_*.png")
    print("  - text_feedback.csv, text_terms.png\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", default="artifacts", help="Where to write outputs")
    parser.add_argument("--show_plots", type=int, default=0, choices=[0, 1],
                        help="1 = display plots inline (Colab). Always saves PNGs.")
    parser.add_argument("--n", type=int, default=3000, help="Number of rows to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    main(out_dir=args.out_dir, show_plots=bool(args.show_plots), n=args.n, seed=args.seed)
