# Fonction d'évaluation (Fitness function) : Limiter les trajets trop long, l'utilisation de camion et surtout doit rééquilibrer les stations

# Paramètres :

poids_camions = 10

def fitness(genome, dist):
    nb_camions, stations = decoder_genome(genome)
    camions = repartir_stations(nb_camions, stations)
    total_distance = distance_totale(camions, dist)

    # Pénalise le nombre de camions
    penalite_camions = nb_camions * poids_camions

    # Moins la valeur est grande, mieux c’est → On inverse pour que la fitness soit à maximiser
    return 1 / (total_distance + penalite_camions + 1e-6)  # éviter division par 0

def decoder_genome(genome):
    nb_camions = genome[0]
    stations = genome[1:]
    return nb_camions, stations

# Réparti les stations à rééquilibrer pour chaque camion
def repartir_stations(nb_camions, stations):
    camions = [[] for _ in range(nb_camions)]
    for i, station in enumerate(stations):
        camions[i % nb_camions].append(station)
    return camions

#Calcul la distance maximal parcourru par tout les camions
def distance_totale(camions, dist):
    total = 0
    for trajet in camions:
        if len(trajet) < 2:
            continue
        for i in range(len(trajet) - 1):
            total += dist[trajet[i]][trajet[i + 1]]
    return total

def flux_stations()