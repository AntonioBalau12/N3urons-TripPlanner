import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
import joblib

def train_model(city, country, theme):
    os.makedirs("scripts", exist_ok=True)

    # === 1. Încarcă datele ===
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folderul unde e scriptul actual
    csv_path = os.path.join(BASE_DIR, "dataset_fe.csv")
    df = pd.read_csv(csv_path)

    # === 2. Elimină rândurile din orașul, țara și tema specificată ===
    df_filtered = df[~((df['city'] == city) & (df['country'] == country) & (df['theme'] == theme))]

    # === 3. Setează target și elimină coloane nerelevante ===
    target = "rating"
    exclude = ['name', 'kind', 'category', 'city', 'country', 'theme', 'category_main', 'rate', 'rating']
    features = [col for col in df.columns if col not in exclude]

    X = df_filtered[features]
    y = df_filtered[target]

    # === 4. Împărțire train/test ===
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # === 5. Pipeline preprocesare ===
    preprocessing = Pipeline([
        ('scaler', StandardScaler()),
    ])

    X_train_processed = preprocessing.fit_transform(X_train)
    X_test_processed = preprocessing.transform(X_test)

    # === 6. Feature Selection ===
    selector = SelectFromModel(RandomForestRegressor(random_state=42), threshold="median")
    X_train_selected = selector.fit_transform(X_train_processed, y_train)
    X_test_selected = selector.transform(X_test_processed)

    # === 7. Modele + antrenare ===
    models = {
        'Ridge': Ridge(),
        'Lasso': Lasso(),
        'ElasticNet': ElasticNet(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42),
        'SVR': SVR(),
        'KNN': KNeighborsRegressor(),
        'ANN (MLP)': MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
    }

    results = []
    for name, model in models.items():
        model.fit(X_train_selected, y_train)
        y_pred = model.predict(X_test_selected)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        results.append({
            'Model': name,
            'MAE': round(mae, 4),
            'MSE': round(mse, 4),
            'RMSE': round(rmse, 4),
            'R²': round(r2, 4)
        })

    results_df = pd.DataFrame(results).sort_values(by="R²", ascending=False).reset_index(drop=True)
    print("\n📊 Rezultate antrenare:")
    print(results_df.to_string(index=False))

    # === 8. Pregătire pentru predicții finale pe întregul dataset ===
    X_full = df[features]
    X_full_processed = preprocessing.transform(X_full)
    X_full_selected = selector.transform(X_full_processed)

    final_model = GradientBoostingRegressor(random_state=42)
    final_model.fit(X_train_selected, y_train)
    df['predicted_rating'] = np.round(final_model.predict(X_full_selected), 1)

    # === 9. Salvare finală ===
    df.to_csv("scripts/dataset_with_predictions.csv", index=False)
    joblib.dump(final_model, "scripts/gradient_boosting_model.pkl")
    joblib.dump(selector, "scripts/feature_selector.pkl")
    joblib.dump(preprocessing, "scripts/preprocessing_pipeline.pkl")

    print("✅ Modelul a fost salvat. Fișierul cu predicții a fost generat în 'scripts/dataset_with_predictions.csv'.")


    return final_model, selector, results_df

# Exemplu de rulare directă
if __name__ == "__main__":
    train_model("Paris", "France", "historic")
