# Geo Analyse Demo

Dépôt pour découvrir pandas, GeoPandas et la cartographie à partir d'un fichier de crimes à Montréal et des limites des postes de quartier (PDQ).


## Données

- `data/interventionscitoyendo.csv` : interventions avec catégorie, date, période, numéro de PDQ et coordonnées. Le fichier est encodé en ISO-8859-1.
- `data/limitepdq.geojson` : limites des PDQ, avec les champs `No_PDQ` et `Nom_PDQ`, en EPSG:4326.

Certaines lignes du CSV ont `LONGITUDE/LATITUDE` égales à `0/0` ou `1/1`. Les scripts les excluent avec une plage géographique approximative de Montréal avant de créer les points. Ce filtre produit un jeu d'exemples, il ne remplace pas une validation complète des données.

## Parcours

| Script | Notions illustrées |
|---|---|
| `scripts/01_pandas_geopandas_basics.py` | Lecture CSV et GeoJSON, aperçu/types, sélection de lignes et colonnes, conversion de date, catégories, création de points depuis longitude/latitude |
| `scripts/02_spatial_analysis.py` | Sélection spatiale avec pyogrio, validité des géométries, index spatial, jointure point-dans-polygone, comparaison entre PDQ déclaré et PDQ géométrique |
| `scripts/03_matplotlib_map.py` | Carte GeoPandas/Matplotlib avec limites et échantillon de points |
| `scripts/04_cartopy_map.py` | Fond Natural Earth, vue orthographique du globe centrée sur Montréal et encart détaillé avec Cartopy |

## Installation avec conda

Conda est recommandé pour réunir les dépendances Python et les bibliothèques géospatiales natives (GDAL/pyogrio, PROJ et Cartopy). Depuis la racine du dépôt :

```bash
conda env create -f environment.yml
conda activate geo-analyse-demo
```

Dans VS Code, sélectionnez ensuite l'interpréteur de l'environnement `geo-analyse-demo` avec la commande **Python: Select Interpreter**.

Pour actualiser un environnement existant après une modification de `environment.yml` :

```bash
conda env update -f environment.yml --prune
```

## Installation avec pip

Dans un environnement virtuel Python :

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Les dépendances géospatiales natives peuvent être plus simples à installer avec conda-forge. Si pip échoue lors de l'installation de GeoPandas, pyogrio ou Cartopy, utilisez la procédure conda ci-dessus.

## Exécution

Lancez les scripts depuis la racine du dépôt. Chaque script trouve les données relativement à son propre emplacement :

```bash
python scripts/01_pandas_geopandas_basics.py
python scripts/02_spatial_analysis.py
python scripts/03_matplotlib_map.py
python scripts/04_cartopy_map.py
```

Les deux derniers scripts enregistrent les cartes PNG dans `outputs/`. Ils tracent au plus 8 000 points, avec un échantillon déterministe, pour garder les cartes lisibles. Au premier lancement du script Cartopy, Natural Earth télécharge et met en cache les couches du fond cartographique; une connexion Internet est nécessaire à cette étape.