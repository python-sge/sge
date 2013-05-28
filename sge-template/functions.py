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

import sge


__all__ = ['show_message', 'get_text_entry', 'get_key_pressed',
           'get_mouse_button_pressed', 'get_joystick_axis', 'get_joystick_hat',
           'get_joystick_button_pressed', 'get_joysticks', 'get_joystick_axes',
           'get_joystick_hats', 'get_joystick_buttons']


def show_message(text, buttons=('OK',), default=0):
    """Show a dialog box and return the button pressed.

    ``text`` indicates the message to show in the dialog box.
    ``buttons`` indicates a list or tuple of strings to put in each of
    the buttons from left to right.  ``default`` indicates the number of
    the button to select by default, where 0 is the first button.

    The dialog box is placed at the center of the window.  The message
    is horizontally aligned to the left and vertically aligned to the
    middle.  All other visual design considerations are left up to the
    implementation.

    While the dialog box is being shown, all events are stopped.  If the
    operating system tells the game to close, the dialog box will close
    immediately, returning None, and leak the command to the rest of the
    game (causing Close events).  If the Esc key is pressed, the dialog
    box will close immediately, returning None.  If the right arrow key
    or Tab key is pressed, a joystick axis is moved from a position less
    than 0.75 to a position greater than or equal to 0.75, a joystick
    HAT is moved to the right, or a joystick trackball is moved to the
    right by at least 0.75, the selection is moved to the right by one;
    if what is currently selected is the last button, the first button
    will be selected.  If the left arrow key is pressed, a joystick axis
    is moved from a position greater than -0.75 to a position less than
    or equal to -0.75, a joystick HAT is moved to the left, or a
    joystick trackball is moved to the left by at least 0.75, the
    selection is moved to the left by one; if what is currently selected
    is the first button, the last button will be selected.  If the Enter
    key, the keypad Enter key, or any joystick button is pressed and
    then released, the dialog box is closed and the number of the of the
    currently selected button is returned, where 0 is the first button.
    If the left mouse button is pressed and then released while the
    mouse is hovering over a button, the dialog box is closed and the
    number of the button the mouse is currently hovering over is
    returned, where 0 is the first button.

    """
    # TODO


def get_text_entry(text, default=''):
    """Show a text entry dialog box and return the text entered.

    ``text`` indicates the message to show in the dialog box.
    ``default`` indicates the text to put in the text entry field
    initially.

    The text entry dialog box is mostly the same as the regular dialog
    box -- see the documentation for sge.show_message for more
    information -- but there are some key differences, outlined below.

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
    """Return whether or not a given key is pressed.

    ``key`` is the key to check.

    """
    # TODO


def get_mouse_button_pressed(button):
    """Return whether or not a given mouse button is pressed.

    ``button`` is the number of the mouse button to check, where 0
    is the first mouse button.

    """
    # TODO


def get_joystick_axis(joystick, axis):
    """Return the position of the given axis.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``axis`` is the number of the axis to
    check, where 0 is the first axis of the joystick.

    Returned value is a float from -1 to 1, where 0 is centered, -1
    is all the way to the left or up, and 1 is all the way to the
    right or down.

    If the joystick or axis requested does not exist, 0 is returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO


def get_joystick_hat(joystick, hat):
    """Return the position of the given HAT.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``hat`` is the number of the HAT to check,
    where 0 is the first HAT of the joystick.

    Returned value is a tuple in the form (x, y), where x is the
    horizontal position and y is the vertical position.  Both x and
    y are 0 (centered), -1 (left or up), or 1 (right or down).

    If the joystick or HAT requested does not exist, (0, 0) is
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO


def get_joystick_button_pressed(joystick, button):
    """Return whether or not the given button is pressed.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``button`` is the number of the button to
    check, where 0 is the first button of the joystick.

    If the joystick or button requested does not exist, False is
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO


def get_joysticks():
    """Return the number of joysticks available.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will always return 0.

    """
    # TODO


def get_joystick_axes(joystick):
    """Return the number of axes available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO


def get_joystick_hats(joystick):
    """Return the number of HATs available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO


def get_joystick_buttons(joystick):
    """Return the number of buttons available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO
