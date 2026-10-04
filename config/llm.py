import os
import streamlit as st
import litellm
from crewai import LLM

# Disable LiteLLM's automatic prompt caching features
litellm.enable_cache = False
litellm.drop_params = True  # Automatically drop unsupported parameters for provider endpoints

# Fetch API key from Streamlit Secrets or Environment
groq_api_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None
if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY", "")

if not groq_api_key:
    raise RuntimeError("GROQ_API_KEY is missing from Streamlit Cloud Secrets.")

# Instantiate LLM with explicitly disabled caching
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0.0,
    cache=False  # Disables cache_breakpoint injection
)
