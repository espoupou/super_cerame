import numpy as np
from sys import stdout
from os import path, remove
from sympy import var, init_printing
from LU import lu_decomposition_crout
from assets import get_params, get_function
from sympy.utilities.lambdify import lambdify
from linear_system_assets import systeme_dir, sys_file_path, sys_file_name
from interpolation_assets import (get_points, interpolation_dir, interpolation_file_path, interpolation_file_name,
                                  interpolation_plotting)


x = var('x')
init_printing(use_unicode=True)


def moindres_carres(X, Y):
    with open(f"{interpolation_file_path}/{interpolation_file_name(created=True)}", 'a') as file:
        [print("\n\n\t INTERPOLATION : MOINDRES CARRES \n", file=fic) for fic in [stdout, file]]
        p = get_params(f"entrez p (max = {len(X) - 1})", typeof=int, maxi=len(X) - 1)
        file.write(f"p = {p}")

        # matrice P
        P = np.zeros((p + 1, p + 2))

        for line in range(p + 1):
            for column in range(p + 1):
                # for x in range(len(X)):
                #     P[line, column] += (X[x]**((2 * p - line) - column)) * Y[x]
                P[line, column] = sum([x_i ** ((2 * p - line) - column) for x_i in X])

        for i in range(p + 1):
            # for x in range(len(X)):
            #     P[x, p + 1] += (X[x]**expo) * Y[x]
            P[i, p + 1] = sum([X[j] ** (p - i) * Y[j] for j in range(len(X))])

        [print(f"\n[P|B]\nP : \n{P[:, :]}", file=fic) for fic in [stdout, file]]

        systeme_dir()
        with open(f"{sys_file_path}/{sys_file_name()}", 'w') as fic:
            fic.write(f"A :\n {str(P)}")
            fic.close()
        alpha = lu_decomposition_crout(P)
        lu_path = f"{sys_file_path}/{sys_file_name(created=True)}"
        with open(f"{lu_path}", 'r') as fic:
            file.write(f"\n{fic.read()}")
            fic.close()

        if path.exists(f"{lu_path}"):
            remove(f"{lu_path}")

        func = f"(({alpha[0]}) * x**{p})"
        for i in range(1, p):
            func += f" + (({alpha[i]}) * x**{p - i})"
        func += f" + ({alpha[p]})"

        P = lambdify(x, func)
        [print(f"\nP(x) = {func}", file=fic) for fic in [stdout, file]]

        return {'P': P, 'name': "Moindres Carrés", 'color': "black", 'linestyle': "o"}


if __name__ == '__main__':
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
            result = moindres_carres(X, Y)
            interpolation_plotting(X, Y, [result], f)

# P :
# [[98. 36. 14.]
#  [36. 14.  6.]
#  [14.  6.  3.]]
# [[-36.]
#  [-14.]
#  [ -6.]]
