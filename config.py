import os
from dotenv import load_dotenv

load_dotenv()

def _get(key):
    """Read from Streamlit secrets (cloud) or .env (local) transparently."""
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

GOOGLE_API_KEY = _get("GOOGLE_API_KEY")
EBAY_APP_ID    = _get("EBAY_APP_ID")
EBAY_CERT_ID   = _get("EBAY_CERT_ID")
DATASET        = "dataset.csv"
MODEL_PATH     = "price_model.pkl"