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

    def color(self):
        color_type = self._type
        if color_type == 0:
            return None
        elif color_type == 1:
            return self._idx
        elif color_type == 2:
            return (self._r, self._g, self._b)
        else:
            raise Exception("unknown color type: %d" % color_type)

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
        return self._attrs._fgcolor.color()

    def bgcolor(self):
        return self._attrs._bgcolor.color()

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

class vt100_loc(Structure):
    _fields_ = [
        ("row", c_int),
        ("col", c_int),
    ]

class vt100_grid(Structure):
    _fields_ = [
        ("_cur", vt100_loc),
        ("_max", vt100_loc),
        ("_saved", vt100_loc),
        ("_scroll_top", c_int),
        ("_scroll_bottom", c_int),
        ("_row_count", c_int),
        ("_row_capacity", c_int),
        ("_row_top", c_int),
        ("_rows", c_void_p),
    ]

class vt100_screen(Structure):
    _fields_ = [
        ("_grid", POINTER(vt100_grid)),
        ("_alternate", POINTER(vt100_grid)),
        ("_title", c_char_p),
        ("_title_len", c_size_t),
        ("_icon_name", c_char_p),
        ("_icon_name_len", c_size_t),
        ("_attrs", vt100_cell_attrs),
        ("_scrollback_length", c_int),
        ("_parser_state", c_void_p),
        ("_hide_cursor", c_ubyte, 1),
        ("_application_keypad", c_ubyte, 1),
        ("_application_cursor", c_ubyte, 1),
        ("_mouse_reporting_press", c_ubyte, 1),
        ("_mouse_reporting_press_release", c_ubyte, 1),
        ("_mouse_reporting_button_motion", c_ubyte, 1),
        ("_mouse_reporting_sgr_mode", c_ubyte, 1),
        ("_bracketed_paste", c_ubyte, 1),
        ("_visual_bell", c_ubyte, 1),
        ("_audible_bell", c_ubyte, 1),
        ("_update_title", c_ubyte, 1),
        ("_update_icon_name", c_ubyte, 1),
        ("_dirty", c_ubyte, 1),
        ("_custom_scrollback_length", c_ubyte, 1),
    ]

# XXX process/cell need mutexes
class vt100(object):
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._screen = vt100_screen.from_address(vt100_raw.new(rows, cols))

    def __del__(self):
        vt100_raw.delete(addressof(self._screen))

    def window_size(self):
        return self._rows, self._cols

    def set_window_size(self, rows, cols):
        self._rows = rows
        self._cols = cols
        vt100_raw.set_window_size(addressof(self._screen), rows, cols)

    def process(self, string):
        return vt100_raw.process_string(addressof(self._screen), string)

    def window_contents(self, row_start=0, col_start=0, row_end=None, col_end=None):
        if row_end is None:
            row_end = self._rows - 1
        if col_end is None:
            col_end = self._cols - 1
        row_start = min(max(row_start, 0), self._rows - 1)
        col_start = min(max(col_start, 0), self._cols - 1)
        row_end = min(max(row_end, 0), self._rows - 1)
        col_end = min(max(col_end, 0), self._cols - 1)
        return vt100_raw.get_string_plaintext(
            addressof(self._screen), row_start, col_start, row_end, col_end
        ).decode('utf-8')

    def window_contents_formatted(self, row_start=0, col_start=0, row_end=None, col_end=None):
        if row_end is None:
            row_end = self._rows - 1
        if col_end is None:
            col_end = self._cols - 1
        row_start = min(max(row_start, 0), self._rows - 1)
        col_start = min(max(col_start, 0), self._cols - 1)
        row_end = min(max(row_end, 0), self._rows - 1)
        col_end = min(max(col_end, 0), self._cols - 1)
        return vt100_raw.get_string_formatted(
            addressof(self._screen), row_start, col_start, row_end, col_end
        ).decode('utf-8')

    def cell(self, row, col):
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return None
        return vt100_cell.from_address(
            vt100_raw.cell_at(addressof(self._screen), row, col)
        )

    def cursor_position(self):
        pos = self._screen._grid.contents._cur
        return pos.row, pos.col

    def title(self):
        title_str = self._screen._title
        if title_str is None:
            return ""
        else:
            return title_str[:self._screen._title_len].decode('utf-8')

    def icon_name(self):
        icon_name_str = self._screen._icon_name
        if icon_name_str is None:
            return ""
        else:
            return icon_name_str[:self._screen._icon_name_len].decode('utf-8')

    def fgcolor(self):
        return self._screen._attrs._fgcolor.color()

    def bgcolor(self):
        return self._screen._attrs._bgcolor.color()

    def all_attrs(self):
        return self._screen._attrs._attrs

    def bold(self):
        return self._screen._attrs._bold != 0

    def italic(self):
        return self._screen._attrs._italic != 0

    def underline(self):
        return self._screen._attrs._underline != 0

    def inverse(self):
        return self._screen._attrs._inverse != 0

    def hide_cursor(self):
        return self._screen._hide_cursor != 0

    def application_keypad(self):
        return self._screen._application_keypad != 0

    def application_cursor(self):
        return self._screen._application_cursor != 0

    def mouse_reporting_press(self):
        return self._screen._mouse_reporting_press != 0

    def mouse_reporting_press_release(self):
        return self._screen._mouse_reporting_press_release != 0

    def mouse_reporting_button_motion(self):
        return self._screen._mouse_reporting_button_motion != 0

    def mouse_reporting_sgr_mode(self):
        return self._screen._mouse_reporting_sgr_mode != 0

    def bracketed_paste(self):
        return self._screen._bracketed_paste != 0

    def alternate_buffer_active(self):
        return bool(self._screen._alternate)

    def seen_visual_bell(self):
        seen = self._screen._visual_bell
        self._screen._visual_bell = 0
        return seen != 0

    def seen_audible_bell(self):
        seen = self._screen._audible_bell
        self._screen._audible_bell = 0
        return seen != 0
