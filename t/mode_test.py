from . import VT100Test

class ModeTest(VT100Test):
    def test_modes(self):
        assert not self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

        self.process("\033[?1h")

        assert not self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert     self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

        self.process("\033[?9h")

        assert not self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert     self.vt.application_cursor()
        assert     self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

        self.process("\033[?25l")

        assert     self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert     self.vt.application_cursor()
        assert     self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

        self.process("\033[?1000h")

        assert     self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert     self.vt.application_cursor()
        assert     self.vt.mouse_reporting_press()
        assert     self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

        self.process("\033[?1002h")

        assert     self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert     self.vt.application_cursor()
        assert     self.vt.mouse_reporting_press()
        assert     self.vt.mouse_reporting_press_release()
        assert     self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

        self.process("\033[?1006h")

        assert     self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert     self.vt.application_cursor()
        assert     self.vt.mouse_reporting_press()
        assert     self.vt.mouse_reporting_press_release()
        assert     self.vt.mouse_reporting_button_motion()
        assert     self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

        self.process("\033[?2004h")

        assert     self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert     self.vt.application_cursor()
        assert     self.vt.mouse_reporting_press()
        assert     self.vt.mouse_reporting_press_release()
        assert     self.vt.mouse_reporting_button_motion()
        assert     self.vt.mouse_reporting_sgr_mode()
        assert     self.vt.bracketed_paste()

        self.process("\033=")

        assert     self.vt.hide_cursor()
        assert     self.vt.application_keypad()
        assert     self.vt.application_cursor()
        assert     self.vt.mouse_reporting_press()
        assert     self.vt.mouse_reporting_press_release()
        assert     self.vt.mouse_reporting_button_motion()
        assert     self.vt.mouse_reporting_sgr_mode()
        assert     self.vt.bracketed_paste()

        self.process("\033[?1l")

        assert     self.vt.hide_cursor()
        assert     self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert     self.vt.mouse_reporting_press()
        assert     self.vt.mouse_reporting_press_release()
        assert     self.vt.mouse_reporting_button_motion()
        assert     self.vt.mouse_reporting_sgr_mode()
        assert     self.vt.bracketed_paste()

        self.process("\033[?9l")

        assert     self.vt.hide_cursor()
        assert     self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert     self.vt.mouse_reporting_press_release()
        assert     self.vt.mouse_reporting_button_motion()
        assert     self.vt.mouse_reporting_sgr_mode()
        assert     self.vt.bracketed_paste()

        self.process("\033[?25h")

        assert not self.vt.hide_cursor()
        assert     self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert     self.vt.mouse_reporting_press_release()
        assert     self.vt.mouse_reporting_button_motion()
        assert     self.vt.mouse_reporting_sgr_mode()
        assert     self.vt.bracketed_paste()

        self.process("\033[?1000l")

        assert not self.vt.hide_cursor()
        assert     self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert     self.vt.mouse_reporting_button_motion()
        assert     self.vt.mouse_reporting_sgr_mode()
        assert     self.vt.bracketed_paste()

        self.process("\033[?1002l")

        assert not self.vt.hide_cursor()
        assert     self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert     self.vt.mouse_reporting_sgr_mode()
        assert     self.vt.bracketed_paste()

        self.process("\033[?1006l")

        assert not self.vt.hide_cursor()
        assert     self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert     self.vt.bracketed_paste()

        self.process("\033[?2004l")

        assert not self.vt.hide_cursor()
        assert     self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

        self.process("\033>")

        assert not self.vt.hide_cursor()
        assert not self.vt.application_keypad()
        assert not self.vt.application_cursor()
        assert not self.vt.mouse_reporting_press()
        assert not self.vt.mouse_reporting_press_release()
        assert not self.vt.mouse_reporting_button_motion()
        assert not self.vt.mouse_reporting_sgr_mode()
        assert not self.vt.bracketed_paste()

    def test_alternate_buffer(self):
        self.process("\033[m\033[2J\033[H1\r\n2\r\n3\r\n4\r\n5\r\n6\r\n7\r\n8\r\n9\r\n10\r\n11\r\n12\r\n13\r\n14\r\n15\r\n16\r\n17\r\n18\r\n19\r\n20\r\n21\r\n22\r\n23\r\n24")
        assert self.vt.window_contents() == "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n"
        self.process("\033[?1049h")
        assert self.vt.window_contents() == ('\n' * 24)
        self.process("foobar")
        assert self.vt.window_contents() == 'foobar' + ('\n' * 24)
        self.process("\033[?1049l")
        assert self.vt.window_contents() == "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n"
