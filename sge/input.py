# Copyright (C) 2014, 2015 Julie Marchant <onpon4@riseup.net>
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
This module provides input event classes.  Input event objects are used
to consolidate all necessary information about input events in a clean
way.

You normally don't need to use input event objects directly.  Input
events are handled automatically in each frame of the SGE's main loop.
You only need to use input event objects directly if you take control
away from the SGE's main loop, e.g. to create your own loop.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


__all__ = ["KeyPress", "KeyRelease", "MouseMove", "MouseButtonPress",
           "MouseButtonRelease", "JoystickAxisMove", "JoystickHatMove",
           "JoystickTrackballMove", "JoystickButtonPress",
           "JoystickButtonRelease", "JoystickEvent", "KeyboardFocusGain",
           "KeyboardFocusLose", "MouseFocusGain", "MouseFocusLose",
           "QuitRequest"]


class KeyPress(object):

    """
    This input event represents a key on the keyboard being pressed.

    .. attribute:: key

       The identifier string of the key that was pressed.  See the
       table in the documentation for :mod:`sge.keyboard`.

    .. attribute:: char

       The unicode string associated with the key press, or an empty
       unicode string if no text is associated with the key press.
       See the table in the documentation for :mod:`sge.keyboard`.
    """

    def __init__(self, key, char):
        self.key = key
        self.char = char


class KeyRelease(object):

    """
    This input event represents a key on the keyboard being released.

    .. attribute:: key

       The identifier string of the key that was released.  See the
       table in the documentation for :class:`sge.input.KeyPress`.
    """

    def __init__(self, key):
        self.key = key


class MouseMove(object):

    """
    This input event represents the mouse being moved.

    .. attribute:: x

       The horizontal relative movement of the mouse.

    .. attribute:: y

       The vertical relative movement of the mouse.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class MouseButtonPress(object):

    """
    This input event represents a mouse button being pressed.

    .. attribute:: button

       The identifier string of the mouse button that was pressed.  See
       the table below.

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

    def __init__(self, button):
        self.button = button


class MouseButtonRelease(object):

    """
    This input event represents a mouse button being released.

    .. attribute:: button

       The identifier string of the mouse button that was released.  See
       the table in the documentation for
       :class:`sge.input.MouseButtonPress`.
    """

    def __init__(self, button):
        self.button = button


class JoystickAxisMove(object):

    """
    This input event represents a joystick axis moving.

    .. attribute:: js_name

       The name of the joystick.

    .. attribute:: js_id

       The number of the joystick, where ``0`` is the first joystick.

    .. attribute:: axis

       The number of the axis that moved, where ``0`` is the first axis
       on the joystick.

    .. attribute:: value

       The tilt of the axis as a float from ``-1`` to ``1``, where ``0``
       is centered, ``-1`` is all the way to the left or up, and ``1``
       is all the way to the right or down.
    """

    def __init__(self, js_name, js_id, axis, value):
        self.js_name = js_name
        self.js_id = js_id
        self.axis = axis
        self.value = max(-1.0, min(value, 1.0))


class JoystickHatMove(object):

    """
    This input event represents a joystick hat moving.

    .. attribute:: js_name

       The name of the joystick.

    .. attribute:: js_id

       The number of the joystick, where ``0`` is the first joystick.

    .. attribute:: hat

       The number of the hat that moved, where ``0`` is the first axis
       on the joystick.

    .. attribute:: x

       The horizontal position of the hat, where ``0`` is centered,
       ``-1`` is left, and ``1`` is right.

    .. attribute:: y

       The vertical position of the hat, where ``0`` is centered, ``-1``
       is up, and ``1`` is down.
    """

    def __init__(self, js_name, js_id, hat, x, y):
        self.js_name = js_name
        self.js_id = js_id
        self.hat = hat
        self.x = x
        self.y = y


class JoystickTrackballMove(object):

    """
    This input event represents a joystick trackball moving.

    .. attribute:: js_name

       The name of the joystick.

    .. attribute:: js_id

       The number of the joystick, where ``0`` is the first joystick.

    .. attribute:: ball

       The number of the trackball that moved, where ``0`` is the first
       trackball on the joystick.

    .. attribute:: x

       The horizontal relative movement of the trackball.

    .. attribute:: y

       The vertical relative movement of the trackball.
    """

    def __init__(self, js_name, js_id, ball, x, y):
        self.js_name = js_name
        self.js_id = js_id
        self.ball = ball
        self.x = x
        self.y = y


