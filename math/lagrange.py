from sys import stdout
from time import sleep
from assets import get_function
from sympy import var, init_printing
from sympy.utilities.lambdify import lambdify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from interpolation_assets import (get_points, interpolation_dir, interpolation_file_path, interpolation_file_name,
                                  interpolation_plotting)


x = var('x')
init_printing(use_unicode=True)


def lagrange(X, Y):
    with open(f"{interpolation_file_path}/{interpolation_file_name(created=True)}", 'a') as file:
        [print("\n\n\t INTERPOLATION : LAGRANGE \n", file=fic) for fic in [stdout, file]]
        while True:
            P = ""
            for i in range(len(X)):
                phi = ""
                for j in range(len(X)):
                    if i != j:
                        phi += f" * ((x - ({X[j]}))/(({X[i]}) - ({X[j]})))"
                P += f" + (({Y[i]})*({phi[3::]}))"
            P = P[3::]

            try:
                func = parse_expr(P, transformations=(standard_transformations +
                                                      (implicit_multiplication_application,)))
                break
            except SyntaxError as er:
                [print("Format incorrect. Rentrer ap nouveau les valeurs : \n", file=fic) for fic in [stdout, file]]
                X, Y = get_points()
                file.write(f"\nX = {X}\t Y = {Y}")

        [print(f"P(x) = {func}", file=fic) for fic in [stdout, file]]
        P = lambdify(x, func)
        file.close()
        sleep(3)
        return {'P': P, 'name': "Lagrange", 'color': "green", 'linestyle': "x"}


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

            result = lagrange(X, Y)
            interpolation_plotting(X, Y, [result], f)

# 2; 1
# 3; -1
# -1; 2
# 4; 3
# x^2 + cos(x^2 + 1) +2x -4
