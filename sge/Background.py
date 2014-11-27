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

class Background(object):

    """Background class.

    This class stores the layers that make up the background (which
    contain the information about what images to use and where) as well
    as the color to use where no image is shown.

    .. attribute:: layers

       A list containing all :class:`sge.BackgroundLayer` objects used
       in this background.  (Read-only)

    .. attribute:: color

       A :class:`sge.Color` object representing the color used in parts
       of the background where no layer is shown.

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)

    """

    def __init__(self, layers, color):
        """Constructor method.

        Arguments set the respective initial attributes of the
        background.  See the documentation for :class:`sge.Background`
        for more information.

        """
        # TODO
