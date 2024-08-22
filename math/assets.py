from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sys import stdout
from os import mkdir, getcwd
import matplotlib.pyplot as plt
import numpy as np

stdout = stdout
eq_file_path = f"{getcwd()}/equations_non_lineaire"


# ==================================== EQUATION NON LINEAIRE =======================================
def equation_dir():
    try:
        mkdir(f"{getcwd()}/equations_non_lineaire")
    except FileExistsError:
        pass


def get_function_from_input():
    string_format = input("Entrer la fonction : ").replace("^", "**").replace(" e ", "E")
    if "x" not in string_format:
        print("La fonction w'ap pas de variable x.")
        return -1
    try:
        func = parse_expr(string_format, transformations=(standard_transformations +
                                                          (implicit_multiplication_application,)))

    except SyntaxError as er:
        print("Format incorrect.")
        print(er)
        return -1

    return func


def get_function():
    parsed = get_function_from_input()
    print(f"la fonction est {parsed}?")
    while input("y pour confirmer... ") != 'y':
        parsed = get_function_from_input()
        print(f"la fonction est {parsed}?")
    return parsed


def get_params(string, typeof=float, maxi=None):
    while True:
        try:
            borne = typeof(input(f"{string} : "))
            if maxi is not None:
                assert borne <= maxi
            break
        except ValueError:
            print("Valeur incorrecte. Entrez un nombre.")
        except AssertionError:
            print(f"Valeur incorrect. maximum : {maxi}.")

    return borne


def isolate(f, a, b):
    if (b - a) > 100:
        print("Balayage de l'intervalle. patienter...")
    try:
        a, b = (a, b) if (a < b) else (b, a)
        x = a
        sign = 1 if f(x) > 0 else -1
        interval = [a]
        if f(a) == 0:
            interval.append(a)
        while x < b:
            if (f(x) > 0 and sign < 0) or (f(x) < 0 and sign > 0):
                sign *= -1
                interval[-1] = ((x - 0.1) + interval[-1]) / 2
                interval.append(x)
            x += 0.1
        if len(interval) == 2:
            interval[1] = b
        else:
            if f(b) * f(interval[-1]) <= 0:
                interval.append(b)

        return [(interval[i], interval[i + 1]) for i in range(len(interval) - 1)]
    except TypeError:
        print("Le programme ne peut pas pas deternimer les valeurs des autres symboles")
        return []


def solution(f, a, b):
    try:
        a, b = (a, b) if (a < b) else (b, a)
        x = a
        sign = 1 if f(x) > 0 else -1
        possible = False  # possibilité de solution
        while x < b:
            if (f(x) > 0 and sign < 0) or (f(x) < 0 and sign > 0):
                sign *= -1
                possible = True
                break
            x += 0.1
        return possible
    except TypeError:
        print("Le programme ne peut pas pas deternimer les valeurs des autres symboles")


def eq_file_name(created=False):
    equation_dir()

    # --------------------------------------------
    def create_name():
        i = 0
        while True:
            try:
                open(f"fonction{i}.eq", 'r').close()

            except FileNotFoundError:
                if not created:
                    with open(f"{eq_file_path}/num.txt", 'w') as file:
                        file.write(f"{i}")
                        file.close()
                return f"fonction{i}.eq" if not created else f"fonction{i - 1}.eq"
            i += 1

    # --------------------------------------------
    try:
        with open(f"{eq_file_path}/num.txt", 'r') as file:
            i = int(file.read()) + 1
            file.close()

        if not created:
            with open(f"{eq_file_path}/num.txt", 'w') as file:
                file.write(str(i))
                file.close()
        return f"fonction{i}.eq" if not created else f"fonction{i - 1}.eq"

    except FileNotFoundError:
        return create_name()
    except ValueError:
        return create_name()

# def solution_plotting(f, solutions):
#     if not all(solutions):
#     ap, b = min(solutions), max(solutions)
#     X = np.linspace(ap, b, 500)
#     plt.plot(X, [f(x) for x in X])
#     s = [x for x in solutions]
