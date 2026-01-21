# Week 1 — Informatics Framing + Industry 5.0 + Cloud Setup

> **Dates:** Jan 20–26, 2026  
> **Theme:** *Data → Information → Decisions → Actions* (and where AI fits)  
> **Primary Text:** Chip Huyen, *AI Engineering* (2024), **Chapter 1**  
> **Repo folder:** https://github.com/AI-Enabled-Informatics-for-Engineers/ISE/tree/main/notebooks/week01  
> **Canvas:** submissions + discussions happen in Canvas (GitHub is the source-of-truth for content)

---

## Quick Start (10 minutes)

- ✅ **1) Open the notebook:** `01_informatics_setup_and_decision_framing.ipynb`  
- ✅ **2) Run it end-to-end** (Google Colab recommended)  
- ✅ **3) Submit:** Canvas Discussion 1 + M0 (Ungraded) Cloud Check + Domain Shortlist

---

<details open>
<summary><strong>1) Learning Goals</strong></summary>

- Explain **informatics** as an engineering pipeline: *data → information → decisions → actions*
- Identify how **Industry 5.0 values** (human-centric, sustainable, resilient) change AI system design choices
- Set up your execution environment (Colab / Codespaces / local) and confirm you can run course notebooks

</details>

<details>
<summary><strong>2) Readings & Interactive Resources (Required)</strong></summary>

### Primary text (required)
- **AI Engineering, Chapter 1** — focus on:
  - Why **AI engineering** is distinct from classic ML engineering
  - Common **generative AI use cases** (consumer vs enterprise)
  - Why **evaluation + reliability + system design** matter more when using foundation models

**Chapter 1 companion summary (highly useful):**
- Chip Huyen’s chapter summary notes: https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md#chapter-1-introduction-to-building-ai-applications-with-foundation-models

### Informatics framing (required)
- NCBI Informatics overview: https://www.ncbi.nlm.nih.gov/books/NBK470564/  
- University of Edinburgh — “What is Informatics?”: https://informatics.ed.ac.uk/about/what-is-informatics  

### Industry 5.0 framing (required)
- European Commission — Industry 5.0 overview: https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/industry-50_en

</details>

<details>
<summary><strong>3) Mini-Lecture Guide (Zoom recording)</strong></summary>

### By the end, you should be able to answer:
- What is **informatics** (in one sentence) and how is it different from “data science” or “AI”?
- What **changes** when you can call a foundation model API instead of training your own model?
- How do **Industry 5.0 values** reshape system requirements (human-in-the-loop, resilience, sustainability)?

### Key concepts to listen for:
- **Decision-first thinking:** start from a decision + stakeholder, then work backward to data + system design
- **AI engineering shift:** integrating foundation models into applications (retrieval, prompting, eval, monitoring)
- **Values → requirements mapping:** values become concrete design choices (approval checkpoints, audit logs, fallbacks)

</details>

<details>
<summary><strong>4) Notebook Walkthrough</strong></summary>

**Notebook:** `notebooks/week01/01_informatics_setup_and_decision_framing.ipynb`

**What you will do:**
1) Confirm your environment can run Python + basic libraries  
2) Load a small dataset (course-provided)  
3) Produce a simple summary table that supports a decision  
4) Write 2–3 short “decision statements” from your analysis

**Common pitfalls:**
- Running from the wrong folder: use the provided Colab “Open in Colab” flow or keep paths relative
- Import errors: restart runtime + run all cells
- Overthinking: this week is about **decision framing**, not “model performance”

</details>

<details>
<summary><strong>5) Discussion 1 (Canvas)</strong></summary>

**Prompt:** Pick **one Industry 5.0 value** (human-centricity, sustainability, or resilience). Explain **one AI system design choice** it changes.

**Requirements:**
- 150–300 words
- Include at least 1 credible link (one of the Week 1 required sources is fine)
- Be ready for a 1–2 minute mini-defense during Thursday TA session

**Scoring (1 point total):**
- 0.6 = Canvas post
- 0.4 = Thursday TA response

</details>

<details>
<summary><strong>6) Deliverables (Canvas)</strong></summary>

### M0 (Ungraded) — Cloud check + domain shortlist
Submit:
- A screenshot or short note proving you can run Week 1 notebook (Colab recommended)
- A **domain shortlist (3 options)**:
  - Domain (e.g., manufacturing, healthcare, transportation, cybersecurity, sports)
  - Decision (one sentence)
  - What data might support it (one sentence)

</details>

<details>
<summary><strong>7) Project Milestone</strong></summary>

No graded milestone due this week.  
Next week you will submit **M1 (graded)**: domain + decision + dataset plan.

Tip: choose a domain you *actually care about* — you will live with it all semester.

</details>

---

## Optional Extensions (for extra practice)

- Browse Kaggle datasets (ideas for your domain shortlist): https://www.kaggle.com/datasets  
- Try running the notebook in GitHub Codespaces (optional): https://github.com/features/codespaces
