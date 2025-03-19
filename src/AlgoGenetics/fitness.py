# Fonction d'évaluation (Fitness function) : Maximiser x²
def fitness(individu):
    x = int("".join(map(str, individu)), 2)  # Convertir binaire → entier
    return x ** 2

