# Copyright (C) 2012, 2013, 2014, 2015 Julian Marchant <onpon4@riseup.net>
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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import traceback
import math
import warnings

import pygame
import six

import sge
from sge import r
from sge.r import (o_update_object_areas, o_update_collision_lists,
                   o_is_other, o_get_origin_offset, o_set_speed, s_get_image,
                   s_get_precise_mask)


__all__ = ['Object', 'Mouse']


class Object(object):

    """
    This class is used for game objects, such as the player, enemies,
    bullets, and the HUD.  Generally, each type of object has its own
    subclass of :class:`sge.Object`.

    .. attribute:: x

       The horizontal position of the object in the room.

    .. attribute:: y

       The vertical position of the object in the room.

    .. attribute:: z

       The Z-axis position of the object in the room.

    .. attribute:: sprite

       The sprite currently in use by this object.  Set to :const:`None`
       for no sprite.

    .. attribute:: visible

       Whether or not the object's sprite should be projected onto the
       screen.

    .. attribute:: active

       Indicates whether the object is active (:const:`True`) or
       inactive (:const:`False`).  While the object is active, it will
       exhibit normal behavior; events will be executed normally as will
       any other automatic functionality, such as adding
       :attr:`xvelocity` and :attr:`yvelocity`
       to :attr:`x` and :attr:`y`.  If :attr:`active` is :const:`False`,
       automatic functionality and normal events will be disabled.

       .. note::

          Inactive :class:`sge.Object` objects are still visible
          by default and continue to be involved in collisions.  In
          addition, collision events and destroy events still occur even
          if the object is inactive.  If you wish for the object to not
          be visible, set :attr:`visible` to :const:`False`.  If you
          wish for the object to not perform collision events, set
          :attr:`checks_collisions` to :const:`False`.

    .. attribute:: checks_collisions

       Whether or not the object should check for collisions
       automatically and cause collision events.  If an object is not
       using collision events, setting this to :const:`False` will give
       a boost in performance.

       .. note::

          This will not prevent automatic collision detection by other
          objects from detecting this object, and it will also not
          prevent this object's collision events from being executed.
          If you wish to disable collision detection entirely, set
          :attr:`tangible` to :const:`False`.

    .. attribute:: tangible

       Whether or not collisions involving the object can be detected.
       Setting this to :const:`False` can improve performance if the
       object doesn't need to be involved in collisions.

       Depending on the game, a useful strategy to boost performance can
       be to exclude an object from collision detection while it is
       outside the view.  If you do this, you likely want to set
       :attr:`active` to :const:`False` as well so that the object
       doesn't move in undesireable ways (e.g. through walls).

       .. note::

          If this is :const:`False`, :attr:`checks_collisions` is
          implied to be :const:`False` as well regardless of its actual
          value.  This is because checking for collisions which can't be
          detected is meaningless.

    .. attribute:: bbox_x

       The horizontal location of the bounding box relative to the
       object's position.  If set to :const:`None`, the value
       recommended by the sprite is used.

    .. attribute:: bbox_y

       The vertical location of the bounding box relative to the
       object's position.  If set to :const:`None`, the value
       recommended by the sprite is used.

    .. attribute:: bbox_width

       The width of the bounding box in pixels.  If set to
       :const:`None`, the value recommended by the sprite is used.

    .. attribute:: bbox_height

       The height of the bounding box in pixels.  If set to
       :const:`None`, the value recommended by the sprite is used.

    .. attribute:: regulate_origin

       If set to :const:`True`, the origin is automatically adjusted to
       be the location of the pixel recommended by the sprite after
       transformation.  This will cause rotation to be about the origin
       rather than being about the center of the image.

       .. note::

          The value of this attribute has no effect on the bounding box.
          If you wish for the bounding box to be adjusted as well, you
          must do so manually.  As an alternative, you may want to
          consider using precise collision detection instead.

    .. attribute:: collision_ellipse

       Whether or not an ellipse (rather than a rectangle) should be
       used for collision detection.

    .. attribute:: collision_precise

       Whether or not precise (pixel-perfect) collision detection should
       be used.  Note that this can be inefficient and does not work
       well with animated sprites.

    .. attribute:: bbox_left

       The position of the left side of the bounding box in the room
       (same as :attr:`x` + :attr:`bbox_x`).

    .. attribute:: bbox_right

       The position of the right side of the bounding box in the room
       (same as :attr:`bbox_left` + :attr:`bbox_width`).

    .. attribute:: bbox_top

       The position of the top side of the bounding box in the room
       (same as :attr:`y` + :attr:`bbox_y`).

    .. attribute:: bbox_bottom

       The position of the bottom side of the bounding box in the room
       (same as :attr:`bbox_top` + :attr:`bbox_height`).

    .. attribute:: xvelocity

       The velocity of the object toward the right in pixels per frame.

    .. attribute:: yvelocity

       The velocity of the object toward the bottom in pixels per frame.

    .. attribute:: speed

       The total (directional) speed of the object in pixels per frame.

    .. attribute:: move_direction

       The direction of the object's movement in degrees, with ``0``
       being directly to the right and rotation in a positive direction
       being counter-clockwise.

    .. attribute:: xacceleration

       The acceleration of the object to the right in pixels per frame.
       If non-zero, movement as a result of :attr:`xvelocity` will be
       adjusted based on the kinematic equation,
       ``v[f]^2 = v[i]^2 + 2*a*d``.

    .. attribute:: yacceleration

       The acceleration of the object downward in pixels per frame.  If
       non-zero, movement as a result of :attr:`yvelocity` will be
       adjusted based on the kinematic equation,
       ``v[f]^2 = v[i]^2 + 2*a*d``.

    .. attribute:: xdeceleration

       Like :attr:`xacceleration`, but its sign is ignored and it always
       causes the absolute value of :attr:`xvelocity` to decrease.

    .. attribute:: ydeceleration

       Like :attr:`yacceleration`, but its sign is ignored and it always
       causes the absolute value of :attr:`yvelocity` to decrease.

    .. attribute:: image_index

       The animation frame currently being displayed, with ``0`` being
       the first one.

    .. attribute:: image_origin_x

       The horizontal location of the origin relative to the left edge
       of the images.  If set to :const:`None`, the value recommended by
       the sprite is used.

    .. attribute:: image_origin_y

       The vertical location of the origin relative to the top edge of
       the images.  If set to :const:`None`, the value recommended by
       the sprite is used.

    .. attribute:: image_fps

       The animation rate in frames per second.  Can be negative, in
       which case animation will be reversed.  If set to :const:`None`,
       the value recommended by the sprite is used.

    .. attribute:: image_speed

       The animation rate as a factor of :attr:`sge.game.fps`.  Can be
       negative, in which case animation will be reversed.  If set to
       :const:`None`, the value recommended by the sprite is used.

    .. attribute:: image_xscale

       The horizontal scale factor for the sprite.

    .. attribute:: image_yscale

       The vertical scale factor for the sprite.

    .. attribute:: image_rotation

       The rotation of the sprite in degrees, with rotation in a
       positive direction being counter-clockwise.

       If :attr:`regulate_origin` is :const:`True`, the image is rotated
       about the origin.  Otherwise, the image is rotated about its
       center.

    .. attribute:: image_alpha

       The alpha value applied to the entire image, where ``255`` is the
       original image, ``128`` is half the opacity of the original
       image, ``0`` is fully transparent, etc.

    .. attribute:: image_blend

       A :class:`sge.Color` object representing the color to blend with
       the sprite.  Set to :const:`None` for no color blending.

    .. attribute:: alarms

       A dictionary containing the alarms of the object.  Each value
       decreases by 1 each frame (adjusted for delta timing if it is
       enabled).  When a value is at or below 0,
       :meth:`sge.Object.event_alarm` is executed with ``alarm_id`` set
       to the respective key, and the item is deleted from this
       dictionary.

    .. attribute:: mask

       The current mask used for non-rectangular collision detection.
       See the documentation for :func:`sge.collision.masks_collide` for
       more information.  (Read-only)

    .. attribute:: xstart

       The initial value of :attr:`x` when the object was created.
       (Read-only)

    .. attribute:: ystart

       The initial value of :attr:`y` when the object was created.
       (Read-only)

    .. attribute:: xprevious

       The value of :attr:`x` at the end of the previous frame.
       (Read-only)

    .. attribute:: yprevious

       The value of :attr:`y` at the end of the previous frame.
       (Read-only)

    .. attribute:: mask_x

       The horizontal location of the mask in the room.  (Read-only)

    .. attribute:: mask_y

       The vertical location of the mask in the room.  (Read-only)

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if self.__x != value:
            self.__x = value
            o_update_object_areas(self)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if self.__y != value:
            self.__y = value
            o_update_object_areas(self)

    @property
    def sprite(self):
        return self.rd["sprite"]

    @sprite.setter
    def sprite(self, value):
        if self.rd["sprite"] != value:
            self.rd["sprite"] = value
            if value is not None:
                self.image_index = self.image_index % value.frames
            o_update_object_areas(self)

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        if self.__active != value:
            self.__active = value
            if value:
                r._active_objects.add(self)
            else:
                r._active_objects.discard(self)

    @property
    def checks_collisions(self):
        return self.__checks_collisions

    @checks_collisions.setter
    def checks_collisions(self, value):
        if self.__checks_collisions != value:
            self.__checks_collisions = value
            o_update_collision_lists(self)

    @property
    def tangible(self):
        return self.rd["tangible"]

    @tangible.setter
    def tangible(self, value):
        if self.rd["tangible"] != value:
            self.rd["tangible"] = value
            o_update_collision_lists(self)

    @property
    def bbox_x(self):
        return self.__bbox_x

    @bbox_x.setter
    def bbox_x(self, value):
        if self.__bbox_x != value:
            if value is not None:
                self.__bbox_x = value
            else:
                if self.sprite is not None:
                    self.__bbox_x = self.sprite.bbox_x
                else:
                    self.__bbox_x = 0
            o_update_object_areas(self)

    @property
    def bbox_y(self):
        return self.__bbox_y

    @bbox_y.setter
    def bbox_y(self, value):
        if self.__bbox_y != value:
            if value is not None:
                self.__bbox_y = value
            else:
                if self.sprite is not None:
                    self.__bbox_y = self.sprite.bbox_y
                else:
                    self.__bbox_y = 0
            o_update_object_areas(self)

    @property
    def bbox_width(self):
        return self.__bbox_width

    @bbox_width.setter
    def bbox_width(self, value):
        if self.__bbox_width != value:
            if value is not None:
                self.__bbox_width = value
            else:
                if self.sprite is not None:
                    self.__bbox_width = self.sprite.bbox_width
                else:
                    self.__bbox_width = 1
            o_update_object_areas(self)

    @property
    def bbox_height(self):
        return self.__bbox_height

    @bbox_height.setter
    def bbox_height(self, value):
        if self.__bbox_height != value:
            if value is not None:
                self.__bbox_height = value
            else:
                if self.sprite is not None:
                    self.__bbox_height = self.sprite.bbox_height
                else:
                    self.__bbox_height = 1
            o_update_object_areas(self)

    @property
    def bbox_left(self):
        return self.x + self.bbox_x

    @bbox_left.setter
    def bbox_left(self, value):
        self.x = value - self.bbox_x

    @property
    def bbox_right(self):
        return self.x + self.bbox_x + self.bbox_width

    @bbox_right.setter
    def bbox_right(self, value):
        self.x = value - self.bbox_width - self.bbox_x

    @property
    def bbox_top(self):
        return self.y + self.bbox_y

    @bbox_top.setter
    def bbox_top(self, value):
        self.y = value - self.bbox_y

    @property
    def bbox_bottom(self):
        return self.y + self.bbox_y + self.bbox_height

    @bbox_bottom.setter
    def bbox_bottom(self, value):
        self.y = value - self.bbox_height - self.bbox_y

    @property
    def xvelocity(self):
        return self.rd["xv"]

    @xvelocity.setter
    def xvelocity(self, value):
        if self.rd["xv"] != value:
            self.rd["xv"] = value
            o_set_speed(self)

    @property
    def yvelocity(self):
        return self.rd["yv"]

    @yvelocity.setter
    def yvelocity(self, value):
        if self.rd["yv"] != value:
            self.rd["yv"] = value
            o_set_speed(self)

    @property
    def speed(self):
        return self.rd["speed"]

    @speed.setter
    def speed(self, value):
        if self.rd["speed"] != value:
            self.rd["speed"] = value
            self.rd["xv"] = math.cos(math.radians(self.rd["mv_dir"])) * value
            self.rd["yv"] = -math.sin(math.radians(self.rd["mv_dir"])) * value

    @property
    def move_direction(self):
        return self.rd["mv_dir"]

    @move_direction.setter
    def move_direction(self, value):
        if self.rd["mv_dir"] != value:
            self.rd["mv_dir"] = value
            self.rd["xv"] = math.cos(math.radians(value)) * self.rd["speed"]
            self.rd["yv"] = -math.sin(math.radians(value)) * self.rd["speed"]

    @property
    def image_origin_x(self):
        if self.regulate_origin and self.sprite is not None:
            id_ = (self.sprite.width, self.sprite.height, self.sprite.origin_x,
                   self.sprite.origin_y, self.image_xscale, self.image_yscale,
                   self.image_rotation)

            if id_ not in self.__origins_x:
                x_offset, y_offset = o_get_origin_offset(self)
                self.__origins_x[id_] = self.sprite.origin_x + x_offset
                self.__origins_y[id_] = self.sprite.origin_y + y_offset

            self.__image_origin_x = self.__origins_x[id_]

        if self.__image_origin_x is None:
            return self.sprite.origin_x if self.sprite is not None else 0
        else:
            return self.__image_origin_x

    @image_origin_x.setter
    def image_origin_x(self, value):
        self.__image_origin_x = value

    @property
    def image_origin_y(self):
        if self.regulate_origin and self.sprite is not None:
            id_ = (self.sprite.width, self.sprite.height, self.sprite.origin_x,
                   self.sprite.origin_y, self.image_xscale, self.image_yscale,
                   self.image_rotation)

            if id_ not in self.__origins_y:
                x_offset, y_offset = o_get_origin_offset(self)
                self.__origins_x[id_] = self.sprite.origin_x + x_offset
                self.__origins_y[id_] = self.sprite.origin_y + y_offset

            self.__image_origin_y = self.__origins_y[id_]

        if self.__image_origin_y is None:
            return self.sprite.origin_y if self.sprite is not None else 0
        else:
            return self.__image_origin_y

    @image_origin_y.setter
    def image_origin_y(self, value):
        self.__image_origin_y = value

    @property
    def image_fps(self):
        return self.__fps

    @image_fps.setter
    def image_fps(self, value):
        if value is None:
            value = self.sprite.fps if self.sprite is not None else 0

        self.__fps = value
        if value:
            self.rd["frame_time"] = 1000 / value
            if not self.rd["frame_time"]:
                # This would be caused by a round-off to 0 resulting
                # from a much too high frame rate.  It would cause a
                # division by 0 later, so this is meant to prevent that.
                self.rd["frame_time"] = 0.000001
                w = "Could not calculate timing for {:.2e} FPS.".format(
                    value)
                warnings.warn(w)
        else:
            self.rd["frame_time"] = None

    @property
    def image_speed(self):
        return self.image_fps / sge.game.fps

    @image_speed.setter
    def image_speed(self, value):
        if value is None:
            value = self.sprite.speed if self.sprite is not None else 0

        self.image_fps = value * sge.game.fps

    @property
    def image_blend(self):
        return self.__image_blend

    @image_blend.setter
    def image_blend(self, value):
        if value is None or isinstance(value, sge.Color):
            self.__image_blend = value
        else:
            e = "`{}` is not a sge.Color object.".format(repr(value))
            raise TypeError(e)

    @property
    def mask(self):
        if self.collision_precise:
            return s_get_precise_mask(
                self.sprite, self.image_index, self.image_xscale,
                self.image_yscale, self.image_rotation)
        else:
            id_ = (self.collision_ellipse, self.bbox_x, self.bbox_y,
                   self.bbox_width, self.bbox_height, self.image_xscale,
                   self.image_yscale)

            if id_ in self.__masks:
                return self.__masks[id_]
            else:
                if self.collision_precise:
                    # Mask based on opacity of the current image.
                    mask = s_get_precise_mask(
                        self.sprite, self.image_index, self.image_xscale,
                        self.image_yscale, self.image_rotation)
                elif self.collision_ellipse:
                    # Elliptical mask based on bounding box.
                    mask = [[False for y in six.moves.range(self.bbox_height)]
                            for x in six.moves.range(self.bbox_width)]
                    a = len(mask) / 2
                    b = len(mask[0]) / 2 if mask else 0

                    for x in six.moves.range(len(mask)):
                        for y in six.moves.range(len(mask[x])):
                            if ((x - a) / a) ** 2 + ((y - b) / b) ** 2 <= 1:
                                mask[x][y] = True
                else:
                    # Mask is all pixels in the bounding box.
                    mask = [[True for y in six.moves.range(self.bbox_height)]
                            for x in six.moves.range(self.bbox_width)]

                self.__masks[id_] = mask
                return mask

    @property
    def mask_x(self):
        if self.collision_precise:
            if self.image_rotation % 180:
                origin_x = self.image_origin_x
                i = ("o_mask_x_offset", self, self.sprite, origin_x,
                     self.image_origin_y, self.image_xscale, self.image_yscale,
                     self.image_rotation)
                offset = r.cache.get(i)
                if offset is None:
                    width = s_get_image(self.sprite, self.image_index,
                                        self.image_xscale, self.image_yscale,
                                        self.image_rotation).get_width()
                    normal_width = s_get_image(self.sprite, self.image_index,
                                               self.image_xscale,
                                               self.image_yscale).get_width()
                    offset = (width - normal_width) / 2

                r.cache.add(i, offset)
                return self.x - (origin_x + offset)
            else:
                return self.x - self.image_origin_x
        else:
            return self.bbox_left

    @property
    def mask_y(self):
        if self.collision_precise:
            if self.image_rotation % 180:
                origin_y = self.image_origin_y
                i = ("o_mask_y_offset", self, self.sprite, self.image_origin_x,
                     origin_y, self.image_xscale, self.image_yscale,
                     self.image_rotation)
                offset = r.cache.get(i)
                if offset is None:
                    height = s_get_image(self.sprite, self.image_index,
                                         self.image_xscale, self.image_yscale,
                                         self.image_rotation).get_height()
                    normal_height = s_get_image(self.sprite, self.image_index,
                                                self.image_xscale,
                                                self.image_yscale).get_height()
                    offset = (height - normal_height) / 2

                r.cache.add(i, offset)
                return self.y - (origin_y + offset)
            else:
                return self.y - self.image_origin_y
        else:
            return self.bbox_top

    def __init__(self, x, y, z=0, sprite=None, visible=True, active=True,
                 checks_collisions=True, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 xacceleration=0, yacceleration=0, xdeceleration=0,
                 ydeceleration=0, image_index=0, image_origin_x=None,
                 image_origin_y=None, image_fps=None, image_xscale=1,
                 image_yscale=1, image_rotation=0, image_alpha=255,
                 image_blend=None):
        """
        Arugments set the respective initial attributes of the object.
        See the documentation for :class:`sge.Object` for more
        information.
        """
        self.rd = {}
        self.__x = x
        self.__y = y
        self.z = z
        self.__active = active
        self.__checks_collisions = checks_collisions
        self.rd["tangible"] = tangible
        self.regulate_origin = regulate_origin
        self.collision_ellipse = collision_ellipse
        self.collision_precise = collision_precise
        self.rd["xv"] = xvelocity
        self.rd["yv"] = yvelocity
        self.rd["mv_dir"] = 0
        self.rd["speed"] = 0
        self.xacceleration = xacceleration
        self.yacceleration = yacceleration
        self.xdeceleration = xdeceleration
        self.ydeceleration = ydeceleration
        self.image_index = image_index
        self.image_origin_x = image_origin_x
        self.image_origin_y = image_origin_y
        self.image_xscale = image_xscale
        self.image_yscale = image_yscale
        self.image_rotation = image_rotation
        self.image_alpha = image_alpha
        self.image_blend = image_blend
        self.alarms = {}
        self.xstart = x
        self.ystart = y
        self.xprevious = x
        self.yprevious = y
        self.rd["anim_count"] = 0
        self.__origins_x = {}
        self.__origins_y = {}
        self.rd["object_areas"] = set()
        self.rd["colliders"] = []
        self.__masks = {}

        self.rd["sprite"] = sprite
        if sprite is not None:
            self.image_index = self.image_index % sprite.frames
            sprite_bbox_x = self.sprite.bbox_x
            sprite_bbox_y = self.sprite.bbox_y
            sprite_bbox_width = self.sprite.bbox_width
            sprite_bbox_height = self.sprite.bbox_height
        else:
            sprite_bbox_x = 0
            sprite_bbox_y = 0
            sprite_bbox_width = 1
            sprite_bbox_height = 1
        self.__bbox_x = bbox_x if bbox_x is not None else sprite_bbox_x
        self.__bbox_y = bbox_y if bbox_y is not None else sprite_bbox_y
        self.__bbox_width = (bbox_width if bbox_width is not None else
                             sprite_bbox_width)
        self.__bbox_height = (bbox_height if bbox_height is not None else
                              sprite_bbox_height)

        self.visible = visible
        self.image_fps = image_fps

        o_set_speed(self)

    def move_x(self, move):
        """
        Move the object horizontally.  This method can be overridden to
        conveniently define a particular way movement should be handled.
        Currently, it is used in the default implementation of
        :meth:`event_update_position`.

        Arguments:

        - ``move`` -- The amount to add to :attr:`x`.

        The default behavior of this method is the following code::

            self.x += move
        """
        self.x += move

    def move_y(self, move):
        """
        Move the object vertically.  This method can be overridden to
        conveniently define a particular way movement should be handled.
        Currently, it is used in the default implementation of
        :meth:`event_update_position`.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.

        The default behavior of this method is the following code::

            self.y += move
        """
        self.y += move

    def collision(self, other=None, x=None, y=None):
        """
        Return a list of objects colliding with this object.

        Arguments:

        - ``other`` -- What to check for collisions with.  Can be one of
          the following:

          - A :class:`sge.Object` object.
          - A list of :class:`sge.Object` objects.
          - A class derived from :class:`sge.Object`.
          - :const:`None`: Check for collisions with all objects.

        - ``x`` -- The horizontal position to pretend this object is at
          for the purpose of the collision detection.  If set to
          :const:`None`, :attr:`x` will be used.
        - ``y`` -- The vertical position to pretend this object is at
          for the purpose of the collision detection.  If set to
          :const:`None`, :attr:`y` will be used.
        """
        room = sge.game.current_room
        if self.tangible and self in room.objects:
            collisions = []

            # Change x and y to be offset values; these are easier to use.
            if x is not None:
                x -= self.x
            else:
                x = 0

            if y is not None:
                y -= self.y
            else:
                y = 0

            if self.collision_precise:
                ax = self.mask_x + x
                ay = self.mask_y + y
                w = len(self.mask)
                h = len(self.mask[0]) if self.mask else 0
            else:
                ax = self.bbox_left + x
                ay = self.bbox_top + y
                w = self.bbox_width
                h = self.bbox_height

            others = room.get_objects_at(ax, ay, w, h)

            for obj in others:
                if obj is not self and obj.tangible and o_is_other(obj, other):
                    if (self.collision_precise or self.collision_ellipse or
                            obj.collision_precise or obj.collision_ellipse):
                        # Use masks.
                        if sge.collision.masks_collide(
                                self.mask_x + x, self.mask_y + y, self.mask,
                                obj.mask_x, obj.mask_y, obj.mask):
                            collisions.append(obj)
                    else:
                        # Use bounding boxes.
                        if sge.collision.rectangles_collide(
                                self.bbox_left + x, self.bbox_top + y,
                                self.bbox_width, self.bbox_height,
                                obj.bbox_left, obj.bbox_top, obj.bbox_width,
                                obj.bbox_height):
                            collisions.append(obj)

            return collisions
        else:
            return []

    def destroy(self):
        """
        Remove the object from the current room.  ``foo.destroy()`` is
        identical to ``sge.game.current_room.remove(foo)``.
        """
        sge.game.current_room.remove(self)

    def event_create(self):
        """
        Called in the following cases:

        - Right after the object is added to the current room.
        - Right after a room starts for the first time after the object
          was added to it, if and only if the object was added to the
          room while it was not the current room.  In this case, this
          event is called for each appropriate object after the
          respective room start event or room resume event, in the same
          order that the objects were added to the room.
        """
        pass

    def event_destroy(self):
        """
        Called right after the object is removed from the current room.

        .. note::

           If the object is removed from a room while it is not the
           current room, this method will not be called.
        """
        pass

    def event_begin_step(self, time_passed, delta_mult):
        """
        Called each frame before automatic updates to objects (such as
        the effects of the speed variables).

        See the documentation for :meth:`sge.Game.event_step` for more
        information.
        """
        pass

    def event_step(self, time_passed, delta_mult):
        """
        Called each frame after automatic updates to objects (such as
        the effects of the speed variables), but before collision
        events.

        See the documentation for :meth:`sge.Game.event_step` for more
        information.
        """
        pass

    def event_end_step(self, time_passed, delta_mult):
        """
        Called each frame after collision events.

        See the documentation for :meth:`sge.Game.event_step` for more
        information.
        """
        pass

    def event_alarm(self, alarm_id):
        """
        See the documentation for :attr:`sge.Object.alarms` for more
        information.
        """
        pass

    def event_animation_end(self):
        """Called when an animation cycle ends."""
        pass

    def event_key_press(self, key, char):
        """
        See the documentation for :class:`sge.input.KeyPress` for more
        information.
        """
        pass

    def event_key_release(self, key):
        """
        See the documentation for :class:`sge.input.KeyRelease` for more
        information.
        """
        pass

    def event_mouse_move(self, x, y):
        """
        See the documentation for :class:`sge.input.MouseMove` for more
        information.
        """
        pass

    def event_mouse_button_press(self, button):
        """
        See the documentation for :class:`sge.input.MouseButtonPress`
        for more information.
        """
        pass

    def event_mouse_button_release(self, button):
        """
        See the documentation for :class:`sge.input.MouseButtonRelease`
        for more information.
        """
        pass

    def event_joystick_axis_move(self, js_name, js_id, axis, value):
        """
        See the documentation for :class:`sge.input.JoystickAxisMove`
        for more information.
        """
        pass

    def event_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """
        See the documentation for :class:`sge.input.JoystickHatMove` for
        more information.
        """
        pass

    def event_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """
        See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.
        """
        pass

    def event_joystick_button_press(self, js_name, js_id, button):
        """
        See the documentation for :class:`sge.input.JoystickButtonPress`
        for more information.
        """
        pass

    def event_joystick_button_release(self, js_name, js_id, button):
        """
        See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.
        """
        pass

    def event_update_position(self, delta_mult):
        """
        Called when it's time to update the position of the object.
        This method handles this functionality, so defining this will
        override the default behavior and allow you to handle the speed
        variables in a special way.

        The default behavior of this method is the following code::

            if delta_mult:
                vi = self.xvelocity
                vf = vi + self.xacceleration * delta_mult
                dc = abs(self.xdeceleration) * delta_mult
                if abs(vf) > dc:
                    vf -= math.copysign(dc, vf)
                else:
                    vf = 0
                self.xvelocity = vf
                self.move_x(((vi + vf) / 2) * delta_mult)

                vi = self.yvelocity
                vf = vi + self.yacceleration * delta_mult
                dc = abs(self.ydeceleration) * delta_mult
                if abs(vf) > dc:
                    vf -= math.copysign(dc, vf)
                else:
                    vf = 0
                self.yvelocity = vf
                self.move_y(((vi + vf) / 2) * delta_mult)

        See the documentation for :meth:`sge.Game.event_step` for more
        information.
        """
        if delta_mult:
            vi = self.xvelocity
            vf = vi + self.xacceleration * delta_mult
            dc = abs(self.xdeceleration) * delta_mult
            if abs(vf) > dc:
                vf -= math.copysign(dc, vf)
            else:
                vf = 0
            self.xvelocity = vf
            self.move_x(((vi + vf) / 2) * delta_mult)

            vi = self.yvelocity
            vf = vi + self.yacceleration * delta_mult
            dc = abs(self.ydeceleration) * delta_mult
            if abs(vf) > dc:
                vf -= math.copysign(dc, vf)
            else:
                vf = 0
            self.yvelocity = vf
            self.move_y(((vi + vf) / 2) * delta_mult)

    def event_collision(self, other, xdirection, ydirection):
        """
        Called when this object collides with another object.

        Arguments:

        - ``other`` -- The other object which was collided with.
        - ``xdirection`` -- The horizontal direction of the collision
          from the perspective of this object.  Can be ``-1`` (left),
          ``1`` (right), or ``0`` (no horizontal direction).
        - ``ydirection`` -- The vertical direction of the collision from
          the perspective of this object.  Can be ``-1`` (up), ``1``
          (down), or ``0`` (no vertical direction).

        Directionless "collisions" (ones with both an xdirection and
        ydirection of ``0``) are possible.  These are typically
        collisions which were already occurring in the previous frame
        (continuous collisions).
        """
        pass

    def event_paused_step(self, time_passed, delta_mult):
        """
        See the documentation for :meth:`sge.Game.event_step` for more
        information.
        """
        pass

    def event_paused_key_press(self, key, char):
        """
        See the documentation for :class:`sge.input.KeyPress` for more
        information.
        """
        pass

    def event_paused_key_release(self, key):
        """
        See the documentation for :class:`sge.input.KeyRelease` for more
        information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """
        See the documentation for :class:`sge.input.MouseMove` for more
        information.
        """
        pass

    def event_paused_mouse_button_press(self, button):
        """
        See the documentation for :class:`sge.input.MouseButtonPress`
        for more information.
        """
        pass

    def event_paused_mouse_button_release(self, button):
        """
        See the documentation for :class:`sge.input.MouseButtonRelease`
        for more information.
        """
        pass

    def event_paused_joystick_axis_move(self, js_name, js_id, axis, value):
        """
        See the documentation for :class:`sge.input.JoystickAxisMove`
        for more information.
        """
        pass

    def event_paused_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """
        See the documentation for :class:`sge.input.JoystickHatMove` for
        more information.
        """
        pass

    def event_paused_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """
        See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.
        """
        pass

    def event_paused_joystick_button_press(self, js_name, js_id, button):
        """
        See the documentation for :class:`sge.input.JoystickButtonPress`
        for more information.
        """
        pass

    def event_paused_joystick_button_release(self, js_name, js_id, button):
        """
        See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.
        """
        pass

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create an object of this class and add it to the current room.

        ``args`` and ``kwargs`` are passed to the constructor method of
        ``cls`` as arguments.  Calling
        ``obj = cls.create(*args, **kwargs)`` is the same as::

            obj = cls(*args, **kwargs)
            sge.game.current_room.add(obj)
        """
        obj = cls(*args, **kwargs)
        sge.game.current_room.add(obj)
        return obj


class Mouse(Object):

    @property
    def x(self):
        if (sge.game.current_room is not None and
                (not sge.game.grab_input or sge.game.mouse.visible)):
            mouse_x = sge.mouse.get_x()
            mouse_y = sge.mouse.get_y()
            for view in sge.game.current_room.views:
                if (view.xport <= mouse_x < view.xport + view.wport and
                        view.yport <= mouse_y < view.yport + view.hport):
                    return ((mouse_x - view.xport) *
                            (view.width / view.wport) + view.x)

        return -1

    @x.setter
    def x(self, value):
        pass

    @property
    def y(self):
        if (sge.game.current_room is not None and
                (not sge.game.grab_input or sge.game.mouse.visible)):
            mouse_x = sge.mouse.get_x()
            mouse_y = sge.mouse.get_y()
            for view in sge.game.current_room.views:
                if (view.xport <= mouse_x <= view.xport + view.wport and
                        view.yport <= mouse_y <= view.yport + view.hport):
                    return ((mouse_y - view.yport) *
                            (view.height / view.hport) + view.y)

        return -1

    @y.setter
    def y(self, value):
        pass

    @property
    def sprite(self):
        return self.rd["sprite"]

    @sprite.setter
    def sprite(self, value):
        self.rd["sprite"] = value
        self.set_cursor()

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.__visible = value
        self.set_cursor()

    @property
    def tangible(self):
        if self.x != -1 and self.y != -1:
            return self.rd["tangible"]
        else:
            return False

    @tangible.setter
    def tangible(self, value):
        self.rd["tangible"] = value

    def __init__(self):
        self.__visible = True
        super(Mouse, self).__init__(0, 0, 10000)

    def event_step(self, time_passed, delta_mult):
        o_update_object_areas(self)
        o_update_collision_lists(self)

    def event_collision(self, other, xdirection, ydirection):
        sge.game.event_mouse_collision(other, xdirection, ydirection)

    def set_cursor(self):
        # Set the mouse cursor and visibility state.
        if not sge.game.grab_input:
            pygame.mouse.set_visible(self.visible and self.sprite is None)
        else:
            pygame.mouse.set_visible(False)

    def project_cursor(self):
        if (not sge.game.grab_input and self.visible and
                self.sprite is not None):
            img = s_get_image(self.sprite, self.image_index, self.image_xscale,
                              self.image_yscale, self.image_rotation,
                              self.image_alpha, self.image_blend)
            x = sge.mouse.get_x()
            y = sge.mouse.get_y()

            if x is not None and y is not None:
                x -= self.image_origin_x
                y -= self.image_origin_y
                r.game_window_projections.append((img, x, y, self.z, None))
