> **Word Document version** with active hyperlinks is available in this folder and on Canvas.

# AI-Enabled Informatics for Engineers (Spring 2026)
**Rutgers ISE Course (Asynchronous / GitHub-first)**

**Instructor:** Ron Iammartino, PhD — [ri128@rutgers.edu](mailto:ri128@rutgers.edu)  
**TA:** Keya Wang — [kw653@scarletmail.rutgers.edu](mailto:kw653@scarletmail.rutgers.edu)  
**Term:** Spring 2026

---

## Course Sites (Start Here)
- **Canvas (announcements, submissions, discussions, grades):** https://rutgers.instructure.com/courses/385339  
- **GitHub (weekly materials, lecture pages, notebooks, assignments, project):** https://github.com/AI-Enabled-Informatics-for-Engineers/ISE

---

## Meetings & Recordings
### Asynchronous Lectures (Zoom recordings)
- **Weekly lecture recordings** posted **Tuesday evenings**  
- **Zoom link (Lecture Recordings):** https://rutgers.zoom.us/j/91287883862?pwd=PiErrbHksviZpre1dVv4fu51PgaPhs.1  
- Full details + calendar links: **Appendix C**

### Required TA Sessions (Live, synchronous)
- **Monday:** 12:10–1:30pm ET  
- **Thursday:** 12:10–1:30pm ET  
- **Zoom link (TA Sessions):** https://rutgers.zoom.us/j/99163542603?pwd=Y6Geby7WVwbWrMawgW8PFXnwmMNQjp.1  
- Full details + calendar links: **Appendix C**

**Office Hours:** By request (email to schedule)

---

# 1) Course Description
This course treats **informatics as an engineering discipline**: how we transform **data → information → decisions → reliable action**, now accelerated by modern AI (foundation models, embeddings, retrieval systems, and agentic workflows). We use **Industry 5.0** as an early framing lens (**human-centric, sustainable, resilient systems**) and apply it to architecture and deployment decisions across the term via a **milestone-based real-world project**.

---

# 2) Learning Objectives
By the end of the course, students will be able to:

1. Explain core informatics concepts and apply them to engineering decision workflows.  
2. Design data models and pipelines that support analytics/ML/LLM systems.  
3. Build and evaluate at least one AI-enabled informatics system (predictive, RAG, or security/risk analytics).  
4. Use cloud tools (Rutgers-supported Azure/AWS access or Colab) for a minimal working prototype.  
5. Apply responsible AI and security practices using authoritative frameworks (NIST AI RMF; OWASP LLM Top 10; basic crypto/key-management hygiene).  
6. Communicate design tradeoffs using concise architecture memos and diagrams.

---

# 3) Prerequisites / Readiness
Students should be comfortable with:
- Python basics (functions, data structures, notebooks)
- Basic probability/statistics (distributions, expectation, uncertainty, confidence, error rates)

**Pre-course refresh (Week 0):**
- Kaggle Learn: Python — https://www.kaggle.com/learn/python  
- Khan Academy: Statistics & probability — https://www.khanacademy.org/math/statistics-probability  

---

# 4) Required & Recommended Materials
## Primary Text (Required)
**Chip Huyen**, *AI Engineering: Building Applications with Foundation Models* (2024/2025)  
(Digital text available via Rutgers Library)

## Informatics Foundations (Required)
- NCBI Informatics overview — https://www.ncbi.nlm.nih.gov/books/NBK470564/  
- University of Edinburgh: “What is Informatics?” — https://informatics.ed.ac.uk/about/what-is-informatics  

## Industry 5.0 (Required + Recommended)
- European Commission: Industry 5.0 overview — https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/industry-50_en  
- EC publication hub (recommended deeper reading) — https://research-and-innovation.ec.europa.eu/knowledge-publications-tools-and-data/publications/all-publications/industry-50-towards-sustainable-human-centric-and-resilient-european-industry_en  

## Responsible AI + Security (Required later in term)
- NIST AI RMF landing page — https://www.nist.gov/itl/ai-risk-management-framework  
- NIST AI RMF PDF — https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf  
- OWASP Top 10 for LLM Apps — https://owasp.org/www-project-top-10-for-large-language-model-applications/  
- Crypto 101 (site) — https://www.crypto101.io/  
- Crypto 101 (PDF) — https://www.crypto101.io/Crypto101.pdf  
- NIST Key Management (SP 800-57 Pt 1 Rev 5) — https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final  

---

