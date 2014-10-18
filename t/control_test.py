from . import VT100Test

class ControlTest(VT100Test):
    def test_bel(self):
        assert not self.vt.seen_audible_bell()
        self.vt.process("\a")
        assert self.vt.seen_audible_bell()
        assert not self.vt.seen_audible_bell()

    def test_bs(self):
        self.vt.process("foo\b\baa")
        assert self.vt.cell(0, 0).contents() == "f"
        assert self.vt.cell(0, 1).contents() == "a"
        assert self.vt.cell(0, 2).contents() == "a"
        assert self.vt.cell(0, 3).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'faa' + ('\n' * 24)
        self.vt.process("\r\nquux\b\b\b\b\b\bbar")
        assert self.vt.cell(1, 0).contents() == "b"
        assert self.vt.cell(1, 1).contents() == "a"
        assert self.vt.cell(1, 2).contents() == "r"
        assert self.vt.cell(1, 3).contents() == "x"
        assert self.vt.cell(1, 4).contents() == ""
        assert self.vt.cell(2, 0).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'faa\nbarx' + ('\n' * 23)

    def test_tab(self):
        self.vt.process("foo\tbar")
        assert self.vt.cell(0, 0).contents() == "f"
        assert self.vt.cell(0, 1).contents() == "o"
        assert self.vt.cell(0, 2).contents() == "o"
        assert self.vt.cell(0, 3).contents() == ""
        assert self.vt.cell(0, 4).contents() == ""
        assert self.vt.cell(0, 5).contents() == ""
        assert self.vt.cell(0, 6).contents() == ""
        assert self.vt.cell(0, 7).contents() == ""
        assert self.vt.cell(0, 8).contents() == "b"
        assert self.vt.cell(0, 9).contents() == "a"
        assert self.vt.cell(0, 10).contents() == "r"
        assert self.vt.cell(0, 11).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'foo     bar' + ('\n' * 24)

    def test_lf(self):
        self.vt.process("foo\nbar")
        assert self.vt.cell(0, 0).contents() == "f"
        assert self.vt.cell(0, 1).contents() == "o"
        assert self.vt.cell(0, 2).contents() == "o"
        assert self.vt.cell(0, 3).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        assert self.vt.cell(1, 1).contents() == ""
        assert self.vt.cell(1, 2).contents() == ""
        assert self.vt.cell(1, 3).contents() == "b"
        assert self.vt.cell(1, 4).contents() == "a"
        assert self.vt.cell(1, 5).contents() == "r"
        assert self.vt.cell(1, 6).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'foo\n   bar' + ('\n' * 23)

    def test_cr(self):
        self.vt.process("fooo\rbar")
        assert self.vt.cell(0, 0).contents() == "b"
        assert self.vt.cell(0, 1).contents() == "a"
        assert self.vt.cell(0, 2).contents() == "r"
        assert self.vt.cell(0, 3).contents() == "o"
        assert self.vt.cell(0, 4).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'baro' + ('\n' * 24)
