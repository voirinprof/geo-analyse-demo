"""Atelier : des interventions CSV à une carte par poste de quartier.

Complétez les fonctions marquées TODO en vous aidant des scripts 01 à 03.
Le script est volontairement incomplet tant que les exercices ne sont pas faits.
"""

from pathlib import Path

import geopandas as gpd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
import pyogrio


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "outputs" / "exercice_crimes_par_pdq.png"
TARGET_PDQ = 4


def load_crimes():
    """TODO 1 : lire les colonnes utiles du CSV dans un DataFrame."""

    # indice : utilisez l'argument usecols pour ne lire que les colonnes nécessaires.
    # indice : utilisez l'argument encoding pour lire correctement le CSV.
    # indice : utilisez l'argument dtype pour forcer le type de la colonne "PDQ" en entier.

    raise NotImplementedError("Complétez la tâche 1 : lire le fichier CSV.")


def prepare_crime_points(crimes):
    """TODO 2 : convertir les types, filtrer les coordonnées et créer des points."""

    # indice : utilisez la méthode pd.to_datetime() pour convertir la colonne "DATE" en type datetime.
    # indice : utilisez la méthode astype("category") pour convertir les colonnes répétitives en type "category".
    # indice : utilisez la méthode between() pour filtrer les coordonnées approximatives de la ville.
    # indice : utilisez gpd.GeoDataFrame() et gpd.points
    #          pour créer une colonne de géométrie de type Point à partir des colonnes "LONGITUDE" et "LATITUDE".
    raise NotImplementedError("Complétez la tâche 2 : préparer les points.")


def load_districts():
    """TODO 3 : lire les PDQ avec GeoPandas et vérifier leurs géométries."""

    # indice : utilisez gpd.read_file() pour lire le fichier GeoJSON.
    # indice : utilisez la méthode is_valid pour vérifier les géométries.
    # indice : utilisez la méthode make_valid() pour corriger les géométries invalides.

    raise NotImplementedError("Complétez la tâche 3 : lire les limites des PDQ.")


def analyze_crimes(crime_points, districts):
    """TODO 4 : appliquer un filtre pyogrio, l'index spatial et une jointure."""

    # indice : utilisez pyogrio.read_dataframe() pour lire seulement les polygones qui croisent l'emprise du PDQ 4.
    # indice : utilisez la méthode sindex.query() pour trouver les points de crimes dans le polygone du PDQ 4.
    # indice : utilisez gpd.sjoin() pour faire une jointure spatiale entre les points de crimes et les polygones des PDQ.
    raise NotImplementedError("Complétez la tâche 4 : analyser spatialement les crimes.")


def create_map(joined):
    """TODO 5 : créer et enregistrer une carte Matplotlib."""

    # indice : utilisez la méthode plot() de GeoDataFrame pour produire une carte simple.
    # indice : utilisez la méthode sample() pour réduire le nombre de points à afficher.
    # indice : utilisez la méthode savefig() pour enregistrer la carte dans un fichier PNG
    raise NotImplementedError("Complétez la tâche 5 : produire la carte.")


def main():
    crimes = load_crimes()
    crime_points = prepare_crime_points(crimes)
    districts = load_districts()
    joined = analyze_crimes(crime_points, districts)
    create_map(joined)


if __name__ == "__main__":
    main()