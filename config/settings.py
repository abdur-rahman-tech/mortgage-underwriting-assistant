
import os

APP_TITLE = "Mortgage Underwriting Assistant"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# The prototype uses the CrewAI/LiteLLM provider prefix.
CREWAI_MODEL_NAME = os.getenv(
    "CREWAI_MODEL",
    f"groq/{MODEL_NAME}",
)

MAX_DOCUMENT_CHARS = int(os.getenv("MAX_DOCUMENT_CHARS", "60000"))
POLICY_TOP_K = int(os.getenv("POLICY_TOP_K", "5"))
