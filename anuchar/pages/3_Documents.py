import os
import tempfile
import streamlit as st
from core import database as db
from core import pdf_reader, ai_service, export_utils

st.set_page_config(page_title="Documents - Anuchar", page_icon="📄", layout="wide")

if not st.session_state.get("user_id"):
    st.warning("Pehle login karo.")
    st.stop()

user_id = st.session_state.user_id
settings = db.get_settings(user_id)

st.markdown("## 📄 Documents")

uploaded = st.file_uploader("PDF upload karo", type=["pdf"])
if uploaded and st.button("📥 Process karo"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name
    with st.spinner("PDF padh raha hoon..."):
        text = pdf_reader.extract_text(tmp_path)
    os.unlink(tmp_path)

    if text:
        db.save_document(user_id, uploaded.name, text)
        st.success(f"'{uploaded.name}' process ho gaya! ({len(text)} characters)")
    else:
        st.error("Is PDF se text nahi nikal paya (shayad scanned image PDF hai).")

st.divider()
st.markdown("### 📂 Tumhare Documents")

docs = db.list_documents(user_id)
if not docs:
    st.info("Abhi tak koi document upload nahi kiya.")
else:
    doc_map = {f"{name} ({created[:10]})": doc_id for doc_id, name, created in docs}
    chosen_label = st.selectbox("Document choose karo", list(doc_map.keys()))
    doc_id = doc_map[chosen_label]
    name, content = db.get_document(doc_id)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "⬇️ Text (.txt)",
            data=export_utils.export_document_txt(name, content),
            file_name=f"{name}.txt",
            use_container_width=True,
        )
    with c2:
        if st.button("🗑️ Delete", use_container_width=True):
            db.delete_document(doc_id)
            st.rerun()
    with c3:
        with st.expander("👀 Preview"):
            st.text(content[:2000] + ("..." if len(content) > 2000 else ""))

    st.divider()
    st.markdown("### ❓ Is document se sawaal poocho")
    q = st.text_input("Sawaal likho")
    if q and st.button("Poocho"):
        with st.spinner("Dhundh raha hoon..."):
            relevant = pdf_reader.find_relevant(content, q)
            result = ai_service.chat_with_context(
                q, [], model=settings["model"], provider=settings["provider"],
                doc_context=relevant,
            )
        st.markdown(f"**🤖 Jawab:** {result['answer']}")
        if result.get("details"):
            with st.expander("📌 Related points"):
                for d in result["details"]:
                    st.markdown(f"- {d}")
