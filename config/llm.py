
from crewai import LLM

from config.settings import CREWAI_MODEL_NAME, GROQ_API_KEY

if not GROQ_API_KEY:
    # CrewAI/LiteLLM can also read GROQ_API_KEY from the environment.
    # We keep this check in the app-facing layer so the error is clear.
    import os
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to Streamlit Secrets as "
        "GROQ_API_KEY = \"your-key\"."
    )

llm = LLM(
    model=CREWAI_MODEL_NAME,
    api_key=GROQ_API_KEY,
    temperature=0,
)
