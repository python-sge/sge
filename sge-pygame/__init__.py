# Copyright (C) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
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

Official implementations of the SGE are `free/libre software
<http://gnu.org/philosophy/free-sw.html>`_, and the SGE documentation is
free/libre as well.

Even if it isn't required, you are encouraged to release your games'
code under a free/libre software license, such as the GNU General Public
License, the Expat License, or the Apache License.  Doing so is easy,
does not negatively affect you, and is highly appreciated as a
contribution to a free society.

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

At a lower level, it is possible to read "input events" from
:attr:`sge.game.input_events` and handle them manually.  See the
documentation for :mod:`sge.input` for more information.  This is not
recommended, however, unless you are running your own loop for some
reason (in which case it is necessary to do this in order to get input
from the user).

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

The Game Loop
-------------

There can occasionally be times where you want to run your own loop,
independent of the SGE's main loop.  This is not recommended in general,
but if you must (to freeze the game, for example), you should know the
general game loop structure::

    while True:
        # Input events
        sge.game.pump_input()
        while sge.game.input_events:
            event = sge.game.input_events.pop(0)

            # Handle event

        # Regulate speed
        time_passed = sge.game.regulate_speed()

        # Logic (e.g. collision detection and step events)

        # Refresh
        sge.game.refresh()

:meth:`sge.Game.pump_input` should be called every frame regardless of
whether or not user input is needed.  Failing to call it will cause the
queue to build up, but more importantly, the OS may decide that the
program has locked up if it doesn't get a response for a long time.

:meth:`sge.Game.regulate_speed` limits the frame rate of the game and
tells you how much time has passed since the last frame.  It is not
technically necessary, but using it is highly recommended; otherwise,
the CPU will be working harder than it needs to and if things are
moving, their speed will be irregular.

:meth:`sge.Game.refresh` is necessary for any changes to the screen to
be seen by the user.  This includes new objects, removed objects, new
projections, discontinued projections, etc.

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

- Python 3.1 or later <http://www.python.org>
- Pygame 1.9.2a0 or later <http://pygame.org>

Formats Support
---------------

:class:`sge.Sprite` supports the following image formats:

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

:class:`sge.Sound` supports the following audio formats:

- Uncompressed WAV
- Ogg Vorbis

:class:`sge.Music` supports the following audio formats:

- Ogg Vorbis
- MP3 (support limited; use not recommended)
- MOD
- XM
- MIDI

For starting position in MOD files, the pattern order number is used
instead of the number of milliseconds.

If Pygame is built without full image support, :class:`sge.Sprite` will
only be able to load uncompressed BMP images.

The pygame.mixer module, which is used for all audio playback, is
optional and depends on SDL_mixer; if pygame.mixer is unavailable,
sounds and music will not play.

On some systems, :class:`sge.Music` attempting to load an unsupported
format can crash the game.  Since MP3 support is limited, it is best to
avoid using it; consider using Ogg Vorbis instead.

Missing Features
----------------

:meth:`sge.Sprite.draw_line`, :meth:`sge.Room.project_line`, and
:meth:`sge.Game.project_line` support anti-aliasing for lines with a
thickness of 1 only.  :meth:`sge.Sprite.draw_text`,
:meth:`sge.Room.project_text`, and :meth:`sge.Game.project_text` support
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

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.10.1.3"

import sys
import os

import pygame

# Constants
PROGRAM_DIR = os.path.dirname(sys.argv[0])
IMPLEMENTATION = "Pygame SGE"
COLLISION_AREA_SIZE_DEFAULT = 128

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

MUSIC_END_EVENT = pygame.USEREVENT + 1

