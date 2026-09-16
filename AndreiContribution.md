# Andrei's Contribution

## Application Development, User Interface & Model Integration

My main responsibility in **N3URONS TripPlanner** was developing the application layer around the machine-learning system and integrating the prediction pipeline into an interactive interface.

The objective was to transform the data-processing and machine-learning components into a usable travel recommendation application where users could select destinations and travel preferences, obtain predicted ratings, and visualize locations on a map.

## Application Interface

The TripPlanner interface was developed using **Streamlit**.

I implemented the main application structure and connected the different UI components required by the user workflow.

The interface allows users to select a destination from the supported European cities and then choose the type of travel experience they are interested in.

Available themes include:

- Culture
- Religion
- Entertainment
- Nature
- Urban Space
- Gastronomy

These selections are passed to the prediction system to generate personalized rating information.

## Modular UI Components

The application was structured using reusable Streamlit components instead of placing the complete interface inside a single file.

Components include:

```text
components/
├── dropdown.py
├── header.py
├── map.py
├── predictor_locations.py
├── rating.py
└── styles.py
```

This separates presentation, prediction results, maps, navigation elements, and styling into independent modules.

## Prediction Integration

I integrated the trained machine-learning system with the application.

The prediction layer loads:

```text
dataset_fe.csv
preprocessing_pipeline.pkl
feature_selector.pkl
gradient_boosting_model.pkl
```

and connects them with the interface.

When the user selects a city and travel theme, the application:

1. triggers the prediction workflow;
2. applies the same preprocessing used during training;
3. applies the trained feature selector;
4. generates predicted ratings;
5. stores the generated predictions;
6. filters the results according to the selected city and theme;
7. presents the resulting rating to the user.

## Travel Recommendation Output

The interface calculates the average predicted rating for locations matching the user's selected city and theme.

The result is presented using both:

- a numerical rating;
- a visual star-based rating.

The application can additionally analyze the generated predictions to determine:

- the city with the highest predicted average rating for the selected theme;
- the theme with the highest predicted average rating for the selected city.

This turns the underlying regression model into information that can be directly understood by the user.

## Google Maps Integration

I integrated **Google Maps** into the TripPlanner interface.

The map component:

- retrieves the selected location;
- geocodes the city using Google Maps;
- centers the map on the selected destination;
- displays a custom location marker;
- applies custom map styling consistent with the application's interface.

This allows the predicted travel information and geographical information to be displayed side by side.

## Application Styling

I also worked on the visual presentation of the application.

The interface includes:

- reusable styling definitions;
- Streamlit theme integration;
- responsive layout elements;
- custom dropdown components;
- a two-column result layout;
- custom map presentation;
- branded visual elements.

The prediction result and destination map are presented together to make the recommendation workflow easier to understand.

## Application Architecture

The relevant part of the project is structured approximately as:

```text
app/
├── interfata.py
├── predictor.py
│
├── components/
│   ├── dropdown.py
│   ├── header.py
│   ├── map.py
│   ├── predictor_locations.py
│   ├── rating.py
│   └── styles.py
│
└── scripts/
    ├── dataset_fe.csv
    ├── dataset_with_predictions.csv
    ├── feature_selection_train.py
    ├── feature_selector.pkl
    ├── gradient_boosting_model.pkl
    └── preprocessing_pipeline.pkl
```

## Contribution to TripPlanner

My contribution represents the **application and integration layer of N3URONS TripPlanner**.

I connected the machine-learning pipeline with an interactive Streamlit interface, implemented the destination and theme selection workflow, integrated rating predictions into the user experience, and added Google Maps visualization so the machine-learning results could be used through a complete travel recommendation application.
