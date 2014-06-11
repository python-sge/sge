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
This module provides functions related to the mouse input.

Many other mouse functionalities are provided through attributes of
:attr:`sge.game.mouse`:

- :attr:`sge.game.mouse.x` and `sge.game.mouse.y` indicate the position
  of the mouse relative to the room.  Set these attributes to change the
  position of the mouse.
- :attr:`sge.game.mouse.xvelocity`, :attr:`sge.game.mouse.yvelocity`,
  :attr:`sge.game.mouse.speed`, and
  :attr:`sge.game.mouse.move_direction` indicate the average movement of
  the mouse during the last 250 milliseconds.
- :attr:`sge.game.mouse.sprite` controls what the mouse cursor looks
  like.  Set to :const:`None` for the default mouse cursor.
- :attr:`sge.game.mouse.visible` controls whether or not the mouse
  cursor is visible.
"""

import pygame

import sge


__all__ = ["get_pressed", "get_x", "get_y"]


def get_pressed(button):
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
    b = {"left": 0, "middle": 1, "right": 2}.setdefault(button.lower())
    if b is not None:
        return pygame.mouse.get_pressed()[b]
    else:
        return False


def get_x():
    """Return the horizontal location of the mouse cursor.

    This function differs from :attr:`sge.game.mouse.x` in that the
    location returned is relative to the window, not the room.

    """
    return pygame.mouse.get_pos()[0]


def get_y():
    """Return the vertical location of the mouse cursor.

    This function differs from :attr:`sge.game.mouse.y` in that the
    location returned is relative to the window, not the room.

    """
    return pygame.mouse.get_pos()[1]
