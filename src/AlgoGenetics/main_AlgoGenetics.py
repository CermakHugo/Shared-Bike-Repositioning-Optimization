# Créé par cerma, le 19/03/2025 en Python 3.7

import random
import mutation
import crossover
import generator
import fitness
import selector

# Paramètres
TAILLE_POP = 10   # Nombre d'individus
LONGUEUR_GENOME = 8  # Taille du chromosome (8 bits → valeurs de 0 à 255)
TAUX_MUTATION = 0.1  # Probabilité de mutation
N_GENERATIONS = 50  # Nombre d'itérations


# Algorithme génétique principal
def algorithme_genetique():
    population = generer_population(TAILLE_POP)

    for generation in range(N_GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        print(f"Génération {generation}: Meilleur score: {fitness(population[0])}")

        nouvelle_population = []
        while len(nouvelle_population) < TAILLE_POP:
            parent1, parent2 = selection(population), selection(population)
            enfant1, enfant2 = crossover(parent1, parent2, LONGUEUR_GENOME)
            nouvelle_population.extend([mutation(enfant1, TAUX_MUTATION), mutation(enfant2, TAUX_MUTATION)])

        population = nouvelle_population[:TAILLE_POP]

    return sorted(population, key=fitness, reverse=True)[0]

# Exécution de l'AG
meilleur_individu = algorithme_genetique()
meilleure_valeur = int("".join(map(str, meilleur_individu)), 2)
print(f"Meilleure solution trouvée: {meilleure_valeur} (f(x)={meilleure_valeur**2})")

