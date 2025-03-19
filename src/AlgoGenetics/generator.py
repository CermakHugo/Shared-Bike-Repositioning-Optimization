# Générer un individu aléatoire
def generer_individu():
    return [random.randint(0, 1) for _ in range(LONGUEUR_GENOME)]

# Générer une population
def generer_population(TAILLE_POP):
    return [generer_individu() for _ in range(TAILLE_POP)]
