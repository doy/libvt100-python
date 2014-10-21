# coding=utf-8
from . import VT100Test

class TextTest(VT100Test):
    def test_ascii(self):
        self.process("foo")
        assert self.vt.cell(0, 0).contents() == "f"
        assert self.vt.cell(0, 1).contents() == "o"
        assert self.vt.cell(0, 2).contents() == "o"
        assert self.vt.cell(0, 3).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'foo' + ('\n' * 24)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ('\n' * 24)

    def test_utf8(self):
        self.process("café")
        assert self.vt.cell(0, 0).contents() == "c"
        assert self.vt.cell(0, 1).contents() == "a"
        assert self.vt.cell(0, 2).contents() == "f"
        assert self.vt.cell(0, 3).contents() == u"é"
        assert self.vt.cell(0, 4).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == u'café' + ('\n' * 24)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == u'café' + ('\n' * 24)

    def test_newlines(self):
        self.process("f\r\noo\r\nood")
        assert self.vt.cell(0, 0).contents() == "f"
        assert self.vt.cell(0, 1).contents() == ""
        assert self.vt.cell(0, 2).contents() == ""
        assert self.vt.cell(1, 0).contents() == "o"
        assert self.vt.cell(1, 1).contents() == "o"
        assert self.vt.cell(1, 2).contents() == ""
        assert self.vt.cell(2, 0).contents() == "o"
        assert self.vt.cell(2, 1).contents() == "o"
        assert self.vt.cell(2, 2).contents() == "d"
        assert self.vt.cell(0, 3).contents() == ""
        assert self.vt.cell(3, 0).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'f\noo\nood' + ('\n' * 22)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'f\noo\nood' + ('\n' * 22)

    def test_wide(self):
        self.process("aデbネ")
        assert self.vt.cell(0, 0).contents() == "a"
        assert self.vt.cell(0, 1).contents() == u"デ"
        assert self.vt.cell(0, 2).contents() == ""
        assert self.vt.cell(0, 3).contents() == "b"
        assert self.vt.cell(0, 4).contents() == u"ネ"
        assert self.vt.cell(0, 5).contents() == ""
        assert self.vt.cell(0, 6).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        print(self.vt.get_string_plaintext(0, 0, 0, 50))
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == u'aデbネ' + ('\n' * 24)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == u'aデbネ' + ('\n' * 24)

    def test_combining(self):
        self.process("a")
        assert self.vt.cell(0, 0).contents() == "a"
        self.process(u"\u0301".encode('utf-8'))
        assert self.vt.cell(0, 0).contents() == u"á"
        self.process("\033[20;20Habcdefg")
        assert self.vt.get_string_plaintext(19, 19, 19, 26) == "abcdefg"
        self.process(u"\033[20;25H\u0301".encode('utf-8'))
        assert self.vt.get_string_plaintext(19, 19, 19, 26) == u"abcdéfg"
        self.process("\033[10;78Haaa")
        assert self.vt.cell(9, 79).contents() == "a"
        self.process(u"\r\n\u0301".encode('utf-8'))
        assert self.vt.cell(9, 79).contents() == "a"
        assert self.vt.cell(10, 0).contents() == ""

    def test_wrap(self):
        self.process("0123456789" * 10)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("0123456789" * 10) + ("\n" * 23)
        self.process("\033[5H" + "0123456789" * 8)
        self.process("\033[6H" + "0123456789" * 8)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == ("0123456789" * 10) + ("\n" * 3) + ("0123456789" * 8) + "\n" + ("0123456789" * 8) + ("\n" * 19)
