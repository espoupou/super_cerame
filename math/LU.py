import numpy as np
from math import sqrt
from sys import stdout
from linear_system_assets import (lu_sum, get_array, y_solution, gauss_solution, line_sum, float_matrix, systeme_dir,
                                  sys_file_path, sys_file_name, matrix_arrange, is_positive_define)


def lu_decomposition_crout(matrix):
    a = np.array(float_matrix(matrix))
    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\t DECOMPOSITION LU : CROUT \n", file=fic) for fic in [stdout, file]]

        L = np.zeros((len(a), len(a) + 1), dtype=float)
        U = np.zeros((len(a), len(a) + 1), dtype=float)

        for i in range(len(a) - 1):
            a[i::, ::] = matrix_arrange(a[i::, ::], i)
            [print(f"A\n{a}\n", file=fic) for fic in [stdout, file]]
            U[i][i] = 1

            for j in range(i, len(a)):
                [print(f"\nL[{j}][{i}] = A[{j}][{i}]", end="", file=fic) for fic in [stdout, file]]
                L[j][i] = a[j][i] - lu_sum(i=j, j=i, stop=i, L=L, U=U)

            [print(f"\n\nL\n{L[:, :len(a):]}\n", file=fic) for fic in [stdout, file]]
            for j in range(i + 1, len(a)):
                try:
                    [print(f"U[{i}][{j}] = (A[{i}][{j}]", end="", file=fic) for fic in [stdout, file]]
                    U[i][j] = (a[i][j] - lu_sum(i, j, stop=i, L=L, U=U))
                    U[i][j] /= L[i][i]
                    [print(f") / L[{i}][{i}]", file=fic) for fic in [stdout, file]]
                except ZeroDivisionError:
                    [print("Division par Zero rencontrée", file=fic) for fic in [stdout, file]]
                    return
                except RuntimeWarning:
                    [print("Division par Zero rencontrée", file=fic) for fic in [stdout, file]]
                    return

            [print(f"\nU\n{U[:, :len(a):]}\n", file=fic) for fic in [stdout, file]]

        # U[w][w] = 1 et Calcul de l[w][w]
        [print(f"\nU[{len(a) - 1}][{len(a) - 1}] = 1", file=fic) for fic in [stdout, file]]
        U[len(a) - 1][len(a) - 1] = 1
        [print(f"\nU\n{U[:, :len(a):]}\n", file=fic) for fic in [stdout, file]]

        [print(f"\nL[{len(a) - 1}][{len(a) - 1}] = ap[{len(a) - 1}][{len(a) - 1}]", end="", file=fic)
         for fic in [stdout, file]]

        L[len(a) - 1][len(a) - 1] = a[len(a) - 1][len(a) - 1] - lu_sum(i=len(a) - 1, j=len(a) - 1, stop=(len(a) - 1),
                                                                       L=L, U=U)
        [print(f"\nL\n{L[:, :len(a):]}\n", file=fic) for fic in [stdout, file]]

        # verification de A = LU
        [print(f"\nA\n{np.matmul(L[:, :len(L):], U[:, :len(L):])}", file=fic) for fic in [stdout, file]]

        # Resolution de LY = b
        [print("\nL = [L|b]", file=fic) for fic in [stdout, file]]
        L[:, len(a)] = a[:, len(a)]
        [print(f"{L}\n", file=fic) for fic in [stdout, file]]
        Y = y_solution(L)
        if Y is None:
            [print("Matrice non inversible", file=fic) for fic in [stdout, file]]
            return
        [print(f"Y = {Y}t\n", file=fic) for fic in [stdout, file]]

        # Resolution de UX = Y
        [print("U = [U|Y]", file=fic) for fic in [stdout, file]]
        U[:, len(a)] = Y
        [print(f"{U}\n", file=fic) for fic in [stdout, file]]
        X = gauss_solution(U)
        [print(f"X = {X}t", file=fic) for fic in [stdout, file]]
    return X


