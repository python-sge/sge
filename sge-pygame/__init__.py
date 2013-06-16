# Copyright (C) 2012, 2013 Julian Marchant <onpon4@lavabit.com>
# 
# This file is part of SGE Pygame.
# 
# SGE Pygame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# SGE Pygame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with SGE Pygame.  If not, see <http://www.gnu.org/licenses/>.

"""SGE Pygame

The Stellar Game Engine (abbreviated "SGE", pronounced as "Sage") is a
Python library for use by Stellar.  It is a game engine loosely based on
the proprietary program, Game Maker.  The purpose of SGE is to make game
development easier, which allows more rapid development by experienced
game developers and also helps less experienced game developers learn
how to develop games.

Unlike Game Maker, you have freedom with SGE.  SGE is free software
(where "free" refers to freedom, not price; see the `Free Software
Definition <http://gnu.org/philosophy/free-sw.html>`_ for more
information).  It is released under the GNU Lesser General Public
License, which means you can modify and redistribute it without
restrictions, and you can use it however you wish.

Although the GNU Lesser General Public License does not require it, we
encourage you to release your games' code under a free software license,
such as the GNU General Public License, the Expat License (often
ambiguously called the "MIT License"), or the Apache 2.0 License.  Doing
so is easy, does not negatively affect you, and is highly appreciated as
a contribution to free software.

SGE Concepts
============

Naming Conventions
------------------

There are many cases where you will want to derive a class from a SGE
class.  Since there can be multiple implementations of SGE, it can be
easy when doing so to overwrite a special variable used by some
implementations internally, which can be disastrous.  To avoid such
occasions, implementations are expected to never introduce any attribute
names which are not explicitly mentioned in the documentation for a
class unless the new attribute names are preceded by an underscore, as
in the hypothetical attribute name ``_foo``.  This naming convention
will protect users of SGE from unexpected errors provided that they do
not use such names themselves.

A suggested convention for users of SGE to use for "private" attributes
in place of the usual leading underscore  is to precede these attributes
with ``v_`` or ``p_``.

Events
------

Much like Game Maker, SGE uses an event-based system, with events
defined by special class methods with names starting with ``event_``.

Except in certain special cases, the order that events are handled in is
arbitrary; if Event A and Event B happen at the same time, one
implementation might handle Event A first, another might handle Event B
first, and another might handle either Event A or Event B first
depending on the circumstances.  This is particularly important to keep
in mind because, for example, there is no guarantee that the Step Event
will be executed before or after collision detection is applied in a
given frame, so code should not be written with that expectation.

The Mouse
---------

The mouse is handled somewhat unusually in SGE.  Rather than having
functions or variables report the mouse position relative to the screen,
the mouse position within the room, calculated based on its position on
the screen by SGE, is recorded in a special `StellarClass` object which
represents the mouse.  This mouse object can be found as
``sge.game.mouse``, and it has the special object ID, ``"mouse"``.

The mouse object differs from most `StellarClass` objects in a few ways.
Its speed variables cannot be manually set, and they always report
numbers which correspond to the average motion of the mouse during the
last quarter of a second.  Setting ``sge.game.mouse.visible`` toggles
whether or not the mouse cursor itself is visible, and setting
``sge.game.mouse.sprite`` sets the mouse cursor to the sprite assigned.

In all other ways, the mouse object is exactly the same as all other
`StellarClass` objects.

Colors
------

Colors can be defined in SGE in a few different ways.

HTML Color Names
~~~~~~~~~~~~~~~~

The sixteen basic HTML colors, provided as strings, are accepted by SGE.
These are case-insensitive, so ``"red"`` is interpreted the same as
``"Red"`` or ``"rEd"``.  If SGE returns a color and chooses this form,
it will use all lowercase letters.  The colors are:

- ``"white"``
- ``"silver"``
- ``"gray``
- ``"black"``
- ``"red"``
- ``"maroon"``
- ``"yellow"``
- ``"olive"``
- ``"lime"``
- ``"green"``
- ``"aqua"``
- ``"teal"``
- ``"blue"``
- ``"navy"``
- ``"fuchsia"``
- ``"purple"``

RGB(A) Tuples
~~~~~~~~~~~~~

A tuple containing three or four values is accepted as a color by SGE.
Each index represents a component of a color: first red, then green,
then blue, with the values being integers from 0 to 255.  For example,
``(255, 128, 0)`` indicates a color with full red intensity, 50% green
intensity, and no blue intensity, which is a shade of orange.  Note that
the components are colors of light, not colors of pigment.

The fourth value of the tuple, if specified, indicates the alpha
transparency of the color, with the possible values again being integers
from 0 to 255.  255 is fully opaque, 0 is fully transparent, and any
value in between indicates the amount of opacity; for example, 128 is
50% transparent.  If the fourth value is unspecified, it is assumed that
the color is fully opaque.

RGBA tuples are the only way to specify alpha transparency of colors in
SGE.  All other methods for indicating color assume full opacity.

HTML Hex Strings and Integers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTML hex strings and integers are accepted as colors by SGE.  HTML hex
strings are in the format ``"#RRGGBB"``, where "RR", "GG", and "BB" are
replaced with the red, green, and blue components of the color,
respectively, in hexadecimal form.  "FF" (equivalent to 255 in decimal
form) is full intensity of the respective color, and "00" (equivalent to
0 in decimal form) is no intensity of the respective color.  For
example, ``"#FF8000"`` is the same as ``(255, 128, 0)``, or orange.

Integers, treated as hexadecimals, are also accepted.  These are in the
same form as HTML hex strings, but integral.  For example, ``0xFF8000``
is the same as ``"#FF8000"``.

Position
--------

In all cases of positioning in SGE, it is based on a two-dimensional
graph with each unit being a pixel.  This graph is not quite like
regular graphs; the horizontal direction, normally called ``x``, is the
same as the x-axis on a regular graph; 0 is the origin, positive numbers
are to the right of the origin, and negative numbers are to the left of
the origin.  However, in the vertical direction, normally called ``y``,
0 is the origin, positive numbers are below the origin, and negative
numbers are above the origin.  While slightly jarring if you are used to
normal graphs, this is in fact common in 2-D game development and is
also how pixels in most image formats are indexed.

Except where otherwise specified, the origin is always located at the
top-leftmost position of an object.

In addition to integers, position variables are allowed to be floating-
point numbers in SGE.

Z-Axis
------

SGE uses a Z-axis to determine where objects are placed in the third
dimension.  Objects with a higher Z value are considered to be closer to
the viewer and thus will be placed over objects which have a lower Z
value.  Note that the Z-axis does not allow 3-D gameplay or effects; it
is only used to tell SGE what to do with objects that overlap.  For
example, if an object called ``spam`` has a Z value of 5 while an object
called ``eggs`` has a Z value of 2, ``spam`` will obscure part or all of
``eggs`` when the two objects overlap.

If two objects with the same Z-axis value overlap, SGE arbitrarily
chooses which one is considered to be closer to the viewer.  SGE is
allowed to change this decision, but only while the objects in question
are not overlapping, since changing the decision while the two objects
are overlapping would cause an undesirable flicker effect.

Global Variables and Constants
==============================

Constants:
- ``sge.IMPLEMENTATION`` -- A string idicating the name of the SGE
  implementation.
- ``sge.ALIGN_LEFT`` -- Flag indicating alignment to the left.
- ``sge.ALIGN_CENTER`` -- Flag indicating alignment to the horizontal
  center.
- ``sge.ALIGN_RIGHT`` -- Flag indicating alignment to the right.
- ``sge.ALIGN_TOP`` -- Flag indicating alignment to the top.
- ``sge.ALIGN_MIDDLE`` -- Flag indicating alignment to the vertical
  middle.
- ``sge.ALIGN_BOTTOM`` -- Flag indicating alignment to the bottom.

Global variables:
- ``sge.game`` -- Stores the current `Game` object.  If there is no
  `Game` object currently, this variable is set to None.
- ``sge.image_directories`` -- A list of directories where images can be
  found.  Default is ./data/images, ./data/sprites, or
  ./data/backgrounds, where "." is the program directory.
- ``sge.font_directories`` -- A list of directories where font files can
  be found.  Default is ./data/fonts, where "." is the program
  directory.
- ``sge.sound_directories`` -- A list of directories where sounds can be
  found.  Default is ./data/sounds, where "." is the program directory.
- ``sge.music_directories`` -- A list of directories where music files
  can be found.  Default is ./data/music, where "." is the program
  directory.

Implementation-Specific Information
===================================

License
-------

SGE Pygame is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SGE Pygame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with SGE Pygame.  If not, see <http://www.gnu.org/licenses/>.

Dependencies
------------

- Python 2.6 or later, but not Python 3 <http://www.python.org>
- Pygame 1.9 or later <http://pygame.org>

Formats Support
---------------

`Sprite` supports the following image formats:
- PNG
- JPEG
- Non-animated GIF
- BMP
- PCX
- Uncompressed Truevision TGA
- TIFF
- ILBM
- Netpbm
- X Pixmap

`Sound` supports the following audio formats:
- Uncompressed WAV
- Ogg Vorbis

`Music` supports the following audio formats:
- Ogg Vorbis
- MP3 (support limited; use not recommended)
- MOD
- XM
- MIDI

For starting position in MOD files, the pattern order number is used
instead of the number of milliseconds.

If Pygame is built without full image support, `Sprite` will only
support uncompressed BMP images.  In addition, the pygame.mixer module,
which is used for audio playback, is optional and depends on SDL_mixer;
if pygame.mixer is unavailable, sounds and music will not play.  If you
encounter problems with loading images or playing sounds, check your
build of Pygame.

On some systems, the game will crash if `Music` attempts to load an
unsupported format.  Since MP3's support is limited, it is best to avoid
using it; consider using Ogg instead.

Missing Optional Features
-------------------------

`Sprite.draw_line` and `Room.project_line` support anti-aliasing for
lines with a thickness of 1 only.  `Sprite.draw_text` and
`Room.project_text` support anti-aliasing in all cases.  No other
drawing or projecting methods support anti-aliasing.

Speed Improvements
------------------

This implementation supports hardware rendering, which can improve
performance in some cases.  It is not enabled by default.  To enable it,
set ``sge.hardware_rendering`` to True.  The benefit of hardware
acceleration is usually negligible, which is why it is disabled by
default.

Projection is highly inefficient, so it should be avoided if speed is
important; use the sprite draw methods instead.

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.3.0.26"

import os

import pygame

from .constants import *
from .Game import Game
from .Sprite import Sprite
from .BackgroundLayer import BackgroundLayer
from .Background import Background
from .Font import Font
from .Sound import Sound
from .Music import Music
from .StellarClass import StellarClass, Mouse
from .Room import Room
from .View import View
from .functions import *


__all__ = [
    # Constants
    'IMPLEMENTATION', 'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT', 'ALIGN_TOP',
    'ALIGN_MIDDLE', 'ALIGN_BOTTOM',

    # Classes
    'Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font', 'Sound',
    'Music', 'StellarClass', 'Room', 'View',

    # Functions
    'create_object', 'sound_stop_all', 'music_clear_queue', 'music_stop_all',
    'get_key_pressed', 'get_mouse_button_pressed', 'get_joystick_axis',
    'get_joystick_hat', 'get_joystick_button_pressed', 'get_joysticks',
    'get_joystick_axes', 'get_joystick_hats', 'get_joystick_buttons'
    ]

# Global variables
game = None
image_directories = [os.path.join(PROGRAM_DIR, 'data', 'images'),
                     os.path.join(PROGRAM_DIR, 'data', 'sprites'),
                     os.path.join(PROGRAM_DIR, 'data', 'backgrounds')]
font_directories = [os.path.join(PROGRAM_DIR, 'data', 'fonts')]
sound_directories = [os.path.join(PROGRAM_DIR, 'data', 'sounds')]
music_directories = [os.path.join(PROGRAM_DIR, 'data', 'music')]

hardware_rendering = False

if DEBUG:
    print("Image directories set to:")
    print(*image_directories, sep="; ")
    print("Font directories set to:")
    print(*font_directories, sep="; ")
    print("Sound directories set to:")
    print(*sound_directories, sep="; ")
    print("Music directories set to:")
    print(*music_directories, sep="; ")

    if hardware_rendering:
        print("Hardware rendering enabled.")
    else:
        print("Hardware rendering disabled.")

# Uncomment this line to tell SDL to center the window.  Disabled by
# default because it seems to cause some weird behavior with window
# resizing on at least some systems.
#os.environ['SDL_VIDEO_CENTERED'] = '1'
