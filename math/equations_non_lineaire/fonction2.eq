		 f(x) = (x**2 + 1)/x

	 BISSECTION 


intervalle : [-0.5000000000000001, 1.0]
e = 0.0001 :	: n = 20 :
    x1     |     x2     |     xm     |   f(x1)    |   f(x2)    |   f(xm)    |    err abs    
  -0.50000 |   +1.00000 |   +0.25000 |   -2.50000 |   +2.00000 |   +4.25000 |  +7.50e-01
  -0.50000 |   +0.25000 |   -0.12500 |   -2.50000 |   +4.25000 |   -8.12500 |  +3.75e-01
  -0.12500 |   +0.25000 |   +0.06250 |   -8.12500 |   +4.25000 |  +16.06250 |  +1.88e-01
  -0.12500 |   +0.06250 |   -0.03125 |   -8.12500 |  +16.06250 |  -32.03125 |  +9.38e-02
  -0.03125 |   +0.06250 |   +0.01562 |  -32.03125 |  +16.06250 |  +64.01563 |  +4.69e-02
  -0.03125 |   +0.01562 |   -0.00781 |  -32.03125 |  +64.01563 | -128.00781 |  +2.34e-02
  -0.00781 |   +0.01562 |   +0.00391 | -128.00781 |  +64.01563 | +256.00391 |  +1.17e-02
  -0.00781 |   +0.00391 |   -0.00195 | -128.00781 | +256.00391 | -512.00195 |  +5.86e-03
  -0.00195 |   +0.00391 |   +0.00098 | -512.00195 | +256.00391 | +1024.00098 |  +2.93e-03
  -0.00195 |   +0.00098 |   -0.00049 | -512.00195 | +1024.00098 | -2048.00049 |  +1.46e-03
  -0.00049 |   +0.00098 |   +0.00024 | -2048.00049 | +1024.00098 | +4096.00024 |  +7.32e-04
  -0.00049 |   +0.00024 |   -0.00012 | -2048.00049 | +4096.00024 | -8192.00012 |  +3.66e-04
  -0.00012 |   +0.00024 |   +0.00006 | -8192.00012 | +4096.00024 | +16384.00006 |  +1.83e-04
  -0.00012 |   +0.00006 |   -0.00003 | -8192.00012 | +16384.00006 | -32768.00003 |  +9.16e-05

La convergence est atteint en 14 it�ration.
racine approximative dans l'intervalle : [-0.5000000000000001, 1.0] : -3.051757812507402e-05
f(-3.051757812507402e-05) = -32768.0000304381 


S = ( -3.051757812507402e-05 )

	 POINT FIXE 

Etablissement des fonctions equivalentes {x = g(x)} (specifiez seulement g(x))
g0(x) = x**2 + x + 1


Fonction equivalente en cours :  x**2 + x + 1
e = 1e-09 :	: n = 50 :	: x0 = 0.25

g'(x) = 2*x + 1
g'(0.25) = 1.5
La fonction est divergeant.
S = (  )

	 NEWTON 

e = 1e-09 :	: n = 50 :	: x0 = 1.0
f'(x) = 2 - (x**2 + 1)/x**2
La deriv�e est null en 1.0.

	 SECANTE 

