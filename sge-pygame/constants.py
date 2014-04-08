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

import sys
import os

import pygame


__all__ = ['IMPLEMENTATION', 'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT',
           'ALIGN_TOP', 'ALIGN_MIDDLE', 'ALIGN_BOTTOM', 'BLEND_NORMAL',
           'BLEND_RGB', 'BLEND_ALPHA', 'BLEND_ADD', 'BLEND_SUBTRACT',
           'BLEND_MULTIPLY', 'BLEND_SCREEN', 'BLEND_MINIMUM', 'BLEND_MAXIMUM',
           'BLEND_RGBA_ADD', 'BLEND_RGBA_SUBTRACT', 'BLEND_RGBA_MULTIPLY',
           'BLEND_RGBA_SCREEN', 'BLEND_RGBA_MINIMUM', 'BLEND_RGBA_MAXIMUM',
           'BLEND_RGB_ADD', 'BLEND_RGB_SUBTRACT', 'BLEND_RGB_MULTIPLY',
           'BLEND_RGB_SCREEN', 'BLEND_RGB_MINIMUM', 'BLEND_RGB_MAXIMUM',
           'PROGRAM_DIR', 'COLORS', 'COLOR_NAMES', 'KEYS', 'KEY_NAMES',
           'MOUSE_BUTTONS', 'MOUSE_BUTTON_NAMES',
           'COLLISION_AREA_SIZE_DEFAULT', 'DEBUG']

PROGRAM_DIR = os.path.dirname(sys.argv[0])
DEBUG = True
if DEBUG:
    print("SGE Art of Debugging enabled.")

COLORS = {'white': '#ffffff', 'silver': '#c0c0c0', 'gray': '#808080',
          'black': '#000000', 'red': '#ff0000', 'maroon': '#800000',
          'yellow': '#ffff00', 'olive': '#808000', 'lime': '#00ff00',
          'green': '#008000', 'aqua': '#00ffff', 'teal': '#008080',
          'blue': '#0000ff', 'navy': '#000080', 'fuchsia': '#ff00ff',
          'purple': '#800080'}
COLOR_NAMES = {}
for pair in COLORS.items():
    COLOR_NAMES[pair[1]] = pair[0]

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

MOUSE_BUTTONS = {"left": 1, "right": 3, "middle": 2, "wheel_up": 4,
                 "wheel_down": 5, "wheel_left": 6, "wheel_right": 7}
MOUSE_BUTTON_NAMES = {}
for pair in MOUSE_BUTTONS.items():
    MOUSE_BUTTON_NAMES[pair[1]] = pair[0]

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
