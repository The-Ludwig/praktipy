# to test if something is a number
import numbers
import numpy as np
from uncertainties import ufloat, UFloat

def gen_from_txt(filename, explicit_none=False):
    """Generates a multi-datatype table (A python list of python lists,
    which contains strings, floats and None).
    You can generate uncertaintie ufloats by writing something like
    42.000+-3.1415.

    WARNING: Not suitable for very large tables (everything under a few thousand line should be fine though).
        Use numpy.genfromtxt instead!

    Parameters
    ----------
    filename : str
        The path to the textfile to parse. Look into the examples, for further
        information on how to format the file.
    explicitNone : bool, optional
        Whether the table structure is determend visually by looking
        at the first line, or with explicit "Nones" where no value is present.
        (the default is False, which looks at the file visually)

    Returns
    -------
    list of lists (python lists) [][]
        The parsed table
    """

    if explicit_none:
        return _gen_from_txt_explicit(filename)
    else:
        return _gen_from_txt_visual

def _gen_from_txt_visual(filename):
    table = []
    column_lengths = []

    # Parse table
    with open(filename) as file:
        for line in file:
            line = line.rstrip()

            # check for comments beginning with '#'
            index_end = line.find("#")
            if index_end != -1:
                line = line[:index_end]

            # Determine position of columns
            # len(columns) == 0
            if not column_lengths:
                if line.strip() == "":
                    continue

                column_lengths = [0]
                found_first_arg = False
                in_arg = False
                in_quotes = False

                for i in range(len(line)):
                    if line[i] == '#' or line[i] == "\n" or line[i] == "\f":
                        break

                    if not found_first_arg:
                        if line[i] != " ":
                            found_first_arg = True
                            in_arg = True
                            if line[i] == '"':
                                in_quotes = True
                    elif in_quotes:
                        if line[i] == '"':
                            in_quotes = False
                            in_arg = False
                    elif not in_arg and line[i] != " ":
                        column_lengths.append(i)
                        in_arg = True
                        if line[i] == '"':
                            in_quotes = True
                    elif in_arg and line[i] == " ":
                        in_arg = False

                for i in column_lengths:
                    table.append(list())

            found_last = False
            for i in range(len(column_lengths)-1):

                if(len(line) <= column_lengths[i+1]):
                    new_word = __parse_word__(line[column_lengths[i]:])
                    table[i].append(new_word)
                    found_last = True
                    # Fill table with nones so we get a rectangular shape
                    for j in range(i+1, len(column_lengths)):
                        table[j].append(None)
                    break

                new_word = __parse_word__(line[column_lengths[i]:column_lengths[i+1]])
                table[i].append(new_word)

            if not found_last:
                new_word = __parse_word__(line[column_lengths[-1]:])
                table[-1].append(new_word)

        file.close()

    return table

def _gen_from_txt_explicit(fi lename):
    # Can you see my c++-heritage?
    class StateEnum:
        IN_WORD     = 0
        IN_QUOTES   = 1
        IN_BETWEEN  = 2

    # Table to return
    table = []

    # Parse file
    with open(filename) as file:
        # Parse every line
        for line in file:
            # to remember column
            column = 0
            # Ignore whitespace and comments (with #)
            line = line.strip()
            index_end = line.find("#")
            if index_end != -1:
                line = line[:index_end]

            new_word = ""
            state = StateEnum.IN_BETWEEN

            for char in line:
                if state == StateEnum.IN_BETWEEN:
                    if char == " ":
                        pass
                    elif char == "\n" or char == "\f" or char == "\0":
                        break
                    elif char == '"':
                        state = StateEnum.IN_QUOTES
                        new_word += char
                    else:
                        new_word += char
                        state = StateEnum.IN_WORD
                elif state == StateEnum.IN_QUOTES:
                    if char == " ":
                        new_word += char
                    elif char == "\n" or char == "\f" or char == "\0":
                        __add_word__(__parse_word__(new_word), table, column)
                        column += 1
                        new_word = ""
                        break
                    elif(char == '"'):
                        new_word += char
                        __add_word__(__parse_word__(new_word), table, column)
                        column += 1
                        new_word = ""
                        state = StateEnum.IN_BETWEEN
                    else:
                        new_word += char
                elif state == StateEnum.IN_WORD:
                    if(char == " "):
                        __add_word__(__parse_word__(new_word), table, column)
                        column += 1
                        new_word = ""
                        state = StateEnum.IN_BETWEEN
                    elif(char == "\n" or char == "\f" or char == "\0"):
                        __add_word__(__parse_word__(new_word), table, column)
                        column += 1
                        new_word = ""
                        break
                    elif char == '"':
                        new_word += char
                    else:
                        new_word += char

            if new_word != "":
                __add_word__(__parse_word__(new_word), table, column)

        file.close()
    return table

def __add_word__(word, table, column):
    if len(table) < column + 1:
        table.append([word])
        return
    table[column].append(word)

