from setuptools import setup
from setuptools.command.install import install
from distutils.command.build import build

VERSION = (1, 0, 5)
VERSION_STR = '.'.join([str(x) for x in VERSION])


def get_ext_modules():
    import lz4
    return [lz4.ffi.verifier.get_extension()]


class CFFIBuild(build):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)


class CFFIInstall(install):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)


setup(
    name='lz4-cffi',
    version=VERSION_STR,
    description='A port of the lz4tools package from to CFFI.',
    long_description=open('README', 'r').read(),
    author='Greg Bowyer',
    author_email='gbowyer@fastmail.co.uk',
    url='http://github.com/GregBowyer/lz4-cffi/',
    packages=['lz4'],
    tests_require=['nose>=1.0'],
    test_suite='nose.collector',
    install_requires=['cffi>=0.8'],
    cmdclass={
        'build': CFFIBuild,
        'install': CFFIInstall,
    },
    setup_requires=['cffi>=0.8'],
    include_package_data=False,
    zip_safe=False,
    package_data={'lz4': ['*.py', '*.c', '*.h']},
    keywords=['lz4', 'pypy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
