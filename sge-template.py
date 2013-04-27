#!/usr/bin/env python

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

"""Stellar Game Engine - [insert implementation name here]

Stellar Game Engine is a library for Stellar.  It is a game engine
loosely based on Game Maker.

Except where otherwise noted, all documented features are required to be
offered by all implementations.  Any implementation failing to do so is
incomplete.

Constants:
    IMPLEMENTATION: A string identifying the how the engine is
        implemented (e.g. the name of the graphics library used).
    ALIGN_LEFT: Flag indicating alignment to the left.
    ALIGN_CENTER: Flag indicating alignment to the horizontal center.
    ALIGN_RIGHT: Flag indicating alignment to the right.
    ALIGN_TOP: Flag indicating alignment to the top.
    ALIGN_MIDDLE: Flag indicating alignment to the vertical middle.
    ALIGN_BOTTOM: Flag indicating alignment to the bottom.
    MOUSE_BUTTON_LEFT: The mouse button number which corresponds with
        the left mouse button.
    MOUSE_BUTTON_RIGHT: The mouse button number which corresponds with
        the right mouse button.
    MOUSE_BUTTON_MIDDLE: The mouse button number which corresponds with
        the middle mouse button.
    MOUSE_BUTTON_WHEEL_UP: The mouse button number which corresponds
        with rolling the mouse wheel up.
    MOUSE_BUTTON_WHEEL_DOWN: The mouse button number which corresponds
        with rolling the mouse wheel down.
    MOUSE_BUTTON_WHEEL_LEFT: The mouse button number which corresponds
        with tilting the mouse wheel to the left.
    MOUSE_BUTTON_WHEEL_RIGHT: The mouse button number which corresponds
        with tilting the mouse wheel to the right.

Global variables:
    game: Stores the current game.  If there is no game currently, this
        variable is set to None.
    image_directories: A list of directories where images can be found.
        Default is ./data/images, ./data/sprites, or ./data/backgrounds.
    font_directories: A list of directories where font files can be
        found.  Default is ./data/fonts.
    sound_directories: A list of directories where sounds can be found.
        Default is ./data/sounds.
    music_directories: A list of directories where music files can be
        found.  Default is ./data/music.

Classes:
    Game: Class which handles the game.
    Sprite: Class used to store images and animations.
    BackgroundLayer: Class used to store a background layer.
    Background: Class used to store parallax-scrolling backgrounds.
    Font: Class used to store and handle fonts.
    Sound: Class used to store and play sound effects.
    Music: Class used to store and play music.
    StellarClass: Class used for game objects.
    Room: Class used for game rooms, e.g. levels.
    View: Class used for views in rooms.

Functions:
    create_object: Create an object in the current room.
    sound_stop_all: Stop playback of all sounds.
    get_key_pressed: Return whether or not a given key is pressed.
    get_mouse_button_pressed: Return whether or not a given mouse
        button is pressed.
    get_joystick_axis: Return the position of the given axis.
    get_joystick_hat: Return the position of the given HAT.
    get_joystick_button_pressed: Return whether or not the given
        joystick button is pressed.
    get_joysticks: Return the number of joysticks available.
    get_joystick_axes: Return the number of axes on the given
        joystick.
    get_joystick_hats: Return the number of HATs on the given
        joystick.
    get_joystick_buttons: Return the number of buttons on the
        given joystick.

Implementation-specific information:
[insert info here]

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.0.42"

import sys
import os
import math

# Import implementation-specific libraries like Pygame here

__all__ = ['Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font', 'Sound',
           'Music', 'StellarClass', 'Room', 'View', 'game', 'ALIGN_LEFT',
           'ALIGN_CENTER', 'ALIGN_RIGHT', 'ALIGN_TOP', 'ALIGN_MIDDLE',
           'ALIGN_BOTTOM', 'create_object', 'sound_stop_all',
           'music_clear_queue', 'music_stop_all', 'get_key_pressed',
           'get_mouse_button_pressed', 'get_joystick_axis', 'get_joystick_hat',
           'get_joystick_button_pressed', 'get_joysticks', 'get_joystick_axes',
           'get_joystick_hats', 'get_joystick_buttons']
# Except in extreme cases, these constants should not be modified.
DEFAULT_SCREENWIDTH = 640
DEFAULT_SCREENHEIGHT = 480
DEFAULT_FULLSCREEN = False
DEFAULT_SCALE = 0
DEFAULT_SCALE_PROPORTIONAL = True
DEFAULT_SCALE_SMOOTH = False
DEFAULT_FPS = 60
DEFAULT_DELTA = False
DEFAULT_DELTA_MIN = 15
COLORS = {'white': '#ffffff', 'silver': '#c0c0c0', 'gray': '#808080',
          'black': '#000000', 'red': '#ff0000', 'maroon': '#800000',
          'yellow': '#ffff00', 'olive': '#808000', 'lime': '#00ff00',
          'green': '#008000', 'aqua': '#00ffff', 'teal': '#008080',
          'blue': '#0000ff', 'navy': '#000080', 'fuchsia': '#ff00ff',
          'purple': '#800080'}
COLORNAMES = {}
for pair in COLORS.items():
    COLORNAMES[pair[1]] = pair[0]

KEYS = {"0": None, "1": None, "2": None, "3": None, "4": None, "5": None, "6": None, "7": None, "8": None, "9": None, "a": None, "b": None, "c": None, "d": None, "e": None, "f": None, "g": None, "h": None, "i": None, "j": None, "k": None, "l": None, "m": None, "n": None, "o": None, "p": None, "q": None, "r": None, "s": None, "t": None, "u": None, "v": None, "w": None, "x": None, "y": None, "z": None, "alt_left": None, "alt_right": None, "ampersand": None, "apostrophe": None, "asterisk": None, "at": None, "backslash": None, "backspace": None, "backtick": None, "bracket_left": None, "bracket_right": None, "break": None, "caps_lock": None, "caret": None, "clear": None, "colon": None, "comma": None, "ctrl_left": None, "ctrl_right": None, "delete": None, "dollar": None, "down": None, "end": None, "enter": None, "equals": None, "escape": None, "euro": None, "exclamation": None, "f1": None, "f2": None, "f3": None, "f4": None, "f5": None, "f6": None, "f7": None, "f8": None, "f9": None, "f10": None, "f11": None, "f12": None, "greater_than": None, "hash": None, "help": None, "home": None, "hyphen": None, "insert": None, "kp_0": None, "kp_1": None, "kp_2": None, "kp_3": None, "kp_4": None, "kp_5": None, "kp_6": None, "kp_7": None, "kp_8": None, "kp_9": None, "kp_divide": None, "kp_enter": None, "kp_equals": None, "kp_minus": None, "kp_multiply": None, "kp_plus": None, "kp_point": None, "left": None, "less_than": None, "menu":None, "meta_left":None, "meta_right":None, "mode":None, "num_lock":None, "pagedown":None, "pageup":None, "parenthesis_left":None, "parenthesis_right":None, "pause":None, "period":None, "plus":None, "power":None, "print_screen":None, "question":None, "quote":None, "right":None, "scroll_lock":None, "semicolon":None, "shift_left":None, "shift_right":None, "slash":None, "space":None, "super_left":None, "super_right":None, "sysrq":None, "tab":None, "underscore":None, "up":None}
KEYNAMES = {}
for pair in KEYS.items():
    KEYNAMES[pair[1]] = pair[0]

IMPLEMENTATION = "Template"
ALIGN_LEFT = 2
ALIGN_CENTER = 3
ALIGN_RIGHT = 1
ALIGN_TOP = 8
ALIGN_MIDDLE = 12
ALIGN_BOTTOM = 4
MOUSE_BUTTON_LEFT = 0
MOUSE_BUTTON_RIGHT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_WHEEL_UP = 3
MOUSE_BUTTON_WHEEL_DOWN = 4
MOUSE_BUTTON_WHEEL_LEFT = 5
MOUSE_BUTTON_WHEEL_RIGHT = 6

# Global variables
game = None
image_directories = [os.path.join('data', 'images'),
                     os.path.join('data', 'sprites'),
                     os.path.join('data', 'backgrounds')]
font_directories = [os.path.join('data', 'fonts')]
sound_directories = [os.path.join('data', 'sounds')]
music_directories = [os.path.join('data', 'music')]


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
            called after any room close events occurring at the same
            time.
        event_mouse_collision: Middle/default mouse collision event.
        event_mouse_collision_left: Left mouse collision event.
        event_mouse_collision_right: Right mouse collision event.
        event_mouse_collision_top: Top mouse collision event.
        event_mouse_collision_bottom: Bottom mouse collision event.
        event_game_end: Called when the game ends.  This is only called
            once and it is always the last event method called.

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

    def __init__(self, width=DEFAULT_SCREENWIDTH, height=DEFAULT_SCREENHEIGHT,
                 fullscreen=DEFAULT_FULLSCREEN, scale=DEFAULT_SCALE,
                 scale_proportional=DEFAULT_SCALE_PROPORTIONAL,
                 scale_smooth=DEFAULT_SCALE_SMOOTH, fps=DEFAULT_FPS,
                 delta=DEFAULT_DELTA, delta_min=DEFAULT_DELTA_MIN):
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

    def event_game_end(self):
        """Game end event.

        Called when the game ends.  This is only called once and it is
        always the last event method called.

        """
        pass

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


class Sprite(object):

    """Class which holds information for images and animations.

    All Sprite objects have the following attributes:
        width: The width of the sprite in pixels.
        height: The height of the sprite in pixels.
        origin_x: The horizontal location of the origin (the pixel
            position in relation to the images to base rendering on),
            where the left edge of the image is 0 and origin_x increases
            toward the right.
        origin_y: The vertical location of the origin (the pixel
            position in relation to the images to base rendering on),
            where the top edge of the image is 0 and origin_y increases
            toward the bottom.
        transparent: True if the image should support transparency,
            False otherwise.  If the image does not have an alpha
            channel or if the implementation used does not support alpha
            transparency, a colorkey will be used, with the transparent
            color being the color of the top-rightmost pixel.
        fps: The suggested rate in frames per second to animate the
            image at.
        bbox_x: The horizontal location of the top-left corner of the
            suggested bounding box to use with this sprite, where
            origin_x is 0 and bbox_x increases toward the right.
        bbox_y: The vertical location of the top-left corner of the
            suggested bounding box to use with this sprite, where
            origin_y is 0 and bbox_y increases toward the bottom.
        bbox_width: The width of the suggested bounding box in pixels.
        bbox_height: The height of the suggested bounding box in pixels.

    The following read-only attributes are also available:
        name: The name of the sprite given when it was created.  See
            Sprite.__init__.__doc__ for more information.

    Sprite methods:
        draw_dot: Draw a single-pixel dot.
        draw_line: Draw a line segment between the given points.
        draw_rectangle: Draw a rectangle at the given position.
        draw_ellipse: Draw an ellipse at the given position.
        draw_circle: Draw a circle at the given position.
        draw_text: Draw the given text at the given position.
        draw_clear: Erase everything from the sprite.

    """

    def __init__(self, name=None, width=None, height=None, origin_x=0,
                 origin_y=0, transparent=True, fps=DEFAULT_FPS, bbox_x=0,
                 bbox_y=0, bbox_width=None, bbox_height=None):
        """Create a new Sprite object.

        ``name`` indicates the base name of the image files.  Files are
        to be located in one of the directories specified in
        ``image_directories``.  If a file with the exact name plus image
        file extensions is not available, numbered images will be
        searched for which have names with one of the following formats,
        where "name" is replaced with the specified base file name and
        "0" can be replaced with any integer:

            name-0
            name_0

        If images are found with names like those, all such images will
        be loaded and become frames of animation.  If not, sprite sheets
        will be searched for which have names with one of the following
        formats, where "name" is replaced with the specified base file
        name and "2" can be replaced with any integer:

            name-strip2
            name_strip2

        The number indicates the number of animation frames in the
        sprite sheet. The sprite sheet will be read like a horizontal
        reel, with the first frame on the far left and the last frame on
        the far right, and no space in between frames.

        ``name`` can also be None, in which case the sprite will be a
        transparent rectangle at the specified size (with both ``width``
        and ``height`` defaulting to 32 if they are set to None).  The
        implementation decides what to assign to the sprite's ``name``
        attribute, but it is always a string.

        If no image is found based on any of the above methods and
        ``name`` is not None, IOError will be raised.

        If ``width`` or ``height`` is set to None, the respective size
        will be taken from the largest animation frame.  If
        ``bbox_width`` or ``bbox_height`` is set to None, the respective
        size will be the respective size of the sprite.

        All remaining arguments set the initial properties of the
        sprite; see Sprite.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def draw_dot(self, x, y, color, frame=None):
        """Draw a single-pixel dot.

        ``x`` and ``y`` indicate the location in the sprite to draw the
        dot, where x=0, y=0 is the origin and x and y increase toward
        the right and bottom, respectively.  ``color`` indicates the
        color of the dot.  ``frame`` indicates the frame of the sprite
        to draw on, where 0 is the first frame; set to None to draw on
        all frames.

        """
        # TODO

    def draw_line(self, x1, y1, x2, y2, color, thickness=1, anti_alias=False,
                  frame=None):
        """Draw a line segment between the given points.

        ``x1``, ``y1``, ``x2``, and ``y2`` indicate the location in the
        sprite of the points between which to draw the line segment,
        where x=0, y=0 is the origin and x and y increase toward the
        right and bottom, respectively.  ``color`` indicates the color
        of the line segment.  ``thickness`` indicates the thickness of
        the line segment in pixels.  ``anti_alias`` indicates whether or
        not anti-aliasing should be used.  ``frame`` indicates the frame
        of the sprite to draw on, where 0 is the first frame; set to
        None to draw on all frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def draw_rectangle(self, x, y, width, height, fill=None, outline=None,
                       outline_thickness=1, frame=None):
        """Draw a rectangle at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the top-left corner of the rectangle, where x=0, y=0 is the
        origin and x and y increase toward the right and bottom,
        respectively.  ``width`` and ``height`` indicate the size of the
        rectangle.  ``fill`` indicates the color of the fill of the
        rectangle; set to None for no fill.  ``outline`` indicates the
        color of the outline of the rectangle; set to None for no
        outline.  ``outline_thickness`` indicates the thickness of the
        outline in pixels (ignored if there is no outline).  ``frame``
        indicates the frame of the sprite to draw on, where 0 is the
        first frame; set to None to draw on all frames.

        """
        # TODO

    def draw_ellipse(self, x, y, width, height, fill=None, outline=None,
                     outline_thickness=1, anti_alias=False, frame=None):
        """Draw an ellipse at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the top-left corner of the imaginary rectangle containing the
        ellipse, where x=0, y=0 is the origin and x and y increase
        toward the right and bottom, respectively.  ``width`` and
        ``height`` indicate the size of the ellipse.  ``fill`` indicates
        the color of the fill of the ellipse; set to None for no fill.
        ``outline`` indicates the color of the outline of the ellipse;
        set to None for no outline.  ``outline_thickness`` indicates the
        thickness of the outline in pixels (ignored if there is no
        outline).  ``anti_alias`` indicates whether or not anti-aliasing
        should be used on the outline.  ``frame`` indicates the frame of
        the sprite to draw on, where 0 is the first frame; set to None
        to draw on all frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def draw_circle(self, x, y, radius, fill=None, outline=None,
                    outline_thickness=1, frame=None):
        """Draw a circle at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the center of the circle, where x=0, y=0 is the origin and x and
        y increase toward the right and bottom, respectively.
        ``radius`` indicates the radius of the circle in pixels.
        ``fill`` indicates the color of the fill of the circle; set to
        None for no fill.  ``outline`` indicates the color of the
        outline of the circle; set to None for no outline.
        ``outline_thickness`` indicates the thickness of the outline in
        pixels (ignored if there is no outline).  ``anti_alias``
        indicates whether or not anti-aliasing should be used on the
        outline.  ``frame`` indicates the frame of the sprite to draw
        on, where 0 is the first frame; set to None to draw on all
        frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def draw_text(self, font, text, x, y, width=None, height=None,
                  color="black", halign=ALIGN_LEFT, valign=ALIGN_TOP,
                  anti_alias=True, frame=None):
        """Draw the given text at the given position.

        ``font`` indicates the font to use to draw the text.  ``text``
        indicates the text to draw.  ``x`` and ``y`` indicate the
        location in the sprite to position the text, where x=0, y=0 is
        the origin and x and y increase toward the right and bottom,
        respectively.  ``width`` and ``height`` indicate the size of the
        imaginary box the text is drawn in; set to None for no imaginary
        box.  ``color`` indicates the color of the text.  ``halign``
        indicates the horizontal alignment of the text and can be
        ALIGN_LEFT, ALIGN_CENTER, or ALIGN_RIGHT.  ``valign`` indicates
        the vertical alignment and can be ALIGN_TOP, ALIGN_MIDDLE, or
        ALIGN_BOTTOM.  ``anti_alias`` indicates whether or not anti-
        aliasing should be used.  ``frame`` indicates the frame of the
        sprite to draw on, where 0 is the first frame; set to None to
        draw on all frames.

        If the text does not fit into the imaginary box specified, the
        text that doesn't fit will be cut off at the bottom if valign is
        ALIGN_TOP, the top if valign is ALIGN_BOTTOM, or equally the top
        and bottom if valign is ALIGN_MIDDLE.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is False.

        """
        # TODO

    def draw_clear(self, frame=None):
        """Erase everything from the sprite.

        ``frame`` indicates the frame of the sprite to clear, where 0 is
        the first frame; set to None to clear all frames.

        """
        # TODO


class BackgroundLayer(object):

    """Special class used for background layers.

    All BackgroundLayer objects have the following attributes:
        sprite: The Sprite object used for this layer.  While it will
            always be an actual Sprite object when read, it can also be
            set to the ID of a sprite.
        x: The horizontal offset of the layer.
        y: The vertical offset of the layer.
        z: The Z-axis position of the layer in the room, which
            determines in what order layers are drawn; layers with a
            higher Z value are drawn in front of layers with a lower Z
            value.
        xscroll_rate: The horizontal speed the layer scrolls as a factor
            of the view scroll speed.
        yscroll_rate: The vertical speed the layer scrolls as a factor
            of the view scroll speed.
        xrepeat: Whether or not the background should be repeated
            horizontally.
        yrepeat: Whether or not the background should be repeated
            vertically.

    """

    def __init__(self, sprite, x, y, z, xscroll_rate=1, yscroll_rate=1,
                 xrepeat=True, yrepeat=True):
        """Create a background layer object.

        Arguments set the properties of the layer.  See
        BackgroundLayer.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO


class Background(object):

    """Background class.

    All Background objects have the following attributes:
        color: A Stellar Game Engine color used in parts of the
            background where there is no layer.

    The following read-only attributes are also available:
        id: The unique identifier for this background.
        layers: A tuple containing all BackgroundLayer objects used in
            this background.

    """

    def __init__(self, layers, color, id_=None, **kwargs):
        """Create a background with the given color and layers.

        Arguments set the properties of the background.  See
        Background.__doc__ for more information.

        If ``id`` is None, it will be set to an integer not currently
        used as an ID (the exact number chosen is implementation-
        specific and may not necessarily be the same between runs).

        In addition to containing actual BackgroundLayer objects,
        ``layers`` can contain valid names of BackgroundLayer objects'
        sprites.

        A game object must exist before an object of this class is
        created.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        # TODO


class Font(object):

    """Font handling class.

    All Font objects have the following attributes:
        size: The height of the font in pixels.
        underline: Whether or not underlined rendering is enabled.
        bold: Whether or not bold rendering is enabled.
        italic: Whether or not italic rendering is enabled.

    The following read-only attributes are also available:
        name: The name of the font given when it was created.  See
            Sound.__init__.__doc__ for more information.

    Font methods:
        get_size: Return the size of the given rendered text.

    """

    def __init__(self, name=None, size=12, underline=False, bold=False,
                 italic=False):
        """Create a new Font object.

        ``name`` indicates the name of the font.  This can be either the
        name of a font file, to be located in one of the directories
        specified in ``font_directories``, or the name of a system
        font.  If the specified font does not exist in either form, a
        default, implementation-dependent font will be used.

        ``name`` can also be a list or tuple of fonts to choose from in
        order of preference.

        Implementations are supposed, but not required, to attempt to
        use a compatible font where possible. For example, if the font
        specified is "Times New Roman" and Times New Roman is not
        available, compatible fonts such as Liberation Serif should be
        attempted as well.

        All remaining arguments set the initial properties of the font.
        See Font.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def get_size(self, text, x, y, width=None, height=None):
        """Return the size of the given rendered text.

        All arguments correspond with the same arguments in Font.render,
        and the size returned reflects rendering rules therein; see
        Font.render.__doc__ for more information.  Returned value is a
        tuple in the form (width, height).

        """
        # TODO


