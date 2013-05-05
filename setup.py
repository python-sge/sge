#!/usr/bin/env python
# -*- coding: utf8 -*-

from distutils.core import setup

setup(name='Stellar Game Engine',
      version='0.2.0',
      description='A 2D game engine for use with Stellar',
      author='Julian Marchant'
      author_email='onpon4@lavabit.com',
      url='https://github.com/Coppolaemilio/StellarGameEngine',
      packages=['sge'],
      package_dir={'sge':'sge-pygame'},
      requires=['pygame >= 1.9.0'],
     )
