import random
import fitness
# Sélection par tournoi
def selection(population):
    return max(random.sample(population, 3), key=fitness.fitness)
