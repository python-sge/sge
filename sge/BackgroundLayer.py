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
# Apache License 2.0.

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

    """

    def __init__(self, sprite, x, y, z, xscroll_rate=1, yscroll_rate=1,
                 xrepeat=True, yrepeat=True):
        """Constructor method.

        Arguments set the respective initial attributes of the layer.
        See the documentation for :class:`sge.BackgroundLayer` for more
        information.

        """
        # TODO
