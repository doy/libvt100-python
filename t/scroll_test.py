from . import VT100Test

class ScrollTest(VT100Test):
    def test_scroll_regions(self):
        self.process("\033[m\033[2J\033[H1\r\n2\r\n3\r\n4\r\n5\r\n6\r\n7\r\n8\r\n9\r\n10\r\n11\r\n12\r\n13\r\n14\r\n15\r\n16\r\n17\r\n18\r\n19\r\n20\r\n21\r\n22\r\n23\r\n24")
        assert self.vt.window_contents() == "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n"

        self.process("\033[24;50H\n")
        assert self.vt.window_contents() == "2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n\n"

        self.process("\033[m\033[2J\033[H1\r\n2\r\n3\r\n4\r\n5\r\n6\r\n7\r\n8\r\n9\r\n10\r\n11\r\n12\r\n13\r\n14\r\n15\r\n16\r\n17\r\n18\r\n19\r\n20\r\n21\r\n22\r\n23\r\n24")
        self.process("\033[10;20r\033[20;50H\n")
        assert self.vt.window_contents() == "1\n2\n3\n4\n5\n6\n7\n8\n9\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n\n21\n22\n23\n24\n"
        assert self.vt.cursor_position() == (19, 49)

        self.process("\033[B")
        assert self.vt.cursor_position() == (19, 49)

        self.process("\033[20A")
        assert self.vt.cursor_position() == (9, 49)
        self.process("\033[1;24r\033[m\033[2J\033[H1\r\n2\r\n3\r\n4\r\n5\r\n6\r\n7\r\n8\r\n9\r\n10\r\n11\r\n12\r\n13\r\n14\r\n15\r\n16\r\n17\r\n18\r\n19\r\n20\r\n21\r\n22\r\n23\r\n24")
        self.process("\033[10;20r\033[15;50H\033[2L")
        assert self.vt.window_contents() == "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n\n\n15\n16\n17\n18\n21\n22\n23\n24\n"
        self.process("\033[10;50H\033M")
        assert self.vt.window_contents() == "1\n2\n3\n4\n5\n6\n7\n8\n9\n\n10\n11\n12\n13\n14\n\n\n15\n16\n17\n21\n22\n23\n24\n"
