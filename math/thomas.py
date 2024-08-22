import numpy as np
from sys import stdout
from linear_system_assets import (is_tridiagonal, float_matrix, sys_file_path, sys_file_name, systeme_dir,
                                  get_array)


def thomas(matrix):
    a = np.array(float_matrix(matrix))

    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a+') as file:
        [print("\n\t THOMAS \n", file=fic) for fic in [stdout, file]]
        if not is_tridiagonal(a[:, :-1]):
            [print("la matrice w'est pas tridiagonal. la méthode de Thomas w'est pas applicable", file=fic)
             for fic in [stdout, file]]
            return

        # liste des valeurs à utiliser
        a_, b_, c_, d_ = [], [], [], []
        for i in range(len(a)):
            if i > 0:
                a_.append(a[i, i - 1])
            b_.append(a[i, i])
            if i < len(a) - 1:
                c_.append(a[i, i + 1])
        a_.insert(0, 0)
        c_.append(0)
        d_ = list(a[:, len(a)])

        [print(f"A = {a_}", f"B = {b_}", f"C = {c_}", f"D = {d_}", sep='\n', file=fic) for fic in [stdout, file]]

        #

        if 0 in b_:
            [print(f"\nB[{b_.index(0)}] est null", file=fic) for fic in [stdout, file]]
            return
        for i in range(1, len(a)):
            w = a_[i] / b_[i - 1]

            b_[i] = b_[i] - w * c_[i - 1]
            d_[i] = d_[i] - w * d_[i - 1]

        # solution

        X = [d_[len(a) - 1] / b_[len(a) - 1]]
        for i in range(len(a) - 2, -1, -1):
            X.insert(0, ((d_[i] - c_[i] * X[0]) / (b_[i])))
        [print(f"\nX = {X}", file=fic) for fic in [stdout, file]]
        return X


if __name__ == '__main__':
    systeme_dir()
    re = False
    while input(f"Entrer pour {'re' if re else ''}commencer...") == "":
        re = True
        a = get_array()
    
        with open(f"{sys_file_path}/{sys_file_name()}", 'w') as file:
            file.write(f"A :\n {str(a)}")
            file.close()
        
        thomas(a)
