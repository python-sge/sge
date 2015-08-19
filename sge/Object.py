# The SGE Specification
# Written in 2012, 2013, 2014, 2015 by Julian Marchant <onpon4@riseup.net> 
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

import math

import sge


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
        # TODO

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

    # TODO: This class is not technically required, but it's easier to
    # implement the Game.mouse attribute this way.  Because users are
    # not supposed to use this class (it is only to be used internally),
    # there are no docs for it and it doesn't have to behave a certain
    # way.  See Game.__doc__ for more information about how the
    # Game.mouse attribute should behave.

    def event_collision(self, other, xdirection, ydirection):
        game.event_mouse_collision(other, xdirection, ydirection)
