# standard imports
import sys
import numpy as np

from .tablehandler import TableHandler, genfromtxt

__all__ = []

if "matplotlib" in sys.modules or "matplotlib.pyplot" in sys.modules:
    print("Praktipy will not set up the matplotlib backend, because it is already set up.")
else:
    from .praktiplot import plt, matplotlib, cla
    __all__ += ["plt", "matplotlib", "cla"]

from scipy.optimize import curve_fit
from scipy import constants as const
from pint import UnitRegistry
from uncertainties import ufloat
import uncertainties.unumpy as unp


unit = UnitRegistry()
noms = unp.nominal_values
stds = unp.std_devs

# standart import useful (SI) units
meter = unit.meter
seconds = unit.seconds
kilogram = unit.kilogram
kelvin = unit.kelvin
celsius = unit.celsius


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


units = ["meter", "seconds", "kilogram", "kelvin", "celsius"]

__all__ += ["TableHandler", "np", "ufloat", "unp", "unit", "noms",
            "stds", "const", "polyplotfit", "genfromtxt", "curveplotfit", "curve_fit"]
__all__ += units
