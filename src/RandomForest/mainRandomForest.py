from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Charger les données sur le nombre de vélo par station
data = fetch_california_housing()
X, y = data.data, data.target  # X = caractéristiques, y = prix

# Diviser entrainement et test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialiser le modèle Random Forest pour la régression
regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train, y_train)

# Prédire les prix des maisons
y_pred = regressor.predict(X_test)

# Évaluer l'erreur (différence entre prédictions et valeurs réelles)
mae = mean_absolute_error(y_test, y_pred)
print(f"Y Predit : {y_pred}")
print(f"Erreur absolue moyenne : {mae:.2f} (Nombre de vélo)")
