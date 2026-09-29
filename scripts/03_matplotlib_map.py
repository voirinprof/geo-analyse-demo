from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Lire les crimes et les postes de quartier depuis les fichiers sources.
crimes = pd.read_csv(
    DATA / "interventionscitoyendo.csv",
    encoding="latin-1",
    usecols=["CATEGORIE", "LONGITUDE", "LATITUDE"],
)

# On conserve seulement les points dans l'emprise approximative de la ville.
valid_coordinates = crimes["LONGITUDE"].between(-74.5, -73.3) & crimes[
    "LATITUDE"
].between(45.0, 46.0)

# On peut passer de DataFrame à GeoDataFrame en utilisant les colonnes de coordonnées pour créer des géométries de points.
crime_points = gpd.GeoDataFrame(
    crimes.loc[valid_coordinates].copy(),
    geometry=gpd.points_from_xy(
        crimes.loc[valid_coordinates, "LONGITUDE"],
        crimes.loc[valid_coordinates, "LATITUDE"],
    ),
    crs="EPSG:4326",
)
districts = gpd.read_file(DATA / "limitepdq.geojson", engine="pyogrio")

# On utilise un échantillon pour garder la carte lisible et rapide à produire.
points_to_plot = crime_points.sample(n=min(8000, len(crime_points)), random_state=42)
# On peut utiliser la méthode plot() de GeoDataFrame pour produire une carte simple.
ax = districts.plot(color="#e3eee8", edgecolor="#45665a", figsize=(9, 8))
# On peut superposer les points de crimes sur la carte des postes de quartier.
points_to_plot.plot(ax=ax, color="#bd4938", markersize=2, alpha=0.3)
ax.set_title("Les crimes signalés et les postes de quartier (matplotlib)")
ax.set_axis_off()

output = ROOT / "outputs" / "matplotlib_crimes.png"
output.parent.mkdir(exist_ok=True)
# On peut utiliser la figure associée à l'axe pour enregistrer la carte.
ax.figure.savefig(output, dpi=160, bbox_inches="tight")
plt.close(ax.figure)
print(f"Carte enregistrée dans {output}")