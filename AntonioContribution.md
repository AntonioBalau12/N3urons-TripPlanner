# Antonio's Contribution

## Data Collection, Scraping & Data Cleaning

My main responsibility in **N3URONS TripPlanner** was building the data pipeline used to collect, combine, and clean the travel-location information required by the machine-learning system.

The goal was to create a sufficiently large and diverse dataset containing information about tourist attractions from multiple European cities.

## Data Collection

I developed the data-collection scripts used to retrieve information from two different travel and location data sources:

- **Google Places**
- **OpenTripMap**

Using multiple sources provided complementary information about each destination and allowed the final dataset to contain both popularity information and detailed location metadata.

## Google Places Data Collection

I developed a Python script that queries Google Places for attractions from multiple European cities.

The collection process searches numerous types of locations, including:

- monuments;
- museums;
- castles;
- palaces;
- churches;
- cathedrals;
- mosques;
- temples;
- theatres;
- concert halls;
- cinemas;
- parks;
- gardens;
- towers;
- fountains;
- railway stations;
- restaurants;
- and other tourist attractions.

For each location, information such as the following was collected:

```text
name
address
city
country
category
latitude
longitude
rating
number of user ratings
price level
```

Duplicate Google Places results were filtered using the unique `place_id` associated with each location.

Pagination was also handled so multiple pages of Google Places results could be collected.

## OpenTripMap Data Collection

A second extraction pipeline was implemented using the OpenTripMap API.

Locations were collected around the geographical coordinates of each supported city.

For each attraction, the dataset included information such as:

```text
name
kind
city
country
latitude
longitude
OpenTripMap rate
description
```

Individual place details were retrieved using each OpenTripMap `xid`.

The script also includes request pacing to reduce the risk of exceeding API limits.

## Cities Covered

The data pipeline was designed around a set of major European tourist destinations, including:

- Amsterdam
- Athens
- Barcelona
- Berlin
- Brussels
- Bucharest
- Budapest
- Copenhagen
- Dublin
- Istanbul
- Krakow
- Lisbon
- London
- Milan
- Munich
- Paris
- Prague
- Rome
- Vienna
- Warsaw
- Zurich

This provided geographically diverse data for the machine-learning stage.

## Dataset Cleaning and Integration

After collecting the two datasets, I developed the processing logic used to identify matching locations and combine their information.

The cleaning and integration process included:

- converting ratings and review counts into numerical values;
- identifying matching locations using geographical coordinates;
- combining Google Places and OpenTripMap information;
- detecting locations situated very close to each other;
- grouping locations located within approximately **50 meters**;
- removing redundant representations of the same attraction;
- combining alternative attraction names;
- merging attraction categories;
- combining location metadata;
- calculating representative coordinates for grouped locations;
- aggregating ratings;
- aggregating review counts;
- calculating representative price levels.

## Geospatial Duplicate Detection

To identify duplicate or near-duplicate attractions, I implemented geographical distance calculations using the **Haversine formula**.

Locations located within a defined distance threshold were grouped together.

This was especially useful because the same real-world attraction could appear differently across Google Places and OpenTripMap.

## Rating Aggregation

When multiple Google Places entries represented the same attraction, ratings were combined using the number of user reviews whenever possible.

This means locations with more user feedback contributed proportionally more to the aggregated rating instead of simply calculating an unweighted average.

## Resulting Dataset

The data pipeline produced the cleaned and merged dataset:

```text
intersect_dataset_geo_clean.csv
```

with fields such as:

```text
name
latitude
longitude
rate
rating
user_ratings_total
kind
category
city
country
price_level
```

This cleaned dataset became the foundation for the feature-engineering and machine-learning stages of TripPlanner.

## Main Files

My work is mainly represented by:

```text
datasets_w_scripts/
├── extract_google_places.py
├── extract_opentripmap.py
├── intersect.py
├── google_places_dataset_geo_clean.csv
├── opentrip_dataset_geo_clean.csv
└── intersect_dataset_geo_clean.csv
```

## Contribution to TripPlanner

My contribution represents the **data foundation of N3URONS TripPlanner**.

I developed the pipeline responsible for acquiring real-world travel data, cleaning and deduplicating it, integrating information from multiple sources, and generating the structured dataset later used for feature engineering and machine-learning training.
