import numpy as np
import uncertainties.unumpy as unp
from uncertainties import ufloat, UFloat
import numbers  # to test if something is a number


def __parseWord__(word):
    """Parse a word from a tablefile"""

    word = word.strip()
    if len(word) == 0:
        return None
    if word[-1] == '"' and word[0] == '"':
        return word[1:-1]

    try:
        ret = float(word)
        return float(ret)
    except:
        return word


def genfromtxt(filename):
    """Generates a Tablehandler out of the table in a given file"""

    # Open file and get lines
    with open(filename) as f:
        lines = f.readlines()
        f.close()

    # Parse table
    table = []
    columns = []
    for line in lines:
        line = line.rstrip()

        indexH = line.find("#")
        if indexH != -1:
            line = line[:indexH]

        # Determine position of columns
        if len(columns) == 0:
            if line.strip() == "":
                continue

            columns = [0]
            foundFirstArg = False
            inArg = False
            inQuotes = False

            for i in range(len(line)):
                if line[i] == '#' or line[i] == "\n" or line[i] == "\f":
                    break

                if foundFirstArg == False:
                    if line[i] != " ":
                        foundFirstArg = True
                        inArg = True
                        if line[i] == '"':
                            inQuotes = True
                elif inQuotes:
                    if line[i] == '"':
                        inQuotes = False
                        inArg = False
                elif inArg == False and line[i] != " ":
                    columns.append(i)
                    inArg = True
                    if line[i] == '"':
                        inQuotes = True
                elif inArg and line[i] == " ":
                    inArg = False

            for i in columns:
                table.append(list())

        found_last = False

        for i in range(len(columns)-1):

            if(len(line) <= columns[i+1]):
                newWord = __parseWord__(line[columns[i]:])
                table[i].append(newWord)
                found_last = True

                # Fill table with nones so we get a rectangular shape
                for j in range(i+1, len(columns)):
                    table[j].append(None)
                break

            newWord = __parseWord__(line[columns[i]:columns[i+1]])
            table[i].append(newWord)

        if not found_last:
            newWord = __parseWord__(line[columns[-1]:])
            table[-1].append(newWord)

    return TableHandler(table)


class TableHandler:
    """ Class to handle tables in the internship easily """

    def __init__(self, table=None):
        """Initalize table, eather from given table or from Filename"""
        self.table = table

    def getDict(self):
        """Retuns a dictionary mapping the first line to its columns"""
        dicti = {}
        for c in self.table:
            dicti[c[0]] = c[1:]
        return dicti

    def getTransposedTable(self, table=None):
        """Returns the transposition of the (underlaying, if table = None) table."""
        if table == None:
            table = self.table

        tTable = []
        for i in table:
            while len(i) > len(tTable):
                tTable.append([])

        for c in table:
            for i in range(len(c)):
                tTable[i].append(c[i])

        return tTable

    def transpose(self):
        """Transposes underlaying table"""
        self.table = self.getTransposedTable()

    def insertRow(self, row, index=None):
        """Add a segment to the table
        row: 1d Table to  add
        index: index to add the table to. Set to None to append"""
        if index == None:
            self.table.append(row)
        else:
            self.table.insert(index, row)

    def popRow(self, index=-1):
        """Deletes row with index index"""
        self.table.pop(index)

    def getRawDict(self):
        """Returns a dictionary mapping the first line to its non-string collumn values"""
        dicti = {}
        for c in self.table:
            dicti[c[0]] = []
            for j in c[1:]:
                if isinstance(j, numbers.Number):
                    dicti[c[0]].append(j)

        return dicti

    def getRawData(self):
        """Returns only floats and ints"""

        data = []
        for i in self.table:
            data.append([])

        for i in range(len(self.table)):
            for w in self.table[i]:
                if isinstance(w, numbers.Number):
                    data[i].append(w)
        return data

    def makeTexTable(self, filename, useSIUnitX=True, precision=None, makeHeader=True, standardRules=True):
        """Generates a .tex table into file"""

        # Generate transposed table
        tTable = self.getTransposedTable()
        # Search length and replace Nones
        maxLen = 0

        maxRowLen = 0

        # find length of row
        for i in tTable:
            if maxRowLen < len(i):
                maxRowLen = len(i)

        for i in range(len(tTable)):
            if len(tTable[i]) < maxRowLen:
                tTable[i] += (maxRowLen - len(tTable[i])) * [""]

            for j in range(len(tTable[i])):
                if(tTable[i][j] == None):
                    tTable[i][j] = ""

                if maxLen < len(str(tTable[i][j])):
                    maxLen = len(str(tTable[i][j]))

        # account for SIUnitX stuff
        maxLen += 10

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
                for i in self.table[:-1]:
                    file.write("S ")
                file.write("S")
            else:
                for i in self.table[:-1]:
                    file.write("c ")
                file.write("c")
            file.write("}\n")

            if standardRules:
                if makeHeader:
                    file.write("\t\t")
                file.write(r"\toprule"+"\n")

        def parseTexWord(word, end=False):
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

            file.write(newWord+(maxLen - len(newWord))*" ")

            if not end:
                file.write(" & ")

        for l in range(len(tTable)):

            if standardRules and l == 1:
                if makeHeader:
                    file.write("\t\t")
                file.write(r"\midrule"+"\n")

            for w in tTable[l][:-1]:
                parseTexWord(w)

            parseTexWord(tTable[l][-1], end=True)
            file.write(r"  \\"+"\n")

        if standardRules:
            if makeHeader:
                file.write("\t\t")
            file.write(r"\bottomrule"+"\n")

        if makeHeader:
            file.write("\t"+r"\end{tabular}"+"\n")
            file.write(r"\end{table}")

        file.close()

    def getMeanValues(self):
        """Returns the mean values and errors of them as ufloats"""

        rawDict = self.getRawDict()
        meanValues = {}
        for v in rawDict.items():
            meanValues[v[0]] = np.mean(ufloat(np.mean(v[1]), np.std(v[1])))

        return meanValues
