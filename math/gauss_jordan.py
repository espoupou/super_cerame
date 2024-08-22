import numpy as np
from sys import stdout
from linear_system_assets import (get_array, gauss_jordan_solution, float_matrix, systeme_dir,
                                  sys_file_path, sys_file_name, matrix_arrange)


def gauss_jordan1(matrix):
    a = np.array(float_matrix(matrix))

    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\t GAUSS JORDAN \n", file=fic) for fic in [stdout, file]]

        n = len(a)

        for i in range(len(a)):
            if a[i][i] == 0:
                [print(f"ap[{i}][{i}]=0", file=fic) for fic in [stdout, file]]
                break
            pivot_line = a[i]
            for j in range(len(a)):
                if i != j:
                    for k in range(n + 1):
                        a[j][k] = a[j][k] - a[j][i] * pivot_line[k] / pivot_line[i]
        x = gauss_jordan_solution(a)
        [print(f"\nX = {x}", file=fic) for fic in [stdout, file]]
        return x


def gauss_jordan(matrix):
    a = np.array(float_matrix(matrix))

    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\t GAUSS JORDAN \n", file=fic) for fic in [stdout, file]]

        [print("Arrangement de la matrice", file=fic) for fic in [stdout, file]]
        for i in range(len(a)):
            a[i::, ::] = matrix_arrange(a[i::, ::], pivot_col=i)
        [print(f"A : \n{a}", file=fic) for fic in [stdout, file]]

        [print("\nElimination des éléments de la partie triangulaire bas ", file=fic) for fic in [stdout, file]]
        for i in range(len(a) - 1):
            [print(f"\n -piviotage", file=fic) for fic in [stdout, file]]
            a[i::, ::] = matrix_arrange(a[i::, ::], i)
            pivot_line = a[i]
            [print(f"\nA \n{a}", file=fic) for fic in [stdout, file]]

            if a[i][i] == 0:
                print("La methode de gauss Jordan w'est pas applicable")
                return

            [print(f"\n -normalisation : ", file=fic) for fic in [stdout, file]]
            [print(f"::: L{i} <- L{i}/{a[i][i]}", file=fic) for fic in [stdout, file]]

            a[i] = a[i] / a[i][i]
            [print(a, file=fic) for fic in [stdout, file]]
            [print("\n -application", file=fic) for fic in [stdout, file]]

            for j in range(i + 1, len(a)):
                [print(f"::: L{j} <- L{j} - ({a[j][i]})*L{i}", file=fic) for fic in [stdout, file]]
                a[j] = a[j] - a[j][i] * pivot_line / pivot_line[i]
                a[j][i] = 0

            [print(a, file=fic) for fic in [stdout, file]]

        [print("\n -normalisation", file=fic) for fic in [stdout, file]]
        [print(f"::: L{len(a) - 1} <- L{len(a) - 1} - ({a[len(a) - 1][len(a) - 1]})*L{len(a) - 1}", file=fic)
         for fic in [stdout, file]]
        a[-1] = a[-1] / a[-1][-2]
        [print(f"A : \n{a}", file=fic) for fic in [stdout, file]]

        [print("\nElimination des éléments de la partie triangulaire haut ", file=fic) for fic in [stdout, file]]
        for i in range(len(a))[::-1]:
            [print(f"\n -application", file=fic) for fic in [stdout, file]]

            for j in range(0, i):
                [print(f"ap[{j}][{i}]::: L{j} <- L{j} - ({a[j][i]})*L{i}", file=fic) for fic in [stdout, file]]
                a[j] = a[j] - a[j][i] * a[i]

            [print(f"A : \n{a}", file=fic) for fic in [stdout, file]]
        x = gauss_jordan_solution(a)
        [print(f"\nX : \n{x}", file=fic) for fic in [stdout, file]]
        return x


if __name__ == "__main__":
    systeme_dir()

    while input("Entrer pour recommencer...") == "":
        # ap = get_array()
        a = [[9, 4, 0, 0, 0, 8],
             [5, 8, 2, 0, 0, 7],
             [0, 2, 8, 5, 0, 9],
             [0, 0, 9, 4, 5, 5],
             [0, 0, 0, 1, 7, 6]]
        # ap = [[1, 1, 1, 1],
        #      [2, 2, 5, 2],
        #      [4, 6, 8, 5]]

        # ap = [[9, 4, 0, 0, 0, 8],
        #      [5, 8, 2, 0, 0, 7],
        #      [0, 2, 8, 5, 0, 9],
        #      [0, 0, 9, 4, 5, 5],
        #      [0, 0, 0, 1, 7, 6]]

        with open(f"{sys_file_path}/{sys_file_name()}", 'w') as file:
            file.write(f"A :\n {str(a)}")
            file.close()

        gauss_jordan(a)

# [[1, 1, 1, 1],
#  [2, 2, 5, 2],
#  [4, 6, 8, 5]]