# 5) Rutgers Student Cloud Accounts (Azure + AWS) + Colab
## Rutgers-supported entry points (recommended)
- Rutgers Cloud Services overview — https://it.rutgers.edu/cloud-services/  
- Rutgers Cloud Services support — https://it.rutgers.edu/cloud-services/get-cloud-support/  
- Rutgers Software Portal listing — https://it.rutgers.edu/software-portal/knowledgebase/products-in-the-university-software-portal/  
- Rutgers public software catalog — https://software.rutgers.edu/public-catalog/  

## Google Colab (Recommended)
- Google Colab — https://colab.research.google.com/  

## Azure (Alternative)
- Azure for Students — https://azure.microsoft.com/en-us/free/students  

## AWS (Alternative)
- AWS Educate — https://aws.amazon.com/education/awseducate/  
- Rutgers AWS AppStream example access pattern — https://its.comminfo.rutgers.edu/knowledge-base/how-do-i-access-and-use-my-aws-appstream-account/  

**Course policy:** Students may implement labs on **Colab, Azure, or AWS**; rubrics evaluate **outcomes**, not vendor choice.

---

# 6) Course Structure (Asynchronous)
Each week includes:
- Lecture recording (posted weekly)
- Weekly applied discussion (**post in Canvas**, respond during **Thursday TA session**)
- Project milestone (selected weeks; see schedule + Appendix B)
- Graded assignments every other week (**Weeks 2, 4, 6, 8, 10, 12, 14**)

---

# 7) Grading (High Level)
- Weekly discussions (applied): **10%**  
- Labs / Assignments (every other week): **30%** (Appendix A + GitHub)  
- Midterm (Week 8): **15%**  
- Semester project (milestones + final): **30%** (Appendix B + GitHub)  
- Final exam (Week 14): **15%**

> **Point rules for Canvas items (implementation detail):**
> - **Assignments 1–5:** 6 points each  
> - **Project Milestones M1–M6:** 4 points each  
> - **Project Milestone M7 (Final):** 6 points  
> - **Each discussion:** 1 point (**60%** Canvas post, **40%** in-class response during Thursday TA session)

(See Appendix A and B for detailed rubrics.)

---

# 8) Weekly Schedule (Readings, Discussions, Tools, Deliverables)

> **Note:** All weekly materials live in GitHub (lecture pages, notebooks, templates). Canvas is for submissions/discussions/grades.

## Week 1 (Jan 20–26) — Informatics framing + Industry 5.0 + cloud setup
**Primary text:** Chapter 1 — *Introduction to Building AI Applications with Foundation Models*  
**Required:**
- NCBI Informatics overview — https://www.ncbi.nlm.nih.gov/books/NBK470564/  
- Edinburgh “What is Informatics?” — https://informatics.ed.ac.uk/about/what-is-informatics  
- Industry 5.0 overview — https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/industry-50_en  

**Discussion (Canvas):** Pick one Industry 5.0 value; explain how it changes AI system design choices.  
**Deliverable (ungraded):** Cloud access check (Colab or Azure or AWS) + **project domain shortlist** (3 options).

---

## Week 2 (Jan 27–Feb 2) — Foundation models + data foundations for decision systems
**Primary text:** Chapter 2 — *Understanding Foundation Models*  
**Interactive SQL (choose one):**
- SQLZoo — https://sqlzoo.net/  
- Kaggle Intro to SQL — https://www.kaggle.com/learn/intro-to-sql  

**Discussion (Canvas):** “How do schema choices create or destroy decision quality?”  
**Assignment 1 (graded):** SQL + decision questions  
- Write 5 decision questions + SQL queries + short interpretation.  
**Project Milestone M1 (graded):** Pick domain + decision + dataset plan.

---

## Week 3 (Feb 3–9) — Dataset engineering + pipelines as informatics reliability
**Primary text:** Chapter 8 — *Dataset Engineering*  
**Tooling:** Prefect docs — https://docs.prefect.io/  
**Discussion (Canvas):** “Data correctness vs decision correctness—give an example.”  
**Project work:** Start pipeline sketch (ingest → transform → store → serve).

---

## Week 4 (Feb 10–16) — Evaluation methodology tied to decisions and costs
**Primary text:** Chapter 3 — *Evaluation Methodology*  
**Optional framework:** NIST AI RMF — https://www.nist.gov/itl/ai-risk-management-framework  
**Discussion:** “Why accuracy is a weak metric in many informatics problems.”  
**Assignment 2 (graded):** decision-aligned evaluation memo  
**Project Milestone M2:** Pipeline + schema + evaluation plan (1 diagram + 1–2 pages).

---

## Week 5 (Feb 17–23) — Prompting as interface + human-centered informatics
**Primary text:** Chapter 5 — *Prompt Engineering*  
**Recommended deeper reading:** https://research-and-innovation.ec.europa.eu/knowledge-publications-tools-and-data/publications/all-publications/industry-50-towards-sustainable-human-centric-and-resilient-european-industry_en  
**Discussion:** “Where should the ‘human-in-the-loop’ sit in your system and why?”  
**Project work:** Define user workflow + minimum UI/UX.

