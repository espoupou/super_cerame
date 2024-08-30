import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import statsmodels.api as sm
from scipy.stats import pearsonr

""":cvar

datas was collected under
 20 bar of pressure with 9 nozzles of 2.4 mm on planta 1
 20 bar of pressure with 10 nozzles of 2.5 mm on planta 2
data = {
    "date 2024" : {
        density (g), viscosity (second), residue (%),
        [grain-size],
        in temperature (celcuis), out temperature (celcuis),
        production (kg/min)
        },
    }
"""

planta1 = {
    "15-07": {
        "density": 167,
        "viscosity": 24,
        "residue": 7,
        "grain-size": [46, 31, 9, 8.5, 2.5, 1],
        "temp-in": 577,
        "temp-out": 111,
        "production": 77
    },

    "16-07": {
        "density": 161,
        "viscosity": 13,
        "residue": 7.5,
        "grain-size": [46, 30, 8.5, 8.5, 3, 1],
        "temp-in": 579,
        "temp-out": 108,
        "production": 67
    },

    "17-07": {
        "density": 165.5,
        "viscosity": 24,
        "residue": 7,
        "grain-size": [0, 0, 0, 0, 0, 0],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "18-07": {
        "density": 167,
        "viscosity": 27,
        "residue": 8,
        "grain-size": [0, 0, 0, 0, 0, 0],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "22-07": {
        "density": 163,
        "viscosity": 14,
        "residue": 7.5,
        "grain-size": [41, 35.5, 9.5, 8.5, 3, 1.5],
        "temp-in": 528,
        "temp-out": 104,
        "production": 71
    },

    "23-07": {
        "density": 166,
        "viscosity": 18,
        "residue": 9,
        "grain-size": [40, 35.5, 10.5, 9, 2.5, 1],
        "temp-in": 559,
        "temp-out": 109,
        "production": 0
    },

    "24-07": {
        "density": 166.5,
        "viscosity": 21,
        "residue": 8,
        "grain-size": [40.5, 33.5, 10, 10.5, 3, 1.5],
        "temp-in": 560,
        "temp-out": 107,
        "production": 0
    },

    "25-07": {
        "density": 166,
        "viscosity": 27,
        "residue": 8,
        "grain-size": [37, 38, 9.5, 9.5, 3, 1],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "29-07": {
        "density": 162,
        "viscosity": 17,
        "residue": 7,
        "grain-size": [0, 0, 0, 0, 0, 0],
        "temp-in": 560,
        "temp-out": 108,
        "production": 70.2
    },
}

planta2 = {
    "15-07": {
        "density": 166,
        "viscosity": 23,
        "residue": 7,
        "grain-size": [48, 31, 8.5, 8, 2.5, 1],
        "temp-in": 0,
        "temp-out": 0,
        "production": 77
    },

    "16-07": {
        "density": 166,
        "viscosity": 23,
        "residue": 7,
        "grain-size": [44.5, 34, 8.5, 9.5, 3, 0.5],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "17-07": {
        "density": 166.5,
        "viscosity": 22,
        "residue": 6,
        "grain-size": [0, 0, 0, 0, 0, 0],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "18-07": {
        "density": 167,
        "viscosity": 26,
        "residue": 7,
        "grain-size": [0, 0, 0, 0, 0, 0],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "22-07": {
        "density": 163,
        "viscosity": 18,
        "residue": 5,
        "grain-size": [0, 0, 0, 0, 0, 0],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "23-07": {
        "density": 164,
        "viscosity": 17,
        "residue": 5,
        "grain-size": [40, 33.5, 9, 9, 3, 1.5],
        "temp-in": 588,
        "temp-out": 113,
        "production": 91.8
    },

    "24-07": {
        "density": 0,
        "viscosity": 0,
        "residue": 0,
        "grain-size": [34.5, 38, 11, 11, 3, 2],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "25-07": {
        "density": 166,
        "viscosity": 22,
        "residue": 7,
        "grain-size": [0, 0, 0, 0, 0, 0],
        "temp-in": 0,
        "temp-out": 0,
        "production": 0
    },

    "26-07": {
        "density": 165,
        "viscosity": 21,
        "residue": 8,
        "grain-size": [45.5, 33.5, 8.5, 8, 2.5, 1.5],
        "temp-in": 556,
        "temp-out": 114,
        "production": 0
    },

    "29-07": {
        "density": 163,
        "viscosity": 17,
        "residue": 7.8,
        "grain-size": [0, 0, 0, 0, 0, 0],
        "temp-in": 568,
        "temp-out": 112,
        "production": 91.6
    },
}

grain_units = ["U425", "U300", "U250", "U180", "U125", "U0"]

all_filters = {
    "density": "densities",
    "viscosity": "viscosities",
    "residue": "residues",
    "production": "productions"
}


class Planta:
    def __init__(self, data):
        self.data = data

    def filter_null(self, key, *filters):
        for item in filters:
            if item.lower() not in self.data[key] or (
                    isinstance(self.data[key][item.lower()], list) and sum(self.data[key][item.lower()]) == 0
            ) or (
                    self.data[key][item.lower()] == 0
            ):
                return False
        return True

    def dates(self, *filters):
        return [key for key, value in self.data.items() if self.filter_null(key, *filters)]

    def densities(self, *filters):
        return [value["density"] for key, value in self.data.items() if self.filter_null(key, *filters)]

    def viscosities(self, *filters):
        return [value["viscosity"] for key, value in self.data.items() if self.filter_null(key, *filters)]

    def residues(self, *filters):
        return [value["residue"] for key, value in self.data.items() if self.filter_null(key, *filters)]

    def productions(self, *filters):
        return [value["production"] for key, value in self.data.items() if self.filter_null(key, *filters)]

    def grain_sizes(self, *filters):
        grains = [value["grain-size"] for key, value in self.data.items()
                  if self.filter_null(key, *[item for item in filters if item != "plot"])]
        if "plot" in filters:
            return np.array([np.array(grain) for grain in grains]).transpose()
        return grains

    def filter_data(self, *filters):
        return {_key: {key_: self.data[_key][key_] for key_ in filters}
                for _key in self.data.keys() if self.filter_null(_key, *filters)}

    # def data_planta(self, **filters):
    #
    #     if filters is None or not filters:
    #         return []
    #     datas = {}
    #     for item in set(filters).intersection(set(all_filters.keys())):
    #         datas[item.capitalize()] = eval(f"self.{all_filters[item]}(")


def daily_log_plot():
    # Plot pour la Densité
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 3, 1)
    plt.plot(unit1.dates(), unit1.densities(), label="Planta 1", marker='o', color='orange')
    plt.title("Évolution de la Densité")
    plt.ylabel("Densité (g)")
    plt.legend()
    plt.subplot(2, 3, 4)
    plt.plot(unit2.dates("density"), unit2.densities("density"), label="Planta 2", marker='o', color='orange')
    plt.xlabel("Date")
    plt.ylabel("Densité (g)")
    plt.legend()

    # Plot pour la Viscosité
    plt.subplot(2, 3, 2)
    plt.plot(unit1.dates(), unit1.viscosities(), label="Planta 1", marker='o')
    plt.title("Évolution de la Viscosité")
    plt.ylabel("Viscosité (s)")
    plt.legend()
    plt.subplot(2, 3, 5)
    plt.plot(unit2.dates("viscosity"), unit2.viscosities("viscosity"), label="Planta 2", marker='o')
    plt.xlabel("Date")
    plt.ylabel("Viscosité (s)")
    plt.legend()

    # Plot pour le Résidu
    plt.subplot(2, 3, 3)
    plt.plot(unit1.dates(), unit1.residues(), label="Planta 1", marker='o', color='green')
    plt.title("Évolution du Résidu")
    plt.ylabel("Viscosité (s)")
    plt.legend()
    plt.subplot(2, 3, 6)
    plt.plot(unit2.dates("residue"), unit2.residues("residue"), label="Planta 2", marker='o', color='green')
    plt.xlabel("Date")
    plt.ylabel("Résidu (%)")
    plt.legend()

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.tight_layout()
    plt.show()


def daily_grainlog_plot():
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(grain_units, unit1.grain_sizes("plot", "grain-size"), label=unit1.dates("grain-size"), marker='o')
    plt.title("Journal de granulométrie")
    plt.ylabel("masse (g)")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(grain_units, unit2.grain_sizes("plot", "grain-size"), label=unit2.dates("grain-size"), marker='o')
    plt.xlabel("taille (um)")
    plt.ylabel("masse (g)")
    plt.legend()
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.tight_layout()
    plt.show()


def prod_k_mean():
    data = {
        "unit": ["Planta 1", "Planta 1", "Planta 1", "Planta 1", "Planta 1", "Planta 1", "Planta 1", "Planta 1",
                 "Planta 1",
                 "Planta 2", "Planta 2", "Planta 2", "Planta 2", "Planta 2", "Planta 2", "Planta 2", "Planta 2",
                 "Planta 2"],
        "density": [167, 161, 163, 162, 163, 166, 166.5, 166, 162,
                    166, 166, 166.5, 167, 163, 164, 166, 165, 163],
        "viscosity": [24, 13, 14, 17, 14, 18, 21, 27, 17,
                      23, 23, 22, 26, 18, 17, 22, 21, 17],
        "residue": [7, 7.5, 7.5, 7, 7.5, 9, 8, 8, 7,
                    7, 7, 6, 7, 5, 5, 7, 8, 7.8],
        "production": [77, 67, 71, 70.2, 71, 0, 0, 0, 70.2,
                       77, 0, 0, 0, 0, 91.8, 0, 0, 91.6]
    }

    df = pd.DataFrame(data)

    # Exclusion of production as 0
    df = df[df['production'] > 0]

    # Normalisation des données
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[["density", "viscosity", "residue"]])

    # Détermination du nombre optimal de clusters avec la méthode du coude
    inertia = []
    for n in range(1, 10):
        kmeans = KMeans(n_clusters=n, random_state=0)
        kmeans.fit(scaled_data)
        inertia.append(kmeans.inertia_)

    # Affichage du graphe de la méthode du coude
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 10), inertia, marker='o')
    plt.title('Méthode du coude pour déterminer le nombre optimal de clusters')
    plt.xlabel('Nombre de clusters')
    plt.ylabel('Inertie')
    plt.grid(True)
    plt.show()

    # Application du K-means avec le nombre de clusters choisi (par exemple 3)
    kmeans = KMeans(n_clusters=3, random_state=0)
    df['cluster'] = kmeans.fit_predict(scaled_data)

    print(df[['unité', 'densité', 'viscosité', 'résidu', 'cluster']])


def prod_lin_reg():
    # correlation de l'unité 1 avec regression linéaire
    df_planta1 = pd.DataFrame(data_planta1)
    X_planta1 = df_planta1[["Densité", "Viscosité", "Résidu"]]
    y_planta1 = df_planta1["Production"]
    model_planta1 = LinearRegression()
    model_planta1.fit(X_planta1, y_planta1)
    y_pred_planta1 = model_planta1.predict(X_planta1)
    coefficients_planta1 = model_planta1.coef_
    intercept_planta1 = model_planta1.intercept_
    r2_planta1 = r2_score(y_planta1, y_pred_planta1)

    # corelation de l'unité 2 avec regression linéaire
    df_planta2 = pd.DataFrame(data_planta2)
    X_planta2 = df_planta2[["Densité", "Viscosité", "Résidu"]]
    y_planta2 = df_planta2["Production"]
    model_planta2 = LinearRegression()
    model_planta2.fit(X_planta2, y_planta2)
    y_pred_planta2 = model_planta2.predict(X_planta2)
    coefficients_planta2 = model_planta2.coef_
    intercept_planta2 = model_planta2.intercept_
    r2_planta2 = r2_score(y_planta2, y_pred_planta2)

    print((coefficients_planta1, intercept_planta1, r2_planta1), (coefficients_planta2, intercept_planta2, r2_planta2))


def cor_viscosity_grain_size(unit):
    df = pd.DataFrame({
        "viscosity": unit.viscosities("viscosity", "grain-size"),
        **dict(zip(grain_units, unit.grain_sizes("viscosity", "grain-size", "plot")))
    })
    X = df[[*grain_units]]
    y = df["viscosity"]
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    coefficients_planta1 = model.coef_
    intercept_planta1 = model.intercept_
    r2_planta1 = r2_score(y, y_pred)
    print((coefficients_planta1, intercept_planta1, r2_planta1))
    new_data = pd.DataFrame({
        "U425": [41],
        "U300": [32],
        "U250": [9.5],
        "U180": [8.5],
        "U125": [3],
        "U0": [1.5]
    })
    predicted_viscosity = model.predict(new_data)
    print(predicted_viscosity[0])


def cor_residue_grain_size_on_viscosity(unit):
    df_planta1 = pd.DataFrame({
        "Viscosité": unit.viscosities("viscosity", "grain-size", "residue"),
        "residue": unit.residues("viscosity", "grain-size", "residue"),
        **dict(zip(grain_units, unit.grain_sizes("viscosity", "grain-size", "residue", "plot")))
    })
    var = ["residue", *grain_units]
    X_planta1 = df_planta1[var]
    y_planta1 = df_planta1["Viscosité"]
    model_planta1 = LinearRegression()
    model_planta1.fit(X_planta1, y_planta1)
    y_pred_planta1 = model_planta1.predict(X_planta1)
    coefficients_planta1 = model_planta1.coef_
    # intercept_planta1 = model_planta1.intercept_
    # r2_planta1 = r2_score(y_planta1, y_pred_planta1)
    print((dict(zip(var, coefficients_planta1))))


def cor_viscosity_grain_size_OLS(unit):
    df = pd.DataFrame({
        "viscosity": unit.viscosities("viscosity", "grain-size"),
        **dict(zip(grain_units, unit.grain_sizes("viscosity", "grain-size", "plot")))
    })

    # Variables indépendantes (granulométrie)
    X = df[grain_units]
    # Ajout de l'intercept
    X = sm.add_constant(X)
    # Variable dépendante (viscosité)
    y = df['viscosity']

    # Modèle de régression linéaire
    model = sm.OLS(y, X).fit()

    # Résumé des résultats
    print(model.summary())

    plt.figure(figsize=(10, 6))
    plt.bar(grain_units, model.params[1:], color='skyblue')
    plt.xlabel('Taille de grain (μm)')
    plt.ylabel('Coefficient')
    plt.title('Impact des différentes tailles de grains sur la viscosité')
    plt.show()
    # new_observation = pd.DataFrame(dict(zip(grain_units, [41, 32, 9.5, 10, 3.5, 1])))
    # new_observation["viscosity"] = [21]
    # # Prédiction pour le 31-07
    # predicted_viscosity = model.predict(new_observation)
    #
    # # Comparaison avec la valeur réelle (21)
    # print(predicted_viscosity)


def cor_density_viscosity():
    # Préparation des données pour l'unité 1
    densities1 = unit1.densities("density", "viscosity")
    viscosities1 = unit1.viscosities("density", "viscosity")

    # Calcul de la corrélation pour l'unité 1
    correlation1, _ = pearsonr(densities1, viscosities1)

    # Préparation des données pour l'unité 2
    densities2 = unit2.densities("density", "viscosity")
    viscosities2 = unit2.viscosities("density", "viscosity")
    correlation2, _ = pearsonr(densities2, viscosities2)

    # Visualisation
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.scatter(densities1, viscosities1, color='blue')
    plt.title(f"Unité 1: Corrélation entre densité et viscosité\n(Corrélation: {correlation1:.2f})")
    plt.xlabel("Densité")
    plt.ylabel("Viscosité")

    # Graphique de dispersion pour l'unité 2
    plt.subplot(1, 2, 2)
    plt.scatter(densities2, viscosities2, color='green')
    plt.title(f"Unité 2: Corrélation entre densité et viscosité\n(Corrélation: {correlation2:.2f})")
    plt.xlabel("Densité")
    plt.ylabel("Viscosité")

    plt.tight_layout()
    plt.show()

    print("planta 1: ", correlation1)
    print("planta 2: ", correlation2)


def effet_on_prod():
    # Conversion des données en DataFrame
    # unit1_data = unit1.filter_data()
    # unit2_data = unit2.filter_data("density", "viscosity", "residue", "grain-size", "production")
    # print(unit1_data, unit2_data)
    df1 = pd.DataFrame({
        "density": unit1.densities("density", "viscosity", "residue", "grain-size", "production"),
        "viscosity": unit1.viscosities("density", "viscosity", "residue", "grain-size", "production"),
        "residue": unit1.residues("density", "viscosity", "residue", "grain-size", "production"),
        **dict(zip(grain_units, unit1.grain_sizes(
            "density", "viscosity", "residue", "grain-size", "production", "plot"))),
        "production": unit1.productions("density", "viscosity", "residue", "grain-size", "production")
    })
    df2 = pd.DataFrame({
        "density": unit2.densities("density", "viscosity", "residue", "grain-size", "production"),
        "viscosity": unit2.viscosities("density", "viscosity", "residue", "grain-size", "production"),
        "residue": unit2.residues("density", "viscosity", "residue", "grain-size", "production"),
        **dict(zip(grain_units, unit2.grain_sizes(
            "density", "viscosity", "residue", "grain-size", "production", "plot"))),
        "production": unit2.productions("density", "viscosity", "residue", "grain-size", "production")
    })
    var = ['density', 'viscosity', 'residue', *grain_units]

    print("PLANTA 1")
    # Analyse de corrélation
    corr_visc_density = df1['viscosity'].corr(df1['density'])
    corr_residue_viscosity = df1['residue'].corr(df1['viscosity'])
    # corr_gran_viscosity = df1[['grain-size']].corrwith(df1['viscosity'])
    # corr_gran_density = df1[['grain-size']].corrwith(df1['density'])

    # Modélisation prédictive pour la production
    X = df1[var]
    y = df1['production']

    X_train, X_test, y_train, y_test = X, X, y, y  # train_test_split(X, y, test_size=0.1, random_state=42)
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    # Analyse des résultats
    coefficients = model.coef_
    r2 = r2_score(y_train, y_pred)

    print("Corrélation Viscosité-Densité:", corr_visc_density)
    print("Corrélation Résidu-Viscosité:", corr_residue_viscosity)
    # print("Corrélation Granulométrie-Viscosité:", corr_gran_viscosity)
    # print("Corrélation Granulométrie-Densité:", corr_gran_density)
    print("R² pour la prédiction de la production:", r2)
    print("Coefficients du modèle:", dict(zip(var, coefficients)))

    print("PLANTA 2")
    # Analyse de corrélation
    corr_visc_density = df2['viscosity'].corr(df1['density'])
    corr_residue_viscosity = df2['residue'].corr(df1['viscosity'])
    # corr_gran_viscosity = df2[['grain-size']].corrwith(df1['viscosity'])
    # corr_gran_density = df2[['grain-size']].corrwith(df1['density'])

    # Modélisation prédictive pour la production
    X = df2[var]
    y = df2['production']

    X_train, X_test, y_train, y_test = X, X, y, y  # train_test_split(X, y, test_size=0.3, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Analyse des résultats
    r2 = r2_score(y_test, y_pred)
    coefficients = model.coef_

    print("Corrélation Viscosité-Densité:", corr_visc_density)
    print("Corrélation Résidu-Viscosité:", corr_residue_viscosity)
    # print("Corrélation Granulométrie-Viscosité:", corr_gran_viscosity)
    # print("Corrélation Granulométrie-Densité:", corr_gran_density)
    print("R² pour la prédiction de la production:", r2)
    print("Coefficients du modèle:", dict(zip(var, coefficients)))


# definition des deux unité avec tous les données recoltées
unit1 = Planta(planta1)
unit2 = Planta(planta2)

data_planta1 = {
    "Production": unit1.productions("production"),
    "Densité": unit1.densities("production"),
    "Viscosité": unit1.viscosities("production"),
    "Résidu": unit1.residues("production"),
}

data_planta2 = {
    "Production": unit2.productions("production"),
    "Densité": unit2.densities("production"),
    "Viscosité": unit2.viscosities("production"),
    "Résidu": unit2.residues("production"),
}

# cor_residue_grain_size_on_viscosity(unit2)
plt.figure(figsize=(12, 6))

plt.subplot(1, 1, 1)
plt.plot(list(range(1, 8)), [560, 1140, 1040, 930, 920, 870, 800], label="temperature", marker='o', color='red')
plt.title("Temperature de cuisson")
plt.ylabel("temperature")
plt.xlabel("niveau")
plt.legend()
plt.tight_layout()
plt.show()
exit()


# Fonction pour préparer les données en ajoutant la granulométrie
def prepare_data_for_model(planta, grain_units):
    X = []
    y = []

    for date, data in planta.items():
        if data["production"] != 0:
            features = [
                data["density"],
                data["residue"],
                *data["grain-size"],
            ]
            X.append(features)
            y.append(data["viscosity"])

    X = np.array(X)
    y = np.array(y)

    # Ajouter une constante pour l'interception
    X = sm.add_constant(X)
    return X, y


# Données pour l'unité 1
X1, y1 = prepare_data_for_model(planta1, grain_units)

# Modèle pour l'unité 1
model1 = sm.OLS(y1, X1).fit()

# Données pour l'unité 2
X2, y2 = prepare_data_for_model(planta2, grain_units)

# Modèle pour l'unité 2
model2 = sm.OLS(y2, X2).fit()

# Nouvelle observation pour le 31-07 pour l'unité 1
new_data1 = [164, 8, 41, 32, 9.5, 10, 3, 3.5]
new_data1 = sm.add_constant(np.array(new_data1).reshape(1, -1))

# Prédiction pour l'unité 1
prediction1 = model1.predict(new_data1)

# Nouvelle observation pour le 31-07 pour l'unité 2
new_data2 = [165, 8, 42.5, 37, 7.5, 8.5, 2.5, 1]
new_data2 = sm.add_constant(np.array(new_data2).reshape(1, -1))

# Prédiction pour l'unité 2
prediction2 = model2.predict(new_data2)

# Afficher les résultats
print(f"Prédiction de la viscosité pour l'unité 1 le 31-07: {prediction1[0]}")
print(f"Prédiction de la viscosité pour l'unité 2 le 31-07: {prediction2[0]}")
