import numpy as np
from sys import stdout
from os import getcwd, mkdir


# ==========================================================
sys_file_path = f"{getcwd()}/systeme_lineaire"


# ======= SYSTEME LINEAIRE =========================================
def systeme_dir():

    try:
        mkdir("./systeme_lineaire")
    except FileExistsError:
        pass


def get_array():
    a, line = [], []
    print("Entrer les coefficients a[x, y] des inconnues suivi par la valeur b[x] séparés par des espaces")
    n = 1
    i = 0
    while i < n:
        print(f"l{i} : ", end='')
        while True:
            try:
                line = list(map(float, input().split(' ')))
                if i == 0:
                    n = len(line) - 1
                assert len(line) == n + 1
                a.append(line)
                break
            except ValueError:
                print("Les valeurs ne sont pas corrects")
            except AssertionError:
                print(f"le nombre d'éléments entrés ({len(line)}) est different de la taille definie ({n + 1})")
            print("ressaisissez la ligne : ", end='')
        i += 1
    return a


def matrix_dominant(a):
    for i in range(len(a)):
        if a[i][i] < sum(a[i][:i:]) + sum(a[i][i+1::]):
            return False
    return True


def sys_file_name(created=False):
    systeme_dir()

    # --------------------------------------------
    def create_name():
        i = 0
        while True:
            try:
                open(f"matrice{i}.sys", 'r').close()

            except FileNotFoundError:
                if not created:
                    with open(f"{sys_file_path}/num.txt", 'w') as file:
                        file.write(f"{i}")
                        file.close()
                return f"matrice{i}.sys" if not created else f"matrice{i-1}.sys"
            i += 1

    # --------------------------------------------
    try:
        with open(f"{sys_file_path}/num.txt", 'r') as file:
            i = int(file.read()) + 1
            file.close()

        if not created:
            with open(f"{sys_file_path}/num.txt", 'w') as file:
                file.write(str(i))
                file.close()
        return f"matrice{i}.sys" if not created else f"matrice{i-1}.sys"

    except FileNotFoundError:
        return create_name()
    except ValueError:
        return create_name()


def float_matrix(a):
    for i in range(len(a)):
        for j in range(len(a) + 1):
            a[i][j] = float(a[i][j])
    return a


def is_positive_define(A):
    if np.array_equal(A, A.T):
        try:
            np.linalg.cholesky(A)
            return True
        except np.linalg.LinAlgError:
            return False
    else:
        return False


# ==============================GAUSS=====================
def gauss_solution(a):
    """
    fonction de calcul de la solution X par remontée
    :param a: la matrice triangulaire
    :return: X: la matrice colonne solution
    """
    X = []
    for i in reversed(range(len(a))):
        x = a[i][len(a)]
        for j in range(i + 1, len(a)):
            x -= float(a[i][j]) * X[j - 1 - i]
        # ---------------------------
        if a[i][i] == 0:
            if a[i, len(a)] == 0:
                print("Infi")
        # ---------------------------
        X.insert(0, x / a[i][i])
    return X


def gauss_t_solution(a):
    """
    fonction de calcul de la solution X par remontée
    :param a: la matrice triangulaire
    :return: X: la matrice colonne solution
    """
    X = []
    for i in reversed(range(len(a))):
        x = a[i][len(a)]
        for j in range(i + 1, len(a)):
            x -= float(a[i][j]) * X[j - 1 - i]
        # ---------------------------
        if a[i][i] == 0:
            if a[i, len(a)] == 0:
                print("Infi")
        # ---------------------------
        X.insert(0, x / a[i][i])
    return X


def gauss_jordan_solution(a):
    """
    fonction de calcul de la solution X de gauss Jordan
    :param a: la matrice diagonale
    :return: X: la matrice colonne solution
    """
    X = []
    for i in range(len(a)):
        X.append(a[i][len(a)] / a[i][i])
    return X


# ==========================LU==================================
def y_solution(L):
    Y = []
    for i in range(len(L)):
        x = L[i][len(L)]
        for j in range(i):
            x -= float(L[i][j] * Y[j])
        if L[i][i] == 0:
            return None
        Y.append(x / L[i][i])
    return Y


def lu_sum(i, j, stop, L, U):
    somme = 0.0
    for k in range(stop):
        print(f" - L[{i}][{k}] * U[{k}][{j}]", end='')
        somme += L[i][k] * U[k][j]
    return somme


def matrix_arrange(a, pivot_col):
    def index(e, k):
        for i in range(len(a)):
            if e[i][0] == k and e[i][1] is True:
                e[i] = (e[i][0], False)
                return i

    pivots = [j[pivot_col] for j in a]
    # le boolean nous permet de verifier si cette ligne ap déjà été utilisée dans le sort
    pivots_bool = [(j[pivot_col], True) for j in a]
    pivots.sort(reverse=True)
    d = np.zeros((len(a), len(a[-1])))
    for i in range(len(pivots)):
        d[i] = a[index(pivots_bool, pivots[i])]
    return d


def column_swap(a, pivot_col, order, file):
    if a[pivot_col, pivot_col] != 0:
        return a, order

    i = pivot_col
    while i < len(a) - 1:
        i += 1
        if a[pivot_col, i] != 0:
            [print(f"\n - pivotage colonne {pivot_col} et colonne {i}", file=fic) for fic in [stdout, file]]
            a[:, i], a[:, pivot_col] = list(a[:, pivot_col]), list(a[:, i])
            order[pivot_col], order[i] = order[i], order[pivot_col]
            break
    return a, order


# ======================= CROUT ==============================
def crout_solution(L, U, n):
    pass


# ===================== DOOLITTLE ============================
def lu_doolittle_sum():
    pass


# ===================== CHOLEVSKY =============================
def line_sum(i, stop, L):
    result = 0
    for k in range(i):
        print(f" - L[{i}][{k}]^2", end='')
        result += L[i][k]**2
    return result


# ===================== INDIRECT =============================
def get_x_0(lenght):
    X = []
    while True:
        try:
            X = list(map(float, input('entrer X0 (valeur séparée par espace) : ').split(' ')))
            if not X:
                return
            assert len(X) == lenght
            return X
        except ValueError:
            if not X:
                return None
            print("Entrer des nombres entiers")
        except AssertionError:
            print(f"le nombre d'élément{'s' if len(X) else ''} de X ({len(X)}) est "
                  f"{'supérieur' if len(X) > lenght else 'inférieur'} ap la taille de la matrice {lenght}")


# ====================== JACOUBI ==============================
def jacobi_sum(line, X, i, model_only=False):
    somme = 0
    for j in range(len(line) - 1):
        if model_only and i != j:
            print(f" - ({line[j]} * X[{j}])", end='')
        elif i != j:
            somme += line[j] * X[j]
    return somme


# ====================== THOMAS ============================
def is_tridiagonal(a):
    if len(a) < 3:
        return True
    if not a[0, 2:].all():
        if not a[-1, :-2].all():
            for i in range(1, len(a[1:-2]) + 1):
                line = list(a[i, :i-1]) + list(a[i, i + 2:])
                if line != [0] * len(line):
                    return False
            return True
    return False


"""
1 2 3 4 5 6 7
4 5 6 7 8 9 0
2 3 4 5 6 7 8
0 1 2 3 4 5 6
9 0 1 2 3 4 5
7 8 9 0 1 2 3
"""
"""

"""
