# setup.py
# Copyright (C) 2012-2016 onpon4 <onpon4@riseup.net>
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

This implementation of the SGE uses Pygame as a backend.
""".strip()

setup(name="sge-pygame",
      version="1.3",
      description="A 2-D game engine for Python",
      long_description=long_description,
      author="onpon4",
      author_email="onpon4@riseup.net",
      url="http://stellarengine.nongnu.org",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: DFSG approved",
                   "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 3",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="GNU Lesser General Public License",
      packages=["sge"],
      package_dir={"sge": "sge"},
      package_data={"sge": ["*.png", "COPYING", "COPYING.LESSER", "LICENSES"]},
      requires=["pygame (>=1.9.1)", "six (>=1.4.0)"],
      provides=["sge"],
      )
