# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from spack import *


class Meshlab(QMakePackage):
    """Open source system for processing and editing 3D triangular meshes."""

    homepage = "http://www.meshlab.net"
    url = "https://github.com/cnr-isti-vclab/meshlab/archive/v2016.12.tar.gz"
    git = "https://github.com/cnr-isti-vclab/meshlab"

    maintainers = ['McClunatic']

    version('master', branch='master', submodules=True)

    depends_on('qt@5.9:+opengl')
    depends_on('eigen@3.2:')
    depends_on('glew@2.0:')
    depends_on('bzip2')
    depends_on('glu')
    depends_on('gmp')

    def qmake_args(self):
        """Produces a list containing all the arguments that must be passed to
        qmake
        """
        return ['QMAKE_CXXFLAGS=-fopenmp',
                'CONFIG+=system_eigen3',
                'CONFIG+=system_glew',
                'CONFIG+=system_bzip2']

    def qmake(self, spec, prefix):
        """Run ``qmake`` to configure the project and generate a Makefile."""
        with working_dir('src'):
            super(Meshlab, self).qmake(spec, prefix)

    def build(self, spec, prefix):
        """Make the build targets"""
        with working_dir('src'):
            super(Meshlab, self).build(spec, prefix)

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir('distrib'):
            mkdirp('bin')
            for binary in ['meshlab', 'meshlabserver']:
                copy(binary, 'bin', True)
                force_remove(binary)
            install_tree('.', prefix)

    # Tests

    def check(self):
        """Searches the Makefile for a ``check:`` target and runs it if found.
        """
        with working_dir('src'):
            super(Meshlab, self).check()
