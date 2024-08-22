import numpy as np
from sys import stdout
from linear_system_assets import matrix_arrange, gauss_solution, get_array, systeme_dir, \
    sys_file_path, sys_file_name, float_matrix, column_swap


def gauss_pivot_partiel_sans_normalisation(matrix):
    a = np.array(float_matrix(matrix))
    print(a)
    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\n\t GAUSS AVEC PIVOT PARTIEL SANS NORMALISATION \n", file=fic) for fic in [stdout, file]]

        for i in range(len(a) - 1):
            [print(f"\npiviotage {i}", file=fic) for fic in [stdout, file]]
            a[i::, ::] = matrix_arrange(a[i::, ::], pivot_col=i)
            pivot_line = a[i]
            [print(f"A\n{a}", file=fic) for fic in [stdout, file]]

            [print(f"\nApplication : ", file=fic) for fic in [stdout, file]]
            for j in range(i + 1, len(a)):
                [print(f"::: L{j + 1} <- L{j + 1} - ({a[j][i]}/{pivot_line[i]})*L{i + 1}", file=fic) for fic in
                 [stdout, file]]
                if pivot_line[i] == 0:
                    [print(f"le pivot A[{i}][{i}] est null. La methode de gauss avec normalisation avec pivotage "
                           f"partiel w'est pas applicable", file=fic) for fic in [stdout, file]]
                    return
                a[j] = a[j] - a[j][i] * pivot_line / pivot_line[i]
                a[j][i] = 0

            [print(f"A \n{a}", file=fic) for fic in [stdout, file]]
        X = gauss_solution(a)
        [print(f"\nX = {X}", file=fic) for fic in [stdout, file]]
        return X


def gauss_pivot_partiel_avec_normalisation(matrix):
    a = np.array(float_matrix(matrix))
    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\t GAUSS AVEC PIVOT PARTIEL AVEC NORMALISATION \n", file=fic) for fic in [stdout, file]]

        for i in range(len(a) - 1):
            [print(f"\n -piviotage", file=fic) for fic in [stdout, file]]
            a[i::, ::] = matrix_arrange(a[i::, ::], i)
            pivot_line = a[i]
            [print(f"\nA \n{a}", file=fic) for fic in [stdout, file]]

            if a[i][i] == 0:
                [print("le pivot A[{x}][{x}] est null. La methode de gauss avec normalisation avec pivotage partiel "
                       "w'est pas applicable", file=fic) for fic in [stdout, file]]
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

        x = gauss_solution(a)
        [print(f"X = {x}", file=fic) for fic in [stdout, file]]
        file.close()
        return x


def gauss_pivot_total(matrix):
    a = np.array(float_matrix(matrix))
    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a') as file:
        [print("\n\t GAUSS AVEC PIVOT TOTAL AVEC NORMALISATION \n", file=fic) for fic in [stdout, file]]

        order = [i for i in range(len(a))]
        for i in range(len(a) - 1):
            [print(f"\n -piviotage ", file=fic) for fic in [stdout, file]]
            a[i::, ::] = matrix_arrange(a[i::, ::], i)
            pivot_line = a[i]
            [print(f"\nA \n{a}", file=fic) for fic in [stdout, file]]

            if a[i][i] == 0:
                a[:, :], order = column_swap(a, i, order, file)
                [print(f"\nA \n{a}", file=fic) for fic in [stdout, file]]

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

        x = gauss_solution(a)
        [print(f"X = {x}", file=fic) for fic in [stdout, file]]
        file.close()
        return x


if __name__ == "__main__":
    import warnings
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        systeme_dir()

        while input("\nEntrer pour commencer...") == "":
            a = get_array()

            with open(f"{sys_file_path}/{sys_file_name()}", 'w') as file:
                file.write(f"A :\n {str(a)}")
                file.close()

            G1 = gauss_pivot_partiel_sans_normalisation(a)
            G2 = gauss_pivot_partiel_avec_normalisation(a)
            G3 = gauss_pivot_total(a)

            print(f"\nGAUSS\n * pivot partiel : \n  - Sans normalisation : {G1}\n  - Avec normalisation : {G2}\n"
                  f" * pivot total : {G3}")
