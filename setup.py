from distutils.core import setup, Extension
import subprocess

# http://code.activestate.com/recipes/502261-python-distutils-pkg-config/
def pkgconfig(*packages, **kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    args = ["pkg-config", "--libs", "--cflags"]
    args.extend(packages)
    for token in subprocess.check_output(args).split():
        token = token.decode('utf-8')
        kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
    return kw

setup(
    name="vt100",
    version="0.3.0",
    description="an in-memory terminal parsing library",
    author="Jesse Luehrs",
    author_email="doy@tozt.net",
    url="https://github.com/doy/libvt100-python/",
    license="MIT License",
    packages=["vt100"],
    ext_modules=[
        Extension(
            name="vt100_raw",
            sources=[
                "vt100module.c",
                "libvt100/src/screen.c",
                "libvt100/src/parser.c",
                "libvt100/src/unicode-extra.c",
            ],
            depends=[
                "libvt100/src/screen.h",
                "libvt100/src/parser.h",
                "libvt100/src/unicode-extra.h",
                "libvt100/src/vt100.h",
            ],
            **pkgconfig('glib-2.0')
        )
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Terminals :: Terminal Emulators/X Terminals",
    ],
)
