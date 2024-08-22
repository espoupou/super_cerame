import numpy as np
from sys import stdout
from linear_system_assets import (matrix_arrange, jacobi_sum, get_array, float_matrix, systeme_dir,
                                  sys_file_path, sys_file_name, )
from assets import get_params


def jacobi(matrix, X=None):
    a = np.array(float_matrix(matrix))
    print(f"\nA :\n{a}")
    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\n\t JACOBI \n", file=fic) for fic in [stdout, file]]

        if X is None:
            X = np.zeros(len(a))

        Y = np.zeros(len(a))
        n = get_params("le nombre maximal d'itération", typeof=int)
        e = get_params("l'erreur", typeof=float)
        k = 0
        finished = False
        head = True

        for i in range(len(a) - 1):
            a[i::, ::] = matrix_arrange(a[i::, ::], i)

        while not finished:
            err = (sum([i ** 2 for i in (np.matmul(a[:, :len(a):], X[:]) - [i[0] for i in a[:, len(a):]])])) ** 0.5
            if head:
                [print("Formule : ", file=fic) for fic in [stdout, file]]

                for i in range(len(a)):
                    [print(f"X[{i}] = ({a[i][len(a)]} ", end='', file=fic) for fic in [stdout, file]]
                    jacobi_sum(a[i], X, i, True)
                    [print(f") / {a[i][i]}", file=fic) for fic in [stdout, file]]

                [print(f"\n|{'k'.center(4)}", end="", file=fic) for fic in [stdout, file]]

                # colonne des x0, x1, x2, ...
                for i in range(len(a)):
                    [print(f"| {str('x' + str(i)).center(15)} ", end="", file=fic) for fic in [stdout, file]]

                [print(f"| {'erreur'.center(15)} |", file=fic) for fic in [stdout, file]]
                head = False

            for i in range(len(a)):
                if a[i][i] == 0:
                    [print("\nLa matrice w'est pas inversible", file=fic) for fic in [stdout, file]]
                    return
                Y[i] = (a[i][len(a)] - jacobi_sum(a[i], X, i)) / a[i][i]

            # affichage
            [print(f"|{str(k).center(4)}", end="", file=fic) for fic in [stdout, file]]
            for i in range(len(a)):
                [print(f"| {str(Y[i])[:15:]:>15} ", end="", file=fic) for fic in [stdout, file]]
            [print(f"| {str(err)[:15:]:>15} |", file=fic) for fic in [stdout, file]]

            if err < e:
                [print(f"Convergence atteint : X= {X}", file=fic) for fic in [stdout, file]]
                return X

            if k >= n:
                [print(f"La converge,ce w'est pas atteint en {k} itération{'s' if k > 1 else ''}", file=fic)
                 for fic in [stdout, file]]
                return

            X = Y
            k += 1


if __name__ == "__main__":
    import warnings

    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        systeme_dir()
        while input("Entrer pour recommencer...") == "":
            a = get_array()
            with open(f"{sys_file_path}/{sys_file_name()}", 'w') as file:
                file.write(f"A :\n {str(a)}")
                file.close()
            jacobi(a)
