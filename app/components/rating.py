import streamlit as st


def rating_component(title, current_rating=0, max_rating=5, key=None):
    """
    Componentă personalizată de rating

    Args:
        title (str): Titlul rating-ului
        current_rating (int): Ratingul curent (default 0)
        max_rating (int): Rating maxim (default 5)
        key (str): Cheia unica pentru session_state

    Returns:
        int: Ratingul selectat
    """
    # Folosim session_state pentru a reține ratingul
    if key not in st.session_state:
        st.session_state[key] = current_rating

    # Creăm HTML pentru rating
    stars_html = "".join(
        f'<span class="star" onclick="document.getElementById(\'{key}_value\').value = {i + 1}">{"★" if i < st.session_state[key] else "☆"}</span>'
        for i in range(max_rating)
    )

    # Afișăm componenta
    st.markdown(
        f"""
        <div class="rating-container">
            <h4>{title}</h4>
            <div class="rating-stars" id="{key}_stars">
                {stars_html}
            </div>
            <p class="rating-recommendation">
                {_get_recommendation(st.session_state[key])}
            </p>
        </div>
        <input type="hidden" id="{key}_value" value="{st.session_state[key]}">
        """,
        unsafe_allow_html=True
    )

    # JavaScript pentru a actualiza ratingul
    st.markdown(
        f"""
        <script>
            document.getElementById("{key}_stars").addEventListener("click", function() {{
                setTimeout(function() {{
                    const value = document.getElementById("{key}_value").value;
                    Streamlit.setComponentValue(parseInt(value));
                }}, 100);
            }});
        </script>
        """,
        unsafe_allow_html=True
    )

    return st.session_state[key]


def _get_recommendation(rating):
    """Returnează textul de recomandare în funcție de rating"""
    if rating > 4:
        return "Recomandare: Excelentă"
    elif rating > 3:
        return "Recomandare: Bună"
    else:
        return "Recomandare: Medie"