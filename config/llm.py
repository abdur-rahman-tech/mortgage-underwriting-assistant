import os
import streamlit as st
import litellm
from crewai import LLM

# 1. Disable LiteLLM caching via package settings
litellm.enable_cache = False
litellm.drop_params = True
os.environ["LITELLM_CACHE"] = "False"

# 2. Retrieve API Key
groq_api_key = st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None
if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY", "")

if not groq_api_key:
    raise RuntimeError("GROQ_API_KEY is missing from Streamlit Cloud Secrets.")

# 3. Instantiate LLM without passing cache=False directly
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0.0,
    # Pass cache settings as a dict if needed, or omit cache parameter entirely
    cache={"no-cache": True},
)
