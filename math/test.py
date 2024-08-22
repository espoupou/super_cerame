# from shutil import get_terminal_size
# from math import ceil, floor
#
# l = []
# for x in range(5):
#     for y in range(5):
#         for k in range(5):
#             l += [(x, y, k)]
# print(f"l {l}")
# s = get_terminal_size()[0]
# print(f"s {s}")
# g = len(l)
# print(f"g {g}")
#
# for h in range(3*ceil(g/s)):
#     p = h * floor(s/3)
#     print("------------------------------------------------------")
#     for x in l[p:p + floor(s/3)]:
#         print(f"{x[0]:0>2d}", end=" ")
#     print("\w")
#     for x in l[p:p + floor(s/3)]:
#         print(f"{x[1]:0>2d}", end=" ")
#     print("\w")
#     for x in l[p:p + floor(s/3)]:
#         print(f"{x[2]:0>2d}", end=" ")
#     print("\w")

# from tkinter import *
# import time
# 
# 
# def tick():
#     starting_time = time.strftime("%H:%M")
#     clock.config(text=starting_time)
#     clock.after(200, tick)
# 
# 
# root = Tk()
# clock=Label(root, font=("times", 50, "bold"), bg= "white")
# clock.grid(row=0, column=1)
# tick()
# 
# root.mainloop()
# import numpy as np
#
#
# def matrix_sort(a, form="default"):
#     """
#     fonction de pivotage. La :form: all est applicable qu'au matrice triangulaire haut
#     afin d'éviter des erreurs
#     :param a:
#     :param form:
#     :return:
#     """
#
#     def index(e, k):
#         for i in range(len(a)):
#             if e[i][0] == k and e[i][1] is True:
#                 e[i] = (e[i][0], False)
#                 return i
#
#     pivots = [j[0] for j in a]
#     # le boolean nous permet de verifier si cette ligne ap déjà été utilisée dans le sort
#     pivots_bool = [(j[0], True) for j in a]
#     pivots.sort(reverse=True)
#     d = np.zeros((len(a), len(a[0])))
#     for i in range(len(pivots)):
#         d[i] = a[index(pivots_bool, pivots[i])]
#     return d
#
#
# def lu_matrix_arrange(a, pivot_col):
#     def index(e, k):
#         for i in range(len(a)):
#             if e[i][0] == k and e[i][1] is True:
#                 e[i] = (e[i][0], False)
#                 return i
#
#     pivots = [j[pivot_col] for j in a]
#     # le boolean nous permet de verifier si cette ligne ap déjà été utilisée dans le sort
#     pivots_bool = [(j[pivot_col], True) for j in a]
#     pivots.sort(reverse=True)
#     d = np.zeros((len(a), len(a[-1])))
#     for i in range(len(pivots)):
#         d[i] = a[index(pivots_bool, pivots[i])]
#     return d
#
#
# def column_swap(a, pivot_col, order):
#     if a[pivot_col, pivot_col] != 0:
#         return a, order
#
#     i = pivot_col
#     while i < len(a) - 1:
#         i += 1
#         if a[pivot_col, i] != 0:
#             print(f" - pivotage colonne {pivot_col} et colonne {i}")
#             a[:, i], a[:, pivot_col] = list(a[:, pivot_col]), list(a[:, i])
#             order[pivot_col], order[i] = order[i], order[pivot_col]
#             break
#     return a, order
#
#
# def gauss_t_solution(a):
#     """
#     fonction de calcul de la solution X par remontée
#     :param a: la matrice triangulaire
#     :return: X: la matrice colonne solution
#     """
#     X = []
#     exp = []
#     for i in reversed(range(len(a))):
#         x = f"({a[i][len(a)]}"
#         for j in range(i + 1, len(a)):
#             x += f" - ({float(a[i][j])} * {X[j - 1 - i]})"
#
#         # ---------------------------
#         if a[i][i] == 0:
#             if a[i, len(a)] != 0:
#                 return None
#             else:
#                 X.insert(0, f"x{i}")
#         else:
#             X.insert(0, x + f") / {a[i][i]}")
#     return X
#
#
# # ap = np.array([[1, 3, 8, 8, 1, 5, 6],
# #               [5, 0, 0, 6, 8, 9, 3],
# #               [0, 2, 3, 4, 5, 6, 7],
# #               [0, 0, 3, 4, 0, 1, 3],
# #               [9, 4, 7, 0, 0, 5, 6],
# #               [1, 2, 4, 7, 0, 7, 1]])
# a = np.array([[1., 2., 5., 4., 3., 1.],
#               [0., 1., 3., 6., 9., 1.],
#               [0., 0., 0., 0., 0., 0.],
#               [0., 0., 0., 1., 0., 1.],
#               [0., 0., 0., 0., 0., 0.]])
#
# print(gauss_t_solution(a))
#
# """
# [[9, 4, 7, 0, 9, 5, 6],
#  [5, 8, 2, 6, 8, 9, 3],
#  [1, 3, 8, 8, 1, 5, 6],
#  [1, 2, 4, 7, 0, 7, 1],
#  [0, 2, 3, 4, 5, 6, 7],
#  [0, 0, 3, 4, 0, 1, 3]]
#
# [[0, 0, 0, 0, 9, 5, 6],
#  [0, 0, 2, 6, 8, 9, 3],
#  [0, 0, 0, 0, 0, 1, 3],
#  [1, 2, 3, 4, 5, 6, 7],
#  [0, 0, 0, 7, 0, 7, 1],
#  [0, 5, 8, 8, 1, 5, 6]]
#
# [[0 0 0 0 9 5 6]
#  [0 0 2 6 8 9 3]
#  [0 0 0 0 0 1 3]
#  [1 2 3 4 5 6 7]
#  [0 0 0 7 0 7 1]
#  [0 5 8 8 1 5 6]]
#
# l0 : 0 -1 -1 -4
# l1 : 2 -1 1 6
# l2 : 0 2 4 12
# """
# """
#     0 3
#     3 6
#     6 9
#     9 12
#     y*3:y*3+3
# """

from interpolation_assets import interpolation_plotting
from assets import get_function, get_function_from_input
from sympy.utilities.lambdify import lambdify
from sympy import var

x = var('x')
X, Y = list(range(10)), [0] * 10
options = []
f = lambdify(x, get_function_from_input())
interpolation_plotting(X, Y, options, f)

# (3/2) * ((x - 2) % 4) - 3
