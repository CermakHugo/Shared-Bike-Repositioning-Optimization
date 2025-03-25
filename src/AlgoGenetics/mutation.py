import random

# Mutation (inversion aléatoire de bits)
def mutation(individu, TAUX_MUTATION):
    return [bit if random.random() > TAUX_MUTATION else str(random.randint(0,10)) for bit in individu]
