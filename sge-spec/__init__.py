# The SGE Specification
# Written in 2012, 2013, 2014 by Julian Marchant <onpon4@riseup.net> 
# 
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty. 
# 
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

# INSTRUCTIONS FOR DEVELOPING AN IMPLEMENTATION: Replace the notice
# above as well as the notices contained in other source files with your
# own copyright notice.  Recommended free  licenses are the GNU General
# Public License, GNU Lesser General Public License, Expat License, or
# Apache License 2.0.

"""
The Stellar Game Engine (abbreviated "SGE", pronounced as "Sage") is a
free 2-D game engine.  The purpose of the SGE is to make game
development easier, which allows more rapid development by experienced
game developers and also helps less experienced game developers learn
how to develop games.

Official implementations of the SGE are `free/libre software
<http://gnu.org/philosophy/free-sw.html>`_, and the SGE documentation is
free/libre as well.

Even if it isn't required of you, we encourage you to release your
games' code under a free/libre software license, such as the GNU General
Public License, the Expat License, or the Apache License.  Doing so is
easy, does not negatively affect you, and is highly appreciated as a
contribution to free/libre software.

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

The SGE uses an event-based system.  When an event occurs, a certain
event method (with a name that begins with ``event_``) is called. To
define actions triggered by events, simply override the appropriate
event method.

The Mouse
---------

The mouse is handled somewhat unusually by the SGE.  Rather than having
functions or variables report the mouse position relative to the screen,
the mouse position within the room, calculated based on its position on
the screen by the SGE, is recorded in a special
:class:`sge.StellarClass` object which represents the mouse.  This mouse
object can be found as :attr:`sge.game.mouse`, and it has the special
object ID, ``"mouse"``.

The mouse object differs from most :class:`sge.StellarClass` objects in
a few ways.  Its speed variables cannot be manually set, and they always
report numbers which correspond to the average motion of the mouse
during the last quarter of a second.  Setting
:attr:`sge.game.mouse.visible` toggles whether or not the mouse cursor
itself is visible, and setting :attr:`sge.game.mouse.sprite` sets the
mouse cursor to the sprite assigned.

In all other ways, the mouse object is exactly the same as all other
:class:`sge.StellarClass` objects.

Colors
------

The SGE accepts a few different formats for defining colors.

The sixteen basic HTML colors, provided as strings, are accepted.  These
are case-insensitive, so ``"red"`` is interpreted the same as ``"Red"``
or ``"rEd"``.  The colors are:

- ``"white"``
- ``"silver"``
- ``"gray"``
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

Tuples containing three or four integers are accepted.  Each index
represents a component of a color: first red, then green, then blue,
with the values being integers from ``0`` to ``255``.  For example,
``(255, 128, 0)`` indicates a color with full red intensity, 50% green
intensity, and no blue intensity, which is a shade of orange.  Note that
the components are colors of light, not colors of pigment.

The fourth value of the tuple, if specified, indicates the alpha
transparency of the color, with the possible values again being integers
from ``0`` to ``255``.  ``255`` is fully opaque, ``0`` is fully
transparent, and any value in between indicates the amount of opacity;
for example, 128 is 50% transparent.  If the fourth value is
unspecified, it is assumed that the color is fully opaque.

RGBA tuples are the only way to specify alpha transparency of colors in
SGE.  All other methods for indicating color assume full opacity.

HTML hex strings and integers are accepted.  HTML hex strings are in the
format ``"#RRGGBB"``, where ``RR``, ``GG``, and ``BB`` are replaced with
the red, green, and blue components of the color, respectively, in
hexadecimal form.  ``FF`` (equivalent to 255 in decimal form) is full
intensity of the respective color, and ``00`` (equivalent to 0 in
decimal form) is no intensity of the respective color.  For example,
``"#FF8000"`` is the same as ``(255, 128, 0)``, or orange.

Integers, treated as hexadecimals, are accepted in the same form as HTML
hex strings, but integral.  For example, ``0xFF8000`` is the same as
``"#FF8000"``.

Position
--------

In all cases of positioning for the SGE, it is based on a
two-dimensional graph with each unit being a pixel.  This graph is not
quite like regular graphs.  The horizontal direction, normally called
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

Information specific to [insert implementation name here]
=========================================================

License
-------

[insert license info here]

Dependencies
------------

- Python [insert Python version here] <http://www.python.org>
- [insert additional dependency here] <[insert dependency link here]>
- [insert additional dependency here] <[insert dependency link here]>
- [...]

[insert other info here]

"""

