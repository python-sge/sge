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
This module provides functions related to keyboard input.

As a general rule, any key press has two strings associated with it: an
identifier string, and a unicode string.  The identifier string is a
consistent identifier for what the key is, consisting only of
alphanumeric ASCII text.  The unicode string is the text associated with
the key press; typically this is an ASCII character printed on the key,
but in some cases (e.g. when an input method is used), it could be any
kind of text.  As a general rule, the unicode string should always be
used for text entry, while the identifier string should be used for all
other purposes.

The table below lists all standard keys along with their corresponding
identifier and unicode strings.  Note that SGE implementations are not
necessarily required to support recognizing all of them, although they
are strongly encouraged to do so. Any key not found on this table, if
detected, will be arbitrarily but consistently assigned an identifier
string beginning with ``"undef_"``.

==================== ======================= ==============
Key Name             Identifier String       Unicode String
==================== ======================= ==============
0                    ``"0"``                 ``"0"``
1                    ``"1"``                 ``"1"``
2                    ``"2"``                 ``"2"``
3                    ``"3"``                 ``"3"``
4                    ``"4"``                 ``"4"``
5                    ``"5"``                 ``"5"``
6                    ``"6"``                 ``"6"``
7                    ``"7"``                 ``"7"``
8                    ``"8"``                 ``"8"``
9                    ``"9"``                 ``"9"``
A                    ``"a"``                 ``"a"``
B                    ``"b"``                 ``"b"``
C                    ``"c"``                 ``"c"``
D                    ``"d"``                 ``"d"``
E                    ``"e"``                 ``"e"``
F                    ``"f"``                 ``"f"``
G                    ``"g"``                 ``"g"``
H                    ``"h"``                 ``"h"``
I                    ``"i"``                 ``"i"``
J                    ``"j"``                 ``"j"``
K                    ``"k"``                 ``"k"``
L                    ``"l"``                 ``"l"``
M                    ``"m"``                 ``"m"``
N                    ``"n"``                 ``"n"``
O                    ``"o"``                 ``"o"``
P                    ``"p"``                 ``"p"``
Q                    ``"q"``                 ``"q"``
R                    ``"r"``                 ``"r"``
S                    ``"s"``                 ``"s"``
T                    ``"t"``                 ``"t"``
U                    ``"u"``                 ``"u"``
V                    ``"v"``                 ``"v"``
W                    ``"w"``                 ``"w"``
X                    ``"x"``                 ``"x"``
Y                    ``"y"``                 ``"y"``
Z                    ``"z"``                 ``"z"``
Period               ``"period"``            ``"."``
Comma                ``"comma"``             ``","``
Less Than            ``"less_than"``         ``"<"``
Greater Than         ``"greater_than"``      ``">"``
Forward Slash        ``"slash"``             ``"/"``
Question Mark        ``"question"``          ``"?"``
Apostrophe           ``"apostrophe"``        ``"'"``
Quotation Mark       ``"quote"``             ``'"'``
Colon                ``"colon"``             ``":"``
Semicolon            ``"semicolon"``         ``";"``
Exclamation Point    ``"exclamation"``       ``"!"``
At                   ``"at"``                ``"@"``
Hash                 ``"hash"``              ``"#"``
Dollar Sign          ``"dollar"``            ``"$"``
Percent Sign         ``"percent"``           ``"%"``
Carat                ``"carat"``             ``"^"``
Ampersand            ``"ampersand"``         ``"&"``
Asterisk             ``"asterisk"``          ``"*"``
Left Parenthesis     ``"parenthesis_left"``  ``"("``
Right Parenthesis    ``"parenthesis_right"`` ``")"``
Hyphen               ``"hyphen"``            ``"-"``
Underscore           ``"underscore"``        ``"_"``
Plus Sign            ``"plus"``              ``"+"``
Equals Sign          ``"equals"``            ``"="``
Left Bracket         ``"bracket_left"``      ``"["``
Right Bracket        ``"bracket_right"``     ``"]"``
Left Brace           ``"brace_left"``        ``"{"``
Right Brace          ``"brace_right"``       ``"}"``
Backslash            ``"backslash"``         ``"\\\\"``
Backtick             ``"backtick"``          ``"`"``
Euro                 ``"euro"``              ``"\\u20ac"``
Keypad 0             ``"kp_0"``              ``"0"``
Keypad 1             ``"kp_1"``              ``"1"``
Keypad 2             ``"kp_2"``              ``"2"``
Keypad 3             ``"kp_3"``              ``"3"``
Keypad 4             ``"kp_4"``              ``"4"``
Keypad 5             ``"kp_5"``              ``"5"``
Keypad 6             ``"kp_6"``              ``"6"``
Keypad 7             ``"kp_7"``              ``"7"``
Keypad 8             ``"kp_8"``              ``"8"``
Keypad 9             ``"kp_9"``              ``"9"``
Keypad Decimal Point ``"kp_point"``          ``"."``
Keypad Plus          ``"kp_plus"``           ``"+"``
Keypad Minus         ``"kp_minus"``          ``"-"``
Keypad Multiply      ``"kp_multiply"``       ``"*"``
Keypad Divide        ``"kp_divide"``         ``"/"``
Keypad Equals        ``"kp_equals"``         ``"="``
Keypad Enter         ``"kp_enter"``          ``"\\n"``
Left Arrow           ``"left"``              ``""``
Right Arrow          ``"right"``             ``""``
Up Arrow             ``"up"``                ``""``
Down Arrow           ``"down"``              ``""``
Home                 ``"home"``              ``""``
End                  ``"end"``               ``""``
Page Up              ``"pageup"``            ``""``
Page Down            ``"pagedown"``          ``""``
Tab                  ``"tab"``               ``"\\t"``
Space Bar            ``"space"``             ``" "``
Enter/Return         ``"enter"``             ``"\\n"``
Backspace            ``"backspace"``         ``"\\b"``
Delete               ``"delete"``            ``""``
Left Shift           ``"shift_left"``        ``""``
Right Shift          ``"shift_right"``       ``""``
Left Ctrl            ``"ctrl_left"``         ``""``
Right Ctrl           ``"ctrl_right"``        ``""``
Left Alt             ``"alt_left"``          ``""``
Right Alt            ``"alt_right"``         ``""``
Left Meta            ``"meta_left"``         ``""``
Right Meta           ``"meta_right"``        ``""``
Caps Lock            ``"caps_lock"``         ``""``
Esc                  ``"escape"``            ``""``
Num Lock             ``"num_lock"``          ``""``
Scroll Lock          ``"scroll_lock"``       ``""``
Break                ``"break"``             ``""``
Insert               ``"insert"``            ``""``
Pause                ``"pause"``             ``""``
Print Screen         ``"print_screen"``      ``""``
SysRq                ``"sysrq"``             ``""``
F1                   ``"f1"``                ``""``
F2                   ``"f2"``                ``""``
F3                   ``"f3"``                ``""``
F4                   ``"f4"``                ``""``
F5                   ``"f5"``                ``""``
F6                   ``"f6"``                ``""``
F7                   ``"f7"``                ``""``
F8                   ``"f8"``                ``""``
F9                   ``"f9"``                ``""``
F10                  ``"f10"``               ``""``
F11                  ``"f11"``               ``""``
F12                  ``"f12"``               ``""``
==================== ======================= ==============
"""


__all__ = ["get_pressed", "get_modifier", "get_focused", "set_repeat",
           "get_repeat_enabled", "get_repeat_interval", "get_repeat_delay"]


import pygame

import sge


_repeat_enabled = False


def get_pressed(key):
    """
    Return whether or not a key is pressed.

    Arguments:

    - ``key`` -- The identifier string of the modifier key to check; see
      the table in the documentation for :mod:`sge.keyboard`.
    """
    key = key.lower()
    if key in sge.KEYS:
        return pygame.key.get_pressed()[sge.KEYS[key]]
    else:
        return False


def get_modifier(key):
    """
    Return whether or not a modifier key is being held.

    Arguments:

    - ``key`` -- The identifier string of the modifier key to check; see
      the table below.

    ================= =================
    Modifier Key Name Identifier String
    ================= =================
    Alt               ``"alt"``
    Left Alt          ``"alt_left"``
    Right Alt         ``"alt_right"``
    Ctrl              ``"ctrl"``
    Left Ctrl         ``"ctrl_left"``
    Right Ctrl        ``"ctrl_right"``
    Meta              ``"meta"``
    Left Meta         ``"meta_left"``
    Right Meta        ``"meta_right"``
    Shift             ``"shift"``
    Left Shift        ``"shift_left"``
    Right Shift       ``"shift_right"``
    Mode              ``"mode"``
    Caps Lock         ``"caps_lock"``
    Num Lock          ``"num_lock"``
    ================= =================
    """
    key = key.lower()
    if key in sge.MODS:
        return pygame.key.get_mods() & sge.MODS[key]
    else:
        return False


def get_focused():
    """Return whether or not the game has keyboard focus."""
    return pygame.key.get_focused()


def set_repeat(enabled=True, interval=0, delay=0):
    """
    Set repetition of key press events.

    Arguments:

    - ``enabled`` -- Whether or not to enable repetition of key press
      events.
    - ``interval`` -- The time in milliseconds in between each repeated
      key press event.
    - ``delay`` -- The time in milliseconds to wait after the first key
      press event before repeating key press events.

    If ``enabled`` is set to true, this causes a key being held down to
    generate additional key press events as long as it remains held
    down.
    """
    global _repeat_enabled
    _repeat_enabled = enabled
    if enabled:
        pygame.key.set_repeat(delay, interval)
    else:
        pygame.key.set_repeat()


def get_repeat_enabled():
    """
    Return whether or not repetition of key press events is enabled.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.
    """
    return _repeat_enabled


def get_repeat_interval():
    """
    Return the interval in between each repeated key press event.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.
    """
    return pygame.key.get_repeat()[1]


def get_repeat_delay():
    """
    Return the delay before repeating key press events.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.
    """
    return pygame.key.get_repeat()[0]
