from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Lire les crimes et les postes de quartier depuis les fichiers sources.
crimes = pd.read_csv(
    DATA / "interventionscitoyendo.csv",
    encoding="latin-1",
    usecols=["LONGITUDE", "LATITUDE"],
)
# On conserve seulement les points dans l'emprise approximative de la ville.
valid_coordinates = crimes["LONGITUDE"].between(-74.5, -73.3) & crimes[
    "LATITUDE"
].between(45.0, 46.0)

# On conserve les colonnes longitude/latitude pour les projeter avec Cartopy.
crime_points = crimes.loc[valid_coordinates]
districts = gpd.read_file(DATA / "limitepdq.geojson", engine="pyogrio")

# On utilise un échantillon pour garder la carte lisible et rapide à produire.
points_to_plot = crime_points.sample(n=min(8000, len(crime_points)), random_state=42)

# Une vue orthographique représente une portion du globe depuis l'espace.
map_crs = ccrs.Orthographic(
    central_longitude=-73.5,
    central_latitude=45.5,
)
data_crs = ccrs.PlateCarree()
fig, ax = plt.subplots(figsize=(11, 8), subplot_kw={"projection": map_crs})
# On peut ajouter des éléments de fond pour représenter l'eau, la terre, les lacs, les rivières, les côtes et les frontières.
ax.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor="#d8eaf0", zorder=0)
ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor="#f2f0e8", zorder=0)
ax.add_feature(cfeature.LAKES.with_scale("50m"), facecolor="#d8eaf0", zorder=1)
# On peut ajouter les rivières, les côtes et les frontières avec des couleurs et des épaisseurs différentes.
ax.add_feature(
    cfeature.RIVERS.with_scale("50m"),
    edgecolor="#a5cbd7",
    linewidth=0.45,
    zorder=1,
)
ax.add_feature(
    cfeature.COASTLINE.with_scale("50m"),
    edgecolor="#71878a",
    linewidth=0.55,
    zorder=1,
)
ax.add_feature(
    cfeature.BORDERS.with_scale("50m"),
    edgecolor="#9c8e7e",
    linewidth=0.7,
    zorder=1,
)
ax.add_geometries(
    districts.geometry,
    crs=data_crs,
    facecolor="#e3eee8",
    edgecolor="#45665a",
    linewidth=0.5,
    zorder=2,
)
ax.scatter(
    points_to_plot["LONGITUDE"],
    points_to_plot["LATITUDE"],
    color="#bd4938",
    s=6,
    alpha=0.6,
    transform=data_crs,
    zorder=3,
)

# L'emprise élargie rend la courbure de la vue sphérique visible.
ax.set_extent([-110.0, -45.0, 15.0, 75.0], crs=data_crs)
ax.set_title("Crimes à Montréal : vue orthographique du globe")

# L'encart conserve un niveau de détail suffisant pour les quartiers et les points.
min_x, min_y, max_x, max_y = districts.total_bounds
padding_x = (max_x - min_x) * 0.03
padding_y = (max_y - min_y) * 0.03
inset = fig.add_axes(
    [0.07, 0.08, 0.34, 0.36],
    projection=map_crs,
)
inset.set_facecolor("#d8eaf0")
inset.add_geometries(
    districts.geometry,
    crs=data_crs,
    facecolor="#e3eee8",
    edgecolor="#45665a",
    linewidth=0.45,
    zorder=2,
)
inset.scatter(
    points_to_plot["LONGITUDE"],
    points_to_plot["LATITUDE"],
    color="#bd4938",
    s=6,
    alpha=0.6,
    transform=data_crs,
    zorder=3,
)
inset.set_extent(
    [min_x - padding_x, max_x + padding_x, min_y - padding_y, max_y + padding_y],
    crs=data_crs,
)
inset.set_title("Détail : Montréal", fontsize=9)
inset.spines["geo"].set_edgecolor("#45665a")
inset.spines["geo"].set_linewidth(1.0)

output = ROOT / "outputs" / "cartopy_crimes.png"
output.parent.mkdir(exist_ok=True)
fig.savefig(output, dpi=160, bbox_inches="tight")
plt.close(fig)
print(f"Carte enregistrée dans {output}")