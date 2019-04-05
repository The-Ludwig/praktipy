# Setting matplotlib layout to match tex settings

import locale
import matplotlib

matplotlib.use('pgf')

import platform
import numpy as np
import matplotlib.pyplot as plt
from os.path import dirname, abspath

# use german locale settings for printing 3.5 as 3,5
locale_strings = {
    'Darwin': 'de_DE',
    'Windows': 'de_de',
    'Linux': 'de_DE.UTF8',
}

def auto_set_backend():
    import sys
    if "release" in sys.argv:
        print("Setting up Matplotlib to the slow, but pretty backend.")
        pretty()
    else:
        print("Setting up Matplotlib to the fast backend.")
        fast()

def fast():
    matplotlib.rcParams.update({
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
        'pgf.texsystem': 'pdflatex',
        'pgf.preamble': r'\input{'+dirname(abspath(__file__)).replace(" ", r"\ ")+r'//matplotlib_header_minimal.tex'+r'}'
    })


def pretty():  
    try:
        locale.setlocale(locale.LC_ALL, locale_strings[platform.system()])
    except locale.Error:
        print("Could not set the language settings! 3.5 will not be written as 3,5! SO SAD!")

    matplotlib.rcParams.update({
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
        'pgf.texsystem': 'lualatex',
        'pgf.preamble': r'\input{'+dirname(abspath(__file__)).replace(" ", r"\ ")+r'//matplotlib_header.tex'+r'}',
        'axes.formatter.use_locale' : True,
    })

# Currently not working
# if platform.system() == "Windows":
#     plt.style.use('file:\\' + os.path.dirname(os.path.abspath(__file__)) + os.sep + 'praktipy.mplstyle')
# else:
#     plt.style.use('file://' + os.path.dirname(os.path.abspath(__file__)) + os.sep + 'praktipy.mplstyle')

# print('file://' + os.path.dirname(os.path.abspath(__file__)) + os.sep + 'praktipy.mplstyle')
# convenience functions

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

## Use fast settings as default
fast()