e = 1e-09 :	: n = 50 :	: x0 = 1.5 :	: x1 = 2.0

 n   |      xn      |    |e(n)|    | |e(n)/e(n-1)|  |
 0   | +1.50000e+00 | -3.75000e+00 |      ---       |
 1   | +2.00000e+00 | +1.80556e+00 |  -4.81481e-01  |
 2   | -1.75000e+00 | -1.59986e+00 |  -8.86076e-01  |
 3   | +5.55556e-02 | +1.73190e-01 |  -1.08253e-01  |
 4   | -1.54430e+00 | +3.98018e+00 |  +2.29816e+01  |
 5   | -1.37111e+00 | -2.33862e+00 |  -5.87565e-01  |
 6   | +2.60907e+00 | +9.51161e+00 |  -4.06719e+00  |
 7   | +2.70454e-01 | -1.58908e+01 |  -1.67068e+00  |
 8   | +9.78206e+00 | +6.16921e+00 |  -3.88225e-01  |
 9   | -6.10875e+00 | -4.47741e+00 |  -7.25768e-01  |
 10  | +6.04600e-02 | +9.78654e-01 |  -2.18576e-01  |
 11  | -4.41695e+00 | +3.99200e+00 |  +4.07907e+00  |
 12  | -3.43830e+00 | -1.54709e+00 |  -3.87548e-01  |
 13  | +5.53701e-01 | +7.09728e-01 |  -4.58750e-01  |
 14  | -9.93391e-01 | -1.49444e+00 |  -2.10565e+00  |
 15  | -2.83663e-01 | -2.38188e+00 |  +1.59383e+00  |
 16  | -1.77810e+00 | +5.08826e+00 |  -2.13624e+00  |
 17  | -4.15998e+00 | -1.59302e+00 |  -3.13077e-01  |
 18  | +9.28279e-01 | +8.27713e-01 |  -5.19589e-01  |
 19  | -6.64737e-01 | -6.15692e-01 |  -7.43847e-01  |
 20  | +1.62976e-01 | +1.82885e-01 |  -2.97039e-01  |
 21  | -4.52715e-01 | -5.53262e-01 |  -3.02519e+00  |
 22  | -2.69831e-01 | -5.81866e-01 |  +1.05170e+00  |
 23  | -8.23092e-01 | +1.56499e+01 |  -2.68960e+01  |
 24  | -1.40496e+00 | -1.36339e+01 |  -8.71182e-01  |
 25  | +1.42449e+01 | -2.53935e+00 |  +1.86253e-01  |
 26  | +6.11033e-01 | +1.32357e+00 |  -5.21226e-01  |
 27  | -1.92831e+00 | +1.58527e+01 |  +1.19772e+01  |
 28  | -6.04738e-01 | -1.38153e+01 |  -8.71479e-01  |
 29  | +1.52479e+01 | -2.23287e+00 |  +1.61624e-01  |
 30  | +1.43266e+00 | +1.09486e+00 |  -4.90338e-01  |
 31  | -8.00218e-01 | -7.03757e-01 |  -6.42781e-01  |
 32  | +2.94646e-01 | +3.06959e-01 |  -4.36172e-01  |
 33  | -4.09112e-01 | -4.31410e-01 |  -1.40543e+00  |
 34  | -1.02153e-01 | -1.38799e-01 |  +3.21734e-01  |
 35  | -5.33563e-01 | -1.20822e+00 |  +8.70476e+00  |
 36  | -6.72362e-01 | +1.15351e+01 |  -9.54719e+00  |
 37  | -1.88058e+00 | -9.24867e+00 |  -8.01787e-01  |
 38  | +9.65449e+00 | -3.85350e+00 |  +4.16655e-01  |
 39  | +4.05821e-01 | +2.17979e+00 |  -5.65664e-01  |
 40  | -3.44768e+00 | +2.66664e+00 |  +1.22335e+00  |
 41  | -1.26790e+00 | -1.35156e+00 |  -5.06842e-01  |
 42  | +1.39874e+00 | +1.50090e+00 |  -1.11049e+00  |
 43  | +4.71773e-02 | +1.72864e-01 |  +1.15174e-01  |
 44  | +1.54807e+00 | -3.68532e+00 |  -2.13192e+01  |
 45  | +1.72094e+00 | +1.90881e+00 |  -5.17950e-01  |
 46  | -1.96439e+00 | -2.21193e+00 |  -1.15880e+00  |
 47  | -5.55747e-02 | -3.90529e-01 |  +1.76556e-01  |
 48  | -2.26751e+00 | +3.63783e+00 |  -9.31513e+00  |
 49  | -2.65804e+00 | -1.44541e+00 |  -3.97328e-01  |
 50  | +9.79796e-01 | +8.18711e-01 |  -5.66420e-01  |
 51  | -4.65617e-01 | -4.49730e-01 |  -5.49315e-01  |

La convergence n'est pas atteint en 50 it�rations.
