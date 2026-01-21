# LECTURE 01 — Informatics, Industry 5.0, and the Rise of AI Engineering

> **Course:** AI-Enabled Informatics for Engineers  
> **Week:** 1  
> **Primary Text:** Chip Huyen, *AI Engineering* (2024/2025), Chapter 1  
> **Lecture format:** GitHub-first, notebook-adjacent, discussion-driven

---

## Quick Links (Start Here)

- **Run the Week 1 notebook:** `01_informatics_setup_and_decision_framing.ipynb`
- **Chip Huyen Ch.1 summary (public):**  
  https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md#chapter-1-introduction-to-building-ai-applications-with-foundation-models
- **Informatics framing (NCBI):** https://www.ncbi.nlm.nih.gov/books/NBK470564/  
- **Informatics framing (Edinburgh):** https://informatics.ed.ac.uk/about/what-is-informatics  
- **Industry 5.0 overview (EU):**  
  https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/industry-50_en

---

## Welcome

Welcome to **AI-Enabled Informatics for Engineers**.

This is not a traditional machine learning course, data science survey, or programming bootcamp.
It’s a course about **how information flows through engineered systems**, and how modern AI—especially
**foundation models**—changes how we design, evaluate, and operate those systems.

By the end of the semester, you’ll build a working **AI-enabled informatics system** that improves a real decision workflow.

---

## Today’s Roadmap

<details open>
<summary><strong>Lecture roadmap</strong></summary>

1. What informatics means (authoritative definitions)
2. Industry 5.0 framing (human-centric, sustainable, resilient)
3. Why AI engineering emerged (Chip Huyen Ch.1)
4. Mini demo: data → information → decision
5. Week 1 deliverables

</details>

---

## Informatics: The Core Idea

> **Informatics is the engineering of data → information → decisions → actions.**

- **Data** is raw
- **Information** is structured and contextualized
- **Decisions** are actionable choices
- **Actions** create real-world outcomes

### Suggested figure (add later)
> **Figure (add later):** Data → Information → Decision → Action pipeline  
> Save as: `assets/informatics_pipeline.svg`

<!-- ![Data → Information → Decision → Action](assets/informatics_pipeline.svg) -->

---

## Informatics: Authoritative Definitions

<details>
<summary><strong>NCBI definition: end-to-end lifecycle</strong></summary>

NCBI describes informatics as **acquisition, storage, retrieval, processing, and decision support**.
Notice the definition is end-to-end: it explicitly includes decision support.

Source: https://www.ncbi.nlm.nih.gov/books/NBK470564/

</details>

<details>
<summary><strong>Edinburgh definition: representation & transformation</strong></summary>

Edinburgh emphasizes **representation, transformation, and communication of information**—
which is especially relevant because foundation models are representation transformers.

Source: https://informatics.ed.ac.uk/about/what-is-informatics

</details>

---

## Why Informatics Matters in 2026

Engineering domains are information-dense (cybersecurity, energy, healthcare, manufacturing).
AI increases capability, but introduces new failure modes (hallucinations, drift, cost spikes).

Informatics provides the discipline to build systems that are:
- reliable
- interpretable
- aligned with human goals and constraints

---

## Industry 5.0 Overview (Framing)

Industry 5.0 emphasizes:
- **Human-centricity**
- **Sustainability**
- **Resilience**

Source: https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/industry-50_en

### Suggested figure (add later)
> **Figure (add later):** Industry 5.0 pillars (human-centric, sustainable, resilient)  
> Save as: `assets/industry5_pillars.png`

<!-- ![Industry 5.0 pillars](assets/industry5_pillars.png) -->

---

## Industry 5.0 → AI Engineering Implications

<details>
<summary><strong>Human-centric</strong></summary>

AI should augment humans. Implications:
- human-in-the-loop approvals
- explainable outputs
- overrides & audit logs

</details>

<details>
<summary><strong>Resilience</strong></summary>

Systems must handle failures and uncertainty. Implications:
- monitoring
- fallback modes
- escalation to a human

</details>

<details>
<summary><strong>Sustainability</strong></summary>

AI consumes compute/money/energy. Implications:
- optimize inference cost & latency
- treat efficiency as a requirement

</details>

---

## Discussion Prompt (Canvas)

Pick **one Industry 5.0 value** and explain **one concrete AI system design choice** it changes.

Examples:
- human-centric → add a human approval checkpoint
- resilience → add monitoring + fallback logic
- sustainability → reduce model calls using caching/retrieval

---

## Chip Huyen Chapter 1: The Rise of AI Engineering

Chip Huyen’s framing in Chapter 1:
- the primary challenge is no longer training models
- it’s building **applications around foundation models**

Public chapter summary:  
https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md#chapter-1-introduction-to-building-ai-applications-with-foundation-models

### Suggested figure (add later)
> **Figure (add later):** “AI engineering” components (retrieval, evaluation, monitoring, UX, feedback)  
> Save as: `assets/aie_ch1_components.png`

<!-- ![AI engineering components](assets/aie_ch1_components.png) -->

---

## What Changed with Foundation Models

Key changes:
- self-supervision at scale
- multimodality
- model-as-a-service APIs

New risks:
- hallucinations
- drift
- cost unpredictability

This is why evaluation and monitoring are central themes in this course.

---

## AI Engineering vs ML Engineering (Simple)

- **ML engineering:** training models
- **AI engineering:** integrating models into systems

In AI engineering, the model is one layer among:
data, retrieval, guardrails, evaluation, monitoring, UI, feedback.

---

## Mini Demo: Data → Decision

This week’s notebook walks through a tiny example:
- load a dataset
- aggregate
- interpret output as a decision

➡️ Run: `01_informatics_setup_and_decision_framing.ipynb`

---

## Week 1 Deliverables (Canvas)

1) **Cloud access check** (Colab or Azure for Students or AWS Educate)  
2) **Project domain shortlist** (3 domains + 1 decision each)

---

## Looking Ahead

Next week you’ll submit **Milestone M1 (graded)**:
- domain
- decision
- dataset plan
- success criteria

---

## Contact

- Use TA sessions for help with assignments, milestones, and debugging
- Office hours by request (email)

