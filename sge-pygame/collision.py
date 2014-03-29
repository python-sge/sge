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


class _cache:

    rectangle_masks = {}
    ellipse_masks = {}
    circle_masks = {}
    line_masks = {}


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
      documentation for :meth:`sge.StellarClass.collision` for more
      information.

    """
    room = sge.game.current_room
    areas = _get_rectangle_collision_areas(x, y, w, h)
    others = _get_others(areas, other)
    collisions = []
    mask_id = (x, y, w, h)

    if mask_id in _cache.rectangle_masks:
        mask = _cache.rectangle_masks[mask_id]
    else:
        mask = [[True for j in range(h)] for i in range(w)]
        _cache.rectangle_masks[mask_id] = mask

    for other in others:
        if other.collision_precise or other.collision_ellipse:
            if masks_collide(x, y, mask, other.mask_x, other.mask_y,
                             other.mask):
                collisions.append(other)
        else:
            if rectangles_collide(x, y, w, h, other.bbox_left, other.bbox_top,
                                  other.bbox_width, other.bbox_height):
                collisions.append(other)

    return collisions


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
      documentation for :meth:`sge.StellarClass.collision` for more
      information.

    """
    room = sge.game.current_room
    areas = _get_rectangle_collision_areas(x, y, w, h)
    others = _get_others(areas, other)
    collisions = []
    mask_id = (x, y, w, h)

    if mask_id in _cache.ellipse_masks:
        mask = _cache.ellipse_masks[mask_id]
    else:
        mask = [[False for j in range(h)] for i in range(w)]
        a = len(mask) / 2
        b = len(mask[0] / 2 if mask else 0

        for i in range(len(mask)):
            for j in range(len(mask[i])):
                if ((i - a) / a) ** 2 + ((j - b) / b) ** 2 <= 1:
                    mask[i][j] = True

        _cache.ellipse_masks[mask_id] = mask

    for other in others:
        if masks_collide(x, y, mask, other.mask_x, other.mask_y,
                         other.mask):
            collisions.append(other)

    return collisions


def circle(x, y, radius, other=None):
    """Return a list of objects colliding with a circle.

    Arguments:

    - ``x`` -- The horizontal position of the center of the circle.
    - ``y`` -- The vertical position of the center of the circle.
    - ``radius`` -- The radius of the circle.
    - ``other`` -- What to check for collisions with.  See the
      documentation for :meth:`sge.StellarClass.collision` for more
      information.

    """
    room = sge.game.current_room
    diameter = radius * 2
    areas = _get_rectangle_collision_areas(x, y, diameter, diameter)
    others = _get_others(areas, other)
    collisions = []
    mask_id = (x, y, radius)

    if mask_id in _cache.circle_masks:
        mask = _cache.circle_masks[mask_id]
    else:
        mask = [[False for j in range(diameter)] for i in range(diameter)]

        for i in range(len(mask)):
            for j in range(len(mask[i])):
                if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                    mask[i][j] = True

        _cache.circle_masks[mask_id] = mask

    for other in others:
        if masks_collide(x - radius, y - radius, mask, other.mask_x,
                         other.mask_y, other.mask):
            collisions.append(other)

    return collisions


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
      documentation for :meth:`sge.StellarClass.collision` for more
      information.

    """
    room = sge.game.current_room
    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    areas = _get_rectangle_collision_areas(x, y, w, h)
    others = _get_others(areas, other)
    collisions = []
    mask_id = (w, h)

    if mask_id in _cache.line_masks:
        mask = _cache.line_masks[mask_id]
    else:
        mask = [[False for j in range(h)] for i in range(w)]
        m = h / w
        b = y1 - m * x1

        for i in range(len(mask)):
            j = int(round(m * i + b))
            if 0 <= j < len(mask[i]):
                mask[i][j] = True

        _cache.line_masks[mask_id] = mask

    for other in others:
        if masks_collide(x, y, mask, other.mask_x, other.mask_y,
                         other.mask):
            collisions.append(other)

    return collisions


def _get_rectangle_collision_areas(x, y, w, h):
    # Get a list of collision areas a rect is in.
    room = sge.game.current_room
    area_size = room._collision_area_size
    areas_x_start = int(x / area_size)
    areas_x_num = math.ceil(w / area_size) + 1
    areas_y_start = int(y / area_size)
    areas_y_num = math.ceil(h / area_size) + 1
    areas = []

    for i in range(areas_x_start, areas_x_start + areas_x_num):
        for j in range(areas_y_start, areas_y_start + areas_y_num):
            if (i >= 0 and j >= 0 and room._collision_areas and
                    i < len(room._collision_areas) and
                    j < len(room._collision_areas[0])):
                areas.append((i, j))
            elif None not in areas:
                areas.append(None)

    return areas


def _get_others(areas, other=None):
    room = sge.game.current_room
    others = []

    for area in areas:
        if area is not None:
            i, j = area
            room_area = room._collision_areas[i][j]
        else:
            room_area = room._collision_area_void

        for obj in room_area:
            if other is None or other is obj:
                others.append(obj)
            elif isinstance(other, (list, tuple)):
                if obj in other:
                    others.append(obj)
            elif other in sge.game.objects:
                if obj is sge.game.objects[other]:
                    others.append(obj)
            else:
                try:
                    if isinstance(obj, other):
                        others.append(obj)
                except TypeError:
                    other = []

    return others
