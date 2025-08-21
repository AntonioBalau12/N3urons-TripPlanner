import pandas as pd
from math import radians, cos, sin, sqrt, atan2, isclose

TOLERANCE = 0.0001
DISTANCE_THRESHOLD = 50

df_otm = pd.read_csv("opentrip_dataset_geo_clean.csv")
df_google = pd.read_csv("google_places_dataset_geo_clean.csv")

df_otm["rate"] = pd.to_numeric(df_otm["rate"], errors="coerce")
df_google["rating"] = pd.to_numeric(df_google["rating"], errors="coerce")
df_google["user_ratings_total"] = pd.to_numeric(df_google["user_ratings_total"], errors="coerce")

combined_data = []
for _, otm_row in df_otm.iterrows():
    lat_otm, lon_otm = otm_row["lat"], otm_row["lon"]
    matching_google = df_google[
        df_google["lat"].apply(lambda x: isclose(x, lat_otm, abs_tol=TOLERANCE)) &
        df_google["lon"].apply(lambda x: isclose(x, lon_otm, abs_tol=TOLERANCE))
    ]
    if not matching_google.empty:
        g_row = matching_google.iloc[0]
        combined_data.append({
            "name_otm": otm_row.get("name"),
            "kind": otm_row.get("kind"),
            "rate": otm_row.get("rate"),
            "description": otm_row.get("description"),
            "name_google": g_row.get("name"),
            "category": g_row.get("category"),
            "rating": g_row.get("rating"),
            "user_ratings_total": g_row.get("user_ratings_total"),
            "address": g_row.get("address"),
            "lat": lat_otm,
            "lon": lon_otm,
            "city": otm_row.get("city") or g_row.get("city"),
            "country": otm_row.get("country") or g_row.get("country"),
            "price_level": g_row.get("price_level")
        })

df = pd.DataFrame(combined_data)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = radians(lat1), radians(lat2)
    d_phi = radians(lat2 - lat1)
    d_lambda = radians(lon2 - lon1)
    a = sin(d_phi/2)**2 + cos(phi1)*cos(phi2)*sin(d_lambda/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

groups, visited = [], set()
for i, row in df.iterrows():
    if i in visited:
        continue
    group = [i]
    visited.add(i)
    lat1, lon1 = row["lat"], row["lon"]
    for j in range(i + 1, len(df)):
        if j in visited:
            continue
        lat2, lon2 = df.loc[j, "lat"], df.loc[j, "lon"]
        if haversine(lat1, lon1, lat2, lon2) <= DISTANCE_THRESHOLD:
            group.append(j)
            visited.add(j)
    groups.append(group)

final_data = []
for group in groups:
    gdf = df.loc[group]
    lat = gdf["lat"].mean()
    lon = gdf["lon"].mean()

    names = pd.concat([gdf["name_otm"], gdf["name_google"]]).dropna().unique()
    full_name = ", ".join(sorted(names))

    cities = gdf["city"].dropna().unique()
    city = cities[0] if len(cities) == 1 else ", ".join(sorted(cities))

    countries = gdf["country"].dropna().unique()
    country = countries[0] if len(countries) == 1 else ", ".join(sorted(countries))

    kinds = gdf["kind"].dropna().unique()
    kind = ", ".join(sorted(set(kinds))) if len(kinds) > 0 else None

    categories = gdf["category"].dropna().unique()
    category = ", ".join(sorted(set(categories))) if len(categories) > 0 else None

    rate_vals = pd.to_numeric(gdf["rate"], errors="coerce").dropna()
    rate = rate_vals.max() if not rate_vals.empty else None

    ratings = gdf[["rating", "user_ratings_total"]].copy()
    ratings["rating"] = pd.to_numeric(ratings["rating"], errors="coerce")
    ratings["user_ratings_total"] = pd.to_numeric(ratings["user_ratings_total"], errors="coerce")
    valid_ratings = ratings["rating"].dropna()
    weighted = ratings.dropna(subset=["rating", "user_ratings_total"])

    if not valid_ratings.empty:
        if not weighted.empty and weighted["user_ratings_total"].sum() > 0:
            rating = (weighted["rating"] * weighted["user_ratings_total"]).sum() / weighted["user_ratings_total"].sum()
        else:
            rating = valid_ratings.mean()
    else:
        rating = None

    reviews = pd.to_numeric(gdf["user_ratings_total"], errors="coerce").dropna().sum()
    price_levels = pd.to_numeric(gdf["price_level"], errors="coerce").dropna()
    price_level = round(price_levels.mean()) if not price_levels.empty else None

    final_data.append({
        "name": full_name,
        "lat": lat,
        "lon": lon,
        "rate": round(rate, 2) if rate is not None else None,
        "rating": round(rating, 2) if rating is not None else None,
        "user_ratings_total": int(reviews) if reviews > 0 else None,
        "kind": kind,
        "category": category,
        "city": city,
        "country": country,
        "price_level": price_level,
    })

df_final = pd.DataFrame(final_data)
df_final.to_csv("intersect_dataset_geo_clean.csv", index=False)
print(f"✅ Grupare completă: {len(df_final)} locații salvate în 'intersect_dataset_geo_clean.csv'")
