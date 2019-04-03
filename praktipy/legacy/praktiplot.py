# Setting matplotlib layout to match tex settings

import matplotlib
import matplotlib.pyplot as plt
from os.path import dirname, abspath
import locale

def cla():
    plt.cla()
    plt.ticklabel_format(useLocale=True)

matplotlib.use('pgf')
matplotlib.rcParams.update({
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'pgf.texsystem': 'lualatex',
    'pgf.preamble': r'\input{'+dirname(abspath(__file__)).replace(" ", r"\ ")+r'//matplotlib_header.tex'+r'}',
})

# use german locale settings for printing 3.4 as 3,4
try:
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF8')
except locale.Error:
    print("Could not set the language settings! 3.5 will not be written as 3,5! SO SAD!")

plt.ticklabel_format(useLocale=True)
