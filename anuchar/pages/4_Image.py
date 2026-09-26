import io
import streamlit as st
from core import database as db
from core import image_gen, config

st.set_page_config(page_title="Image - Anuchar", page_icon="🎨", layout="wide")

if not st.session_state.get("user_id"):
    st.warning("Pehle login karo.")
    st.stop()

user_id = st.session_state.user_id

st.markdown("## 🎨 AI Image Generator")

prompt = st.text_area("Prompt likho (jo image chahiye uska description)", height=100)
c1, c2, c3 = st.columns(3)
style = c1.selectbox("Style", config.IMAGE_STYLES)
size = c2.selectbox("Size", ["512x512", "768x768", "1024x1024"], index=2)
seed = c3.number_input("Seed (optional)", min_value=0, value=0, step=1)

w, h = map(int, size.split("x"))

if st.button("✨ Generate Karo", type="primary", use_container_width=True):
    if not prompt.strip():
        st.warning("Pehle prompt likho.")
    else:
        with st.spinner("Image bana raha hoon..."):
            try:
                img, full_prompt, url = image_gen.generate_image(prompt, style, w, h, seed)
                st.image(img, caption=full_prompt, use_container_width=True)

                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button(
                    "⬇️ Download PNG",
                    data=buf.getvalue(),
                    file_name="anuchar_image.png",
                    mime="image/png",
                )
                db.save_image(user_id, prompt, style)
            except Exception as e:
                st.error(f"Image generate nahi ho payi: {e}")

st.divider()
st.markdown("### 🖼️ Recent Prompts")
images = db.list_images(user_id)
if not images:
    st.info("Abhi tak koi image generate nahi ki.")
else:
    for _id, p, s, created in images[:10]:
        st.markdown(f"- **{p}** _(style: {s}, {created[:16]})_")
