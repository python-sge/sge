# Copyright (C) 2012, 2013 Julian Marchant <onpon4@riseup.net>
# 
# This file is part of the Pygame SGE.
# 
# The Pygame SGE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# The Pygame SGE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with the Pygame SGE.  If not, see <http://www.gnu.org/licenses/>.

"""
The Stellar Game Engine (abbreviated "SGE", pronounced as "Sage") is a
free 2-D game engine.  The purpose of the SGE is to make game
development easier, which allows more rapid development by experienced
game developers and also helps less experienced game developers learn
how to develop games.

Official implementations of the SGE are free software (where "free"
refers to freedom, not price; see the `Free Software Definition
<http://gnu.org/philosophy/free-sw.html>`_ for more information), and
the documentation has been (to the extent legally possible) released to
the public domain via the CC0 license.

Even if it isn't required of you, we encourage you to release your
games' code under a free software license, such as the GNU General
Public License, the Expat License (often ambiguously called the "MIT
License"), or the Apache License 2.0.  Doing so is easy, does not
negatively affect you, and is highly appreciated as a contribution to
free software.

SGE Concepts
============

Naming Conventions
------------------

There are many cases where you will want to derive a class from a SGE
class.  Since there can be multiple implementations of the SGE, it can
be easy when doing so to overwrite a special variable used by some
implementations internally, which can be disastrous.  To avoid such
occasions, implementations are expected to never introduce any attribute
names which are not explicitly mentioned in the documentation for a
class unless the new attribute names are preceded by an underscore, as
in the hypothetical attribute name ``_foo``.  This naming convention
will protect users of the SGE from unexpected errors provided that they
do not use such names themselves.

A suggested convention for users of the SGE to use for "private"
attributes in place of the usual leading underscore  is to precede these
attributes with ``v_`` or ``p_``.

Events
------

The SGE uses an event-based system, with events defined by special class
methods with names starting with ``event_``.

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

The mouse is handled somewhat unusually by the SGE.  Rather than having
functions or variables report the mouse position relative to the screen,
the mouse position within the room, calculated based on its position on
the screen by the SGE, is recorded in a special :class:`StellarClass`
object which represents the mouse.  This mouse object can be found as
:attr:`sge.game.mouse`, and it has the special object ID, ``"mouse"``.

The mouse object differs from most :class:`StellarClass` objects in a
few ways.  Its speed variables cannot be manually set, and they always
report numbers which correspond to the average motion of the mouse
during the last quarter of a second.  Setting
:attr:`sge.game.mouse.visible` toggles whether or not the mouse cursor
itself is visible, and setting :attr:`sge.game.mouse.sprite` sets the
mouse cursor to the sprite assigned.

In all other ways, the mouse object is exactly the same as all other
:class:`StellarClass` objects.

Colors
------

Colors can be defined for the SGE in a few different ways.

HTML Color Names
~~~~~~~~~~~~~~~~

The sixteen basic HTML colors, provided as strings, are accepted by the
SGE.  These are case-insensitive, so ``"red"`` is interpreted the same
as ``"Red"`` or ``"rEd"``.  The colors are:

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

A tuple containing three or four values is accepted as a color by the
SGE.  Each index represents a component of a color: first red, then
green, then blue, with the values being integers from ``0`` to ``255``.
For example, ``(255, 128, 0)`` indicates a color with full red
intensity, 50% green intensity, and no blue intensity, which is a shade
of orange.  Note that the components are colors of light, not colors of
pigment.

The fourth value of the tuple, if specified, indicates the alpha
transparency of the color, with the possible values again being integers
from ``0`` to ``255``.  ``255`` is fully opaque, ``0`` is fully
transparent, and any value in between indicates the amount of opacity;
for example, 128 is 50% transparent.  If the fourth value is
unspecified, it is assumed that the color is fully opaque.

RGBA tuples are the only way to specify alpha transparency of colors in
SGE.  All other methods for indicating color assume full opacity.

HTML Hex Strings and Integers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTML hex strings and integers are accepted as colors by the SGE.  HTML
hex strings are in the format ``"#RRGGBB"``, where ``RR``, ``GG``, and
``BB`` are replaced with the red, green, and blue components of the
color, respectively, in hexadecimal form.  ``FF`` (equivalent to 255 in
decimal form) is full intensity of the respective color, and ``00``
(equivalent to 0 in decimal form) is no intensity of the respective
color.  For example, ``"#FF8000"`` is the same as ``(255, 128, 0)``, or
orange.

Integers, treated as hexadecimals, are also accepted.  These are in the
same form as HTML hex strings, but integral.  For example, ``0xFF8000``
is the same as ``"#FF8000"``.

Position
--------

In all cases of positioning for the SGE, it is based on a
two-dimensional graph with each unit being a pixel.  This graph is not
quite like regular graphs; the horizontal direction, normally called
``x``, is the same as the x-axis on a regular graph; ``0`` is the
origin, positive numbers are to the right of the origin, and negative
numbers are to the left of the origin.  However, in the vertical
direction, normally called ``y``, ``0`` is the origin, positive numbers
are below the origin, and negative numbers are above the origin.  While
slightly jarring if you are used to normal graphs, this is in fact
common in 2-D game development and is so how pixels in most image
formats are indexed.

Except where otherwise specified, the origin is always located at the
top-leftmost position of an object.

In addition to integers, position variables are allowed by the SGE to be
floating-point numbers.

Z-Axis
------

The SGE uses a Z-axis to determine where objects are placed in the third
dimension.  Objects with a higher Z value are considered to be closer to
the viewer and thus will be placed over objects which have a lower Z
value.  Note that the Z-axis does not allow 3-D gameplay or effects; it
is only used to tell the SGE what to do with objects that overlap.  For
example, if an object called ``spam`` has a Z value of ``5`` while an
object called ``eggs`` has a Z value of ``2``, ``spam`` will obscure
part or all of ``eggs`` when the two objects overlap.

If two objects with the same Z-axis value overlap, the SGE arbitrarily
chooses which one is considered to be closer to the viewer.  The SGE is
allowed to change this decision, but only while the objects in question
are not overlapping, since changing the decision while the two objects
are overlapping would cause an undesirable flicker effect.

Global Variables and Constants
==============================

.. data:: sge.IMPLEMENTATION

   A string indicating the name of the SGE implementation.

.. data:: sge.ALIGN_LEFT

   Flag indicating horizontal alignment to the left.

.. data:: sge.ALIGN_CENTER

   Flag indicating horizontal alignment to the center.

.. data:: sge.ALIGN_RIGHT

   Flag indicating horizontal alignment to the right.

.. data:: sge.ALIGN_TOP

   Flag indicating vertical alignment to the top

.. data:: sge.ALIGN_MIDDLE

   Flag indicating vertical alignment to the middle.

.. data:: sge.ALIGN_BOTTOM

   Flag indicating vertical alignment to the bottom.

.. data:: sge.BLEND_NORMAL

   Flag indicating normal blending.

.. data:: sge.BLEND_RGBA_ADD

   Flag indicating RGBA Addition blending: the red, green, blue, and
   alpha color values of the source are added to the respective color
   values of the destination, to a maximum of 255.

.. data:: sge.BLEND_RGBA_SUBTRACT

   Flag indicating RGBA Subtract blending: the red, green, blue, and
   alpha color values of the source are subtracted from the respective
   color values of the destination, to a minimum of 0.

.. data:: sge.BLEND_RGBA_MULTIPLY

   Flag indicating RGBA Multiply blending: the red, green, blue,
   and alpha color values of the source and destination are converted to
   values between 0 and 1 (divided by 255), the resulting destination
   color values are multiplied by the respective resulting source color
   values, and these results are converted back into values between 0
   and 255 (multiplied by 255).

.. data:: sge.BLEND_RGBA_SCREEN

   Flag indicating RGBA Screen blending: the red, green, blue, and alpha
   color values of the source and destination are inverted (subtracted
   from 255) and converted to values between 0 and 1 (divided by 255),
   the resulting destination color values are multiplied by the
   respective resulting source color values, and these results are
   converted back into values between 0 and 255 (multiplied by 255) and
   inverted again (subtracted from 255).

.. data:: sge.BLEND_RGBA_MINIMUM

   Flag indicating RGBA Minimum (Darken Only) blending: the smallest
   respective red, green, blue, and alpha color values out of the source
   and destination are used.

.. data:: sge.BLEND_RGBA_MAXIMUM

   Flag indicating RGBA Maximum (Lighten Only) blending: the largest
   respective red, green, blue, and alpha color values out of the source
   and destination are used.

.. data:: sge.BLEND_RGB_ADD

   Flag indicating RGB Addition blending: the same thing as RGBA
   Addition blending (see :data:`sge.BLEND_RGBA_ADD`) except the
   destination's alpha values are not changed.

.. data:: sge.BLEND_RGB_SUBTRACT

   Flag indicating RGB Subtract blending: the same thing as RGBA
   Subtract blending (see :data:`sge.BLEND_RGBA_SUBTRACT`) except the
   destination's alpha values are not changed.

.. data:: sge.BLEND_RGB_MULTIPLY

   Flag indicating RGB Multiply blending: the same thing as RGBA
   Multiply blending (see :data:`sge.BLEND_RGBA_MULTIPLY`) except the
   destination's alpha values are not changed.

.. data:: sge.BLEND_RGB_SCREEN

   Flag indicating RGB Screen blending: the same thing as RGBA Screen
   blending (see :data:`sge.BLEND_RGBA_SCREEN`) except the destination's
   alpha values are not changed.

.. data:: sge.BLEND_RGB_MINIMUM

   Flag indicating RGB Minimum (Darken Only) blending: the same thing
   as RGBA Minimum blending (see :data:`sge.BLEND_RGBA_MINIMUM`) except
   the destination's alpha values are not changed.

.. data:: sge.BLEND_RGB_MAXIMUM

   Flag indicating RGB Maximum (Lighten Only) blending: the same thing
   as RGBA Maximum blending (see :data:`sge.BLEND_RGBA_MAXIMUM`) except
   the destination's alpha values are not changed.

.. data:: sge.game

   Stores the current :class:`sge.Game` object.  If there is no
   :class:`sge.Game` object currently, this variable is set to
   :const:`None`.

.. data:: sge.image_directories

   A list of directories where images can be found.  Default is
   ``./data/images``, ``./data/sprites``, or ``./data/backgrounds``,
   where ``.`` is the program directory.

.. data:: sge.font_directories

   A list of directories where font files can be found.  Default is
   ``./data/fonts``, where ``.`` is the program directory.

.. data:: sge.sound_directories

   A list of directories where sounds can be found.  Default is
   ``./data/sounds``, where ``.`` is the program directory.

.. data:: sge.music_directories

   A list of directories where music files can be found.  Default is
   ``./data/music``, where ``.`` is the program directory.

Information specific to the Pygame SGE
======================================

License
-------

The Pygame SGE is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The Pygame SGE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with the Pygame SGE.  If not, see <http://www.gnu.org/licenses/>.

Dependencies
------------

- Python 2.6 or later, but not Python 3 <http://www.python.org>
- Pygame 1.9 or later <http://pygame.org>

Formats Support
---------------

:class:`Sprite` supports the following image formats:

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

:class:`Sound` supports the following audio formats:

- Uncompressed WAV
- Ogg Vorbis

:class:`Music` supports the following audio formats:

- Ogg Vorbis
- MP3 (support limited; use not recommended)
- MOD
- XM
- MIDI

For starting position in MOD files, the pattern order number is used
instead of the number of milliseconds.

If Pygame is built without full image support, :class:`sge.Sprite` will
only support uncompressed BMP images.  In addition, the pygame.mixer
module, which is used for audio playback, is optional and depends on
SDL_mixer; if pygame.mixer is unavailable, sounds and music will not
play.  If you encounter problems with loading images or playing sounds,
check your build of Pygame.

On some systems, the game will crash if :class:`sge.Music` attempts to
load an unsupported format.  Since MP3's support is limited, it is best
to avoid using it; consider using Ogg instead.

Missing Features
----------------

:meth:`sge.Sprite.draw_line` and :meth:`sge.Room.project_line` support
anti-aliasing for lines with a thickness of 1 only.
:meth:`sge.Sprite.draw_text` and :meth:`sge.Room.project_text` support
anti-aliasing in all cases.  No other drawing or projecting methods
support anti-aliasing.

:data:`sge.BLEND_RGBA_SCREEN` and :data:`sge.BLEND_RGB_SCREEN` are
unsupported. If one of these blend modes is attempted, normal blending
will be used instead.

Speed Improvements
------------------

The Pygame SGE supports hardware rendering, which can improve
performance in some cases.  It is not enabled by default.  To enable it,
set :data:`sge.hardware_rendering` to :const:`True`.  The benefit of
hardware acceleration is usually negligible, which is why it is disabled
by default.

Projection methods are highly inefficient, so they should be avoided if
speed is important; use the :class:`sge.Sprite` draw methods instead.

Other Notes
-----------

Changing the :attr:`sge.Sprite.width` and :attr:`sge.Sprite.height`
attributes of :class:`sge.Sprite` objects is a destructive
transformation in the Pygame SGE, so each time one of these variables
changes, pixel information can be lost.  For example, scaling a 128x128
pixel image down to 16x16 and then back up to 128x128 will not yield the
same image, but rather either a pixelated version or a blurry version,
depending on the value of :attr:`sge.game.scale_smooth`.  This is
because of the way the drawing methods of :class:`sge.Sprite` are
implemented.  Because of this, you should avoid changing this value as
much as possible.  For best results, set it only when the sprite is
created and then leave it alone; do any other routine transformations
with the :attr:`sge.StellarClass.image_xscale` and
:attr:`sge.StellarClass.image_yscale` attributes.

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.6.0.16"

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
