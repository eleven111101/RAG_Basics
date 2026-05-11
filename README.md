# ADAS Scenario Translation & Intelligence Pipeline

> Enterprise-grade automation pipeline for parsing, translating, and generating structured test artifacts from Japanese ADAS scenario Excel sheets.

---

## What It Does

- Parses structured Japanese ADAS Excel sheets
- Extracts scenario-wise and sub-scenario-wise data
- Converts scenarios into structured JSON
- Generates AI-driven English test steps *(Phase 2)*
- Translates Japanese → English via OpenAI *(Phase 2)*
- Produces translated Excel artifacts *(Phase 2)*
- Stores artifacts in Git/S3 *(Phase 2)*
- Tracks AI token usage and cost analytics *(Phase 2)*

---

## Current Phase: Phase 1 — Excel → Structured JSON

Phase 1 focuses exclusively on deterministic parsing — no AI yet.

**Goals:**
- Read and parse Excel files
- Detect and extract scenarios
- Map parameters to structured fields
- Build validated JSON output
- Log all operations centrally

---

## Project Structure

```
translation-parser/
│
├── app/
│   ├── parser/
│   │   ├── excel_reader.py       # Reads Excel files via openpyxl
│   │   ├── sheet_parser.py       # Parses individual sheets
│   │   ├── scenario_parser.py    # Extracts scenario blocks
│   │   ├── parameter_mapper.py   # Maps raw JP keys → canonical keys
│   │   └── json_builder.py       # Assembles final JSON output
│   │
│   ├── models/
│   │   └── schemas.py            # Pydantic models for validation
│   │
│   ├── config/
│   │   ├── parser_config.yaml        # Column mappings and sheet config
│   │   └── parameter_mapping.yaml    # Canonical parameter mapping table
│   │
│   └── utils/
│       ├── helpers.py
│       └── logger.py             # Centralized logging
│
├── input/                        # Drop Excel files here
├── output/                       # Parsed JSON written here
├── logs/                         # application.log written here
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Excel Structure

The parser assumes a stable enterprise Excel structure with scenario grouping and fixed column mappings.

| Scenario ID | Parameter Name | Value    | Scenario Title |
|-------------|----------------|----------|----------------|
| ICC-001     | 自車速度           | 100 km/h | 設定速度維持         |
|             | 路面状態           | 乾燥       |                |

---

## Output JSON Format

```json
{
  "sheet_name": "FEB シナリオ",
  "scenario_id": "FEB-001",
  "scenario_title_jp": "乾燥路面・静止車両への接近",
  "parameters": {
    "自車速度": "60 km/h",
    "路面状態": "乾燥"
  },
  "parameters_canonical": {
    "ego_vehicle_speed": "60 km/h",
    "road_condition": "乾燥"
  }
}
```

Both the raw Japanese parameters and their canonical equivalents are always preserved in output.

---

## Canonical Parameter Mapping Layer

### Overview

The Canonical Parameter Mapping Layer converts raw client-specific Japanese parameter names into standardized internal semantic keys. It acts as the **semantic normalization engine** of the pipeline — sitting between raw extraction and AI translation.

> Canonical mapping is **not** translation. These are distinct layers with different purposes.

| Layer               | Purpose                                    |
|---------------------|--------------------------------------------|
| Raw Japanese        | Original client/source data                |
| Canonical Key       | Internal semantic representation           |
| English Translation | Human-readable localized text *(Phase 2)*  |

---

### What Is a Canonical Key?

A canonical key is a stable, snake_case internal identifier used consistently across the entire platform regardless of client or language.

| Raw Parameter | Canonical Key       |
|---------------|---------------------|
| 自車速度          | `ego_vehicle_speed` |
| 路面状態          | `road_condition`    |
| 天候            | `weather`           |
| 前方障害物         | `forward_obstacle`  |

---

### Example Flow

**Raw parsed data:**
```json
{
  "自車速度": "60 km/h",
  "路面状態": "乾燥"
}
```

**After canonical mapping:**
```json
{
  "ego_vehicle_speed": "60 km/h",
  "road_condition": "乾燥"
}
```

**After human translation layer *(Phase 2)*:**
```json
{
  "parameter_name_en": "Ego Vehicle Speed",
  "parameter_value_en": "60 km/h"
}
```

---

### Why This Matters for AI

Without canonicalization, the AI must understand Japanese, infer automotive context, and infer parameter intent — all at once. With canonical keys, the AI receives clean structured semantic information, which improves accuracy, reduces token usage, and makes prompts deterministic.

---

### Mapping Config

Mappings are defined in `app/config/parameter_mapping.yaml`:

```yaml
自車速度: ego_vehicle_speed
路面状態: road_condition
天候: weather
前方障害物: forward_obstacle
```

---

### Unmapped Parameters

If no canonical mapping exists for a parameter, the original Japanese key is preserved as-is in `parameters_canonical`. This helps identify new parameters, ontology gaps, and client-specific extensions.

```json
{
  "摩擦係数 μ": "0.45"
}
```

---

### Architecture Position

```
Excel
  ↓
