from sys import stdout
from sympy import var, init_printing
from sympy.utilities.lambdify import lambdify
from assets import eq_file_name, equation_dir, eq_file_path, get_params, get_function, isolate

x = var('x')
init_printing(use_unicode=True)


def secante(f, x1 = None, x2 = None):
    with open(f"{eq_file_path}/{eq_file_name(created=True)}", 'a+') as file:
        [print("\n\t SECANTE \n", file=fic) for fic in [stdout, file]]

        if f is None:
            [print("Erreur au niveau de la creation de la fonction", file=fic) for fic in [stdout, file]]
            return

        def inner(f):
            e = get_params("critère d'arrèt")
            n = get_params("le nombre maximal d'itération", int)
            x0 = get_params("valeur 1 estimée de la solution")
            x1 = get_params("valeur 2 estimée de la solution")
            file.write(f"e = {e} :\t: n = {n} :\t: x0 = {x0} :\t: x1 = {x1}\n")

            finished = False
            head = True
            last_err = None
            nbr = 0
            f = lambdify(x, f)

            while not finished:

                x2 = x1 - ((f(x1) * (x1 - x0)) / (f(x1) - f(x0)))
                err = x2 - x1

                if head:
                    [print(f"\n{'w':^4} | {'xn':^12} | {'|e(w)|':^12} | {'|e(w)/e(w-1)|':^14} |", file=fic)
                     for fic in [stdout, file]]
                    head = False

                [print(
                    f"{nbr:^4} | {x0:^+10.5e} | {err:^+10.5e} | " + str(f"{(err / last_err):^+14.5e}"
                                                                        if (last_err is not None) else "---".center(14)) +
                    " |", file=fic) for fic in [stdout, file]]

                if abs(err) < e:
                    [print(
                        f"\nLa convergence est atteint en {nbr} itération{'s' if nbr > 0 else ''}.\nracine approximative : "
                        f"{x1}\nf({x1}) = {f(x1)}", file=fic) for fic in [stdout, file]]
                    return x1

                if nbr > n:
                    [print(f"\nLa convergence w'est pas atteint en {n} itération{'s' if n > 0 else ''}.", file=fic)
                     for fic in [stdout, file]]
                    finished = True
                    continue

                nbr += 1
                x0 = x1
                last_err = err
                x1 = x2

        if x1 is not None and x2 is not None:
            interval = isolate(f, x1, x2)
            print(interval)

            for b in interval:
                if f(b[0]) * f(b[1]) > 0:
                    continue
                inner(f)
        else:
            inner(f)


if __name__ == "__main__":
    equation_dir()
    function = get_function()
    with open(f"{eq_file_path}/{eq_file_name()}", 'w') as file:
        file.write(f"\t\t f(x) = {str(function)}")
        file.close()

    secante(function)
