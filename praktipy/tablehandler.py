# to test if something is a number
import numbers
import warnings
import math
import numpy as np
from uncertainties import ufloat, UFloat
from math import log10


# Define what chars do
SEP_CHARS = (" ", "\t")
END_CHARS = ("\n", "\f", "\0")
QUOTE_CHARS = ('"')
COMMENT_CHARS = ("#")


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
        return _gen_from_txt_visual(filename)


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
                    if line[i] in COMMENT_CHARS or line[i] in END_CHARS:
                        break

                    if not found_first_arg:
                        if line[i] in SEP_CHARS:
                            found_first_arg = True
                            in_arg = True
                            if line[i] in COMMENT_CHARS:
                                in_quotes = True
                    elif in_quotes:
                        if line[i] in QUOTE_CHARS:
                            in_quotes = False
                            in_arg = False
                    elif not in_arg and line[i] not in SEP_CHARS:
                        column_lengths.append(i)
                        in_arg = True
                        if line[i] in QUOTE_CHARS:
                            in_quotes = True
                    elif in_arg and line[i] in SEP_CHARS:
                        in_arg = False

                for i in column_lengths:
                    table.append(list())

            found_last = False
            for i in range(len(column_lengths)-1):

                if len(line) <= column_lengths[i+1]:
                    new_word = __parse_word__(line[column_lengths[i]:])
                    table[i].append(new_word)
                    found_last = True
                    # Fill table with nones so we get a rectangular shape
                    for j in range(i+1, len(column_lengths)):
                        table[j].append(None)
                    break

                new_word = __parse_word__(
                    line[column_lengths[i]:column_lengths[i+1]])
                table[i].append(new_word)

            if not found_last:
                new_word = __parse_word__(line[column_lengths[-1]:])
                table[-1].append(new_word)

        file.close()

    return table


def _gen_from_txt_explicit(filename):
    # Can you see my c++-heritage?
    class StateEnum:
        IN_WORD = 0
        IN_QUOTES = 1
        IN_BETWEEN = 2

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
                    if char in SEP_CHARS:
                        pass
                    elif char in END_CHARS:
                        break
                    elif char in QUOTE_CHARS:
                        state = StateEnum.IN_QUOTES
                        new_word += char
                    else:
                        new_word += char
                        state = StateEnum.IN_WORD
                elif state == StateEnum.IN_QUOTES:
                    if char in SEP_CHARS:
                        new_word += char
                    elif char in END_CHARS:
                        __add_word__(__parse_word__(new_word), table, column)
                        column += 1
                        new_word = ""
                        break
                    elif char in QUOTE_CHARS:
                        new_word += char
                        __add_word__(__parse_word__(new_word), table, column)
                        column += 1
                        new_word = ""
                        state = StateEnum.IN_BETWEEN
                    else:
                        new_word += char
                elif state == StateEnum.IN_WORD:
                    if char in SEP_CHARS:
                        __add_word__(__parse_word__(new_word), table, column)
                        column += 1
                        new_word = ""
                        state = StateEnum.IN_BETWEEN
                    elif char in END_CHARS:
                        __add_word__(__parse_word__(new_word), table, column)
                        column += 1
                        new_word = ""
                        break
                    elif char in QUOTE_CHARS:
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
    if len(uncertainty_rep) == 2:
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

    _raw_dict = raw_data(table)
    mean_values = []
    for v in _raw_dict:
        mean_values.append(ufloat(np.mean(v), np.std(v)/np.sqrt(len(v))))

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

    for column in table:
        for i in range(len(column)):
            t_table[i].append(column[i])

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


