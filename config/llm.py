import os
import streamlit as st
import litellm
from crewai import LLM

# 1. Disable prompt caching globally in LiteLLM
litellm.enable_cache = False
litellm.drop_params = True  # Automatically drop unsupported params (like cache_breakpoint) for providers that don't support them
os.environ["LITELLM_CACHE"] = "False"

# 2. Get API Key from Streamlit secrets or env vars
groq_api_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None
if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY", "")

if not groq_api_key:
    raise RuntimeError("GROQ_API_KEY is missing from Streamlit Cloud Secrets or environment variables.")

# 3. Instantiate LLM with explicit LiteLLM parameters
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0.0,
    # Set cache to False via extra_body or omit cache attributes completely
    extra_body={"cache": {"no-cache": True}},
)
