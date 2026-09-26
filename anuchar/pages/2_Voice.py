import streamlit as st
from core import database as db
from core import ai_service, voice, config

st.set_page_config(page_title="Voice - Anuchar", page_icon="🎙️", layout="wide")

if not st.session_state.get("user_id"):
    st.warning("Pehle login karo.")
    st.stop()

user_id = st.session_state.user_id
settings = db.get_settings(user_id)
lang_label = [k for k, v in config.VOICE_LANGS.items() if v[0] == settings["voice_lang"]]
lang_label = lang_label[0] if lang_label else "Hindi"

st.markdown("## 🎙️ Voice Assistant")
st.caption("Bolke poocho, Anuchar tumhe jawab bhi bolke dega.")

chosen = st.selectbox("Language", list(config.VOICE_LANGS.keys()), index=list(config.VOICE_LANGS.keys()).index(lang_label))
lang_code, tts_code = config.VOICE_LANGS[chosen]
if chosen != lang_label:
    db.update_settings(user_id, voice_lang=lang_code)

audio = st.audio_input("🎤 Record karo")

if audio is not None:
    with st.spinner("Sun raha hoon..."):
        text, err = voice.transcribe_audio(audio.getvalue(), language=tts_code)

    if err:
        st.error(err)
    elif text:
        st.success(f"**Tumne kaha:** {text}")

        with st.spinner("Soch raha hoon..."):
            result = ai_service.chat(text, [], model=settings["model"], provider=settings["provider"])

        st.markdown(f"**🤖 Anuchar:** {result['answer']}")

        if result.get("details"):
            with st.expander("📌 Related points"):
                for d in result["details"]:
                    st.markdown(f"- {d}")

        with st.spinner("Awaaz taiyar kar raha hoon..."):
            audio_bytes = voice.text_to_speech(result["answer"], lang=tts_code)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("Kuch samajh nahi aaya, dobara try karo.")
