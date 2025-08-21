import os
import numpy as np
from pathlib import Path
import pandas as pd
import joblib

APP_DIR = Path(__file__).resolve().parent          # ...\N3urons TripPlanner\app
SCRIPTS_DIR = APP_DIR / "scripts"                  # ...\N3urons TripPlanner\app\scripts

CSV_PATH = SCRIPTS_DIR / "dataset_fe.csv"
PREP_PATH = SCRIPTS_DIR / "preprocessing_pipeline.pkl"
MODEL_PATH = SCRIPTS_DIR / "gradient_boosting_model.pkl"   # schimbă dacă ai alt nume
SELECTOR_PATH = SCRIPTS_DIR / "feature_selector.pkl"

# --- DEBUG ca să vezi clar de unde citește (poți lăsa temporar) ---
print("[predictor] APP_DIR     =", APP_DIR)
print("[predictor] SCRIPTS_DIR =", SCRIPTS_DIR)
print("[predictor] CSV exists? =", CSV_PATH.exists())

# Assert explicit (dacă pică, îți arată exact calea căutată)
if not CSV_PATH.exists():
    raise FileNotFoundError(f"Nu găsesc dataset_fe.csv la: {CSV_PATH}")

# Încarcă datele și artefactele
df = pd.read_csv(CSV_PATH)
preprocessing = joblib.load(PREP_PATH)
model = joblib.load(MODEL_PATH)
selector = joblib.load(SELECTOR_PATH)

def generate_predictions(city, country, theme):
    from scripts.feature_selection_train import train_model

    # Antrenează modelul și obține și preprocessing + selector
    model, selector, _ = train_model(city, country, theme)

    # Încarcă și pipeline-ul de preprocesare salvat
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folderul curent (app/)
    scripts_dir = os.path.join(BASE_DIR, "scripts")
    pkl_path = os.path.join(scripts_dir, "preprocessing_pipeline.pkl")

    preprocessing = joblib.load(pkl_path)

    # Încarcă datasetul complet original
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folderul unde e scriptul actual
    csv_path = os.path.join(BASE_DIR, "scripts/dataset_fe.csv")
    df = pd.read_csv(csv_path)

    # Elimină aceleași coloane ca la antrenare
    drop_cols = ['name', 'kind', 'category', 'city', 'country', 'theme', 'category_main', 'rate', 'rating']
    features = [col for col in df.columns if col not in drop_cols]
    X = df[features]

    # 1️⃣ Aplică preprocessing (imputer + scaler)
    X_processed = preprocessing.transform(X)

    # 2️⃣ Aplică feature selectorul deja antrenat
    X_selected = selector.transform(X_processed)

    # 3️⃣ Predict și salvare
    df['predicted_rating'] = np.round(model.predict(X_selected), 1)

    df.to_csv("scripts/dataset_with_predictions.csv", index=False)
    print("✅ Predicțiile au fost salvate în 'scripts/dataset_with_predictions.csv'.")
