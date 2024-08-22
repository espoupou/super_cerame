import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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

all_filters = {
    "density": "densities",
    "viscosity": "viscosities",
    "residue": "residues",
    "production": "productions"
}

grain_units = ["U425", "U300", "U250", "U180", "U125", "U0"]


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

def daily_grainlog_plot()   qee


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
