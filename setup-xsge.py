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
xSGE is a collection of extensions for the SGE licensed under the GNU
General Public License.  They are designed to give additional features
to games which are released under the GNU GPL without any extra work.

xSGE extensions are not dependent on any particular SGE implementation.
They should would with any implementation that follows the
specification.
""".strip()

setup(name="xsge",
      version="0.1.0",
      description="A 2-D game engine for Python",
      long_description=long_description,
      author="Julian Marchant",
      author_email="onpon4@riseup.net",
      url="http://stellarengine.nongnu.org",
      license="GNU General Public License,
      packages=["xsge"],
      package_dir={"xsge": "xsge"},
      package_data={"xsge": ["COPYING", "gui_data"]},
      requires=["sge"],
     )
