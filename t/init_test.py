from . import VT100Test

class InitTest(VT100Test):
    def test_init(self):
        assert self.vt.rows == 24
        assert self.vt.cols == 80

        row, col = self.vt.cursor_pos()
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

        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ('\n' * 24)
        assert self.vt.get_string_formatted(0, 0, 500, 500) == ('\n' * 24)

        assert self.vt.title() == ""
        assert self.vt.icon_name() == ""

        color = self.vt.default_fgcolor()
        assert color.color() is None
        color = self.vt.default_bgcolor()
        assert color.color() is None

        assert not self.vt.default_bold()
        assert not self.vt.default_italic()
        assert not self.vt.default_underline()
        assert not self.vt.default_inverse()

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
