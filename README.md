# MedSafe AI — Intelligent Healthcare Safety Platform

> **An AI-powered healthcare safety assistant** built with Python and Streamlit, combining rule-based clinical logic, fuzzy text matching, OCR prescription reading, and large-language-model (LLM) guidance to help users understand their medicines and health risks.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [SkillWallet Milestones & Activities](#2-skillwallet-milestones--activities)
3. [Healthcare Scenarios Covered](#3-healthcare-scenarios-covered)
4. [Architecture](#4-architecture)
5. [Module Reference](#5-module-reference)
6. [Application Tabs — Feature Guide](#6-application-tabs--feature-guide)
7. [Setup & Installation](#7-setup--installation)
8. [Running the Application](#8-running-the-application)
9. [Technology Stack](#9-technology-stack)
10. [Project File Structure](#10-project-file-structure)
11. [Configuration](#11-configuration)
12. [Disclaimer](#12-disclaimer)

---

## 1. Project Overview

MedSafe AI addresses a critical gap in consumer healthcare: patients routinely take multiple medicines without understanding which combinations are dangerous, what their symptoms indicate, or when a situation warrants emergency care. This project delivers five integrated safety tools in a single dark-themed web application:

| Tool                             | Core Purpose                                                     |
| -------------------------------- | ---------------------------------------------------------------- |
| **Medicine Interaction Checker** | Detect harmful drug–drug interactions from a typed medicine list |
| **Prescription OCR Reader**      | Extract medicine names directly from a photo of a prescription   |
| **Symptom & Doubt Solver**       | Provide evidence-aligned advice for described symptoms           |
| **Side-Effect Monitor**          | Log and analyse post-medication experiences                      |
| **Emergency Risk Predictor**     | Score the urgency level of symptoms on a 0–100 scale             |

All features operate with **rule-based local logic** so they work offline. When Ollama (local LLM service) is available, every module gains an additional AI explanation layer using LLaMA 3.

---

## 2. SkillWallet Milestones & Activities

### Milestone 1 — Foundation & Data Layer

| Activity                                   | Description                                                                                                                                          | File         |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **Activity 1** — Medicine Database Design  | Build a structured dictionary of 30+ commonly prescribed medicines with generic name, active salt, therapeutic category, and popular brand names     | `med_db.py`  |
| **Activity 2** — Drug Interaction Metadata | Define 15 clinically validated drug–drug interaction pairs with severity rating (HIGH / MODERATE / LOW) and plain-language warning text              | `med_db.py`  |
| **Activity 3** — Symptom Knowledge Base    | Encode 14 symptom categories with rule-based advice, lifestyle recommendations (yoga, diet), red-flag warning signs, and keyword-to-symptom mappings | `symptom.py` |

### Milestone 2 — Intelligence & Risk Engine

| Activity                                 | Description                                                                                                                                                                           | File             |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| **Activity 4** — Emergency Risk Scoring  | Build a 0–100 numeric risk engine using 35 high-risk symptom indicators, 13 moderate-risk indicators, age-based multipliers, and high-risk medicine combinations                      | `risk_engine.py` |
| **Activity 5** — Fuzzy Medicine Matching | Implement `rapidfuzz` WRatio scorer (threshold 75) to tolerate spelling errors and variant medicine brand names typed by users                                                        | `ocr_utils.py`   |
| **Activity 6** — OCR Pipeline            | Integrate Tesseract OCR via `pytesseract` to extract raw text from uploaded prescription images, with image pre-processing for accuracy                                               | `ocr_utils.py`   |
| **Activity 7** — LLM Integration         | Connect four separate LLM-powered analysis functions using Ollama + LLaMA 3 for interaction explanations, symptom guidance, side-effect education, and prescription entity extraction | `ocr_utils.py`   |

### Milestone 3 — User Interface

| Activity                                   | Description                                                                                                                                                 | File               |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| **Activity 8** — Dark-Theme Streamlit UI   | Build a professional five-tab Streamlit application with custom CSS (dark palette, card components, success/warning/error colour-coded boxes, metric tiles) | `streamlit_app.py` |
| **Activity 9** — Session State Management  | Persist OCR-detected medicines, interaction results, side-effect logs, and risk scores across tab switches using `st.session_state`                         | `streamlit_app.py` |
| **Activity 10** — Medicine Interaction Tab | Interactive multi-input checker: type medicine names → fuzzy-match → identify known pairs → severity-coloured interaction cards → optional AI safety note   | `streamlit_app.py` |
| **Activity 11** — Prescription OCR Tab     | Drag-and-drop image upload → Tesseract extraction → rule-based or LLM parsing → auto-populate medicine list for interaction checking                        | `streamlit_app.py` |

### Milestone 4 — Advanced Features & Safety

| Activity                                        | Description                                                                                                                                                                                 | File               |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| **Activity 12** — Symptom & Side-Effect Modules | Two dedicated tabs: Symptom Solver (multi-select + free text → structured advice + AI) and Side-Effect Monitor (log symptom + medicine → AI educational note)                               | `streamlit_app.py` |
| **Activity 13** — Emergency Risk Predictor      | Full emergency triage form: symptom description, age, gender, medicine list, dosages → numeric risk score (0–100) with colour-coded level, contributing factors, and recommended next steps | `streamlit_app.py` |

---

## 3. Healthcare Scenarios Covered

### Scenario A — Elderly Multi-Drug Patient

An elderly patient (65+) takes five or more daily medicines for hypertension, diabetes, and cholesterol. They visit a pharmacy and are given a new antibiotic. MedSafe AI lets them:

1. Type all current medicines into the **Interaction Checker** — receives an immediate HIGH-severity alert if, for example, the antibiotic interacts with their blood thinner.
2. Upload the prescription photo to **Prescription OCR** — medicines are extracted automatically without typing.
3. Describe dizziness and chest tightness in the **Emergency Risk Predictor** — system applies the senior age multiplier and flags CRITICAL risk with instructions to call emergency services.

### Scenario B — Young Adult with Mild Illness

A 25-year-old has a fever, headache, and sore throat. They want to self-medicate safely. MedSafe AI lets them:

1. Select their symptoms in the **Symptom Solver** — receives rule-based dietary advice, yoga recommendations, and a specific red-flag warning list (e.g., "seek doctor if fever exceeds 103°F for more than 3 days").
2. Check whether Paracetamol + Ibuprofen together is safe in the **Interaction Checker** — receives a MODERATE severity warning about combined NSAID/Paracetamol use.
3. Log nausea after medication in the **Side-Effect Monitor** — receives an AI educational note on why nausea occurs and what to monitor.

---

## 4. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   streamlit_app.py                      │
│           (5-Tab Web UI + Session State)                │
└──────┬──────────┬──────────┬──────────┬─────────────────┘
       │          │          │          │
  med_db.py  symptom.py  risk_engine  ocr_utils.py
  (Database)  (Rules)     (Scoring)   (OCR + LLM)
       │          │          │          │
  ┌────┴────┐     │          │    ┌─────┴──────┐
  │Drug     │     │          │    │Tesseract   │
  │Interact │     │          │    │OCR Engine  │
  │Pairs    │     │          │    ├────────────┤
  └─────────┘     │          │    │Ollama LLM  │
                  │          │    │(LLaMA 3)   │
            ┌─────┴────┐     │    └────────────┘
            │Symptom   │     │
            │Knowledge │     │
            │Base      │     │
            └──────────┘     │
                       ┌─────┴────┐
                       │Risk Score│
                       │Engine    │
                       │(0-100)   │
                       └──────────┘
```

**Data Flow:**

```
User Input → streamlit_app.py
    ↓
[Medicine names] → ocr_utils.py (fuzzy match) → med_db.py (lookup)
    ↓                                                ↓
 Identified medicines ──────────────────→ check_interactions()
    ↓                                                ↓
[Optional] Ollama API ←─────────── Interaction warning text
    ↓
AI explanation rendered in UI
```

---

## 5. Module Reference

### `med_db.py` — Medicine Database

**Purpose:** Master data store for all medicine knowledge and interaction rules.

**Key Data Structures:**

```python
MED_DB: dict[str, dict]
# Key: lowercase medicine name
# Value: {generic, salt, category, brand_names[]}
# 30+ entries — common analgesics, antibiotics, antidiabetics,
# antihypertensives, statins, anticoagulants, and more

INTERACTIONS: dict[frozenset, dict]
# Key: frozenset of two medicine names
# Value: {severity: "HIGH"|"MODERATE"|"LOW", warning: str}
# 15 validated drug pairs
```

**Key Functions:**

| Function                            | Parameters  | Returns                                |
| ----------------------------------- | ----------- | -------------------------------------- |
| `get_all_medicine_names()`          | —           | `list[str]` — all medicine names       |
| `get_medicine_info(name)`           | `name: str` | `dict` or `None`                       |
| `check_interactions(medicine_list)` | `list[str]` | `list[dict]` of triggered interactions |

**Sample Interaction Pairs (15 total):**

| Pair                          | Severity |
| ----------------------------- | -------- |
| Aspirin + Warfarin            | HIGH     |
| Metformin + Alcohol           | HIGH     |
| SSRI + MAOI                   | HIGH     |
| Ibuprofen + Paracetamol       | MODERATE |
| Atorvastatin + Clarithromycin | MODERATE |
| Amlodipine + Simvastatin      | MODERATE |

---

### `symptom.py` — Symptom Knowledge Base

**Purpose:** Rule-based symptom library with structured advice for 14 common health conditions.

**Covered Symptoms:**

`fever` · `headache` · `cough` · `sore throat` · `stomach pain` · `nausea` · `dizziness` · `fatigue` · `chest pain` · `shortness of breath` · `skin rash` · `joint pain` · `back pain` · `eye irritation`

**Each symptom entry contains:**

- `label` — display name
- `advice` — list of actionable recommendations
- `yoga` — relevant yoga poses / breathing exercises
- `diet` — dietary guidance
- `warning` — red-flag signs that require medical attention

**Key Functions:**

| Function                   | Parameters  | Returns                          |
| -------------------------- | ----------- | -------------------------------- |
| `parse_symptoms(text)`     | `text: str` | `list[str]` matched symptom keys |
| `get_symptom_advice(keys)` | `list[str]` | `list[dict]` full advice objects |
| `get_all_symptom_labels()` | —           | `list[str]` display labels       |

---

### `ocr_utils.py` — OCR & LLM Utilities

**Purpose:** Handles all image processing, text extraction, fuzzy medicine matching, and Ollama LLM API calls.

**Availability Flags (set at import time):**

```python
OCR_AVAILABLE: bool    # True when pytesseract + Tesseract binary found
OLLAMA_AVAILABLE: bool # True when ollama package is importable
```

**OCR Pipeline:**

```
Image upload (PIL) → image_to_string() (Tesseract) → raw text
    → parse_ocr_text_rule_based()  (keyword + pattern matching)
    → find_medicine_fuzzy()        (WRatio ≥ 75 threshold)
    → list of identified medicines
```

**LLM Functions (all require Ollama running locally):**

| Function                                                       | Purpose                                                       | Model  |
| -------------------------------------------------------------- | ------------------------------------------------------------- | ------ |
| `extract_medicines_with_llm(text)`                             | Structured JSON extraction of medicines + salts from OCR text | llama3 |
| `explain_interaction_with_llm(med1, med2, warning)`            | Plain-language safety explanation for an interaction          | llama3 |
| `generate_symptom_explanation_with_llm(symptom, advice)`       | Personalised symptom guidance                                 | llama3 |
| `generate_side_effect_explanation_with_llm(medicine, symptom)` | Educational side-effect note                                  | llama3 |

All LLM functions use `try/except` — if Ollama is unavailable or returns an error, they return `None` and the UI falls back to rule-based output gracefully.

**Fuzzy Matching Details:**

```python
rapidfuzz.fuzz.WRatio(query, candidate) >= 75
# Handles:
#   "Paracetamol" → "paracetamol" ✓
#   "Crocin"      → "paracetamol" ✓  (brand name match)
#   "Parcetamol"  → "paracetamol" ✓  (typo tolerance)
#   "Metformine"  → "metformin"   ✓  (suffix variation)
```

---

### `risk_engine.py` — Emergency Risk Scoring Engine

**Purpose:** Converts symptom descriptions, patient demographics, and medicine data into a numeric risk score.

**Scoring System:**

```
Risk Score (0–100) = Base keyword score
                   × Age modifier
                   + High-risk medicine combo bonus

Levels:
  LOW       —  0 to 19   (green)
  MODERATE  — 20 to 39   (orange)
  HIGH      — 40 to 69   (red)
  CRITICAL  — 70 to 100  (dark red)
```

**Indicators Used:**

- **35 HIGH-RISK symptom keywords** (e.g., "chest pain", "can't breathe", "unconscious", "stroke", "seizure") — each adds 15–25 points
- **13 MODERATE-RISK keywords** (e.g., "moderate fever", "mild chest", "blurred vision") — each adds 8–12 points
- **Age modifiers:** infant ×1.3, child ×1.1, adult ×1.0, senior (65+) ×1.2
- **High-risk medicine combos** (e.g., blood thinners + NSAIDs) — add flat bonus points

**Primary Function:**

```python
compute_risk_score(
    symptom_text: str,
    age: int,
    gender: str,
    medicines: list[str],
    dosages: str
) -> {
    "score": int,       # 0–100
    "level": str,       # "LOW" | "MODERATE" | "HIGH" | "CRITICAL"
    "color": str,       # hex colour for UI display
    "reasons": list[str],   # matched risk indicators
    "next_steps": list[str] # recommended actions
}
```

---

### `streamlit_app.py` — Main Application

**Purpose:** Full web application. Renders five tabs, manages session state, calls all backend modules, and displays results with custom CSS.

**Session State Keys:**

| Key                   | Type         | Purpose                                                 |
| --------------------- | ------------ | ------------------------------------------------------- |
| `ocr_medicines`       | `list[str]`  | Medicines extracted from OCR, auto-populated into Tab 1 |
| `interaction_results` | `list[dict]` | Most recent interaction check results                   |
| `side_effect_logs`    | `list[dict]` | History of side-effect entries logged                   |
| `risk_result`         | `dict`       | Latest risk scoring result                              |
| `last_ocr_text`       | `str`        | Raw OCR text from last prescription read                |

**CSS Theme:** Dark background (`#0e1117`), card-based layout, colour-coded severity classes (`interaction-high`, `interaction-mod`, `interaction-low`), and custom metric tiles via `st.metric`.

---

## 6. Application Tabs — Feature Guide

### Tab 1 — 💊 Medicine Interaction Checker

**Use case:** User enters medicines they are taking (or those extracted by OCR).

**Workflow:**

1. Type medicine names, one per line, in the text area (brand or generic names accepted).
2. Click **Check Interactions**.
3. System fuzzy-matches names against the 30+ medicine database.
4. Matched medicines are shown with green success badges.
5. The Medicine Details expander reveals generic name, salt, category, and brand names for each identified medicine.
6. Interaction Analysis scans all pairs against the 15 interaction rules:
   - **No interactions:** Green success message.
   - **Interactions found:** Severity-coloured cards (🔴 HIGH / 🟠 MODERATE / 🟡 LOW) with warning text.
   - If Ollama is running, an AI safety note is generated for each interaction.
7. Results are stored in session state so the side-effect tab can reference them.

---

### Tab 2 — 📄 Prescription OCR

**Use case:** User uploads a photo of a handwritten or printed prescription.

**Workflow:**

1. Upload image (JPG, PNG, BMP accepted).
2. Preview is shown.
3. Click **Read Prescription**.
4. Tesseract OCR extracts raw text (displayed in an expander).
5. **Rule-based parser** scans for medicine keywords and fuzzy-matches them.
6. If Ollama is running and **Use AI extraction** is enabled, LLaMA 3 additionally parses the OCR text for structured `{medicine, salt}` pairs.
7. All identified medicines are stored in session state and auto-populate Tab 1 for interaction checking.

**Requirements:** Tesseract OCR binary must be installed at `C:\Program Files\Tesseract-OCR\tesseract.exe` (Windows) or the path edited in `ocr_utils.py`.

---

### Tab 3 — 🩺 Symptom & Doubt Solver

**Use case:** User wants to understand their symptoms and get safe management advice.

**Workflow:**

1. Select symptoms from the multi-select dropdown (14 options) or type a free-text description.
2. System detects matched symptoms via keyword matching.
3. Each matched symptom generates a structured advice card containing:
   - Actionable recommendations
   - Relevant yoga / breathing exercises
   - Dietary guidance
   - **Red-flag warnings** that indicate a need for professional care
4. If Ollama is running, an AI-enhanced explanation card is generated below.

---

### Tab 4 — ⚠️ Side-Effect Monitor

**Use case:** User has started a new medicine and wants to log and understand an unexpected symptom.

**Workflow:**

1. Enter the medicine name and a brief description of the symptom experienced.
2. Click **Log & Analyse**.
3. The entry is added to the session log (date-stamped).
4. If Ollama is running, an AI educational note explains why the symptom may occur and what to monitor.
5. The complete log for the session is displayed below the form.

---

### Tab 5 — 🚨 Emergency Risk Predictor

**Use case:** User or carer wants to quickly determine how urgent a set of symptoms is.

**Workflow:**

1. Fill in the form:
   - Detailed symptom description
   - Patient age and gender
   - Current medicines (comma-separated)
   - Dosage information
2. Click **Assess Risk**.
3. The risk engine calculates a score from 0–100.
4. Result is shown with:
   - A large colour-coded score display
   - Risk level (LOW / MODERATE / HIGH / CRITICAL)
   - Matched risk indicators
   - Specific next-step guidance (e.g., "Call emergency services immediately" for CRITICAL)

---

## 7. Setup & Installation

### Prerequisites

| Requirement   | Version | Notes                         |
| ------------- | ------- | ----------------------------- |
| Python        | 3.9+    | Tested on 3.13                |
| Tesseract OCR | 5.x     | Required for OCR tab only     |
| Ollama        | 0.6.x   | Required for AI features only |

### Step 1 — Create a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**

| Package       | Version | Purpose                                  |
| ------------- | ------- | ---------------------------------------- |
| `streamlit`   | ≥1.32.0 | Web UI framework                         |
| `pytesseract` | ≥0.3.10 | Python wrapper for Tesseract OCR         |
| `Pillow`      | ≥10.0.0 | Image loading and pre-processing         |
| `rapidfuzz`   | ≥3.6.1  | Fuzzy string matching for medicine names |
| `ollama`      | ≥0.1.8  | Local LLM API client                     |

### Step 3 — Install Tesseract OCR (for Prescription OCR Tab)

**Windows:**

1. Download the installer from [UB Mannheim Tesseract Releases](https://github.com/UB-Mannheim/tesseract/wiki).
2. Install to the default path: `C:\Program Files\Tesseract-OCR\`
3. The path is already configured in `ocr_utils.py`. If you install elsewhere, update line:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

**macOS:**

```bash
brew install tesseract
```

**Ubuntu / Debian:**

```bash
sudo apt update && sudo apt install tesseract-ocr
```

### Step 4 — Install Ollama + LLaMA 3 (for AI Features)

1. Download Ollama from [https://ollama.com](https://ollama.com) and install.
2. Pull the LLaMA 3 model:
   ```bash
   ollama pull llama3
   ```
3. Start the Ollama service (keep running in background):
   ```bash
   ollama serve
   ```

> **Note:** All five application tabs work fully without Ollama. AI features degrade gracefully to rule-based fallbacks when Ollama is unavailable.

---

## 8. Running the Application

```bash
# From the project directory, with virtual environment activated:
streamlit run streamlit_app.py
```

The application opens at **http://localhost:8501** in your default browser.

**Application Logs:**  
Runtime logs are written to `medsafe_log.txt` in the project directory. Each log entry includes a timestamp, log level, and event description.

---

## 9. Technology Stack

```
Frontend        → Streamlit 1.x (Python web framework, custom CSS dark theme)
OCR             → Tesseract 5.x + pytesseract + Pillow
Fuzzy Matching  → rapidfuzz (WRatio algorithm, threshold 75)
LLM             → Ollama 0.6.x + LLaMA 3 (local, no API key required)
Data Storage    → In-memory Python dicts + Streamlit session state
Logging         → Python standard logging → medsafe_log.txt
```

No external database, no cloud APIs, and no internet access required at runtime (beyond initial Ollama model download).

---

## 10. Project File Structure

```
e:\skillwallet\
│
├── streamlit_app.py     # Main application — 5-tab Streamlit UI, session state,
│                        # custom CSS, all user interactions (~500 lines)
│
├── med_db.py            # Medicine database (30+ entries) and interaction
│                        # metadata (15 drug pairs) with lookup functions
│
├── symptom.py           # 14-symptom knowledge base with advice, yoga,
│                        # diet guidance, and red-flag warnings
│
├── ocr_utils.py         # Tesseract OCR pipeline, rapidfuzz matcher,
│                        # and 4 Ollama LLM API functions
│
├── risk_engine.py       # Emergency risk scoring engine (0–100 scale)
│                        # with 48 indicators and age/medicine modifiers
│
├── requirements.txt     # Python dependency specifications
├── README.md            # This file
└── medsafe_log.txt      # Runtime application log (auto-created)
```

---

## 11. Configuration

All configuration is embedded in source files. Key values to adjust if needed:

| Setting               | File               | Location                | Default                                        |
| --------------------- | ------------------ | ----------------------- | ---------------------------------------------- |
| Tesseract binary path | `ocr_utils.py`     | Line ~15                | `C:\Program Files\Tesseract-OCR\tesseract.exe` |
| Ollama model name     | `ocr_utils.py`     | LLM function calls      | `"llama3"`                                     |
| Fuzzy match threshold | `ocr_utils.py`     | `find_medicine_fuzzy()` | `75`                                           |
| Risk level thresholds | `risk_engine.py`   | `compute_risk_score()`  | LOW<20, MOD<40, HIGH<70                        |
| Log file path         | `streamlit_app.py` | `logging.FileHandler`   | `medsafe_log.txt`                              |

---

## 12. Disclaimer

> **MedSafe AI is an educational tool only.**  
> All outputs — including interaction warnings, symptom advice, risk scores, and AI explanations — are informational and must **not** be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider before making any medical decision. In any emergency, call your local emergency services immediately.
