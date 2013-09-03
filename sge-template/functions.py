# The SGE Template
# Written in 2012, 2013 by Julian Marchant <onpon4@riseup.net> 
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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sge


__all__ = ['show_message', 'get_text_entry', 'get_key_pressed',
           'get_mouse_button_pressed', 'get_joystick_axis', 'get_joystick_hat',
           'get_joystick_button_pressed', 'get_joysticks', 'get_joystick_axes',
           'get_joystick_hats', 'get_joystick_buttons']


def show_message(text, buttons=('OK',), default=0):
    """Show a dialog box and return the button pressed.

    Arguments:

    - ``text`` -- The message to show in the dialog box as a string.
    - ``buttons`` -- A list or tuple of strings to put in each of the
      buttons from left to right.
    - ``default`` -- The number of the button to select by default,
      where ``0`` is the first button.

    The dialog box is placed at the center of the window.  The message
    is horizontally aligned to the left and vertically aligned to the
    middle.  All other visual design considerations are decided by the
    SGE.

    While the dialog box is being shown, all events are stopped.  If the
    operating system tells the game to close, the dialog box will close
    immediately, returning :const:`None`, and leak the command to the
    rest of the game (causing Close events).  If the Esc key is pressed,
    the dialog box will close immediately, returning :const:`None`.  If
    the right arrow key or Tab key is pressed, a joystick axis is moved
    from a position less than ``0.75`` to a position greater than or
    equal to ``0.75``, a joystick HAT is moved to the right, or a
    joystick trackball is moved to the right by at least ``0.75``, the
    selection is moved to the right by one; if what is currently
    selected is the last button, the first button will be selected.  If
    the left arrow key is pressed, a joystick axis is moved from a
    position greater than ``-0.75`` to a position less than or equal to
    ``-0.75``, a joystick HAT is moved to the left, or a joystick
    trackball is moved to the left by at least ``0.75``, the selection
    is moved to the left by one; if what is currently selected is the
    first button, the last button will be selected.  If the Enter key,
    the keypad Enter key, or any joystick button is pressed and then
    released, the dialog box is closed and the number of the of the
    currently selected button is returned, where ``0`` is the first
    button.  If the left mouse button is pressed and then released while
    the mouse is hovering over a button, the dialog box is closed and
    the number of the button the mouse is currently hovering over is
    returned, where ``0`` is the first button.

    """
    # TODO


def get_text_entry(text, default=''):
    """Show a text entry dialog box and return the text entered.

    Arguments:

    - ``text`` -- The message to show in the dialog box as a string.
    - ``default`` -- The text to put in the text entry field initially.

    The text entry dialog box is mostly the same as the regular dialog
    box -- see the documentation for :func:`show_message` for more
    information -- but there are some key differences, outlined here.

    There is always an OK button on the right and a Cancel button on the
    left.  If the OK button is chosen, the text in the text entry field
    is returned.   If the Cancel button is chosen, None is returned.
    The OK button is selected by default.

    The left arrow key and right arrow key do not perform the respective
    functions they perform in the regular dialog box.  Instead, they are
    used to navigate the text entry field.

    """
    # TODO


def get_key_pressed(key):
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
    Keypad Enter         ``"kp_enter"``
    Left Arrow           ``"left"``
    Right Arrow          ``"right"``
    Up Arrow             ``"up"``
    Down Arrow           ``"down"``
    Tab                  ``"tab"``               ``"\\t"``
    Space Bar            ``"space"``             ``" "``
    Enter/Return         ``"enter"``             ``"\\n"``
    Backspace            ``"backspace"``         ``"\\b"``
    Delete               ``"delete"``
    Insert               ``"insert"``
    Left Shift           ``"shift_left"``
    Right Shift          ``"shift_right"``
    Left Ctrl            ``"ctrl_left"``
    Right Ctrl           ``"ctrl_right"``
    Left Alt             ``"alt_left"``
    Right Alt            ``"alt_right"``
    Left Super           ``"super_left"``
    Right Super          ``"super_right"``
    Caps Lock            ``"caps_lock"``
    Home                 ``"home"``
    End                  ``"end"``
    Page Up              ``"pageup"``
    Page Down            ``"pagedown"``
    Pause                ``"pause"``
    Break                ``"break"``
    Print Screen         ``"print_screen"``
    SysRq                ``"sysrq"``
    Clear                ``"clear"``
    Menu                 ``"menu"``
    Mode                 ``"mode"``
    Power                ``"power"``
    Scroll Lock          ``"scroll_lock"``
    Esc                  ``"escape"``
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


def get_mouse_button_pressed(button):
    """Return whether or not a mouse button is pressed.

    Arguments:

    - ``button`` -- The identifier string of the mouse button to check;
      see below for a table of the identifier strings.

    ====================== =================
    Mouse Button Name      Identifier String
    ====================== =================
    Left mouse button      ``"left"``
    Right mouse button     ``"right"``
    Middle mouse button    ``"middle"``
    Mouse wheel up         ``"wheel_up"``
    Mouse wheel down       ``"wheel_down"``
    Mouse wheel tilt left  ``"wheel_left"``
    Mouse wheel tilt right ``"wheel_right"``
    ====================== =================

    """
    # TODO


def get_joystick_axis(joystick, axis):
    """Return the position of a joystick axis.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick.
    - ``axis`` -- The number of the axis to check, where ``0`` is the
      first axis of the joystick.

    Return a float from ``-1`` to ``1``, where ``0`` is centered, ``-1``
    is all the way to the left or up, and ``1`` is all the way to the
    right or down.  Return ``0`` if the requested joystick or axis does
    not exist.

    """
    # TODO


def get_joystick_hat(joystick, hat):
    """Return the position of a joystick HAT.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick.
    - ``hat`` -- The number of the HAT to check, where ``0`` is the
      first HAT of the joystick.

    Return a two-part tuple in the form ``(x, y)``.  ``x`` can be ``-1``
    (left), ``0`` (horizontally centered), or ``1`` (right).  ``y`` can
    be ``-1`` (up), ``0`` (vertically centered), or ``1`` (down).
    Return ``(0, 0)`` if the requested joystick or axis does not exist.

    """
    # TODO


def get_joystick_button_pressed(joystick, button):
    """Return whether or not a joystick button is pressed.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick.
    - ``button`` -- The number of the button to check, where ``0`` is
      the first button of the joystick.

    ``joystick`` is the number of the joystick to check, where ``0`` is
    the first joystick.  ``button`` is the number of the button to
    check, where ``0`` is the first button of the joystick.

    Return :const:`False` if the requested joystick or button does not
    exist.

    """
    # TODO


def get_joysticks():
    """Return the number of joysticks available."""
    # TODO


def get_joystick_axes(joystick):
    """Return the number of axes available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick.

    Return ``0`` if the requested joystick does not exist.

    """
    # TODO


def get_joystick_hats(joystick):
    """Return the number of HATs available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick.

    Return ``0`` if the requested joystick does not exist.

    """
    # TODO


def get_joystick_buttons(joystick):
    """Return the number of buttons available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick.

    Return ``0`` if the requested joystick does not exist.

    """
    # TODO
