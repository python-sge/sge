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


__all__ = ['Game']


class Game(object):

    """Class which handles the game.

    A Game object must be created before anything else is done.

    All Game objects have the following attributes:
        width: The width of the game's display in pixels.
        height: The height of the game's display in pixels.
        fullscreen: True if the game should be in fullscreen, False
            otherwise.
        scale: A number indicating a fixed scale factor (e.g. 1 for no
            scaling, 2 for doubled size).  If set to 0, scaling is
            automatic (causes the game to fit the window or screen).
        scale_proportional: If set to True, scaling is always
            proportional.  If set to False, the image may be stretched
            to completely fill the game window or screen.  This has no
            effect unless ``scale`` is 0.
        scale_smooth: If set to True, a smooth scaling algorithm will be
            used, if available.  Otherwise, simple scaling (e.g. pixel
            doubling) will always be used.  Support for smooth scaling
            in Stellar Game Engine implementations is optional.  If the
            implementation used does not support smooth scaling, this
            option will always be treated as False.
        fps: The rate the game should run in frames per second.  Note
            that this is only the maximum; if the computer is not fast
            enough, the game may run more slowly.
        delta: If set to True, delta timing will be enabled, which
            adjusts speeds and animation rates if the game cannot run at
            the specified frame rate.
        delta_min: Delta timing can cause the game to be choppy.  This
            setting limits this by pretending that the frame rate is
            never lower than this amount, resulting in the game slowing
            down like normal if it is.
        grab_input: If set to True, all input will be locked into the
            game.
        window_text: The text for the OS to display as the window title,
            e.g. in the frame of the window.  If set to None, the
            implementation chooses the text.  Support for this feature
            in Stellar Game Engine implementations is optional.
        window_icon: The name of the image file to use as the window
            icon, to be located in one of the directories specified in
            ``sge.image_directories``.  If set to None, the
            implementation chooses the icon.  Support for this feature
            in Stellar Game Engine implementations is optional.

    The following read-only attributes are also available:
        sprites: A dictionary containing all loaded sprites, using their
            names as the keys.
        background_layers: A dictionary containing all loaded background
            layers, using their sprites' names as the keys.
        backgrounds: A dictionary containing all loaded backgrounds,
            using their unique identifiers as the keys.
        fonts: A dictionary containing all loaded fonts, using their
            names as the keys.
        sounds: A dictionary containing all loaded sounds, using their
            file names as the keys.
        music: A dictionary containing all loaded music, using their
            file names as the keys.
        objects: A dictionary containing all StellarClass objects in the
            game, using their unique identifiers as the keys.
        rooms: A list containing all rooms in order of their creation.
        current_room: The Room object which is currently active.
        mouse: A StellarClass object which represents the mouse cursor.
            Its ID is "mouse" and its bounding box is one pixel.
            Speed variables are determined by averaging all mouse
            movement during the last quarter of a second.  Assigning to
            its ``visible`` attribute controls whether or not the mouse
            cursor is shown.  Setting its sprite sets the mouse cursor.

    Game methods:
        start: Start the game at the first room.
        end: Properly end the game.
        pause: Pause the game.
        unpause: Unpause the game.

    Game events are handled by special methods.  The exact timing of
    their calling is implementation-dependent except where otherwise
    noted.  The methods are:
        event_game_start: Called when the game starts.  This is only
            called once (it is not called again when the game restarts)
            and it is always the first event method called.
        event_game_end: Called when the game ends.  This is only called
            once and it is always the last event method called.
        event_step: Called once each frame.
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
        event_close: Close event (e.g. close button).  It is always
            called after any room close events occurring at the same
            time.
        event_mouse_collision: Middle/default mouse collision event.
        event_mouse_collision_left: Left mouse collision event.
        event_mouse_collision_right: Right mouse collision event.
        event_mouse_collision_top: Top mouse collision event.
        event_mouse_collision_bottom: Bottom mouse collision event.

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
        event_paused_close

    """

    def __init__(self, width=640, height=480, fullscreen=False, scale=0,
                 scale_proportional=True, scale_smooth=False, fps=60,
                 delta=False, delta_min=15, grab_input=False,
                 window_text=None, window_icon=None):
        """Create a new Game object and assign it to ``game``.

        Arguments set the properties of the game.  See Game.__doc__ for
        more information.

        """
        # TODO

    def start(self):
        """Start the game at the first room.

        Can be called in the middle of a game to start the game over.
        If you do this, everything will be reset to its original state.

        """
        # TODO

    def end(self):
        """Properly end the game."""
        # TODO

    def pause(self, sprite=None):
        """Pause the game.

        ``sprite`` is the sprite to show when the game is paused.  If
        set to None, a default image will be shown.  The default image
        is at the discretion of the Stellar Game Engine implementation,
        as are any additional visual effects, with the stipulation that
        the following conditions are met:

            1. The default image must unambiguously demonstrate that the
                game is paused (the easiest way to do this is to include
                the word "paused" somewhere in the image).
            2. The view must stay in place.
            3. What was going on within the view before the game was
                paused must remain visible while the game is paused.

        While the game is paused, all game events will be halted.
        Events whose names start with "event_paused_" will occur during
        this time instead.

        """
        # TODO

    def unpause(self):
        """Unpause the game."""
        # TODO

    def event_game_start(self):
        """Game start event.

        Called when the game starts.  This is only called once (it is
        not called again when the game restarts) and it is always the
        first event method called.

        """
        pass

    def event_game_end(self):
        """Game end event.

        Called when the game ends.  This is only called once and it is
        always the last event method called.

        """
        pass

    def event_step(self, time_passed):
        """Global step event.

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

    def event_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event.

        ``joystick`` indicates the number of the joystick, where 0 is
        the first joystick.  ``ball`` indicates the number of the
        trackball, where 0 is the first trackball.  ``x`` and ``y``
        indicate the relative movement of the trackball.

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

        It is always called after any room close events occurring at the
        same time.

        """
        pass

    def event_mouse_collision(self, other):
        """Middle/default mouse collision event."""
        pass

    def event_mouse_collision_left(self, other):
        """Left mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_right(self, other):
        """Right mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_top(self, other):
        """Top mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_bottom(self, other):
        """Bottom mouse collision event."""
        self.event_mouse_collision(other)

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See Game.event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See Game.event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See Game.event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See Game.event_mouse_button_press.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See Game.event_mouse_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See Game.event_joystick_axis_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See Game.event_joystick_hat_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event when paused.

        See Game.event_joystick_trackball_move.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See Game.event_joystick_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See Game.event_joystick_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_close(self):
        """Close event (e.g. close button) when paused.

        See Game.event_close.__doc__ for more information.

        """
        pass
