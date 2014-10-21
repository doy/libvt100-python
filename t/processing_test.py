# coding=utf-8
from . import VT100Test

class ProcessingTest(VT100Test):
    def test_split_escape_sequences(self):
        assert self.vt.process("abc") == 3
        assert self.vt.process("abc\033[12;24Hdef") == 14

        assert self.vt.process("\033") == 0
        assert self.vt.process("\033[") == 0
        assert self.vt.process("\033[1") == 0
        assert self.vt.process("\033[12") == 0
        assert self.vt.process("\033[12;") == 0
        assert self.vt.process("\033[12;2") == 0
        assert self.vt.process("\033[12;24") == 0
        assert self.vt.process("\033[12;24H") == 8

        assert self.vt.process("abc\033") == 3
        assert self.vt.process("abc\033[") == 3
        assert self.vt.process("abc\033[1") == 3
        assert self.vt.process("abc\033[12") == 3
        assert self.vt.process("abc\033[12;") == 3
        assert self.vt.process("abc\033[12;2") == 3
        assert self.vt.process("abc\033[12;24") == 3
        assert self.vt.process("abc\033[12;24H") == 11

        assert self.vt.process("\033") == 0
        assert self.vt.process("\033[") == 0
        assert self.vt.process("\033[?") == 0
        assert self.vt.process("\033[?1") == 0
        assert self.vt.process("\033[?10") == 0
        assert self.vt.process("\033[?100") == 0
        assert self.vt.process("\033[?1000") == 0
        assert self.vt.process("\033[?1000h") == 8

        assert self.vt.process("\033]") == 0
        assert self.vt.process("\033]4") == 0
        assert self.vt.process("\033]49") == 0
        assert self.vt.process("\033]499") == 0
        assert self.vt.process("\033]499;") == 0
        assert self.vt.process("\033]499;a") == 0
        assert self.vt.process("\033]499;a ") == 0
        assert self.vt.process("\033]499;a '") == 0
        assert self.vt.process("\033]499;a '[") == 0
        assert self.vt.process("\033]499;a '[]") == 0
        assert self.vt.process("\033]499;a '[]_") == 0
        assert self.vt.process("\033]499;a '[]_\007") == 13

    def test_split_utf8(self):
        assert self.vt.process("a") == 1

        assert self.vt.process(b"\303") == 0
        assert self.vt.process(b"\303\241") == 2
        assert self.vt.process("á") == 2

        assert self.vt.process(b"\343") == 0
        assert self.vt.process(b"\343\202") == 0
        assert self.vt.process(b"\343\202\255") == 3
        assert self.vt.process("キ") == 3

        assert self.vt.process(b"\360") == 0
        assert self.vt.process(b"\360\237") == 0
        assert self.vt.process(b"\360\237\222") == 0
        assert self.vt.process(b"\360\237\222\251") == 4
        assert self.vt.process("💩") == 4
