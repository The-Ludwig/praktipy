# you can use this program as an example on how to use this library

# import the TableHandler Class
from praktipy import TableHandler

# Parse in the Table
th = TableHandler("exampleTable.txt")

# Print the mean values with errors
print(th.getMeanValues())

# Generate a tex table
th.makeTexTable("example.tex")
