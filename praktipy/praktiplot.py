# Setting matplotlib layout to match tex settings

import locale
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from os.path import dirname, abspath

matplotlib.use('pgf')
matplotlib.rcParams.update({
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'pgf.texsystem': 'lualatex',
    'pgf.preamble': r'\input{'+dirname(abspath(__file__)).replace(" ", r"\ ")+r'//matplotlib_header.tex'+r'}',
})

# use german locale settings for printing 3.5 as 3,5
try:
    locale.setlocale(locale.LC_ALL, 'de_DE')
except locale.Error:
    print("Could not set the language settings! 3.5 will not be written as 3,5! SO SAD!")

plt.ticklabel_format(useLocale=True)

# convenience functions
@jit
def polyplotfit(x, params, N=1000, border=0.05):
    """Plots a polynome, which was fitted.
    x: the original x value which was fitted
    params: the parameters in the polynome
    N: Number of x_values to calculate
    border: percentage of x_range to make a border"""

    dx = x[-1] - x[0]
    x_fit = np.linspace(x[0] - dx*border, x[-1] + dx*border, N)
    y_fit = np.zeros(len(x_fit))
    deg = len(params)
    for i in range(deg):
        y_fit += params[deg-1-i] * x_fit**i

    return (x_fit, y_fit)

@jit
def curveplotfit(f, x, params, N=1000, border=0.05, logscale=False):
    """Plots a general function, which was fitted.
    x: the original x value which was fitted
    params: the parameters in the polynome
    N: Number of x_values to calculate
    border: percentage of x_range to make a border"""
    dx = x[-1] - x[0]
    if logscale:
        x_fit = np.logspace(np.log10(
            x[0]) - np.log10(x[0])*border*0.6, np.log10(x[-1])+np.log10(x[-1])*border*0.2, N)
    else:
        x_fit = np.linspace(x[0] - dx*border, x[-1] + dx*border, N)
    y_fit = f(x_fit, *params)

    return (x_fit, y_fit)

def cla():
    """
    Calls the matplotlib plt.cla, but turns the useLocale option back on.
    """
    plt.cla()
    plt.ticklabel_format(useLocale=True)