def __parse_word__(word):
    """Parse a word from a tablefile"""

    word = word.strip()
    # len(word) == 0
    if not word:
        return None
    if word[-1] == '"' and word[0] == '"':
        return word[1:-1]

    if(word == "None"):
        return None

    # parse uncertainty value
    uncertainty_rep = word.split("+-")
    if(len(uncertainty_rep) == 2):
        try:
            ret = ufloat(float(uncertainty_rep[0]), float(uncertainty_rep[1]))
            return ret
        except ValueError:
            return word

    try:
        ret = float(word)
        return float(ret)
    except ValueError:
        return word

def mean_values(table):
    """Returns the mean values and errors of the given tables as ufloats."""

    _raw_dict = raw_dict(table)
    mean_values = []
    for v in _raw_dict.items():
        mean_values.append(np.mean(ufloat(np.mean(v[1]), np.std(v[1]))))

    return mean_values

def mean_values_dict(table):
    """Returns the mean values and errors of the given tables as ufloats."""

    _raw_dict = raw_dict(table)
    mean_values = {}
    for v in _raw_dict.items():
        mean_values[v[0]].append(np.mean(ufloat(np.mean(v[1]), np.std(v[1]))))

    return mean_values

def dict_from_table(table):
    """Retuns a dictionary mapping the first line to its columns"""
    dict_ret = {}
    for _c in table:
        dict_ret[_c[0]] = _c[1:]
    return dict_ret

def raw_dict(table):
    """Returns a dictionary mapping the first line to its non-string collumn values"""
    dictRet = {}
    for c in table:
        dictRet[c[0]] = []
        for j in c[1:]:
            # Use isinstance to account for numpy floats.
            if isinstance(j, numbers.Number) or isinstance(j, UFloat):
                dictRet[c[0]].append(j)

    return dictRet

def transposed(table):
    """Returns the transposition of the table."""
    if table == None:
        return None

    t_table = []
    for i in table:
        while len(i) > len(t_table):
            t_table.append([])

    for collumn in table:
        for i in range(len(collumn)):
            t_table[i].append(collumn[i])

    return t_table

def raw_data(table):
    """Returns numbers only"""

    data = []
    for i in table:
        data.append([])

    for i in range(len(table)):
        for w in table[i]:
            if isinstance(w, numbers.Number):
                data[i].append(w)
    return data

def gen_tex_table(table, filename, useSIUnitX=True, precision=None, makeHeader=True, standardRules=True):
    """Generates a .tex table into file"""

    # Generate transposed table
    t_table = transposed(table)
    # Search length and replace Nones
    max_len = 0
    max_row_len = 0

    # find length of row
    for i in t_table:
        if max_row_len < len(i):
            max_row_len = len(i)

    for i in range(len(t_table)):
        if len(t_table[i]) < max_row_len:
            t_table[i] += (max_row_len - len(t_table[i])) * [""]

        for j in range(len(t_table[i])):
            if(t_table[i][j] == None):
                t_table[i][j] = ""

            if max_len < len(str(t_table[i][j])):
                max_len = len(str(t_table[i][j]))

    # account for SIUnitX stuff
    max_len += 10

    # Write TeX
    file = open(filename, "w+")

    if makeHeader:
        file.write(r"\begin{table}"+"\n")

        file.write("\t"+r"\caption{TABLE}"+"\n")
        file.write("\t"+r"\label{tab:NAME}"+"\n")
        if(useSIUnitX):
            file.write("\t"+r"\sisetup{table-format=X.")
            if(precision != None):
                file.write(str(int(precision)))
            else:
                file.write("X")
            file.write("}\n")

        file.write("\t"+r"\begin{tabular}{")
        if useSIUnitX:
            for i in table[:-1]:
                file.write("S ")
            file.write("S")
        else:
            for i in table[:-1]:
                file.write("c ")
            file.write("c")
        file.write("}\n")

        if standardRules:
            if makeHeader:
                file.write("\t\t")
            file.write(r"\toprule"+"\n")

    def __parse_tex_word__(word, end=False):
        newWord = ""
        if isinstance(word, numbers.Number) or isinstance(word, UFloat):
            if precision != None:
                newWord = ("{:."+str(int(precision))+"f}").format(word)
            else:
                newWord = str(word)
        else:
            newWord = str(word)
            if(useSIUnitX):
                newWord = "{"+newWord+"}"

        if makeHeader:
            file.write("\t\t")

        file.write(newWord+(max_len - len(newWord))*" ")

        if not end:
            file.write(" & ")

    for l in range(len(t_table)):

        if standardRules and l == 1:
            if makeHeader:
                file.write("\t\t")
            file.write(r"\midrule"+"\n")

        for w in t_table[l][:-1]:
            __parse_tex_word__(w)

        __parse_tex_word__(t_table[l][-1], end=True)
        file.write(r"  \\"+"\n")

    if standardRules:
        if makeHeader:
            file.write("\t\t")
        file.write(r"\bottomrule"+"\n")

    if makeHeader:
        file.write("\t"+r"\end{tabular}"+"\n")
        file.write(r"\end{table}")

    file.close()
