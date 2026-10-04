
# Mortgage Underwriting Assistant

A beginner-friendly multi-agent mortgage underwriting support prototype built with:

- **CrewAI** for the multi-agent system
- **Groq** with `openai/gpt-oss-120b`
- **Streamlit** for the web UI
- **FAISS** for local policy retrieval
- **Python** for deterministic financial calculations

## Important

This is a decision-support prototype. It does **not** approve or deny a mortgage. A qualified human underwriter must review the evidence, policy interpretation, calculations, and unresolved conditions.

## Five agents

1. **Document Review Agent** — extracts borrower facts, missing information, conflicts, and evidence.
2. **Policy Retrieval Agent** — retrieves relevant policy passages from the FAISS policy library.
3. **Calculation Review Agent** — uses deterministic Python calculations for income, obligations, DTI, and estimated closing funds.
4. **Assessment Agent** — combines the first three outputs into a proposed assessment and conditions.
5. **Validation Agent** — checks evidence, citations, calculations, policy support, and unresolved items.

## Project structure

```text
mortgage-underwriting-assistant/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── config/
│   ├── settings.py
│   └── llm.py
├── agents/
│   ├── document_review_agent.py
│   ├── policy_retrieval_agent.py
│   ├── calculation_review_agent.py
│   ├── assessment_agent.py
│   └── validation_agent.py
├── tasks/
│   ├── document_tasks.py
│   ├── policy_tasks.py
│   ├── calculation_tasks.py
│   ├── assessment_tasks.py
│   └── validation_tasks.py
├── crew/
│   └── underwriting_crew.py
├── tools/
│   ├── document_parser.py
│   ├── policy_search.py
│   └── financial_calculator.py
├── policy/
│   ├── policies.json
│   ├── policy.index
│   └── metadata.json
├── models/
│   └── schemas.py
├── reports/
│   └── report_generator.py
└── sample_documents/
```

## No local installation workflow

You said you do not want to install Python libraries on your laptop. You can use this workflow:

```text
Write/edit code with an AI assistant
        ↓
Create/update files in GitHub
        ↓
Push/commit to GitHub
        ↓
Connect repository to Streamlit Community Cloud
        ↓
Streamlit reads requirements.txt
        ↓
Cloud installs the dependencies
        ↓
Streamlit runs app.py
        ↓
Live web application
```

You still need a Groq API key, but you do not need to put it in GitHub.

## GitHub setup

Create a repository named:

```text
mortgage-underwriting-assistant
```

Upload the contents of this ZIP while preserving the folder structure.

Do **not** commit a Groq API key.

## Streamlit deployment

1. Open Streamlit Community Cloud.
2. Sign in with GitHub.
3. Create a new app.
4. Select your repository.
5. Select `app.py` as the entrypoint.
6. Choose Python 3.12.
7. Open Advanced settings / Secrets.
8. Add:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

9. Deploy.

The repository contains `requirements.txt`, so Streamlit can install the packages in the cloud.

## Policy library

`policy/policies.json` contains synthetic demonstration policies. They are intentionally not real lending guidelines.

For a real implementation, replace the demo policies with properly licensed, current policy material and preserve source metadata/page references.

When the app starts, `tools/policy_search.py` creates the FAISS index if `policy.index` is missing or invalid.

## Financial calculations

The Calculation Review Agent calls Python functions rather than asking the LLM to perform the arithmetic.

Supported calculations:

- gross monthly income
- total monthly obligations
- DTI
- loan-to-value (LTV)
- estimated closing funds

## First test

After deployment:

1. Open the app.
2. Leave **Use the built-in demo application** enabled.
3. Click **Analyze Application**.
4. Review the five agent outputs.
5. Download the Markdown report.

## Production improvements

Before using real borrower data, add:

- authentication and authorization
- encrypted storage
- audit logs
- stronger document classification
- real policy sources and licensing
- policy versioning
- structured JSON/Pydantic outputs
- human approval workflow
- PII redaction
- automated test suite
- observability and cost controls
- retention/deletion policies
- security review
