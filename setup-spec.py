#!/usr/bin/env python3

# setup.py
# Copyright (C) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
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

import sys
from distutils.core import setup

long_description = """
The Stellar Game Engine (abbreviated "SGE", pronounced as "Sage") is a
free 2-D game engine. The purpose of the SGE is to make game development
easier, which allows more rapid development by experienced game
developers and also helps less experienced game developers learn how to
develop games.
""".strip()

name = "sge"
author = "Julian Marchant"
author_email = "onpon4@riseup.net"
url = "http://stellarengine.nongnu.org"
license = "CC0"
idir = "sge"
requires = []

setup(name=name,
      version='0.9.2',
      description='A 2-D game engine for Python',
      long_description=long_description,
      author=author,
      author_email=author_email,
      url=url,
      license=license,
      packages=['sge'],
      package_dir={'sge': idir},
      package_data={'sge': ["COPYING"]},
      requires=requires,
     )
