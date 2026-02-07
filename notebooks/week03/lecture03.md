Lecture 03 — Dataset Engineering, Reliability, and the Informatics Backbone

Course: AI-Enabled Informatics for Engineers
Week: 3
Primary Text: Chip Huyen, AI Engineering (2024/2025), Chapter 8 — Dataset Engineering
Format: GitHub-first · demo-driven · informatics-anchored

Why This Lecture Matters

Up to this point, we’ve explored:

Lecture 01: Informatics as data → information → decision → action

Lecture 02: Foundation models, schemas, and decision-aligned SQL

Today we move into the real engineering substrate:

Datasets are the reliability layer of AI systems.

Not models.
Not prompts.
Not clever architectures.

Datasets.

And Chapter 8 makes a bold but correct claim:

Most real-world AI failures are dataset failures in disguise.

This lecture connects dataset engineering → informatics reliability → decision quality.

1. Informatics Revisited: Reliability Lives in the Data Layer

Recall the informatics pipeline:

data → information → decisions → action


Dataset engineering determines whether:

information is trustworthy

decisions are stable

actions are safe in the real world

Without dataset discipline:

evaluation lies

models drift

automation becomes dangerous

This is why Chapter 8 sits at the heart of AI engineering.

2. What Chapter 8 Actually Teaches (Condensed Precisely)

Chapter 8 reframes datasets from:

static training files

to:

living production infrastructure

Key shifts:

2.1 Datasets Are Dynamic Systems

Real data changes:

distributions drift

schemas evolve

sensors fail

humans behave differently

Static training assumptions collapse in deployment.

2.2 Dataset Quality > Model Complexity

A simple model with:

clean labels

correct schema

representative distribution

beats a large model trained on noisy data.

This is one of the most consistent empirical truths in ML.

2.3 Evaluation Depends on Dataset Design

If your test set is flawed:

metrics mislead

thresholds fail

decisions become unsafe

So evaluation is a dataset engineering problem.

3. Visualizing Dataset Failure Modes
Distribution Shift (Credible Visualization)

See:

Google ML Crash Course — Training vs Serving Skew
https://developers.google.com/machine-learning/crash-course/production-ml-systems/monitoring

This diagram shows:

Models fail not because they are wrong —
but because reality moved.

Data-Centric AI Perspective

Andrew Ng’s data-centric AI framing:

https://landing.ai/data-centric-ai/

Core idea:

Improving data quality often yields bigger gains than model tuning.

This aligns directly with Chapter 8’s thesis.

4. Real-World Dataset Sources for Course Projects

These are credible, decision-relevant datasets aligned with informatics.

Predictive Maintenance — NASA C-MAPSS

https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

Used for:

remaining useful life prediction

maintenance scheduling decisions

Cybersecurity — CICIDS2017

https://www.unb.ca/cic/datasets/ids-2017.html

Used for:

intrusion detection

SOC alert prioritization

Healthcare — UCI Diabetes

https://archive.ics.uci.edu/ml/datasets/diabetes%2B130-us%2Bhospitals%2Bfor%2Byears%2B1999-2008

Used for:

readmission risk

intervention allocation

Energy — PJM Consumption

https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption

Used for:

load forecasting

grid decision optimization

5. Synthetic Data in AI Engineering (Why It Matters)

Chapter 8 emphasizes:

Real data is scarce, biased, or sensitive.

So engineers use:

synthetic structured data

synthetic text

synthetic images

embedding-guided augmentation

But:

Synthetic data must preserve decision-relevant structure
or it becomes useless.

6. Demo 1 — Synthetic Structured Data (Tabular)
import numpy as np
import pandas as pd

np.random.seed(42)

n = 1000

data = pd.DataFrame({
    "temperature": np.random.normal(75, 10, n),
    "vibration": np.random.normal(0.5, 0.1, n),
    "pressure": np.random.normal(30, 5, n),
})

data["failure"] = (
    (data["temperature"] > 90) &
    (data["vibration"] > 0.6)
).astype(int)

data.head()

Informatics Insight

This creates:

causal structure

decision signal

testable pipeline input

Synthetic ≠ fake
Synthetic = controlled experiment space.

7. Demo 2 — Synthetic Text Generation for Rare Classes
from faker import Faker
fake = Faker()

alerts = [fake.sentence(nb_words=8) for _ in range(10)]
alerts


Use cases:

rare fraud scenarios

medical edge cases

cybersecurity anomalies

Key warning from Chapter 8:

Synthetic text can amplify hallucinated patterns
if not validated.

8. Demo 3 — Synthetic Images (Conceptual + Tooling)

Common tools:

Stable Diffusion

Midjourney

DALL·E-style generators

Credible overview:

https://arxiv.org/abs/2301.04246

Use cautiously:

label noise risk

domain realism gaps

9. Demo 4 — Embedding-Guided Augmentation
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embeddings = np.random.rand(5, 4)

similarity = cosine_similarity(embeddings)
similarity


Used for:

semantic diversity

training coverage expansion

retrieval robustness

This connects directly to Lecture 02 embeddings.

10. The Deep Link: Dataset Engineering → Informatics Decisions

Here is the key conceptual bridge:

Dataset Engineering Controls Decision Reliability
Dataset Property	Decision Impact
Label noise	Wrong interventions
Missing features	Hidden risk
Skewed sampling	Biased policy
Drift	Unsafe automation

So:

Dataset engineering is decision engineering.

That is pure informatics.

11. Hands-On Notebook for This Week

Run:

notebooks/week03/03_dataset_engineering_demo.ipynb


This notebook will:

load a real dataset

generate synthetic variants

compare decision thresholds

simulate drift

12. Week 3 Discussion Prompt (Canvas)

Prompt:

Describe one realistic way your dataset could fail in production.
What decision would be harmed?
How would you detect it?

This forces:

informatics thinking

not just modeling

13. Project Progress This Week

You should now begin:

Pipeline Sketch
ingest → validate → transform → store → serve → monitor


Deliverable coming in Milestone M2.

14. Looking Ahead

Next lecture:

Evaluation Methodology (Chapter 3)

We move from:

“Does the model work?”

to:

“Does the decision improve?”

That is the central intellectual shift of this course.

15. Closing Thought

Chapter 8 quietly delivers one of the most important truths in AI:

Reliable AI systems are built
less by training models
and more by engineering data correctly.

And in informatics language:

Better data → better information → better decisions → safer action.

That is the backbone of everything we are building this semester.
