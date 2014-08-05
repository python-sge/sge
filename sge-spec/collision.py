# The SGE Specification
# Written in 2014 by Julian Marchant <onpon4@riseup.net> 
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
This module provides easy-to-use collision detection functions, from
basic rectangle-based collision detection to shape-based collision
detection.
"""

__all__ = ["rectangles_collide", "masks_collide", "rectangle", "ellipse",
           "circle", "line"]


def rectangles_collide(x1, y1, w1, h1, x2, y2, w2, h2):
    """Return whether or not two rectangles collide.

    Arguments:

    - ``x1`` -- The horizontal position of the first rectangle.
    - ``y1`` -- The vertical position of the first rectangle.
    - ``w1`` -- The width of the first rectangle.
    - ``h1`` -- The height of the first rectangle.
    - ``x2`` -- The horizontal position of the second rectangle.
    - ``y2`` -- The vertical position of the second rectangle.
    - ``w2`` -- The width of the second rectangle.
    - ``h2`` -- The height of the second rectangle.

    """
    return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)


def masks_collide(x1, y1, mask1, x2, y2, mask2):
    """Return whether or not two masks collide.

    Arguments:

    - ``x1`` -- The horizontal position of the first mask.
    - ``y1`` -- The vertical position of the first mask.
    - ``mask1`` -- The first mask (see below).
    - ``x2`` -- The horizontal position of the second mask.
    - ``y2`` -- The vertical position of the second mask.
    - ``mask2`` -- The second mask (see below).

    ``mask1`` and ``mask2`` are both lists of lists of boolean values.
    Each value in the mask indicates whether or not a pixel is counted
    as a collision; the masks collide if at least one pixel at the same
    location is :const:`True` for both masks.

    Masks are indexed as ``mask[x][y]``, where ``x`` is the column and
    ``y`` is the row.

    """
    if mask1 and mask2 and mask1[0] and mask2[0]:
        x1 = int(round(x1))
        y1 = int(round(y1))
        w1 = len(mask1)
        h1 = len(mask1[0])
        x2 = int(round(x2))
        y2 = int(round(y2))
        w2 = len(mask2)
        h2 = len(mask2[0])

        if rectangles_collide(x1, y1, w1, h1, x2, y2, w2, h2):
            for i in range(max(x1, x2), min(x1 + w1, x2 + w2)):
                for j in range(max(y1, y2), min(y1 + h1, y2 + h2)):
                    if (mask1[i - x1][j - y1] and mask2[i - x2][j - y2]):
                        return True

    return False


def rectangle(x, y, w, h, other=None):
    """Return a list of objects colliding with a rectangle.

    Arguments:

    - ``x`` -- The horizontal position of the rectangle.
    - ``y`` -- The vertical position of the rectangle.
    - ``w`` -- The width of the rectangle.
    - ``h`` -- The height of the rectangle.
    - ``other`` -- What to check for collisions with.  See the
      documentation for :meth:`sge.Object.collision` for more
      information.

    """
    # TODO


def ellipse(x, y, w, h, other=None):
    """Return a list of objects colliding with an ellipse.

    Arguments:

    - ``x`` -- The horizontal position of the imaginary rectangle
      containing the ellipse.
    - ``y`` -- The vertical position of the imaginary rectangle
      containing the ellipse.
    - ``w`` -- The width of the ellipse.
    - ``h`` -- The height of the ellipse.
    - ``other`` -- What to check for collisions with.  See the
      documentation for :meth:`sge.Object.collision` for more
      information.

    """
    # TODO


def circle(x, y, radius, other=None):
    """Return a list of objects colliding with a circle.

    Arguments:

    - ``x`` -- The horizontal position of the center of the circle.
    - ``y`` -- The vertical position of the center of the circle.
    - ``radius`` -- The radius of the circle.
    - ``other`` -- What to check for collisions with.  See the
      documentation for :meth:`sge.Object.collision` for more
      information.

    """
    # TODO


def line(x1, y1, x2, y2, other=None):
    """Return a list of objects colliding with a line segment.

    Arguments:

    - ``x1`` -- The horizontal position of the first endpoint of the
      line segment.
    - ``y1`` -- The vertical position of the first endpoint of the line
      segment.
    - ``x2`` -- The horizontal position of the second endpoint of the
      line segment.
    - ``y2`` -- The vertical position of the second endpoint of the line
      segment.
    - ``other`` -- What to check for collisions with.  See the
      documentation for :meth:`sge.Object.collision` for more
      information.

    """
    # TODO