class JoystickButtonPress(object):

    """
    This input event represents a joystick button being pressed.

    .. attribute:: js_name

       The name of the joystick.

    .. attribute:: js_id

       The number of the joystick, where ``0`` is the first joystick.

    .. attribute:: button

       The number of the button that was pressed, where ``0`` is the
       first button on the joystick.
    """

    def __init__(self, js_name, js_id, button):
        self.js_name = js_name
        self.js_id = js_id
        self.button = button


class JoystickButtonRelease(object):

    """
    This input event represents a joystick button being released.

    .. attribute:: js_name

       The name of the joystick.

    .. attribute:: js_id

       The number of the joystick, where ``0`` is the first joystick.

    .. attribute:: button

       The number of the button that was released, where ``0`` is the
       first button on the joystick.
    """

    def __init__(self, js_name, js_id, button):
        self.js_name = js_name
        self.js_id = js_id
        self.button = button


class JoystickEvent(object):

    """
    This input event represents the movement of any joystick input.
    This makes it possible to treat all joystick inputs the same way,
    which can be used to simplify things like control customization.

    .. attribute:: js_name

       The name of the joystick.

    .. attribute:: js_id

       The number of the joystick, where ``0`` is the first joystick.

    .. attribute:: input_type

       The type of joystick control that was moved.  Can be one of the
       following:

       - ``"axis-"`` -- The tilt of a joystick axis to the left or up
         changes.
       - ``"axis+"`` -- The tilt of a joystick axis to the right or down
         changes.
       - ``"axis0"`` -- The tilt of a joystick axis changes.
       - ``"hat_left"`` -- Whether or not a joystick hat's position is
         to the left changes.
       - ``"hat_right"`` -- Whether or not a joystick hat's position is
         to the right changes.
       - ``"hat_center_x"`` -- Whether or not a joystick hat is
         horizontally centered changes.
       - ``"hat_up"`` -- Whether or not a joystick hat's position is up
         changes.
       - ``"hat_down"`` -- Whether or not a joystick hat's position is
         down changes.
       - ``"hat_center_y"`` -- Whether or not a joystick hat is
         vertically centered changes.
       - ``"trackball_left"`` -- A joystick trackball is moved left.
       - ``"trackball_right"`` -- A joystick trackball is moved right.
       - ``"trackball_up"`` -- A joystick trackball is moved up.
       - ``"trackball_down"`` -- A joystick trackball is moved down.
       - ``"button"`` -- Whether or not a joystick button is pressed
         changes.

    .. attribute:: input_id

       The number of the joystick control that was moved, where ``0`` is
       the first control of its type on the joystick.

    .. attribute:: value

       The value of the event, which is different depending on the value
       of :attr:`input_type`.  If :attr:`input_type` is
       ``"trackball_left"``, ``"trackball_right"``, ``"trackball_up"``,
       or ``"trackball_down"``, this is the relative movement of the
       trackball in the respective direction.  Otherwise, this is the
       new value of the respective control.  See the documentation for
       :func:`sge.joystick.get_value` for more information.
    """

    def __init__(self, js_name, js_id, input_type, input_id, value):
        self.js_name = js_name
        self.js_id = js_id
        self.input_type = input_type
        self.input_id = input_id
        self.value = value


class KeyboardFocusGain(object):

    """
    This input event represents the game window gaining keyboard focus.
    Keyboard focus is normally needed for keyboard input to be received.

    .. note::

       On some window systems, such as the one used by Windows, no
       distinction is made between keyboard and mouse focus, but on
       some other window systems, such as the X Window System, a
       distinction is made: one window can have keyboard focus while
       another has mouse focus.  Be careful to observe the
       difference; failing to do so may result in annoying bugs,
       and you won't notice these bugs if you are testing on a
       window manager that doesn't recognize the difference.
    """


class KeyboardFocusLose(object):

    """
    This input event represents the game window losing keyboard focus.
    Keyboard focus is normally needed for keyboard input to be received.

    .. note::

       See the note in the documentation for
       :class:`sge.input.KeyboardFocusGain`.
    """


class MouseFocusGain(object):

    """
    This input event represents the game window gaining mouse focus.
    Mouse focus is normally needed for mouse input to be received.

    .. note::

       See the note in the documentation for
       :class:`sge.input.KeyboardFocusGain`.
    """


class MouseFocusLose(object):

    """
    This input event represents the game window losing mouse focus.
    Mouse focus is normally needed for mouse input to be received.

    .. note::

       See the note in the documentation for
       :class:`sge.input.KeyboardFocusGain`.
    """


class QuitRequest(object):

    """
    This input event represents the OS requesting for the program to
    close (e.g. when the user presses a "close" button on the window
    border).
    """
