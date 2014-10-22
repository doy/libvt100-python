from . import VT100Test

class InitTest(VT100Test):
    def test_init(self):
        assert self.vt.window_size() == (24, 80)

        row, col = self.vt.cursor_position()
        assert row == 0
        assert col == 0

        cell = self.vt.cell(0, 0)
        assert cell.contents() == ""
        cell = self.vt.cell(23, 79)
        assert cell.contents() == ""
        cell = self.vt.cell(24, 0)
        assert cell is None
        cell = self.vt.cell(0, 80)
        assert cell is None

        assert self.vt.window_contents(0, 0, 500, 500) == ('\n' * 24)
        assert self.vt.window_contents_formatted(0, 0, 500, 500) == ('\n' * 24)

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
