from time import sleep
from sys import stdout
from sympy import var, init_printing
from sympy.utilities.lambdify import lambdify
from assets import eq_file_path, get_params, isolate, get_function, equation_dir, eq_file_name

x = var('x')
init_printing(use_unicode=True)


def bissection(f):
    with open(f"{eq_file_path}/{eq_file_name(created=True)}", 'a') as file:
        [print("\n\t BISSECTION \n", file=fic) for fic in [stdout, file]]

        if f is None:
            [print("Erreur au niveau de la creation de la fonction", file=fic) for fic in [stdout, file]]
            return

        def inner(X1, X2):

            n = get_params("le nombre maximal d'itération", int)
            file.write(f"e = {e} :\t: n = {n} :\n")

            nbr = 0
            finished = False
            head = True

            while not finished:
                if f(x1) == 0:
                    [print(
                        f"\nLa convergence est atteint en {nbr} itération.\nracine approximative dans l'intervalle :"
                        f" [{b[0]}, {b[1]}] : {x1}\nf({x1}) = {f(x1)} ", file=fic) for fic in [stdout, file]]
                    racines.append(x1)
                    return
                nbr += 1
                xm = (X1 + X2) / 2
                xm = xm + float("10e-10") if xm == 0 else xm
                erreur = abs(X2 - X1) / 2  # (2 * abs(xm))

                if f(X1) * f(X2) > 0:
                    [print("pas de solution dans l'interval", file=fic) for fic in [stdout, file]]
                    return

                if head:
                    [print(
                        f"{'x1'.center(10)} | {'x2'.center(10)} | {'xm'.center(10)} | {'f(x1)'.center(10)} | "
                        f"{'f(x2)'.center(10)} | {'f(xm)'.center(10)} | {'err abs'.center(14)}", file=fic)
                        for fic in [stdout, file]]
                    head = False

                [print(
                    f"{X1:+10.5f} | {X2:+10.5f} | {xm:+10.5f} | {f(X1):+10.5f} | {f(X2):+10.5f} | {f(xm):+10.5f} | "
                    f"{erreur:+10.2e}", file=fic) for fic in [stdout, file]]

                if erreur <= e or f(xm) == 0:
                    [print(
                        f"\nLa convergence est atteint en {nbr} itération.\nracine approximative dans l'intervalle :"
                        f" [{b[0]}, {b[1]}] : {xm}\nf({xm}) = {f(xm)} ", file=fic) for fic in [stdout, file]]
                    racines.append(xm)
                    finished = True
                    continue

                if f(X1) * f(xm) < 0:
                    X2 = xm
                elif f(xm) * f(X2) < 0:
                    X1 = xm

                if nbr >= n:
                    [print(
                        f"\nLa convergence n'est pas atteint en {n} itération{'s' if n > 1 else ''}.",
                        file=fic) for fic in [stdout, file]]
                    finished = True
                    continue

        f = lambdify(x, f)
        x1 = get_params("la borne inferieur")
        x2 = get_params("la borne superieur")
        e = get_params("critère d'arrèt")
        racines = []

        interval = isolate(f, x1, x2)
        print(f"\nintervalle{'s' if len(interval) > 1 else '' } de solutions {interval}")

        for b in interval:
            if f(b[0]) * f(b[1]) > 0:
                continue
            [print(f"\nintervalle : [{b[0]}, {b[1]}]", file=fic) for fic in [stdout, file]]
            inner(*b)
            [print("\n", file=fic) for fic in [stdout, file]]

        [print(f"S = (", ', '.join([str(racine) for racine in racines]), ")", file=fic) for fic in [stdout, file]]
        file.close()
    sleep(1)
    return racines


if __name__ == "__main__":
    equation_dir()
    begin = True
    while True if begin else input("Entrer pour recommencer...") == "":
        
        function = get_function()
        with open(f"{eq_file_path}/{eq_file_name()}", 'w') as file:
            file.write(f"\t\t f(x) = {str(function)}")
            file.close()

        bissection(function)
