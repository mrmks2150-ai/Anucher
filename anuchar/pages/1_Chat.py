import uuid
import streamlit as st
from core import database as db
from core import ai_service, web_search, config

st.set_page_config(page_title="Chat - Anuchar", page_icon="💬", layout="wide")

if not st.session_state.get("user_id"):
    st.warning("Pehle login karo.")
    st.stop()

user_id = st.session_state.user_id
settings = db.get_settings(user_id)

# ---- Sidebar: sessions ----
with st.sidebar:
    st.markdown("### 💬 Chat Sessions")
    if st.button("➕ Naya Chat", use_container_width=True):
        st.session_state.current_session = str(uuid.uuid4())
        st.session_state.pop("messages", None)
        st.rerun()

    sessions = db.list_sessions(user_id)
    for sid, title, created in sessions:
        cols = st.columns([4, 1])
        if cols[0].button(f"🗂️ {title or 'New Chat'}", key=f"s_{sid}", use_container_width=True):
            st.session_state.current_session = sid
            st.session_state.messages = db.load_messages(sid)
            st.rerun()
        if cols[1].button("🗑️", key=f"d_{sid}"):
            db.delete_session(sid)
            st.rerun()

    st.divider()
    web_on = st.toggle("🌐 Web Search", value=settings["web_search"])
    if web_on != settings["web_search"]:
        db.update_settings(user_id, web_search=int(web_on))

if "current_session" not in st.session_state:
    st.session_state.current_session = str(uuid.uuid4())
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = db.load_messages(st.session_state.current_session)

st.markdown("## 💬 Chat")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

query = st.chat_input("Kuch bhi pucho...")

if query:
    sid = st.session_state.current_session
    db.create_session(sid, user_id, title=query[:40])

    st.session_state.messages.append({"role": "user", "content": query})
    db.save_message(sid, user_id, "user", query)
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            web_ctx = ""
            if settings["web_search"] and web_search.needs_web_search(query):
                results = web_search.search_web(query)
                web_ctx = web_search.format_results(results)

            result = ai_service.chat_with_context(
                query,
                st.session_state.messages,
                model=settings["model"],
                provider=settings["provider"],
                web_context=web_ctx or None,
            )

            st.markdown(result["answer"])

            if result.get("details"):
                with st.expander("📌 Related points"):
                    for d in result["details"]:
                        st.markdown(f"- {d}")

            if result.get("options"):
                st.markdown("**💡 Follow-up:**")
                cols = st.columns(len(result["options"]))
                for i, opt in enumerate(result["options"]):
                    cols[i].button(opt, key=f"opt_{i}_{len(st.session_state.messages)}")

    full_answer = result["answer"]
    st.session_state.messages.append({"role": "assistant", "content": full_answer})
    db.save_message(sid, user_id, "assistant", full_answer)
    db.update_session_title(sid, query[:40])
