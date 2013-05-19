#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
from distutils.core import setup

long_description = """
Stellar Game Engine (SGE) is an engine for Stellar, a free program which makes development of 2D games faster and easier. SGE can also be used by itself as an easy-to-use game engine.

SGE is designed to easily allow multiple implementations. Currently, only a Pygame implementation is available.
""".strip()

if sys.version_info.major == 3:
    idir = 'sge-pygame-py3k'
    ireq = 'pygame (>= 1.9.0)'
elif sys.version_info.major == 2 and sys.version_info.minor >= 6:
    idir = 'sge-pygame'
    ireq = 'pygame (>= 1.9.0)'
else:
    sys.exit('Python version unsupported.')

setup(name='Stellar Game Engine',
      version='0.3.0',
      description='A 2D game engine for use with Stellar',
      long_description=long_description,
      author='Julian Marchant',
      author_email='onpon4@lavabit.com',
      url='http://stellarengine.nongnu.org',
      license='GNU Lesser General Public License version 3 or later',
      packages=['sge'],
      package_dir={'sge':idir},
      requires=[ireq],
     )
