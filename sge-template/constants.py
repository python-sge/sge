# Stellar Game Engine Template
# Copyright (C) 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os


__all__ = ['IMPLEMENTATION', 'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT',
           'ALIGN_TOP', 'ALIGN_MIDDLE', 'ALIGN_BOTTOM', 'PROGRAM_DIR',
           'COLORS', 'COLOR_NAMES', 'KEYS', 'KEY_NAMES', 'MOUSE_BUTTONS',
           'MOUSE_BUTTON_NAMES']

PROGRAM_DIR = os.path.dirname(sys.argv[0])

COLORS = {'white': '#ffffff', 'silver': '#c0c0c0', 'gray': '#808080',
          'black': '#000000', 'red': '#ff0000', 'maroon': '#800000',
          'yellow': '#ffff00', 'olive': '#808000', 'lime': '#00ff00',
          'green': '#008000', 'aqua': '#00ffff', 'teal': '#008080',
          'blue': '#0000ff', 'navy': '#000080', 'fuchsia': '#ff00ff',
          'purple': '#800080'}
COLOR_NAMES = {}
for pair in COLORS.items():
    COLOR_NAMES[pair[1]] = pair[0]

KEYS = {"0": None, "1": None, "2": None, "3": None, "4": None, "5": None, "6": None, "7": None, "8": None, "9": None, "a": None, "b": None, "c": None, "d": None, "e": None, "f": None, "g": None, "h": None, "i": None, "j": None, "k": None, "l": None, "m": None, "n": None, "o": None, "p": None, "q": None, "r": None, "s": None, "t": None, "u": None, "v": None, "w": None, "x": None, "y": None, "z": None, "alt_left": None, "alt_right": None, "ampersand": None, "apostrophe": None, "asterisk": None, "at": None, "backslash": None, "backspace": None, "backtick": None, "bracket_left": None, "bracket_right": None, "break": None, "caps_lock": None, "caret": None, "clear": None, "colon": None, "comma": None, "ctrl_left": None, "ctrl_right": None, "delete": None, "dollar": None, "down": None, "end": None, "enter": None, "equals": None, "escape": None, "euro": None, "exclamation": None, "f1": None, "f2": None, "f3": None, "f4": None, "f5": None, "f6": None, "f7": None, "f8": None, "f9": None, "f10": None, "f11": None, "f12": None, "greater_than": None, "hash": None, "help": None, "home": None, "hyphen": None, "insert": None, "kp_0": None, "kp_1": None, "kp_2": None, "kp_3": None, "kp_4": None, "kp_5": None, "kp_6": None, "kp_7": None, "kp_8": None, "kp_9": None, "kp_divide": None, "kp_enter": None, "kp_equals": None, "kp_minus": None, "kp_multiply": None, "kp_plus": None, "kp_point": None, "left": None, "less_than": None, "menu":None, "meta_left":None, "meta_right":None, "mode":None, "num_lock":None, "pagedown":None, "pageup":None, "parenthesis_left":None, "parenthesis_right":None, "pause":None, "period":None, "plus":None, "power":None, "print_screen":None, "question":None, "quote":None, "right":None, "scroll_lock":None, "semicolon":None, "shift_left":None, "shift_right":None, "slash":None, "space":None, "super_left":None, "super_right":None, "sysrq":None, "tab":None, "underscore":None, "up":None}
KEY_NAMES = {}
for pair in KEYS.items():
    KEY_NAMES[pair[1]] = pair[0]

MOUSE_BUTTONS = {"left": 0, "right": 1, "middle": 2, "wheel_up": 3,
                 "wheel_down": 4, "wheel_left": 5, "wheel_right": 6}
MOUSE_BUTTON_NAMES = {}
for pair in MOUSE_BUTTONS.items():
    MOUSE_BUTTON_NAMES[pair[1]] = pair[0]

IMPLEMENTATION = "SGE Template"
ALIGN_LEFT = 2
ALIGN_CENTER = 3
ALIGN_RIGHT = 1
ALIGN_TOP = 8
ALIGN_MIDDLE = 12
ALIGN_BOTTOM = 4
