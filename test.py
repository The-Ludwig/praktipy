import praktipy.tablehandler as th
table = th.gen_from_txt("./examples/example_table_visual.txt", False)
th.gen_full_tex_table(table, "", "", "", "", 3, "")
    