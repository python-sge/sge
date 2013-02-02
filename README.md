Stellar Game Engine
===================

## About
Stellar Game Engine (also "SGE" or simply "Stellar Engine") is an engine
for use with Stellar, in order to make its development easier and also
offer an option to those who want only a game engine without a graphical
interface.

SGE is supposed to be able to have differing "implementations"
available.  The first implementation developed will likely be one that
uses Pygame, but an implementation using Pyglet might be developed
later, for instance.  This allows increased flexibility in Stellar.

## Developing an Implementation
To develop an implementation of SGE, copy sge-template.py and add in the
functionality.  In order to prevent confusion, do *not* use docstrings
on anything that is not included in the template, and do not modify the
docstrings except for adding in the name of the implementation and
implementation-specific information to the module docstring.  Use normal
comments to document custom functions specific to a given
implementation.

Note that, except where otherwise noted, all documented features are
required for an implementation to be considered complete.
