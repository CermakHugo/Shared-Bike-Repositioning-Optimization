from RandomForest import BikeFluctuationPredictor
from OR_Strategies import TSPSolver
from AlgoGenetics import GeneticAlgorithm
import pandas as pd
import numpy as np

def main():
    # === 1. Prédire les flux de vélos du jour suivant ===
    predictor = BikeFluctuationPredictor(
        data_path="../data/diff_dic.csv",
        target_column="2020-04-30"  # à remplacer dynamiquement si besoin
    )
    predictor.run()
    flux_prevu = predictor.y_pred  # Liste de prédictions

    # === 2. Charger la matrice de distances ===

    dist_df = pd.read_csv("../data/matrice_distance.csv", index_col=0)
    distance_matrix = dist_df.values.tolist()

    # === 3. Algorithme Génétique ===
    ag = GeneticAlgorithm(
        genome_length=len(flux_prevu),
        population_size=100,
        mutation_rate=0.1,
        generations=500,
        distance_matrix=distance_matrix,
        stations=flux_prevu
    )
    best_genome, score_ag = ag.run()

    # === 4. Solution avec OR-Tools ===
    or_solver = VRPSolver("../data/matrice_distance.csv")
    solution_or, dist_or = or_solver.solve_return()

    # === 5. Présentation & comparaison ===
    print("\n Comparaison des solutions :")
    print("---------------------------------------------------")
    print(f" Algorithme génétique :")
    print(f"  → Génome : {best_genome}")
    print(f"  → Fitness : {score_ag:.4f}")

    print("\n OR-Tools :")
    for v_id, (route, dist) in solution_or.items():
        print(f"  → Véhicule {v_id + 1} : {' → '.join(map(str, route))} | Distance : {dist} unités")
    print(f"  → Distance totale OR-Tools : {dist_or} unités")
    print(f"  → Fitness : {1/ (1 + dist_or)}")
    print("---------------------------------------------------")

    # Comparatif simplifié
    print("\n Résumé :")
    print(f"Distance AG (estimée via fitness) : ~{round(1 / score_ag)} unités")
    print(f"Distance OR-Tools : {dist_or} unités")
    if (1 / score_ag) < dist_or:
        print(" L'algorithme génétique propose une meilleure solution !")
    else:
        print(" OR-Tools propose une meilleure solution !")


main()