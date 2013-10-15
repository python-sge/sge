#!/usr/bin/env python
# -*- coding: utf8 -*-

# SGE setup.py
# Copyright (C) 2012, 2013 Julian Marchant <onpon4@riseup.net>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import sys
from distutils.core import setup

long_description = """
Stellar Game Engine (SGE) is a free, easy-to-use 2-D game engine for Python.

SGE is designed to easily allow multiple implementations. Currently, only a Pygame implementation is available.
""".strip()
py3_input = input if sys.version_info.major >= 3 else raw_input

# Defaults
name = "SGE"
author = "Julian Marchant"
author_email = "onpon4@riseup.net"
url = "http://stellarengine.nongnu.org"
license = "CC0"
idir = "sge"
requires = []

def choose_lib(libs_available):
    """Return the library (as a string) to use.

    Arguments:

    - ``libs_available`` -- A list or tuple of the possible libraries to
      choose from.

    """
    if not libs_available:
        return None
    elif len(libs_available) == 1:
        return 0
    else:
        print("Please choose one of the following libraries to use for SGE:")
        
        i = 0
        for lib in libs_available:
            print("{0} ({1})".format(lib, i))
            i += 1

        choice = py3_input("Enter the number of your choice [0] ").strip()
        
        if not choice:
            choice = "0"
        
        while not (choice.isdigit() and 0 <= choice < len(libs_available)):
            print("Invalid entry; must be an integer from 0 to {0}.".format(
                len(libs_available)))
            choice = py3_input("Enter the number of your choice [0] ").strip()

            if not choice:
                choice = "0"

        return choice

if sys.version_info.major == 3:
    libs_available = []
    try:
        import pygame
        if pygame.version.vernum >= (1, 9):
            libs_available.append('pygame')
    except ImportError:
        pass

    choice = choose_lib(libs_available)

    if choice == 'pygame':
        name = 'SGE Pygame'
        license = "GNU Lesser General Public License version 3 or later"
        idir = 'sge-pygame-py3k'
        requires = ['pygame (>= 1.9.0)']
elif sys.version_info.major == 2 and sys.version_info.minor >= 6:
    libs_available = []
    try:
        import pygame
        if pygame.version.vernum >= (1, 9):
            libs_available.append('pygame')
    except ImportError:
        pass

    choice = choose_lib(libs_available)

    if choice == 'pygame':
        name = 'SGE Pygame'
        license = "GNU Lesser General Public License version 3 or later"
        idir = 'sge-pygame'
        requires = ['pygame (>= 1.9.0)']
else:
    sys.exit('Python version unsupported.')

setup(name=name,
      version='0.4.0-dev',
      description='A 2-D game engine for Python',
      long_description=long_description,
      author=author,
      author_email=author_email,
      url=url,
      license=license,
      packages=['sge'],
      package_dir={'sge':idir},
      requires=requires,
     )
