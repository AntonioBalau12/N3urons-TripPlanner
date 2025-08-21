import requests
import csv
import time

API_KEY = ("5ae2e3f221c38a28845f05b6df6acfa1dac8c96da293483ebd590c11")
print(f"🔑 API Key loaded: {API_KEY[:4]}...")  # doar primele caractere

# Orașe de interes + coordonate
cities = {
    "Amsterdam":  {"lat": 52.3676, "lon": 4.9041,   "country": "NL"}, "Athens":     {"lat": 37.9838, "lon": 23.7275,  "country": "GR"},
    "Barcelona":  {"lat": 41.3851, "lon": 2.1734,   "country": "ES"}, "Berlin":     {"lat": 52.5200, "lon": 13.4050,  "country": "DE"},
    "Brussels":   {"lat": 50.8503, "lon": 4.3517,   "country": "BE"}, "Bucharest":  {"lat": 44.4268, "lon": 26.1025,  "country": "RO"},
    "Budapest":   {"lat": 47.4979, "lon": 19.0402,  "country": "HU"}, "Copenhagen": {"lat": 55.6761, "lon": 12.5683,  "country": "DK"},
    "Dublin":     {"lat": 53.3498, "lon": -6.2603,  "country": "IE"}, "Istanbul":   {"lat": 41.0082, "lon": 28.9784,  "country": "TR"},
    "Krakow":     {"lat": 50.0647, "lon": 19.9450,  "country": "PL"}, "Lisbon":     {"lat": 38.7169, "lon": -9.1399,  "country": "PT"},
    "London":     {"lat": 51.5074, "lon": -0.1278,  "country": "GB"}, "Milan":      {"lat": 45.4642, "lon": 9.1900,   "country": "IT"},
    "Munich":     {"lat": 48.1351, "lon": 11.5820,  "country": "DE"}, "Paris":      {"lat": 48.8566, "lon": 2.3522,   "country": "FR"},
    "Prague":     {"lat": 50.0755, "lon": 14.4378,  "country": "CZ"}, "Rome":       {"lat": 41.9028, "lon": 12.4964,  "country": "IT"},
    "Vienna":     {"lat": 48.2082, "lon": 16.3738,  "country": "AT"}, "Warsaw":     {"lat": 52.2297, "lon": 21.0122,  "country": "PL"},
    "Zurich":     {"lat": 47.3769, "lon": 8.5417,   "country": "CH"},
}


def get_places(city_name, lat, lon, country_code, max_places=1000):
    print(f"\n📍 Extragem locații din {city_name}...")
    url = 'https://api.opentripmap.com/0.1/en/places/radius'
    params = {
        'radius': 10000,
        'lon': lon,
        'lat': lat,
        'limit': max_places,
        'apikey': API_KEY,
        'rate': 2  # doar locații populare
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Eroare la interogarea principală: {e}")
        return []

    places = response.json().get('features', [])
    results = []

    for idx, place in enumerate(places):
        xid = place['properties']['xid']
        details_url = f'https://api.opentripmap.com/0.1/en/places/xid/{xid}'

        try:
            details = requests.get(details_url, params={'apikey': API_KEY}).json()
            results.append({
                'name': details.get('name', ''),
                'kind': details.get('kinds', 'unknown'),
                'city': city_name,
                'country': country_code,
                'lat': details.get('point', {}).get('lat'),
                'lon': details.get('point', {}).get('lon'),
                'rate': details.get('rate', ''),
                'description': details.get('info', {}).get('descr', '')
            })
        except Exception as e:
            print(f"⚠️ Eroare la detalii pentru {xid}: {e}")

        time.sleep(0.2)  # evită blocarea API-ului

        if idx % 50 == 0:
            print(f"  → {idx} locații procesate...")

    return results

# Colectăm date din fiecare oraș
all_data = []
for city, info in cities.items():
    city_data = get_places(city, info['lat'], info['lon'], info['country'], max_places=1000)
    all_data.extend(city_data)

# Salvăm în CSV
output_file = "opentrip_dataset_geo_clean.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'name', 'kind', 'city', 'country', 'lat', 'lon', 'rate', 'description'
    ])
    writer.writeheader()
    writer.writerows(all_data)

print(f"\n✅ Fișier salvat: {output_file} cu {len(all_data)} locații.")


