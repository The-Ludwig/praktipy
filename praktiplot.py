# Setting matplotlib layout to match tex settings 

import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from os.path import dirname, abspath
matplotlib.rcParams.update({
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'pgf.texsystem': 'lualatex',
    'pgf.preamble': r'\input{'+dirname(abspath(__file__))+r'//matplotlib_header.tex'+r'}',
})