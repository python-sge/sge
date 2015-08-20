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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sge
from sge.r import v_limit


__all__ = ['View']


class View(object):

    """
    This class controls what the player sees in a room at any given
    time.  Multiple views can exist in a room, and this can be used to
    create a split-screen effect.

    .. attribute:: x

       The horizontal position of the view in the room.  When set, if it
       brings the view outside of the room it is in, it will be
       re-adjusted so that the view is completely inside the room.

    .. attribute:: y

       The vertical position of the view in the room.  When set, if it
       brings the view outside of the room it is in, it will be
       re-adjusted so that the view is completely inside the room.

    .. attribute:: xport

       The horizontal position of the view port on the window.

    .. attribute:: yport

       The vertical position of the view port on the window.

    .. attribute:: width

       The width of the view.  When set, if it results in the view being
       outside of the room it is in, :attr:`x` will be adjusted so that
       the view is completely inside the room.

    .. attribute:: height

       The height of the view.  When set, if it results in the view
       being outside the room it is in, :attr:`y` will be adjusted so
       that the view is completely inside the room.

    .. attribute:: wport

       The width of the view port.  Set to :const:`None` to make it the
       same as :attr:`width`.  If this value differs from :attr:`width`,
       the image will be horizontally scaled so that it fills the port.

    .. attribute:: hport

       The height of the view port.  Set to :const:`None` to make it the
       same as :attr:`height`.  If this value differs from
       :attr:`height`, the image will be vertically scaled so that it
       fills the port.

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def x(self):
        return self.rd["x"]

    @x.setter
    def x(self, value):
        self.rd["x"] = value
        v_limit(self)

    @property
    def y(self):
        return self.rd["y"]

    @y.setter
    def y(self, value):
        self.rd["y"] = value
        v_limit(self)

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value
        v_limit(self)

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value
        v_limit(self)

    @property
    def wport(self):
        return self.__wport if self.__wport is not None else self.width

    @wport.setter
    def wport(self, value):
        self.__wport = value

    @property
    def hport(self):
        return self.__hport if self.__hport is not None else self.height

    @hport.setter
    def hport(self, value):
        self.__hport = value

    def __init__(self, x, y, xport=0, yport=0, width=None, height=None,
                 wport=None, hport=None):
        """
        Arguments:

        - ``width`` -- The width of the view.  If set to :const:`None`,
          it will become ``sge.game.width - xport``.
        - ``height`` -- The height of the view.  If set to
          :const:`None`, it will become ``sge.game.height - yport``.

        All other arugments set the respective initial attributes of the
        view.  See the documentation for :class:`sge.View` for more
        information.
        """
        self.rd = {}
        self.rd["x"] = x
        self.rd["y"] = y
        self.xport = xport
        self.yport = yport
        self.__width = width if width else sge.game.width - xport
        self.__height = height if height else sge.game.height - yport
        v_limit(self)
        self.wport = wport
        self.hport = hport
