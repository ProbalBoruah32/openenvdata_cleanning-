---
title: Data Cleaning OpenEnv Environment
emoji: 🧹
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: 3.11
app_file: app_simple.py
pinned: false
---

# Data Cleaning OpenEnv Environment

A production-ready reinforcement learning environment for training agents to clean structured data. Compliant with OpenEnv specification with typed models, graders, and multi-task support.

## Overview

This environment simulates a real-world data cleaning task where agents learn to:
- Fill missing values in numeric and object columns
- Normalize text data (lowercase, trim whitespace)
- Remove duplicate rows based on specific columns

The environment provides:
[OK] Full OpenEnv API specification (/reset, /step, /state)
[OK] 5 tasks with difficulty variation (easy -> medium -> hard)
[OK] Intelligent grading system (0.0 - 1.0 scores)
[OK] Meaningful reward function with partial progress signals
[OK] FastAPI backend with Docker deployment
[OK] Production-ready inference pipeline

---

## Quick Start

### 1. Setup Environment

```bash
cd data-cleaning-env
python -m venv .venv

# Windows:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

### 2. Run Locally

```bash
& .venv\Scripts\Activate.ps1 ; uvicorn app:app --reload
# Server at http://localhost:8000
```

### 3. Run Inference

```bash
python inference.py
python run_all_tasks.py
```

### 4. Docker Deployment

```bash
docker build -t data-cleaning-env:latest .
docker run -p 8000:8000 --env-file .env data-cleaning-env:latest
curl http://localhost:8000/reset
```

---

## Environment Specification

### Action Space (Type: Discrete, 3 actions)

| ID | Name | Description | Reward |
|----|------|-------------|--------|
| 0 | fill_missing | Fill missing values (mean/ffill/bfill) | 0.3 |
| 1 | normalize | Lowercase and trim whitespace | 0.3 |
| 2 | remove_duplicates | Remove duplicate rows by name | 0.4 |

### Observation Space (Type: Dictionary)

```python
{
    "data": List[Dict],      # List of cleaned records
    "step_count": int       # Number of steps
}
```

### Final Score Space (Type: Float in [0.0, 1.0])

Based on grade_hard() grader:
- No missing values: +0.33
- Normalized text: +0.33
- No duplicate names: +0.34

---

## API Endpoints

GET /reset
POST /step (Request: {"action_type": "fill_missing|normalize|remove_duplicates"})
GET /state
GET /tasks
POST /clean-file (multipart/form-data)

---

## Tasks Overview

Easy (1 task):
- easy_data_cleaning: Fill missing values in 2-row dataset
- Expected Score: 0.6-0.8

Medium (2 tasks):
- medium_data_cleaning: Normalize mixed-case names
- medium_missing_cleaning: Fill missing values in 3-row dataset
- Expected Score: 0.5-0.8

Hard (2 tasks):
- hard_data_cleaning: Full pipeline
- hard_complex_cleaning: Complex 8-row dataset
- Expected Score: 0.9-1.0

Summary:
Easy Average: 0.70
Medium Average: 0.65
Hard Average: 1.00
Overall Average: 0.80
Score Variation: 0.40

---

## Grading System

grade_hard() Scoring:

Check 1: No missing values -> +0.33
Check 2: Text normalization -> +0.33
Check 3: No duplicate names -> +0.34
Total: 1.0 max

---

## Inference Pipeline

Expected Output Format:

[START]
task: uploaded_data_cleaning

[STEP]
action: fill_missing
reward: 0.3

[STEP]
action: normalize
reward: 0.3

[STEP]
action: remove_duplicates
reward: 0.4

[END]
score: 1.0

---

## Environment Variables

OPENAI_API_KEY - Your OpenAI API key
HF_TOKEN - Your Hugging Face token
API_BASE_URL - API endpoint (default: http://localhost:8000)
MODEL_NAME - LLM model (default: gpt-3.5-turbo)

Optional:
ENVIRONMENT - development | production
DEBUG - true | false
LOG_LEVEL - DEBUG | INFO | WARNING | ERROR
HOST - Server host (default: 0.0.0.0)
PORT - Server port (default: 8000)

---

## Project Structure

data-cleaning-env/
|- app.py                      # FastAPI application
|- inference.py                # Baseline inference script
|- run_all_tasks.py           # Task runner
|- config.py                  # Configuration
|- requirements.txt           # Dependencies
|- openenv.yaml              # Specification
|- Dockerfile                # Docker image
|- .env.example              # Env template
|- README.md                 # This file
|
|- env/                      # Package
   |- __init__.py
   |- environment.py         # DataCleaningEnv
   |- models.py              # Types
   |- tasks.py               # Tasks
   |- graders.py             # Grading

...

---

## System Requirements

Minimum:
- CPU: 2 vCPU
- Memory: 8 GB RAM
- Python: 3.8+

Tested on: Python 3.11, FastAPI 0.95+, Pandas 1.3+

---

## Performance &Constraints

Max Steps: 5
Timeout: 60 seconds per action
Inference Runtime: < 20 minutes
API Response: < 1 second
Docker Build: < 5 minutes

---

## Validation & Testing

Pre-Submission Checklist:

```bash
python validator.py
curl http://localhost:8000/reset
docker build -t data-cleaning-env:latest .
python inference.py
```

Automated Validation:
[OK] openenv.yaml parsing
[OK] Typed models
[OK] API responses (200 status)
[OK] Inference execution
[OK] Score range (0.0-1.0)
[OK] Task count (3+)
[OK] Dockerfile build

---

## Deployment to Hugging Face Spaces

1. Create HF Repository
2. Push Code
3. Configure Dockerfile (auto-detected)
4. Set Secrets: OPENAI_API_KEY, HF_TOKEN
5. Verify: curl https://YOUR_USERNAME-data-cleaning-env.hf.space/reset

---

## Troubleshooting

Docker build fails:
  pip freeze > requirements.txt

OPENAI_API_KEY error:
  export OPENAI_API_KEY="sk-..."
  or add to .env file

Port 8000 in use:
  uvicorn app:app --port 8001

Inference timeout:
  Check task complexity and system resources

---

## License

MIT License

---

## Contact

For questions or issues, please create a GitHub issue or contact the maintainers.
