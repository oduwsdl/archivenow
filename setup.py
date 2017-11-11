#!/usr/bin/env python

from setuptools import setup, find_packages
from archivenow import __version__

long_description = open('README.rst').read()
desc = """A Python library to push web resources into public web archives"""


setup(
    name='archivenow',
    version=__version__,
    description=desc,
    long_description=long_description,
    author='Mohamed Aturban',
    author_email='maturban@cs.odu.edu',
    url='https://github.com/maturban/archivenow',
    packages=find_packages(),
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',        
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=[
        'flask',
        'requests'
    ],
    package_data={
        'archivenow': [
            'handlers/*.*',
            'templates/*.*',
            'static/*.*'
          ]
    },
    entry_points='''
        [console_scripts]
        archivenow=archivenow.archivenow:args_parser
    '''   
)
