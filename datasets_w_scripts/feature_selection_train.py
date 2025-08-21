import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor

# === 1. Încarcă datele ===
df = pd.read_csv("dataset_fe.csv")

# === 2. Definește target și elimină coloane irelevante ===
target = "rating"
exclude = ['name', 'kind', 'category', 'city', 'country', 'theme', 'category_main', 'rate', 'rating']
features = [col for col in df.columns if col not in exclude]

X = df[features]
y = df[target]

# === 3. Împărțire train/test ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 4. Pipeline preprocesare + feature selection ===
preprocessing = Pipeline([
    ('scaler', StandardScaler()),
    ('imputer', SimpleImputer()),
])

X_train_processed = preprocessing.fit_transform(X_train)
X_test_processed = preprocessing.transform(X_test)

# === 5. Feature Selection cu Random Forest ===
selector = SelectFromModel(RandomForestRegressor(random_state=42), threshold="median")
X_train_selected = selector.fit_transform(X_train_processed, y_train)
X_test_selected = selector.transform(X_test_processed)

# === 6. Modele pentru antrenare ===
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

# === 7. Antrenare + evaluare ===
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

# === 8. Afișare rezultate finale ===
results_df = pd.DataFrame(results).sort_values(by="R²", ascending=False).reset_index(drop=True)
print("\n📊 Rezultate cu Feature Selection (median threshold):")
print(results_df.to_string(index=False))