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
from scipy.stats import linregress
from scipy import constants as const
import pint
from uncertainties import ufloat
import uncertainties.unumpy as unp

units = pint.UnitRegistry()
noms = unp.nominal_values
stds = unp.std_devs

__all__ += ["th", "np", "ufloat", "unp", "units", "noms",
            "stds", "const", "curve_fit", "linregress"]
