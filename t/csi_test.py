from . import VT100Test

class CSITest(VT100Test):
    def test_cup(self):
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[10;10H")
        assert self.vt.cursor_pos() == (9, 9)

        self.process("\033[H")
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[8H")
        assert self.vt.cursor_pos() == (7, 0)

        self.process("\033[0;0H")
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[1;1H")
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[500;500H")
        assert self.vt.cursor_pos() == (23, 79)

    def test_directional_movement(self):
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[C")
        assert self.vt.cursor_pos() == (0, 1)

        self.process("\033[C")
        assert self.vt.cursor_pos() == (0, 2)

        self.process("\033[20C")
        assert self.vt.cursor_pos() == (0, 22)

        self.process("\033[D")
        assert self.vt.cursor_pos() == (0, 21)

        self.process("\033[D")
        assert self.vt.cursor_pos() == (0, 20)

        self.process("\033[9D")
        assert self.vt.cursor_pos() == (0, 11)

        self.process("\033[500C")
        assert self.vt.cursor_pos() == (0, 79)

        self.process("\033[500D")
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[B")
        assert self.vt.cursor_pos() == (1, 0)

        self.process("\033[B")
        assert self.vt.cursor_pos() == (2, 0)

        self.process("\033[20B")
        assert self.vt.cursor_pos() == (22, 0)

        self.process("\033[A")
        assert self.vt.cursor_pos() == (21, 0)

        self.process("\033[A")
        assert self.vt.cursor_pos() == (20, 0)

        self.process("\033[9A")
        assert self.vt.cursor_pos() == (11, 0)

        self.process("\033[500B")
        assert self.vt.cursor_pos() == (23, 0)

        self.process("\033[500A")
        assert self.vt.cursor_pos() == (0, 0)
