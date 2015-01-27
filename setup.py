from setuptools import setup
import lz4

VERSION = (1, 0, 4)
VERSION_STR = '.'.join([str(x) for x in VERSION])

setup(
    name='lz4-cffi',
    version=VERSION_STR,
    description='A port of the lz4tools package from to CFFI.',
    long_description=open('README', 'r').read(),
    author='Greg Bowyer',
    author_email='gbowyer@fastmail.co.uk',
    url='http://github.com/GregBowyer/lz4-cffi/',
    packages=['lz4'],
    ext_modules=[
        lz4.ffi.verifier.get_extension(),
    ],
    tests_require=['nose>=1.0'],
    test_suite='nose.collector',
    install_requires=['cffi>=0.8'],
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
