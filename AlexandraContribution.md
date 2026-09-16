# Alexandra's Contribution

## Feature Engineering & Machine Learning

My main responsibility in **N3URONS TripPlanner** was preparing the processed travel dataset for machine learning and developing the models used to predict destination ratings.

The objective was to transform the collected location data into meaningful numerical features and build a supervised learning pipeline capable of estimating the expected rating of travel locations.

## Feature Engineering

I developed the feature engineering stage used to enrich the cleaned dataset before model training.

This included:

- encoding categorical information such as city, country, and attraction category;
- grouping individual attraction categories into broader travel themes:
  - Culture
  - Religion
  - Entertainment
  - Nature
  - Urban Space
  - Gastronomy
- encoding the newly created travel themes;
- creating a `price_per_review` feature;
- applying logarithmic transformations to highly skewed numerical variables;
- calculating the distance between each attraction and the center of its city;
- identifying locations situated near city centers;
- creating binary thematic indicators;
- calculating the number of categories associated with each attraction;
- extracting characteristics from attraction names such as:
  - name length;
  - word count;
- calculating theme popularity;
- calculating category density within each city;
- normalizing review counts relative to the average popularity of locations in the same city.

The resulting engineered dataset was saved as `dataset_fe.csv` and used as the input for the machine-learning stage.

## Data Preprocessing

Before model training, I prepared the dataset by separating the target variable from the predictive features.

The prediction target was:

```text
rating
```

The machine-learning pipeline included:

- an **80/20 train-test split**;
- feature scaling using `StandardScaler`;
- missing-value handling in the experimental pipeline;
- reproducible experiments using a fixed random state.

## Feature Selection

To reduce the number of unnecessary or weak features, I implemented model-based feature selection using:

```text
SelectFromModel
RandomForestRegressor
```

Feature importance obtained from the Random Forest model was used with a median threshold to retain the most relevant variables before training the regression models.

## Machine Learning Models

Instead of relying on a single algorithm, I trained and compared multiple regression approaches:

1. Ridge Regression
2. Lasso Regression
3. Elastic Net
4. Decision Tree Regressor
5. Random Forest Regressor
6. Gradient Boosting Regressor
7. Support Vector Regression
8. K-Nearest Neighbors Regressor
9. Multi-Layer Perceptron / Artificial Neural Network

This allowed us to compare several machine-learning approaches on the same dataset and determine which models were more suitable for travel-location rating prediction.

## Model Evaluation

Each trained model was evaluated on previously unseen test data using several regression metrics:

- **MAE — Mean Absolute Error**
- **MSE — Mean Squared Error**
- **RMSE — Root Mean Squared Error**
- **R² — Coefficient of Determination**

The models were then compared based primarily on their R² performance while also considering prediction error.

## Final Model

For the prediction pipeline integrated into TripPlanner, **Gradient Boosting Regression** was used as the final prediction model.

The application pipeline stores the trained artifacts required for inference:

```text
gradient_boosting_model.pkl
feature_selector.pkl
preprocessing_pipeline.pkl
```

These files allow the application to reproduce the same preprocessing and feature-selection stages when generating predictions.

The training routine used by the application can also remove the currently selected city/country/theme combination from the training dataset before producing its prediction, allowing the application to estimate ratings for data treated as unseen during that training operation.

## Main Files

My work is mainly represented by:

```text
datasets_w_scripts/
├── mapping.py
├── feature_engineering_final.py
├── feature_selection_train.py
└── dataset_fe.csv

app/scripts/
├── feature_selection_train.py
├── preprocessing_pipeline.pkl
├── feature_selector.pkl
├── gradient_boosting_model.pkl
└── model_performance.png
```

## Contribution to TripPlanner

My contribution represents the **machine-learning core of N3URONS TripPlanner**.

The feature-engineering and training pipeline transforms the collected travel information into a supervised regression problem and provides the predictive models required by the application to estimate destination ratings.
