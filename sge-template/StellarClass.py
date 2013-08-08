# SGE Template
# Written in 2012, 2013 by Julian Marchant <onpon4@riseup.net> 
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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


__all__ = ['StellarClass', 'Mouse']


class StellarClass(object):

    """Class for game objects.

    This class is used for game objects, such as the player, enemies,
    bullets, and the HUD.  Generally, each type of object has its own
    subclass of `StellarClass`.

    One attribute which needs some explanation is ``active``.  This
    attribute indicates whether the object is active (``True``) or
    inactive (``False``).  While the object is active, it will exhibit
    normal behavior; events will be executed normally as will any other
    automatic functionality, such as adding ``xvelocity`` and
    ``yvelocity`` to ``x`` and ``y``.  If ``active`` is False, automatic
    functionality and normal events will be disabled and events which
    have names starting with "event_inactive_" will be executed instead
    of the corresponding normal events.

    It is important to recognize that making an object inactive is not
    like deactivating an instance in Game Maker.  Unlike deactivated
    instances in Game Maker, inactive `StellarClass` objects are still
    visible by default and continue to be involved in collisions.  In
    addition, collision events and destroy events still occur even if the
    object is inactive.  If you wish for the object to not be visible, set
    ``visible`` to False.  If you wish for the object to not be involved
    in collisions, set ``detects_collisions`` to False.

    It is also important to note that making an object inactive will not
    likely have a significant effect on performance.  For performance
    enhancement, it is far more effective to exclude objects from
    collision detection.  Object deactivation is meant to be used to
    easily maintain control over objects that are currently being excluded
    from collision detection (e.g. to prevent a gravity effect that would
    otherwise occur, or to prevent the object from moving through walls).

    Attributes:
    - ``x`` -- The horizontal position of the object in the room.
    - ``y`` -- The vertical position of the object in the room.
    - ``z`` -- The Z-axis position of the object in the room.
    - ``sprite`` -- The sprite currently in use by this object.  Set to
      None for no (visible) sprite.
    - ``visible`` -- Whether or not the object's sprite should be projected
      onto the screen.
    - ``active`` -- Whether or not the object should be active.  If this is
      False, all normal occurances (including events) will not execute.
      Only collision events, destroy events, and events with names that
      start with "event_inactive_" will be executed.
    - ``detects_collisions`` -- Whether or not the object should be involved
      in collision detection.  Setting this to False can improve
      performance if the object doesn't need to detect collisions.
    - ``bbox_x`` -- The horizontal location of the bounding box relative to
      the object's position.  If set to None, the value recommended by
      the sprite is used.
    - ``bbox_y`` -- The vertical location of the bounding box relative to the
      object's position.  If set to None, the value recommended by the
      sprite is used.
    - ``bbox_width`` -- The width of the bounding box in pixels.  If set to
      None, the value recommended by the sprite is used.
    - ``bbox_height`` -- The height of the bounding box in pixels.  If set to
      None, the value recommended by the sprite is used.
    - ``collision_ellipse`` -- Whether or not an ellipse (rather than a
      rectangle) should be used for collision detection.
    - ``collision_precise`` -- Whether or not precise (pixel-perfect)
      collision detection should be used.  Note that this can be
      inefficient and in some cases can lead to collision detection
      errors.
    - ``bbox_left`` -- The position of the left side of the bounding box in
      the room (same as x + bbox_x).
    - ``bbox_right`` -- The position of the right side of the bounding box in
      the room (same as bbox_left + bbox_width).
    - ``bbox_top`` -- The position of the top side of the bounding box in the
      room (same as y + bbox_y).
    - ``bbox_bottom`` -- The position of the bottom side of the bounding box
      in the room (same as bbox_top + bbox_height).
    - ``xvelocity`` -- The velocity of the object toward the right.
    - ``yvelocity`` -- The velocity of the object toward the bottom.
    - ``speed`` -- The total (directional) speed of the object.
    - ``move_direction`` -- The direction of the object's movement in degrees,
      with 0 being directly to the right and rotation in a positive
      direction being counter-clockwise.  Default is 0.
    - ``image_index`` -- The animation frame currently being displayed, with 0
      being the first one.
    - ``image_fps`` -- The animation rate in frames per second.  If set to
      None, the value recommended by the sprite is used.
    - ``image_xscale`` -- The horizontal scale factor for the sprite.
    - ``image_yscale`` -- The vertical scale factor for the sprite.
    - ``image_rotation`` -- The rotation of the sprite in degrees, with
      rotation in a positive direction being counter-clockwise.
    - ``image_alpha`` -- The alpha value applied to the entire image, where
      255 is the original image, 128 is half the opacity of the original
      image, 0 is fully transparent, etc.
    - ``image_blend`` -- The color to blend with the sprite.  Set to None for
      no color blending.

    Read-Only Attributes:
    - ``id`` -- The unique identifier for this object.
    - ``xstart`` -- The initial value of x when the object was created.
    - ``ystart`` -- The initial value of y when the object was created.
    - ``xprevious`` -- The previous value of x.
    - ``yprevious`` -- The previous value of y.

    """

    def __init__(self, x, y, z=0, id_=None, sprite=None, visible=True,
                 active=True, detects_collisions=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 collision_ellipse=False, collision_precise=False,
                 xvelocity=0, yvelocity=0, image_index=0, image_fps=None,
                 image_xscale=1, image_yscale=1, image_rotation=0,
                 image_alpha=255, image_blend=None, **kwargs):
        """Create a new StellarClass object.

        Arguments:
        - ``id`` -- The unique identifier of the sound.  If set to None,
          ``fname`` minus the extension will be used, modified by SGE if
          it is already the unique identifier of another music object.

        All other arugments set the respective initial attributes of the
        object.  See the documentation for `StellarClass` for more
        information.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        # TODO

    def collides(self, other, x=None, y=None):
        """Return whether or not this object collides with another.

        Arguments:
        - ``other`` -- The object to check for a collision with, or the
          unique identifier of said object.  ``other`` can also be a
          class to check for collisions with.
        - ``x`` -- The horizontal position to pretend this object is at
          for the purpose of the collision detection.  If set to None,
          ``self.x`` will be used.
        - ``y`` -- The vertical position to pretend this object is at
          for the purpose of the collision detection.  If set to None,
          ``self.y`` will be used.

        """
        # TODO

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Arguments:
        - ``alarm_id`` -- The unique identifier of the alarm to set.
          Any value can be used as a unique identifier for an alarm.
        - ``value`` -- The value to set the alarm to.  Set to None to
          disable the alarm.

        After this method is called, ``value`` will reduce by 1 each
        frame (adjusted for delta timing if it is enabled) until it
        reaches 0, at which point `StellarClass.event_alarm` will be
        executed with ``alarm_id``.

        """
        # TODO

    def get_alarm(self, alarm_id):
        """Return the value of an alarm.

        - ``alarm_id`` -- The unique identifier of the alarm to check.

        If the alarm has not been set, None will be returned.

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

        See the documentation for `sge.Game.event_step` for more
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

        See the documentation for `sge.Game.event_key_press` for more
        information.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        See the documentation for `sge.Game.event_key_release` for more
        information.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        See the documentation for `sge.Game.event_mouse_move` for more
        information.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        See the documentation for `sge.Game.event_mouse_button_press`
        for more information.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        See the documentation for `sge.Game.event_mouse_button_release`
        for more information.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        See the documentation for `sge.Game.event_joystick_axis_move`
        for more information.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        See the documentation for `sge.Game.event_joystick_hat_move` for
        more information.

        """
        pass

    def event_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event.

        See the documentation for
        `sge.Game.event_joystick_trackball_move` for more information.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        See the documentation for `sge.Game.event_joystick_button_press`
        for more information.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        See the documentation for
        `sge.Game.event_joystick_button_release` for more information.

        """
        pass

    def event_collision(self, other):
        """Default collision event.

        Called when another object collides with this object and none of
        the directional collision events are appropriate.  In
        particular, this is called if the collision was already
        happening in the previous frame.  This is also the event method
        called by the directional collision event methodss by default.

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
        `StellarClass.event_collision`.

        """
        self.event_collision(other)

    def event_collision_right(self, other):
        """Right collision event.

        Called when another object collides with this object's right
        side.

        Arguments:
        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        `StellarClass.event_collision`.

        """
        self.event_collision(other)

    def event_collision_top(self, other):
        """Top collision event.

        Called when another object collides with this object's top side.

        Arguments:
        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        `StellarClass.event_collision`.

        """
        self.event_collision(other)

    def event_collision_bottom(self, other):
        """Bottom collision event.

        Called when another object collides with this object's bottom
        side.

        Arguments:
        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        `StellarClass.event_collision`.

        """
        self.event_collision(other)

    def event_inactive_step(self, time_passed):
        """Step event when this object is inactive.

        See the documentation for `sge.Game.event_step` for more
        information.  The object is considered to be inactive when its
        ``active`` attribute is False.

        """

    def event_inactive_key_press(self, key, char):
        """Key press event when this object is inactive.

        See the documentation for `sge.Game.event_key_press` for more
        information.  The object is considered to be inactive when its
        ``active`` attribute is False.

        """
        pass

    def event_inactive_key_release(self, key):
        """Key release event when this object is inactive.

        See the documentation for `sge.Game.event_key_release` for more
        information.  The object is considered to be inactive when its
        ``active`` attribute is False.

        """
        pass

    def event_inactive_mouse_move(self, x, y):
        """Mouse move event when this object is inactive.

        See the documentation for `sge.Game.event_mouse_move` for more
        information.  The object is considered to be inactive when its
        ``active`` attribute is False.

        """
        pass

    def event_inactive_mouse_button_press(self, button):
        """Mouse button press event when this object is inactive.

        See the documentation for `sge.Game.event_mouse_button_press`
        for more information.  The object is considered to be inactive
        when its ``active`` attribute is False.

        """
        pass

    def event_inactive_mouse_button_release(self, button):
        """Mouse button release event when this object is inactive.

        See the documentation for `sge.Game.event_mouse_button_release`
        for more information.  The object is considered to be inactive
        when its ``active`` attribute is False.

        """
        pass

    def event_inactive_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when this object is inactive.

        See the documentation for `sge.Game.event_joystick_axis_move`
        for more information.  The object is considered to be inactive
        when its ``active`` attribute is False.

        """
        pass

    def event_inactive_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when this object is inactive.

        See the documentation for `sge.Game.event_joystick_hat_move` for
        more information.  The object is considered to be inactive when
        its ``active`` attribute is False.

        """
        pass

    def event_inactive_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event when this object is inactive.

        See the documentation for
        `sge.Game.event_joystick_trackball_move` for more information.
        The object is considered to be inactive when its ``active``
        attribute is False.

        """
        pass

    def event_inactive_joystick_button_press(self, joystick, button):
        """Joystick button press event when this object is inactive.

        See the documentation for `sge.Game.event_joystick_button_press`
        for more information.  The object is considered to be inactive
        when its ``active`` attribute is False.

        """
        pass

    def event_inactive_joystick_button_release(self, joystick, button):
        """Joystick button release event when this object is inactive.

        See the documentation for
        `sge.Game.event_joystick_button_release` for more information.
        The object is considered to be inactive when its ``active``
        attribute is False.

        """
        pass

    def event_paused_key_press(self, key, char):
        """Key press event when paused.

        See the documentation for `sge.Game.event_key_press` for more
        information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See the documentation for `sge.Game.event_key_release` for more
        information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See the documentation for `sge.Game.event_mouse_move` for more
        information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See the documentation for `sge.Game.event_mouse_button_press`
        for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See the documentation for `sge.Game.event_mouse_button_release`
        for more information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See the documentation for `sge.Game.event_joystick_axis_move`
        for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See the documentation for `sge.Game.event_joystick_hat_move` for
        more information.

        """
        pass

    def event_paused_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event when paused.

        See the documentation for
        `sge.Game.event_joystick_trackball_move` for more information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See the documentation for `sge.Game.event_joystick_button_press`
        for more information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See the documentation for
        `sge.Game.event_joystick_button_release` for more information.

        """
        pass

    @classmethod
    def create(cls, *args, **kwargs):
        """Create an object of this class in the current room it.

        ``args`` and ``kwargs`` are passed to ``cls.__init__`` as
        arguments.  Calling ``obj = cls.create(*args, **kwargs)`` is the
        same as:::

            obj = cls(*args, **kwargs)
            sge.game.current_room.add(obj)

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