KEYS = {"0": pygame.K_0, "1": pygame.K_1, "2": pygame.K_2, "3": pygame.K_3,
        "4": pygame.K_4, "5": pygame.K_5, "6": pygame.K_6, "7": pygame.K_7,
        "8": pygame.K_8, "9": pygame.K_9, "a": pygame.K_a, "b": pygame.K_b,
        "c": pygame.K_c, "d": pygame.K_d, "e": pygame.K_e, "f": pygame.K_f,
        "g": pygame.K_g, "h": pygame.K_h, "i": pygame.K_i, "j": pygame.K_j,
        "k": pygame.K_k, "l": pygame.K_l, "m": pygame.K_m, "n": pygame.K_n,
        "o": pygame.K_o, "p": pygame.K_p, "q": pygame.K_q, "r": pygame.K_r,
        "s": pygame.K_s, "t": pygame.K_t, "u": pygame.K_u, "v": pygame.K_v,
        "w": pygame.K_w, "x": pygame.K_x, "y": pygame.K_y, "z": pygame.K_z,
        "alt_left": pygame.K_LALT, "alt_right": pygame.K_RALT,
        "ampersand": pygame.K_AMPERSAND, "apostrophe": pygame.K_QUOTE,
        "asterisk": pygame.K_ASTERISK, "at": pygame.K_AT,
        "backslash": pygame.K_BACKSLASH, "backspace": pygame.K_BACKSPACE,
        "backtick": pygame.K_BACKQUOTE, "bracket_left": pygame.K_LEFTBRACKET,
        "bracket_right": pygame.K_RIGHTBRACKET, "break": pygame.K_BREAK,
        "caps_lock": pygame.K_CAPSLOCK, "caret": pygame.K_CARET,
        "clear": pygame.K_CLEAR, "colon": pygame.K_COLON,
        "comma": pygame.K_COMMA, "ctrl_left": pygame.K_LCTRL,
        "ctrl_right": pygame.K_RCTRL, "delete": pygame.K_DELETE,
        "dollar": pygame.K_DOLLAR, "down": pygame.K_DOWN, "end": pygame.K_END,
        "enter": pygame.K_RETURN, "equals": pygame.K_EQUALS,
        "escape": pygame.K_ESCAPE, "euro": pygame.K_EURO,
        "exclamation": pygame.K_EXCLAIM, "f1": pygame.K_F1, "f2": pygame.K_F2,
        "f3": pygame.K_F3, "f4": pygame.K_F4, "f5": pygame.K_F5,
        "f6": pygame.K_F6, "f7": pygame.K_F7, "f8": pygame.K_F8,
        "f9": pygame.K_F9, "f10": pygame.K_F10, "f11": pygame.K_F11,
        "f12": pygame.K_F12, "greater_than": pygame.K_GREATER,
        "hash": pygame.K_HASH, "help": pygame.K_HELP, "home": pygame.K_HOME,
        "hyphen": pygame.K_MINUS, "insert": pygame.K_INSERT,
        "kp_0": pygame.K_KP0, "kp_1": pygame.K_KP1, "kp_2": pygame.K_KP2,
        "kp_3": pygame.K_KP3, "kp_4": pygame.K_KP4, "kp_5": pygame.K_KP5,
        "kp_6": pygame.K_KP6, "kp_7": pygame.K_KP7, "kp_8": pygame.K_KP8,
        "kp_9": pygame.K_KP9, "kp_divide": pygame.K_KP_DIVIDE,
        "kp_enter": pygame.K_KP_ENTER, "kp_equals": pygame.K_KP_EQUALS,
        "kp_minus": pygame.K_KP_MINUS, "kp_multiply": pygame.K_KP_MULTIPLY,
        "kp_plus": pygame.K_KP_PLUS, "kp_point": pygame.K_KP_PERIOD,
        "left": pygame.K_LEFT, "less_than": pygame.K_LESS,
        "menu": pygame.K_MENU, "meta_left": pygame.K_LMETA,
        "meta_right": pygame.K_RMETA, "mode": pygame.K_MODE,
        "num_lock": pygame.K_NUMLOCK, "pagedown": pygame.K_PAGEDOWN,
        "pageup": pygame.K_PAGEUP, "parenthesis_left": pygame.K_LEFTPAREN,
        "parenthesis_right": pygame.K_RIGHTPAREN, "pause": pygame.K_PAUSE,
        "period": pygame.K_PERIOD, "plus": pygame.K_PLUS,
        "power": pygame.K_POWER, "print_screen": pygame.K_PRINT,
        "question": pygame.K_QUESTION, "quote": pygame.K_QUOTEDBL,
        "right": pygame.K_RIGHT, "scroll_lock": pygame.K_SCROLLOCK,
        "semicolon": pygame.K_SEMICOLON, "shift_left": pygame.K_LSHIFT,
        "shift_right": pygame.K_RSHIFT, "slash": pygame.K_SLASH,
        "space": pygame.K_SPACE, "super_left": pygame.K_LSUPER,
        "super_right": pygame.K_RSUPER, "sysrq": pygame.K_SYSREQ,
        "tab": pygame.K_TAB, "underscore": pygame.K_UNDERSCORE,
        "up": pygame.K_UP}
