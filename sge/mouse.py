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

   This attribute can be assigned to safely, but doing so will not have
   any effect.

.. attribute:: sge.game.mouse.sprite

   Determines what sprite will be used to represent the mouse cursor.
   Set to :const:`None` for the default mouse cursor.

.. attribute:: sge.game.mouse.visible

   Controls whether or not the mouse cursor is visible.  If this is
   :const:`False` and :attr:`sge.game.grab_input` is :const:`True`, the
   mouse will be in relative mode.  Otherwise, the mouse will be in
   absolute mode.
"""

import sge


__all__ = ["get_pressed", "get_x", "get_y", "set_x", "set_y"]


def get_pressed(button):
    """
    Return whether or not a mouse button is pressed.

    See the documentation for :class:`sge.input.MouseButtonPress` for
    more information.
    """
    # TODO


def get_x():
    """
    Return the horizontal location of the mouse cursor.

    The location returned is relative to the window, excluding any
    scaling, pillarboxes, and letterboxes.  If the mouse is in
    relative mode, this function returns :const:`None`.
    """
    # TODO


def get_y():
    """
    Return the vertical location of the mouse cursor.

    The location returned is relative to the window, excluding any
    scaling, pillarboxes, and letterboxes.  If the mouse is in
    relative mode, this function returns :const:`None`.
    """
    # TODO


def set_x(value):
    """
    Set the horizontal location of the mouse cursor.

    The location returned is relative to the window, excluding any
    scaling, pillarboxes, and letterboxes.  If the mouse is in
    relative mode, this function has no effect.
    """
    # TODO


def set_y(value):
    """
    Set the vertical location of the mouse cursor.

    The location returned is relative to the window, excluding any
    scaling, pillarboxes, and letterboxes.  If the mouse is in
    relative mode, this function has no effect.
    """
    # TODO
