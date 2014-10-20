from . import VT100Test

class EscapeTest(VT100Test):
    def test_deckpam(self):
        assert not self.vt.application_keypad()
        self.vt.process("\033=")
        assert self.vt.application_keypad()
        self.vt.process("\033>")
        assert not self.vt.application_keypad()

    def test_ri(self):
        self.vt.process("foo\nbar\033Mbaz")
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'foo   baz\n   bar' + ('\n' * 23)

    def test_ris(self):
        pass # XXX

    def test_vb(self):
        assert not self.vt.seen_visual_bell()
        self.vt.process("\033g")
        assert self.vt.seen_visual_bell()
        assert not self.vt.seen_visual_bell()

    def test_decsc(self):
        self.vt.process("foo\0337\r\n\r\n\r\n         bar\0338baz")
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'foobaz\n\n\n         bar' + ('\n' * 21)
