from pathlib import Path

import geopandas as gpd
import pandas as pd
import pyogrio


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Lire les crimes et les postes de quartier depuis les fichiers sources.
crimes = pd.read_csv(
    DATA / "interventionscitoyendo.csv",
    encoding="latin-1",
    usecols=["CATEGORIE", "PDQ", "LONGITUDE", "LATITUDE"],
)

# On conserve seulement les points dans l'emprise approximative de la ville.
valid_coordinates = crimes["LONGITUDE"].between(-74.5, -73.3) & crimes[
    "LATITUDE"
].between(45.0, 46.0)
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

# Lire seulement les limites qui croisent l'emprise du PDQ 4.
sample_district = districts.loc[districts["No_PDQ"] == 4].geometry.iloc[0]
nearby_districts = pyogrio.read_dataframe(
    DATA / "limitepdq.geojson",
    columns=["No_PDQ", "Nom_PDQ"],
    bbox=sample_district.bounds,
)
print(f"Polygones de PDQ lus dans l'emprise sélectionnée : {len(nearby_districts)}")

# Vérifier les géométries; ne réparer que celles qui sont invalides.
invalid_geometries = ~districts.geometry.is_valid
print(f"Géométries de PDQ invalides : {invalid_geometries.sum()}")
if invalid_geometries.any():
    districts.loc[invalid_geometries, "geometry"] = districts.loc[
        invalid_geometries, "geometry"
    ].make_valid()

# L'index spatial trouve rapidement les points candidats dans un poste donné.
point_positions = crime_points.sindex.query(sample_district, predicate="contains")
print(f"Points du PDQ 4 trouvés par l'index spatial : {len(point_positions):,}")

# La jointure ajoute le numéro de poste trouvé à partir de la géométrie.
# On utilise la colonne "geometry" pour la jointure spatiale, et on ne garde que les colonnes utiles.
joined = gpd.sjoin(
    crime_points,
    districts[["No_PDQ", "Nom_PDQ", "geometry"]],
    how="left",
    predicate="within",
)

# On élimine les points qui n'ont pas de poste associé.
matched = joined.dropna(subset=["No_PDQ"]).copy()
# On peut comparer le PDQ déclaré dans le CSV avec le PDQ trouvé par la jointure spatiale.
reported_pdq = pd.to_numeric(matched["PDQ"], errors="coerce")
# On peut compter les écarts entre le PDQ déclaré et le PDQ trouvé par la jointure spatiale.
mismatches = reported_pdq.ne(matched["No_PDQ"]).sum()

print(f"\nPoints aux coordonnées valides : {len(crime_points):,}")
print(f"Points associés à un poste : {len(matched):,}")
print(f"Points sans poste associé : {joined['No_PDQ'].isna().sum():,}")
print(f"Écarts entre le PDQ déclaré et le PDQ spatial : {mismatches:,}")
print("\nNombre de crimes par poste attribué spatialement :")

# On peut compter le nombre de crimes par poste attribué spatialement.
print(joined.groupby("Nom_PDQ", dropna=False).size().sort_values(ascending=False).head(10))