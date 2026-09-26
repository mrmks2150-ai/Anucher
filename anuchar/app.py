import streamlit as st
from core import auth, config

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.username = None


def show_login():
    st.markdown(
        f"<h1 style='text-align:center;'>🤖 {config.APP_NAME}</h1>"
        "<p style='text-align:center;color:gray;'>Tumhara personal AI assistant</p>",
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        tab_login, tab_signup = st.tabs(["🔑 Login", "🆕 Signup"])

        with tab_login:
            with st.form("login_form"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)
                if submitted:
                    ok, result = auth.login(u, p)
                    if ok:
                        st.session_state.user_id = result
                        st.session_state.username = u.strip().lower()
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(result)

        with tab_signup:
            with st.form("signup_form"):
                u = st.text_input("Naya Username")
                p = st.text_input("Naya Password", type="password")
                p2 = st.text_input("Password confirm karo", type="password")
                submitted = st.form_submit_button("Account Banao", use_container_width=True)
                if submitted:
                    if p != p2:
                        st.error("Passwords match nahi kar rahe.")
                    else:
                        ok, msg = auth.signup(u, p)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)

    if not config.GROQ_API_KEY:
        st.warning(
            "⚠️ GROQ_API_KEY set nahi hai. `.streamlit/secrets.toml` me apni key daalo. "
            "Free key yahan se lo: https://console.groq.com/keys"
        )


def show_home():
    st.sidebar.success(f"👋 Namaste, **{st.session_state.username}**")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()

    st.markdown(f"# 🤖 Welcome to {config.APP_NAME}")
    st.markdown("Left sidebar se koi bhi feature choose karo 👇")

    c1, c2, c3, c4 = st.columns(4)
    c1.info("💬 **Chat**\n\nAI se baat karo")
    c2.info("🎙️ **Voice**\n\nBol ke poocho")
    c3.info("📄 **Documents**\n\nPDF padho & poocho")
    c4.info("🎨 **Image**\n\nAI se image banao")

    c5, c6, c7 = st.columns(3)
    c5.info("✅ **Tasks**\n\nApna to-do manage karo")
    c6.info("📊 **Analytics**\n\nApni activity dekho")
    c7.info("⚙️ **Settings**\n\nModel & preferences")

    st.caption(f"Anuchar v{config.VERSION}")


if st.session_state.user_id:
    show_home()
else:
    show_login()
