# 🤖 Anuchar

Personal AI Assistant — Streamlit web app. Chat, Voice, Documents (PDF Q&A), AI Image generation, Tasks, Analytics.

## 🚀 Local Setup

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# secrets.toml me apni GROQ_API_KEY daalo -> https://console.groq.com/keys
streamlit run app.py
```

## ☁️ Streamlit Cloud pe Deploy

1. Is poore folder ko GitHub repo me push karo (`secrets.toml` push mat karo — `.gitignore` me already excluded hai).
2. https://share.streamlit.io pe jao, apna GitHub repo connect karo, `app.py` ko main file select karo.
3. App settings me **Secrets** section me jaake yeh add karo:
   ```
   GROQ_API_KEY = "gsk_xxxxxxxxxxxx"
   ```
4. Deploy dabao — kuch minute me live URL mil jaayega.
5. Phone ke browser me URL kholo -> "Add to Home Screen" karo -> app jaisa icon mil jaayega.

## 📁 Structure

```
anuchar/
├── app.py                 # Login/Signup + home
├── requirements.txt
├── .streamlit/config.toml
├── core/                  # Business logic (AI, DB, auth, PDF, image, voice)
└── pages/                 # Multi-page app (Chat, Voice, Documents, Image, Tasks, Analytics, Settings)
```

## 🔑 Features

- 💬 Multi-session AI chat (Groq Llama models) with Hindi/Hinglish/English auto-detect
- 🎙️ Voice input (Groq Whisper) + voice output (gTTS)
- 📄 PDF upload & question-answering
- 🎨 Free AI image generation (Pollinations.ai, no key needed)
- ✅ Task manager with PDF export
- 📊 Usage analytics dashboard
- 🔐 Per-user login (SQLite + salted password hashing)
