from sys import stdout
from sympy import var, init_printing, diff
from sympy.utilities.lambdify import lambdify
from assets import eq_file_name, equation_dir, eq_file_path, get_params, get_function


x = var('x')
init_printing(use_unicode=True)


def newton(f):
    with open(f"{eq_file_path}/{eq_file_name(created=True)}", 'a+') as file:
        [print("\n\t NEWTON \n", file=fic) for fic in [stdout, file]]
        if f is None:
            [print("erreur au niveau de la creation de la fonction", file=fic) for fic in [stdout, file]]
            return

        e = get_params("critère d'arrèt")
        n = get_params("le nombre maximal d'itération", int)
        x0 = get_params("valeur estimée initiale de la solution")
        file.write(f"e = {e} :\t: w = {n} :\t: x0 = {x0}\n")

        nbr = 0
        finished = False
        head = True
        last_err = None

        der = diff(f, x)
        [print(f"f'(x) = {der}", file=fic) for fic in [stdout, file]]

        der = lambdify(x, der)
        f = lambdify(x, f)
        while not finished:
            der_x0 = der(x0)
            if der_x0 == 0:
                [print(f"La derivée est null en {x0}.", file=fic) for fic in [stdout, file]]
                return

            x1 = x0 - (f(x0) / der_x0)
            err = abs(x1 - x0)

            if head:
                [print(f"{'w':^4} | {'xn':^12} | {'|e(w)|':^12} | {'|e(w)/e(w-1)|':^14} |", file=fic)
                 for fic in [stdout, file]]
                head = False

            [print(
                f"{nbr:^4} | {x0:^+10.5e} | {err:^+10.5e} | " + str(f"{(err / last_err):^+14.5e}"
                                                                    if (last_err is not None) else "---".center(14)) +
                " |", file=fic) for fic in [stdout, file]]

            if abs(err) < e or f(x1) == 0:
                [print(f"\nLa convergence est atteint en {nbr} itération.\nracine approximative : "
                       f"{x1}\nf({x1}) = {f(x1)}", file=fic) for fic in [stdout, file]]
                finished = True
                continue

            if nbr >= n:
                [print(f"\nLa convergence w'est pas atteint en {n} itération{'s' if n > 0 else ''}.", file=fic)
                 for fic in [stdout, file]]
                finished = True
                continue

            nbr += 1
            last_err = err
            x0 = x1

        file.close()
        print(f"\nS = ({x1})")
        return x1


if __name__ == "__main__":
    equation_dir()
    function = get_function()
    with open(f"{eq_file_path}/{eq_file_name()}", 'w') as file:
        file.write(f"\t\t f(x) = {str(function)}")
        file.close()

    newton(function)
