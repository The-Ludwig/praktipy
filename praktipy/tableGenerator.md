# My plans for the latex table generator

Idea: 
* Makes a full table header, to just \\input the whole file into latex -> not edit the file by hand anymore
* retain readability in tex table, to be able to look at the .tex source by hand
* Automaticly make uncertainty collumns if a ufloat is detected in the collumn
* Automaticly use SiUnitX, option not to use it is not that smart

Options: 

* caption: str="Caption of table with \caption{}"
* centering: bool ="Whether to \center the table"
* label: str="Lable of table with \label{tab:}
    
* standart rules: bool ="Whether to put \toprule \midrule \bottomrule"
* subtables: int = "number of subtables to split the table into"
* precision: int/int[] ="precision for all columns or every column on its own.
* or:format: str/str[]="example number to format the numbers as such"