---

## Week 6 (Feb 24–Mar 2) — Inference optimization + operational constraints
**Primary text:** Chapter 9 — *Inference Optimization*  
**Optional dataset:** NASA C-MAPSS — https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data  
**Discussion:** “What is your system’s tightest bottleneck (cost, latency, reliability)?”  
**Assignment 3 (graded):** MVP build  
**Project Milestone M3:** MVP demo checkpoint.

---

## Week 7 (Mar 3–9) — System architecture + user feedback loops
**Primary text:** Chapter 10 — *AI Engineering Architecture and User Feedback*  
**Discussion:** “How do you detect ‘decision drift’ in the real world?”  
**Project work:** Add monitoring/logging plan + feedback loop.

---

## Spring Break (Mar 14–22) — No classes

---

## Week 8 (Mar 24–30) — Midterm (async) + architecture checkpoint
**Primary text:** Chapter 4 — *Evaluate AI Systems*  
**Midterm (graded):**
- Part A: timed short answers (concept + application)  
- Part B: artifact submission (system diagram + 1-page justification)  
**Project Milestone M4:** Midterm architecture packet.

---

## Week 9 (Mar 31–Apr 6) — Embeddings + semantic retrieval as informatics
**Primary text:** Chapter 6 — *RAG and Agents* (retrieval portion)  
**Tools:**
- Chroma — https://docs.trychroma.com/docs/overview/introduction  
- FAISS — https://github.com/facebookresearch/faiss  
**Discussion:** “What does ‘meaning’ in embeddings capture—and what does it miss?”  
**Project work:** Retrieval index or explainability hook.

---

## Week 10 (Apr 7–13) — RAG systems: grounding + evaluation
**Primary text:** Chapter 6 — *RAG and Agents* (continued)  
**References:**
- OpenAI Cookbook — https://cookbook.openai.com/  
- RAG explainer — https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts  
- LangChain docs — https://docs.langchain.com/  

**Assignment 4 (graded):** evaluation harness  
**Project Milestone M5:** “Advanced capability” checkpoint.

---

## Week 11 (Apr 14–20) — Agentic workflows + human oversight
**Primary text:** Chapter 6 — *RAG and Agents* (agents portion)  
**Required security lens:** OWASP LLM Top 10 — https://owasp.org/www-project-top-10-for-large-language-model-applications/  
**Discussion:** “What’s the smallest useful autonomy that still creates value?”  
**Project work:** Add a human-in-the-loop approval point + audit log.

---

## Week 12 (Apr 21–27) — Causal informatics: interventions and decision impact
**Tool:** DoWhy — https://www.pywhy.org/dowhy/  
**Assignment 5 (graded):** causal mini-study  
**Discussion:** “When is prediction insufficient—you need causal reasoning to act?”

---

## Week 13 (Apr 28–May 4) — Responsible AI + cybersecurity + encryption basics
**Primary text:** Chapter 4 — *Evaluate AI Systems* (revisited for governance)  
**Required:**
- NIST AI RMF — https://www.nist.gov/itl/ai-risk-management-framework  
- OWASP LLM Top 10 — https://owasp.org/www-project-top-10-for-large-language-model-applications/  
- Crypto 101 — https://www.crypto101.io/  
- NIST SP 800-57 — https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final  

**Discussion:** Threat model your system.  
**Project Milestone M6:** Trust/security package.

---

## Week 14 (May 5–13) — Final project + final exam
**Final Project (graded):** demo video (6–10 min) + report + runnable artifact  
**Final Exam (graded):** applied questions tied to project design choices  
**Project Milestone M7:** Final submission.

---

# 9) Semester Project (7 Milestones Total)
**Project Goal:** Build an AI-enabled informatics system that improves a real decision workflow (**not “just a model”**).

**Milestones:**
- **M1 (Week 2):** Domain + decision + dataset plan  
- **M2 (Week 4):** Pipeline + schema + evaluation plan  
- **M3 (Week 6):** MVP demo checkpoint  
- **M4 (Week 8):** Architecture packet (midterm checkpoint)  
- **M5 (Week 10):** Advanced capability  
- **M6 (Week 13):** Trust & security package  
- **M7 (Week 14):** Final demo + report + runnable artifact  

**Suggested dataset menu (examples; students may propose alternatives):**
- NASA C-MAPSS — https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data  
- CICIDS2017 — https://www.unb.ca/cic/datasets/ids-2017.html  
- UCI Diabetes — https://archive.ics.uci.edu/ml/datasets/diabetes%2B130-us%2Bhospitals%2Bfor%2Byears%2B1999-2008  
- PJM energy consumption — https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption  

