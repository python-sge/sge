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


class Background(object):

    """Background class.

    All Background objects have the following attributes:
        x: The horizontal position of the background in the room.
        y: The vertical position of the background in the room.
        color: A Stellar Game Engine color used in parts of the
            background where there is no layer.

    The following read-only attributes are also available:
        id: The unique identifier for this background.
        layers: A tuple containing all BackgroundLayer objects used in
            this background.

    """

    def __init__(self, layers, color, x=0, y=0, id_=None, **kwargs):
        """Create a background with the given color and layers.

        Arguments set the properties of the background.  See
        Background.__doc__ for more information.

        If ``id`` is None, it will be set to an integer not currently
        used as an ID (the exact number chosen is implementation-
        specific and may not necessarily be the same between runs).

        In addition to containing actual BackgroundLayer objects,
        ``layers`` can contain valid names of BackgroundLayer objects'
        sprites.

        A game object must exist before an object of this class is
        created.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        # TODO
