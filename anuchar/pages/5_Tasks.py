import streamlit as st
from core import database as db
from core import export_utils

st.set_page_config(page_title="Tasks - Anuchar", page_icon="✅", layout="wide")

if not st.session_state.get("user_id"):
    st.warning("Pehle login karo.")
    st.stop()

user_id = st.session_state.user_id

st.markdown("## ✅ Tasks")

with st.form("add_task", clear_on_submit=True):
    c1, c2 = st.columns([4, 1])
    new_task = c1.text_input("Naya task", label_visibility="collapsed", placeholder="Naya task likho...")
    submitted = c2.form_submit_button("➕ Add", use_container_width=True)
    if submitted and new_task.strip():
        db.add_task(user_id, new_task.strip())
        st.rerun()

st.divider()

tasks = db.list_tasks(user_id)
if not tasks:
    st.info("Koi task nahi hai. Upar se add karo!")
else:
    for task_id, title, done in tasks:
        c1, c2, c3 = st.columns([0.5, 4, 0.5])
        checked = c1.checkbox("", value=bool(done), key=f"chk_{task_id}")
        if checked != bool(done):
            db.toggle_task(task_id)
            st.rerun()
        style = "text-decoration: line-through; color: gray;" if done else ""
        c2.markdown(f"<span style='{style}'>{title}</span>", unsafe_allow_html=True)
        if c3.button("🗑️", key=f"del_{task_id}"):
            db.delete_task(task_id)
            st.rerun()

    st.divider()
    done_count = sum(1 for _, _, d in tasks if d)
    st.progress(done_count / len(tasks) if tasks else 0)
    st.caption(f"{done_count}/{len(tasks)} tasks complete")

    st.download_button(
        "⬇️ Tasks PDF export karo",
        data=export_utils.export_tasks_pdf(tasks),
        file_name="anuchar_tasks.pdf",
        mime="application/pdf",
    )
