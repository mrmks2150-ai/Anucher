import requests
import io
from . import config


def transcribe_audio(audio_bytes, language="hi"):
    if not config.GROQ_API_KEY:
        return None, "GROQ_API_KEY nahi mili."

    files = {
        "file": ("audio.wav", audio_bytes, "audio/wav"),
    }
    data = {
        "model": "whisper-large-v3",
        "language": language,
        "response_format": "json",
    }
    headers = {"Authorization": f"Bearer {config.GROQ_API_KEY}"}

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers=headers,
            files=files,
            data=data,
            timeout=60,
        )
        if r.status_code == 200:
            return r.json().get("text", "").strip(), None
        return None, f"Whisper error {r.status_code}: {r.text[:150]}"
    except Exception as e:
        return None, f"Error: {e}"


def text_to_speech(text, lang="hi"):
    try:
        from gtts import gTTS
        tts = gTTS(text=text[:500], lang=lang, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None
