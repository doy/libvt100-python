from . import VT100Test

class AttrTest(VT100Test):
    def test_colors(self):
        assert self.vt.default_fgcolor() is None
        assert self.vt.default_bgcolor() is None

        self.process("foo\033[31mbar")
        assert self.vt.cell(0, 0).contents() == "f"
        assert self.vt.cell(0, 0).fgcolor() is None
        assert self.vt.cell(0, 0).bgcolor() is None
        assert self.vt.cell(0, 3).contents() == "b"
        assert self.vt.cell(0, 3).fgcolor() == 1
        assert self.vt.cell(0, 3).bgcolor() is None
        assert self.vt.default_fgcolor() == 1
        assert self.vt.default_bgcolor() is None

        self.process("\033[2D\033[45mab")
        assert self.vt.cell(0, 4).contents() == "a"
        assert self.vt.cell(0, 4).fgcolor() == 1
        assert self.vt.cell(0, 4).bgcolor() == 5
        assert self.vt.default_fgcolor() == 1
        assert self.vt.default_bgcolor() == 5

        self.process("\033[m")
        assert self.vt.default_fgcolor() is None
        assert self.vt.default_bgcolor() is None

        self.process("\033[15;15Hfoo\033[31mbar\033[m")
        assert self.vt.cell(14, 14).contents() == "f"
        assert self.vt.cell(14, 14).fgcolor() is None
        assert self.vt.cell(14, 14).bgcolor() is None
        assert self.vt.cell(14, 17).contents() == "b"
        assert self.vt.cell(14, 17).fgcolor() == 1
        assert self.vt.cell(14, 17).bgcolor() is None
        assert self.vt.default_fgcolor() is None
        assert self.vt.default_bgcolor() is None

        self.process("\033[2D\033[45mab")
        assert self.vt.cell(14, 18).contents() == "a"
        assert self.vt.cell(14, 18).fgcolor() is None
        assert self.vt.cell(14, 18).bgcolor() == 5
        assert self.vt.default_fgcolor() is None
        assert self.vt.default_bgcolor() == 5

        self.process("\033[m\033[2J\033[H")
        self.process("a\033[38;5;123mb\033[48;5;158mc")
        assert self.vt.default_fgcolor() == 123
        assert self.vt.default_bgcolor() == 158
        assert self.vt.cell(0, 0).fgcolor() is None
        assert self.vt.cell(0, 0).bgcolor() is None
        assert self.vt.cell(0, 1).fgcolor() == 123
        assert self.vt.cell(0, 1).bgcolor() is None
        assert self.vt.cell(0, 2).fgcolor() == 123
        assert self.vt.cell(0, 2).bgcolor() == 158

        self.process("\033[38;2;50;75;100md\033[48;2;125;150;175me")
        assert self.vt.default_fgcolor() == (50, 75, 100)
        assert self.vt.default_bgcolor() == (125, 150, 175)
        assert self.vt.cell(0, 3).fgcolor() == (50, 75, 100)
        assert self.vt.cell(0, 3).bgcolor() == 158
        assert self.vt.cell(0, 4).fgcolor() == (50, 75, 100)
        assert self.vt.cell(0, 4).bgcolor() == (125, 150, 175)

        self.process("\033[m\033[2J\033[H")
        self.process("\033[32;47mfoo")
        assert self.vt.default_fgcolor() == 2
        assert self.vt.default_bgcolor() == 7
        assert self.vt.cell(0, 1).fgcolor() == 2
        assert self.vt.cell(0, 1).bgcolor() == 7

    def test_attrs(self):
        assert not self.vt.default_bold()
        assert not self.vt.default_italic()
        assert not self.vt.default_underline()
        assert not self.vt.default_inverse()

        self.process("f\033[1mo\033[3mo\033[4mo\033[7mo")
        assert     self.vt.default_bold()
        assert     self.vt.default_italic()
        assert     self.vt.default_underline()
        assert     self.vt.default_inverse()
        assert not self.vt.cell(0, 0).bold()
        assert not self.vt.cell(0, 0).italic()
        assert not self.vt.cell(0, 0).underline()
        assert not self.vt.cell(0, 0).inverse()
        assert     self.vt.cell(0, 1).bold()
        assert not self.vt.cell(0, 1).italic()
        assert not self.vt.cell(0, 1).underline()
        assert not self.vt.cell(0, 1).inverse()
        assert     self.vt.cell(0, 2).bold()
        assert     self.vt.cell(0, 2).italic()
        assert not self.vt.cell(0, 2).underline()
        assert not self.vt.cell(0, 2).inverse()
        assert     self.vt.cell(0, 3).bold()
        assert     self.vt.cell(0, 3).italic()
        assert     self.vt.cell(0, 3).underline()
        assert not self.vt.cell(0, 3).inverse()
        assert     self.vt.cell(0, 4).bold()
        assert     self.vt.cell(0, 4).italic()
        assert     self.vt.cell(0, 4).underline()
        assert     self.vt.cell(0, 4).inverse()

        self.process("\033[m")
        assert not self.vt.default_bold()
        assert not self.vt.default_italic()
        assert not self.vt.default_underline()
        assert not self.vt.default_inverse()

        self.process("\033[2J\033[H")
        self.process("\033[1;4mf")
        assert     self.vt.default_bold()
        assert not self.vt.default_italic()
        assert     self.vt.default_underline()
        assert not self.vt.default_inverse()
        assert     self.vt.cell(0, 0).bold()
        assert not self.vt.cell(0, 0).italic()
        assert     self.vt.cell(0, 0).underline()
        assert not self.vt.cell(0, 0).inverse()

        self.process("\033[22mo\033[24mo")
        assert not self.vt.default_bold()
        assert not self.vt.default_italic()
        assert not self.vt.default_underline()
        assert not self.vt.default_inverse()
        assert not self.vt.cell(0, 1).bold()
        assert not self.vt.cell(0, 1).italic()
        assert     self.vt.cell(0, 1).underline()
        assert not self.vt.cell(0, 1).inverse()
        assert not self.vt.cell(0, 2).bold()
        assert not self.vt.cell(0, 2).italic()
        assert not self.vt.cell(0, 2).underline()
        assert not self.vt.cell(0, 2).inverse()

        self.process("\033[1;3;4;7mo")
        assert     self.vt.default_bold()
        assert     self.vt.default_italic()
        assert     self.vt.default_underline()
        assert     self.vt.default_inverse()
        assert     self.vt.cell(0, 3).bold()
        assert     self.vt.cell(0, 3).italic()
        assert     self.vt.cell(0, 3).underline()
        assert     self.vt.cell(0, 3).inverse()
