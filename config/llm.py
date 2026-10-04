
# from crewai import LLM

# from config.settings import CREWAI_MODEL_NAME, GROQ_API_KEY

# if not GROQ_API_KEY:
#     # CrewAI/LiteLLM can also read GROQ_API_KEY from the environment.
#     # We keep this check in the app-facing layer so the error is clear.
#     import os
#     GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# if not GROQ_API_KEY:
#     raise RuntimeError(
#         "GROQ_API_KEY is missing. Add it to Streamlit Secrets as "
#         "GROQ_API_KEY = \"your-key\"."
#     )

# llm = LLM(
#     model=CREWAI_MODEL_NAME,
#     api_key=GROQ_API_KEY,
#     temperature=0,
# )
import os
import streamlit as st
from crewai import LLM

# Try loading from Streamlit Secrets first, then fall back to environment variables
groq_api_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None

if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY", "")

if not groq_api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Please add GROQ_API_KEY to your Streamlit Cloud Secrets."
    )

# Instantiate CrewAI LLM configured for Groq
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0.0,
)
