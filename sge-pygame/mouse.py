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

import pygame

import sge


__all__ = ["get_pressed"]


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
