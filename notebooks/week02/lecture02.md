# Lecture 02 — Foundation Models, Schemas, and SQL for Decision Quality  
**Course:** AI-Enabled Informatics for Engineers  
**Week:** 2  
**Primary Text:** Chip Huyen, *AI Engineering* (2024/2025), Chapter 2 (and/or the public chapter summary)  
**Format:** GitHub-first · notebook-adjacent · discussion-driven

This lecture moves from *framing* (Week 1) to *execution discipline*: how you represent information (schemas), query it (SQL), and connect it to decisions — **before** you add AI.

A recurring theme of this course: **bad structure produces bad decisions**, even with great models.  
If your schema is unclear, your joins are wrong, your definitions drift, or your metrics are inconsistent, the model will only amplify confusion.

By the end of Week 2, you should be able to:  
- describe what a foundation model is in engineering terms (capabilities + failure modes)  
- explain how **schema choices** change what you can know and decide  
- use SQL to compute decision-relevant aggregates and slices  
- connect “query results” to “actionable decision logic” in a notebook workflow

---

## Quick Links (Start Here)

### 📘 Chip Huyen — Chapter summaries (public)
https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md

### ✅ Required materials (live links)
- **SQLZoo (interactive):** https://sqlzoo.net/  
- **Kaggle: Intro to SQL:** https://www.kaggle.com/learn/intro-to-sql  

### 💻 Coding lab (Colab)
- **Notebook:** `notebooks/week02/02_sql_for_decisions.ipynb`  
- **Open in Colab:** https://colab.research.google.com/github/AI-Enabled-Informatics-for-Engineers/ISE/blob/main/notebooks/week02/02_sql_for_decisions.ipynb

### 🧵 Canvas discussion prompt (Week 2)
**How do schema choices create or destroy decision quality?**

---

## Today’s Roadmap

In this lecture, we will:

1. Define foundation models in *engineering* terms  
2. Identify common failure modes (hallucination, brittleness, drift, cost volatility)  
3. Show why **schemas** are decision infrastructure  
4. Use SQL to compute decision-relevant facts  
5. Connect SQL outputs to a decision workflow (thresholds, policies, actions)  
6. Review Week 2 deliverables and next milestones

---

## Foundation Models: The Engineering Definition

A **foundation model** is a large, general-purpose model trained on broad data at scale, then adapted to many tasks via prompting, fine-tuning, or retrieval.

Engineering implications:
- You usually **don’t train** the model.
- You **compose** it into a system: retrieval + prompts + evaluation + monitoring + UX + governance.
- The model behaves like a powerful but imperfect component:
  - can summarize, classify, extract, reason (sometimes)
  - can also fabricate, misinterpret, and drift

### What they’re good at (in practice)
- text understanding + generation  
- extraction and transformation (with guardrails)  
- “good enough” first drafts  
- semantic search when paired with embeddings + retrieval

### What they’re risky at
- “facts” without sources  
- math and precise logic under ambiguity  
- policy decisions without explicit constraints  
- unmonitored production workflows

---

## Why Week 2 is SQL, Not Prompts

Because **decisions need ground truth**.

SQL gives you:
- explicit definitions  
- reproducible queries  
- auditable metrics  
- a shared language between engineers, analysts, and decision-makers

Before we let an LLM talk, we want the system to *know*:
- what a “customer” is  
- what counts as “late”  
- how we define “risk”  
- which time window matters  
- what “success” means

SQL is your first tool for building those definitions into the system.

---

## Schemas are Decision Infrastructure

A schema is not just “tables.”  
It encodes what your organization believes is true.

### A schema defines:
- **entities** (users, devices, incidents, shipments, patients)  
- **relationships** (one-to-many, many-to-many)  
- **time** (event timestamps, reporting periods)  
- **granularity** (daily totals vs event-level logs)  
- **meaning** (status codes, categories, labels)

### The key claim:
**Schema choices change decision quality.**

If you store only “final outcome,” you can’t analyze causes.  
If you store events without timestamps, you can’t detect drift.  
If you store free text without structure, you can’t reliably aggregate.

---

## Mini-Example: Same Problem, Different Schema, Different Decision

**Decision:** “Do we need to add staff to reduce late deliveries?”

### Schema A: Only stores delivery outcome
- `order_id`, `delivered_on_time` (true/false)

You can compute:
- percent late overall

You cannot compute:
- which routes are late
- whether lateness is seasonal
- whether specific carriers are failing
- what the leading indicators were

### Schema B: Stores event timeline
- `order_events(order_id, event_type, timestamp, location_id, carrier_id)`

Now you can compute:
- lateness by carrier and route  
- bottleneck stages (pickup, sort, last-mile)  
- early-warning signals (scan delays)  
- targeted interventions (carrier contract change vs staffing)

Same “AI model,” completely different usefulness.

---

## SQL for Decisions: Patterns You Must Master

In this notebook, you will practice the SQL building blocks that translate into *decision metrics*:

### 1) Filters (WHERE)
Define the population that matters:
- last 30 days
- a specific region
- critical incidents only

### 2) Aggregations (GROUP BY)
Transform events into decision facts:
- counts
- rates
- averages
- percentiles (where supported)

### 3) Joins
Create context:
- incidents + systems
- orders + customers
- patients + diagnoses + outcomes

### 4) Windows / Time
Decisions are time-sensitive:
- week-over-week change
- rolling 7-day average
- before/after interventions

---

## Notebook Walkthrough

▶️ Run:
`notebooks/week02/02_sql_for_decisions.ipynb`

In the lab, you will:
- load a dataset (or connect to a public one)
- design/inspect a schema
- write queries that produce decision-relevant metrics
- translate query outputs into a recommended action

---

## Design Rule: Query → Metric → Decision → Action

A correct Week 2 submission should have this chain:

1. **Query** (reproducible SQL)  
2. **Metric** (defined clearly)  
3. **Decision rule** (thresholds / policy)  
4. **Action** (what changes in the real world)

Example (generic):
- Query: late deliveries by carrier for last 30 days  
- Metric: % late per carrier  
- Decision rule: if late rate > 8% for 2 consecutive weeks → escalation  
- Action: add inspection, renegotiate SLA, route change, staffing shift

---

## Canvas Discussion Prompt (Week 2)

**How do schema choices create or destroy decision quality?**

Answer with:
1. One concrete schema choice (e.g., event-level vs summary-level, timestamps, normalization)  
2. What decision it enables or blocks  
3. How it changes evaluation or accountability  
4. One mitigation if you can’t change the schema (workaround)

---

## Week 2 Deliverables (Canvas)

1) **SQL practice completed**
- SQLZoo sections (as assigned)
- Kaggle Intro to SQL modules (as assigned)

2) **Notebook submission**
- `02_sql_for_decisions.ipynb` completed with:
  - working SQL queries
  - clear metric definitions
  - a decision rule and an action recommendation

3) **Discussion post**
- schema choice → decision quality explanation

---

## Looking Ahead (Week 3 Preview)

Next week we’ll introduce:
- retrieval (RAG) as “schema for unstructured text”
- prompting as “interface design”
- evaluation as “decision correctness, not vibes”

Your project Milestone M1 is coming soon:
- domain + decision + dataset plan + success criteria

---

## Contact & Support

**TA Sessions**
- Twice weekly (check Canvas announcements)

**TA**
- Keyi Wang  
- kw653@scarletmail.rutgers.edu  
- Office hours by request (email)
