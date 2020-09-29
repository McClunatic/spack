# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# from spack import *
from spack.build_systems.autotools import AutotoolsPackage
from spack.directives import (
    depends_on,
    patch,
    variant,
    version,
)
from llnl.util.filesystem import join_path, install, mkdirp, working_dir


class Mutil(AutotoolsPackage):
    """Multi-thread/Multi-Node Utilities.

    Mutil provides drop-in replacements for cp and md5sum that utilize
    multiple types of parallelism to achieve maximum copy and checksum
    performance on clustered file systems.
    """

    homepage = 'https://code.nasa.gov/?tag=mutil'

    build_directory = 'spack-build'

    version(
        '1.822.6',
        sha256='5b3e94998152c017e6c75d56b9b994188eb71bf46d4038a642cb9141f6ff1212',  # noqa: E501
        url='http://ftpmirror.gnu.org/coreutils/coreutils-8.22.tar.xz',
    )

    variant(
        'static',
        default=False,
        description='statically link libgcrypt, libgpg-error, and gnutls',
    )
    variant(
        'tcp',
        default=False,
        description='build with multi-node TCP support',
    )
    variant(
        'mpi',
        default=False,
        description='build with multi-node MPI support',
    )

    depends_on('autoconf@2.69', type='build')
    depends_on('automake@1.14.1', type='build')
    depends_on('libgcrypt@1.6.2')
    depends_on('libgpg-error@1.17:')
    depends_on('zlib', when='+static')
    depends_on('gnutls@3.5.19', when='+tcp')
    depends_on('mpi', when='+mpi')

    patch(
        'https://raw.githubusercontent.com/pkolano/mutil/edac76b163513e4b7ca7bed094f191cb6d0c1fb3/patch/coreutils-8.22.patch',  # noqa: E501
        sha256='8c8cce51cbe673d1de5278444adf044e9ed03b909414ad71843a6e32f4cc4c6d',  # noqa: E501
        when='@1.822.6',
    )

    def configure_args(self):
        configure_args = []
        # TODO: fix static build, not working with GCC 7.4.0 (Ubuntu 18.04 LTS)
        if "+static" in self.spec:
            configure_args.append('--with-static-gcrypt')
            if self.spec.satisfies('%gcc@4.3:'):
                configure_args.append('CFLAGS=-g -O2 -fgnu89-inline')
            elif self.spec.satisfies('%gcc@4.2:'):
                configure_args.append('CFLAGS=-g -O2')

        return configure_args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(join_path(prefix.man, 'man1'))
        with working_dir('spack-build'):
            install(join_path('src', 'cp'), join_path(prefix.bin, 'mcp'))
            install(join_path('src', 'md5sum'), join_path(prefix.bin, 'msum'))
            install(join_path('man', 'cp.1'),
                    join_path(prefix.man, 'man1', 'mcp.1'))
            install(join_path('man', 'md5sum.1'),
                    join_path(prefix.man, 'man1', 'msum.1'))
