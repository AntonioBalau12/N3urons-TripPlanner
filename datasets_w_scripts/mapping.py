import pandas as pd

# === ÎNCĂRCARE DATASET ===
df = pd.read_csv(r"C:\Users\anton\PycharmProjects\PythonProject3\scrapping\csv\intersect_dataset_geo_clean.csv")

# === MAPARE CATEGORY ========
category_map = {
    'art gallery': 1, 'burial_places': 2, 'castles': 3, 'cathedrals': 4, 'cemetery': 5, 'churches': 6,
    'cinemas': 7, 'concert hall': 8, 'fortresses': 9, 'fountains': 10, 'galleries': 11, 'gardens': 12,
    'gates': 13, 'installations': 14, 'landmark': 15, 'mausoleums': 16, 'monasteries': 17, 'monuments': 18,
    'mosques': 19, 'museums': 20, 'palaces': 21, 'parks': 22, 'public sculpture': 23, 'railway stations': 24,
    'restaurants': 25, 'sculptures': 26, 'synagogues': 27, 'temples': 28, 'theatres': 29, 'towers': 30,
    'walls': 31, 'watchtowers': 32
}

df['category_main'] = df['category'].dropna().str.split(',').str[0].str.strip()
df['category_encoded'] = df['category_main'].map(category_map)

# === MAPARE CITY ============
city_map = {
    'Amsterdam': 1, 'Athens': 2,'Barcelona': 3,'Berlin': 4,'Brussels': 5,'Bucharest': 6,
    'Budapest': 7,'Copenhagen': 8,'Dublin': 9,'Istanbul': 10,'Krakow': 11,'Lisbon': 12,'London': 13,
    'Milan': 14,'Munich': 15,'Paris': 16,'Prague': 17,'Rome': 18,'Vienna': 19,'Warsaw': 20,'Zurich': 21
}

df['city_encoded'] = df['city'].map(city_map)

# === MAPARE COUNTRY =========
country_map = {
    'NL': 1,'GR': 2,'ES': 3,'DE': 4,'BE': 5,'RO': 6,'HU': 7,'DK': 8,'IE': 9,'TR': 10,
    'PL': 11,'PT': 12,'GB': 13,'IT': 14,'FR': 15,'CZ': 16,'AT': 17,'CH': 18
}

df['country_encoded'] = df['country'].map(country_map)

# === SALVARE ================
df.to_csv("dataset_encoded_final.csv", index=False)
print("✅ Dataset salvat: dataset_encoded_final.csv")
