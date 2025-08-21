import streamlit as st
import os, sys
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from components.dropdown import custom_dropdown
from components.header import header
from components.map import show_custom_map
from components.styles import get_styles
from components.predictor_locations import location_rating_component
from components.rating import rating_component


colors = {
    "primary": st.get_option("theme.primaryColor"),
    "background": st.get_option("theme.backgroundColor"),
    "secondary": st.get_option("theme.secondaryBackgroundColor"),
    "text": st.get_option("theme.textColor"),
    "font": st.get_option("theme.font"),
    "accent": "#fb6f92",
    "medium": "#ffb3c6"
}

st.set_page_config(
    page_title="Trip Chatbot",
    layout="wide",
    page_icon="🗺️",
    initial_sidebar_state="expanded"
)

# Responsive CSS with media queries

st.markdown(get_styles(colors), unsafe_allow_html=True)


# Call header component
header()

# Call the chat component

#chat_component()

#Nou component dropdown
# În altă parte a aplicației
countries = ['Amsterdam, NL', 'Athens, GR', 'Barcelona, ES', 'Berlin, DE', 'Brussels, BE',
 'Bucharest, RO', 'Budapest, HU', 'Copenhagen, DK', 'Dublin, IE', 'Istanbul, TR',
 'Krakow, PL', 'Lisbon, PT', 'London, GB', 'Milan, IT', 'Munich, DE',
 'Paris, FR', 'Prague, CZ', 'Rome, IT', 'Vienna, AT', 'Warsaw, PL', 'Zurich, CH']
selected_country = custom_dropdown(
    options=countries,
    label="Select a country",
    key="country_dropdown"
)

if selected_country:
    # Input pentru locație
    categories=['Culture', 'Religion', 'Entertainment', 'Nature', 'Urban space', 'Gastronomy']
    city,country=selected_country.split(',')
    selected_category=custom_dropdown(
        label="Select a theme",
        options=categories,
        key="category_dropdown"
    )
    if selected_category:
        col1,col2=st.columns(2)
        with col1:
        # Componenta de rating interactivă
            if(selected_category=="Urban space"):
                selected_category="Urban_space"
            location_rating_component(city, country, selected_category.lower())

        with col2:
            show_custom_map(selected_country)  # This will use the styled map

# # Toggle button to show/hide graphs
# if 'show_graphs' not in st.session_state:
#     st.session_state.show_graphs = False
#
# toggle_button = st.button("Show Graphs 🗺️", key="toggle_button")
# if toggle_button:
#     st.session_state.show_graphs = not st.session_state.show_graphs
#
# # Display graphs if toggle is True
# if st.session_state.show_graphs:
#     display_graphs()