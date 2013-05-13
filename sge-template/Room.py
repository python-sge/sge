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


__all__ = ['Room']


class Room(object):

    """Class for rooms.

    All Room objects have the following attributes:
        width: The width of the room in pixels.  If set to None,
            ``sge.game.width`` is used.
        height: The height of the room in pixels.  If set to None,
            ``sge.game.height`` is used.
        views: A list containing all View objects in the room.
        background: The Background object used.  While it will always be
            the actual object when read, it can be set to either an
            actual background object or the ID of a background.

    The following read-only attributes are also available:
        objects: A tuple containing all StellarClass objects in the
            room.
        room_number: The index of this room in the game, where 0 is the
            first room, or None if this room has not been added to a
            game.

    Room methods:
        add: Add a StellarClass object to the room.
        start: Start the room.
        resume: Continue the room from where it left off.
        end: Go to the next room.

    Room events are handled by special methods.  The exact timing of
    their calling is implementation-dependent except where otherwise
    noted.  The methods are:
        event_room_start: Called when the room starts.  It is always
            called after any game start events and before any object
            create events occurring at the same time.
        event_room_end: Called when the room ends.  It is always called
            before any game end events occurring at the same time.
        event_step: Called once each frame.
        event_key_press: Key press event.
        event_key_release: Key release event.
        event_mouse_move: Mouse move event.
        event_mouse_button_press: Mouse button press event.
        event_mouse_button_release: Mouse button release event.
        event_joystick_axis_move: Joystick axis move event.
        event_joystick_hat_move: Joystick HAT move event.
        event_joystick_button_press: Joystick button press event.
        event_joystick_button_release: Joystick button release event.
        event_close: Close event (e.g. close button).  It is always
            called before any game close events occurring at the same
            time.
        event_room_end: Called when the room ends.  It is always called
            before any game end events occurring at the same time.

    The following alternative events are executed when the game is
    paused in place of the corresponding normal events:
        event_paused_key_press
        event_paused_key_release
        event_paused_mouse_move
        event_paused_mouse_button_press
        event_paused_mouse_button_release
        event_paused_joystick_axis_move
        event_paused_joystick_hat_move
        event_paused_joystick_button_press
        event_paused_joystick_button_release
        event_paused_close

    """

    def __init__(self, objects=(), width=None, height=None, views=None,
                 background=None):
        """Create a new Room object.

        Arguments set the properties of the room.  See Room.__doc__ for
        more information.

        If ``views`` is set to None, a new view will be created with
        x=0, y=0, and all other arguments unspecified, which will become
        the first view of the room.  If ``background`` is set to None, a
        new background is created with no layers and the color set to
        "black".

        In addition to containing actual StellarClass objects,
        ``objects`` can contain valid IDs of StellarClass objects.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def add(self, obj):
        """Add a StellarClass object to the room.

        ``obj`` is the StellarClass object to add.  It can also be an
        object's ID.

        """
        # TODO

    def start(self):
        """Start the room.

        If the room has been changed, reset it to its original state.

        """
        # TODO

    def resume(self):
        """Continue the room from where it left off.

        If the room is unchanged (e.g. has not been started yet), this
        method behaves in the same way that Room.start does.

        """
        # TODO

    def end(self, next_room=None, resume=True):
        """End the current room.

        ``next_room`` indicates the room number of the room to go to
        next; if set to None, the room after this one is chosen.
        ``resume`` indicates whether or not to resume the next room
        instead of restarting it.  If the room chosen as the next room
        does not exist, the game is ended.

        This triggers this room's ``event_room_end`` and resets the
        state of this room.

        """
        # TODO

    def project_dot(self, x, y, z, color):
        """Project a single-pizel dot onto the room.

        ``x`` and ``y`` indicate the location in the room to project the
        dot.  ``z`` indicates the Z-axis position of the projection in
        the room.  ``color`` indicates the color of the dot.

        """
        # TODO

    def project_line(self, x1, y1, x2, y2, z, color, thickness=1,
                     anti_alias=False):
        """Project a line segment onto the room.

        ``x1``, ``y1``, ``x2``, and ``y2`` indicate the location in the
        room of the points between which to project the line segment.
        ``z`` indicates the Z-axis position of the projection in the
        room.  ``color`` indicates the color of the line segment.
        ``thickness`` indicates the thickness of the line segment in
        pixels.  ``anti_alias`` indicates whether or not anti-aliasing
        should be used.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def project_rectangle(self, x, y, z, width, height, fill=None,
                          outline=None, outline_thickness=1):
        """Project a rectangle onto the room.

        ``x`` and ``y`` indicate the location in the room to position
        the top-left corner of the rectangle.  ``z`` indicates the
        Z-axis position of the projection in the room.  ``width`` and
        ``height`` indicate the size of the rectangle.  ``fill``
        indicates the color of the fill of the rectangle; set to None
        for no fill.  ``outline`` indicates the color of the outline of
        the rectangle; set to None for no outline.
        ``outline_thickness`` indicates the thickness of the outline in
        pixels (ignored if there is no outline).

        """
        # TODO

    def project_ellipse(self, x, y, z, width, height, fill=None, outline=None,
                        outline_thickness=1, anti_alias=False):
        """Project an ellipse onto the room.

        ``x`` and ``y`` indicate the location in the room to position
        the top-left corner of the imaginary rectangle containing the
        ellipse.  ``z`` indicates the Z-axis position of the projection
        in the room.  ``width`` and ``height`` indicate the size of the
        ellipse.  ``fill`` indicates the color of the fill of the
        ellipse; set to None for no fill.  ``outline`` indicates the
        color of the outline of the ellipse; set to None for no outline.
        ``outline_thickness`` indicates the thickness of the outline in
        pixels (ignored if there is no outline).  ``anti_alias``
        indicates whether or not anti-aliasing should be used on the
        outline.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def project_circle(self, x, y, z, radius, fill=None, outline=None,
                       outline_thickness=1, anti_alias=False):
        """Project a circle onto the room.

        ``x`` and ``y`` indicate the location in the room to position
        the center of the circle.  ``z`` indicates the Z-axis position
        of the projection in the room.  ``radius`` indicates the radius
        of the circle in pixels.  ``fill`` indicates the color of the
        fill of the circle; set to None for no fill.  ``outline``
        indicates the color of the outline of the circle; set to None
        for no outline.  ``outline_thickness`` indicates the thickness
        of the outline in pixels (ignored if there is no outline).
        ``anti_alias`` indicates whether or not anti-aliasing should be
        used on the outline.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def project_sprite(self, sprite, image, x, y, z):
        """Project a sprite onto the room.

        ``sprite`` indicates the sprite to draw.  ``image`` indicates
        the frame of the sprite to draw, where 0 is the first frame.
        ``x`` and ``y`` indicate the location in the room to position
        the sprite.  ``z`` indicates the Z-axis position of the
        projection in the room.

        """
        # TODO

    def project_text(self, font, text, x, y, z, width=None, height=None,
                    color="black", halign=sge.ALIGN_LEFT, valign=sge.ALIGN_TOP,
                    anti_alias=True):
        """Project text onto the room.

        ``font`` indicates the font to use for the text.  ``text``
        indicates the text to project.  ``x`` and ``y`` indicate the
        location in the room to project the text.  ``width`` and
        ``height`` indicate the size of the imaginary box the text is
        projected in; set to None for no imaginary box.  ``color``
        indicates the color of the text.  ``halign`` indicates the
        horizontal alignment of the text and can be ALIGN_LEFT,
        ALIGN_CENTER, or ALIGN_RIGHT.  ``valign`` indicates the vertical
        alignment and can be ALIGN_TOP, ALIGN_MIDDLE, or ALIGN_BOTTOM.
        ``anti_alias`` indicates whether or not anti-aliasing should be
        used.

        If the text does not fit into the imaginary box specified, the
        text that doesn't fit will be cut off at the bottom if valign is
        ALIGN_TOP, the top if valign is ALIGN_BOTTOM, or equally the top
        and bottom if valign is ALIGN_MIDDLE.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is False.

        """
        # TODO

    def event_room_start(self):
        """Room start event.

        Called when the room starts.  It is always called after any game
        start events and before any object create events occurring at
        the same time.

        """
        pass

    def event_room_end(self):
        """Room end event.

        Called when the room ends.  It is always called before any game
        end events occurring at the same time.

        """
        pass

    def event_step(self, time_passed):
        """Room step event.

        Called once each frame.  ``time_passed`` is the number of
        milliseconds that have passed during the last frame. 

        """
        pass

    def event_key_press(self, key):
        """Key press event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        ``x`` and ``y`` indicate the relative movement of the mouse.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        ``button`` is the number of the mouse button that was pressed;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        ``button`` is the number of the mouse button that was released;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``axis`` is the number of the axis, where 0 is the
        first axis.  ``value`` is the tilt of the axis, where 0 is in
        the center, -1 is tilted all the way to the left or up, and 1 is
        tilted all the way to the right or down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``hat`` is the number of the HAT, where 0 is the
        first HAT.  ``x`` and ``y`` indicate the position of the HAT,
        where 0 is in the center, -1 is left or up, and 1 is right or
        down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_close(self):
        """Close event (e.g. close button).

        It is always called before any game close events occurring at
        the same time.

        """
        pass

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See Room.event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See Room.event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See Room.event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See Room.event_mouse_button_press.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See Room.event_mouse_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See Room.event_joystick_axis_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See Room.event_joystick_hat_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See Room.event_joystick_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See Room.event_joystick_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_close(self):
        """Close event (e.g. close button) when paused.

        See Room.event_close.__doc__ for more information.

        """
        pass
