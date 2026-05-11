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
│   │   ├── parameter_mapper.py   # Maps parameters to schema fields
│   │   └── json_builder.py       # Assembles final JSON output
│   │
│   ├── models/
│   │   └── schemas.py            # Pydantic models for validation
│   │
│   ├── config/
│   │   └── parser_config.yaml    # Column mappings and sheet config
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
  "sheet_name": "ICC",
  "scenario_id": "ICC-001",
  "scenario_title_jp": "設定速度維持",
  "parameters": {
    "自車速度": "100 km/h",
    "路面状態": "乾燥"
  }
}
```

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
- [x] Validation Layer
- [x] Logging

### 🔜 Phase 2 — AI Translation & Artifact Generation
- [ ] Japanese → English translation via OpenAI
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