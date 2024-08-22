import numpy as np
from sys import stdout
from time import sleep
from assets import get_function
from sympy import var, init_printing
from linear_system_assets import y_solution
from interpolation_assets import (get_points, interpolation_file_name, interpolation_file_path, interpolation_dir,
                                  interpolation_plotting)
from sympy.utilities.lambdify import lambdify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

x = var('x')
init_printing(use_unicode=True)


def newton_interpolation(X, Y):
    with open(f"{interpolation_file_path}/{interpolation_file_name(created=True)}", 'a+') as file:
        [print("\n\n\t INTERPOLATION : NEWTON \n", file=fic) for fic in [stdout, file]]
        while True:

            a = np.zeros((len(X), len(X) + 1), dtype=float)
            [print(f"matice de newton : \n{a}", file=fic) for fic in [stdout, file]]
            for i in range(len(X)):
                for j in range(i + 1):
                    [print(f"\nap[{i}][{j}] = ", end='', file=fic) for fic in [stdout, file]]
                    a[i][j] = 1
                    [print(1, end='', file=fic) for fic in [stdout, file]]
                    for x_i in X[:j]:
                        [print(f" * ({X[i]} - {x_i})", end='', file=fic) for fic in [stdout, file]]
                        a[i][j] *= X[i] - x_i
                [print('\n\n', a, file=fic) for fic in [stdout, file]]

            [print("\n[ap|y]", file=fic) for fic in [stdout, file]]
            a[:, len(a)] = Y
            [print('\n', a, file=fic) for fic in [stdout, file]]

            alpha = y_solution(a)
            [print(f"\nalpha : {alpha}", file=fic) for fic in [stdout, file]]

            P = ""
            for i in range(len(X)):
                P += " + (" + str(alpha[i])
                for x_i in X[:i]:
                    P += f" * (x - {x_i})"
                P += ")"
            P = P[3::]

            try:
                func = parse_expr(P, transformations=(standard_transformations +
                                                      (implicit_multiplication_application,)))
                break
            except SyntaxError:
                [print("Format incorrect. Rentrez à nouveau les valeurs : \n", file=fic) for fic in [stdout, file]]
                X, Y = get_points()
                file.write(f"\nX = {X}\t Y = {Y}")

        [print(f"P(x) = {func}", file=fic) for fic in [stdout, file]]
        P = lambdify(x, func)
        file.close()

        sleep(5)
        return {'P': P, 'name': "Newton", 'color': "blue", 'linestyle': "--"}


if __name__ == "__main__":
    import warnings
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        interpolation_dir()
        first = True
        while first if first else input("Entrer pour recommencer...") == "":
            f = None
            first = False
            # X, Y = get_points()
            X, Y = [2, 3, -1, 4], [1, -1, 2, 3]
            if input("\ny pour ajouter la fonction exacte... ") == 'y':
                f = lambdify(x, get_function())

            with open(f"{interpolation_file_path}/{interpolation_file_name()}", 'w') as file:
                file.write(f"X = {X}\t Y = {Y}")
                file.close()

            result = newton_interpolation(X, Y)
            interpolation_plotting(X, Y, [result], f)

# 2; 1
# 3; -1
# -1; 2
# 4; 3
# x^2 + cos(x^2 + 1) +2x -4
