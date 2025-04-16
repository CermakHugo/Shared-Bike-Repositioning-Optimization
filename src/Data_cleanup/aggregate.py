import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------- UTILITAIRES ET FONCTIONS DE CALCUL -----------------
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcule la distance haversine (en km) entre deux points géographiques.
    Vous pouvez adapter le rayon de la Terre ici (défaut = 6371 km).
    """
    R = 6371  # Rayon de la Terre en km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def compute_distance_matrix(station_info):
    """
    Calcule la matrice des distances pour un dictionnaire {station_id: (lat, lng)}.
    La matrice retournée est un DataFrame pandas.
    """
    stations = sorted(station_info.keys())
    data = []
    for s1 in stations:
        row = []
        lat1, lon1 = station_info[s1]
        for s2 in stations:
            lat2, lon2 = station_info[s2]
            row.append(haversine_distance(lat1, lon1, lat2, lon2))
        data.append(row)
    df_dist = pd.DataFrame(data, index=stations, columns=stations)
    df_dist.index.name = 'station_id'
    return df_dist

def unify_coordinates(df):
    """
    Unifie les coordonnées pour chaque station en calculant la moyenne des coordonnées.
    Applique ce traitement séparément pour les départs et les arrivées.
    """
    # Pour les départs
    if 'start_station_name' in df.columns and 'start_lat' in df.columns:
        mean_start = df.groupby('start_station_name')[['start_lat', 'start_lng']].mean()
        df = df.merge(mean_start, on='start_station_name', suffixes=('', '_meanstart'))
        df['start_lat'] = df['start_lat_meanstart']
        df['start_lng'] = df['start_lng_meanstart']
        df.drop(['start_lat_meanstart', 'start_lng_meanstart'], axis=1, inplace=True)
    # Pour les arrivées
    if 'end_station_name' in df.columns and 'end_lat' in df.columns:
        mean_end = df.groupby('end_station_name')[['end_lat', 'end_lng']].mean()
        df = df.merge(mean_end, on='end_station_name', suffixes=('', '_meanend'))
        df['end_lat'] = df['end_lat_meanend']
        df['end_lng'] = df['end_lng_meanend']
        df.drop(['end_lat_meanend', 'end_lng_meanend'], axis=1, inplace=True)
    return df

def assign_station_ids(df):
    """
    Attribue un identifiant numérique à chaque station basée sur le nom.
    Retourne le DataFrame modifié et un dictionnaire mapping station_name -> station_id.
    """
    if 'start_station_name' not in df.columns or 'end_station_name' not in df.columns:
        return df, {}
    all_stations = set(df['start_station_name'].unique()) | set(df['end_station_name'].unique())
    station_mapping = {name: i + 1 for i, name in enumerate(sorted(all_stations))}
    df['start_station_id'] = df['start_station_name'].map(station_mapping)
    df['end_station_id'] = df['end_station_name'].map(station_mapping)
    return df, station_mapping

# ----------------- FONCTIONS DE PRÉTRAITEMENT DES DONNÉES -----------------
def clean_data(df):
    """
    Nettoie et prépare le DataFrame :
      - Uniformise les noms de colonnes,
      - Convertit les colonnes de dates,
      - Remplit les valeurs manquantes,
      - Met en minuscule les noms de stations,
      - Supprime les doublons.
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Conversion en datetime
    for col in ['started_at', 'ended_at']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Suppression des lignes avec dates invalides
    df.dropna(subset=['started_at', 'ended_at'], inplace=True)
    
    # Remplissage des valeurs manquantes pour les noms de stations
    for col in ['start_station_name', 'end_station_name']:
        if col in df.columns:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Remplissage des valeurs manquantes pour les coordonnées
    for col in ['start_lat', 'start_lng', 'end_lat', 'end_lng']:
        if col in df.columns:
            df[col].fillna(df[col].mean(), inplace=True)
    
    # Mise en minuscule
    for col in ['start_station_name', 'end_station_name']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower()
    
    # Suppression des doublons
    df.drop_duplicates(inplace=True)
    return df

def categorize_duration(duration):
    """
    Catégorise la durée du trajet :
      - 'short' si <= 15 minutes,
      - 'medium' si <= 45 minutes,
      - 'long' sinon.
    """
    if duration <= 15:
        return 'short'
    elif duration <= 45:
        return 'medium'
    else:
        return 'long'

