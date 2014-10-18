import unittest

import vt100

class VT100Test(unittest.TestCase):
    def setUp(self):
        self.vt = vt100.vt100(24, 80)
