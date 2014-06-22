# The SGE Specification
# Written in 2014 by Julian Marchant <onpon4@riseup.net> 
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

"""
This module provides input event classes.  Input event objects are used
to consolidate all necessary information about input events in a clean
way.

You normally don't need to use input event objects directly.  Input
events are handled automatically in each frame of the SGE's main loop.
You only need to use input event objects directly if you take control
away from the SGE's main loop, e.g. to create your own loop.
"""


__all__ = ["KeyPress", "KeyRelease", "MouseMove", "MouseButtonPress",
           "MouseButtonRelease", "JoystickAxisMove", "JoystickHatMove",
           "JoystickTrackballMove", "JoystickButtonPress",
           "JoystickButtonRelease", "KeyboardFocusGain", "KeyboardFocusLose",
           "MouseFocusGain", "MouseFocusLose", "QuitRequest"]


class KeyPress:

    """Key press input event class.

    This input event represents a key on the keyboard being pressed.

    .. attribute:: key

       The identifier string of the key that was pressed.  See the
       documentation for :func:`sge.keyboard.get_pressed` for more
       information.

    .. attribute:: char

       The Unicode character associated with the key press, or an empty
       Unicode string if no Unicode character is associated with the key
       press.  See the documentation for
       :func:`sge.keyboard.get_pressed` for more information.

    """

    def __init__(self, key, char):
        self.key = key
        self.char = char


class KeyRelease:

    """Key release input event class.

    This input event represents a key on the keyboard being released.

    .. attribute:: key

       The identifier string of the key that was released.  See the
       documentation for :func:`sge.keyboard.get_pressed` for more
       information.

    """

    def __init__(self, key):
        self.key = key


class MouseMove:

    """Mouse move input event class.

    This input event represents the mouse being moved.

    .. attribute:: x

       The horizontal relative movement of the mouse.

    .. attribute:: y

       The vertical relative movement of the mouse.

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class MouseButtonPress:

    """Mouse button press input event class.

    This input event represents a mouse button being pressed.

    .. attribute:: button

       The identifier string of the mouse button that was pressed.  See
       the documentation for :func:`sge.mouse.get_pressed` for more
       information.

    """

    def __init__(self, button):
        self.button = button


class MouseButtonRelease:

    """Mouse button release input event class.

    This input event represents a mouse button being released.

    .. attribute:: button

       The identifier string of the mouse button that was released.  See
       the documentation for :func:`sge.mouse.get_pressed` for more
       information.

    """

    def __init__(self, button):
        self.button = button


class JoystickAxisMove:

    """Joystick axis move input event class.

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
        self.value = value


class JoystickHatMove:

    """Joystick hat move input event class.

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


class JoystickTrackballMove:

    """Joystick trackball move input event class.

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


class JoystickButtonPress:

    """Joystick button press input event class.

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


class JoystickButtonRelease:

    """Joystick button release input event class.

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


class KeyboardFocusGain:

    """Keyboard focus gain input event class.

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


class KeyboardFocusLose:

    """Keyboard focus lose input event class.

    This input event represents the game window losing keyboard focus.
    Keyboard focus is normally needed for keyboard input to be received.

    .. note::

       See the note in the documentation for
       :class:`sge.input.KeyboardFocusGain`.

    """


class MouseFocusGain:

    """Mouse focus gain input event class.

    This input event represents the game window gaining mouse focus.
    Mouse focus is normally needed for mouse input to be received.

    .. note::

       See the note in the documentation for
       :class:`sge.input.KeyboardFocusGain`.

    """


class MouseFocusLose:

    """Mouse focus lose input event class.

    This input event represents the game window losing mouse focus.
    Mouse focus is normally needed for mouse input to be received.

    .. note::

       See the note in the documentation for
       :class:`sge.input.KeyboardFocusGain`.

    """


class QuitRequest:

    """Quit request input event class.

    This input event represents the OS requesting for the program to
    close (e.g. when the user presses a "close" button on the window
    border).

    """
