# Sélection par tournoi
def selection(population):
    return max(random.sample(population, 3), key=fitness)