---

# 10) Academic Integrity and Use of AI Tools (Rutgers Policy)
Rutgers Academic Integrity Policy: https://academicintegrity.rutgers.edu/node/7  

**Course-specific AI guidance:**
- AI tools may be used for brainstorming, debugging, and formatting, but submissions must reflect your own understanding.  
- Any use of AI-generated text/code must be disclosed in a short **AI Use Statement** (tool used, what it did, what you validated/changed).  
- The midterm includes an artifact-based component designed to assess independent reasoning.

---

# 11) Accessibility and Student Support (Rutgers)
- Office of Disability Services (ODS): https://ods.rutgers.edu/home  
- CAPS: https://health.rutgers.edu/counseling-services  
- Religious observances (absence policy): https://studentsupport.rutgers.edu/services/absence-and-verification-notices/absences-for-religious-obligations  

---

# Appendix A — Assignment Grading Rubrics
> Detailed rubrics, submission checklists, and credible resources live in GitHub. (This appendix is the syllabus summary.)

## A1 — SQL + Decision Questions (Week 2)
**Purpose:** Translate decisions into data questions and answer them with SQL.  
**Helpful resources:** SQLZoo (https://sqlzoo.net/), Kaggle Intro to SQL (https://www.kaggle.com/learn/intro-to-sql)

## A2 — Decision-Aligned Evaluation Memo (Week 4)
**Purpose:** Evaluate systems using decision outcomes and costs (not just accuracy).  
**Helpful resources:** NIST AI RMF (https://www.nist.gov/itl/ai-risk-management-framework)

## A3 — MVP Build (Week 6)
**Purpose:** Build a minimal end-to-end informatics system supporting a decision.  
**Helpful resources:** OpenAI Cookbook (https://cookbook.openai.com/), LangChain (https://docs.langchain.com/)

## A4 — Evaluation Harness (Week 10)
**Purpose:** Measure quality, identify failure modes, propose mitigations.  
**Helpful resources:** OpenAI RAG explainer (https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts), Chroma (https://docs.trychroma.com/docs/overview/introduction)

## A5 — Causal Mini-Study (Week 12)
**Purpose:** Use causal reasoning when prediction is not enough.  
**Helpful resources:** DoWhy (https://www.pywhy.org/dowhy/)

---

# Appendix B — Project Milestone Rubrics & Instructions
> Detailed milestone “cut sheets,” checklists, and rubrics live in GitHub. (This appendix is the syllabus summary.)

- **M0 (Week 1, ungraded):** Domain shortlist  
- **M1 (Week 2):** Problem definition (domain + decision + dataset plan)  
- **M2 (Week 4):** Pipeline + schema + evaluation plan  
- **M3 (Week 6):** MVP demo checkpoint  
- **M4 (Week 8):** Architecture packet (midterm checkpoint)  
- **M5 (Week 10):** Advanced capability  
- **M6 (Week 13):** Trust/security package  
- **M7 (Week 14):** Final delivery  

---

# Appendix C — Zoom Dial-in Information
## Weekly Lecture Recordings
Join: https://rutgers.zoom.us/j/91287883862?pwd=PiErrbHksviZpre1dVv4fu51PgaPhs.1  
Calendar (ICS): https://rutgers.zoom.us/meeting/tJUvf-6gpjgiHNZw718E1KFVYJ7aybqNEIL4/ics?icsToken=DCUs8R4a4XXkAaQx8AAALAAAAA4kx7M2Rwk_W-Vb_NsjI6JI84g_NgjdeP6n199qu3-TqcbQcmTfnLSfQE9nQANT7Ws-DgDHC1W7tskXBDAwMDAwMQ  
Meeting ID: 912 8788 3862  
Passcode: 101239  

## Required TA Sessions (live sessions Mon/Thu with TA 1210-130pm ET)
Join: https://rutgers.zoom.us/j/99163542603?pwd=Y6Geby7WVwbWrMawgW8PFXnwmMNQjp.1  
Calendar (ICS): https://rutgers.zoom.us/meeting/tJ0sceqtqjksGtdP0lNophBYoJfspagsZ8Ns/ics?icsToken=DCFr5E8BOiPE3bhoGgAALAAAAMdyqhUlW65lCb0f9kKncaTUFSwyAse-egk4PGfY1wOeK38fGD06AobZEBS7K-GwxkOgCukifV0hG15B_TAwMDAwMQ  
Meeting ID: 991 6354 2603  
Passcode: 893075  

Rutgers OIT Help Desk: https://it.rutgers.edu/help-support/
