import streamlit as st
import os
import smtplib
import zipfile
import importlib
from email.message import EmailMessage
mashup_logic = importlib.import_module("102317014")

st.set_page_config(page_title="Mashup Studio Pro", page_icon="🎵")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #1e1b4b, #0f172a); color: white; }
    .stTextInput>div>div>input { background: rgba(255,255,255,0.05)!important; color: white!important; border-radius: 10px!important; }
    .stButton>button { background: linear-gradient(135deg, #6366f1, #a855f7)!important; color: white!important; border-radius: 12px!important; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 Mashup Studio Pro")
st.write("Professional Video-to-Audio Blending Service")

with st.form("mashup_form"):
    singer = st.text_input("Singer Name", placeholder="e.g., Karan Aujla")
    col1, col2 = st.columns(2)
    with col1:
        n = st.slider("Number of Videos", 11, 40, 11)
    with col2:
        y = st.slider("Duration (sec)", 21, 60, 25)
    email = st.text_input("Email ID", placeholder="artist@studio.com")
    submit_button = st.form_submit_button("GENERATE MASHUP ✨")

if submit_button:
    if not singer or not email:
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Processing... This takes about a minute."):
            try:
                output_mp3 = "mashup_result.mp3"
                mashup_logic.run_mashup(singer, n, y, output_mp3)

                zip_name = "mashup.zip"
                with zipfile.ZipFile(zip_name, 'w') as zipf:
                    zipf.write(output_mp3)

                msg = EmailMessage()
                msg['Subject'] = f'Your Mashup for {singer}'
                msg['From'] = 'imneerajsir@gmail.com'
                msg['To'] = email
                msg.set_content(f"Here is your mashup for {singer} ({n} tracks, {y}s each).")

                with open(zip_name, 'rb') as f:
                    msg.add_attachment(f.read(), maintype='application', subtype='zip', filename=zip_name)

                app_pass = st.secrets["EMAIL_PASS"]
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login('imneerajsir@gmail.com', app_pass)
                    smtp.send_message(msg)

                st.balloons()
                st.success(f"Successfully sent to {email}!")

                if os.path.exists(output_mp3): os.remove(output_mp3)
                if os.path.exists(zip_name): os.remove(zip_name)

            except Exception as e:
                st.error(f"Error: {e}")