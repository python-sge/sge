# Copyright (C) 2012, 2013, 2014, 2015 Julian Marchant <onpon4@riseup.net>
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

    """
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

    .. attribute:: repeat_left

       Whether or not the layer should be repeated (tiled) to the left.

    .. attribute:: repeat_right

       Whether or not the layer should be repeated (tiled) to the right.

    .. attribute:: repeat_up

       Whether or not the layer should be repeated (tiled) upwards.

    .. attribute:: repeat_down

       Whether or not the layer should be repeated (tiled) downwards.

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    def __init__(self, sprite, x, y, z=0, xscroll_rate=1, yscroll_rate=1,
                 repeat_left=False, repeat_right=False, repeat_up=False,
                 repeat_down=False):
        """
        Arguments set the respective initial attributes of the layer.
        See the documentation for :class:`sge.BackgroundLayer` for more
        information.
        """
        self.rd = {}
        self.sprite = sprite
        self.x = x
        self.y = y
        self.z = z
        self.xscroll_rate = xscroll_rate
        self.yscroll_rate = yscroll_rate
        self.repeat_left = repeat_left
        self.repeat_right = repeat_right
        self.repeat_up = repeat_up
        self.repeat_down = repeat_down

        self.rd["fps"] = 0
        self.rd["image_index"] = 0
        self.rd["count"] = 0
        self.rd["frame_time"] = None
