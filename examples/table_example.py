# you can use this program as an example on how to use this library

# import the TableHandler Class
import praktipy.tablehandler as th

# Parse in the Table
table = th.gen_from_txt("example_table_visual.txt")

# Print the table
print(table)

# Generate a tex table
th.gen_tex_table(
        table, "example_table.tex",
        tex_caption="Put your laTeX caption here", 
        tex_label="Put your laTex label here",
        # the number of equaly sized subtables 
        # to put split the table into 0 or None to not use subtables 
        subtables=2, 
        # A string representing 
        # the format of the numbers per column
        # in SiUnitX style 
        precision=["2.3", 3, "1.9"], 
        # Where to put the midrule. This also defines the header rows
        midrule=2)
