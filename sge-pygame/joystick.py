# Copyright (C) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
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
This module provides functions related to joystick input.
"""

import pygame

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
    joystick = get_id(joystick)

    if (joystick is not None and joystick < len(sge.game._joysticks) and
            axis < sge.game._joysticks[joystick].get_numaxes()):
        return sge.game._joysticks[joystick].get_axis(axis)
    else:
        return 0


def _get_hat(joystick, hat):
    # Return the position of a joystick HAT.
    joystick = get_id(joystick)

    if (joystick is not None and joystick < len(sge.game._joysticks) and
            hat < sge.game._joysticks[joystick].get_numhats()):
        return sge.game._joysticks[joystick].get_hat(hat)
    else:
        return (0, 0)


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
    return _get_hat(joystick, hat)[0]


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
    return _get_hat(joystick, hat)[1]


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
    joystick = get_id(joystick)

    if (joystick is not None and joystick < len(sge.game._joysticks) and
            button < sge.game._joysticks[joystick].get_numbuttons()):
        return sge.game._joysticks[joystick].get_button(button)
    else:
        return False


def get_joysticks():
    """Return the number of joysticks available."""
    return len(sge.game._joysticks)


def get_name(joystick):
    """Return the name of a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return :const:`None` if the requested joystick does not exist.

    """
    if isinstance(joystick, int):
        return sge.game._js_names.setdefault(joystick)
    elif joystick in sge.game._js_names.values():
        return joystick
    else:
        return None


def get_id(joystick):
    """Return the number of a joystick, where ``0`` is the first joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return :const:`None` if the requested joystick does not exist.

    """
    if not isinstance(joystick, int):
        return sge.game._js_ids.setdefault(joystick)
    elif joystick in sge.game._js_ids.values():
        return joystick
    else:
        return None


def get_axes(joystick):
    """Return the number of axes available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return ``0`` if the requested joystick does not exist.

    """
    joystick = get_id(joystick)

    if joystick is not None and joystick < len(sge.game._joysticks):
        return sge.game._joysticks[joystick].get_numaxes()
    else:
        return 0


def get_hats(joystick):
    """Return the number of HATs available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return ``0`` if the requested joystick does not exist.

    """
    joystick = get_id(joystick)

    if joystick is not None and joystick < len(sge.game._joysticks):
        return sge.game._joysticks[joystick].get_numhats()
    else:
        return 0


def get_trackballs(joystick):
    """Return the number of trackballs available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return ``0`` if the requested joystick does not exist.

    """
    joystick = get_id(joystick)

    if joystick is not None and joystick < len(sge.game._joysticks):
        return sge.game._joysticks[joystick].get_numballs()
    else:
        return 0


def get_buttons(joystick):
    """Return the number of buttons available on a joystick.

    Arguments:

    - ``joystick`` -- The number of the joystick to check, where ``0``
      is the first joystick, or the name of the joystick to check.

    Return ``0`` if the requested joystick does not exist.

    """
    joystick = get_id(joystick)

    if joystick is not None and joystick < len(sge.game._joysticks):
        return sge.game._joysticks[joystick].get_numbuttons()
    else:
        return 0