def gen_tex_table(
        table, filename,
        tex_caption="", tex_label="",
        subtables=None, precision="",
        midrule=2):
    """Generates a .tex file containing only a table.
    The whole file does not have to be modified anymore,
    it can be directly included with \\input{}.
    Uses LaTeX packages (include them!):
    * \\usepackage[
            locale=DE,
            separate-uncertainty=true,  % use \pm
            per-mode=symbol-or-fraction,
            %per-mode=reciprocal,
            %output-decimal-marker=.,
        ]{siunitx}
    * \\susepackage{subcaption}
    Uses S
    Parameters
    ----------
    table : [][] list of lists
        The table which should be parsed.
    ===
    filename : str
        The (relative) filepath where the table is saved.
    ===
    tex_caption : str
        The caption of the table in LaTeX.
    ===
    tex_label : str
        The label of the table in LaTeX.
    ===
    subtables : int or None
    The number of subtables to split into. (0 or None, for no subtables)
    ===
    precision : int[] or int or str[] or str
        The precision per column (as a list) or the precision for every number.
        The format string per column (see https://docs.python.org/3/library/string.html#format-string-syntax)
        or the format string for every number.
    ===
    midrule : int
        After which row to put the midrule. Every row after that will be treated as the header.
    """
    # Track row size to make it rectangular
    rows = 0
    # get the column meta data an put that in the list as __ColumnMeta
    column_meta = []
    # Gather Meta information and parse strings which can be parsed
    for col_index, column  in enumerate(table):
        meta_data = __ColumnMeta()
        if isinstance(precision, list):
            meta_data.precision = precision[col_index]
        else:
            meta_data.precision = precision
        if len(column) > rows:
            rows = len(column)
        for row_index, cell in enumerate(column):
            if isinstance(cell, UFloat):
                meta_data.HAS_UFloats = True
                if cell.std_dev >= 1 and meta_data.MAX_MAGNITUDE < int(log10(cell.std_dev)) + 1:
                    meta_data.MAX_MAGNITUDE = int(log10(cell.std_dev)) + 1
                if cell.nominal_value >= 1 and meta_data.MAX_MAGNITUDE < int(log10(cell.nominal_value)) + 1:
                    meta_data.MAX_MAGNITUDE = int(log10(cell.nominal_value)) + 1
            elif isinstance(cell, numbers.Number):
                if cell >= 1 and meta_data.MAX_MAGNITUDE < int(log10(cell)) + 1:
                    meta_data.MAX_MAGNITUDE = int(log10(cell)) + 1
        column_meta.append(meta_data)

    # Generate empty string table, to maintain rectangular size
    str_table = [["" for j in table] for i in range(rows)]

    # Generate all the strings in the table
    for col_index, column  in enumerate(table):
        for row_index, cell in enumerate(column):
            new_str = __tex_format__(cell, column_meta, col_index)
            if column_meta[col_index].MAX_LEN < len(new_str):
                column_meta[col_index].MAX_LEN = len(new_str)
            str_table[row_index][col_index] = new_str

    # Make the file
    with open(filename, "w") as file:
        file.write(r"\begin{table}"+"\n")
        file.write("\t"+r"\caption{"+tex_caption+"}\n")
        file.write("\t"+r"\label{"  +tex_label+"}\n")
        file.write("\t"+r"\centering"+"\n")
        # Make subtables
        if subtables and subtables != 0:
            if not isinstance(subtables, int):
                raise ValueError("Subtables must be None or a not negative integer.")
            header = str_table[:midrule]
            table = str_table[midrule:]
            rows_st = rows - midrule
            rows_per_subtable = math.ceil(rows_st/subtables)
            for i in range(subtables-1):
                file.write("\t"+r"\begin{subtable}{"+str(round(1.0/subtables - 0.01, 2))+r"\textwidth"+"}\n")
                file.write("\t\t"+r"\centering"+"\n")
                __write_tabular__(file, header+table[i*rows_per_subtable:(i+1)*rows_per_subtable]
                                  , column_meta, midrule, level=2)
                file.write("\t"+r"\end{subtable}"+"\n")
            # Write the last subtable
            file.write("\t"+r"\begin{subtable}{"+str(round(1.0/subtables - 0.01, 2))+r"\textwidth"+"}\n")
            file.write("\t\t"+r"\centering"+"\n")
            __write_tabular__(file, header+table[rows_per_subtable*(subtables-1):]
                                , column_meta, midrule, level=2, fillTo=midrule+rows_per_subtable)
            file.write("\t"+r"\end{subtable}"+"\n")

        else:
            __write_tabular__(file, str_table, column_meta, midrule)

        file.write(r"\end{table}")
        file.close()