__version__ = "0.9.2.8"

import sys
import os

# Import implementation-specific libraries like Pygame here

# Constants
PROGRAM_DIR = os.path.dirname(sys.argv[0])
IMPLEMENTATION = "SGE Template"

ALIGN_LEFT = 2
ALIGN_CENTER = 3
ALIGN_RIGHT = 1
ALIGN_TOP = 8
ALIGN_MIDDLE = 12
ALIGN_BOTTOM = 4

BLEND_NORMAL = 0
BLEND_RGB = 1
BLEND_ALPHA = 2
BLEND_ADD = 4
BLEND_SUBTRACT = 8
BLEND_MULTIPLY = 12
BLEND_SCREEN = 16
BLEND_MINIMUM = 20
BLEND_MAXIMUM = 24

BLEND_RGBA_ADD = BLEND_RGB | BLEND_ALPHA | BLEND_ADD
BLEND_RGBA_SUBTRACT = BLEND_RGB | BLEND_ALPHA | BLEND_SUBTRACT
BLEND_RGBA_MULTIPLY = BLEND_RGB | BLEND_ALPHA | BLEND_MULTIPLY
BLEND_RGBA_SCREEN = BLEND_RGB | BLEND_ALPHA | BLEND_SCREEN
BLEND_RGBA_MINIMUM = BLEND_RGB | BLEND_ALPHA | BLEND_MINIMUM
BLEND_RGBA_MAXIMUM = BLEND_RGB | BLEND_ALPHA | BLEND_MAXIMUM

BLEND_RGB_ADD = BLEND_RGB | BLEND_ADD
BLEND_RGB_SUBTRACT = BLEND_RGB | BLEND_SUBTRACT
BLEND_RGB_MULTIPLY = BLEND_RGB | BLEND_MULTIPLY
BLEND_RGB_SCREEN = BLEND_RGB | BLEND_SCREEN
BLEND_RGB_MINIMUM = BLEND_RGB | BLEND_MINIMUM
BLEND_RGB_MAXIMUM = BLEND_RGB | BLEND_MAXIMUM

COLORS = {'white': '#ffffff', 'silver': '#c0c0c0', 'gray': '#808080',
          'black': '#000000', 'red': '#ff0000', 'maroon': '#800000',
          'yellow': '#ffff00', 'olive': '#808000', 'lime': '#00ff00',
          'green': '#008000', 'aqua': '#00ffff', 'teal': '#008080',
          'blue': '#0000ff', 'navy': '#000080', 'fuchsia': '#ff00ff',
          'purple': '#800080'}
COLOR_NAMES = {}
for pair in COLORS.items():
    COLOR_NAMES[pair[1]] = pair[0]

