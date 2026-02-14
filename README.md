# 🎵 Music Mashup Service
A web-based tool that automates searching, downloading, and stitching music tracks into a single mashup, delivered straight to your email.

# 🚀 Live Link
Try the App Here: https://mashup-service.streamlit.app/

<img width="1251" height="712" alt="image" src="https://github.com/user-attachments/assets/382bbedc-9ed4-4ddc-93c5-66244148f02f" />

# 🏗️ How it Works
The app follows a 4-step automated pipeline:

Search: Finds the artist using a custom search engine.

Download: Uses a "mobile-signature" bypass to avoid server blocks.

Process: Clips and joins audio using FFmpeg.

Deliver: Zips the result and sends it via SMTP.

# 🛡️ The "403 Forbidden" Solution
The biggest technical hurdle was being blocked by media servers. I solved this by mimicking an Android Player Client, which allows the cloud server to download audio without being flagged as a bot.
