#!/usr/bin/env python3
"""
Lecture 03 Demos — Chapter 8 Dataset Engineering (single runnable file)

What it does (end-to-end):
  1) Generates a synthetic telemetry dataset
  2) Runs sanity-check visualizations and saves plots to ./artifacts
  3) Enforces a data contract (Pandera) and demonstrates contract failure
  4) Demonstrates proper time-based splitting and an example leakage feature
  5) Simulates drift and computes PSI + KS stats + drift visualizations

How to run (Colab):
  !pip -q install pandas numpy matplotlib pandera scipy scikit-learn
  !python lecture03_demos.py --show_plots 0

How to run (local/Azure):
  pip install -r requirements.txt   (or install packages above)
  python lecture03_demos.py --out_dir artifacts --show_plots 0

Outputs:
  - CSVs saved in out_dir
  - PNG plots saved in out_dir
  - Summary printed to console

Notes:
  - Uses matplotlib only (no seaborn).
  - Designed to be readable, classroom-friendly, and deterministic.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import ks_2samp

# Pandera (data contracts)
import pandera as pa
from pandera import Column, DataFrameSchema, Check

# Simple model utilities for leakage demo (optional but helpful)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


# -----------------------------
# Utilities
# -----------------------------

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def savefig(path: str, show_plots: bool) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    if show_plots:
        plt.show()
    plt.close()

def set_deterministic(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)

def safe_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    # ROC AUC requires both classes present; handle edge case cleanly.
    if len(np.unique(y_true)) < 2:
        return float("nan")
    return roc_auc_score(y_true, y_score)

def summarize_df(df: pd.DataFrame, name: str) -> None:
    print(f"\n--- {name} ---")
    print(df.head(5))
    print(df.describe(include="all").transpose().head(12))


# -----------------------------
# Synthetic dataset generation
# -----------------------------

@dataclass
class SynthConfig:
    n_rows: int = 6000
    n_devices: int = 50
    start_date: str = "2025-01-01"
    freq: str = "H"  # hourly
    seed: int = 7

def generate_synthetic_telemetry(cfg: SynthConfig) -> pd.DataFrame:
    """
    Generates synthetic telemetry with interpretable signal and labels.
    Columns:
      - timestamp, device_id
      - temperature_c, vibration_mm_s, pressure_kpa
      - region, device_age_days
      - risk_score (continuous), maintenance_required (binary)
    """
    rng = set_deterministic(cfg.seed)

    timestamps = pd.date_range(cfg.start_date, periods=cfg.n_rows, freq=cfg.freq)
    device_ids = [f"dev-{i:03d}" for i in range(cfg.n_devices)]
    device_id = rng.choice(device_ids, size=cfg.n_rows, replace=True)

    region = rng.choice(["east", "west", "south", "north"], size=cfg.n_rows, replace=True, p=[0.35, 0.25, 0.25, 0.15])

    # Device age in days (bounded)
    device_age_days = rng.integers(low=30, high=3650, size=cfg.n_rows)

    # Base signals + some seasonality + device/region effects
    t = np.arange(cfg.n_rows)

    # Temperature in Celsius: baseline 45 +/- 10, with mild seasonality
    temperature_c = 45 + 8*np.sin(2*np.pi*t/500) + rng.normal(0, 3.0, cfg.n_rows)

    # Vibration: baseline 3.5 +/- 1.5, with occasional spikes
    vibration_mm_s = 3.5 + 0.7*np.sin(2*np.pi*t/120) + rng.normal(0, 0.6, cfg.n_rows)
    spike_idx = rng.choice(np.arange(cfg.n_rows), size=max(1, cfg.n_rows//80), replace=False)
    vibration_mm_s[spike_idx] += rng.normal(3.0, 1.0, size=len(spike_idx))

    # Pressure kPa: baseline 210 +/- 12
    pressure_kpa = 210 + 6*np.sin(2*np.pi*t/240) + rng.normal(0, 4.0, cfg.n_rows)

    # Region effect
    region_temp_offset = pd.Series(region).map({"east": 0.5, "west": -0.5, "south": 1.0, "north": -1.0}).to_numpy()
    temperature_c = temperature_c + region_temp_offset

    # Device aging effect increases vibration and reduces pressure slightly
    age_factor = (device_age_days / device_age_days.max())
    vibration_mm_s = vibration_mm_s + 0.8*age_factor
    pressure_kpa = pressure_kpa - 4.0*age_factor

    # Risk score: weighted combination + noise (bounded 0..1-ish)
    raw_risk = (
        0.05*(temperature_c - 45) +
        0.40*(vibration_mm_s - 3.5) +
        0.03*(210 - pressure_kpa) +
        0.30*age_factor +
        rng.normal(0, 0.5, cfg.n_rows)
    )
    # Convert to 0..1 probability-ish
    risk_prob = 1 / (1 + np.exp(-raw_risk))

    # Maintenance required when probability exceeds threshold with some label noise
    base_label = (risk_prob > 0.62).astype(int)
    noise_flip = rng.random(cfg.n_rows) < 0.03  # 3% label noise
    maintenance_required = np.where(noise_flip, 1-base_label, base_label)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "device_id": device_id,
        "region": region,
        "device_age_days": device_age_days.astype(int),
        "temperature_c": temperature_c.astype(float),
        "vibration_mm_s": vibration_mm_s.astype(float),
        "pressure_kpa": pressure_kpa.astype(float),
        "risk_score": risk_prob.astype(float),
        "maintenance_required": maintenance_required.astype(int),
    }).sort_values("timestamp").reset_index(drop=True)

    return df


# -----------------------------
# Data contract (Pandera)
# -----------------------------

def build_contract_schema() -> DataFrameSchema:
    # Semantics: temperature is Celsius; pressure is kPa; vibration in mm/s
    # Null policy: none allowed for core fields in this demo.
    schema = DataFrameSchema(
        {
            "timestamp": Column(pa.DateTime, nullable=False),
            "device_id": Column(str, Check.str_length(1, 32), nullable=False),
            "region": Column(str, Check.isin(["east", "west", "south", "north"]), nullable=False),
            "device_age_days": Column(int, Check.in_range(0, 10000), nullable=False),
            "temperature_c": Column(float, Check.in_range(-40.0, 130.0), nullable=False),
            "vibration_mm_s": Column(float, Check.in_range(0.0, 50.0), nullable=False),
            "pressure_kpa": Column(float, Check.in_range(50.0, 400.0), nullable=False),
            "risk_score": Column(float, Check.in_range(0.0, 1.0), nullable=False),
            "maintenance_required": Column(int, Check.isin([0, 1]), nullable=False),
        },
        strict=True,  # no extra columns in this demo
        coerce=True
    )
    return schema

def validate_contract(df: pd.DataFrame) -> pd.DataFrame:
    schema = build_contract_schema()
    return schema.validate(df)


# -----------------------------
# Visualizations
# -----------------------------

def plot_distributions(df: pd.DataFrame, out_dir: str, show_plots: bool) -> None:
    ensure_dir(out_dir)

    # Target distribution
    plt.figure()
    counts = df["maintenance_required"].value_counts().sort_index()
    plt.bar(counts.index.astype(str), counts.values)
    plt.title("Maintenance Required (class balance)")
    plt.xlabel("class")
    plt.ylabel("count")
    savefig(os.path.join(out_dir, "class_balance.png"), show_plots)

    # Histograms
    for col in ["temperature_c", "vibration_mm_s", "pressure_kpa", "risk_score", "device_age_days"]:
        plt.figure()
        plt.hist(df[col].values, bins=40)
        plt.title(f"Distribution: {col}")
        plt.xlabel(col)
        plt.ylabel("count")
        savefig(os.path.join(out_dir, f"dist_{col}.png"), show_plots)

def plot_relationships(df: pd.DataFrame, out_dir: str, show_plots: bool) -> None:
    ensure_dir(out_dir)

    # Risk vs features (scatter subsample)
    sample = df.sample(n=min(1500, len(df)), random_state=7)

    for xcol in ["temperature_c", "vibration_mm_s", "pressure_kpa", "device_age_days"]:
        plt.figure()
        plt.scatter(sample[xcol].values, sample["risk_score"].values, s=8)
        plt.title(f"risk_score vs {xcol}")
        plt.xlabel(xcol)
        plt.ylabel("risk_score")
        savefig(os.path.join(out_dir, f"risk_vs_{xcol}.png"), show_plots)

    # Time series snapshot
    plt.figure()
    subset = df.iloc[:600]
    plt.plot(subset["timestamp"], subset["temperature_c"])
    plt.title("Temperature over time (first 600 hours)")
    plt.xlabel("timestamp")
    plt.ylabel("temperature_c")
    plt.xticks(rotation=30, ha="right")
    savefig(os.path.join(out_dir, "temperature_timeseries.png"), show_plots)


# -----------------------------
# Leakage + splitting demos
# -----------------------------

def time_split(df: pd.DataFrame, cutoff: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    cutoff_ts = pd.Timestamp(cutoff)
    train = df[df["timestamp"] < cutoff_ts].copy()
    test = df[df["timestamp"] >= cutoff_ts].copy()
    return train, test

def add_leaky_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds an intentionally leaky feature:
      - future_risk_mean_24h: uses *future* values (invalid in production)
    This is purely instructional.
    """
    out = df.copy()
    # Shift backward so "rolling mean" looks into the future relative to each row
    out["future_risk_mean_24h"] = out["risk_score"].shift(-24).rolling(window=24, min_periods=1).mean()
    return out

