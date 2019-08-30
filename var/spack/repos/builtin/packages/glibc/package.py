# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other # Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class Glibc(AutotoolsPackage):
    """The GNU C Library."""

    homepage = "https://gnu.org/software/libc"
    url = "http://ftp.gnu.org/gnu/libc/glibc-2.16.tar.bz2"

    version('2.16.0',
            sha256='660ffe8ce6d9620796073f9e6f43cbf664d755fc0354f3b9f8930ce76d3bbf4c')

    provides('libc')
    provides('libc@:2.30', when='@2.30:')
    provides('libc@:2.29', when='@2.29:')
    provides('libc@:2.28', when='@2.28:')
    provides('libc@:2.27', when='@2.27:')
    provides('libc@:2.26', when='@2.26:')
    provides('libc@:2.25', when='@2.25:')
    provides('libc@:2.24', when='@2.24:')
    provides('libc@:2.23', when='@2.23:')
    provides('libc@:2.22', when='@2.22:')
    provides('libc@:2.21', when='@2.21:')
    provides('libc@:2.20', when='@2.20:')
    provides('libc@:2.19', when='@2.19:')
    provides('libc@:2.18', when='@2.18:')
    provides('libc@:2.17', when='@2.17:')
    provides('libc@:2.16.0', when='@2.16:')
    provides('libc@:2.15', when='@2.15:')
    provides('libc@:2.14', when='@2.14:')
    provides('libc@:2.13', when='@2.13:')
    provides('libc@:2.12', when='@2.12:')

    variant('binutils',
            default=False,
            description='Build using Spack binutils (assembler and linker)')
    variant('shared',
            default=True,
            description='Build shared libraries')

    depends_on('autoconf')
    depends_on('gettext')
    depends_on('binutils')
    depends_on('texinfo')
    depends_on('perl@5:')
    depends_on('python@3.4:', when='@2.25:')

    build_directory = 'spack-build'

    def configure_args(self):
        spec = self.spec
        options = []

        # Binutils
        if spec.satisfies('+binutils'):
           options.append(
               '--with-binutils={0}'.format(spec['binutils'].prefix.bin))

        # Disabling shared
        if not spec.satisfies('+shared'):
           options.append('--disable-shared')

        return options

    @property
    def libs(self):
        shared = spec.satisfies('+shared')
        for dirname in ['lib64', 'lib']:
            libs = find_libraries(['libc'],
                                  join_path(self.prefix, dirname),
                                  shared=True, recursive=False)
            if libs:
                return libs

    @property
    def linker(self):
        for dirname in ['lib64', 'lib']:
            linker = find_libraries('ld-linux',
                                    join_path(self.prefix, dirname),
                                    shared=True, recursive=False)
            if linker:
                return linker
