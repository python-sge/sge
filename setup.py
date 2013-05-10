#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
from distutils.core import setup

if sys.version_info.major == 3:
    idir = 'sge-pygame-py3k'
    ireq = 'pygame >= 1.9.0'
elif sys.version_info.major == 2 and sys.version_info.minor >= 6:
    idir = 'sge-pygame'
    ireq = 'pygame >= 1.9.0'
else:
    sys.exit('Python version unsupported.')

setup(name='Stellar Game Engine',
      version='0.2.1',
      description='A 2D game engine for use with Stellar',
      author='Julian Marchant'
      author_email='onpon4@lavabit.com',
      url='https://github.com/Coppolaemilio/StellarGameEngine',
      packages=['sge'],
      package_dir={'sge':'sge-pygame'},
      requires=['pygame >= 1.9.0'],
     )
