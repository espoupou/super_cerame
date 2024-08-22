from sys import stdout
from assets import get_params, get_function
from sympy import var, init_printing
from sympy.utilities.lambdify import lambdify
from equa_diff_assets import (ed_get_function, equa_diff_file_path, equa_diff_file_name, equa_diff_dir,
                              equa_diff_plotting)


x, y, t = var('x y t')
init_printing(use_unicode=True)


def euler(f, t0, y0, h, b):
    with open(f"{equa_diff_file_path}/{equa_diff_file_name(created=True)}", 'a+') as file:
        [print("\n\n\t EQUATION DIFFERENTIELLE : EULER \n", file=fic) for fic in [stdout, file]]

        Y, T = [y0], [t0]
        n = 0
        finished = False
        head = True
        t_i = t0 + h

        print(f"Yn+1 = Yn + {h} * f(t, Yn)")
        while not finished:
            if head:
                print(f"| {'w':^3} | {'Yn':^10} | {'tn':^10} | {'f(tn, Yn)':^10} | {'h':^9} | {'ΔY':^10} | {'Yn+1':^10} |")
                head = False
            T.append(t_i)
            f_t = f.subs({y: Y[-1], t: t_i})
            Y.append(Y[-1] + h*f_t)
            print(f"| {n:^3} | {Y[-2]:^+10.2e} | {t_i:^+10.2e} | {f_t:^+10.2e} | {h:^+3.2e} | {abs(Y[-1] - Y[-2]):^+10.2e} "
                  f"| {Y[-1]:^+10.2e} |")
            if t_i >= b:
                finished = True
                continue
            t_i += h
            n += 1

        print(T)
        print(Y)
        return {'T': T, 'Y': Y, 'name': "euler", 'color': "green"}


if __name__ == '__main__':

    import warnings

    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        equa_diff_dir()
        first = True
        while first if first else input("Entrer pour recommencer...") == "":
            first = False
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

            result = euler(f, t0, y0, h, b)
            equa_diff_plotting([result], t0, b, f_)

# 2 - 2y - exp(-4t)
# t^2- 2t - 2y + 3