KEYS = {"0": None, "1": None, "2": None, "3": None, "4": None, "5": None,
        "6": None, "7": None, "8": None, "9": None, "a": None, "b": None,
        "c": None, "d": None, "e": None, "f": None, "g": None, "h": None,
        "i": None, "j": None, "k": None, "l": None, "m": None, "n": None,
        "o": None, "p": None, "q": None, "r": None, "s": None, "t": None,
        "u": None, "v": None, "w": None, "x": None, "y": None, "z": None,
        "alt_left": None, "alt_right": None, "ampersand": None,
        "apostrophe": None, "asterisk": None, "at": None, "backslash": None,
        "backspace": None, "backtick": None, "bracket_left": None,
        "bracket_right": None, "break": None, "caps_lock": None, "caret": None,
        "clear": None, "colon": None, "comma": None, "ctrl_left": None,
        "ctrl_right": None, "delete": None, "dollar": None, "down": None,
        "end": None, "enter": None, "equals": None, "escape": None,
        "euro": None, "exclamation": None, "f1": None, "f2": None, "f3": None,
        "f4": None, "f5": None, "f6": None, "f7": None, "f8": None, "f9": None,
        "f10": None, "f11": None, "f12": None, "greater_than": None,
        "hash": None, "help": None, "home": None, "hyphen": None,
        "insert": None, "kp_0": None, "kp_1": None, "kp_2": None, "kp_3": None,
        "kp_4": None, "kp_5": None, "kp_6": None, "kp_7": None, "kp_8": None,
        "kp_9": None, "kp_divide": None, "kp_enter": None, "kp_equals": None,
        "kp_minus": None, "kp_multiply": None, "kp_plus": None,
        "kp_point": None, "left": None, "less_than": None, "menu": None,
        "meta_left": None, "meta_right": None, "mode": None, "num_lock": None,
        "pagedown": None, "pageup": None, "parenthesis_left": None,
        "parenthesis_right": None, "pause": None, "period": None, "plus": None,
        "power": None, "print_screen": None, "question": None, "quote": None,
        "right": None, "scroll_lock": None, "semicolon": None,
        "shift_left": None, "shift_right": None, "slash": None, "space": None,
        "super_left": None, "super_right": None, "sysrq": None, "tab": None,
        "underscore": None, "up":None}
KEY_NAMES = {}
for pair in KEYS.items():
    KEY_NAMES[pair[1]] = pair[0]

MODS = {"alt": None, "alt_left": None, "alt_right": None, "caps_lock": None,
        "ctrl": None, "ctrl_left": None, "ctrl_right": None, "meta": None,
        "meta_left": None, "meta_right": None, "mode": None, "num_lock": None,
        "shift": None, "shift_left": None, "shift_right": None}

MOUSE_BUTTONS = {"left": 0, "right": 1, "middle": 2, "wheel_up": 3,
                 "wheel_down": 4, "wheel_left": 5, "wheel_right": 6}
MOUSE_BUTTON_NAMES = {}
for pair in MOUSE_BUTTONS.items():
    MOUSE_BUTTON_NAMES[pair[1]] = pair[0]

from sge.Game import Game
from sge.Sprite import Sprite
from sge.BackgroundLayer import BackgroundLayer
from sge.Background import Background
from sge.Font import Font
from sge.Sound import Sound
from sge.Music import Music
from sge.StellarClass import StellarClass, Mouse
from sge.Room import Room
from sge.View import View
from sge.functions import *
from sge import collision, joystick, keyboard, mouse


__all__ = [
    # Modules
    "collision", "joystick", "keyboard", "mouse",

    # Constants
    'IMPLEMENTATION', 'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT', 'ALIGN_TOP',
    'ALIGN_MIDDLE', 'ALIGN_BOTTOM', 'BLEND_RGBA_ADD', 'BLEND_RGBA_SUBTRACT',
    'BLEND_RGBA_MULTIPLY', 'BLEND_RGBA_SCREEN', 'BLEND_RGBA_MINIMUM',
    'BLEND_RGBA_MAXIMUM', 'BLEND_RGB_ADD', 'BLEND_RGB_SUBTRACT',
    'BLEND_RGB_MULTIPLY', 'BLEND_RGB_SCREEN', 'BLEND_RGB_MINIMUM',
    'BLEND_RGB_MAXIMUM',

    # Classes
    'Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font', 'Sound',
    'Music', 'StellarClass', 'Room', 'View',

    # Functions
    'show_message', 'get_text_entry'
    ]

# Global variables
game = None
image_directories = [os.path.join(PROGRAM_DIR, 'data', 'images'),
                     os.path.join(PROGRAM_DIR, 'data', 'sprites'),
                     os.path.join(PROGRAM_DIR, 'data', 'backgrounds')]
font_directories = [os.path.join(PROGRAM_DIR, 'data', 'fonts')]
sound_directories = [os.path.join(PROGRAM_DIR, 'data', 'sounds')]
music_directories = [os.path.join(PROGRAM_DIR, 'data', 'music')]
