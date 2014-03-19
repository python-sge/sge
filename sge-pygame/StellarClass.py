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

import os
import sys
import traceback
import math
import weakref

import pygame

import sge


__all__ = ['StellarClass', 'Mouse', '_PygameProjectionSprite']


class StellarClass:

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
          wish for the object to not be involved in collisions, set
          :attr:`detects_collisions` to :const:`False`.

       .. note::

          Making an object inactive will not likely have a significant
          effect on performance.  For performance enhancement, it is far
          more effective to exclude objects from collision detection.
          Object deactivation is meant to be used to easily maintain
          control over objects that are currently being excluded from
          collision detection (e.g. to prevent a gravity effect that
          would otherwise occur, or to prevent the object from moving
          through walls).

    .. attribute:: detects_collisions

       Whether or not the object should be involved in collision
       detection.  Setting this to :const:`False` can improve
       performance if the object doesn't need to detect collisions.

       Depending on the game, a useful strategy to boost performance can
       be to exclude an object from collision detection while it is
       outside the view.  If you do this, you likely also to set
       :attr:`active` to :const:`False` as well so that the object
       doesn't move in undesireable ways (e.g. through walls).

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

    .. attribute:: image_alpha

       The alpha value applied to the entire image, where ``255`` is the
       original image, ``128`` is half the opacity of the original
       image, ``0`` is fully transparent, etc.

    .. attribute:: image_blend

       The color to blend with the sprite.  Set to :const:`None` for no
       color blending.

    .. attribute:: id

       The unique identifier for this object.  (Read-only)

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

    """

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

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

        self.image_index = self.image_index % len(self._sprite._images)

    @property
    def detects_collisions(self):
        return self._detects_collisions

    @detects_collisions.setter
    def detects_collisions(self, value):
        self._detects_collisions = value
        position = None
        for i in range(len(sge.game._colliders)):
            if sge.game._colliders[i]() is self:
                position = i
                break

        if self._detects_collisions:
            if position is None:
                sge.game._colliders.append(weakref.ref(self))
        else:
            if position is not None:
                del sge.game._colliders[position]

    @property
    def collision_ellipse(self):
        return self._collision_ellipse

    @collision_ellipse.setter
    def collision_ellipse(self, value):
        if value != self._collision_ellipse:
            self._collision_ellipse = value
            self._set_mask()

    @property
    def collision_precise(self):
        return self._collision_precise

    @collision_precise.setter
    def collision_precise(self, value):
        if value != self._collision_precise:
            self._collision_precise = value
            self._set_mask()

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

    def __init__(self, x, y, z=0, ID=None, sprite=None, visible=True,
                 active=True, detects_collisions=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 collision_ellipse=False, collision_precise=False,
                 xvelocity=0, yvelocity=0, image_index=0, image_fps=None,
                 image_xscale=1, image_yscale=1, image_rotation=0,
                 image_alpha=255, image_blend=None):
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
        self.detects_collisions = detects_collisions
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
        self.bbox_x = bbox_x if bbox_x is not None else sprite_bbox_x
        self.bbox_y = bbox_y if bbox_y is not None else sprite_bbox_y
        self.bbox_width = (bbox_width if bbox_width is not None else
                           sprite_bbox_width)
        self.bbox_height = (bbox_height if bbox_height is not None else
                            sprite_bbox_height)
        self._collision_ellipse = collision_ellipse
        self._collision_precise = collision_precise
        self._collision_areas = []
        self._colliders = []

        if ID is not None:
            self.id = ID
        else:
            ID = 0
            while ID in sge.game.objects:
                ID += 1
            self.id = ID

        sge.game.objects[self.id] = self

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
        self.image_fps = image_fps
        self.image_xscale = image_xscale
        self.image_yscale = image_yscale
        self.image_rotation = image_rotation
        self.image_alpha = image_alpha
        self.image_blend = image_blend

        self._alarms = {}

        self._rect = pygame.Rect(self.bbox_x, self.bbox_y, self.bbox_width,
                                 self.bbox_height)
        if self.id != "mouse":
            self._pygame_sprite = _PygameSprite(self)
        else:
            self._pygame_sprite = _FakePygameSprite(self)
        self._set_mask()

        self.z = z

        self._start_x = self.x
        self._start_y = self.y
        self._start_z = self.z
        self._start_sprite = self.sprite
        self._start_visible = self.visible
        self._start_detects_collisions = self.detects_collisions
        self._start_bbox_x = self.bbox_x
        self._start_bbox_y = self.bbox_y
        self._start_bbox_width = self.bbox_width
        self._start_bbox_height = self.bbox_height
        self._start_collision_ellipse = self.collision_ellipse
        self._start_collision_precise = self.collision_precise

    def collides(self, other, x=None, y=None):
        """Return whether or not this object collides with another.

        Arguments:

        - ``other`` -- The object to check for a collision with, or the
          unique identifier of said object.  ``other`` can also be a
          class to check for collisions with.
        - ``x`` -- The horizontal position to pretend this object is at
          for the purpose of the collision detection.  If set to
          :const:`None`, :attr:`x` will be used.
        - ``y`` -- The vertical position to pretend this object is at
          for the purpose of the collision detection.  If set to
          :const:`None`, :attr:`y` will be used.

        """
        if isinstance(other, StellarClass):
            others = [other]
        elif other in sge.game.current_room.objects_by_class:
            others = []
            for obj in sge.game.current_room.objects_by_class[other]:
                if obj.detects_collisions:
                    others.append(obj)
        else:
            others = []
            for ref in sge.game._colliders:
                if isinstance(ref(), other):
                    others.append(ref())

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
                self_rect = pygame.Rect(round(self.bbox_left + x),
                                        round(self.bbox_top + y),
                                        self.bbox_width, self.bbox_height)
                other_rect = pygame.Rect(round(other.bbox_left),
                                         round(other.bbox_top),
                                         other.bbox_width, other.bbox_height)

                if self.sprite is not None:
                    # Offset for rotation
                    w, h = self.sprite._get_image(
                        self.image_index, self.image_xscale,
                        self.image_yscale, self.image_rotation).get_size()

                    nw, nh = self.sprite._get_image(
                        self.image_index, self.image_xscale,
                        self.image_yscale).get_size()

                    offset = _get_rotation_offset(
                        self.sprite.origin_x, self.sprite.origin_y,
                        self.image_rotation, w, h, nw, nh)

                    self_rect.left -= offset[0]
                    self_rect.top -= offset[1]

                collide_rect = self_rect.clip(other_rect)
                self_xoffset = collide_rect.left - self_rect.left
                self_yoffset = collide_rect.top - self_rect.top
                other_xoffset = collide_rect.left - other_rect.left
                other_yoffset = collide_rect.top - other_rect.top

                for a in range(collide_rect.w):
                    for b in range(collide_rect.h):
                        if (self._hitmask[
                                a + self_xoffset][b + self_yoffset] and
                            other._hitmask[
                                a + other_xoffset][b + other_yoffset]):
                            return True
                        
            else:
                # Use bounding boxes.
                if (self.bbox_left + x < other.bbox_right and
                        self.bbox_right + x > other.bbox_left and
                        self.bbox_top + y < other.bbox_bottom and
                        self.bbox_bottom + y > other.bbox_top):
                    return True

        return False

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Arguments:

        - ``alarm_id`` -- The unique identifier of the alarm to set.
          Any value can be used as a unique identifier for an alarm.
        - ``value`` -- The value to set the alarm to.  Set to
          :const:`None` to disable the alarm.

        After this method is called, ``value`` will reduce by 1 each
        frame (adjusted for delta timing if it is enabled) until it
        reaches 0, at which point :meth:`sge.StellarClass.event_alarm`
        will be executed with ``alarm_id``.

        """
        if value is not None:
            self._alarms[alarm_id] = value
        elif alarm_id in self._alarms:
            del self._alarms[alarm_id]

    def get_alarm(self, alarm_id):
        """Return the value of an alarm.

        Arguments:

        - ``alarm_id`` -- The unique identifier of the alarm to check.

        If the alarm has not been set, :const:`None` will be returned.

        """
        if alarm_id in self._alarms:
            return self._alarms[alarm_id]
        else:
            return None

    def destroy(self):
        """Destroy the object."""
        self.event_destroy()
        self._pygame_sprite.kill()
        del sge.game.objects[self.id]

        for room in sge.game.rooms:
            while self in room.objects:
                room.objects.remove(self)

            for cls in room.objects_by_class:
                if isinstance(self, cls):
                    while self in room.objects_by_class[cls]:
                        room.objects_by_class[cls].remove(self)

    def event_create(self):
        """Create event.

        Called when the object is created.  It is always called after
        any room start events occurring at the same time.

        """
        pass

    def event_destroy(self):
        """Destroy event."""
        pass

    def event_begin_step(self, time_passed):
        """Begin step event.

        This event is executed each frame before automatic updates to
        objects (such as the effects of the speed variables).

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        .. note::

           Automatic updates, the only occurances between this event and
           :meth:`sge.StellarClass.event_step`, do not occur, so there
           is no need for an "inactive" variant of this event.  Use
           :meth:`sge.StellarClass.event_inactive_step` instead.

        """
        pass

    def event_step(self, time_passed):
        """Step event.

        This event is executed each frame after automatic updates to
        objects (such as the effects of the speed variables), but before
        collision events.

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        """
        pass

    def event_end_step(self, time_passed):
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

        Called when the value of an alarm reaches 0.

        Arguments:

        - ``alarm_id`` -- The unique identifier of the alarm which was
          set off.

        """
        pass

    def event_animation_end(self):
        """Animation End event.

        Called when an animation cycle ends.

        """
        pass

    def event_key_press(self, key, char):
        """Key press event.

        See the documentation for :meth:`sge.Game.event_key_press` for
        more information.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        See the documentation for :meth:`sge.Game.event_key_release` for
        more information.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        See the documentation for :meth:`sge.Game.event_mouse_move` for
        more information.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_press` for more information.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_release` for more
        information.

        """
        pass

    def event_joystick_axis_move(self, name, ID, axis, value):
        """Joystick axis move event.

        See the documentation for
        :meth:`sge.Game.event_joystick_axis_move` for more information.

        """
        pass

    def event_joystick_hat_move(self, name, ID, hat, x, y):
        """Joystick HAT move event.

        See the documentation for
        :meth:`sge.Game.event_joystick_hat_move` for more information.

        """
        pass

    def event_joystick_trackball_move(self, name, ID, ball, x, y):
        """Joystick trackball move event.

        See the documentation for
        :meth:`sge.Game.event_joystick_trackball_move` for more
        information.

        """
        pass

    def event_joystick_button_press(self, name, ID, button):
        """Joystick button press event.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_press` for more
        information.

        """
        pass

    def event_joystick_button_release(self, name, ID, button):
        """Joystick button release event.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_release` for more
        information.

        """
        pass

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

    def event_inactive_step(self, time_passed):
        """Step event when this object is inactive.

        See the documentation for :meth:`sge.StellarClass.event_step`
        for more information.  The object is considered to be inactive
        when :attr:`active` is :attr:`False`.

        """
        pass

    def event_inactive_end_step(self, time_passed):
        """End step event when this object is inactive.

        See the documentation for
        :meth:`sge.StellarClass.event_end_step` for more information.
        The object is considered to be inactive when :attr:`active` is
        :attr:`False`.

        """
        pass

    def event_inactive_key_press(self, key, char):
        """Key press event when this object is inactive.

        See the documentation for :meth:`sge.Game.event_key_press` for
        more information.  The object is considered to be inactive when
        :attr:`active` is :const:`False`.

        """
        pass

    def event_inactive_key_release(self, key):
        """Key release event when this object is inactive.

        See the documentation for :meth:`sge.Game.event_key_release` for
        more information.  The object is considered to be inactive when
        :attr:`active` is :attr:`False`.

        """
        pass

    def event_inactive_mouse_move(self, x, y):
        """Mouse move event when this object is inactive.

        See the documentation for :meth:`sge.Game.event_mouse_move` for
        more information.  The object is considered to be inactive when
        :attr:`active` is :attr:`False`.

        """
        pass

    def event_inactive_mouse_button_press(self, button):
        """Mouse button press event when this object is inactive.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_press` for more information.
        The object is considered to be inactive when :attr:`active` is
        :attr:`False`.

        """
        pass

    def event_inactive_mouse_button_release(self, button):
        """Mouse button release event when this object is inactive.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_release` for more
        information.  The object is considered to be inactive when
        :attr:`active` is :attr:`False`.

        """
        pass

    def event_inactive_joystick_axis_move(self, name, ID, axis, value):
        """Joystick axis move event when this object is inactive.

        See the documentation for
        :meth:`sge.Game.event_joystick_axis_move` for more information.
        The object is considered to be inactive when :attr:`active` is
        :attr:`False`.

        """
        pass

    def event_inactive_joystick_hat_move(self, name, ID, hat, x, y):
        """Joystick HAT move event when this object is inactive.

        See the documentation for
        :meth:`sge.Game.event_joystick_hat_move` for more information.
        The object is considered to be inactive when :attr:`active` is
        :attr:`False`.

        """
        pass

    def event_inactive_joystick_trackball_move(self, name, ID, ball, x, y):
        """Joystick trackball move event when this object is inactive.

        See the documentation for
        :meth:`sge.Game.event_joystick_trackball_move` for more
        information.  The object is considered to be inactive when
        :attr:`active` is :attr:`False`.

        """
        pass

    def event_inactive_joystick_button_press(self, name, ID, button):
        """Joystick button press event when this object is inactive.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_press` for more
        information.  The object is considered to be inactive when
        :attr:`active` is :attr:`False`.

        """
        pass

    def event_inactive_joystick_button_release(self, name, ID, button):
        """Joystick button release event when this object is inactive.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_release` for more
        information.  The object is considered to be inactive when
        :attr:`active` is :attr:`False`.

        """
        pass

    def event_paused_key_press(self, key, char):
        """Key press event when paused.

        See the documentation for :meth:`sge.Game.event_key_press` for
        more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See the documentation for :meth:`sge.Game.event_key_release` for
        more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See the documentation for :meth:`sge.Game.event_mouse_move` for
        more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_press` for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_release` for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, name, ID, axis, value):
        """Joystick axis move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_axis_move` for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, name, ID, hat, x, y):
        """Joystick HAT move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_hat_move` for more information.

        """
        pass

    def event_paused_joystick_trackball_move(self, name, ID, ball, x, y):
        """Joystick trackball move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_trackball_move` for more
        information.

        """
        pass

    def event_paused_joystick_button_press(self, name, ID, button):
        """Joystick button press event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_press` for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, name, ID, button):
        """Joystick button release event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_release` for more
        information.

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
        for a in self._alarms:
            self._alarms[a] -= delta_mult
            if self._alarms[a] <= 0:
                del self._alarms[a]
                self.event_alarm(a)

        # Movement
        if self.xvelocity or self.yvelocity:
            if self.id != "mouse":
                self.x += self.xvelocity * delta_mult
                self.y += self.yvelocity * delta_mult

        room = sge.game.current_room
        area_size = room._collision_area_size
        areas_x_start = int(self.bbox_left / area_size)
        areas_x_num = math.ceil(self.bbox_width / area_size) + 1
        areas_y_start = int(self.bbox_top / area_size)
        areas_y_num = math.ceil(self.bbox_height / area_size) + 1

        my_areas = []
        for i in range(areas_x_start, areas_x_start + areas_x_num):
            for j in range(areas_y_start, areas_y_start + areas_y_num):
                if (i >= 0 and j >= 0 and room._collision_areas and
                        i < len(room._collision_areas) and
                        j < len(room._collision_areas[0])):
                    my_areas.append((i, j))
                elif None not in my_areas:
                    my_areas.append(None)

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

    def _detect_collisions(self):
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

            if self.collides(other):
                self_prev_bbox_left = self.xprevious + self.bbox_x
                self_prev_bbox_right = self_prev_bbox_left + self.bbox_width
                self_prev_bbox_top = self.yprevious + self.bbox_y
                self_prev_bbox_bottom = self_prev_bbox_top + self.bbox_height
                other_prev_bbox_left = other.xprevious + other.bbox_x
                other_prev_bbox_right = other_prev_bbox_left + other.bbox_width
                other_prev_bbox_top = other.yprevious + other.bbox_y
                other_prev_bbox_bottom = other_prev_bbox_top + other.bbox_height

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

    def _set_mask(self):
        # Properly set the hit mask based on the collision settings.
        if self.collision_precise:
            # Mask based on opacity of the current image.
            left = self.bbox_x + self.sprite.origin_x
            right = left + self.bbox_width
            top = self.bbox_y + self.sprite.origin_y
            bottom = top + self.bbox_height

            mask = self.sprite._get_precise_mask(self.image_index)[left:right]
            for i in range(len(mask)):
                mask[i] = mask[i][top:bottom]

            self._hitmask = mask
        elif self.collision_ellipse:
            # Elliptical mask based on bounding box.
            self._hitmask = [[False for y in range(self.bbox_height)]
                             for x in range(self.bbox_width)]
            a = len(self._hitmask) / 2
            b = len(self._hitmask[0]) / 2
            for x in range(len(self._hitmask)):
                for y in range(len(self._hitmask[x])):
                    if ((x - a) / a) ** 2 + ((y - b) / b) ** 2 <= 1:
                        self._hitmask[x][y] = True
        else:
            # Mask is all pixels in the bounding box.
            self._hitmask = [[True for y in range(self.bbox_height)]
                             for x in range(self.bbox_width)]

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
        if sge.DEBUG:
            print("mouse.visible has been set to:", value)

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
            x = (self.mouse_x / sge.game._xscale) - self.sprite.origin_x
            y = (self.mouse_y / sge.game._yscale) - self.sprite.origin_y
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
        super().__init__(*groups)
        self.parent = weakref.ref(parent)
        self.image = pygame.Surface((1, 1))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x_offset = 0
        self.y_offset = 0

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

                    w, h = self.image.get_size()

                    nw, nh = parent.sprite._get_image(
                        parent.image_index, parent.image_xscale,
                        parent.image_yscale).get_size()

                    self.x_offset, self.y_offset = _get_rotation_offset(
                        parent.sprite.origin_x, parent.sprite.origin_y,
                        parent.image_rotation, w, h, nw, nh)

                if self.visible != self.parent().visible:
                    self.visible = int(self.parent().visible)
                    self.dirty = 1

                self.update_rect(parent.x, parent.y, parent.z, parent.sprite,
                                 parent.image_xscale, parent.image_yscale)
            else:
                self.image = pygame.Surface((1, 1))
                self.image.set_colorkey((0, 0, 0))
                self.dirty = 1
        else:
            self.kill()

    def update_rect(self, x, y, z, sprite, image_xscale, image_yscale):
        # Update the rect of this Pygame sprite, based on the SGE sprite
        # and coordinates given.  This involves creating "proxy"
        # one-time sprites for multiple views if necessary.
        views = sge.game.current_room.views

        if image_xscale >= 0:
            origin_x = sprite.origin_x * abs(image_xscale)
        else:
            origin_x = (sprite.width - sprite.origin_x) * abs(image_xscale)

        if image_yscale >= 0:
            origin_y = sprite.origin_y * abs(image_yscale)
        else:
            origin_y = (sprite.height - sprite.origin_y) * abs(image_yscale)

        if (len(views) == 1 and views[0].xport == 0 and views[0].yport == 0 and
                views[0].width == sge.game.width and
                views[0].height == sge.game.height):
            # There is only one view that takes up the whole screen, so
            # we don't need to worry about it.
            x = x - views[0].x - origin_x
            y = y - views[0].y - origin_y
            new_rect = self.image.get_rect()
            new_rect.left = (round(x * sge.game._xscale) - self.x_offset +
                             sge.game._x)
            new_rect.top = (round(y * sge.game._yscale) - self.y_offset +
                            sge.game._y)

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
                new_rect.left = (round(x * sge.game._xscale) - self.x_offset +
                                 sge.game._x)
                new_rect.top = (round(y * sge.game._yscale) - self.y_offset +
                                sge.game._y)
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

                        x = (sge.game._x +
                             round((x - self.x_offset) * sge.game._xscale))
                        y = (sge.game._y +
                             round((y - self.y_offset) * sge.game._yscale))
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
        self.sprite = sprite
        self.image_index = image_index
        self.image = sprite._get_image(image_index)
        self.rect = self.image.get_rect()
        self.x_offset = 0
        self.y_offset = 0

    def update(self):
        if self.dirty:
            self.image = self.sprite._get_image(self.image_index)
            self.update_rect(self.x, self.y, self.z, self.sprite, 50, 50)
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
        super().__init__(*groups)
        self.image = image
        self.rect = rect
        self.dirty = 1

    def update(self):
        if not self.dirty:
            self.kill()


def _get_rotation_offset(origin_x, origin_y, rotation, image_width,
                         image_height, image_width_normal,
                         image_height_normal):
    # Return what to offset an origin when the object is rotated as a
    # two-part tuple: (x_offset, y_offset)
    x_offset = 0
    y_offset = 0

    if rotation % 180:
        # Adjust offset for the borders getting bigger.
        x_offset += (image_width - image_width_normal) / 2
        y_offset += (image_height - image_height_normal) / 2

    if rotation % 360:
        # Rotate about the origin
        center_x = image_width_normal / 2
        center_y = image_height_normal / 2
        xorig = origin_x - center_x
        yorig = origin_y - center_y
        start_angle = math.atan2(-yorig, xorig)
        radius = math.hypot(xorig, yorig)
        new_angle = start_angle + math.radians(rotation)
        new_center_x = origin_x + radius * math.cos(new_angle)
        new_center_y = origin_y - radius * math.sin(new_angle)
        x_offset += new_center_x + center_x
        y_offset += new_center_y + center_y

    return (x_offset, y_offset)
