import os

try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

DEFAULT_PROVIDER = "groq"

GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "gemma2-9b-it",
]

OLLAMA_MODELS = [
    "llama3.2",
    "phi3",
    "mistral",
    "gemma2:2b",
]

APP_NAME = "Anuchar"
VERSION = "3.0.0"

VOICE_LANGS = {
    "Hindi": ("hi-IN", "hi"),
    "English (India)": ("en-IN", "en"),
    "English (US)": ("en-US", "en"),
}

IMAGE_STYLES = [
    "Realistic", "Anime", "3D Render", "Cartoon",
    "Cyberpunk", "Watercolor", "Oil Painting", "Pixel Art",
]
