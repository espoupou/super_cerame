from sys import stdout
from assets import get_params, get_function
from sympy import var, init_printing
from sympy.utilities.lambdify import lambdify
from equa_diff_assets import (ed_get_function, equa_diff_file_name, equa_diff_file_path, equa_diff_dir,
                              equa_diff_plotting)

x, y, t = var('x y t')
init_printing(use_unicode=True)


def runge_kunta(f, t0, y0, h, b):
    with open(f"{equa_diff_file_path}/{equa_diff_file_name(created=True)}", 'a+') as file:
        [print("\n\n\t EQUATION DIFFERENTIELLE : RUNGE KUTTA \n", file=fic) for fic in [stdout, file]]

        Y, T = [y0], [t0]
        n = 0
        t_i = t0
        finished = False
        head = True

        [print(f"Yn+1 = Yn + {h} * f(tn + (h / 2), Yn + (h/2) * f(tn, Yn)", file=fic) for fic in [stdout, file]]
        while not finished:
            if head:
                [print(f"| {'w':^3} | {'Yn':^10} | {'tn':^10} | {'f(tn, Yn)':^10} | {'h':^9} | {'Y':^10} |"
                       f" {'Yn+1':^10} |", file=fic) for fic in [stdout, file]]
                head = False

            T.append(t_i)
            f_demi = f.subs({t: T[-1], y: Y[-1]})
            y_demi = Y[-1] + (h / 2) * f_demi

            f_t = f.subs({t: T[-1] + (h / 2), y: y_demi})
            Y.append(Y[-1] + h * f_t)

            [print(f"| {n:^3} | {Y[-2]:^+10.2e} | {t_i:^+10.2e} | {f_t:^+10.2e} | {h:^+3.2e} | "
                   f"{abs(Y[-1] - Y[-2]):^+10.2e} | {Y[-1]:^+10.2e} |", file=fic) for fic in [stdout, file]]

            if t_i >= b:
                finished = True
                continue
            t_i += h
            n += 1
        [print(f"Y = {Y} \n T = {T}", file=fic) for fic in [stdout, file]]
        file.close()

        return {'T': T, 'Y': Y, 'name': "Runge Kunta", 'color': "red"}


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

            result = runge_kunta(f, t0, y0, h, b)
            equa_diff_plotting([result], t0, b, f_)
