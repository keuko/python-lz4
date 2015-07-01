#!/usr/bin/env python


from setuptools import setup, find_packages, Extension
import subprocess
import os

VERSION = (0, 7, 0)
VERSION_STR = ".".join([str(x) for x in VERSION])

# Check to see if we have a lz4 library installed on the system and
# use it if so. If not, we'll use the bundled library. If lz4 is
# installed it will have a pkg-config file, so we'll use pkg-config to
# check for existence of the library.
pkg_config_exe = os.environ.get('PKG_CONFIG', None) or 'pkg-config'
cmd = '{0} --exists liblz4'.format(pkg_config_exe).split()
liblz4_found = subprocess.call(cmd) == 0

if liblz4_found:
    # Use system lz4, and don't set optimization and warning flags for
    # the compiler. Specifically we don't define LZ4_VERSION since the
    # system lz4 library could be updated (that's the point of a
    # shared library).
    lz4mod = Extension('lz4',
                       [
                           'src/python-lz4.c'
                       ],
                       extra_compile_args=[
                           "-std=c99",
                           "-DVERSION=\"%s\"" % VERSION_STR,
                       ],
                       libraries=['lz4'],
    )
else:
    # Use the bundled lz4 libs, and set the compiler flags as they
    # historically have been set. We do set LZ4_VERSION here, since it
    # won't change after compilation.
    lz4mod = Extension('lz4',
                       [
                           'src/lz4.c',
                           'src/lz4hc.c',
                           'src/python-lz4.c'
                       ],
                       extra_compile_args=[
                           "-std=c99",
                           "-O3",
                           "-Wall",
                           "-W",
                           "-Wundef",
                           "-DVERSION=\"%s\"" % VERSION_STR,
                           "-DLZ4_VERSION=\"r130\"",
                       ]
    )


setup(
    name='lz4',
    version=VERSION_STR,
    description="LZ4 Bindings for Python",
    long_description=open('README.rst', 'r').read(),
    author='Steeve Morin',
    author_email='steeve.morin@gmail.com',
    url='https://github.com/steeve/python-lz4',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    ext_modules=[lz4mod,],
    tests_require=["nose>=1.0"],
    test_suite = "nose.collector",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
)
