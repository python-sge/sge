# Copyright (C) 2014 Julian Marchant <onpon4@riseup.net>
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

import sge


__all__ = ["rectangles_collide", "masks_collide"]


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
