import os

import litellm
from crewai import LLM

from config.settings import CREWAI_MODEL_NAME, GROQ_API_KEY

# ---------------------------------------------------------------------------
# 1. API key (settings -> Streamlit secrets -> environment variable)
# ---------------------------------------------------------------------------
_api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")

if not _api_key:
    try:
        import streamlit as st
        _api_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        _api_key = ""

if not _api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to Streamlit Secrets as "
        'GROQ_API_KEY = "your-key".'
    )

# ---------------------------------------------------------------------------
# 2. Strip fields Groq does not support from every message
#    (CrewAI adds "cache" / "cache_breakpoint" / "cache_control" to messages)
# ---------------------------------------------------------------------------
_UNSUPPORTED_KEYS = {"cache", "cache_breakpoint", "cache_control"}


def _strip_keys(obj):
    if isinstance(obj, dict):
        return {k: _strip_keys(v) for k, v in obj.items() if k not in _UNSUPPORTED_KEYS}
    if isinstance(obj, list):
        return [_strip_keys(item) for item in obj]
    return obj


def _clean_messages(messages):
    cleaned = []
    for msg in messages or []:
        if isinstance(msg, dict):
            msg = _strip_keys(msg)
            content = msg.get("content")
            # Flatten text-only content blocks into a plain string for Groq
            if isinstance(content, list) and all(
                isinstance(p, dict) and p.get("type") == "text" for p in content
            ):
                msg["content"] = "\n".join(p.get("text", "") for p in content)
        cleaned.append(msg)
    return cleaned


if not getattr(litellm, "_groq_sanitizer_applied", False):
    _orig_completion = litellm.completion
    _orig_acompletion = litellm.acompletion

    def _safe_completion(*args, **kwargs):
        if "messages" in kwargs:
            kwargs["messages"] = _clean_messages(kwargs["messages"])
        return _orig_completion(*args, **kwargs)

    async def _safe_acompletion(*args, **kwargs):
        if "messages" in kwargs:
            kwargs["messages"] = _clean_messages(kwargs["messages"])
        return await _orig_acompletion(*args, **kwargs)

    litellm.completion = _safe_completion
    litellm.acompletion = _safe_acompletion
    litellm.drop_params = True
    litellm._groq_sanitizer_applied = True

# ---------------------------------------------------------------------------
# 3. The LLM used by all five agents (no cache=... argument here!)
# ---------------------------------------------------------------------------
llm = LLM(
    model=CREWAI_MODEL_NAME,   # e.g. "groq/llama-3.3-70b-versatile"
    api_key=_api_key,
    temperature=0,
)
