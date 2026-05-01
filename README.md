# SustainAI Finance

Sustainability analytics platform for financial reports and transaction data.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run locally

```bash
python backend/app.py
```

Then open http://localhost:7860

## Docker

```bash
docker build -t sustainai-fin .
docker run -p 7860:7860 sustainai-fin
```

## Notes

- Upload CSV files for analysis
- Results include sustainability score, anomalies, and recommendations
- Requires OpenAI API key for LLM features (optional fallback available)
