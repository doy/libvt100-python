import hexdump

import vt100

vt = vt100.vt100(24, 80)
string = b"foo\033[31m\033[32mb\033[3;7;42ma\033[23mr"
vt.process(string)

hexdump.hexdump(vt.get_string_plaintext(0, 0, 0, 50))
hexdump.hexdump(vt.get_string_formatted(0, 0, 0, 50))
print(vt.cell(0, 4).contents())
