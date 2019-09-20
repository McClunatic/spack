# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dakota(CMakePackage):
    """The Dakota toolkit provides a flexible, extensible interface between
    analysis codes and iterative systems analysis methods. Dakota
    contains algorithms for:

    - optimization with gradient and non gradient-based methods;
    - uncertainty quantification with sampling, reliability, stochastic
    - expansion, and epistemic methods;
    - parameter estimation with nonlinear least squares methods;
    - sensitivity/variance analysis with design of experiments and
    - parameter study methods.

    These capabilities may be used on their own or as components within
    advanced strategies such as hybrid optimization, surrogate-based
    optimization, mixed integer nonlinear programming, or optimization
    under uncertainty.

    """

    homepage = 'https://dakota.sandia.gov/'
    url = 'https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.3-public.src.tar.gz'

    version('6.9', 'a3993709c7b2ef94b44da4544dc06275', url='https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.9-release-public-src.zip')
    version('6.3', '05a58d209fae604af234c894c3f73f6d')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('hdf5', default=True,
            description='Activates HDF5 support')
    variant('trilinos', default=True,
            description='Activates Trilinos Teuchos support')
    variant('openblas', default=True,
            description='Hints for OpenBLAS for BLAS LAPACK support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')
    depends_on('python')
    depends_on('boost@1.49.0:1.67.0')
    depends_on('cmake@2.8.9:', type='build')
    depends_on('hdf5+cxx+fortran+hl+mpi', when='+hdf5')
    depends_on('trilinos+rol+teuchos+complex', when='+trilinos')
    depends_on('openblas', when='+openblas')

    # Ensure <cmath> is included where std::isnan is used
    patch('JEGA-discrete-design-cmath.patch', when='@6.9')

    def cmake_args(self):
        spec = self.spec

        if len(spec['blas'].lib) > 1:
            raise ValueError('Multiple libraries found for blas, aborting')
        if len(spec['lapack'].lib) > 1:
            raise ValueError('Multiple libraries found for lapack, aborting')

        args = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DDAKOTA_HAVE_HDF5:BOOL=%s' % (
                'ON' if '+hdf5' in spec else 'OFF'),
            '-DBUILD_IN_TRILINOS:BOOL=%s' % (
                'OFF' if '+trilinos' in spec else 'ON'),
            '-DBLAS_LIBS=%s' % spec['blas'].libs[0],
            '-DLAPACK_LIBS=%s' % spec['lapack'].libs[0]),
            '-DDAKOTA_HAVE_MPI:BOOL=ON',
            '-DMPI_CXX_COMPILER:STRING=%s' % spec['mpi'].mpicxx,
        ]

        return args
