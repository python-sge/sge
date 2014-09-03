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
The SGE Game Engine ("SGE", pronounced like "Sage") is a general-purpose
2-D game engine.  It takes care of several details for you so you can
focus on the game itself.  This makes more rapid game development
possible, and it also makes the SGE easy to learn.
""".strip()

setup(name="sge",
      version="0.12.dev0",
      description="A 2-D game engine for Python",
      long_description=long_description,
      author="Julian Marchant",
      author_email="onpon4@riseup.net",
      url="http://stellarengine.nongnu.org",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="CC0",
      packages=["sge"],
      package_dir={"sge": "sge"},
      package_data={"sge": ["COPYING"]},
      requires=[],
     )
