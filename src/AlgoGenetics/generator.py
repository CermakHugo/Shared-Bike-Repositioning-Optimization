import random

# Générer un individu aléatoire en fonction du nombre de station
def generer_individu(STATION_NUMBER):
    return [random.randint(0,100)].append([random.randint(0,STATION_NUMBER) for _ in range (STATION_NUMBER)])

# Générer une population
def generer_population(LONGUEUR_GENOME, TAILLE_POP):
    return [generer_individu(LONGUEUR_GENOME) for _ in range(TAILLE_POP)]
