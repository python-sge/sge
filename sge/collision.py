# Copyright (C) 2014, 2016 Julie Marchant <onpon4@riseup.net>
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

"""
This module provides easy-to-use collision detection functions, from
basic rectangle-based collision detection to shape-based collision
detection.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import math

import six

import sge
from sge import r
from sge.r import s_get_precise_mask


__all__ = ["rectangles_collide", "masks_collide", "rectangle", "ellipse",
           "circle", "line"]


def rectangles_collide(x1, y1, w1, h1, x2, y2, w2, h2):
    """
    Return whether or not two rectangles collide.

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
    """
    Return whether or not two masks collide.

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
            for i in six.moves.range(max(x1, x2), min(x1 + w1, x2 + w2)):
                for j in six.moves.range(max(y1, y2), min(y1 + h1, y2 + h2)):
                    if (mask1[i - x1][j - y1] and mask2[i - x2][j - y2]):
                        return True

    return False


def rectangle(x, y, w, h, other=None):
    """
    Return a list of objects colliding with a rectangle.

    Arguments:

    - ``x`` -- The horizontal position of the rectangle.
    - ``y`` -- The vertical position of the rectangle.
    - ``w`` -- The width of the rectangle.
    - ``h`` -- The height of the rectangle.
    - ``other`` -- What to check for collisions with.  See the
      documentation for :meth:`sge.dsp.Object.collision` for more
      information.
    """
    room = sge.game.current_room
    others = room.get_objects_at(x, y, w, h)
    collisions = []
    mask_id = ("rectangle_masks", x, y, w, h)

    mask = r.cache.get(mask_id)
    if mask is None:
        mask = [[True for j in six.moves.range(int(h))]
                for i in six.moves.range(int(w))]

    r.cache.add(mask_id, mask)

    for obj in others:
        if obj.tangible and r.o_is_other(obj, other):
            if obj.collision_precise or obj.collision_ellipse:
                if masks_collide(x, y, mask, obj.mask_x, obj.mask_y, obj.mask):
                    collisions.append(obj)
            else:
                if rectangles_collide(x, y, w, h, obj.bbox_left, obj.bbox_top,
                                      obj.bbox_width, obj.bbox_height):
                    collisions.append(obj)

    return collisions


def ellipse(x, y, w, h, other=None):
    """
    Return a list of objects colliding with an ellipse.

    Arguments:

    - ``x`` -- The horizontal position of the imaginary rectangle
      containing the ellipse.
    - ``y`` -- The vertical position of the imaginary rectangle
      containing the ellipse.
    - ``w`` -- The width of the ellipse.
    - ``h`` -- The height of the ellipse.
    - ``other`` -- What to check for collisions with.  See the
      documentation for :meth:`sge.dsp.Object.collision` for more
      information.
    """
    room = sge.game.current_room
    others = room.get_objects_at(x, y, w, h)
    collisions = []
    mask_id = ("ellipse_masks", x, y, w, h)

    mask = r.cache.get(mask_id)

    if mask is None:
        mask = [[False for j in six.moves.range(int(h))]
                for i in six.moves.range(int(w))]
        a = len(mask) / 2
        b = len(mask[0]) / 2 if mask else 0

        for i in six.moves.range(len(mask)):
            for j in six.moves.range(len(mask[i])):
                if ((i - a) / a) ** 2 + ((j - b) / b) ** 2 <= 1:
                    mask[i][j] = True

    r.cache.add(mask_id, mask)

    for obj in others:
        if (obj.tangible and r.o_is_other(obj, other) and
                masks_collide(x, y, mask, obj.mask_x, obj.mask_y, obj.mask)):
            collisions.append(obj)

    return collisions


def circle(x, y, radius, other=None):
    """
    Return a list of objects colliding with a circle.

    Arguments:

    - ``x`` -- The horizontal position of the center of the circle.
    - ``y`` -- The vertical position of the center of the circle.
    - ``radius`` -- The radius of the circle.
    - ``other`` -- What to check for collisions with.  See the
      documentation for :meth:`sge.dsp.Object.collision` for more
      information.
    """
    room = sge.game.current_room
    diameter = radius * 2
    others = room.get_objects_at(x - radius, y - radius, diameter, diameter)
    collisions = []
    mask_id = ("circle_masks", x, y, radius)

    mask = r.cache.get(mask_id)

    if mask is None:
        mask = [[False for j in six.moves.range(int(diameter))]
                for i in six.moves.range(int(diameter))]

        for i in six.moves.range(len(mask)):
            for j in six.moves.range(len(mask[i])):
                if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                    mask[i][j] = True

    r.cache.add(mask_id, mask)

    for obj in others:
        if (obj.tangible and r.o_is_other(obj, other) and
                masks_collide(x - radius, y - radius, mask, obj.mask_x,
                              obj.mask_y, obj.mask)):
            collisions.append(obj)

    return collisions


def line(x1, y1, x2, y2, other=None):
    """
    Return a list of objects colliding with a line segment.

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
      documentation for :meth:`sge.dsp.Object.collision` for more
      information.
    """
    room = sge.game.current_room
    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x2 - x1) + 1
    h = abs(y2 - y1) + 1

    if w <= 1 or h <= 1:
        return rectangle(x, y, w, h)

    others = room.get_objects_at(x, y, w, h)
    collisions = []
    mask_id = ("line_masks", x1 - x, y1 - y, x2 - x, y2 - y, w, h)

    mask = r.cache.get(mask_id)

    if mask is None:
        sp = sge.gfx.Sprite(width=w, height=h)
        sp.draw_line(x1 - x, y1 - y, x2 - x, y2 - y, sge.gfx.Color("white"))
        mask = s_get_precise_mask(sp, 0, 1, 1, 0)

    r.cache.add(mask_id, mask)

    for obj in others:
        if (obj.tangible and r.o_is_other(obj, other) and
                masks_collide(x, y, mask, obj.mask_x, obj.mask_y, obj.mask)):
            collisions.append(obj)

    return collisions
