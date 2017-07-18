# This file has been dedicated to the public domain, to the extent
# possible under applicable law, via CC0. See
# http://creativecommons.org/publicdomain/zero/1.0/ for more
# information. This file is offered as-is, without any warranty.

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
      version="1.5.1",
      description="A 2-D game engine for Python",
      long_description=long_description,
      author="Julie Marchant",
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
      package_data={"sge": ["COPYING", "COPYING.LESSER"]},
      requires=["pygame (>=1.9.1)", "six (>=1.4.0)", "uniseg"],
      provides=["sge"],
      )
