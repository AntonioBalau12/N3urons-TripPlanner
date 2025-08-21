import pandas as pd
import numpy as np
from numpy.linalg import norm

# === 1. Încarcă fișierul original ===
df = pd.read_csv(r"dataset_encoded_final.csv")

# === 2. Creează coloana theme și theme_encoded din category_main ===
category_to_theme = {
    'churches': 'religion','cathedrals': 'religion','mosques': 'religion','synagogues': 'religion','temples': 'religion',
    'museums': 'culture','art gallery': 'culture','monuments': 'culture', 'sculptures': 'culture',
    'cinemas': 'entertainment','concert hall': 'entertainment','theatres': 'entertainment','opera house': 'entertainment',
    'restaurants': 'gastronomy',
    'parks': 'nature','gardens': 'nature',
    'landmark': 'urban_space','public sculpture': 'urban_space','fountains': 'urban_space','installations': 'urban_space',
}
df['theme'] = df['category_main'].map(category_to_theme)

theme_map = {
    'culture': 1,
    'religion': 2,
    'entertainment': 3,
    'nature': 4,
    'urban_space': 5,
    'gastronomy': 6
}
df['theme_encoded'] = df['theme'].map(theme_map)

# === 3. Creează price_per_review ===
df['price_per_review'] = df['price_level'] / (df['user_ratings_total'] + 1)

# === 4. Transformări log pentru distribuții skewed ===
df['log_user_ratings'] = np.log1p(df['user_ratings_total'])
df['log_price_per_review'] = np.log1p(df['price_per_review'])

# === 5. Coordonate centrale pentru fiecare oraș ===
city_centers = {
    'Amsterdam': (52.3676, 4.9041),     'Athens': (37.9838, 23.7275),
    'Barcelona': (41.3851, 2.1734),     'Berlin': (52.5200, 13.4050),
    'Brussels': (50.8503, 4.3517),      'Bucharest': (44.4268, 26.1025),
    'Budapest': (47.4979, 19.0402),     'Copenhagen': (55.6761, 12.5683),
    'Dublin': (53.3498, -6.2603),       'Istanbul': (41.0082, 28.9784),
    'Krakow': (50.0647, 19.9450),       'Lisbon': (38.7169, -9.1399),
    'London': (51.5074, -0.1278),       'Milan': (45.4642, 9.1900),
    'Munich': (48.1351, 11.5820),       'Paris': (48.8566, 2.3522),
    'Prague': (50.0755, 14.4378),       'Rome': (41.9028, 12.4964),
    'Vienna': (48.2082, 16.3738),       'Warsaw': (52.2297, 21.0122),
    'Zurich': (47.3769, 8.5417)
}

# === 6. Calcul distanță față de centrul orașului ===
def compute_distance(row):
    center = city_centers.get(row['city'], None)
    if center:
        return norm([row['lat'] - center[0], row['lon'] - center[1]])
    else:
        return np.nan

df['distance_to_city_center'] = df.apply(compute_distance, axis=1)
df['in_center_dynamic'] = (df['distance_to_city_center'] < 0.01).astype(int)

# === 7. Flaguri tematice binare ===
df['is_religious'] = (df['theme_encoded'] == 2).astype(int)
df['is_entertainment'] = (df['theme_encoded'] == 3).astype(int)

# === 8. Contează ce categorii are un obiectiv? Da! ===
df['kind_count'] = df['kind'].apply(lambda x: len(str(x).split(',')))

# === 9. Complexitatea numelui ===
df['name_length'] = df['name'].apply(lambda x: len(str(x)))
df['word_count'] = df['name'].apply(lambda x: len(str(x).split()))

# === 10. Popularitatea temei ===
theme_freq = df['theme_encoded'].value_counts().to_dict()
df['theme_popularity'] = df['theme_encoded'].map(theme_freq)

# === 11. Densitate locală per oraș și categorie ===
density = df.groupby(['city', 'category_main']).size().to_dict()
df['city_category_density'] = df.apply(lambda row: density.get((row['city'],
                                              row['category_main']), 0), axis=1)

# === 12. Recenzii relative față de media orașului ===
mean_city_ratings = df.groupby('city')['user_ratings_total'].transform('mean')
df['user_ratings_relative'] = df['user_ratings_total'] / (mean_city_ratings + 1)

# === 13. Salvează dataset final ===
output_path = r"C:\Users\anton\PycharmProjects\PythonProject3\model\dataset_fe.csv"
df.to_csv(output_path, index=False)
print(f"✅ Fișier salvat cu succes la: {output_path}")