def feature_engineering(df):
    """
    Ajoute des caractéristiques au DataFrame :
      - Durée du trajet en minutes,
      - Jour de la semaine et heure de départ,
      - Distance du trajet (avec haversine),
      - Catégorisation de la durée du trajet.
    """
    df['trip_duration'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
    # Filtrage des trajets avec durée négative ou trop longue
    df = df[(df['trip_duration'] >= 0) & (df['trip_duration'] <= 120)]
    df['day_of_week'] = df['started_at'].dt.dayofweek
    df['hour_of_day'] = df['started_at'].dt.hour
    if set(['start_lat', 'start_lng', 'end_lat', 'end_lng']).issubset(df.columns):
        df['trip_distance'] = haversine_distance(df['start_lat'], df['start_lng'],
                                                 df['end_lat'], df['end_lng'])
    else:
        df['trip_distance'] = np.nan
    df['trip_duration_category'] = df['trip_duration'].apply(categorize_duration)
    return df

def process_trip_csv(file_path):
    """
    Traite un CSV de trajets :
      - Lecture, nettoyage et enrichissement,
      - Unification des coordonnées,
      - Attribution des identifiants de stations.
    Retourne le DataFrame traité.
    """
    df = pd.read_csv(file_path, low_memory=False)
    df = clean_data(df)
    df = feature_engineering(df)
    df = unify_coordinates(df)
    df, station_mapping = assign_station_ids(df)
    return df

def process_station_csv(file_path):
    """
    Traite un CSV listant les stations (par ex. 'Divvy_Stations_2015'):
      - Lecture et renommage éventuel des colonnes,
      - Retourne un dictionnaire {station_id: (lat, lng)}.
    """
    df = pd.read_csv(file_path, low_memory=False)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    # Renommer les colonnes si besoin
    if 'lat' not in df.columns and 'start_lat' in df.columns:
        df.rename(columns={'start_lat': 'lat', 'start_lng': 'lng'}, inplace=True)
    if 'station_id' not in df.columns and 'id' in df.columns:
        df.rename(columns={'id': 'station_id'}, inplace=True)
    
    station_info = {}
    for _, row in df.iterrows():
        sid = row['station_id']
        lat = row['lat'] if 'lat' in row else np.nan
        lng = row['lng'] if 'lng' in row else np.nan
        if pd.notnull(lat) and pd.notnull(lng):
            station_info[sid] = (lat, lng)
    return station_info

# ----------------- FONCTIONS D'AGRÉGATION ET TRAITEMENT GLOBAL -----------------
def get_all_csv_files(input_folder):
    """
    Recherche récursive de tous les fichiers CSV dans input_folder.
    Retourne deux listes : une pour les fichiers de trajets et une pour les fichiers de stations.
    """
    all_files = glob.glob(os.path.join(input_folder, "**", "*.csv"), recursive=True)
    trip_files = []
    station_files = []
    for file in all_files:
        fname = os.path.basename(file).lower()
        if "stations" in fname:
            station_files.append(file)
        else:
            trip_files.append(file)
    return trip_files, station_files

def process_station_files(station_files):
    """
    Traite tous les CSV de stations et retourne un dictionnaire global des stations.
    """
    global_station_info = {}
    for file in station_files:
        try:
            info = process_station_csv(file)
            global_station_info.update(info)
            print(f"Station CSV traité : {file}")
        except Exception as e:
            print(f"Erreur dans le fichier station {file}: {e}")
    return global_station_info

def process_trip_files(trip_files):
    """
    Traite tous les CSV de trajets et retourne un DataFrame agrégé.
    """
    trips_list = []
    for file in trip_files:
        try:
            df_trip = process_trip_csv(file)
            trips_list.append(df_trip)
            print(f"Trip CSV traité : {file}")
        except Exception as e:
            print(f"Erreur lors du traitement du fichier trip {file}: {e}")
    if trips_list:
        return pd.concat(trips_list, ignore_index=True)
    else:
        return None

def update_station_info_from_trips(df_all):
    """
    Extrait les informations de stations à partir du DataFrame de trajets.
    Retourne un dictionnaire {station_id: (mean_lat, mean_lng)}.
    """
    df_all, computed_mapping = assign_station_ids(df_all)
    computed_station_info = {}
    for name, sid in computed_mapping.items():
        subset_start = df_all[df_all['start_station_id'] == sid][['start_lat', 'start_lng']]
        subset_end = df_all[df_all['end_station_id'] == sid][['end_lat', 'end_lng']]
        lat_vals = pd.concat([subset_start['start_lat'], subset_end['end_lat']], ignore_index=True)
        lng_vals = pd.concat([subset_start['start_lng'], subset_end['end_lng']], ignore_index=True)
        if not lat_vals.empty and not lng_vals.empty:
            computed_station_info[sid] = (lat_vals.mean(), lng_vals.mean())
    return computed_station_info

def merge_station_info(global_station_info, computed_station_info):
    """
    Fusionne les informations de stations obtenues via les CSV de stations
    et celles calculées à partir des trajets. Les infos déjà présentes sont conservées.
    """
    for sid, coords in computed_station_info.items():
        if sid not in global_station_info:
            global_station_info[sid] = coords
    return global_station_info

def compute_usage_counts(df_all, global_station_info):
    """
    Calcule l'usage total (nombre de départs + arrivées) pour chaque station.
    Retourne la série usage_count et la liste des top 20% des stations.
    """
    usage_count = pd.Series(0, index=global_station_info.keys(), dtype=float)
    for sid in global_station_info.keys():
        count_start = (df_all['start_station_id'] == sid).sum()
        count_end = (df_all['end_station_id'] == sid).sum()
        usage_count[sid] = count_start + count_end
    usage_sorted = usage_count.sort_values(ascending=False)
    cutoff = int(np.ceil(len(usage_sorted) * 0.2))  # Top 20%
    top_stations = usage_sorted.index[:cutoff]
    return usage_count, top_stations

def save_distance_matrices(global_station_info, top_stations, output_folder):
    """
    Calcule et sauvegarde les matrices de distance pour toutes les stations
    et pour le top 20% des stations les plus utilisées.
    """
    df_dist_all = compute_distance_matrix(global_station_info)
    df_dist_all.to_csv(os.path.join(output_folder, "GLOBAL_distance_all.csv"))
    
    station_info_top = {s: global_station_info[s] for s in top_stations}
    df_dist_top = compute_distance_matrix(station_info_top)
    df_dist_top.to_csv(os.path.join(output_folder, "GLOBAL_distance_top20pct.csv"))
    print("Matrices de distances sauvegardées.")

def save_graph(df_all, output_folder):
    """
    Sauvegarde un histogramme de la distribution des durées de trajets.
    """
    plt.figure(figsize=(8, 5))
    sns.histplot(df_all['trip_duration'], bins=30, kde=True)
    plt.title("Distribution des durées des trajets")
    plt.savefig(os.path.join(output_folder, "aggregated_trip_duration_hist.png"))
    plt.close()
    print("Graphique sauvegardé.")

# ----------------- FONCTION MAIN -----------------
def main():
    """
    Fonction principale :
      1. Définit les dossiers d'entrée et de sortie.
      2. Recherche récursive des CSV dans le dossier d'entrée.
      3. Traite et agrège les CSV de trajets.
      4. Met à jour la liste globale des stations à partir des trajets et des CSV stations.
      5. Calcule l'usage des stations et extrait le top 20%.
      6. Calcule et sauvegarde les matrices de distances.
      7. Sauvegarde un graphique d'analyse.
    """
    # Chemins modifiables selon votre structure
    input_folder = "/home/timeworid/Documents/AI Project/divvydata"
    output_folder = "/home/timeworid/Documents/AI Project/data_output"
    os.makedirs(output_folder, exist_ok=True)
    
    # 1. Recherche des fichiers CSV dans tous les sous-dossiers
    trip_files, station_files = get_all_csv_files(input_folder)
    
    # Affichage de debug pour vérifier les fichiers trouvés
    print("Fichiers CSV de trajets trouvés :")
    for f in trip_files:
        print(" -", f)
    print("Fichiers CSV de stations trouvés :")
    for f in station_files:
        print(" -", f)
    
    # 2. Traitement des CSV de stations
    global_station_info = process_station_files(station_files)
    
    # 3. Traitement et agrégation des CSV de trajets
    df_all = process_trip_files(trip_files)
    if df_all is None:
        print("Aucune donnée de trajets traitée.")
        return
    agg_csv = os.path.join(output_folder, "aggregated_trips.csv")
    df_all.to_csv(agg_csv, index=False)
    print("Données de trajets agrégées sauvegardées :", agg_csv)
    
    # 4. Mise à jour de la liste des stations à partir des trajets
    computed_station_info = update_station_info_from_trips(df_all)
    global_station_info = merge_station_info(global_station_info, computed_station_info)
    
    # 5. Calcul de l'usage des stations et extraction du top 20%
    usage_count, top_stations = compute_usage_counts(df_all, global_station_info)
    
    # 6. Calcul et sauvegarde des matrices de distance
    save_distance_matrices(global_station_info, top_stations, output_folder)
    
    # 7. Sauvegarde d'un graphique d'analyse
    save_graph(df_all, output_folder)
    
    print("Traitement global terminé. Résultats dans :", output_folder)

if __name__ == "__main__":
    main()
