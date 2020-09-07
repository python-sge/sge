# This file has been dedicated to the public domain, to the extent
# possible under applicable law, via CC0. See
# http://creativecommons.org/publicdomain/zero/1.0/ for more
# information. This file is offered as-is, without any warranty.

import sys
from distutils.core import setup

long_description = """
The Seclusion Game Engine ("SGE") is a general-purpose 2-D game engine.
It takes care of several details for you so you can focus on the game
itself.  This makes more rapid game development possible, and it also
makes the SGE easy to learn.

This implementation of the SGE uses Pygame as a backend.
""".strip()

setup(name="sge",
      version="1.7",
      description="Seclusion Game Engine (Pygame implementation)",
      long_description=long_description,
      author="Layla Marchant",
      author_email="diligentcircle@riseup.net",
      url="https://python-sge.github.io",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: DFSG approved",
                   "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="GNU Lesser General Public License",
      packages=["sge"],
      package_dir={"sge": "sge"},
      package_data={"sge": ["COPYING", "COPYING.LESSER"]},
      requires=["pygame (>=1.9.1)", "uniseg"],
      provides=["sge"],
      )
