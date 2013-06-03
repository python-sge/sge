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

    This class stores the layers that make up the background (which
    contain the information about what images to use and where) as well as
    the color to use where no image is shown.

    Attributes:
    * color: The color used in parts of the background where no layer is
      shown.

    Read-Only Attributes:
    * id: The unique identifier for this background.
    * layers: A tuple containing all sge.BackgroundLayer objects used in
      this background.

    """

    def __init__(self, layers, color, id_=None, **kwargs):
        """Create a background with the given color and layers.

        Arguments set the respective initial attributes of the
        background.  See the documentation for sge.Background for more
        information.

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
