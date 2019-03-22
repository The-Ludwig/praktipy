import unittest


class TableToolTest(unittest.TestCase):

    def setUp(self):
        from praktipy import tablehandler as th
        self.th = th
        self.table = th.gen_from_txt("data/example_table_visual.txt")

    def test_texTable(self):
        import filecmp

        # Generate a tex table & compare it to the correct result
        self.th.gen_tex_table(table=self.table, filename="test_tabletool_res.tex",
                              tex_caption="TestCaption", tex_label="TestLabel",
                              subtables=2, precision=["2.4", "2.1", "2.3"], midrule=2)
        self.assertTrue(filecmp.cmp(
            "test_tabletool_res.tex", "data/test_tabletool.tex"))

if __name__ == '__main__':
    unittest.main()
