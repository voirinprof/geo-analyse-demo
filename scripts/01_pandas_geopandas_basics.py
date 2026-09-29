from pathlib import Path

import geopandas as gpd
import pandas as pd

# On utilise le chemin relatif
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Le CSV source est encodé en ISO-8859-1.
crimes = pd.read_csv(DATA / "interventionscitoyendo.csv", encoding="latin-1")
print("Premières lignes :")
print(crimes.head())
print("\nTypes des colonnes :")
print(crimes.dtypes)

# Sélectionner des lignes avec une condition et ne conserver que quelques colonnes.
vehicle_thefts = crimes.loc[
    crimes["CATEGORIE"].str.contains("Vol de véhicule", na=False),
    ["CATEGORIE", "DATE", "PDQ"],
].copy()
print(f"\nNombre de vols de véhicule : {len(vehicle_thefts)}")
print(vehicle_thefts.head())

# Convertir une date texte et les colonnes répétitives en catégories.
# gestion des erreurs pour les dates invalides, coercer les valeurs invalides en NaT (Not a Time).
crimes["DATE"] = pd.to_datetime(crimes["DATE"], errors="coerce")

# On mesure la mémoire avant et après la conversion en type "category" pour les colonnes répétitives.
memory_before = crimes["CATEGORIE"].memory_usage(deep=True)
crimes["CATEGORIE"] = crimes["CATEGORIE"].astype("category")
crimes["QUART"] = crimes["QUART"].astype("category")
memory_after = crimes["CATEGORIE"].memory_usage(deep=True)

print(f"\nMémoire de la catégorie : {memory_before:,} -> {memory_after:,} octets")
print(f"Type de la date convertie : {crimes['DATE'].dtype}")

# Les coordonnées 0,0 et 1,1 sont des valeurs de remplacement, pas Montréal.
# on peut conserver seulement les points dans l'emprise de la ville.
valid_coordinates = crimes["LONGITUDE"].between(-74.5, -73.3) & crimes[
    "LATITUDE"
].between(45.0, 46.0)

# On peut passer de DataFrame à GeoDataFrame en utilisant les colonnes de coordonnées pour créer des géométries de points.
# On peut convertir les géométries en Point x,y
crime_points = gpd.GeoDataFrame(
    crimes.loc[valid_coordinates].copy(),
    geometry=gpd.points_from_xy(
        crimes.loc[valid_coordinates, "LONGITUDE"],
        crimes.loc[valid_coordinates, "LATITUDE"],
    ),
    crs="EPSG:4326",
)

# Lire les limites des postes de quartier depuis un fichier GeoJSON.
districts = gpd.read_file(
    DATA / "limitepdq.geojson",
    engine="pyogrio",
    columns=["No_PDQ", "Nom_PDQ"],
)
print(f"\nPoints de crimes aux coordonnées valides : {len(crime_points):,}")
print(f"SCR des postes de quartier : {districts.crs}")
print(districts[["No_PDQ", "Nom_PDQ"]].head())