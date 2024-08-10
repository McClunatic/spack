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
#     spack install helix
#
# You can edit this file again by typing:
#
#     spack edit helix
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Helix(Package):
    """A post-modern text editor.

    Helix is a modal editor with multiple cursors, tree-sitter integration,
    language server support and more. It is built in Rust and has no dependencies
    on Electron, VimScript or JavaScript.
    """

    homepage = "https://helix-editor.com"
    url = "https://github.com/helix-editor/helix/archive/refs/tags/24.07.tar.gz"

    maintainers("McClunatic")

    license("MPL-2.0", checked_by="McClunatic")

    version("24.07", sha256="0f466ed2de039a7eca6faf29fc0db712c92e1a59d0bdc7e8916c717ceee8b3b3")

    depends_on("rust@1.78:", type="build")

    variant("grammars", default=True, description="Fetch and build grammars.")

    def setup_build_environment(self, env):
        if self.spec.satisfies("~grammars"):
            env.set("HELIX_DISABLE_AUTO_GRAMMAR_BUILD", "true")

    def install(self, spec, prefix):
        cargo = Executable("cargo")
        cargo("install", "--path", "helix-term", "--root", prefix, "--locked")
        install_tree("runtime", join_path(prefix.bin, "runtime"))