Raw Extraction
  ↓
Canonical Mapping        ← This layer
  ↓
Semantic Normalization
  ↓
AI Translation (Phase 2)
  ↓
Step Generation (Phase 2)
```

---

### Enterprise Benefits

- Deterministic AI prompts across all clients
- Stable semantic contracts independent of source language
- Reusable validation, analytics, and automation logic
- Multilingual scalability without changing internal schemas
- Foundation for the future **ADAS Semantic Ontology Layer**

---

### Future: Value Canonicalization *(Phase 2)*

In addition to key normalization, values will also be standardized:

| Raw Value | Canonical Value |
|-----------|-----------------|
| 乾燥        | `dry`           |
| 湿潤        | `wet`           |
| 晴れ        | `clear`         |

---

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_key_here         # Required for Phase 2
ANONYMIZED_TELEMETRY=false           # Silences ChromaDB telemetry
```

---

## Run

```bash
python main.py
```

Place your Excel file in `input/` before running. Parsed JSON will be written to `output/`.

---

## Logging

All modules write to a centralized log file:

```
logs/application.log
```

Example output:
```
2026-05-11 12:40:11 | INFO | app.parser.excel_reader | Reading Excel File
```

---

## Tech Stack

| Component           | Technology         |
|---------------------|--------------------|
| Language            | Python             |
| Excel Parsing       | openpyxl           |
| Validation          | Pydantic           |
| Logging             | Python logging     |
| AI Translation      | OpenAI *(Phase 2)* |
| Storage             | Amazon S3 *(Phase 2)* |
| Git Automation      | GitPython *(Phase 2)* |
| API Layer           | FastAPI *(Phase 2)* |
| Queue               | Redis/Celery *(Phase 2)* |
| Artifact Generation | pandas/openpyxl *(Phase 2)* |

---

## Roadmap

### ✅ Phase 1 — Parser Engine
- [x] Excel Reader
- [x] Scenario Parser
- [x] JSON Builder
- [x] Canonical Parameter Mapping
- [x] Unmapped Parameter Fallback
- [x] Validation Layer
- [x] Logging

### 🔜 Phase 2 — AI Translation & Artifact Generation
- [ ] Japanese → English translation via OpenAI
- [ ] Value canonicalization (乾燥 → `dry`, 湿潤 → `wet`)
- [ ] AI test step generation
- [ ] Translation memory (avoid retranslating repeated terms)
- [ ] Cost analytics (tokens, model, cost per run)
- [ ] Translated Excel artifact writer
- [ ] S3 storage integration
- [ ] Git artifact branch automation

---

## Design Principles

- **Deterministic parsing** — stable, schema-driven, no guesswork
- **Modular architecture** — each concern isolated in its own module
- **Enterprise auditability** — full logging and validation at every step
- **Low AI token cost** — translation memory avoids redundant API calls
- **Automotive-domain consistency** — glossary support for ADAS terminology

---

## Long-Term Vision

```
Git Webhook
      ↓
FastAPI Orchestrator
      ↓
Parser Engine
      ↓
Scenario Classification
      ↓
AI Translation Pipeline
      ↓
Validation Engine
      ↓
Artifact Generator
      ↓
S3 + Git Artifact Branch
```

Build a scalable **ADAS Scenario Intelligence & Localization Platform** for enterprise automotive validation workflows.