import streamlit as st
import pandas as pd
from app.predictor import generate_predictions


def location_rating_component(city, country, theme):
    # Generează predicții și salvează fișierul
    generate_predictions(city, country, theme)

    # Încarcă fișierul rezultat
    df = pd.read_csv("scripts/dataset_with_predictions.csv")

    # === 1. Rating pentru combinația city + theme ===
    filtered_df = df[(df['city'] == city) & (df['theme'] == theme)]

    if filtered_df.empty:
        st.warning("⚠️ Nu există predicții pentru acest oraș și această temă.")
        return

    location_theme_mean = filtered_df["predicted_rating"].mean()

    full_stars = int(round(location_theme_mean))
    empty_stars = 5 - full_stars
    stars = "⭐" * full_stars + "☆" * empty_stars
    st.markdown(f"### Rating estimat pentru locație: {stars} ({location_theme_mean:.2f})")
    st.caption(f"{len(filtered_df)} locații culturale analizate pentru această temă în {city}.")

    # === 2. Cel mai bun oraș pentru tema selectată ===
    best_city_for_theme = (
        df[df['theme'] == theme]
        .groupby('city')["predicted_rating"]
        .mean()
        .sort_values(ascending=False)
        .head(1)
    )

    if not best_city_for_theme.empty:
        best_city = best_city_for_theme.index[0]
        best_city_rating = best_city_for_theme.iloc[0]
        st.markdown(f"🏙️ **Cel mai bun oraș pentru tema _{theme}_:** `{best_city}` ({best_city_rating:.2f})")

    # === 3. Cea mai bună temă în orașul selectat ===
    best_theme_for_city = (
        df[df['city'] == city]
        .groupby('theme')["predicted_rating"]
        .mean()
        .sort_values(ascending=False)
        .head(1)
    )

    if not best_theme_for_city.empty:
        best_theme = best_theme_for_city.index[0]
        best_theme_rating = best_theme_for_city.iloc[0]
        st.markdown(f"🎭 **Cea mai bună temă în `{city}`:** _{best_theme}_ ({best_theme_rating:.2f})")
