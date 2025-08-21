import base64
import os
import streamlit as st

# Logo path (update with your image path)
logo_path = os.path.join(os.path.dirname(__file__), '../assets', 'logo.png')

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = image_to_base64(logo_path)

def header():
    st.markdown(f"""
    <div class="header-container">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="header-logo">
        <h1>Trip Planner Chatbot</h1>
    </div>
    """, unsafe_allow_html=True)