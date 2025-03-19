# Mutation (inversion aléatoire de bits)
def mutation(individu, TAUX_MUTATION):
    return [bit if random.random() > TAUX_MUTATION else 1 - bit for bit in individu]
