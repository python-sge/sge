# Copyright (C) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
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
import weakref

import pygame

import sge


__all__ = ['StellarClass', 'Mouse', '_PygameProjectionSprite']


class StellarClass(object):

    """Class for game objects.

    This class is used for game objects, such as the player, enemies,
    bullets, and the HUD.  Generally, each type of object has its own
    subclass of :class:`sge.StellarClass`.

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
       automatic functionality and normal events will be disabled and
       events which have names starting with ``event_inactive_`` will be
       executed instead of the corresponding normal events.

       .. note::

          Inactive :class:`sge.StellarClass` objects are still visible
          by default and continue to be involved in collisions.  In
          addition, collision events and destroy events still occur even
          if the object is inactive.  If you wish for the object to not
          be visible, set :attr:`visible` to :const:`False`.  If you
          wish for the object to not perform collision events, set
          :attr:`checks_collisions` to :const:`False`.

       .. note::

          Making an object inactive will not likely have a significant
          effect on performance.  For performance enhancement, it is far
          more effective to exclude objects from collision detection.
          Object deactivation is meant to be used to easily maintain
          control over objects that are currently being excluded from
          collision detection (e.g. to prevent a gravity effect that
          would otherwise occur, or to prevent the object from moving
          through walls).

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
       outside the view.  If you do this, you likely also to set
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

       The velocity of the object toward the right.

    .. attribute:: yvelocity

       The velocity of the object toward the bottom.

    .. attribute:: speed

       The total (directional) speed of the object.

    .. attribute:: move_direction

       The direction of the object's movement in degrees, with ``0``
       being directly to the right and rotation in a positive direction
       being counter-clockwise.

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

       The animation rate in frames per second.  If set to
       :const:`None`, the value recommended by the sprite is used.

    .. attribute:: image_speed

       The animation rate as a factor of :attr:`sge.game.fps`.  If set
       to :const:`None`, the value recommended by the sprite is used.

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

    .. attribute:: id

       The unique identifier for this object.  (Read-only)

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

    """

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._update_collision_areas()

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._update_collision_areas()

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        if self._pygame_sprite in sge.game._pygame_sprites:
            self._pygame_sprite.kill()
            sge.game._pygame_sprites.add(self._pygame_sprite, layer=self._z)

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

        # Make the mouse have a higher Z-axis value
        if ("mouse" in sge.game.objects and
                sge.game.objects["mouse"].z <= value):
            sge.game.objects["mouse"]._z = value + 1

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        if isinstance(value, sge.Sprite) or value is None:
            self._sprite = value
        else:
            self._sprite = sge.game.sprites[value]

        if self._sprite is not None:
            self.image_index = self.image_index % len(self._sprite._images)

    @property
    def tangible(self):
        return self._tangible

    @tangible.setter
    def tangible(self, value):
        self._tangible = value
        position = None
        for i in range(len(sge.game._colliders)):
            if sge.game._colliders[i]() is self:
                position = i
                break

        if self._tangible:
            if position is None:
                sge.game._colliders.append(weakref.ref(self))
        else:
            if position is not None:
                del sge.game._colliders[position]

    @property
    def bbox_x(self):
        return self._bbox_x

    @bbox_x.setter
    def bbox_x(self, value):
        self._bbox_x = value
        self._update_collision_areas()

    @property
    def bbox_y(self):
        return self._bbox_y

    @bbox_y.setter
    def bbox_y(self, value):
        self._bbox_y = value
        self._update_collision_areas()

    @property
    def bbox_width(self):
        return self._bbox_width

    @bbox_width.setter
    def bbox_width(self, value):
        self._bbox_width = value
        self._update_collision_areas()

    @property
    def bbox_height(self):
        return self._bbox_height

    @bbox_height.setter
    def bbox_height(self, value):
        self._bbox_height = value
        self._update_collision_areas()

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
        return self._xvelocity

    @xvelocity.setter
    def xvelocity(self, value):
        self._xvelocity = value
        self._set_speed()

    @property
    def yvelocity(self):
        return self._yvelocity

    @yvelocity.setter
    def yvelocity(self, value):
        self._yvelocity = value
        self._set_speed()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
        self._xvelocity = math.cos(radians(self.move_direction)) * value
        self._yvelocity = math.sin(radians(self.move_direction)) * value

    @property
    def move_direction(self):
        return self._move_direction

    @move_direction.setter
    def move_direction(self, value):
        self._move_direction = value
        self._xvelocity = math.cos(radians(value)) * self.speed
        self._yvelocity = math.sin(radians(value)) * self.speed

    @property
    def image_index(self):
        return self._image_index

    @image_index.setter
    def image_index(self, value):
        if self.sprite is not None:
            self._image_index = value
            while self._image_index >= len(self.sprite._images):
                self._image_index -= len(self.sprite._images)
                self.event_animation_end()
        else:
            self._image_index = 0

    @property
    def image_origin_x(self):
        if self.regulate_origin and self.sprite is not None:
            id_ = (self.sprite.id, self.sprite.width, self.sprite.height,
                   self.sprite.origin_x, self.sprite.origin_y,
                   self.image_xscale, self.image_yscale, self.image_rotation)

            if id_ not in self._origins_x:
                x_offset, y_offset = self._get_origin_offset()
                self._origins_x[id_] = self.sprite.origin_x + x_offset
                self._origins_y[id_] = self.sprite.origin_y + y_offset

            self._image_origin_x = self._origins_x[id_]

        if self._image_origin_x is None:
            return self.sprite.origin_x if self.sprite is not None else 0
        else:
            return self._image_origin_x

    @image_origin_x.setter
    def image_origin_x(self, value):
        self._image_origin_x = value

    @property
    def image_origin_y(self):
        if self.regulate_origin and self.sprite is not None:
            id_ = (self.sprite.id, self.sprite.width, self.sprite.height,
                   self.sprite.origin_x, self.sprite.origin_y,
                   self.image_xscale, self.image_yscale, self.image_rotation)

            if id_ not in self._origins_y:
                x_offset, y_offset = self._get_origin_offset()
                self._origins_x[id_] = self.sprite.origin_x + x_offset
                self._origins_y[id_] = self.sprite.origin_y + y_offset

            self._image_origin_y = self._origins_y[id_]

        if self._image_origin_y is None:
            return self.sprite.origin_y if self.sprite is not None else 0
        else:
            return self._image_origin_y

    @image_origin_y.setter
    def image_origin_y(self, value):
        self._image_origin_y = value

    @property
    def image_fps(self):
        return self._fps

    @image_fps.setter
    def image_fps(self, value):
        if value is None:
            value = self.sprite.fps if self.sprite is not None else 0

        self._fps = abs(value)
        if self._fps != 0:
            self._frame_time = 1000 / self._fps
            if not self._frame_time:
                # This would be caused by a round-off to 0 resulting
                # from a much too high frame rate.  It would cause a
                # division by 0 later, so this is meant to prevent that.
                self._frame_time = 0.000001
        else:
            self._frame_time = None

    @property
    def image_speed(self):
        return self.image_fps / sge.game.fps

    @image_speed.setter
    def image_speed(self, value):
        if value is None:
            value = self.sprite.speed if self.sprite is not None else 0

        self.image_fps = value * sge.game.fps

    @property
    def mask(self):
        if self.collision_precise:
            id_ = ("precise", self.sprite.id, self.sprite.width,
                   self.sprite.height, self.image_index, self.image_xscale,
                   self.image_yscale, self.image_rotation)
        else:
            id_ = (self.collision_ellipse, self.bbox_x, self.bbox_y,
                   self.bbox_width, self.bbox_height, self.image_xscale,
                   self.image_yscale)

        if id_ in self._masks:
            return self._masks[id_]
        else:
            if self.collision_precise:
                # Mask based on opacity of the current image.
                mask = self.sprite._get_precise_mask(
                    self.image_index, self.image_xscale, self.image_yscale,
                    self.image_rotation)
            elif self.collision_ellipse:
                # Elliptical mask based on bounding box.
                mask = [[False for y in range(self.bbox_height)]
                        for x in range(self.bbox_width)]
                a = len(mask) / 2
                b = len(mask[0]) / 2 if mask else 0

                for x in range(len(mask)):
                    for y in range(len(mask[x])):
                        if ((x - a) / a) ** 2 + ((y - b) / b) ** 2 <= 1:
                            mask[x][y] = True
            else:
                # Mask is all pixels in the bounding box.
                mask = [[True for y in range(self.bbox_height)]
                        for x in range(self.bbox_width)]

            self._masks[id_] = mask
            return mask

    @property
    def mask_x(self):
        if self.collision_precise:
            id_ = (self.sprite.id, self.sprite.width, self.sprite.height,
                   self.image_origin_x, self.image_origin_y, self.image_xscale,
                   self.image_yscale, self.image_rotation)
            if id_ in self._masks_x_offset:
                offset = self._masks_x_offset[id_]
                return self.x - (self.image_origin_x + offset)
            elif self.image_rotation % 180:
                width = self._get_image_width()
                normal_width = self._get_normal_image_width()
                offset = (width - normal_width) / 2
                self._masks_x_offset[id_] = offset
                return self.x - (self.image_origin_x + offset)
            else:
                self._masks_x_offset[id_] = 0
                return self.x - self.image_origin_x
        else:
            return self.bbox_left

    @property
    def mask_y(self):
        if self.collision_precise:
            id_ = (self.sprite.id, self.sprite.width, self.sprite.height,
                   self.image_origin_x, self.image_origin_y, self.image_xscale,
                   self.image_yscale, self.image_rotation)
            if id_ in self._masks_y_offset:
                offset = self._masks_y_offset[id_]
                return self.y - (self.image_origin_y + offset)
            elif self.image_rotation % 180:
                height = self._get_image_height()
                normal_height = self._get_normal_image_height()
                offset = (height - normal_height) / 2
                self._masks_y_offset[id_] = offset
                return self.y - (self.image_origin_y + offset)
            else:
                self._masks_y_offset[id_] = 0
                return self.y - self.image_origin_y
        else:
            return self.bbox_top

    def __init__(self, x, y, z=0, ID=None, sprite=None, visible=True,
                 active=True, checks_collisions=True, tangible=True,
                 bbox_x=None, bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        """Constructor method.

        Arguments:

        - ``ID`` -- The value to set :attr:`id` to.  If set to
          :const:`None`, ``fname`` minus the extension will be used,
          modified by the SGE if it is already the unique identifier of
          another music object.

        All other arugments set the respective initial attributes of the
        object.  See the documentation for :class:`sge.StellarClass` for
        more information.

        """
        self.xstart = x
        self.ystart = y
        self.xprevious = x
        self.yprevious = y

        self._image_index = image_index
        self.sprite = sprite
        self.visible = visible
        self.active = active
        self.checks_collisions = checks_collisions
        self.tangible = tangible
        if self.sprite is not None:
            sprite_bbox_x = self.sprite.bbox_x
            sprite_bbox_y = self.sprite.bbox_y
            sprite_bbox_width = self.sprite.bbox_width
            sprite_bbox_height = self.sprite.bbox_height
        else:
            sprite_bbox_x = 0
            sprite_bbox_y = 0
            sprite_bbox_width = 1
            sprite_bbox_height = 1
        self._bbox_x = bbox_x if bbox_x is not None else sprite_bbox_x
        self._bbox_y = bbox_y if bbox_y is not None else sprite_bbox_y
        self._bbox_width = (bbox_width if bbox_width is not None else
                            sprite_bbox_width)
        self._bbox_height = (bbox_height if bbox_height is not None else
                             sprite_bbox_height)
        self.regulate_origin = regulate_origin
        self.collision_ellipse = collision_ellipse
        self.collision_precise = collision_precise
        self._collision_areas = []
        self._colliders = []

        objects = sge.game.objects.copy()
        if ID is not None:
            self.id = ID
        else:
            ID = 0
            while ID in objects:
                ID += 1
            self.id = ID

        objects[self.id] = self
        sge.game.objects = objects

        self._x = x
        self._y = y
        self._z = z
        self._xvelocity = 0
        self._yvelocity = 0
        self._move_direction = 0
        self._speed = 0
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self._anim_count = 0
        self._origins_x = {}
        self._origins_y = {}
        self.image_origin_x = image_origin_x
        self.image_origin_y = image_origin_y
        self.image_fps = image_fps
        self.image_xscale = image_xscale
        self.image_yscale = image_yscale
        self.image_rotation = image_rotation
        self.image_alpha = image_alpha
        self.image_blend = image_blend
        self._masks = {}
        self._masks_x_offset = {}
        self._masks_y_offset = {}

        self._alarms = {}

        self._rect = pygame.Rect(self.bbox_x, self.bbox_y, self.bbox_width,
                                 self.bbox_height)
        if self.id != "mouse":
            self._pygame_sprite = _PygameSprite(self)
        else:
            self._pygame_sprite = _FakePygameSprite(self)

        self.z = z

        self._start_x = self.x
        self._start_y = self.y
        self._start_z = self.z
        self._start_sprite = self.sprite
        self._start_visible = self.visible
        self._start_checks_collisions = self.checks_collisions
        self._start_bbox_x = self.bbox_x
        self._start_bbox_y = self.bbox_y
        self._start_bbox_width = self.bbox_width
        self._start_bbox_height = self.bbox_height
        self._start_collision_ellipse = self.collision_ellipse
        self._start_collision_precise = self.collision_precise

    def collision(self, other=None, x=None, y=None):
        """Return a list of objects colliding with this object.

        Arguments:

        - ``other`` -- What to check for collisions with.  Can be one of
          the following:

          - A :class:`sge.StellarClass` object.
          - The unique identifier of a :class:`sge.StellarClass` object.
          - A list of :class:`sge.StellarClass` objects and/or unique
            identifiers of :class:`sge.StellarClass` objects.
          - A class derived from :class:`sge.StellarClass`.
          - :const:`None`: Check for collisions with all objects.

        - ``x`` -- The horizontal position to pretend this object is at
          for the purpose of the collision detection.  If set to
          :const:`None`, :attr:`x` will be used.
        - ``y`` -- The vertical position to pretend this object is at
          for the purpose of the collision detection.  If set to
          :const:`None`, :attr:`y` will be used.

        """
        if self.tangible:
            room = sge.game.current_room
            others = []
            collisions = []

            for area in self._collision_areas:
                if area is not None:
                    i, j = area
                    room_area = room._collision_areas[i][j]
                else:
                    room_area = room._collision_area_void

                for ref in room_area:
                    obj = ref()
                    if obj is not None and obj is not self:
                        if other is None:
                            others.append(obj)
                        elif isinstance(other, StellarClass):
                            if obj is other:
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
                                pass

            # Change x and y to be offset values; these are easier to use.
            if x is not None:
                x -= self.x
            else:
                x = 0

            if y is not None:
                y -= self.y
            else:
                y = 0

            for other in others:
                if (self.collision_precise or self.collision_ellipse or
                        other.collision_precise or other.collision_ellipse):
                    # Use masks.
                    if sge.collision.masks_collide(
                            self.mask_x + x, self.mask_y + y, self.mask,
                            other.mask_x, other.mask_y, other.mask):
                        collisions.append(other)
                else:
                    # Use bounding boxes.
                    if sge.collision.rectangles_collide(
                            self.bbox_left + x, self.bbox_top + y,
                            self.bbox_width, self.bbox_height, other.bbox_left,
                            other.bbox_top, other.bbox_width,
                            other.bbox_height):
                        collisions.append(other)

            return collisions
        else:
            return []

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        After this method is called, ``value`` will reduce by 1 each
        frame (adjusted for delta timing if it is enabled) until it
        reaches 0, at which point :meth:`sge.StellarClass.event_alarm`
        will be executed with ``alarm_id``.

        See the documentation for :meth:`sge.Game.set_alarm` for more
        information.

        """
        if value is not None:
            self._alarms[alarm_id] = value
        elif alarm_id in self._alarms:
            del self._alarms[alarm_id]

    def get_alarm(self, alarm_id):
        """Return the value of an alarm.

        See the documentation for :meth:`sge.Game.get_alarm` for more
        information.

        """
        if alarm_id in self._alarms:
            return self._alarms[alarm_id]
        else:
            return None

    def destroy(self):
        """Destroy the object."""
        sge.game._background_changed = True
        self.event_destroy()
        self._pygame_sprite.kill()
        objects = sge.game.objects.copy()
        if self.id in objects:
            del objects[self.id]
        sge.game.objects = objects

        for room in sge.game.rooms:
            objects = room.objects[:]
            while self in objects:
                objects.remove(self)
            room.objects = objects

            objects_by_class = room.objects_by_class.copy()
            for cls in objects_by_class:
                if isinstance(self, cls):
                    objects = objects_by_class[cls][:]
                    while self in objects:
                        objects.remove(self)
                    objects_by_class[cls] = objects
            room.objects_by_class = objects_by_class

    def event_create(self):
        """Create event.

        Called when the object is created.  It is always called after
        any room start events occurring at the same time.

        """
        pass

    def event_destroy(self):
        """Destroy event."""
        pass

    def event_begin_step(self, time_passed, delta_mult):
        """Begin step event.

        This event is executed each frame before automatic updates to
        objects (such as the effects of the speed variables).

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        .. note::

           Automatic updates, the only occurances between this event and
           :meth:`sge.StellarClass.event_step`, do not occur unless the
           object is active, so there is no "inactive" variant of this
           event.  Use :meth:`sge.StellarClass.event_inactive_step`
           instead.

        """
        pass

    def event_step(self, time_passed, delta_mult):
        """Step event.

        This event is executed each frame after automatic updates to
        objects (such as the effects of the speed variables), but before
        collision events.

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        """
        pass

    def event_end_step(self, time_passed, delta_mult):
        """Step event.

        This event is executed each frame after automatic updates to
        objects (such as the effects of the speed variables), but before
        collision events.

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        """
        pass

    def event_alarm(self, alarm_id):
        """Alarm event.

        See the documentation for :meth:`sge.Game.event_alarm` for more
        information.

        """
        pass

    def event_animation_end(self):
        """Animation End event.

        Called when an animation cycle ends.

        """
        pass

    def event_key_press(self, key, char):
        """Key press event.

        See the documentation for :class:`sge.input.KeyPress` for more
        information.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        See the documentation for :class:`sge.input.KeyRelease` for more
        information.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        See the documentation for :class:`sge.input.MouseMove` for more
        information.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        See the documentation for :class:`sge.input.MouseButtonPress`
        for more information.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        See the documentation for :class:`sge.input.MouseButtonRelease`
        for more information.

        """
        pass

    def event_joystick_axis_move(self, js_name, js_id, axis, value):
        """Joystick axis move event.

        See the documentation for :class:`sge.input.JoystickAxisMove`
        for more information.

        """
        pass

    def event_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """Joystick hat move event.

        See the documentation for :class:`sge.input.JoystickHatMove` for
        more information.

        """
        pass

    def event_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """Joystick trackball move event.

        See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.

        """
        pass

    def event_joystick_button_press(self, js_name, js_id, button):
        """Joystick button press event.

        See the documentation for :class:`sge.input.JoystickButtonPress`
        for more information.

        """
        pass

    def event_joystick_button_release(self, js_name, js_id, button):
        """Joystick button release event.

        See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.

        """
        pass

    def event_update_position(self, delta_mult):
        """Update position event.

        Called when it's time to update the position of the object.
        This method handles this functionality, so defining this will
        override the default behavior and allow you to handle the speed
        variables in a special way.

        The default behavior of this method is::

            self.x += self.xvelocity * delta_mult
            self.y += self.yvelocity * delta_mult

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        """
        self.x += self.xvelocity * delta_mult
        self.y += self.yvelocity * delta_mult

    def event_collision(self, other):
        """Default collision event.

        Called when another object collides with this object and none of
        the directional collision events are appropriate.  In
        particular, this is called if the collision was already
        happening in the previous frame.  This is also the event method
        called by the directional collision event methods by default.

        Arguments:

        - ``other`` -- The other object which was collided with.

        """
        pass

    def event_collision_left(self, other):
        """Left collision event.

        Called when another object collides with this object's left
        side.

        Arguments:

        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        :meth:`sge.StellarClass.event_collision`.

        """
        self.event_collision(other)

    def event_collision_right(self, other):
        """Right collision event.

        Called when another object collides with this object's right
        side.

        Arguments:
        
        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        :meth:`sge.StellarClass.event_collision`.

        """
        self.event_collision(other)

    def event_collision_top(self, other):
        """Top collision event.

        Called when another object collides with this object's top side.

        Arguments:

        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        :meth:`sge.StellarClass.event_collision`.

        """
        self.event_collision(other)

    def event_collision_bottom(self, other):
        """Bottom collision event.

        Called when another object collides with this object's bottom
        side.

        Arguments:

        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        :meth:`sge.StellarClass.event_collision`.

        """
        self.event_collision(other)

    def event_inactive_step(self, time_passed, delta_mult):
        """Step event when this object is inactive.

        See the documentation for :meth:`sge.StellarClass.event_step`
        for more information.  The object is considered to be inactive
        when :attr:`active` is :const:`False`.

        """
        pass

    def event_inactive_end_step(self, time_passed, delta_mult):
        """End step event when this object is inactive.

        See the documentation for
        :meth:`sge.StellarClass.event_end_step` for more information.
        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        """
        pass

    def event_inactive_key_press(self, key, char):
        """Key press event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for :class:`sge.input.KeyPress` for more
        information.

        """
        pass

    def event_inactive_key_release(self, key):
        """Key release event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for :class:`sge.input.KeyRelease` for more
        information.

        """
        pass

    def event_inactive_mouse_move(self, x, y):
        """Mouse move event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for :class:`sge.input.MouseMove` for more
        information.

        """
        pass

    def event_inactive_mouse_button_press(self, button):
        """Mouse button press event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for :class:`sge.input.MouseButtonPress`
        for more information.

        """
        pass

    def event_inactive_mouse_button_release(self, button):
        """Mouse button release event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for :class:`sge.input.MouseButtonRelease`
        for more information.

        """
        pass

    def event_inactive_joystick_axis_move(self, js_name, js_id, axis, value):
        """Joystick axis move event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for :class:`sge.input.JoystickAxisMove`
        for more information.

        """
        pass

    def event_inactive_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """Joystick hat move event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for :class:`sge.input.JoystickHatMove` for
        more information.

        """
        pass

    def event_inactive_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """Joystick trackball move event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.

        """
        pass

    def event_inactive_joystick_button_press(self, js_name, js_id, button):
        """Joystick button press event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for :class:`sge.input.JoystickButtonPress`
        for more information.

        """
        pass

    def event_inactive_joystick_button_release(self, js_name, js_id, button):
        """Joystick button release event when this object is inactive.

        The object is considered to be inactive when :attr:`active` is
        :const:`False`.

        See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.

        """
        pass

    def event_paused_key_press(self, key, char):
        """Key press event when paused.

        See the documentation for :class:`sge.input.KeyPress` for more
        information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See the documentation for :class:`sge.input.KeyRelease` for more
        information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See the documentation for :class:`sge.input.MouseMove` for more
        information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See the documentation for :class:`sge.input.MouseButtonPress`
        for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See the documentation for :class:`sge.input.MouseButtonRelease`
        for more information.

        """
        pass

    def event_paused_joystick_axis_move(self, js_name, js_id, axis, value):
        """Joystick axis move event when paused.

        See the documentation for :class:`sge.input.JoystickAxisMove`
        for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """Joystick hat move event when paused.

        See the documentation for :class:`sge.input.JoystickHatMove` for
        more information.

        """
        pass

    def event_paused_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """Joystick trackball move event when paused.

        See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.

        """
        pass

    def event_paused_joystick_button_press(self, js_name, js_id, button):
        """Joystick button press event when paused.

        See the documentation for :class:`sge.input.JoystickButtonPress`
        for more information.

        """
        pass

    def event_paused_joystick_button_release(self, js_name, js_id, button):
        """Joystick button release event when paused.

        See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.

        """
        pass

    @classmethod
    def create(cls, *args, **kwargs):
        """Create an object of this class in the current room.

        ``args`` and ``kwargs`` are passed to the constructor method of
        ``cls`` as arguments.  Calling
        ``obj = cls.create(*args, **kwargs)`` is the same as::

            obj = cls(*args, **kwargs)
            sge.game.current_room.add(obj)

        """
        obj = cls(*args, **kwargs)
        sge.game.current_room.add(obj)
        return obj

    def _update(self, time_passed, delta_mult):
        # Update this object (should be called each frame).
        # Update the animation frame.
        if self.image_fps:
            self._anim_count += time_passed
            self.image_index += int(self._anim_count // self._frame_time)
            self._anim_count %= self._frame_time

        # Alarms
        activated_alarms = []
        for a in self._alarms:
            self._alarms[a] -= delta_mult
            if self._alarms[a] <= 0:
                activated_alarms.append(a)
        for a in activated_alarms:
            del self._alarms[a]
            self.event_alarm(a)

        # Movement
        if self.id != "mouse":
            self.event_update_position(delta_mult)

    def _update_collision_areas(self):
        if self.tangible:
            room = sge.game.current_room

            if self.collision_precise:
                my_areas = sge.collision._get_rectangle_collision_areas(
                    self.mask_x, self.mask_y, len(self.mask),
                    len(self.mask[0]) if self.mask else 0)
            else:
                my_areas = sge.collision._get_rectangle_collision_areas(
                    self.bbox_left, self.bbox_top, self.bbox_width,
                    self.bbox_height)

            for area in self._collision_areas:
                if area not in my_areas:
                    if area is not None:
                        i, j = area
                        room_area = room._collision_areas[i][j]
                    else:
                        room_area = room._collision_area_void

                    for i in range(len(room_area), 0, -1):
                        if room_area[i - 1]() is self:
                            del room_area[i - 1]

            for area in my_areas:
                if area not in self._collision_areas:
                    if area is not None:
                        i, j = area
                        room._collision_areas[i][j].append(weakref.ref(self))
                    else:
                        room._collision_area_void.append(weakref.ref(self))

            self._collision_areas = my_areas
        else:
            self._collision_areas = []

    def _detect_collisions(self):
        if self.checks_collisions:
            for other_ref in self._colliders:
                if other_ref() is not None and other_ref() is not self:
                    other = other_ref()
                else:
                    continue

                # Delete self from the other object's list of colliders to
                # prevent redundancy.
                for i in range(len(other._colliders)):
                    if other._colliders[i]() is self:
                        del other._colliders[i]
                        break

                if self.collision(other):
                    self_prev_bbox_left = self.xprevious + self.bbox_x
                    self_prev_bbox_right = (self_prev_bbox_left +
                                            self.bbox_width)
                    self_prev_bbox_top = self.yprevious + self.bbox_y
                    self_prev_bbox_bottom = (self_prev_bbox_top +
                                             self.bbox_height)
                    other_prev_bbox_left = other.xprevious + other.bbox_x
                    other_prev_bbox_right = (other_prev_bbox_left +
                                             other.bbox_width)
                    other_prev_bbox_top = other.yprevious + other.bbox_y
                    other_prev_bbox_bottom = (other_prev_bbox_top +
                                              other.bbox_height)

                    if self_prev_bbox_right <= other_prev_bbox_left:
                        xdirection = 1
                    elif self_prev_bbox_left >= other_prev_bbox_right:
                        xdirection = -1
                    else:
                        xdirection = 0

                    if self_prev_bbox_bottom <= other_prev_bbox_top:
                        ydirection = 1
                    elif self_prev_bbox_top >= other_prev_bbox_bottom:
                        ydirection = -1
                    else:
                        ydirection = 0

                    if xdirection or ydirection:
                        if xdirection == 1:
                            self.event_collision_right(other)
                            other.event_collision_left(self)
                        elif xdirection == -1:
                            self.event_collision_left(other)
                            other.event_collision_right(self)

                        if ydirection == 1:
                            self.event_collision_bottom(other)
                            other.event_collision_top(self)
                        elif ydirection == -1:
                            self.event_collision_top(other)
                            other.event_collision_bottom(self)
                    else:
                        self.event_collision(other)
                        other.event_collision(self)

    def _get_image_width(self):
        # Get the width of the sprite when scaled rotated.
        return int(self.sprite._get_image(
            self.image_index, self.image_xscale, self.image_yscale,
            self.image_rotation).get_width() / sge.game._xscale)

    def _get_normal_image_width(self):
        # Get the width of the sprite without scaling and rotation.
        return int(self.sprite._get_image(
            self.image_index, self.image_xscale,
            self.image_yscale).get_width() / sge.game._xscale)

    def _get_image_height(self):
        # Get the height of the sprite when scaled rotated.
        return int(self.sprite._get_image(
            self.image_index, self.image_xscale, self.image_yscale,
            self.image_rotation).get_height() / sge.game._xscale)

    def _get_normal_image_height(self):
        # Get the height of the sprite without scaling and rotation.
        return int(self.sprite._get_image(
            self.image_index, self.image_xscale,
            self.image_yscale).get_height() / sge.game._xscale)

    def _get_origin_offset(self):
        # Return the amount to offset the origin as (x, y).
        new_origin_x = self.sprite.origin_x
        new_origin_y = self.sprite.origin_y

        width = self._get_image_width() / abs(self.image_xscale)
        height = self._get_image_height() / abs(self.image_yscale)
        normal_width = self._get_normal_image_width() / abs(self.image_xscale)
        normal_height = self._get_normal_image_height() / abs(self.image_yscale)

        if self.image_rotation % 360:
            center_x = normal_width / 2
            center_y = normal_height / 2
            c_origin_x = new_origin_x - center_x
            c_origin_y = new_origin_y - center_y
            start_angle = math.atan2(-c_origin_y, c_origin_x)
            radius = math.hypot(c_origin_x, c_origin_y)
            new_angle = start_angle + math.radians(self.image_rotation)
            new_c_origin_x = radius * math.cos(new_angle)
            new_c_origin_y = -(radius * math.sin(new_angle))
            new_origin_x = new_c_origin_x + center_x
            new_origin_y = new_c_origin_y + center_y

        if self.image_xscale < 0:
            new_origin_x = width - new_origin_x

        if self.image_yscale < 0:
            new_origin_y = height - new_origin_y

        new_origin_x *= abs(self.image_xscale)
        new_origin_y *= abs(self.image_yscale)

        x_offset = new_origin_x - self.sprite.origin_x
        y_offset = new_origin_y - self.sprite.origin_y

        return (x_offset, y_offset)

    def _set_speed(self):
        # Set the speed and move direction based on xvelocity and
        # yvelocity.
        self._speed = math.sqrt(self._xvelocity ** 2 + self._yvelocity ** 2)

        if self._yvelocity == 0:
            base_angle = 0
        elif self._xvelocity == 0:
            base_angle = 90
        else:
            base_angle = math.degrees(math.atan(abs(self._yvelocity) /
                                                abs(self._xvelocity)))

        if self._xvelocity < 0 and self._yvelocity < 0:
            self._move_direction += 180
        elif self._xvelocity < 0:
            self._move_direction = 180 - base_angle
        elif self._yvelocity < 0:
            self._move_direction = 360 - base_angle
        else:
            self._move_direction = base_angle

        self._move_direction %= 360

    def _reset(self):
        # Reset the object back to its original state.
        self.x = self._start_x
        self.y = self._start_y
        self.z = self._start_z
        self.sprite = self._start_sprite
        self.visible = self._start_visible
        self.detects_collisions = self._start_detects_collisions
        self.bbox_x = self._start_bbox_x
        self.bbox_y = self._start_bbox_y
        self.bbox_width = self._start_bbox_width
        self.bbox_height = self._start_bbox_height
        self.collision_ellipse = self._start_collision_ellipse
        self.collision_precise = self._start_collision_precise


class Mouse(StellarClass):

    @property
    def x(self):
        if sge.game.current_room is not None:
            mouse_x = self.mouse_x / sge.game._xscale
            mouse_y = self.mouse_y / sge.game._yscale
            for view in sge.game.current_room.views:
                if (view.xport <= mouse_x <= view.xport + view.width and
                        view.yport <= mouse_y <= view.yport + view.height):
                    # We save this value so that if the mouse is in none of
                    # the views, the last known position in a view is used.
                    self._x = (mouse_x - view.xport) + view.x
                    break

            return self._x
        else:
            return 0

    @x.setter
    def x(self, value):
        rel_x = (value - self.x) * sge.game._xscale
        self.mouse_x += rel_x

        self.xprevious = self._x
        self._x = value
        self._bbox_left = value + self.bbox_x
        self._bbox_right = self.bbox_left + self.bbox_width

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

        pygame.mouse.set_pos(self.mouse_x, self.mouse_y)

    @property
    def y(self):
        if sge.game.current_room is not None:
            mouse_x = self.mouse_x / sge.game._xscale
            mouse_y = self.mouse_y / sge.game._yscale
            for view in sge.game.current_room.views:
                if (view.xport <= mouse_x <= view.xport + view.width and
                        view.yport <= mouse_y <= view.yport + view.height):
                    # We save this value so that if the mouse is in none of
                    # the views, the last known position in a view is used.
                    self._y = (mouse_y - view.yport) + view.y
                    break

            return self._y
        else:
            return 0

    @y.setter
    def y(self, value):
        rel_y = (value - self.y) * sge.game._yscale
        self.mouse_y += rel_y

        self.yprevious = self._y
        self._y = value
        self._bbox_top = value + self.bbox_y
        self._bbox_bottom = self.bbox_top + self.bbox_height

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

        pygame.mouse.set_pos(self.mouse_x, self.mouse_y)

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        if isinstance(value, sge.Sprite) or value is None:
            self._sprite = value
        else:
            self._sprite = sge.game.sprites[value]

        self.set_cursor()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self.set_cursor()

    def __init__(self):
        self._visible = True
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_xprevious = self.mouse_x
        self.mouse_yprevious = self.mouse_y
        self.previous_speeds = []

        super(Mouse, self).__init__(0, 0, 0, ID='mouse')

    def event_collision(self, other):
        sge.game.event_mouse_collision(other)

    def event_collision_left(self, other):
        sge.game.event_mouse_collision_left(other)

    def event_collision_right(self, other):
        sge.game.event_mouse_collision_right(other)

    def event_collision_top(self, other):
        sge.game.event_mouse_collision_top(other)

    def event_collision_bottom(self, other):
        sge.game.event_mouse_collision_bottom(other)

    def _update(self, time_passed, delta_mult):
        self.update_speed(time_passed)
        super(Mouse, self)._update(time_passed, delta_mult)
        self._update_collision_areas()

    def update_speed(self, time_passed):
        # Update the speed variables.  ``time_passed`` is the number of
        # milliseconds since the last speed update.
        self.previous_speeds.insert(0, (self.mouse_x - self.mouse_xprevious,
                                        self.mouse_y - self.mouse_yprevious,
                                        time_passed))
        time = 0
        num_steps = 0
        total_xvelocity = 0
        total_yvelocity = 0

        for speed in self.previous_speeds:
            time += speed[2]
            if time <= 250:
                num_steps += 1
                total_xvelocity += speed[0]
                total_yvelocity += speed[1]

        self.previous_speeds = self.previous_speeds[:num_steps]

        if num_steps > 0:
            self.xvelocity = total_xvelocity / num_steps
            self.yvelocity = total_yvelocity / num_steps
        else:
            self.xvelocity = 0
            self.yvelocity = 0

        self.mouse_xprevious = self.mouse_x
        self.mouse_yprevious = self.mouse_y
        self.xprevious = self.x
        self.yprevious = self.y

    def set_cursor(self):
        # Set the mouse cursor and visibility state.
        if not sge.game.grab_input:
            pygame.mouse.set_visible(self.visible and self.sprite is None)
        else:
            pygame.mouse.set_visible(False)

    def project_cursor(self):
        if (not sge.game.grab_input and self.visible and
                self.sprite is not None):
            x = (self.mouse_x / sge.game._xscale) - self.image_origin_x
            y = (self.mouse_y / sge.game._yscale) - self.image_origin_y
            img = self.sprite._get_image(
                self.image_index, self.image_xscale, self.image_yscale, 
                self.image_rotation, self.image_alpha, self.image_blend)

            sge.game._window_projections.append((img, x, y, None))

    def _reset(self):
        # Reset the mouse back to its original state, but NOT position.
        self.z = self._start_z
        self.sprite = self._start_sprite
        self.visible = self._start_visible
        self.detects_collisions = self._start_detects_collisions
        self.bbox_x = self._start_bbox_x
        self.bbox_y = self._start_bbox_y
        self.bbox_width = self._start_bbox_width
        self.bbox_height = self._start_bbox_height
        self.collision_ellipse = self._start_collision_ellipse
        self.collision_precise = self._start_collision_precise


class _PygameSprite(pygame.sprite.DirtySprite):

    # Handles drawing in this implementation.
    #
    # Scaling is handled transparently in the update method, which is
    # always called before drawing.  Everything else is the
    # responsibility of StellarClass, including animation (the current
    # frame is grabbed from the _image attribute of the parent object).

    def __init__(self, parent, *groups):
        # See pygame.sprite.DirtySprite.__init__.__doc__.  ``parent``
        # is a StellarClass object that this object belongs to.
        super(_PygameSprite, self).__init__(*groups)
        self.parent = weakref.ref(parent)
        self.image = pygame.Surface((1, 1))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

    def update(self):
        if self.parent() is not None:
            parent = self.parent()
            if parent.sprite is not None:
                new_image = parent.sprite._get_image(
                    parent.image_index, parent.image_xscale,
                    parent.image_yscale, parent.image_rotation,
                    parent.image_alpha, parent.image_blend)
                if self.image is not new_image:
                    self.must_redraw = False
                    self.image = new_image
                    self.dirty = 1

                if self.visible != parent.visible:
                    self.visible = int(parent.visible)
                    self.dirty = 1

                width = parent._get_image_width()
                normal_width = parent._get_normal_image_width()
                height = parent._get_image_height()
                normal_height = parent._get_normal_image_height()
                x_offset = (width - normal_width) / 2
                y_offset = (height - normal_height) / 2

                self.update_rect(parent.x, parent.y, parent.z, parent.sprite,
                                 parent.image_origin_x + x_offset,
                                 parent.image_origin_y + y_offset)
            else:
                self.image = pygame.Surface((1, 1))
                self.image.set_colorkey((0, 0, 0))
                self.dirty = 1
        else:
            self.kill()

    def update_rect(self, x, y, z, sprite, origin_x, origin_y):
        # Update the rect of this Pygame sprite, based on the SGE sprite
        # and coordinates given.  This involves creating "proxy"
        # one-time sprites for multiple views if necessary.
        views = sge.game.current_room.views

        if (len(views) == 1 and views[0].xport == 0 and views[0].yport == 0 and
                views[0].width == sge.game.width and
                views[0].height == sge.game.height):
            # There is only one view that takes up the whole screen, so
            # we don't need to worry about it.
            x = x - views[0].x - origin_x
            y = y - views[0].y - origin_y
            new_rect = self.image.get_rect()
            new_rect.left = round(x * sge.game._xscale) + sge.game._x
            new_rect.top = round(y * sge.game._yscale) + sge.game._y

            if self.rect != new_rect:
                self.rect = new_rect
                self.dirty = 1
        else:
            # There is something more complicated.  Have to account for
            # the possibility of edges or multiple appearances.
            original_used = False
            self.dirty = 1
            real_x = x
            real_y = y
            for view in views:
                x = real_x - view.x - origin_x + view.xport
                y = real_y - view.y - origin_y + view.yport
                w = sprite.width
                h = sprite.height
                new_rect = self.image.get_rect()
                new_rect.left = round(x * sge.game._xscale) + sge.game._x
                new_rect.top = round(y * sge.game._yscale) + sge.game._y
                inside_view = (x >= view.xport and
                               x + w <= view.xport + view.width and
                               y >= view.yport and
                               y + h <= view.yport + view.height)
                within_view = (x + w > view.xport and
                               x < view.xport + view.width and
                               y + h > view.yport and
                               y < view.yport + view.height)

                if not original_used and inside_view:
                    original_used = True
                    if self.rect == new_rect:
                        self.dirty = 0
                    else:
                        self.rect = new_rect
                elif within_view:
                    if inside_view:
                        img = self.image
                        rect = new_rect
                    else:
                        # Make a cut-off version of the sprite and
                        # adjust the rect accordingly.
                        if x < view.xport:
                            cut_x = view.xport - x
                            x = view.xport
                            w -= cut_x
                        else:
                            cut_x = 0

                        if x + w > view.xport + view.width:
                            w -= (x + w) - (view.xport + view.width)

                        if y < view.yport:
                            cut_y = view.yport - y
                            y = view.yport
                            h -= cut_y
                        else:
                            cut_y = 0

                        if y + h > view.yport + view.height:
                            h -= (y + h) - (view.yport + view.height)

                        x = sge.game._x + round(x * sge.game._xscale)
                        y = sge.game._y + round(y * sge.game._yscale)
                        cut_x *= sge.game._xscale
                        cut_y *= sge.game._yscale
                        w = round(w * sge.game._xscale)
                        h = round(h * sge.game._yscale)
                        rect = pygame.Rect(x, y, w, h)
                        cut_rect = pygame.Rect(cut_x, cut_y, w, h)
                        img = self.image.subsurface(cut_rect)

                    # Create proxy one-time sprite
                    proxy = _PygameOneTimeSprite(img, rect)
                    sge.game._pygame_sprites.add(proxy, layer=z)

            if not original_used:
                self.image = pygame.Surface((1, 1))
                self.image.set_colorkey((0, 0, 0))


class _PygameProjectionSprite(_PygameSprite):

    # Special Pygame sprite used for room projections.

    def __init__(self, x, y, z, sprite, image_index=0):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.x = x
        self.y = y
        self.z = z
        if isinstance(sprite, sge.Sprite):
            self.sprite = sprite
        else:
            self.sprite = sge.game.sprites[sprite]
        self.image_index = image_index
        self.image = self.sprite._get_image(image_index)
        self.rect = self.image.get_rect()

    def update(self):
        if self.dirty:
            self.image = self.sprite._get_image(self.image_index)
            self.update_rect(self.x, self.y, self.z, self.sprite,
                             self.sprite.origin_x, self.sprite.origin_y)
        else:
            self.kill()


class _FakePygameSprite(_PygameSprite):

    # Fake Pygame sprite for "use" by the mouse.

    def update(self):
        pass

    def update_rect(self):
        pass


class _PygameOneTimeSprite(pygame.sprite.DirtySprite):

    # A regular DirtySprite that only displays once, and then destroys
    # itself.

    def __init__(self, image, rect, *groups):
        super(_PygameOneTimeSprite, self).__init__(*groups)
        self.image = image
        self.rect = rect
        self.dirty = 1

    def update(self):
        if not self.dirty:
            self.kill()
