import streamlit as st


def custom_dropdown(options, label="Select an option", key=None):
    """
    Componentă personalizată de dropdown

    Args:
        options (list): Lista de opțiuni
        label (str): Eticheta pentru dropdown
        key (str): Cheia unica pentru session_state

    Returns:
        str: Opțiunea selectată
    """
    # Folosim un container pentru a aplica stilurile noastre
    with st.container():
        st.markdown(f'<label style="color: var(--text-color); display: block;">{label}</label>',
                    unsafe_allow_html=True)
        st.markdown(f'<div class="custom-dropdown">', unsafe_allow_html=True)
        selected = st.selectbox(
            label,
            options,
            key=key,
            label_visibility="collapsed"  # Ascundem eticheta default
        )


    return selected