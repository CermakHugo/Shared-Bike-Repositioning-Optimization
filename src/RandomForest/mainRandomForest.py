from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

class BikeFluctuationPredictor:
    def __init__(self, data_path, target_column, test_size=0.2, n_estimators=100):
        self.data_path = data_path
        self.target_column = target_column
        self.test_size = test_size
        self.n_estimators = n_estimators
        self.model = RandomForestRegressor(n_estimators=self.n_estimators)
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None

    def load_data(self):
        self.data = pd.read_csv(self.data_path)
        X = self.data.drop(columns=[self.target_column])
        y = self.data[self.target_column]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=self.test_size)

    def train(self):
        self.model.fit(self.X_train, self.y_train)

    def predict(self):
        self.y_pred = self.model.predict(self.X_test)
        return self.y_pred

    def evaluate(self):
        self.predict()
        mae = mean_absolute_error(self.y_test, self.y_pred)
        print(f"Erreur absolue moyenne : {mae:.2f} (Nombre de vélo)")
        return mae

    def run(self):
        print("Chargement des données...")
        self.load_data()
        print("Entraînement du modèle...")
        self.train()
        print("Prédictions...")
        predictions = self.predict()
        print("Évaluation du modèle...")
        self.evaluate()
        print(f"Y Prédit : {predictions}")
