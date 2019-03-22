import praktipy.tablehandler as th
table = th.gen_from_txt("./examples/example_table_long.txt", False)
th.gen_tex_table(table=table, filename="test.tex", tex_caption="TestCaption", tex_label="TestLable"
                 , subtables=4, precision="", midrule=2)
    