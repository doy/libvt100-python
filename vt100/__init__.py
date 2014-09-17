from ctypes import *

import vt100_raw

class vt100_rgb_color(Union):
    _fields_ = [
        ("r", c_ubyte),
        ("g", c_ubyte),
        ("b", c_ubyte),
    ]

class vt100_color(Structure):
    _anonymous_ = ("rgb",)
    _fields_ = [
        ("rgb", vt100_rgb_color),
        ("type", c_ubyte),
    ]

class vt100_named_attrs(Structure):
    _fields_ = [
        ("bold", c_ubyte, 1),
        ("italic", c_ubyte, 1),
        ("underline", c_ubyte, 1),
        ("inverse", c_ubyte, 1),
    ]

class vt100_attrs(Union):
    _anonymous_ = ("named",)
    _fields_ = [
        ("named", vt100_named_attrs),
        ("attrs", c_ubyte),
    ]

class vt100_cell_attrs(Structure):
    _anonymous_ = ("cell_attrs",)
    _fields_ = [
        ("fgcolor", vt100_color),
        ("bgcolor", vt100_color),
        ("cell_attrs", vt100_attrs),
    ]

class vt100_cell(Structure):
    _fields_ = [
        ("_contents", c_char * 8),
        ("len", c_size_t),
        ("attrs", vt100_cell_attrs),
        ("is_wide", c_ubyte, 1),
    ]

    def contents(self):
        return self._contents[:self.len].decode('utf-8')

# XXX process/cell need mutexes
class vt100(object):
    def __init__(self, rows, cols):
        self.vt = vt100_raw.new(rows, cols)

    def __del__(self):
        vt100_raw.delete(self.vt)

    def set_window_size(self, rows, cols):
        vt100_raw.set_window_size(self.vt, rows, cols)

    def process(self, string):
        return vt100_raw.process_string(self.vt, string)

    def get_string_formatted(self, row_start, col_start, row_end, col_end):
        return vt100_raw.get_string_formatted(
            self.vt, row_start, col_start, row_end, col_end
        )

    def get_string_plaintext(self, row_start, col_start, row_end, col_end):
        return vt100_raw.get_string_plaintext(
            self.vt, row_start, col_start, row_end, col_end
        )

    def cell(self, x, y):
        return cast(vt100_raw.cell_at(self.vt, x, y), vt100_cell)
