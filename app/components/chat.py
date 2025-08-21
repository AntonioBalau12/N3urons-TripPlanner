# components/chat.py
import streamlit as st


def chat_component():
    """Reusable chat component that can be imported and used in the main app"""

    # Chat section
    st.markdown("<div class='stChat'><h3>💬 Chatbot</h3></div>", unsafe_allow_html=True)
    user_input = st.text_input("Write me a message")

    if user_input:
        response = f"Still learning!"
        st.text_area("Answer:", response, height=100)

    return user_input