import numpy as np
from os import getcwd, mkdir
import matplotlib.pyplot as plt

interpolation_file_path = f"{getcwd()}/interpolation"


# =============================
def get_value():
    correct = False
    value = 0
    while not correct:
        try:
            value = int(input("entrer le nombre de point : "))
            assert value >= 0
            correct = True
        except ValueError:
            print("Entrer des valeurs entière")
        except AssertionError:
            print("La valeur doit etre supperieur a 0")
        except:
            print("Erreur")
    return value


def get_points():
    X, Y = [], []
    print("Entrer les points sous forme x; y")
    for i in range(get_value()):
        correct = False
        while not correct:
            try:
                
                x, y = map(float,
                           [i for i in input(f"point {i} : ").replace(',', '.').split(';') if i not in [' ', '']])
                X.append(x)
                Y.append(y)
                correct = True
            except ValueError:
                print("Entrer des valeurs enetières")
            except:
                print("Erreur")
    return X, Y


def interpolation_dir():
    try:
        mkdir("./interpolation")
    except FileExistsError:
        pass


def interpolation_file_name(created=False):
    interpolation_dir()

    # --------------------------------------------
    def create_name():
        i = 0
        while True:
            try:
                open(f"equation{i}.intp", 'r').close()

            except FileNotFoundError:
                if not created:
                    with open(f"{interpolation_file_path}/num.txt", 'w') as file:
                        file.write(f"{i}")
                        file.close()
                return f"equation{i}.intp" if not created else f"equation{i - 1}.intp"
            i += 1

    # --------------------------------------------
    try:
        with open(f"{interpolation_file_path}/num.txt", 'r') as file:
            i = int(file.read()) + 1
            file.close()

        if not created:
            with open(f"{interpolation_file_path}/num.txt", 'w') as file:
                file.write(str(i))
                file.close()
        return f"equation{i}.intp" if not created else f"equation{i - 1}.intp"

    except FileNotFoundError:
        return create_name()
    except ValueError:
        return create_name()


def interpolation_plotting(X, Y, options, f=None):
    plot_x = np.linspace(min(X) - 2, max(X) + 2, 500)
    plt.scatter(X, Y, label="points initiaux", color="red")
    if f is not None:
        plt.plot(plot_x, np.array([f(x_i) for x_i in plot_x]), label="solution exacte", color="orange")

    for option in options:
        plt.plot(plot_x, np.array([option['P'](x_i) for x_i in plot_x]), label=option['name'], color=option['color'])

    plt.legend()
    plt.show()
