# Lecture 02 — Foundation Models, Transformers, and Decision-Oriented Data Systems

**Course:** AI-Enabled Informatics for Engineers  
**Week:** 2  
**Primary Text:** Chip Huyen, *AI Engineering* (2024/2025), Chapter 2  
**Format:** GitHub-first · notebook-adjacent · discussion-driven  

---

## Purpose of This Lecture

Lecture 01 established the course framing: informatics as the engineering discipline that turns data into decisions and actions.

This lecture focuses on a narrower but critical question:

**What exactly are foundation models, why do they work, and how should engineers reason about them as system components rather than magical endpoints?**

The goal is not to teach model internals for their own sake, but to build *engineering judgment* about:
- when a model is appropriate,
- which kind of model is appropriate,
- and how models interact with data, schemas, and decisions.

---

## Required Reading Context

This lecture corresponds primarily to **Chapter 2** of Chip Huyen’s *AI Engineering*.

Public chapter summary (recommended pre-read):  
https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md#chapter-2-foundation-models

Full text via Rutgers (O’Reilly):  
https://learning.oreilly.com/library/view/ai-engineering/9781098166298/

You should read Chapter 2 as an *engineering taxonomy*, not as a vendor guide.

---

## Foundation Models: An Engineering Definition

A foundation model is not defined by its architecture alone.

From an engineering standpoint, a foundation model is a model that:

- is pre-trained on broad, heterogeneous data,
- learns general representations,
- can be adapted to many downstream tasks with minimal additional training.

What matters operationally is not how the model was trained, but **how it is used**.

Foundation models function as:
- representation engines,
- probabilistic reasoning layers,
- adaptable interfaces between data and decisions.

They are not decision systems.  
They are components *inside* decision systems.

---

## Why Transformers Matter (Without the Math)

Transformers are the architectural foundation that enabled modern foundation models.

You do **not** need to derive attention equations to reason about them effectively.

What matters for engineers:

- Transformers process entire sequences at once, not step-by-step.
- They use attention to weight relevance dynamically.
- They scale well with both data and compute.

This makes them unusually good at:
- language understanding,
- contextual reasoning,
- cross-task generalization.

A clear, non-technical visualization is here (required viewing):  
https://jalammar.github.io/illustrated-transformer/

> Key takeaway: transformers trade **efficiency and determinism** for **flexibility and expressiveness**.

That tradeoff shows up everywhere else in the system.

---

## Model Size, Parameters, and Tradeoffs (Core Chapter 2 Material)

One of the most important points in Chapter 2 is that **model selection is an engineering decision**, not a leaderboard contest.

Models vary along multiple axes:

- parameter count,
- context window size,
- latency,
- cost per token,
- fine-tuning capability,
- openness (open vs closed),
- update cadence and version stability.

Larger models tend to:
- reason better in open-ended contexts,
- generalize across tasks,
- but cost more, respond more slowly, and drift more frequently.

Smaller models tend to:
- be cheaper and faster,
- behave more predictably,
- require stronger structure to be useful.

A practical cost/performance discussion is here:  
https://newsletter.semianalysis.com/p/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures?utm_source=chatgpt.com

**Engineering principle:**  
> If a system requires a very large model to work at all, the system design is usually the real problem.

---

## Adaptation Paths: Prompting, Fine-Tuning, and Retrieval

Chapter 2 emphasizes that *how* you adapt a model often matters more than *which* model you pick.

Three dominant adaptation strategies:

### Prompting
- Fastest to deploy
- Least stable
- Highly sensitive to wording and context

### Fine-tuning
- More stable behavior
- Higher upfront cost
- Harder to update and govern

### Retrieval-Augmented Generation (RAG)
- Grounds models in external data
- Improves correctness and traceability
- Introduces new failure modes (retrieval quality, stale data)

This course will emphasize **retrieval and structure** over prompt cleverness.

---

## The Role of Schemas in AI Systems

Schemas are one of the most important — and most neglected — tools in AI engineering.

A schema is not just a database artifact.
It is a **contract** between:
- data,
- models,
- humans,
- and downstream systems.

Schemas:
- constrain ambiguity,
- enable validation,
- allow partial automation,
- make evaluation possible.

Without schemas:
- outputs drift,
- errors hide in text,
- decisions become untraceable.

Schemas are how probabilistic models become **operationally safe**.

---

## SQL as Decision Logic, Not Legacy

SQL plays a central role in informatics systems because it:

- forces explicit assumptions,
- exposes aggregation choices,
- makes decision logic inspectable.

In this course, SQL is used to:
- define decision-relevant information,
- validate model outputs,
- create grounding layers before AI is applied.

Week 2 notebook:  
`notebooks/week02/02_sql_for_decisions.ipynb`

Open in Colab:  
https://colab.research.google.com/github/AI-Enabled-Informatics-for-Engineers/ISE/blob/main/notebooks/week02/02_sql_for_decisions.ipynb

---

## Example: A Minimal Informatics Loop

A simple but complete loop:

1. Raw data ingestion
2. Schema-enforced storage
3. SQL aggregation
4. Interpretation
5. Decision threshold
6. Action

AI can assist at steps 3–5, but it does not eliminate any of them.

This is why informatics remains the controlling discipline.

---

## Discussion Focus (TA Sessions)

Discussion prompt (Canvas):

**How do schema choices create or destroy decision quality?**

Students should be prepared to:
- modify schema assumptions,
- observe changes in outputs,
- explain downstream decision impact.

This is not a philosophical discussion.  
It is a design discussion.

---

## Week 2 Deliverables

- **Assignment 1 (6 points):** SQL + decision framing
- **Discussion (1 point):**
  - 60% written Canvas post
  - 40% live TA participation
- **Project Milestone M1 (4 points):**
  - domain
  - decision
  - dataset plan
  - success criteria

---

## Why This Lecture Matters for the Project

Your project is not “build a model.”

Your project is:
> **design a system that improves a real decision.**

Model choice, schema design, and data grounding decisions made now will determine whether your project scales cleanly or collapses under its own complexity.

---

## Closing Perspective

Foundation models are powerful.

They are also:
- expensive,
- probabilistic,
- and easy to misuse.

Informatics — not modeling — is what keeps AI systems aligned with reality, cost, and human judgment.

---

## Support

**TA:** Keyi Wang  
📧 kw653@scarletmail.rutgers.edu  

TA sessions are the best place to test assumptions and catch design mistakes early.