def quick_leakage_model_demo(train: pd.DataFrame, test: pd.DataFrame) -> Dict[str, float]:
    """
    Trains a small logistic regression on:
      - non-leaky features
      - leaky features
    Reports AUC to show how leakage inflates evaluation.
    """
    # Non-leaky features
    features_clean = ["temperature_c", "vibration_mm_s", "pressure_kpa", "device_age_days"]
    # Leaky feature included
    features_leaky = features_clean + ["future_risk_mean_24h"]

    y_train = train["maintenance_required"].values
    y_test = test["maintenance_required"].values

    # Clean model
    Xtr_clean = train[features_clean].fillna(0.0).values
    Xte_clean = test[features_clean].fillna(0.0).values

    model_clean = LogisticRegression(max_iter=1000)
    model_clean.fit(Xtr_clean, y_train)
    p_clean = model_clean.predict_proba(Xte_clean)[:, 1]
    auc_clean = safe_auc(y_test, p_clean)

    # Leaky model
    Xtr_leaky = train[features_leaky].fillna(0.0).values
    Xte_leaky = test[features_leaky].fillna(0.0).values

    model_leaky = LogisticRegression(max_iter=1000)
    model_leaky.fit(Xtr_leaky, y_train)
    p_leaky = model_leaky.predict_proba(Xte_leaky)[:, 1]
    auc_leaky = safe_auc(y_test, p_leaky)

    return {"auc_clean": auc_clean, "auc_leaky": auc_leaky}


