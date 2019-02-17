# you can use this program as an example on how to use this library

# import the TableHandler Class
from praktipy import TableHandler, genfromtxt

# Parse in the Table
th = genfromtxt("example_table.txt")

# Print the mean values with errors
print(th.getMeanValues())

# Generate a tex table
th.makeTexTable("example.tex", useSIUnitX=True, precision=10, makeHeader=True, standardRules=True)