class Sound(object):

    """Sound handling class.

    All Sound objects have the following attributes:
        volume: The volume of the sound in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the sound effect on stereo speakers.  A
            value of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all sounds will be played through both
            speakers equally (assuming stereo sound is used).
        max_play: The maximum instances of this sound playing permitted.
            Set to 0 for no limit.

    The following read-only attributes are also available:
        fname: The file name of the sound given when it was created.
            See Sound.__init__.__doc__ for more information.
        length: The length of the sound in milliseconds.
        playing: The number of instances of this sound playing.

    Sound methods:
        Sound.play: Play the sound.
        Sound.stop: Stop the sound.
        Sound.pause: Pause playback of the sound.
        Sound.unpause: Resume playback of the sound if paused.

    Ogg Vorbis and uncompressed WAV are supported at a minimum.
    Depending on the implementation, other formats may be supported.

    """

    def __init__(self, fname, volume=100, balance=0, max_play=1):
        """Create a new sound object.

        ``fname`` indicates the name of the sound file, to be located in
        one of the directories specified in ``sound_directories``.

        All remaining arguments set the initial properties of the sound.
        See Sound.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def play(self, loops=0, maxtime=None, fade_time=None):
        """Play the sound.

        ``loops`` indicates the number of extra times to play the sound
        after it is played the first time; set to -1 or None to loop
        indefinitely.  ``maxtime`` indicates the maximum amount of time
        to play the sound in milliseconds; set to 0 or None for no
        limit. ``fade_time`` indicates the time in milliseconds over
        which to fade the sound in; set to 0 or None to immediately play
        the sound at full volume.

        """
        # TODO

    def stop(self, fade_time=None):
        """Stop the sound.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the sound.

        """
        # TODO

    def pause(self):
        """Pause playback of the sound."""
        # TODO

    def unpause(self):
        """Resume playback of the sound if paused."""
        # TODO


class Music(object):

    """Music handling class.

    Music is mostly the same as sound, but only one can be played at a
    time.

    All Music objects have the following attributes:
        volume: The volume of the music in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the music on stereo speakers.  A value
            of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all music will be played through both
            speakers equally (assuming stereo sound is used).

    The following read-only attributes are also available:
        fname: The file name of the music given when it was created.
            See Music.__init__.__doc__ for more information.
        length: The length of the music in milliseconds.
        playing: Whether or not the music is playing.
        position: The current position (time) on the music in
            milliseconds.

    Music methods:
        Music.play: Play the music.
        Music.queue: Queue the music for playback.
        Music.stop: Stop the music.
        Music.pause: Pause playback of the music.
        Music.unpause: Resume playback of the music if paused.
        Music.restart: Restart music from the beginning.

    Ogg Vorbis is supported at a minimum.  Depending on the
    implementation, other formats may be supported.

    """

    def __init__(self, fname, volume=100, balance=0):
        """Create a new music object.

        ``fname`` indicates the name of the sound file, to be located in
        one of the directories specified in ``music_directories``.

        All remaining arguments set the initial properties of the music.
        See Music.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def play(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Play the music.

        If music was already playing when this is called, it will be
        stopped.

        ``start`` indicates the number of milliseconds from the
        beginning to start at.  ``loops`` indicates the number of extra
        times to play the sound after it is played the first time; set
        to -1 or None to loop indefinitely.  ``maxtime`` indicates the
        maximum amount of time to play the sound in milliseconds; set to
        0 or None for no limit.  ``fade_time`` indicates the time in
        milliseconds over which to fade the sound in; set to 0 or None
        to immediately play the music at full volume.

        """
        # TODO

    def queue(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        See Music.play.__doc__ for information about the arguments.

        """
        # TODO

    def stop(self, fade_time=None):
        """Stop the music.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the music.

        """
        # TODO

    def pause(self):
        """Pause playback of the music."""
        # TODO

    def unpause(self):
        """Resume playback of the music if paused."""
        # TODO


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
            increases toward the right.
        bbox_y: The vertical location of the top-left corner of the
            bounding box in relation to y, where 0 is y and bbox_y
            increases toward the bottom.
        bbox_width: The width of the bounding box in pixels.
        bbox_height: The height of the bounding box in pixels.
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
        xvelocity: The velocity of the object toward the right.  Default
            is 0.
        yvelocity: The velocity of the object toward the bottom.
            Default is 0.
        speed: The total (directional) speed of the object.  Default is
            0.
        move_direction: The direction of the object's movement in
            degrees, with 0 being directly to the right and rotation in
            a positive direction being counter-clockwise.  Default is 0.
        image_index: The animation frame currently being displayed, with
            0 being the first one.  Default is 0.
        image_fps: The animation rate in frames per second.  Default is
            the value recommended by the sprite, or 0 if there is no
            sprite.
        image_xscale: The horizontal scale factor for the sprite.
            Default is 1.
        image_yscale: The vertical scale factor for the sprite.  Default
            is 1.
        image_rotation: The rotation of the sprite, with rotation in a
            positive direction being counter-clockwise.  Default is 0.
        image_alpha: The alpha value applied to the entire image, where
            255 is the original image, 128 is half the opacity of the
            original image, 0 is fully transparent, etc.  Default is
            255.
        image_blend: The color to blend with the sprite.  Set to None
            for no color blending.  Default is None.

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
        destroy: Destroy the object.

    StellarClass events are handled by special methods.  The exact
    timing of their calling is implementation-dependent except where
    otherwise noted.  The methods are:
        event_create: Called when the object is created.  It is always
            called after any room start events occurring at the same
            time.
        event_step: Called once each frame.
        event_alarm: Called when an alarm counter reaches 0.
        event_key_press: Key press event.
        event_key_release: Key release event.
        event_mouse_move: Mouse move event.
        event_mouse_button_press: Mouse button press event.
        event_mouse_button_release: Mouse button release event.
        event_joystick_axis_move: Joystick axis move event.
        event_joystick_hat_move: Joystick HAT move event.
        event_joystick_button_press: Joystick button press event.
        event_joystick_button_release: Joystick button release event.
        event_collision: Middle/default collision event.
        event_collision_left: Left collision event.
        event_collision_right: Right collision event.
        event_collision_top: Top collision event.
        event_collision_bottom: Bottom collision event.
        event_animation_end: Called when an animation cycle ends.
        event_destroy: Destroy event.

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

        ``x`` and ``y``, indicate the position to check for collisions
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

    def event_step(self, time_passed):
        """Step event.

        Called once each frame.  ``time_passed`` is the number of
        milliseconds that have passed during the last frame.

        """
        pass

    def event_alarm(self, alarm_id):
        """Alarm event.

        Called when an alarm counter reaches 0.  ``alarm_id`` is the ID
        of the alarm that was set off.

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

    def event_animation_end(self):
        """Animation End event.

        Called when an animation cycle ends.

        """
        pass

    def event_destroy(self):
        """Destroy event."""
        pass

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See StellarClass.event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See StellarClass.event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See StellarClass.event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See StellarClass.event_mouse_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See StellarClass.event_mouse_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See StellarClass.event_joystick_axis_move.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See StellarClass.event_joystick_hat_move.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See StellarClass.event_joystick_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See StellarClass.event_joystick_button_release.__doc__ for more
        information.

        """
        pass


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


class Room(object):

    """Class for rooms.

    All Room objects have the following attributes:
        width: The width of the room in pixels.
        height: The height of the room in pixels.
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

    def __init__(self, objects=(), width=DEFAULT_SCREENWIDTH,
                 height=DEFAULT_SCREENHEIGHT, views=None, background=None):
        """Create a new Room object.

        Arguments set the properties of the room.  See Room.__doc__ for
        more information.

        If ``views`` is set to None, a new view will be  created with
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


class View(object):

    """Class for room views.

    All View objects have the following attributes:
        x: The horizontal position of the view in the room, where the
            left edge is 0 and x increases toward the right.
        y: The vertical position of the view in the room, where the top
            edge is 0 and y increases toward the bottom.
        xport: The horizontal position of the view on the screen, where
            the left edge is 0 and xport increases toward the right.
        yport: The vertical position of the view on the screen, where
            the top edge is 0 and yport increases toward the bottom.
        width: The width of the view in pixels.
        height: The height of the view in pixels.

    """

    def __init__(self, x, y, xport=0, yport=0, width=None, height=None):
        """Create a new View object.

        Arguments set the properties of the view.  See View.__doc__ for
        more information.

        If ``width`` or ``height`` is set to None, the respective size
        will be set such that the view takes up all of the space that it
        can (i.e. game.width - xport or game.height - yport).

        """
        # TODO


def create_object(cls, *args, **kwargs):
    """Create an object in the current room.

    ``cls`` is the class (derived from StellarClass) to create an object
    of.  ``args`` and ``kwargs`` are passed on to cls.__init__ as
    arguments.

    Calling this function is equivalent to:
        sge.game.current_room.add(cls(*args, **kwargs))

    """
    game.current_room.add(cls(*args, **kwargs))


def sound_stop_all():
    """Stop playback of all sounds."""
    for i in game.sounds:
        game.sounds[i].stop()


def music_clear_queue():
    """Clear the music queue."""
    # TODO


def music_stop_all():
    """Stop playback of any music and clear the queue."""
    for i in game.music:
        game.music[i].stop()

    music_clear_queue()


def get_key_pressed(key):
    """Return whether or not a given key is pressed.

    ``key`` is the key to check.

    """
    # TODO

def get_mouse_button_pressed(button):
    """Return whether or not a given mouse button is pressed.

    ``button`` is the number of the mouse button to check, where 0
    is the first mouse button.

    """
    # TODO

def get_joystick_axis(joystick, axis):
    """Return the position of the given axis.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``axis`` is the number of the axis to
    check, where 0 is the first axis of the joystick.

    Returned value is a float from -1 to 1, where 0 is centered, -1
    is all the way to the left or up, and 1 is all the way to the
    right or down.

    If the joystick or axis requested does not exist, 0 is returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO

def get_joystick_hat(joystick, hat):
    """Return the position of the given HAT.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``hat`` is the number of the HAT to check,
    where 0 is the first HAT of the joystick.

    Returned value is a tuple in the form (x, y), where x is the
    horizontal position and y is the vertical position.  Both x and
    y are 0 (centered), -1 (left or up), or 1 (right or down).

    If the joystick or HAT requested does not exist, (0, 0) is
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO

def get_joystick_button_pressed(joystick, button):
    """Return whether or not the given button is pressed.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``button`` is the number of the button to
    check, where 0 is the first button of the joystick.

    If the joystick or button requested does not exist, False is
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO

def get_joysticks():
    """Return the number of joysticks available.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will always return 0.

    """
    # TODO

def get_joystick_axes(joystick):
    """Return the number of axes available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO

def get_joystick_hats(joystick):
    """Return the number of HATs available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO

def get_joystick_buttons(joystick):
    """Return the number of buttons available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    # TODO
