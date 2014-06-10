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

# INSTRUCTIONS FOR DEVELOPING AN IMPLEMENTATION: Replace  the notice
# above as well as the notices contained in other source files with your
# own copyright notice.  Recommended free  licenses are  the GNU General
# Public License, GNU Lesser General Public License, Expat License, or
# Apache License 2.0.

import sge


__all__ = ["get_pressed", "get_modifier", "get_focused", "set_repeat",
           "get_repeat_enabled", "get_repeat_interval", "get_repeat_delay"]


def get_pressed(key):
    """Return whether or not a key is pressed.

    Arguments:

    - ``key`` -- The identifier string of the key to check; see below
      for a table of the identifier strings.

    ==================== ======================= =================
    Key Name             Identifier String       Unicode Character
    ==================== ======================= =================
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
    Left Arrow           ``"left"``
    Right Arrow          ``"right"``
    Up Arrow             ``"up"``
    Down Arrow           ``"down"``
    Home                 ``"home"``
    End                  ``"end"``
    Page Up              ``"pageup"``
    Page Down            ``"pagedown"``
    Tab                  ``"tab"``               ``"\\t"``
    Space Bar            ``"space"``             ``" "``
    Enter/Return         ``"enter"``             ``"\\n"``
    Backspace            ``"backspace"``         ``"\\b"``
    Delete               ``"delete"``
    Clear                ``"clear"``
    Left Shift           ``"shift_left"``
    Right Shift          ``"shift_right"``
    Left Ctrl            ``"ctrl_left"``
    Right Ctrl           ``"ctrl_right"``
    Left Alt             ``"alt_left"``
    Right Alt            ``"alt_right"``
    Left Super           ``"super_left"``
    Right Super          ``"super_right"``
    Mode                 ``"mode"``
    Menu                 ``"menu"``
    Caps Lock            ``"caps_lock"``
    Esc                  ``"escape"``
    Num Lock             ``"num_lock"``
    Scroll Lock          ``"scroll_lock"``
    Break                ``"break"``
    Insert               ``"insert"``
    Pause                ``"pause"``
    Power                ``"power"``
    Print Screen         ``"print_screen"``
    SysRq                ``"sysrq"``
    F1                   ``"f1"``
    F2                   ``"f2"``
    F3                   ``"f3"``
    F4                   ``"f4"``
    F5                   ``"f5"``
    F6                   ``"f6"``
    F7                   ``"f7"``
    F8                   ``"f8"``
    F9                   ``"f9"``
    F10                  ``"f10"``
    F11                  ``"f11"``
    F12                  ``"f12"``
    ==================== ======================= =================

    """
    # TODO


def get_modifier(key):
    """Return whether or not a modifier key is being held.

    Arguments:

    - ``key`` -- The identifier string of the modifier key to check; see
      below for a table of the identifier strings.

    ================= =================
    Modifier Key Name Identifier String
    ================= =================
    Alt               alt
    Left Alt          alt_left
    Right Alt         alt_right
    Ctrl              ctrl
    Left Ctrl         ctrl_left
    Right Ctrl        ctrl_right
    Meta              meta
    Left Meta         meta_left
    Right Meta        meta_right
    Shift             shift
    Left Shift        shift_left
    Right Shift       shift_right
    Mode              mode
    Caps Lock         caps_lock
    Num Lock          num_lock

    """
    # TODO


def get_focused():
    """Return whether or not the game has keyboard focus."""
    # TODO


def set_repeat(enabled=True, interval=0, delay=0):
    """Set repetition of key press events.

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
    # TODO


def get_repeat_enabled():
    """Return whether or not repetition of key press events is enabled.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.

    """
    # TODO


def get_repeat_interval():
    """Return the interval in between each repeated key press event.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.

    """
    # TODO


def get_repeat_delay():
    """Return the delay before repeating key press events.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.

    """
    # TODO
