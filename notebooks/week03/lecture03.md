# Lecture 03 — Dataset Engineering & Reliability (AI Engineering, Chapter 8)
**Course:** AI-Enabled Informatics for Engineers  
**Theme:** Turning messy signals into dependable information systems  
**Reading:** Chip Huyen, *AI Engineering* — **Chapter 8** (Dataset Engineering)

---

## Why this lecture matters
Models don’t fail politely. They fail silently—because the **data changed**, a **join broke**, a **field got redefined**, or a “helpful” feature accidentally included the future.

Chapter 8’s core idea is central to both AI and Informatics:

> **The dataset is a product.**  
> Not a CSV. Not “the data folder.” A product with contracts, tests, versioning, and monitoring.

This is also exactly what **informatics** is: engineering the information supply chain so decisions are trustworthy.

---

## Learning outcomes
By the end of this lecture you should be able to:

- Explain how dataset engineering is an informatics discipline (data → information → action).
- Name common dataset failure modes (schema drift, leakage, label noise, coverage gaps).
- Define a **data contract** (schema + constraints + semantics).
- Implement basic reliability checks: schema validation, leakage-safe split, drift checks.
- Keep demos simple: run them in **Google Colab** with copy/paste (no extra files required).
- (Optional) Store demos in your repo in a clean way if you want them versioned.

---

# 1) Dataset engineering is informatics
Informatics is the study and practice of transforming raw data into usable, reliable information.

In AI systems, the dataset is the *lens* the model uses to interpret the world.

If the lens is distorted:
- accuracy looks fine… until it doesn’t
- evaluation results are “great”… because you leaked the future
- the model “degrades”… because the input meaning changed (not the algorithm)

A practical framing:

- **Data engineering:** move and shape data
- **Dataset engineering (Chapter 8):** make data dependable for learning and decision-making
- **Informatics:** build the end-to-end system that keeps information true over time

---

# 2) The dataset is a product (not a file)
A dataset “product” has owners, users, requirements, a release process, and tests.

### A dataset product must answer:
- **What is it for?** (decision support, forecasting, ranking, detection)
- **What does each field mean?** (semantics, units, definitions)
- **What are the rules?** (ranges, null policy, invariants)
- **How is it made?** (pipeline + transformations)
- **How do we know it’s still valid today?** (tests + monitoring)

### Your new default mindset
If the dataset feeds a model that affects decisions, treat it like production software:
- contracts
- tests
- versioning
- observability

---

# 3) Failure modes that happen in real life
These are the recurring villains from Chapter 8, phrased the way they show up at work.

## 3.1 Schema drift (loud break or silent break)
- A field changes type: `"42"` becomes `42`
- A field changes name: `zip` becomes `postal_code`
- A field changes unit: Celsius becomes Fahrenheit
- A field changes meaning: `status="active"` now includes “trial users” too

Schema drift is dangerous because it can be:
- **obvious** (pipeline crashes)
- **silent** (pipeline runs, model performance quietly drops)

## 3.2 Data leakage (evaluation lies)
Leakage is when your training features contain information that wouldn’t exist at prediction time.

Common leakage sources:
- random split when time ordering matters
- using “post-event” features (e.g., “refund_flag” for predicting churn)
- joining future outcomes into features by accident
- duplicating entities across train/test

If you remember one rule:
> **Your features must be available at the moment the decision is made.**

## 3.3 Label noise and label drift
Labels are rarely “ground truth.” They’re often:
- subjective
- inconsistently applied
- delayed
- impacted by policy changes (what the org considers “fraud” this year)

Two big patterns:
- **noise:** labels are wrong/inconsistent
- **drift:** label definitions change over time

## 3.4 Coverage gaps (your model never saw that slice of the world)
Even when the overall metrics look fine, performance can collapse for:
- rare segments (low volume)
- new user types
- edge behaviors
- new regions/products/policies

This is informatics: the dataset defines which reality is represented.

---

# 4) The simplest reliable dataset architecture
A minimal “reliable dataset” structure in plain English:

1. **Raw logs** (append-only if possible)
2. **Validated staging table** (schema + sanity checks)
3. **Curated training set** (features + labels + metadata)
4. **Evaluation sets** (frozen / versioned)
5. **Monitoring** (drift + quality gates)

You don’t need expensive tooling to start. You need discipline.

---

# 5) Data contracts: the practical definition
A data contract is **a written, testable agreement** that defines what the data must look like and what it means.

A good contract includes:

### 5.1 Schema (structure)
- column names
- data types
- required vs optional fields

### 5.2 Constraints (rules)
- ranges (0 ≤ latency_ms ≤ 120000)
- allowed values (region in {NA, EU, APAC})
- uniqueness rules (primary keys)
- missingness policy (null allowed or not)

### 5.3 Invariants (relationships that must always hold)
- end_time ≥ start_time
- count_success + count_fail = count_total
- if `is_employee=true`, then `email` is non-null

### 5.4 Semantics (meaning)
- units (ms, seconds, dollars)
- definition (“active user” means logged in within last 30 days)
- provenance (where it comes from, how it’s computed)

**Why semantics matter:**  
A model can’t protect you from a definition change it doesn’t know happened.

---

# 6) Evaluation integrity: splitting without lying
A model evaluation should answer a single question:

> “If I deploy this, how will it perform on the next data it sees?”

That means your split must reflect deployment reality.

## 6.1 Time-based split (most common)
If the world changes over time (it does), use:
- train = past
- test = future

## 6.2 Group/entity split (when identity matters)
If multiple rows belong to the same entity (user/device/patient):
- keep that entity in **one** split
- otherwise you get “identity leakage”

## 6.3 Frozen test sets (for honesty over time)
If you keep regenerating the test set, you keep moving the goalposts.
A frozen test set becomes your “benchmark reality.”

---

# 7) Drift: the difference between “works” and “still works”
Drift checks aren’t fancy. They’re practical.

### 7.1 Data quality drift
- null rate changed
- range changed
- new categories appeared
- schema changed

### 7.2 Distribution drift
- feature distribution shifts
- correlations shift
- segment mix shifts (different population)

### 7.3 Concept drift (harder)
- relationship between inputs and target changes  
Example: “fraud” behavior evolves, or policies change.

**Minimum viable drift monitoring** (start here):
- null rate per column
- range checks
- PSI (Population Stability Index)
- KS test (distribution shift)

---

# 8) Datasets for Testing

- **NASA C-MAPSS (predictive maintenance)** dataset page  
  https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data  
- **UCI ML Repository** (classic datasets, well documented)  
  https://archive.ics.uci.edu/  
- **CIC IDS 2017** (cyber intrusion dataset)  
  https://www.unb.ca/cic/datasets/ids-2017.html  

Tip: Many dataset pages include schema descriptions, feature lists, and usage papers—those are often the most credible because they come with definitions.

---

# 9) Demos: run directly in Google Colab 
Run these demos by copy/pasting each block into Colab.

## 9.1 Colab quick start
1. Open: https://colab.research.google.com
2. Click **New Notebook**
3. Create cells and paste the blocks below **in order**
4. Run top to bottom

---

## DEMO 0 — Install + imports
```python
!pip -q install pandas numpy matplotlib scipy scikit-learn pandera

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.stats import ks_2samp

print("Ready.")
