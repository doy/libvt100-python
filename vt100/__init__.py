from ctypes import *

import vt100_raw

class vt100_rgb_color(Structure):
    _fields_ = [
        ("_r", c_ubyte),
        ("_g", c_ubyte),
        ("_b", c_ubyte),
    ]

class vt100_color_type(Union):
    _anonymous_ = ("_rgb",)
    _fields_ = [
        ("_rgb", vt100_rgb_color),
        ("_idx", c_ubyte),
    ]

class vt100_color_def(Structure):
    _anonymous_ = ("_color",)
    _fields_ = [
        ("_color", vt100_color_type),
        ("_type", c_ubyte),
    ]

class vt100_color(Union):
    _anonymous_ = ("_color",)
    _fields_ = [
        ("_color", vt100_color_def),
        ("_id", c_uint32),
    ]

    def type(self):
        if self._type == 0:
            return "default"
        elif self._type == 1:
            return "indexed"
        elif self._type == 2:
            return "rgb"
        else:
            raise Exception("unknown color type: %d" % self._type)

    def color(self):
        color_type = self.type()
        if color_type == "default":
            return None
        elif color_type == "indexed":
            return self._idx
        elif color_type == "rgb":
            return (self._r, self._g, self._b)
        else:
            raise Exception("unknown color type: %s" % color_type)

class vt100_named_attrs(Structure):
    _fields_ = [
        ("_bold", c_ubyte, 1),
        ("_italic", c_ubyte, 1),
        ("_underline", c_ubyte, 1),
        ("_inverse", c_ubyte, 1),
    ]

class vt100_attrs(Union):
    _anonymous_ = ("_named",)
    _fields_ = [
        ("_named", vt100_named_attrs),
        ("_attrs", c_ubyte),
    ]

class vt100_cell_attrs(Structure):
    _anonymous_ = ("_cell_attrs",)
    _fields_ = [
        ("_fgcolor", vt100_color),
        ("_bgcolor", vt100_color),
        ("_cell_attrs", vt100_attrs),
    ]

class vt100_cell(Structure):
    _fields_ = [
        ("_contents", c_char * 8),
        ("_len", c_size_t),
        ("_attrs", vt100_cell_attrs),
        ("_is_wide", c_ubyte, 1),
    ]

    def contents(self):
        return self._contents[:self._len].decode('utf-8')

    def fgcolor(self):
        return self._attrs._fgcolor

    def bgcolor(self):
        return self._attrs._bgcolor

    def all_attrs(self):
        return self._attrs._attrs

    def bold(self):
        return self._attrs._bold != 0

    def italic(self):
        return self._attrs._italic != 0

    def underline(self):
        return self._attrs._underline != 0

    def inverse(self):
        return self._attrs._inverse != 0

    def is_wide(self):
        return self._is_wide != 0

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
        return vt100_cell.from_address(vt100_raw.cell_at(self.vt, x, y))
