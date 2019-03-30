# prakitpy

This provides a little script to handle tables in textfiles (similar, but more powerful, to numpy.genfromtxt()).

**Note:** This is the legacy version. Please see the [releases](https://github.com/The-Ludwig/praktipy/releases) branch for the most recent release!

# Using Matplotlib

Praktipy will try to set up the matplotlib backend to enable printing of beautiful (german number format and nice math-font) plots. If you want to set up matplotlib yourself, just do that before you import anything from praktipy.

# Documentation

The code currently is not very well documented (Allthough tablehandler.py itself provides nice Docstrings).
You will find some examples in ./examples/, which you can use for orientation.

# Dependencies

- python 3
- numpy
- uncertainties
- pint

# Installation

```sh
$ python3 setup.py install

# If python 3 is installed only

$ python setup.py install
```

The setup script will download and install all needed dependencies.

# Thanks

Thanks a lot to [PEP et al.](https://pep-dortmund.org/) for their [Toolbox-Workshop](https://toolbox.pep-dortmund.org/notes.html) and materials they provide. I basicly stole their matplotlib-tex-header!