# -----------------------------
# Drift metrics: PSI + KS
# -----------------------------

def psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    """
    Population Stability Index (PSI).
    expected: baseline distribution (train)
    actual: new distribution (production)
    """
    expected = np.asarray(expected)
    actual = np.asarray(actual)

    # Compute quantile-based bin edges from expected
    quantiles = np.linspace(0, 1, bins + 1)
    edges = np.quantile(expected, quantiles)
    # Make edges strictly increasing (handle duplicates)
    edges = np.unique(edges)
    if len(edges) < 3:
        return float("nan")

    exp_counts, _ = np.histogram(expected, bins=edges)
    act_counts, _ = np.histogram(actual, bins=edges)

    exp_perc = exp_counts / max(1, exp_counts.sum())
    act_perc = act_counts / max(1, act_counts.sum())

    # Avoid division by zero
    eps = 1e-6
    exp_perc = np.clip(exp_perc, eps, 1.0)
    act_perc = np.clip(act_perc, eps, 1.0)

    value = np.sum((act_perc - exp_perc) * np.log(act_perc / exp_perc))
    return float(value)

def simulate_drift(df: pd.DataFrame, seed: int = 11) -> pd.DataFrame:
    """
    Create a 'production' dataset with drift:
      - temperature increases
      - pressure decreases
      - vibration slightly increases for older devices
    """
    rng = set_deterministic(seed)
    out = df.copy()

    out["temperature_c"] = out["temperature_c"] + rng.normal(2.5, 1.2, len(out))
    out["pressure_kpa"] = out["pressure_kpa"] - rng.normal(3.0, 1.0, len(out))
    out["vibration_mm_s"] = out["vibration_mm_s"] + 0.2*(out["device_age_days"]/out["device_age_days"].max()) + rng.normal(0, 0.2, len(out))

    # Risk score is not recomputed here on purpose: in real life labels may lag or be missing.
    return out

def drift_report(baseline: pd.DataFrame, prod: pd.DataFrame, cols: Optional[list] = None) -> pd.DataFrame:
    if cols is None:
        cols = ["temperature_c", "vibration_mm_s", "pressure_kpa", "device_age_days"]

    rows = []
    for c in cols:
        psi_val = psi(baseline[c].values, prod[c].values, bins=10)
        ks_stat, ks_p = ks_2samp(baseline[c].values, prod[c].values)
        rows.append({"feature": c, "psi": psi_val, "ks_stat": float(ks_stat), "ks_pvalue": float(ks_p)})
    return pd.DataFrame(rows).sort_values("psi", ascending=False).reset_index(drop=True)

