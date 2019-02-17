import unittest


class TableToolTest(unittest.TestCase):

    def setUp(self):
        from praktipy import TableHandler, genfromtxt
        self.th = genfromtxt("data/example_table.txt")

    def test_texTable(self):
        import filecmp

        # Generate a tex table & compare it to the correct result
        self.th.makeTexTable("test_tabletool_res.tex", useSIUnitX=True,
                             precision=10, makeHeader=True, standardRules=True)
        self.assertTrue(filecmp.cmp(
            "test_tabletool_res.tex", "data/test_tabletool.tex"))

if __name__ == '__main__':
    unittest.main()
