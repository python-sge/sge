# SGE Template
# Written in 2012, 2013 by Julian Marchant <onpon4@lavabit.com> 
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
# Apache License 2.0.

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
