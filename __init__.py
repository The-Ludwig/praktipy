# standart imports
import sys 
if "matplotlib" in sys.modules or "matplotlib.pyplot" in sys.modules:
    print("Praktipy will not set up the matplotlib backend, because it is allready set up.")
else:
    from .praktiplot import plt, matplotlib
    __all__ += ["plt", "matplotlib"]
from .tablehandler import TableHandler, genfromtxt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
from pint import UnitRegistry
from scipy import constants as const

unit = UnitRegistry()
noms = unp.nominal_values
stds = unp.std_devs

# standart import useful (SI) units
meter       = unit.meter
seconds     = unit.seconds
kilogram    = unit.kilogram
kelvin      = unit.kelvin
celsius     = unit.celsius


# convenience function

def polyplotfit(x, params, N = 1000, border=0.05):
    """Plots a polynome which was fitted. 
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


units = ["meter", "seconds", "kilogram", "kelvin", "celsius"]

__all__ = ["TableHandler", "np", "ufloat", "unp", "unit", "noms", "stds", "const", "polyplotfit", "genfromtxt"]
__all__ += units