def lu_decomposition_doolittle(matrix):
    a = np.array(float_matrix(matrix))
    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\t DECOMPOSITION LU : DOOLITTLE \n", file=fic) for fic in [stdout, file]]

        L = np.zeros((len(a), len(a) + 1), dtype=float)
        U = np.zeros((len(a), len(a) + 1), dtype=float)
        for i in range(len(a)):
            a[i::, ::] = matrix_arrange(a[i::, ::], i)
            [print(f"A\n{a}\n", file=fic) for fic in [stdout, file]]

            [print(f"A\n{a}\nL[{i}][{i}] = 1", file=fic) for fic in [stdout, file]]
            L[i][i] = 1
            for j in range(i, len(a)):
                [print(f"U[{i}][{j}] = A[{i}][{j}]\n", end='', file=fic) for fic in [stdout, file]]
                U[i][j] = a[i][j] - lu_sum(i, j, i, L, U)
            [print(f"\nU {U}", file=fic) for fic in [stdout, file]]

            for j in range(i + 1, len(a)):
                [print(f"L[{j}][{i}] = (A[{j}][{i}]", end='', file=fic) for fic in [stdout, file]]
                L[j][i] = a[j][i] - lu_sum(j, i, i, L, U)
                [print(f") / U[{i}][{i}]", file=fic) for fic in [stdout, file]]
                L[j][i] /= U[i][i]
            [print(f"L {L}", file=fic) for fic in [stdout, file]]

        [print(f"A\n{np.matmul(L[:, :len(L):], U[:, :len(L):])}", file=fic) for fic in [stdout, file]]

        # Resolution de LY = b
        [print("\nL = [L|b]", file=fic) for fic in [stdout, file]]
        L[:, len(a)] = a[:, len(a)]
        [print(f"{L}\n", file=fic) for fic in [stdout, file]]
        Y = y_solution(L)
        if Y is None:
            [print("Matrice non inversible", file=fic) for fic in [stdout, file]]
            return
        [print(f"Y = {Y}\n", file=fic) for fic in [stdout, file]]

        # Resolution de UX = Y
        [print("U = [U|Y]", file=fic) for fic in [stdout, file]]
        U[:, len(a)] = Y
        [print(f"{U}\n", file=fic) for fic in [stdout, file]]
        X = gauss_solution(U)
        [print(f"X = {X}t", file=fic) for fic in [stdout, file]]
        file.close()
    return X


def lu_decomposition_cholesky(matrix):
    a = np.array(float_matrix(matrix))

    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\t DECOMPOSITION LU : CHOLESKY \n", file=fic) for fic in [stdout, file]]

        if not is_positive_define(a):
            [print("La matrice w'est pas définie positive", file=fic) for fic in [stdout, file]]
            return

        L = np.zeros((len(a), len(a) + 1))
        LT = np.zeros((len(a), len(a) + 1))
        [print(f"A\n{a}\n", file=fic) for fic in [stdout, file]]
        [print("Arrangement de la matrice", file=fic) for fic in [stdout, file]]
        for i in range(len(a) - 1):
            a[i::, ::] = matrix_arrange(a[i::, ::], pivot_col=i)
        [print(f"A\n{a}\n", file=fic) for fic in [stdout, file]]

        for i in range(len(a)):
            for j in range(i):
                [print(f"L[{i}][{j}] = (ap[{j}][{i}]", end='', file=fic) for fic in [stdout, file]]
                if L[j][j] == 0:
                    print("la matrice w'est pas inversible")
                    return

                L[i][j] = (a[j][i] - lu_sum(i, j, i, L, LT)) / L[j][j]
                LT[j][i] = L[i][j]
                [print(f")/L[{i}][{i}]", file=fic) for fic in [stdout, file]]
            [print(f"L[{i}][{i}] = sqrt(ap[{i}][{i}]", end='', file=fic) for fic in [stdout, file]]
            try:
                L[i][i] = sqrt(a[i][i] - line_sum(i, i, L))
            except ValueError:
                [print("\nLa methode de choleski w'est pas applicable à cette matrice.", file=fic) for fic in
                 [stdout, file]]
                return
            LT[i][i] = L[i][i]
            [print(")", file=fic) for fic in [stdout, file]]
            [print(f"\nL\n{L}", file=fic) for fic in [stdout, file]]
            [print(f"\nLT\n{LT}\n", file=fic) for fic in [stdout, file]]
        [print(f"A\n{np.matmul(L[:, :len(L):], LT[:, :len(L):])}", file=fic) for fic in [stdout, file]]

        # Resolution de LY = b
        [print("\nL = [L|b]", file=fic) for fic in [stdout, file]]
        L[:, len(a)] = a[:, len(a)]
        [print(f"{L}\n", file=fic) for fic in [stdout, file]]
        Y = y_solution(L)
        if Y is None:
            [print("Matrice non inversible", file=fic) for fic in [stdout, file]]
            return
        [print(f"Y = {Y}\n", file=fic) for fic in [stdout, file]]

        # Resolution de UX = Y
        [print("LT = [LT|Y]", file=fic) for fic in [stdout, file]]
        LT[:, len(a)] = Y
        [print(f"{LT}\n", file=fic) for fic in [stdout, file]]
        X = gauss_solution(LT)
        [print(f"X = {X}t", file=fic) for fic in [stdout, file]]
        file.close()
    return X


if __name__ == "__main__":
    systeme_dir()

    while input("Entrer pour recommencer...") == "":
        import warnings

        a = get_array()

        with open(f"{sys_file_path}/{sys_file_name()}", 'w') as file:
            file.write(f"A :\n {str(a)}")
            file.close()

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            Cr = lu_decomposition_crout(a)
            Do = lu_decomposition_doolittle(a)
            Ch = lu_decomposition_cholesky(a)
        print(f"\n Crout : {Cr}\n Doolittle : {Do}\n Cholesky : {Ch}")
