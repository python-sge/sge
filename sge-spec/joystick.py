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

"""
This module provides functions related to joystick input.
"""

import sge


__all__ = ["get_axis", "get_hat_x", "get_hat_y", "get_button_pressed",
           "get_joysticks", "get_name", "get_id", "get_axes", "get_hats",
           "get_trackballs", "get_buttons"]


def get_axis(joystick, axis):
    """Return the position of a joystick axis.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.
    - ``axis`` -- The number of the axis to check, where ``0`` is the
      first axis of the joystick.

    Return a float from ``-1`` to ``1``, where ``0`` is centered, ``-1``
    is all the way to the left or up, and ``1`` is all the way to the
    right or down.  Return ``0`` if the requested joystick or axis does
    not exist.

    """
    # TODO


def get_hat_x(joystick, hat):
    """Return the horizontal position of a joystick hat (d-pad).

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.
    - ``hat`` -- The number of the hat to check, where ``0`` is the
      first hat of the joystick.

    Return ``-1`` (left), ``0`` (centered), or ``1`` (right).  Return
    ``0`` if the requested joystick or hat does not exist.

    """
    # TODO


def get_hat_y(joystick, hat):
    """Return the vertical position of a joystick hat (d-pad).

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.
    - ``hat`` -- The number of the hat to check, where ``0`` is the
      first hat of the joystick.

    Return ``-1`` (up), ``0`` (centered), or ``1`` (down).  Return ``0``
    if the requested joystick or hat does not exist.

    """
    # TODO


def get_pressed(joystick, button):
    """Return whether or not a joystick button is pressed.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.
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


def get_name(joystick):
    """Return the name of a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return :const:`None` if the requested joystick does not exist.

    """
    # TODO


def get_id(joystick):
    """Return the number of a joystick, where ``0`` is the first joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return :const:`None` if the requested joystick does not exist.

    """
    # TODO


def get_axes(joystick):
    """Return the number of axes available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return ``0`` if the requested joystick does not exist.

    """
    # TODO


def get_hats(joystick):
    """Return the number of HATs available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return ``0`` if the requested joystick does not exist.

    """
    # TODO


def get_trackballs(joystick):
    """Return the number of trackballs available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return ``0`` if the requested joystick does not exist.

    """
    # TODO


def get_buttons(joystick):
    """Return the number of buttons available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return ``0`` if the requested joystick does not exist.

    """
    # TODO
