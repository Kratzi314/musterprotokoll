import sys
import numpy as np
import matplotlib.pyplot as plt
import kafe
from kafe.function_tools import FitFunction, LaTeX, ASCII
from kafe.function_library import quadratic_3par

# read columns from file:
if len(sys.argv) == 2:
    infile = sys.argv[1]
else:
    infile = 'Messtabelle.txt'

m_g, s_cm = np.loadtxt(infile, unpack=True)      # read from file
#print(m,s)

s=s_cm
m=m_g
D=14.6

xO=np.mean(s)
# ---- fit function definition in kafe style
#         (decorators for nice output not mandatory)
@ASCII(expression='k * ( x - xO ) + c')
@LaTeX(name='f', parameter_names=('k', 'c' ,'xO'), expression=r'k\,(x+\tilde{x})\,+c')
@FitFunction
def lin(x, k=1.0, c=0.0):
    return k*(x + xO) + c

# ---- begin of fit ---
# set the function
fitf = lin            # own definition
#fitf=quadratic_3par   # or from kafe function library
# --------- begin of workflow ----------------------
# set data

kdata = kafe.Dataset(data=(m, s), basename='kData',
                     title='example data')
kdata.add_error_source('y', 'simple', 1.0)
kfit = kafe.Fit(kdata, fitf)    # create the fit
kfit.do_fit()                   # perform fit
print(kfit)

kplot = kafe.Plot(kfit)         # create plot object
kplot.axis_labels = ['x', 'Daten und  f(x)']
kplot.plot_all()                # make plots
kplot.save('Blatt6_b_fit.pdf')
kplot.show()
