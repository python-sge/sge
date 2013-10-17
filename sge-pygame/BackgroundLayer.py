# Copyright (C) 2012, 2013 Julian Marchant <onpon4@riseup.net>
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


__all__ = ['BackgroundLayer']


class BackgroundLayer(object):

    """Special class used for background layers.

    This class stores a sprite and certain information for a layer of a
    background.  In particular, it stores the location of the layer,
    whether the layer tiles horizontally, vertically, or both, and the
    rate at which it scrolls.

    .. attribute:: sprite

       The sprite used for this layer.  It will be animated normally if
       it contains multiple frames.

    .. attribute:: x

       The horizontal location of the layer relative to the background.

    .. attribute:: y

       The vertical location of the layer relative to the background.

    .. attribute:: z

       The Z-axis position of the layer in the room.

    .. attribute:: xscroll_rate

       The horizontal rate that the layer scrolls as a factor of the
       additive inverse of the horizontal movement of the view.

    .. attribute:: yscroll_rate

       The vertical rate that the layer scrolls as a factor of the
       additive inverse of the vertical movement of the view.

    .. attribute:: xrepeat

       Whether or not the layer should be repeated (tiled) horizontally.

    .. attribute:: yrepeat

       Whether or not the layer should be repeated (tiled) vertically.

    .. attribute:: id

       The unique identifier of the layer.  (Read-only)

    """

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        if not isinstance(value, sge.Sprite):
            value = sge.game.sprites[value]

        if self._sprite != value:
            self._sprite = value
            sge.game._background_changed = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self._x != value:
            self._x = value
            sge.game._background_changed = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self._y != value:
            self._y = value
            sge.game._background_changed = True

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if self._z != value:
            self._z = value
            sge.game._background_changed = True

    @property
    def xscroll_rate(self):
        return self._xscroll_rate

    @xscroll_rate.setter
    def xscroll_rate(self, value):
        if self._xscroll_rate != value:
            self._xscroll_rate = value
            sge.game._background_changed = True

    @property
    def yscroll_rate(self):
        return self._yscroll_rate

    @yscroll_rate.setter
    def yscroll_rate(self):
        if self._yscroll_rate != value:
            self._yscroll_rate = value
            sge.game._background_changed = True

    @property
    def xrepeat(self):
        return self._xrepeat

    @xrepeat.setter
    def xrepeat(self, value):
        if self._xrepeat != value:
            self._xrepeat = value
            sge.game._background_changed = True

    @property
    def yrepeat(self):
        return self._yrepeat

    @yrepeat.setter
    def yrepeat(self, value):
        if self._yrepeat != value:
            self._yrepeat = value
            sge.game._background_changed = True

    def __init__(self, sprite, x, y, z, ID=None, xscroll_rate=1,
                 yscroll_rate=1, xrepeat=True, yrepeat=True):
        """Constructor method.

        Arguments:

        - ``ID`` -- The value to set :attr:`id` to.  If set to
          :const:`None`, :attr:`sprite.id` will be used, modified by the
          SGE if it is already the unique identifier of another
          background layer.

        All other arguments set the respective initial attributes of the
        layer.  See the documentation for :class:`BackgroundLayer` for
        more information.

        """
        self._sprite = None
        self.sprite = sprite
        self._x = x
        self._y = y
        self._z = z
        self._xscroll_rate = xscroll_rate
        self._yscroll_rate = yscroll_rate
        self._xrepeat = xrepeat
        self._yrepeat = yrepeat

        if ID is not None:
            self.id = ID
        else:
            self.id = self.sprite.id

            while self.id in sge.game.background_layers:
                self.id += "_"

        self._image_index = 0
        self._count = 0
        if self.sprite.fps != 0:
            self._frame_time = 1000 / self.sprite.fps
            if not self._frame_time:
                # This would be caused by a round-off to 0 resulting
                # from a much too high frame rate.  It would cause a
                # division by 0 later, so this is meant to prevent that.
                self._frame_time = 0.01
        else:
            self._frame_time = None

        sge.game.background_layers[self.id] = self

    def _update(self, time_passed):
        # Update the animation frame.
        if self._frame_time is not None:
            self._count += time_passed
            self._image_index += int(self._count // self._frame_time)
            self._count %= self._frame_time
            self._image_index %= len(self.sprite._images)

    def _get_image(self):
        return self.sprite._get_image(self._image_index)
