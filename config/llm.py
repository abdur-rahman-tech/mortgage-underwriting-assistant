import os
import streamlit as st
from crewai import LLM

# Load GROQ_API_KEY from Streamlit Secrets or Environment
groq_api_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None

if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY", "")

if not groq_api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Please add GROQ_API_KEY to Streamlit Cloud Secrets."
    )

# Disable prompt caching to satisfy Groq's API constraints
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0.0,
    cache=False,  # Explicitly disable CrewAI prompt caching for Groq compatibility
)
