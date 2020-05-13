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

Some other mouse functionalities are provided through attributes of
:attr:`sge.game.mouse`.  These attributes are listed below.

The mouse can be in either absolute or relative mode.  In absolute mode,
the mouse has a position.  In relative mode, the mouse only moves.
Which mode the mouse is in depends on the values of
:attr:`sge.game.grab_input` and :attr:`sge.game.mouse.visible`.

.. attribute:: sge.game.mouse.x
               sge.game.mouse.y

   If the mouse is in absolute mode and within a view port, these
   attributes indicate the
   position of the mouse in the room, based on its proximity to the view
   it is in.  Otherwise, they will return ``-1``.

   These attributes can be assigned to safely, but doing so will not
   have any effect.

.. attribute:: sge.game.mouse.z

   The Z-axis position of the mouse cursor's projection in relation to
   other window projections.  The default value is ``10000``.

.. attribute:: sge.game.mouse.sprite

   Determines what sprite will be used to represent the mouse cursor.
   Set to ``None`` for the default mouse cursor.

.. attribute:: sge.game.mouse.visible

   Controls whether or not the mouse cursor is visible.  If this is
   :const:`False` and :attr:`sge.game.grab_input` is :const:`True`, the
   mouse will be in relative mode.  Otherwise, the mouse will be in
   absolute mode.
"""


__all__ = ["get_pressed", "get_x", "get_y", "set_x", "set_y"]


import pygame

import sge
from sge import r


def get_pressed(button):
    """
    Return whether or not a mouse button is pressed.

    See the documentation for :class:`sge.input.MouseButtonPress` for
    more information.
    """
    b = {"left": 0, "middle": 1, "right": 2}.setdefault(button.lower())
    if b is not None:
        return pygame.mouse.get_pressed()[b]
    else:
        return False


def get_x():
    """
    Return the horizontal location of the mouse cursor.

    The location returned is relative to the window, excluding any
    scaling, pillarboxes, and letterboxes.  If the mouse is in
    relative mode, this function returns ``None``.
    """
    if sge.game.grab_input and not sge.game.mouse.visible:
        return None
    else:
        return (pygame.mouse.get_pos()[0] - r.game_x) / r.game_xscale


def get_y():
    """
    Return the vertical location of the mouse cursor.

    The location returned is relative to the window, excluding any
    scaling, pillarboxes, and letterboxes.  If the mouse is in
    relative mode, this function returns ``None``.
    """
    if sge.game.grab_input and not sge.game.mouse.visible:
        return None
    else:
        return (pygame.mouse.get_pos()[1] - r.game_y) / r.game_yscale


def set_x(value):
    """
    Set the horizontal location of the mouse cursor.

    The location returned is relative to the window, excluding any
    scaling, pillarboxes, and letterboxes.  If the mouse is in
    relative mode, this function has no effect.
    """
    if not sge.game.grab_input or sge.game.mouse.visible:
        pygame.mouse.set_pos(value * r.game_xscale + r.game_x,
                             pygame.mouse.get_pos()[1])


def set_y(value):
    """
    Set the vertical location of the mouse cursor.

    The location returned is relative to the window, excluding any
    scaling, pillarboxes, and letterboxes.  If the mouse is in
    relative mode, this function has no effect.
    """
    if not sge.game.grab_input or sge.game.mouse.visible:
        pygame.mouse.set_pos(pygame.mouse.get_pos()[0],
                             value * r.game_yscale + r.game_y)
