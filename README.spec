Copyright (C) 2013, 2014 Julian Marchant <onpon4@riseup.net>

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.

========================================================================

This is the specification for the SGE, written as a template.  For a
reference implementation, see the Pygame SGE.

To develop an implementation of SGE:

* Edit setup.py to include the name of the implementation and proper
  information about it.
* Replace this README with README.dist

Then, go to the "sge" directory and:

* Define the values of the constants in constants.py.
* Replace the license text on top of all source code files with
  appropriate license text for the license you intend to use for your
  implementation.  Suggested license choices are the GNU GPL, the GNU
  LGPL, the Apache License 2.0, or the Expat License.
* Replace the "TODO" comments found throughout the Python files with
  actual functionality.
* Insert the name of your implementation into the
  implementation-specific information section of __init__.py and insert
  all important information that is specific to your implementation in
  this section.
* Other than the implementation-specific information section, please do
  NOT modify the docstrings.
* Replace README with a file containing all important
  implementation-specific information.  You can just copy the
  appropriate section from the docstring of __init__.py.

Finally, go to the "doc" directory and:

* Replace "template" in the name of "template.rst" with a string
  identifying your implementation.  Modify its contents appropriately.
* Replace "template" in the toctree directive of index.rst with the
  string you used in the previous step.
* Add your name to the copyright notice in "index.rst", or modify the
  copyright notice to specify a different license.
* Use the resulting files in this directory to generate Sphinx
  documentation (e.g. with sphinx-quickstart).

To test the implementation, use the examples found in the examples
directory.

Please see also VERSION_NUMBERING, which explains how the SGE's version
numbering works.
