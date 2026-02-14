import streamlit as st
import os, smtplib, zipfile, importlib
from email.message import EmailMessage

mashup_logic = importlib.import_module("102317014")

st.set_page_config(page_title="Mashup Studio", page_icon="🎵")
st.title("🎵 Mashup Studio Pro")

with st.form("mashup_form"):
    singer = st.text_input("Singer Name")
    col1, col2 = st.columns(2)
    n = col1.slider("Videos", 11, 40, 11)
    y = col2.slider("Seconds", 21, 60, 25)
    email = st.text_input("Email ID")
    submit = st.form_submit_button("GENERATE MASHUP ✨")

if submit:
    if not singer or not email:
        st.error("Fields cannot be empty.")
    else:
        with st.spinner("Processing... (This takes 1-2 minutes)"):
            try:
                out_mp3 = "result.mp3"
                mashup_logic.run_mashup(singer, n, y, out_mp3)

                zip_name = "mashup.zip"
                with zipfile.ZipFile(zip_name, 'w') as z: z.write(out_mp3)

                msg = EmailMessage()
                msg['Subject'] = f'Mashup: {singer}'
                msg['From'] = 'imneerajsir@gmail.com'
                msg['To'] = email
                msg.set_content(f"Done! Created from {n} videos.")

                with open(zip_name, 'rb') as f:
                    msg.add_attachment(f.read(), maintype='application', subtype='zip', filename=zip_name)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login('imneerajsir@gmail.com', st.secrets["EMAIL_PASS"])
                    smtp.send_message(msg)

                st.balloons()
                st.success(f"Sent to {email}!")
                os.remove(out_mp3)
                os.remove(zip_name)
            except Exception as e:
                st.error(f"Error: {e}")
