# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install wezterm
#
# You can edit this file again by typing:
#
#     spack edit wezterm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Wezterm(Package):
    """Wez's terminal emulator.

    WezTerm is a powerful cross-platform terminal emulator and multiplexer
    written by @wez and implemented in Rust.
    """

    homepage = "https://wezfurlong.org/wezterm"
    git = "https://github.com/wez/wezterm.git"

    maintainers("McClunatic")

    license("MIT", checked_by="McClunatic")

    version("20240203-110809-5046fc22",
            commit="5046fc225992db6ba2ef8812743fadfdfe4b184a",
            submodules=True)

    depends_on("rust@1.78:", type="build")
    depends_on("perl", type="build")
    depends_on("fontconfig")
    depends_on("libx11")
    depends_on("libxcb")
    depends_on("libxkbcommon")
    depends_on("mesa")
    depends_on("openssl")
    depends_on("wayland")
    depends_on("xcb-util")
    depends_on("xcb-util-image")
    depends_on("xcb-util-keysyms")
    depends_on("xcb-util-wm")
    depends_on("zlib-ng")
    depends_on("xkeyboard-config")

    def setup_build_environment(self, env):
        pass

    def install(self, spec, prefix):
        cargo = Executable("cargo")
        cargo("build", "--release")
        mkdirp(prefix.bin)
        for binary in ("wezterm-mux-server", "wezterm-gui", "wezterm", "strip-ansi-escapes"):
            install(join_path("target", "release", binary), join_path(prefix.bin, binary))
