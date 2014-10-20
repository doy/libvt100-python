from . import VT100Test

class OSCTest(VT100Test):
    def test_title(self):
        assert self.vt.title() == ""
        assert self.vt.icon_name() == ""
        self.process("\033]2;it's a title\007")
        assert self.vt.title() == "it's a title"
        assert self.vt.icon_name() == ""
        self.process("\033]2;\007")
        assert self.vt.title() == ""
        assert self.vt.icon_name() == ""

    def test_icon_name(self):
        assert self.vt.title() == ""
        assert self.vt.icon_name() == ""
        self.process("\033]1;it's an icon name\007")
        assert self.vt.title() == ""
        assert self.vt.icon_name() == "it's an icon name"
        self.process("\033]1;\007")
        assert self.vt.title() == ""
        assert self.vt.icon_name() == ""

    def test_title_icon_name(self):
        assert self.vt.title() == ""
        assert self.vt.icon_name() == ""
        self.process("\033]0;it's both\007")
        assert self.vt.title() == "it's both"
        assert self.vt.icon_name() == "it's both"
        self.process("\033]0;\007")
        assert self.vt.title() == ""
        assert self.vt.icon_name() == ""

    def test_unknown_sequence(self):
        assert self.vt.cell(0, 0).contents() == ""
        self.process("\033]499;some long, long string?\007")
        assert self.vt.cell(0, 0).contents() == ""
