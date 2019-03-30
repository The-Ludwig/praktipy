# standard imports
import sys
import numpy as np

from . import tablehandler as th
__all__ = []

if "matplotlib" in sys.modules or "matplotlib.pyplot" in sys.modules:
    print("Praktipy will not set up the matplotlib backend, because it is already set up.")
else:
    from .praktiplot import plt, matplotlib
    from . import praktiplot as pplt
    __all__ += ["plt", "matplotlib", "pplt"]

from scipy.optimize import curve_fit
from scipy import constants as const
from pint import UnitRegistry
from uncertainties import ufloat
import uncertainties.unumpy as unp

unit = UnitRegistry()
noms = unp.nominal_values
stds = unp.std_devs

# standard import useful (SI) units
meter = unit.meter
seconds = unit.seconds
kilogram = unit.kilogram
kelvin = unit.kelvin
celsius = unit.celsius

units = ["meter", "seconds", "kilogram", "kelvin", "celsius"]

__all__ += ["th", "np", "ufloat", "unp", "unit", "noms",
            "stds", "const", "curve_fit"]
__all__ += units
