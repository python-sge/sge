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
# Apache License.

import sge


class Object(object):

    """Class for game objects.

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
       automatic functionality and normal events will be disabled and
       events which have names starting with ``event_inactive_`` will be
       executed instead of the corresponding normal events.

       .. note::

          Inactive :class:`sge.Object` objects are still visible
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

    def __init__(self, x, y, z=0, sprite=None, visible=True, active=True,
                 checks_collisions=True, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        """Constructor method.

        Arugments set the respective initial attributes of the object.
        See the documentation for :class:`sge.Object` for more
        information.

        """
        # TODO

    def collision(self, other=None, x=None, y=None):
        """Return a list of objects colliding with this object.

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
        # TODO

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        After this method is called, ``value`` will reduce by 1 each
        frame (adjusted for delta timing if it is enabled) until it
        reaches 0, at which point :meth:`sge.Object.event_alarm`
        will be executed with ``alarm_id``.

        See the documentation for :meth:`sge.Game.set_alarm` for more
        information.

        """
        # TODO

    def get_alarm(self, alarm_id):
        """Return the value of an alarm.

        See the documentation for :meth:`sge.Game.get_alarm` for more
        information.

        """
        # TODO

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
          event is called after the respective room start event.
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
        """Begin step event.

        This event is executed each frame before automatic updates to
        objects (such as the effects of the speed variables).

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        .. note::

           Automatic updates, the only occurances between this event and
           :meth:`sge.Object.event_step`, do not occur, so there
           is no need for an "inactive" variant of this event.  Use
           :meth:`sge.Object.event_inactive_step` instead.

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
        :meth:`sge.Object.event_collision`.

        """
        self.event_collision(other)

    def event_collision_right(self, other):
        """Right collision event.

        Called when another object collides with this object's right
        side.

        Arguments:
        
        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        :meth:`sge.Object.event_collision`.

        """
        self.event_collision(other)

    def event_collision_top(self, other):
        """Top collision event.

        Called when another object collides with this object's top side.

        Arguments:

        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        :meth:`sge.Object.event_collision`.

        """
        self.event_collision(other)

    def event_collision_bottom(self, other):
        """Bottom collision event.

        Called when another object collides with this object's bottom
        side.

        Arguments:

        - ``other`` -- The other object which was collided with.

        By default, this method simply calls
        :meth:`sge.Object.event_collision`.

        """
        self.event_collision(other)

    def event_inactive_step(self, time_passed, delta_mult):
        """Step event when this object is inactive.

        See the documentation for :meth:`sge.Object.event_step`
        for more information.  The object is considered to be inactive
        when :attr:`active` is :const:`False`.

        """
        pass

    def event_inactive_end_step(self, time_passed, delta_mult):
        """End step event when this object is inactive.

        See the documentation for
        :meth:`sge.Object.event_end_step` for more information.
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
