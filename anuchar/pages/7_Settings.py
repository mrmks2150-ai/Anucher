import streamlit as st
from core import database as db
from core import config

st.set_page_config(page_title="Settings - Anuchar", page_icon="⚙️", layout="wide")

if not st.session_state.get("user_id"):
    st.warning("Pehle login karo.")
    st.stop()

user_id = st.session_state.user_id
settings = db.get_settings(user_id)

st.markdown("## ⚙️ Settings")

st.markdown("### 🧠 AI Model")
provider = st.radio("Provider", ["groq", "ollama"], index=0 if settings["provider"] == "groq" else 1, horizontal=True)
model_list = config.GROQ_MODELS if provider == "groq" else config.OLLAMA_MODELS
current_model = settings["model"] if settings["model"] in model_list else model_list[0]
model = st.selectbox("Model", model_list, index=model_list.index(current_model))

st.markdown("### 🎙️ Voice")
lang_label = [k for k, v in config.VOICE_LANGS.items() if v[0] == settings["voice_lang"]]
lang_label = lang_label[0] if lang_label else "Hindi"
voice_lang_choice = st.selectbox("Voice Language", list(config.VOICE_LANGS.keys()), index=list(config.VOICE_LANGS.keys()).index(lang_label))
auto_speak = st.toggle("Answers auto-speak karo", value=settings["auto_speak"])

st.markdown("### 🌐 Web Search")
web_search_on = st.toggle("Web search allow karo", value=settings["web_search"])

if st.button("💾 Save Settings", type="primary", use_container_width=True):
    db.update_settings(
        user_id,
        provider=provider,
        model=model,
        voice_lang=config.VOICE_LANGS[voice_lang_choice][0],
        auto_speak=int(auto_speak),
        web_search=int(web_search_on),
    )
    st.success("Settings save ho gayi!")

st.divider()
st.markdown("### ℹ️ About")
st.caption(f"{config.APP_NAME} v{config.VERSION}")
if not config.GROQ_API_KEY:
    st.warning("⚠️ GROQ_API_KEY set nahi hai. `.streamlit/secrets.toml` me daalo.")

if st.button("🚪 Logout"):
    st.session_state.user_id = None
    st.session_state.username = None
    st.rerun()
