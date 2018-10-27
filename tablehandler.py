import numpy as np 
import uncertainties.unumpy as unp
from uncertainties import ufloat


class TableHandler:
    """ Class to handle all tables in the internship """

    def __init__(self, filename):        
        """initialisation, put the filename here!"""
        # Open file and get lines
        with open(filename) as f:
            self.lines = f.readlines()
            f.close()
        
        # Parse table
        self.table = []
        self.collumns = []
        for line in self.lines:
            line = line.rstrip()

            indexH = line.find("#")
            if indexH != -1:
                line = line[:indexH]

            # Determine position of collumns
            if len(self.collumns) == 0:
                if line.strip() == "":
                    continue

                self.collumns = [0]
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
                        self.collumns.append(i)
                        inArg = True
                        if line[i] == '"':
                            inQuotes = True     
                    elif inArg and line[i] == " ":
                        inArg = False

                for i in self.collumns:
                    self.table.append(list())

            found_last = False
            for i in range(len(self.collumns)-1):
                if(len(line) <= self.collumns[i+1]):
                    newWord = self.__parseWord( line[self.collumns[i]:] )
                    if newWord != None:
                        self.table[i].append( newWord )
                    found_last = True
                    break
                newWord = self.__parseWord(line[self.collumns[i]:self.collumns[i+1]])
                if newWord != None:
                    self.table[i].append(newWord)
        
            if found_last == False:
                newWord = self.__parseWord(line[self.collumns[-1]:])
                if newWord != None:
                    self.table[-1].append(newWord)

    def getDict(self):
        """Retuns a dictionary mapping the first line to its collumns"""
        dicti = {}
        for c in self.table:
            dicti[c[0]] = c[1:]
        return dicti

    def getRawDict(self):
        """Returns a dictionary mapping the first line to its non-string collumn values"""
        dicti = {}
        for c in self.table:
            dicti[c[0]] = []
            for j in c[1:]:
                if type(j) != str and type(j) != chr:
                    dicti[c[0]].append(j)

        return dicti

    def getRawData(self):
        """Returns only the non-strings"""
        data = []
        for i in self.table:
            data.append([])
        for i in range(len(self.table)):
            for w in self.table[i]:
                if type(w) == float or type(w) == int:
                    data[i].append(w)
        return data

    def makeTexTable(self, filename):
        """Generates a .tex table into file"""
        
        # Generate transposed table
        tTable = []
        for i in self.table:
            while len(i) > len(tTable):
                tTable.append([])
        for c in self.table:
            for i in range(len(c)):
                tTable[i].append(c[i])
        
        # Search length
        maxLen = 0
        for i in tTable:
            for j in i:
                if maxLen < len(str(j)):
                    maxLen = len(str(j))

        # Write TeX
        file = open(filename, "w+")                
        for line in tTable:
            for w in line[:-1]:
                file.write(str(w)+(maxLen - len(str(w)))*" ")
                file.write(" & ")
            file.write(str(line[-1])+r"  \\"+"\n")            
        file.close()

    def getMeanValues(self):
        """Returns the mean values and errors of them as ufloats"""
        rawDict = self.getRawDict()
        meanValues = {}
        for v in rawDict.items():
            meanValues[v[0]] = np.mean(ufloat(np.mean(v[1]), np.std(v[1])))
        return meanValues

    # Parse a Word
    def __parseWord(self, word):
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
    