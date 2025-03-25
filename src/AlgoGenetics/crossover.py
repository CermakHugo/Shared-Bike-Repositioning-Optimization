import random

# Croisement (Crossover) à un point
def crossover(parent1, parent2, LONGUEUR_GENOME):
    point = random.randint(1, LONGUEUR_GENOME - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