def __write_tabular__(file, str_table, column_meta, midrule, level=1, fillTo=None):
    for _ in range(level):
        file.write("\t")
    file.write(r"\begin{tabular}{"+__si_table_header__(column_meta)+"}\n")
    for i in range(level):
        file.write("\t")
    file.write("\t"+r"\toprule"+"\n")
    for row_index, row in enumerate(str_table):
        for i in range(level):
            file.write("\t")
        file.write("\t")
        for col_index, cell in enumerate(row[:-1]):
            file.write(__tex_cell__(cell, column_meta[col_index].MAX_LEN))
            file.write(" & ")
        file.write(__tex_cell__(row[-1], column_meta[-1].MAX_LEN))
        file.write(r"\\"+"\n")
        if row_index + 1 == midrule:
            for i in range(level):
                file.write("\t")
            file.write("\t")
            file.write(r"\midrule"+"\n")
    if fillTo is not None and fillTo > len(str_table):
        for i in range(fillTo - len(str_table)):
            for i in range(level):
                file.write("\t")
            file.write("\t")
            for col_index, cell in enumerate(str_table[-1][:-1]):
                file.write(
                    r"\phantom{"+__tex_cell__(cell, column_meta[col_index].MAX_LEN).strip()+"}")
                file.write(" & ")
            file.write(
                r"\phantom{"+__tex_cell__(row[-1], column_meta[-1].MAX_LEN).strip()+"}")
            file.write(r"\\"+"\n")

    for i in range(level):
        file.write("\t")
    file.write("\t"+r"\bottomrule"+"\n")
    for i in range(level):
        file.write("\t")
    file.write(r"\end{tabular}"+"\n")


class __ColumnMeta:
    MAX_LEN = 0
    HAS_UFloats = False
    MAX_MAGNITUDE = 1
    precision = None


def __si_table_header__(column_meta):
    ret = ""
    for col in column_meta:
        if isinstance(col.precision, str) and col.precision.find(":") == -1:
            ret += r"S[table-format=" + col.precision + r"] "
        elif isinstance(col.precision, str):
            ret += r"S[table-format=" + \
            str(col.MAX_MAGNITUDE)+"."+ "0" + r"] "
        else:
            ret += r"S[table-format=" + \
                str(col.MAX_MAGNITUDE)+"."+str(col.precision) + r"] "
        if col.HAS_UFloats:
            ret += r"@{${}\pm{}$} "
            if isinstance(col.precision, str) and col.precision.find(":"):
                ret += r"S[table-format=" + col.precision + r"] "
            elif isinstance(col.precision, str):
                ret += r"S[table-format=" + \
                str(col.MAX_MAGNITUDE)+"."+ "0" + r"] "
            else:
                ret += r"S[table-format=" + \
                    str(col.MAX_MAGNITUDE)+"."+str(col.precision) + r"] "
    return ret
  

def __tex_cell__(cell, max_len_column):
    remaining_spaces = max_len_column - len(cell)
    while remaining_spaces > 0:
        cell += " "
        remaining_spaces -= 1
    return cell


def __tex_format__(cell, column_meta, column_index):

    formatter = column_meta[column_index].precision

    # Numbers
    if isinstance(cell, numbers.Number):
        if isinstance(formatter, int):
            if formatter < 0:
                raise ValueError(
                    "Negative precision ("+formatter+") makes no sense.")
            formatter = "{:."+str(formatter)+"f}"

        elif isinstance(formatter, float):
            if formatter < 0:
                raise ValueError(
                    "Negative precision ("+formatter+") makes no sense.")
            formatter = ("{:" + str(int(formatter)) + "."
                         + str(int(round((formatter - int(formatter))*10))) + "f}"
                         )

        elif isinstance(formatter, str):
            if(formatter.find(":") == -1):
                formatter = "{:"+formatter+"f}"
            else:
                formatter = "{"+formatter+"}"

        if column_meta[column_index].HAS_UFloats:
            warnings.warn(
                "You have normal numbers in a column where one or more UFloats exist. That can lead to ugly tables.")
            formatter += "&0"

        assert isinstance(formatter, str)

        return formatter.format(cell)

    if isinstance(cell, UFloat):
        if isinstance(formatter, str):
            if(formatter.find(":") == -1):
                cell_ufloat = ("{:"+formatter+"u}").format(cell).split("+/-")
            else:
                cell_ufloat = ("{"+formatter+"}").format(cell).split("+/-")                
        else:
            # Let uncertainty handle the precision
            cell_ufloat = "{:u}".format(cell).split("+/-")

        return cell_ufloat[0]+" & "+cell_ufloat[1]
    # cell is Null
    if not cell:
        return "{}"

    # No known rules (Maybe it is a string)
    # Add multicol stuff
    if column_meta[column_index].HAS_UFloats:
        return r"\multicolumn{2}{c}{"+str(cell)+r"}"
    return r"{"+str(cell)+r"}"
