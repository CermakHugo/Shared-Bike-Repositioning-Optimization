# Créé par cerma, le 19/03/2025 en Python 3.7

import random
import pandas as pd

class GeneticAlgorithm:
    def __init__(self,
                 genome_length=8,
                 population_size=10,
                 mutation_rate=0.5,
                 generations=50,
                 poids_camions = 10,
                 poids_flux = 20,
                 poid_distance = 1,
                 distance_matrix=None,
                 stations=None):
        self.genome_length = genome_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.poids_camions = poids_camions
        self.poids_flux = poids_flux
        self.poid_distance = poid_distance
        self.distance_matrix = distance_matrix
        self.stations = stations
        self.population = []

    def initialize_population(self):
        self.population = self.generator.generer_population()

    # Générer un individu aléatoire en fonction du nombre de station
    def generer_individu(self):
        return [random.randint(1,100)]+[random.randint(0, self.genome_length) for i in range (self.genome_length)]

    # Générer une population
    def generer_population(self):
        return [self.generer_individu() for _ in range(self.population_size)]

    # Fonction d'évaluation (Fitness function) : Limiter les trajets trop long, l'utilisation de camion et surtout doit rééquilibrer les stations

    def fitness(self, genome):
        nb_camions, stations = self.decoder_genome(genome)
        camions = self.repartir_stations(nb_camions, stations)
        flux_stations = self.flux_stations(stations, camions)
        total_distance = self.distance_totale(camions)

        # Pénalise le nombre de camions
        penalite_camions = nb_camions * self.poids_camions

        # Pénalise les flux mal réparti
        penalite_flux = flux_stations * self.poids_flux

        # Pénalité pour des trajets trop long

        penalite_distance = total_distance * self.poid_distance

        # Moins la valeur est grande, mieux c’est → On inverse pour que la fitness soit à maximiser
        return 1 / (penalite_distance + penalite_camions + penalite_flux + 1e-6)  # éviter division par 0

    def decoder_genome(self, genome):
        nb_camions = int(genome[0])
        stations = genome[1:]
        return nb_camions, stations

    # Réparti les stations à rééquilibrer pour chaque camion
    def repartir_stations(self, nb_camions, stations):
        camions = [[] for _ in range(int(nb_camions))]
        if nb_camions > 0 :
            for i, station in enumerate(stations):
                camions[i % nb_camions].append(int(station))
        return camions

    #Calcul la distance maximal parcourru par tout les camions
    def distance_totale(self, camions):
        total = 0
        for trajet in camions:
            if len(trajet) < 2:
                continue
            for i in range(len(trajet) - 1):
                total += self.distance_matrix[trajet[i]][trajet[i + 1]]
        return total

    # Compte la différence total des fluxs de vélo dans toute les stations
    def flux_stations(self, stations, camions):
        total = 0
        all_stations = self.calculate_flow(camions)
        for i in all_stations :
            total += abs(i)
        return total

    # Met les fluxs de vélo après le passage des camions
    def calculate_flow(self, camions):
        all_stations = self.stations.copy()
        for camion in camions:
            for i in range(len(camion)):
                all_stations[int(camion[i])-1] = 0
        return all_stations

    # Croisement (Crossover) à un point
    def crossover(self, parent1, parent2):
        point = random.randint(1, self.genome_length - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

    # Mutation (inversion aléatoire de bits)
    def mutation(self, individu):
        return [bit if random.random() > self.mutation_rate else str(random.randint(0,10)) for bit in individu]

    # Sélection par tournoi
    def selection(self):
        return max(random.sample(self.population, 3), key=self.fitness)

    def evolve(self):
        self.population = self.generer_population()

        for generation in range(self.generations):
            self.population = sorted(
                self.population,
                key=self.fitness,
                reverse=True
            )
            best = self.population[0]
            best_score = self.fitness(best)
            print(f"Génération {generation}: Meilleur score: {best_score}")

            new_population = []
            while len(new_population) < self.population_size:
                parent1 = self.selection()
                parent2 = self.selection()
                enfant1, enfant2 = self.crossover(parent1, parent2)
                enfant1 = self.mutation(enfant1)
                enfant2 = self.mutation(enfant2)
                new_population.extend([enfant1, enfant2])

            self.population = new_population[:self.population_size]

        return sorted(
            self.population,
            key=self.fitness,
            reverse=True
        )[0]

    def run(self):
        best_genome = self.evolve()
        print(f"Meilleure solution trouvée : {best_genome}")
        score = self.fitness(best_genome)
        print(f"Fitness finale : {score}")
        return best_genome, score