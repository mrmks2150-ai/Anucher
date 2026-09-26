import pandas as pd
import plotly.express as px
import streamlit as st
from core import database as db

st.set_page_config(page_title="Analytics - Anuchar", page_icon="📊", layout="wide")

if not st.session_state.get("user_id"):
    st.warning("Pehle login karo.")
    st.stop()

user_id = st.session_state.user_id
stats = db.get_stats(user_id)

st.markdown("## 📊 Analytics")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💬 Sessions", stats["sessions"])
c2.metric("✉️ Messages", stats["messages"])
c3.metric("📄 Documents", stats["documents"])
c4.metric("🎨 Images", stats["images"])
c5.metric("✅ Tasks", stats["tasks"])

st.divider()

if stats["daily"]:
    df = pd.DataFrame(stats["daily"], columns=["Date", "Messages"])
    fig = px.bar(df, x="Date", y="Messages", title="Last 7 Days — Chat Activity")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Abhi tak koi chat activity nahi hai.")

st.divider()
st.markdown("### 📈 Usage Breakdown")
breakdown = pd.DataFrame({
    "Feature": ["Sessions", "Messages", "Documents", "Images", "Tasks"],
    "Count": [stats["sessions"], stats["messages"], stats["documents"], stats["images"], stats["tasks"]],
})
fig2 = px.pie(breakdown, names="Feature", values="Count", title="Overall Usage")
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)
