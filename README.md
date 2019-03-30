praktipy
====
These python files will make your life easier when handling with human readable
tables in the physik-praktikum at TU-Dortmund(, hopefully).

# Table of Contents
- [praktipy](#praktipy)
- [Table of Contents](#table-of-contents)
- [Needed software](#needed-software)
- [Installation](#installation)
- [or without make:](#or-without-make)
  - ["But I don't want to install the whole thing"](#%22but-i-dont-want-to-install-the-whole-thing%22)
- [Handling tables](#handling-tables)
  - [Generating tables out of text files](#generating-tables-out-of-text-files)
- [Look what the parser has parsed](#look-what-the-parser-has-parsed)
  - [Generating tex tables](#generating-tex-tables)
- [It is that quick.](#it-is-that-quick)
  - [Manipulating the table.](#manipulating-the-table)
- [Using Matplotlib](#using-matplotlib)
- [Wildcard imports](#wildcard-imports)
- [Documentation](#documentation)
- [Old versions](#old-versions)
- [Thanks](#thanks)

# Needed software
* python 3
* some python 3 packages, which will be installed by the install script
* laTeX

# Installation
~~~sh
$ make install
# or without make:
$ python3 setup.py install
~~~
## "But I don't want to install the whole thing"
If you don't want to install the whole package on your computer, you can just download the relevant files directly:
* Table handling:
  Download "praktipy/tablehandler.py". Just put the file into your currently used directory and import it with "import tablehandler as th"
* Plots: Use praktiplot.py in a similar way.

# Handling tables
If you have installed the module use
~~~python
import praktipy.tablehandler as th
~~~
If you just downloaded the file
~~~python
import tablehandler as th
~~~
## Generating tables out of text files
Praktipy uses 2-dimensional standart python-lists, to represent its lists.
It can generate them out of a human readable text file (th.gen_from_txt). That seems very similar to numpy.genfromtxt, but although it is way more inefficient, it much more powerful. 
I can't recommend it to parse very large files (use numpy.genfromtxt for that), but every human readable table should be fine.

Why gen_from_txt is useful:
* You can have "**None**" values in your table. (Holes)
* You can have **ufloats** in your table. (Write them as "42.14+-6.5")
* You can have **strings** in your table.
* You can write your table visually.  (gen_from_txt(filename, explicit_none=False))
* You can write your table explicitly.  (gen_from_txt(filename, explicit_none=True))

~~~python
table = th.gen_from_txt("./path/to/table")
# Look what the parser has parsed
print(table)
~~~
More detailed information in the source code docstrings and the */examples* directory.
## Generating tex tables
Once you have an 2 dimensional python list (actually it could be any 2 dimensional iterable), you can very easily make a beautiful .tex table out of it.

Why gen_tex_table is useful:
* You can direcly **\input** the generated file.
* You can split the table into **subtables** automaticly.
* You can set laTeX **labels** and **captions**.
* You can set the **precision** per column or globaly.


~~~python
# It is that quick.
th.gen_tex_table(
        table, 
        "/path/to/output/tex/file",
        tex_caption="Put your laTeX caption here", 
        tex_label="Put your laTex label here",
        subtables=2, 
        precision=["2.3", 3, "1.9"],
        midrule=2
    )
~~~
More detailed information in the source code docstrings and the */examples* directory.

## Manipulating the table.
You can manipulate the table with all the known python list functions. Ontop of that some functions to make your life easier are provided.
* **Tranposing** table: th.transposed(table)
* Getting the **data** (numbers) from the table: th.raw_data(table)
* etc. (look in the module for further information, e.g. dir(th))
  
# Using Matplotlib

Praktipy will try to set up the matplotlib backend to enable printing of pretty (german number format and nice math-font) plots. If you want to set up matplotlib yourself, just do that before you import anything from praktipy.

Praktipy also provides some convenience function,
for example to generate nice datapoints ontop of a fitted function. 

# Wildcard imports
Generally you should only import things you need in python. But nontheless it is quite handy to just import everything you need and see some code completion of things you usally need for the internship.
Praktipy provides that with the wildcard import:
~~~python
from praktipy import *
~~~
That will import everything you will probably need for the internship.

# Documentation

The code currently is not very well documented (Allthough tablehandler.py itself provides nice Docstrings).
You will find some examples in ./examples/, which you can use for orientation.

# Old versions
If you have already written some code with an old version of praktipy (before 2.0), it is very 
likely that that won't work with the new versions.

I redid the whole code style of praktipy to be a bit more pythonic.

But fear not! There is an easy trick to access old version of praktipy fro within the new version. Whenever you have written something with praktipy, like
~~~python
from praktipy import *
~~~ 
just substitute *praktipy* with *praktipy.legacy* like that
~~~python
from praktipy.legacy import *
~~~
and your code will work without problems.



# Thanks
Thanks a lot to [PEP et al.](https://pep-dortmund.org/) for their [Toolbox-Workshop](https://toolbox.pep-dortmund.org/notes.html) and materials they provide. I basicly stole their matplotlib-tex-header!
