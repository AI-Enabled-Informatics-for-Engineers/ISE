# lecture03_demos.py
# AI-Enabled Informatics for Engineers — Lecture 03
# Dataset Engineering + Informatics Reliability Demo
# Aligned to Chip Huyen Chapter 8

import argparse
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


# -------------------------------------------------------------------
# DEMO 1 — Synthetic dataset with intentional problems
# -------------------------------------------------------------------
def generate_data(n=3000, seed=42):
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "source": rng.choice(["alpha", "bravo", "charlie"], size=n),
        "week": rng.integers(1, 13, size=n),
        "load": rng.normal(0, 1, size=n),
        "latency_ms": rng.lognormal(4.2, 0.35, size=n),
        "quality_score": np.clip(rng.normal(0.75, 0.12, size=n), 0, 1)
    })

    # derived label
    logits = df["load"] * 0.8 + (df["latency_ms"] - df["latency_ms"].mean()) * 0.01 - (df["quality_score"] - 0.7) * 2
    prob = 1 / (1 + np.exp(-logits))
    df["risk_flag"] = rng.binomial(1, np.clip(prob * 0.6, 0, 1))

    # Inject problems
    df.loc[rng.choice(n, int(n * 0.02)), "latency_ms"] = np.nan
    df.loc[rng.choice(n, int(n * 0.005)), "latency_ms"] *= 6
    df.loc[rng.choice(n, int(n * 0.003)), "source"] = "charliee"

    return df


# -------------------------------------------------------------------
# DEMO 2 — Schema report
# -------------------------------------------------------------------
def schema_report(df, path):
    lines = []
    for c in df.columns:
        s = df[c]
        lines.append(f"{c} | dtype={s.dtype} | missing={s.isna().mean():.2%}")
    with open(path, "w") as f:
        f.write("\n".join(lines))


# -------------------------------------------------------------------
# DEMO 3 — Quality diagnostics
# -------------------------------------------------------------------
def quality_plots(df, out_dir):
    missing = df.isna().mean()
    missing.plot(kind="bar", title="Missingness by Column")
    plt.savefig(f"{out_dir}/missingness.png")
    plt.close()

    df.select_dtypes(float).corr().plot(kind="imshow")
    plt.title("Correlation")
    plt.savefig(f"{out_dir}/correlation.png")
    plt.close()


# -------------------------------------------------------------------
# DEMO 4 — Cleaning policy
# -------------------------------------------------------------------
def clean(df):
    df = df.copy()
    df["source"] = df["source"].replace({"charliee": "charlie"})
    df["latency_ms"] = df.groupby("source")["latency_ms"].transform(lambda s: s.fillna(s.median()))
    df["latency_ms"] = df["latency_ms"].clip(upper=df["latency_ms"].quantile(0.995))
    return df


# -------------------------------------------------------------------
# DEMO 5 — Synthetic text + NLP features
# -------------------------------------------------------------------
def text_demo(df, out_dir):
    texts = [
        "Latency spike in system",
        "Model output confusing",
        "Performance improved",
        "Data incomplete for source",
        "Too many false alarms"
    ]

    sample = df.sample(500, random_state=0)
    feedback = pd.DataFrame({
        "text": np.random.choice(texts, len(sample))
    })

    vec = CountVectorizer(stop_words="english")
    X = vec.fit_transform(feedback["text"])

    counts = np.asarray(X.sum(axis=0)).ravel()
    terms = vec.get_feature_names_out()

    plt.bar(terms, counts)
    plt.title("Top Terms")
    plt.savefig(f"{out_dir}/text_terms.png")
    plt.close()

    feedback.to_csv(f"{out_dir}/text_feedback.csv", index=False)


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
def main(out_dir):
    ensure_dir(out_dir)

    df = generate_data()
    df.to_csv(f"{out_dir}/raw.csv", index=False)

    schema_report(df, f"{out_dir}/schema.txt")
    quality_plots(df, out_dir)

    clean_df = clean(df)
    clean_df.to_csv(f"{out_dir}/clean.csv", index=False)

    text_demo(clean_df, out_dir)

    print("Lecture 03 demo complete. Check artifacts folder.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", default="artifacts")
    args = parser.parse_args()
    main(args.out_dir)
