# Copyright (C) 2012-2017 Julie Marchant <onpon4@riseup.net>
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
The SGE Game Engine ("SGE", pronounced like "Sage") is a general-purpose
2-D game engine.  It takes care of several details for you so you can
focus on the game itself.  This makes more rapid game development
possible, and it also makes the SGE easy to learn.

The SGE is `libre software <http://gnu.org/philosophy/free-sw.html>`_,
and the SGE documentation (including all docstrings) is released to the
public domain via CC0.

Although it isn't required, you are encouraged to release your games'
code under a libre software license, such as the GNU General Public
License, the Expat License, or the Apache License.  Doing so is easy,
does not negatively affect you, and is highly appreciated as a
contribution to a free society.

SGE Concepts
============

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
common in 2-D game development and is also how pixels in most image
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

If two objects with the same Z-axis value overlap, the object which was
most recently added to the room is placed in front.

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

:meth:`sge.dsp.Game.pump_input` should be called every frame regardless
of whether or not user input is needed.  Failing to call it will cause
the queue to build up, but more importantly, the OS may decide that the
program has locked up if it doesn't get a response for a long time.

:meth:`sge.dsp.Game.regulate_speed` limits the frame rate of the game
and tells you how much time has passed since the last frame.  It is not
technically necessary, but using it is highly recommended; otherwise,
the CPU will be working harder than it needs to and if things are
moving, their speed will be irregular.

:meth:`sge.dsp.Game.refresh` is necessary for any changes to the screen
to be seen by the user.  This includes new objects, removed objects, new
projections, discontinued projections, etc.

Global Variables and Constants
==============================

.. data:: sge.IMPLEMENTATION

   A string indicating the name of the SGE implementation.

.. data:: sge.SCALE_METHODS

   A list of specific scale methods supported by the SGE implementation.

   .. note::

      This list does not include the generic scale methods, ``"noblur"``
      and ``"smooth"``.  It is also possible for this list to be empty.

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

   Stores the current :class:`sge.dsp.Game` object.  If there is no
   :class:`sge.dsp.Game` object currently, this variable is set to
   :const:`None`.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "1.5"

import sys
import os

try:
    import pygame
except ImportError as e:
    try:
        import pygame_sdl2
    except ImportError:
        raise e
    else:
        pygame_sdl2.import_as_pygame()
        import pygame

# Constants
IMPLEMENTATION = "Pygame SGE"
SCALE_METHODS = ["scale2x"]

BLEND_NORMAL = None
BLEND_ALPHA = 1
BLEND_RGB_ADD = 2
BLEND_RGB_SUBTRACT = 4
BLEND_RGB_MULTIPLY = 6
BLEND_RGB_SCREEN = 8
BLEND_RGB_MINIMUM = 10
BLEND_RGB_MAXIMUM = 12

BLEND_RGBA_ADD = BLEND_ALPHA | BLEND_RGB_ADD
BLEND_RGBA_SUBTRACT = BLEND_ALPHA | BLEND_RGB_SUBTRACT
BLEND_RGBA_MULTIPLY = BLEND_ALPHA | BLEND_RGB_MULTIPLY
BLEND_RGBA_SCREEN = BLEND_ALPHA | BLEND_RGB_SCREEN
BLEND_RGBA_MINIMUM = BLEND_ALPHA | BLEND_RGB_MINIMUM
BLEND_RGBA_MAXIMUM = BLEND_ALPHA | BLEND_RGB_MAXIMUM

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
        "undef_clear": pygame.K_CLEAR, "colon": pygame.K_COLON,
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
        "hash": pygame.K_HASH, "undef_help": pygame.K_HELP,
        "home": pygame.K_HOME, "hyphen": pygame.K_MINUS,
        "insert": pygame.K_INSERT,
        "kp_0": pygame.K_KP0, "kp_1": pygame.K_KP1, "kp_2": pygame.K_KP2,
        "kp_3": pygame.K_KP3, "kp_4": pygame.K_KP4, "kp_5": pygame.K_KP5,
        "kp_6": pygame.K_KP6, "kp_7": pygame.K_KP7, "kp_8": pygame.K_KP8,
        "kp_9": pygame.K_KP9, "kp_divide": pygame.K_KP_DIVIDE,
        "kp_enter": pygame.K_KP_ENTER, "kp_equals": pygame.K_KP_EQUALS,
        "kp_minus": pygame.K_KP_MINUS, "kp_multiply": pygame.K_KP_MULTIPLY,
        "kp_plus": pygame.K_KP_PLUS, "kp_point": pygame.K_KP_PERIOD,
        "left": pygame.K_LEFT, "less_than": pygame.K_LESS,
        "menu": pygame.K_MENU, "meta_left": pygame.K_LMETA,
        "meta_right": pygame.K_RMETA, "undef_mode": pygame.K_MODE,
        "num_lock": pygame.K_NUMLOCK, "pagedown": pygame.K_PAGEDOWN,
        "pageup": pygame.K_PAGEUP, "parenthesis_left": pygame.K_LEFTPAREN,
        "parenthesis_right": pygame.K_RIGHTPAREN, "pause": pygame.K_PAUSE,
        "period": pygame.K_PERIOD, "plus": pygame.K_PLUS,
        "undef_power": pygame.K_POWER, "print_screen": pygame.K_PRINT,
        "question": pygame.K_QUESTION, "quote": pygame.K_QUOTEDBL,
        "right": pygame.K_RIGHT, "scroll_lock": pygame.K_SCROLLOCK,
        "semicolon": pygame.K_SEMICOLON, "shift_left": pygame.K_LSHIFT,
        "shift_right": pygame.K_RSHIFT, "slash": pygame.K_SLASH,
        "space": pygame.K_SPACE, "undef_super_left": pygame.K_LSUPER,
        "undef_super_right": pygame.K_RSUPER, "sysrq": pygame.K_SYSREQ,
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

from sge import (collision, dsp, gfx, input, joystick, keyboard, mouse, snd, s,
                 r)


__all__ = [
    # Modules
    "collision", "gfx", "input", "joystick", "keyboard", "mouse",

    # Constants
    'IMPLEMENTATION', 'BLEND_RGBA_ADD', 'BLEND_RGBA_SUBTRACT',
    'BLEND_RGBA_MULTIPLY', 'BLEND_RGBA_SCREEN', 'BLEND_RGBA_MINIMUM',
    'BLEND_RGBA_MAXIMUM', 'BLEND_RGB_ADD', 'BLEND_RGB_SUBTRACT',
    'BLEND_RGB_MULTIPLY', 'BLEND_RGB_SCREEN', 'BLEND_RGB_MINIMUM',
    'BLEND_RGB_MAXIMUM',
    ]

# Global variables
game = None

# Uncomment this line to tell SDL to center the window.  Disabled by
# default because it seems to cause some weird behavior with window
# resizing on at least some systems.
#os.environ['SDL_VIDEO_CENTERED'] = '1'
