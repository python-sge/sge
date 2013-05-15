# Stellar Game Engine Template
# Copyright (C) 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


__all__ = ['StellarClass', 'Mouse']


class StellarClass(object):

    """Class for game objects.

    All StellarClass objects have the following attributes:
        x: The horizontal position of the object in the room, where the
            left edge is 0 and x increases toward the right.
        y: The vertical position of the object in the room, where the
            top edge is 0 and y increases toward the bottom.
        z: The Z-axis position of the object in the room, which
            determines in what order objects are drawn; objects with a
            higher Z value are drawn in front of objects with a lower Z
            value.
        sprite: The sprite currently in use by this object.  Set to None
            for no (visible) sprite.  While it will always be an actual
            Sprite object or None when read, it can also be set to the
            ID of a sprite.
        visible: Whether or not the object should be drawn.
        detects_collisions: Whether or not the object should be involved
            in collisions.
        bbox_x: The horizontal location of the top-left corner of the
            bounding box in relation to x, where 0 is x and bbox_x
            increases toward the right.  If set to None, the value
            recommended by the sprite is used.
        bbox_y: The vertical location of the top-left corner of the
            bounding box in relation to y, where 0 is y and bbox_y
            increases toward the bottom.  If set to None, the value
            recommended by the sprite is used.
        bbox_width: The width of the bounding box in pixels.  If set to
            None, the value recommended by the sprite is used.
        bbox_height: The height of the bounding box in pixels.  If set
            to None, the value recommended by the sprite is used.
        collision_ellipse: Whether or not an ellipse (rather than a
            rectangle) should be used for collision detection.
        collision_precise: Whether or not precise (pixel-perfect)
            collision detection should be used.
        bbox_left: The position of the left side of the bounding box in
            the room (same as x + bbox_x).
        bbox_right: The position of the right side of the bounding box
            in the room (same as bbox_left + bbox_width).
        bbox_top: The position of the top side of the bounding box
            (same as y + bbox_y).
        bbox_bottom: The position of the bottom side of the bounding
            box (same as bbox_top + bbox_height).
        xvelocity: The velocity of the object toward the right.
        yvelocity: The velocity of the object toward the bottom.
        speed: The total (directional) speed of the object.
        move_direction: The direction of the object's movement in
            degrees, with 0 being directly to the right and rotation in
            a positive direction being counter-clockwise.  Default is 0.
        image_index: The animation frame currently being displayed, with
            0 being the first one.
        image_fps: The animation rate in frames per second.  If set to
            None, the value recommended by the sprite is used.
        image_xscale: The horizontal scale factor for the sprite.
        image_yscale: The vertical scale factor for the sprite.
        image_rotation: The rotation of the sprite, with rotation in a
            positive direction being counter-clockwise.
        image_alpha: The alpha value applied to the entire image, where
            255 is the original image, 128 is half the opacity of the
            original image, 0 is fully transparent, etc.
        image_blend: The color to blend with the sprite.  Set to None
            for no color blending.

    The following read-only attributes are also available:
        id: The unique identifier for this object.
        xstart: The initial value of x when the object was created.
        ystart: The initial value of y when the object was created.
        xprevious: The previous value of x.
        yprevious: The previous value of y.

    StellarClass methods:
        collides: Return whether or not this object collides with
            another.
        set_alarm: Set an alarm.
        get_alarm: Return the count on an alarm.
        destroy: Destroy the object.

    StellarClass events are handled by special methods.  The exact
    timing of their calling is implementation-dependent except where
    otherwise noted.  The methods are:
        event_create: Called when the object is created.  It is always
            called after any room start events occurring at the same
            time.
        event_destroy: Destroy event.
        event_step: Called once each frame.
        event_alarm: Called when an alarm counter reaches 0.
        event_animation_end: Called when an animation cycle ends.
        event_key_press: Key press event.
        event_key_release: Key release event.
        event_mouse_move: Mouse move event.
        event_mouse_button_press: Mouse button press event.
        event_mouse_button_release: Mouse button release event.
        event_joystick_axis_move: Joystick axis move event.
        event_joystick_hat_move: Joystick HAT move event.
        event_joystick_trackball_move: Joystick trackball move event.
        event_joystick_button_press: Joystick button press event.
        event_joystick_button_release: Joystick button release event.
        event_collision: Middle/default collision event.
        event_collision_left: Left collision event.
        event_collision_right: Right collision event.
        event_collision_top: Top collision event.
        event_collision_bottom: Bottom collision event.

    The following alternative events are executed when the game is
    paused in place of the corresponding normal events:
        event_paused_key_press
        event_paused_key_release
        event_paused_mouse_move
        event_paused_mouse_button_press
        event_paused_mouse_button_release
        event_paused_joystick_axis_move
        event_paused_joystick_hat_move
        event_paused_joystick_trackball_move
        event_paused_joystick_button_press
        event_paused_joystick_button_release

    """

    def __init__(self, x, y, z, id_=None, sprite=None, visible=True,
                 detects_collisions=True, bbox_x=None, bbox_y=None,
                 bbox_width=None, bbox_height=None, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_fps=0, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None,
                 **kwargs):
        """Create a new StellarClass object.

        Arguments set the properties of the object.  See
        StellarClass.__doc__ for more information.

        If bbox_x, bbox_y, bbox_width, or bbox_height is None, the
        respective argument will be determined by the sprite's suggested
        bounding box.

        If ``id`` is None, it will be set to an integer not currently
        used as an ID (the exact number chosen is implementation-
        specific and may not necessarily be the same between runs).

        A game object must exist before an object of this class is
        created.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        # TODO

    def collides(self, other, x=None, y=None):
        """Return whether or not this object collides with another.

        ``other`` indicates the object to check for a collision with, or
        the name of said object.  ``other`` can also be a class to check
        for collisions with.

        ``x`` and ``y`` indicate the position to check for collisions
        at.  If unspecified or None, this object's current position will
        be used.

        """
        # TODO

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Set the alarm with the given ``alarm_id`` with the given
        ``value``.  The alarm will then reduce by 1 each frame until it
        reaches 0 and set off the alarm event with the same ID.
        ``alarm_id`` can be any value.  ``value`` should be a number
        greater than 0.  You can also set ``value`` to None to disable
        the alarm.

        """
        # TODO

    def get_alarm(self, alarm_id):
        """Return the count on an alarm.

        Get the number of frames before the alarm with ``alarm_id`` will
        go off.  If the alarm has not been set, None will be returned.

        """
        # TODO

    def destroy(self):
        """Destroy the object."""
        # TODO

    def event_create(self):
        """Create event.

        Called when the object is created.  It is always called after
        any room start events occurring at the same time.

        """
        pass

    def event_destroy(self):
        """Destroy event."""
        pass

    def event_step(self, time_passed):
        """Step event.

        See the documentation for sge.Game.event_step for more
        information.

        """
        pass

    def event_alarm(self, alarm_id):
        """Alarm event.

        Called when an alarm counter reaches 0.  ``alarm_id`` is the ID
        of the alarm that was set off.

        """
        pass

    def event_animation_end(self):
        """Animation End event.

        Called when an animation cycle ends.

        """
        pass

    def event_key_press(self, key):
        """Key press event.

        See the documentation for sge.Game.event_key_press for more
        information.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        See the documentation for sge.Game.event_key_release for more
        information.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        See the documentation for sge.Game.event_mouse_move for more
        information.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        See the documentation for sge.Game.event_mouse_button_press for
        more information.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        See the documentation for sge.Game.event_mouse_button_release
        for more information.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        See the documentation for sge.Game.event_joystick_axis_move for
        more information.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        See the documentation for sge.Game.event_joystick_hat_move for
        more information.

        """
        pass

    def event_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event.

        See the documentation for sge.Game.event_joystick_trackball_move
        for more information.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        See the documentation for sge.Game.event_joystick_button_press
        for more information.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        See the documentation for sge.Game.event_joystick_button_release
        for more information.

        """
        pass

    def event_collision(self, other):
        """Middle/default collision event."""
        pass

    def event_collision_left(self, other):
        """Left collision event."""
        self.event_collision(other)

    def event_collision_right(self, other):
        """Right collision event."""
        self.event_collision(other)

    def event_collision_top(self, other):
        """Top collision event."""
        self.event_collision(other)

    def event_collision_bottom(self, other):
        """Bottom collision event."""
        self.event_collision(other)

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See the documentation for sge.Game.event_key_press for more
        information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See the documentation for sge.Game.event_key_release for more
        information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See the documentation for sge.Game.event_mouse_move for more
        information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See the documentation for sge.Game.event_mouse_button_press for
        more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See the documentation for sge.Game.event_mouse_button_release
        for more information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See the documentation for sge.Game.event_joystick_axis_move for
        more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See the documentation for sge.Game.event_joystick_hat_move for
        more information.

        """
        pass

    def event_paused_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event when paused.

        See the documentation for sge.Game.event_joystick_trackball_move
        for more information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See the documentation for sge.Game.event_joystick_button_press
        for more information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See the documentation for sge.Game.event_joystick_button_release
        for more information.

        """
        pass

    @classmethod
    def create(cls, *args, **kwargs):
        """Create an object of this class in the current room and return
        the object created.

        ``args`` and ``kwargs`` are passed to ``cls`` as arguments.
        Calling this class method is the same as:
            obj = cls(*args, **kwargs)
            sge.game.current_room.add(obj)
            return obj

        """
        obj = cls(*args, **kwargs)
        sge.game.current_room.add(obj)
        return obj


class Mouse(StellarClass):

    # TODO: This class is not technically required, but it's easier to
    # implement the Game.mouse attribute this way.  Because users are
    # not supposed to use this class (it is only to be used internally),
    # there are no docs for it and it doesn't have to behave a certain
    # way.  See Game.__doc__ for more information about how the
    # Game.mouse attribute should behave.

    def event_collision(self, other):
        game.event_mouse_collision(other)

    def event_collision_left(self, other):
        game.event_mouse_collision_left(other)

    def event_collision_right(self, other):
        game.event_mouse_collision_right(other)

    def event_collision_top(self, other):
        game.event_mouse_collision_top(other)

    def event_collision_bottom(self, other):
        game.event_mouse_collision_bottom(other)
