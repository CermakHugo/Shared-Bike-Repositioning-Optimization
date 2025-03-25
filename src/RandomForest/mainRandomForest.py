from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

# Charger les données sur le nombre de vélo par station
data = pd.read_csv("../../data/diff_dic.csv")

# X = date, y = liste de fluctuation de vélo
X = data.drop(columns=["2020-04-30"])
y = data["2020-04-30"]


# Diviser entrainement et test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Initialiser le modèle Random Forest pour la régression
regressor = RandomForestRegressor(n_estimators=100)
regressor.fit(X_train, y_train)

# Prédire les prix des maisons
y_pred = regressor.predict(X_test)

# Évaluer l'erreur (différence entre prédictions et valeurs réelles)
mae = mean_absolute_error(y_test, y_pred)
print(f"Y Predit : {y_pred}")
print(f"Erreur absolue moyenne : {mae:.2f} (Nombre de vélo)")
