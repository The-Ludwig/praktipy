prakitpy
====
This provides a little script to handle tables in textfiles (similar, but more powerful, to numpy.genfromtxt()).

# Using Matplotlib

Praktipy will try to set up the matplotlib backend to enable printing of beautiful (german number format and nice math-font) plots. If you want to set up matplotlib yourself, just do that before you import anything from praktipy.

# Documentation

The code currently is not very well documented (Allthough tablehandler.py itself provides nice Docstrings).
You will find some examples in ./examples/, which you can use for orientation.

# Dependencies
* python
* numpy
* uncertainties
* pint

Please install numpy, uncertainties with the following commands (using pip).
~~~sh
$ pip install numpy
$ pip install uncertainties
$ pip install pint
~~~

# Installation
For now: execute install.bash. Maybe I will add a nicer version later (which is in tone to the rest of python).
~~~sh
$ ./install.bash
~~~

# Thanks
Thanks a lot to [PEP et al.](https://pep-dortmund.org/) for their [Toolbox-Workshop](https://toolbox.pep-dortmund.org/notes.html) and materials they provide. I basicly stole their matplotlib-tex-header! 
