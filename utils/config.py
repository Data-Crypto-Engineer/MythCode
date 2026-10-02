"""
Configuration and secrets loader for MythCode.
Extracts configuration safely from Streamlit Secrets or Environment Variables.
"""
import os
from typing import Dict, Any

def get_app_config() -> Dict[str, Any]:
    """
    Returns app configuration safely.
    Attempts to read from streamlit.secrets if available, then fallback to os.environ.
    """
    llm_provider = os.getenv("LLM_PROVIDER", "gemini")
    llm_model = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    api_key = os.getenv("GEMINI_API_KEY", os.getenv("LLM_API_KEY", ""))
    env = os.getenv("APP_ENV", "development")

    # Safely try streamlit secrets if streamlit is imported
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "llm" in st.secrets:
                llm_cfg = st.secrets["llm"]
                llm_provider = llm_cfg.get("provider", llm_provider)
                llm_model = llm_cfg.get("model", llm_model)
                api_key = llm_cfg.get("api_key", api_key)
            if "app" in st.secrets:
                app_cfg = st.secrets["app"]
                env = app_cfg.get("environment", env)
    except Exception:
        pass

    return {
        "llm_provider": llm_provider,
        "llm_model": llm_model,
        "has_api_key": bool(api_key and api_key != "YOUR_API_KEY_HERE"),
        "api_key": api_key if api_key != "YOUR_API_KEY_HERE" else "",
        "environment": env,
        "database_path": os.getenv("DATABASE_PATH", "mythcode_storage.db"),
    }
