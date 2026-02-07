Lecture 03 — Data, Datasets, and Synthetic Reality

Course: AI-Enabled Informatics for Engineers
Week: 3
Primary Text: Chip Huyen, AI Engineering (2024/2025), Chapter 8
Format: GitHub-first · demo-driven · informatics-anchored

Why This Lecture Matters

Modern AI systems rarely fail because of model architecture alone.
They fail because of data:

missing data

biased data

stale data

misaligned data

or no data at all for the decision we actually care about

This week shifts our focus from:

models → information pipelines

That shift is the heart of informatics.

The Informatics Lens on Data

Recall the course backbone:

data → information → decision → action


Chapter 8 lives almost entirely in the data → information boundary.

Key insight:

AI engineering is often data engineering in disguise.

Real-world implication:

The best model with the wrong data → useless

A simple model with the right data → transformative

Three Properties of Useful Training Data

(Huyen, Ch. 8 synthesis)

Every dataset can be evaluated along three axes:

1. Quantity

How much data exists?

Tokens

Rows

Images

Events

Scaling laws show performance often rises with more data—
but only to a point.

2. Quality

Is the data correct, clean, and meaningful?

Low-quality data introduces:

hallucination risk

bias propagation

brittle predictions

Small high-quality datasets often outperform massive noisy ones.

3. Diversity

Does the data represent the real decision environment?

Missing diversity causes:

domain failure

language failure

demographic bias

distribution shift in production

Visualization — Data Quality vs Quantity Tradeoff

Credible reference:
Stanford AI Index & scaling-law literature consistently show:

performance improves with scale

but plateaus without quality improvements

Recommended visual:

https://hai.stanford.edu/ai-index


Look for:

training compute vs performance curves

This is the empirical foundation of Chapter 8.

Dataset Sources Used in Real AI Systems

Below are credible, industry-relevant datasets worth knowing.

Web-Scale Text

Common Crawl
https://commoncrawl.org

C4 Dataset
https://www.tensorflow.org/datasets/catalog/c4

These power many foundation models.

Structured / Tabular

UCI Machine Learning Repository
https://archive.ics.uci.edu

Kaggle datasets
https://www.kaggle.com/datasets

Useful for decision-oriented ML.

Multimodal

LAION image-text datasets
https://laion.ai

Critical for:

diffusion models

vision-language systems

Informatics Insight

Notice something important:

None of these datasets were built for your decision.

That gap explains:

domain-specific models

retrieval-augmented generation

synthetic data

evaluation pipelines

All core AI-engineering patterns.

Synthetic Data — Engineering Reality When Reality Is Missing

Synthetic data = artificially generated training examples
that preserve:

structure

distribution

semantics

without requiring:

expensive collection

sensitive data access

rare real-world events

Why Synthetic Data Exists

Three dominant reasons:

1. Privacy

Healthcare, finance, defense.

Real data cannot be freely shared.

2. Scarcity

Rare failures, edge cases, anomalies.

Exactly the cases we most need to learn from.

3. Cost

Human labeling is expensive and slow.

Synthetic generation scales instantly.

Visualization — Real vs Synthetic Data Pipeline

Helpful conceptual diagram:

Real World → Small Real Dataset → Synthetic Expansion → Model Training → Evaluation → Decision


Credible reference discussion:

https://hai.stanford.edu/news/synthetic-data-ai

Hands-On Demo — Creating Synthetic Tabular Data
Goal

Simulate a decision dataset when real data is unavailable.

Python Example
import pandas as pd
import numpy as np

np.random.seed(42)

n = 500

data = pd.DataFrame({
    "age": np.random.normal(40, 10, n).astype(int),
    "income": np.random.normal(70000, 15000, n).astype(int),
    "risk_score": np.random.uniform(0, 1, n)
})

data["decision"] = (data["risk_score"] > 0.6).astype(int)

data.head()

Informatics Reflection

What just happened?

We engineered information:

defined variables

defined distributions

defined a decision rule

This is informatics in action.

Demo Extension — Synthetic Text with an LLM
from openai import OpenAI

client = OpenAI()

prompt = """
Generate 5 realistic customer support complaints
about delayed shipping. Keep each under 20 words.
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

print(response.output[0].content[0].text)

Why This Matters

Synthetic text enables:

classifier training

evaluation benchmarks

edge-case simulation

without scraping real users.

Risks of Synthetic Data

(Critical Chapter 8 theme)

Synthetic data can silently fail.

Distribution Drift

Generated data may not match reality.

Feedback Loops

Models trained on synthetic outputs
learn their own mistakes.

Hidden Bias

Synthetic generation reflects
the bias of the generator.

Informatics Principle

Synthetic data must always be evaluated against real-world decisions.

Not just statistical similarity.

Connecting Back to AI Engineering

We now see a layered system:

Data Engineering
    ↓
Dataset Strategy
    ↓
Model Training / Selection
    ↓
Evaluation
    ↓
Decision Support


Chapter 8 focuses on the first two layers—
the ones most courses ignore.

Live Discussion Prompt (Canvas)

Question:

When is synthetic data more valuable than real data?

Consider:

privacy

safety

cost

rare events

simulation

Post one concrete engineering scenario.

Week 3 Practical Task
Build a Tiny Decision Dataset

Choose a domain

Define 3–5 variables

Generate synthetic rows

Define a decision rule

Reflect:

What real-world assumptions did you encode?

Submit:

notebook link

1-paragraph informatics reflection

Looking Ahead — Lecture 04

Next week we move into:

Evaluation as the core of AI engineering

Because:

A system that cannot be evaluated
cannot be trusted.

Closing Thought

The most important shift so far in this course:

AI success is rarely about the model.

It is about
how we construct reality through data
to support better human decisions.

That idea—more than any algorithm—
is the foundation of AI-enabled informatics.
