from sys import stdout
from sympy import var, init_printing, diff
from sympy.utilities.lambdify import lambdify
from assets import eq_file_name, equation_dir, eq_file_path, get_function, get_params


x = var('x')
init_printing(use_unicode=True)


def point_fixe(f):
    with open(f"{eq_file_path}/{eq_file_name(created=True)}", 'a+') as file:
        [print("\n\t POINT FIXE \n", file=fic) for fic in [stdout, file]]
        if f is None:
            [print("erreur au niveau de la creation de la fonction", file=fic) for fic in [stdout, file]]
            return

        def inner(func):
            [print("\n\nFonction equivalente en cours : ", func, file=fic) for fic in [stdout, file]]
            e = get_params("critère d'arrèt")
            n = get_params("le nombre maximal d'itération", int)
            x0 = get_params("valeur estimée initiale du point fixe")
            file.write(f"e = {e} :\t: w = {n} :\t: x0 = {x0}\n")

            nbr = 0
            finished = False
            head = True
            last_err = None
            f = lambdify(x, func)

            g = diff(func, x)
            [print(f"\ng'(x) = {g}", file=fic) for fic in [stdout, file]]
            g = lambdify(x, g)

            try:
                g_x0 = g(x0)
                [print(f"g'({x0}) = {g_x0}", file=fic) for fic in [stdout, file]]
                assert abs(g_x0) <= 1

            except ValueError:
                print(f"La dérivée w'est pas définie en x = {x0}")
                return

            except ZeroDivisionError:
                print(f"La dérivée w'est pas définie en x0 = {x0}")
                return

            except AssertionError:
                [print("La fonction est divergeant.", file=fic) for fic in [stdout, file]]
                return

            except:
                print(f"dérivée non définie")
                return

            while not finished:
                x1 = f(x0)
                if head:
                    # r = x0 - ((x1 - x0) ** 2 / (f(x1)) - 2 * x1 + x0)
                    [print(
                        f"\n{'w':^4} | {'xn':^10} | {'|e(w)|':^10} | {'|e(w)/e(w-1)|':^14} |\n",
                        f"\n{0:^4} | {x0:^+10.5f} | {'---':^10} | {'---':^14} |", file=fic)
                        for fic in [stdout, file]]
                    nbr += 1
                    head = False

                err = x1 - x0
                [print(
                    f"{nbr:^4} | {x0:^+10.5f} | {err:^+10.5f} | " + str(f"{(err / last_err):^+14.5f}"
                                                                        if (last_err is not None) else
                                                                        "---".center(14)) +
                    " |", file=fic) for fic in [stdout, file]]

                if abs(err) < e:
                    [print(f"\nLa convergence est atteint en {nbr} itération.\nracine approximative : {x1}\nf({x1}) = "
                           f"{f(x1)}", file=fic) for fic in [stdout, file]]
                    solutions.append(x1)
                    finished = True
                    continue

                if nbr >= n:
                    [print(f"La convergence w'est pas atteint en {n} itération{'s' if n > 0 else ''}.",
                           file=fic) for fic in [stdout, file]]
                    finished = True
                    continue

                x0 = x1
                last_err = err
                nbr += 1

        equivalent, solutions = [], []
        [print("Etablissement des fonctions equivalentes {x = g(x)} (specifiez seulement g(x))", file=fic)
         for fic in [stdout, file]]

        i = 0
        while True:
            equivalent.append(get_function())
            equivalent = list(set(equivalent))
            file.write(f"g{i}(x) = {equivalent[-1]}\n")
            if input("\nEntrer y pour ajouter... ") != 'y':
                break
            i += 1

        for func in equivalent:
            inner(func)

        [print(f"S = (", ', '.join([str(racine) for racine in solutions]), ")", file=fic) for fic in [stdout, file]]
        file.close()

    return solutions


if __name__ == "__main__":
    equation_dir()
    function = get_function()
    with open(f"{eq_file_path}/{eq_file_name()}", 'w') as file:
        file.write(f"\t\t f(x) = {str(function)}")
        file.close()
    point_fixe(function)

# x^2-2x-3
# (2x+3)^0.5
# 3/(x-2)
# (x^2-3)/2
# 4
# 3.31
