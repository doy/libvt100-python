from . import VT100Test

class CSITest(VT100Test):
    def test_absolute_movement(self):
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[10;10H")
        assert self.vt.cursor_pos() == (9, 9)

        self.process("\033[d")
        assert self.vt.cursor_pos() == (0, 9)

        self.process("\033[15d")
        assert self.vt.cursor_pos() == (14, 9)

        self.process("\033[H")
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[8H")
        assert self.vt.cursor_pos() == (7, 0)

        self.process("\033[15G")
        assert self.vt.cursor_pos() == (7, 14)

        self.process("\033[G")
        assert self.vt.cursor_pos() == (7, 0)

        self.process("\033[0;0H")
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[1;1H")
        assert self.vt.cursor_pos() == (0, 0)

        self.process("\033[500;500H")
        assert self.vt.cursor_pos() == (23, 79)

    def test_relative_movement(self):
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

    def test_ed(self):
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("foo\033[5;5Hbar\033[10;10Hbaz\033[20;20Hquux")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         baz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[10;12H\033[0J")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         ba' + ("\n" * 15)

        self.process("\033[5;7H\033[1J")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 4) + '      r' + ("\n" * 5) + '         ba' + ("\n" * 15)

        self.process("\033[7;7H\033[2J")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("\033[2J\033[H")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("foo\033[5;5Hbar\033[10;10Hbaz\033[20;20Hquux")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         baz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[10;12H\033[J")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         ba' + ("\n" * 15)

        self.process("\033[2J\033[H")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("foo\033[5;5Hbar\033[10;10Hbaz\033[20;20Hquux")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         baz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[10;12H\033[?0J")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         ba' + ("\n" * 15)

        self.process("\033[5;7H\033[?1J")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 4) + '      r' + ("\n" * 5) + '         ba' + ("\n" * 15)

        self.process("\033[7;7H\033[?2J")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("\033[2J\033[H")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("foo\033[5;5Hbar\033[10;10Hbaz\033[20;20Hquux")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         baz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[10;12H\033[?J")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         ba' + ("\n" * 15)

    def test_el(self):
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("foo\033[5;5Hbarbar\033[10;10Hbazbaz\033[20;20Hquux")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    barbar' + ("\n" * 5) + '         bazbaz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[5;8H\033[0K")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         bazbaz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[10;13H\033[1K")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '            baz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[20;22H\033[2K")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '            baz' + ("\n" * 15)

        self.process("\033[1;2H\033[K")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'f' + ("\n" * 4) + '    bar' + ("\n" * 5) + '            baz' + ("\n" * 15)

        self.process("\033[2J\033[H")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("foo\033[5;5Hbarbar\033[10;10Hbazbaz\033[20;20Hquux")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    barbar' + ("\n" * 5) + '         bazbaz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[5;8H\033[?0K")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '         bazbaz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[10;13H\033[?1K")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '            baz' + ("\n" * 10) + '                   quux' + ("\n" * 5)

        self.process("\033[20;22H\033[?2K")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ("\n" * 4) + '    bar' + ("\n" * 5) + '            baz' + ("\n" * 15)

        self.process("\033[1;2H\033[?K")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'f' + ("\n" * 4) + '    bar' + ("\n" * 5) + '            baz' + ("\n" * 15)

    def test_ich_dch_ech(self):
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("\033[10;10Hfoobar")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         foobar' + ("\n" * 15)

        self.process("\033[10;12H\033[3@")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         fo   obar' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 11)

        self.process("\033[4P")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         fobar' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 11)

        self.process("\033[100@")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         fo' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 11)

        self.process("obar")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         foobar' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 15)

        self.process("\033[10;12H\033[100P")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         fo' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 11)

        self.process("obar")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         foobar' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 15)

        self.process("\033[10;13H\033[X")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         foo ar' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 12)

        self.process("\033[10;11H\033[4X")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         f    r' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 10)

        self.process("\033[10;11H\033[400X")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         f' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 10)

    def test_il_dl(self):
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("\033[10;10Hfoobar\033[3D")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         foobar' + ("\n" * 15)
        assert self.vt.cursor_pos() == (9, 12)

        self.process("\033[L")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 10) + '         foobar' + ("\n" * 14)
        assert self.vt.cursor_pos() == (9, 12)

        self.process("\033[3L")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 13) + '         foobar' + ("\n" * 11)
        assert self.vt.cursor_pos() == (9, 12)

        self.process("\033[500L")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)
        assert self.vt.cursor_pos() == (9, 12)

        self.process("\033[10;10Hfoobar\033[3D\033[6A")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 9) + '         foobar' + ("\n" * 15)
        assert self.vt.cursor_pos() == (3, 12)

        self.process("\033[M")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 8) + '         foobar' + ("\n" * 16)
        assert self.vt.cursor_pos() == (3, 12)

        self.process("\033[3M")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 5) + '         foobar' + ("\n" * 19)
        assert self.vt.cursor_pos() == (3, 12)

        self.process("\033[500M")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)
        assert self.vt.cursor_pos() == (3, 12)

    def test_scroll(self):
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("\n" * 24)

        self.process("1\r\n2\r\n3\r\n4\r\n5\r\n6\r\n7\r\n8\r\n9\r\n10\r\n11\r\n12\r\n13\r\n14\r\n15\r\n16\r\n17\r\n18\r\n19\r\n20\r\n21\r\n22\r\n23\r\n24")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n"

        self.process("\033[15;15H")
        assert self.vt.cursor_pos() == (14, 14)

        self.vt.process("\033[S")
        print(self.vt.get_string_plaintext(0, 0, 500, 500).replace('\n', '\\n'))
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == "2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n\n"
        assert self.vt.cursor_pos() == (14, 14)

        self.vt.process("\033[3S")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == "5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n\n\n\n\n"
        assert self.vt.cursor_pos() == (14, 14)

        self.vt.process("\033[T")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == "\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n\n\n\n"
        assert self.vt.cursor_pos() == (14, 14)

        self.vt.process("\033[5T")
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == "\n\n\n\n\n\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n"
        assert self.vt.cursor_pos() == (14, 14)
