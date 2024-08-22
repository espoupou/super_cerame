import warnings
from time import sleep
from sys import stdout, modules
from sympy import var, init_printing
from sympy.utilities.lambdify import lambdify
from lagrange import lagrange
from moindres_carres import moindres_carres
from newton_interpolation import newton_interpolation
from interpolation_assets import (get_points, interpolation_dir, interpolation_file_name, interpolation_file_path,
                                  interpolation_plotting)
from assets import get_function, equation_dir, eq_file_path, eq_file_name
from linear_system_assets import get_array, systeme_dir, get_x_0, sys_file_path, sys_file_name


def equation_non_linearire():
    # ----------%Setting%-----------
    equation_dir()
    print("Le nom de variable dans les fonctions est 'x'")

    # ----------%modules%-----------
    from newton import newton
    from secante import secante
    from bissection import bissection
    from point_fixe import point_fixe

    # ------------%main%------------
    f = get_function()
    with open(f"{eq_file_path}/{eq_file_name()}", 'w') as file:
        file.write(f"\t\t f(x) = {str(f)}\n")
        file.close()

    methodes = [bissection,
                point_fixe,
                newton,
                secante]
    result = [
        methode(f) for methode in methodes
    ]


def systeme_lineaire():
    from thomas import thomas
    from gauss_jordan import gauss_jordan
    from LU import lu_decomposition_crout, lu_decomposition_doolittle, lu_decomposition_cholesky
    from gauss import gauss_pivot_partiel_avec_normalisation, gauss_pivot_partiel_sans_normalisation

    a = get_array()
    x0 = get_x_0(len(a))
    systeme_dir()

    with open(f"{sys_file_path}/{sys_file_name()}", 'w') as file:
        file.write(f"\t\t A :\n{str(a)}\n")

        [print("Methodes directes", file=fic) for fic in [stdout, file]]
        file.close()

    direct = {
        methode.__name__: methode(a) for methode in [gauss_pivot_partiel_avec_normalisation,
                                                     gauss_pivot_partiel_sans_normalisation,
                                                     gauss_jordan,
                                                     lu_decomposition_crout,
                                                     lu_decomposition_doolittle,
                                                     lu_decomposition_cholesky,
                                                     thomas
                                                     ]
    }
    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a+') as file:
        [print("\n--- RESULTAT METHODE DIRECTE ---\n", file=fic) for fic in [stdout, file]]
        for name, result in direct.items():
            [print(f"{' '.join(name.split('_'))} : {result}", file=fic) for fic in [stdout, file]]

        [print(f"\nMéthode indirect\n X0 = {x0}", file=fic) for fic in [stdout, file]]
        file.close()

    sleep(10)

    from jacobi import jacobi
    from gauss_seidel import gauss_seidel
    indirect = {
        methode.__name__: methode(a, x0) if x0 is not None else methode(a) for methode in [jacobi,
                                                                                           gauss_seidel
                                                                                           ]
    }

    with open(f"{sys_file_path}/{sys_file_name(created=True)}", 'a+') as file:
        [print("\n--- RESULTAT METHODE DIRECTE ---\n", file=fic) for fic in [stdout, file]]
        for name, result in direct.items():
            [print(f"{(' '.join(name.split('_'))).capitalize()} : {result}", file=fic) for fic in [stdout, file]]

        [print("\n--- RESULTAT METHODE INDIRECTE ---\n", file=fic) for fic in [stdout, file]]
        for name, result in indirect.items():
            [print(f"{(' '.join(name.split('_'))).capitalize()} : {result}", file=fic) for fic in [stdout, file]]

        file.close()


def interpolation():
    # ----------%modules%-----------

    # -----------%directory%----------
    interpolation_dir()

    print("kkk")
    # X, Y = get_points()
    # X, Y = [2, 3, -1, 4], [1, -1, 2, 3]
    X = [0.0, 10.0, 25.0, 37.0, 48.0, 65.0, 73.0, 80.0]
    Y = [1.66, 1.65, 1.64, 1.63, 1.63, 1.615, 1.61, 1.605]
    f = None

    if input("\ny pour ajouter la fonction exacte... ") == 'y':
        f = lambdify(x, get_function())

    with open(f"{interpolation_file_path}/{interpolation_file_name()}", 'w') as file:
        file.write(f"X = {X}\t Y = {Y}")
        file.close()
    options = [
        methode(X, Y) for methode in [lagrange,
                                      newton_interpolation,
                                      moindres_carres
                                      ]
    ]

    interpolation_plotting(X, Y, options, f)


def equation_differentielle():
    from euler import euler
    from assets import get_params
    from runge_kunta import runge_kunta
    from equa_diff_assets import equa_diff_plotting, ed_get_function, equa_diff_file_path, equa_diff_file_name

    f = ed_get_function()
    t0 = get_params("t0")
    y0 = get_params("y0")
    h = get_params("h")
    b = get_params("la borne superieur")
    f_ = None
    if input("\ny pour ajouter la fonction exacte... ") == 'y':
        f_ = lambdify(x, get_function())

    with open(f"{equa_diff_file_path}/{equa_diff_file_name()}", 'w') as file:
        file.write(f"f(x) = {f}\n\nt0 = {t0} | y0 = {y0} | h = {h} | borne = {b}")
        file.close()

    options = [
        methode(f, t0, y0, h, b) for methode in [euler,
                                                 runge_kunta
                                                 ]
    ]
    equa_diff_plotting(options, t0, b, f_)


# ----------%Setting%-----------

# ---------%directory%----------
systeme_dir()

# ---------%definition%---------
x = var('x')
init_printing(use_unicode=True)

# ------------%main%------------
running = True

while running:
    menu = ("Methodes : "
            "\n 1 : equation non lineaire"
            "\n 2 : systeme lineaire"
            "\n 3 : interpolation"
            "\n 4 : equation différentielle"
            )
    print(menu)
    choix = 0
    try:
        choix = int(input("Choix : "))
        assert 1 <= choix <= menu.count('\n')
    except ValueError:
        correct = False
        while not correct:
            try:
                choix = int(input("choix incorrect. réessayer : "))
                assert 1 <= choix <= menu.count('\n')
                correct = True
            except ValueError:
                pass
            except AssertionError:
                pass
    except AssertionError:
        correct = False
        while not correct:
            try:
                choix = int(input("choix incorrect. réessayer : "))
                assert 1 <= choix <= menu.count('\n')
                correct = True
            except ValueError:
                pass
            except AssertionError:
                pass
    try:
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            [equation_non_linearire, systeme_lineaire, interpolation, equation_differentielle][choix - 1]()
    except ValueError as e:
        print("Erreur de valeur rencontrée", e)
    except ZeroDivisionError:
        print("Division par zero rencontrée")
    except FileExistsError:
        print("Le fichier d'enregistrement ne peut pas être écrasé")
    except FileNotFoundError:
        print("Le fichier d'enregistrement n'est pas trouvé")
    except:
        print("Erreur au cours de l'execution")

    if input("\nEntrer y pour recommencer... ") != 'y':
        running = False
