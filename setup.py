#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages

setup(name='sge',
    version='0.0.30',
    description='Stellar Game Engine (also "SGE" or simply "Stellar Engine") is an engine for use with Stellar,'
                'in order to make its development easier and also offer an option to those who want only a game engine without a graphical interface. '
    author='Julian Marchant',
    author_email='onpon4@lavabit.com',
    url='https://github.com/Coppolaemilio/StellarGameEngine',
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read(),
    install_requires = [
        "pygame >= 1.9.0"
    ]
)
