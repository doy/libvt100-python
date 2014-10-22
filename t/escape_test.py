from . import VT100Test

class EscapeTest(VT100Test):
    def test_deckpam(self):
        assert not self.vt.application_keypad()
        self.process("\033=")
        assert self.vt.application_keypad()
        self.process("\033>")
        assert not self.vt.application_keypad()

    def test_ri(self):
        self.process("foo\nbar\033Mbaz")
        assert self.vt.window_contents() == 'foo   baz\n   bar' + ('\n' * 23)

    def test_ris(self):
        row, col = self.vt.cursor_position()
        assert row == 0
        assert col == 0

        cell = self.vt.cell(0, 0)
        assert cell.contents() == ""

        assert self.vt.window_contents() == ('\n' * 24)
        assert self.vt.window_contents_formatted() == ('\n' * 24)

        assert self.vt.title() == ""
        assert self.vt.icon_name() == ""

        assert self.vt.fgcolor() is None
        assert self.vt.bgcolor() is None

        assert not self.vt.bold()
        assert not self.vt.italic()
        assert not self.vt.underline()
        assert not self.vt.inverse()

        assert not self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()
        assert not self.vt.seen_visual_bell()
        assert not self.vt.seen_audible_bell()

        self.process("f\033[31m\033[47;1;3;4moo\033[7m\033[21;21H\033]2;window title\007\033]1;window icon name\007\033[?25l\033[?1h\033=\033[?9h\033[?1000h\033[?1002h\033[?1006h\033[?2004h\007\033g")

        row, col = self.vt.cursor_position()
        assert row == 20
        assert col == 20

        cell = self.vt.cell(0, 0)
        assert cell.contents() == "f"

        assert self.vt.window_contents() == 'foo' + ('\n' * 24)
        assert self.vt.window_contents_formatted() == 'f\033[31;47;1;3;4moo' + ('\n' * 24)

        assert self.vt.title() == "window title"
        assert self.vt.icon_name() == "window icon name"

        assert self.vt.fgcolor() == 1
        assert self.vt.bgcolor() == 7

        assert self.vt.bold()
        assert self.vt.italic()
        assert self.vt.underline()
        assert self.vt.inverse()

        assert self.vt.hide_cursor()
        assert self.vt.application_keypad()
        assert self.vt.application_cursor()
        assert self.vt.mouse_reporting_press()
        assert self.vt.mouse_reporting_press_release()
        assert self.vt.mouse_reporting_button_motion()
        assert self.vt.mouse_reporting_sgr_mode()
        assert self.vt.bracketed_paste()
        assert self.vt.seen_visual_bell()
        assert self.vt.seen_audible_bell()

        self.process("\033c")

        row, col = self.vt.cursor_position()
        assert row == 0
        assert col == 0

        cell = self.vt.cell(0, 0)
        assert cell.contents() == ""

        assert self.vt.window_contents() == ('\n' * 24)
        assert self.vt.window_contents_formatted() == ('\n' * 24)

        # title and icon name don't change with reset
        assert self.vt.title() == "window title"
        assert self.vt.icon_name() == "window icon name"

        assert self.vt.fgcolor() is None
        assert self.vt.bgcolor() is None

        assert not self.vt.bold()
        assert not self.vt.italic()
        assert not self.vt.underline()
        assert not self.vt.inverse()

        assert not self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()
        assert not self.vt.seen_visual_bell()
        assert not self.vt.seen_audible_bell()

    def test_vb(self):
        assert not self.vt.seen_visual_bell()
        self.process("\033g")
        assert self.vt.seen_visual_bell()
        assert not self.vt.seen_visual_bell()

    def test_decsc(self):
        self.process("foo\0337\r\n\r\n\r\n         bar\0338baz")
        assert self.vt.window_contents() == 'foobaz\n\n\n         bar' + ('\n' * 21)
