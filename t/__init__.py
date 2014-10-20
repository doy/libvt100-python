import unittest

import vt100

class VT100Test(unittest.TestCase):
    def setUp(self):
        self.vt = vt100.vt100(24, 80)

    def process(self, text):
        if type(text) == type(""):
            length = len(text.encode("utf-8"))
        else:
            length = len(text)
        assert self.vt.process(text) == length
