import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

class TSPSolver:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.distance = self.load_distance()

    def load_distance(self):
        df = pd.read_csv(self.csv_path, index_col=0)
        return df.values.tolist()

    def create_data_model(self):
        return {
            'distance': self.distance,
            'num_vehicles': 1,
            'depot': 0  # Station de départ (par défaut : première station)
        }

    def solve(self):
        data = self.create_data_model()

        # Création du gestionnaire d'index
        manager = pywrapcp.RoutingIndexManager(
            len(data['distance']), data['num_vehicles'], data['depot']
        )
        # Création du modèle de routage
        routing = pywrapcp.RoutingModel(manager)

        # Fonction de coût
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Paramètres de recherche
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Résolution
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            self.print_solution(manager, routing, solution)
            return self.return_solution(manager, routing, solution, data)
        else:
            print("Aucune solution trouvée.")

    def print_solution(self, manager, routing, solution):
        index = routing.Start(0)
        route = []
        total_distance = 0
        print("Chemin optimal :")
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            next_index = solution.Value(routing.NextVar(index))
            total_distance += routing.GetArcCostForVehicle(index, next_index, 0)
            index = next_index
        route.append(manager.IndexToNode(index))
        print(" → ".join(map(str, route)))
        print(f"Distance totale : {total_distance} unités")
    
    def return_solution(self,manager, routing, solution, data):
        total_distance = 0
        routes = {}

        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0
            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                next_index = solution.Value(routing.NextVar(index))
                print(f"route_distance = {route_distance}")
                print(f"index : {index} & next_index : {next_index}")
                print(f"distance = {data['distance'][index-1][next_index-1]}")
                route_distance += routing.GetArcCostForVehicle(index, next_index, vehicle_id)
                index = next_index
            route.append(manager.IndexToNode(index))  # retour au dépôt
            total_distance += route_distance
            routes[vehicle_id] = (route, route_distance)
        return routes, total_distance
