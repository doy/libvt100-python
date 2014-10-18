from . import VT100Test

class TextTest(VT100Test):
    def test_ascii(self):
        self.vt.process("foo")
        assert self.vt.cell(0, 0).contents() == "f"
        assert self.vt.cell(0, 1).contents() == "o"
        assert self.vt.cell(0, 2).contents() == "o"
        assert self.vt.cell(0, 3).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'foo' + ('\n' * 24)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'foo' + ('\n' * 24)

    def test_utf8(self):
        self.vt.process("café")
        assert self.vt.cell(0, 0).contents() == "c"
        assert self.vt.cell(0, 1).contents() == "a"
        assert self.vt.cell(0, 2).contents() == "f"
        assert self.vt.cell(0, 3).contents() == "é"
        assert self.vt.cell(0, 4).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'café' + ('\n' * 24)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'café' + ('\n' * 24)

    def test_newlines(self):
        self.vt.process("f\r\noo\r\nood")
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
        self.vt.process("aデbネ")
        assert self.vt.cell(0, 0).contents() == "a"
        assert self.vt.cell(0, 1).contents() == "デ"
        assert self.vt.cell(0, 2).contents() == ""
        assert self.vt.cell(0, 3).contents() == "b"
        assert self.vt.cell(0, 4).contents() == "ネ"
        assert self.vt.cell(0, 5).contents() == ""
        assert self.vt.cell(0, 6).contents() == ""
        assert self.vt.cell(1, 0).contents() == ""
        print(self.vt.get_string_plaintext(0, 0, 0, 50))
        assert self.vt.get_string_plaintext(0, 0, 23, 79) == 'aデbネ' + ('\n' * 24)
        assert self.vt.get_string_plaintext(0, 0, 500, 500) == 'aデbネ' + ('\n' * 24)
