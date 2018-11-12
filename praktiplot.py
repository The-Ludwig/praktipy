# Setting matplotlib layout to match tex settings 

import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from os.path import dirname, abspath
import locale
matplotlib.rcParams.update({
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'pgf.texsystem': 'lualatex',
    'pgf.preamble': r'\input{'+dirname(abspath(__file__))+r'//matplotlib_header.tex'+r'}',
})
# use german locale settings for printing 3.4 as 3,4
locale.setlocale(locale.LC_ALL, 'de_DE.UTF8')
plt.ticklabel_format(useLocale=True)