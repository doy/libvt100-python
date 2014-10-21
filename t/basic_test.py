import unittest

import vt100

class BasicTest(unittest.TestCase):
    def test_basic(self):
        vt = vt100.vt100(24, 80)
        string = b"foo\033[31m\033[32mb\033[3;7;42ma\033[23mr"
        vt.process(string)
        assert vt.get_string_plaintext(0, 0, 0, 50) == "foobar\n"
        assert vt.cell(0, 0).fgcolor() is None
        assert vt.cell(0, 3).fgcolor() == 2
        assert vt.cell(0, 4).fgcolor() == 2
        assert vt.cell(0, 4).bgcolor() == 2
        assert vt.cell(0, 4).italic()
