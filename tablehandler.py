import numpy as np 
import uncertainties.unumpy as unp
from uncertainties import ufloat

def __parseWord(word):
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
    collumns = []
    for line in lines:
        line = line.rstrip()

        indexH = line.find("#")
        if indexH != -1:
            line = line[:indexH]

        # Determine position of collumns
        if len(collumns) == 0:
            if line.strip() == "":
                continue

            collumns = [0]
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
                    collumns.append(i)
                    inArg = True
                    if line[i] == '"':
                        inQuotes = True     
                elif inArg and line[i] == " ":
                    inArg = False

            for i in collumns:
                table.append(list())

        found_last = False
        for i in range(len(collumns)-1):
            if(len(line) <= collumns[i+1]):
                newWord = __parseWord( line[collumns[i]:] )
                table[i].append( newWord )
                found_last = True
                # Fill table with nones so we get a rectangular shape
                for j in range(i+1, len(collumns)):
                    table[j].append( None )
                break
            newWord = __parseWord(line[collumns[i]:collumns[i+1]])
            
            table[i].append(newWord)
    
        if found_last == False:
            newWord = __parseWord(line[collumns[-1]:])
            table[-1].append(newWord)

    return TableHandler(table)

class TableHandler:
    """ Class to handle tables in the internship easily """

    def __init__(self, table = None):        
        """Initalize table, eather from given table or from Filename"""
        self.table = table

    def getDict(self):
        """Retuns a dictionary mapping the first line to its collumns"""
        dicti = {}
        for c in self.table:
            dicti[c[0]] = c[1:]
        return dicti

    def getTransposedTable(self, table = None):
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

    def insertRow(self, row, index = None ):
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
                if type(j) != str and type(j) != chr and j != None:
                    dicti[c[0]].append(j)

        return dicti

    def getRawData(self):
        """Returns only floats and ints"""
        data = []
        for i in self.table:
            data.append([])
        for i in range(len(self.table)):
            for w in self.table[i]:
                if type(w) == float or type(w) == int:
                    data[i].append(w)
        return data

    def makeTexTable(self, filename, useSIUnitX=False, precision=None):
        """Generates a .tex table into file"""
        
        # Generate transposed table
        tTable = self.getTransposedTable()

        # Search length and replace Nones
        maxLen = 0
        for i in range(len(tTable)):
            for j in range(len(tTable[0])):
                if(tTable[i][j] == None):
                    tTable[i][j] = ""
                if maxLen < len(str(tTable[i][j])):
                    maxLen = len(str(tTable[i][j]))

        # account for SIUnitX stuff
        maxLen += 10 

        # Write TeX
        file = open(filename, "w+")                
        for line in tTable:

            for w in line[:-1]:
                newWord = ""
                if type(w)==float or type(w)==int or type(w) == ufloat:
                    if precision != None:
                        newWord = ("{:."+str(int(precision))+"g}").format(w)
                    else:
                        newWord = str(w)
                    if useSIUnitX == True:
                        newWord = r"\num{"+newWord+"}"
                else:
                    newWord = str(w)

                file.write(newWord+(maxLen - len(newWord))*" ")
                
                file.write(" & ")

            newWord = ""
            w = line[-1]
            if type(w)==float or type(w)==int or type(w) == ufloat:
                if precision != None:
                    newWord = ("{:."+str(int(precision))+"g}").format(w)
                else:
                    newWord = str(w)
                if useSIUnitX == True:
                    newWord = r"\num{"+newWord+"}"
            else:
                newWord = str(w)

            file.write(newWord+(maxLen - len(newWord))*" ")
            file.write(r"  \\"+"\n")        
        file.close()

    def getMeanValues(self):
        """Returns the mean values and errors of them as ufloats"""
        rawDict = self.getRawDict()
        meanValues = {}
        for v in rawDict.items():
            meanValues[v[0]] = np.mean(ufloat(np.mean(v[1]), np.std(v[1])))
        return meanValues