def plot_drift_overlays(baseline: pd.DataFrame, prod: pd.DataFrame, out_dir: str, show_plots: bool) -> None:
    ensure_dir(out_dir)
    cols = ["temperature_c", "vibration_mm_s", "pressure_kpa", "device_age_days"]

    for c in cols:
        plt.figure()
        plt.hist(baseline[c].values, bins=40, alpha=0.6, label="baseline")
        plt.hist(prod[c].values, bins=40, alpha=0.6, label="production")
        plt.title(f"Drift overlay: {c}")
        plt.xlabel(c)
        plt.ylabel("count")
        plt.legend()
        savefig(os.path.join(out_dir, f"drift_overlay_{c}.png"), show_plots)


# -----------------------------
# Main runner
# -----------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--out_dir", type=str, default="artifacts", help="Where to write outputs (plots + CSVs).")
    p.add_argument("--n_rows", type=int, default=6000, help="Number of synthetic rows.")
    p.add_argument("--n_devices", type=int, default=50, help="Number of devices.")
    p.add_argument("--seed", type=int, default=7, help="Random seed.")
    p.add_argument("--cutoff", type=str, default="2025-03-01", help="Time split cutoff for leakage demo.")
    p.add_argument("--show_plots", type=int, default=0, help="1 to display plots interactively.")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    out_dir = args.out_dir
    show_plots = bool(args.show_plots)

    ensure_dir(out_dir)

    print("== Lecture 03 Demos: Chapter 8 Dataset Engineering ==")
    print(f"Output dir: {out_dir}")

    # DEMO 1 — Generate synthetic data
    cfg = SynthConfig(n_rows=args.n_rows, n_devices=args.n_devices, seed=args.seed)
    df = generate_synthetic_telemetry(cfg)
    summarize_df(df, "Synthetic Telemetry Dataset")
    df_path = os.path.join(out_dir, "synthetic_telemetry.csv")
    df.to_csv(df_path, index=False)
    print(f"\nSaved dataset: {df_path}")

    # DEMO 2 — Visual sanity checks
    plot_distributions(df, out_dir, show_plots)
    plot_relationships(df, out_dir, show_plots)
    print(f"Saved plots into: {out_dir}")

    # DEMO 3 — Data contract validation (Pandera)
    print("\n== Contract validation (Pandera) ==")
    try:
        df_valid = validate_contract(df)
        print("Contract check: PASS ✅")
    except Exception as e:
        print("Contract check: FAIL ❌")
        print(e)
        raise

    # Intentionally break the contract
    df_broken = df.copy()
    df_broken.loc[df_broken.sample(n=3, random_state=args.seed).index, "temperature_c"] = -999.0
    print("\n== Contract failure demonstration ==")
    try:
        validate_contract(df_broken)
        print("Unexpected: contract still passed (should not happen).")
    except Exception as e:
        print("Contract correctly failed ✅")
        print("Failure summary (truncated):")
        msg = str(e)
        print(msg[:900] + ("..." if len(msg) > 900 else ""))

    broken_path = os.path.join(out_dir, "synthetic_telemetry_broken.csv")
    df_broken.to_csv(broken_path, index=False)
    print(f"Saved broken dataset: {broken_path}")

    # DEMO 4 — Time-based split + leakage
    print("\n== Leakage + evaluation integrity demo ==")
    df_leaky = add_leaky_feature(df)
    train, test = time_split(df_leaky, cutoff=args.cutoff)
    print(f"Split cutoff: {args.cutoff}")
    print(f"Train rows: {len(train):,} | Test rows: {len(test):,}")

    metrics = quick_leakage_model_demo(train, test)
    print("AUC (clean features):", metrics["auc_clean"])
    print("AUC (with leaky feature):", metrics["auc_leaky"])
    print("Interpretation: if leaky AUC jumps materially, evaluation is inflated by leakage.")

    # DEMO 5 — Drift simulation + PSI/KS
    print("\n== Drift simulation + drift report (PSI/KS) ==")
    prod = simulate_drift(df, seed=11)
    drift = drift_report(df, prod)
    print(drift)

    drift_path = os.path.join(out_dir, "drift_report.csv")
    drift.to_csv(drift_path, index=False)
    print(f"Saved drift report: {drift_path}")

    plot_drift_overlays(df, prod, out_dir, show_plots)
    prod_path = os.path.join(out_dir, "synthetic_telemetry_production_drift.csv")
    prod.to_csv(prod_path, index=False)
    print(f"Saved production (drifted) dataset: {prod_path}")

    # Quick closing summary
    print("\n== Done ==")
    print("Artifacts created:")
    print(f" - {df_path}")
    print(f" - {broken_path}")
    print(f" - {prod_path}")
    print(f" - {drift_path}")
    print(f" - PNG plots in {out_dir}")
    print("\nTip: In Colab, download the artifacts folder or commit it to a /artifacts path ignored by git.")

if __name__ == "__main__":
    main()