KEY_NAMES = {}
for pair in KEYS.items():
    KEY_NAMES[pair[1]] = pair[0]

MODS = {"alt": pygame.KMOD_ALT, "alt_left": pygame.KMOD_LALT,
        "alt_right": pygame.KMOD_RALT, "caps_lock": pygame.KMOD_CAPS,
        "ctrl": pygame.KMOD_CTRL, "ctrl_left": pygame.KMOD_LCTRL,
        "ctrl_right": pygame.KMOD_RCTRL, "meta": pygame.KMOD_META,
        "meta_left": pygame.KMOD_LMETA, "meta_right": pygame.KMOD_RMETA,
        "mode": pygame.KMOD_MODE, "num_lock": pygame.KMOD_NUM,
        "shift": pygame.KMOD_SHIFT, "shift_left": pygame.KMOD_LSHIFT,
        "shift_right": pygame.KMOD_RSHIFT}

MOUSE_BUTTONS = {"left": 1, "right": 3, "middle": 2, "wheel_up": 4,
                 "wheel_down": 5, "wheel_left": 6, "wheel_right": 7}
MOUSE_BUTTON_NAMES = {}
for pair in MOUSE_BUTTONS.items():
    MOUSE_BUTTON_NAMES[pair[1]] = pair[0]

from sge.Color import Color
from sge.Game import Game
from sge.Sprite import Sprite
from sge.BackgroundLayer import BackgroundLayer
from sge.Background import Background
from sge.Font import Font
from sge.Sound import Sound
from sge.Music import Music
from sge.Object import Object, Mouse, _PygameProjectionSprite
from sge.Room import Room
from sge.View import View
from sge import collision, input, joystick, keyboard, mouse


__all__ = [
    # Modules
    "collision", "input", "joystick", "keyboard", "mouse",

    # Constants
    'IMPLEMENTATION', 'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT', 'ALIGN_TOP',
    'ALIGN_MIDDLE', 'ALIGN_BOTTOM', 'BLEND_RGBA_ADD', 'BLEND_RGBA_SUBTRACT',
    'BLEND_RGBA_MULTIPLY', 'BLEND_RGBA_SCREEN', 'BLEND_RGBA_MINIMUM',
    'BLEND_RGBA_MAXIMUM', 'BLEND_RGB_ADD', 'BLEND_RGB_SUBTRACT',
    'BLEND_RGB_MULTIPLY', 'BLEND_RGB_SCREEN', 'BLEND_RGB_MINIMUM',
    'BLEND_RGB_MAXIMUM',

    # Classes
    'Color', 'Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font',
    'Sound', 'Music', 'Object', 'Room', 'View',

    # Functions
    'show_message', 'get_text_entry',
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

# Uncomment this line to tell SDL to center the window.  Disabled by
# default because it seems to cause some weird behavior with window
# resizing on at least some systems.
#os.environ['SDL_VIDEO_CENTERED'] = '1'


def _scale(surface, width, height):
    # Scale the given surface to the given width and height, taking the
    # scale factor of the screen into account.
    width = int(round(width * game._xscale))
    height = int(round(height * game._yscale))

    if game.scale_smooth:
        try:
            new_surf = pygame.transform.smoothscale(surface, (width, height))
        except pygame.error:
            new_surf = pygame.transform.scale(surface, (width, height))
    else:
        new_surf = pygame.transform.scale(surface, (width, height))

    return new_surf
