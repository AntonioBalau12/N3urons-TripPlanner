import requests
import csv
import time

API_KEY = ("AIzaSyCWmrFAIgGxDdOWX090LSUijW-WPTPmqR4")

if not API_KEY:
    raise ValueError("⚠️ GOOGLE_API_KEY nu este definit!")

cities = [
    {'city': 'Amsterdam', 'country': 'NL'}, {'city': 'Athens', 'country': 'GR'}, {'city': 'Barcelona', 'country': 'ES'},
    {'city': 'Berlin', 'country': 'DE'}, {'city': 'Brussels', 'country': 'BE'},{'city': 'Bucharest', 'country': 'RO'},
    {'city': 'Budapest', 'country': 'HU'},{'city': 'Copenhagen', 'country': 'DK'},{'city': 'Dublin', 'country': 'IE'},
    {'city': 'Istanbul', 'country': 'TR'},{'city': 'Krakow', 'country': 'PL'}, {'city': 'Lisbon', 'country': 'PT'},
    {'city': 'London', 'country': 'GB'},{'city': 'Milan', 'country': 'IT'},{'city': 'Munich', 'country': 'DE'},
    {'city': 'Paris', 'country': 'FR'},{'city': 'Prague', 'country': 'CZ'},{'city': 'Rome', 'country': 'IT'},
    {'city': 'Vienna', 'country': 'AT'},{'city': 'Warsaw', 'country': 'PL'},{'city': 'Zurich', 'country': 'CH'},
]

categories = [
    "monuments", "sculptures","palaces","castles","landmark","museums","art gallery","churches",
    "cathedrals","monasteries","synagogues","mosques","temples","theatres","opera house","concert hall",
    "cinemas","parks","gardens","fortresses","towers","walls","gates","railway stations",
    "watchtowers","mausoleums","installations","public sculpture","fountains","restaurants"
]

def fetch_places(query):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'key': API_KEY
    }

    all_results = []
    seen = set()

    while url:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for result in data.get('results', []):
            place_id = result.get("place_id")
            if place_id in seen:
                continue  # evită duplicate
            seen.add(place_id)

            all_results.append({
                "name": result.get("name", ""),
                "address": result.get("formatted_address", ""),
                "lat": result.get("geometry", {}).get("location", {}).get("lat", ""),
                "lon": result.get("geometry", {}).get("location", {}).get("lng", ""),
                "rating": result.get("rating", ""),
                "user_ratings_total": result.get("user_ratings_total", ""),
                "price_level": result.get("price_level", "")
            })

        next_page_token = data.get("next_page_token")
        if next_page_token:
            time.sleep(2)
            params['pagetoken'] = next_page_token
        else:
            break

    return all_results

# 🔁 Colectăm din toate orașele și categorii
all_data = []
for city, info in cities.items():
    for category in categories:
        query = f"{category} in {info['base']}"
        print(f"\n📍 Extragem: {query}...")
        city_data = fetch_places(query)
        for item in city_data:
            item["city"] = city
            item["country"] = info["country"]
            item["category"] = category
        all_data.extend(city_data)

# 💾 Salvăm în CSV
output_file = "google_places_dataset_geo_clean.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        "name", "address", "city", "country", "category", "lat", "lon", "rating", "user_ratings_total","price_level"
    ])
    writer.writeheader()
    writer.writerows(all_data)

print(f"\n✅ Fișier salvat: {output_file} cu {len(all_data)} locații.")