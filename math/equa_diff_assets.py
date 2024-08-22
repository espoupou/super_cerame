import numpy as np
from os import mkdir, getcwd
import matplotlib.pyplot as plt
from sympy import var, init_printing
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

y, t = var('y t')
init_printing(use_unicode=True)

equa_diff_file_path = f"{getcwd()}/equa_diff"


# ============================
def get_function_from_input():
    string_format = input("Entrer la fonction : ").replace("^", "**")
    if "y" not in string_format and "t" not in string_format:
        print("La fonction n'a pas de variable t ou y.")
        return 0
    try:
        func = parse_expr(string_format, transformations=(standard_transformations +
                                                          (implicit_multiplication_application,)))

    except SyntaxError as er:
        print("Format incorrect.")
        print(er)
        return 0

    return func


def ed_get_function():
    parsed = get_function_from_input()
    print(f"la fonction est {parsed}?")
    while input("y pour confirmer... ") != 'y':
        parsed = get_function_from_input()
        print(f"la fonction est {parsed}?")
    return parsed


def equa_diff_dir():
    try:
        mkdir("./equa_diff")
    except FileExistsError:
        pass


def equa_diff_file_name(created=False):
    equa_diff_dir()

    # --------------------------------------------
    def create_name():
        i = 0
        while True:
            try:
                open(f"function{i}.aqdi", 'r').close()

            except FileNotFoundError:
                if not created:
                    try:
                        with open(f"{equa_diff_file_path}/num.txt", 'w') as file:
                            file.write(f"{i}")
                            file.close()
                    except FileNotFoundError:
                        continue
                return f"function{i}.eqdi" if not created else f"function{i - 1}.eqdi"
            i += 1

    # --------------------------------------------
    try:
        with open(f"{equa_diff_file_path}/num.txt", 'r') as file:
            i = int(file.read()) + 1
            file.close()

        if not created:
            with open(f"{equa_diff_file_path}/num.txt", 'w') as file:
                file.write(str(i))
                file.close()
        return f"function{i}.eqdi" if not created else f"function{i - 1}.eqdi"

    except FileNotFoundError:
        return create_name()
    except ValueError:
        return create_name()


def equa_diff_plotting(options, t0, b, f=None):
    for option in options:
        plt.plot(option['T'], option['Y'], label=option['name'], color=option['color'])

    if f is not None:
        plot_x = np.linspace(t0 - 1, b + 1, 500)
        plt.plot(plot_x, np.array([f(x_i) for x_i in plot_x]), label="solution exacte", color="orange")
    plt.legend()
    plt.show()
