#!/usr/bin/env python

from setuptools import setup

long_description = open('README.rst').read()
desc = """A simple Python library that can be used push web resources into public web archives"""


setup(
    name='archivenow',
    version='0.0.2',
    description=desc,
    long_description=long_description,
    author='Mohamed Aturban',
    author_email='maturban@cs.odu.edu',
    url='https://github.com/maturban/archivenow',
    packages=['archivenow'],
    include_package_data=True,
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'flask',
        'requests',
        'bs4'
    ],
entry_points='''
        [console_scripts]
        archivenow=archivenow.archivenow:args_parser
    '''   
)