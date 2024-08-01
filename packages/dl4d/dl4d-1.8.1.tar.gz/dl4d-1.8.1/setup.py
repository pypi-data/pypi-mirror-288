# !/usr/bin/env python

import os
import re
from setuptools import setup


def resource(*args):
    return os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)),
                        *args)


with open(resource('dl4d', '__init__.py')) as version_file:
    version_file = version_file.read()
    VERSION = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                        version_file, re.M)
    VERSION = VERSION.group(1)

with open(resource('README.md')) as readme_file:
    README = readme_file.read()

setup(
    name='dl4d',
    packages=['dl4d',
              'dl4d.models',
              'dl4d.training'],
    version=VERSION,
    description='Deep Learning for empirical DownScaling',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Carlos Alberto Gomez Gonzalez',
    license='Apache v2.0',
    author_email='carlos.gomez@bsc.es',
    url='https://github.com/carlgogo/dl4ds',
    keywords=[
        'deep learning', 
        'downscaling', 
        'super-resolution', 
        'neural networks',
        'Earth data',
        'EO' 
        ],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'xarray',
        'ecubevis',
        'tensorflow',
        'scikit-learn',
        'opencv-python',
        'joblib',
        'seaborn',
        'absl-py'
        ],
    extras_require={
        'horovod':['horovod'] 
    },
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        ],
)