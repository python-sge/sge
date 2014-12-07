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
# Apache License.

"""
This module provides functions related to keyboard input.
"""

__all__ = ["get_pressed", "get_modifier", "get_focused", "set_repeat",
           "get_repeat_enabled", "get_repeat_interval", "get_repeat_delay"]


def get_pressed(key):
    """
    Return whether or not a key is pressed.

    See the documentation for :class:`sge.input.KeyPress` for more
    information.
    """
    # TODO


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
    # TODO


def get_focused():
    """Return whether or not the game has keyboard focus."""
    # TODO


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
    # TODO


def get_repeat_enabled():
    """
    Return whether or not repetition of key press events is enabled.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.
    """
    # TODO


def get_repeat_interval():
    """
    Return the interval in between each repeated key press event.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.
    """
    # TODO


def get_repeat_delay():
    """
    Return the delay before repeating key press events.

    See the documentation for :func:`sge.keyboard.set_repeat` for more
    information.
    """
    # TODO
