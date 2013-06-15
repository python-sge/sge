# Stellar Game Engine Template
# Copyright (C) 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


__all__ = ['BackgroundLayer']


class BackgroundLayer(object):

    """Special class used for background layers.

    This class stores a sprite and certain information for a layer of a
    background.  In particular, it stores the location of the layer,
    whether the layer tiles horizontally, vertically, or both, and the
    rate at which it scrolls.

    Attributes:

    - ``sprite`` -- The sprite used for this layer.  It will be animated
      normally if it contains multiple frames.

    - ``x`` -- The horizontal location of the layer relative to the
      background.

    - ``y`` -- The vertical location of the layer relative to the
      background.

    - ``z`` -- The Z-axis position of the layer in the room.

    - ``xscroll_rate`` -- The horizontal rate that the layer scrolls as
      a factor of the additive inverse of the horizontal movement of the
      view.

    - ``yscroll_rate`` -- The vertical rate that the layer scrolls as a
      factor of the additive inverse of the vertical movement of the
      view.

    - ``xrepeat`` -- Whether or not the layer should be repeated (tiled)
      horizontally.

    - ``yrepeat`` -- Whether or not the layer should be repeated (tiled)
      vertically.

    Read-Only Attributes:

    - ``id`` -- The unique identifier of the layer.

    """

    def __init__(self, sprite, x, y, z, id_=None, xscroll_rate=1,
                 yscroll_rate=1, xrepeat=True, yrepeat=True, **kwargs):
        """Create a background layer object.

        Arguments:

        - ``id`` -- The unique identifier of the sprite.  If set to
          None, the ``id`` attribute of the sprite will be used,
          modified by SGE if it is already the unique identifier of
          another background layer.

        All other arguments set the respective initial attributes of the
        layer.  See the documentation for `BackgroundLayer` for more
        information.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        # TODO
