#!/usr/bin/env python

# Stellar Game Engine - Pygame
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

"""Stellar Game Engine - Pygame

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

Global variables:
    game: Stores the current game.  If there is no game currently, this
        variable is set to None.

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

Implementation-specific information:
Since Pygame supports trackballs, they are implemented as extra analog
sticks.  Their movement is limited to the range of an analog stick to
ensure full compatibility.

In addition to Ogg Vorbis, Music supports the following formats:

    MP3 (support limited; use not recommended)
    MOD
    XM
    MIDI

For starting position in MOD files, the pattern order number is used
instead of the number of milliseconds.  For some other extra formats,
specifying the starting position may have no effect.

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.0.15"

import sys
import os
import math
import weakref

import pygame

__all__ = ['Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font', 'Sound',
           'Music', 'StellarClass', 'Room', 'View', 'game', 'ALIGN_LEFT',
           'ALIGN_CENTER', 'ALIGN_RIGHT', 'ALIGN_TOP', 'ALIGN_MIDDLE',
           'ALIGN_BOTTOM']
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

KEYS = {"0": pygame.K_0, "1": pygame.K_1, "2": pygame.K_2, "3": pygame.K_3,
        "4": pygame.K_4, "5": pygame.K_5, "6": pygame.K_6, "7": pygame.K_7,
        "8": pygame.K_8, "9": pygame.K_9, "a": pygame.K_a, "b": pygame.K_b,
        "c": pygame.K_c, "d": pygame.K_d, "e": pygame.K_e, "f": pygame.K_f,
        "g": pygame.K_g, "h": pygame.K_h, "i": pygame.K_i, "j": pygame.K_j,
        "k": pygame.K_k, "l": pygame.K_l, "m": pygame.K_m, "n": pygame.K_n,
        "o": pygame.K_o, "p": pygame.K_p, "q": pygame.K_q, "r": pygame.K_r,
        "s": pygame.K_s, "t": pygame.K_t, "u": pygame.K_u, "v": pygame.K_v,
        "w": pygame.K_w, "x": pygame.K_x, "y": pygame.K_y, "z": pygame.K_z,
        "alt_left": pygame.K_LALT, "alt_right": pygame.K_RALT,
        "ampersand": pygame.K_AMPERSAND, "apostrophe": pygame.K_QUOTE,
        "asterisk": pygame.K_ASTERISK, "at": pygame.K_AT,
        "backslash": pygame.K_BACKSLASH, "backspace": pygame.K_BACKSPACE,
        "backtick": pygame.K_BACKQUOTE, "bracket_left": pygame.K_LEFTBRACKET,
        "bracket_right": pygame.K_RIGHTBRACKET, "break": pygame.K_BREAK,
        "caps_lock": pygame.K_CAPSLOCK, "caret": pygame.K_CARET,
        "clear": pygame.K_CLEAR, "colon": pygame.K_COLON,
        "comma": pygame.K_COMMA, "ctrl_left": pygame.K_LCTRL,
        "ctrl_right": pygame.K_RCTRL, "delete": pygame.K_DELETE,
        "dollar": pygame.K_DOLLAR, "down": pygame.K_DOWN, "end": pygame.K_END,
        "enter": pygame.K_RETURN, "equals": pygame.K_EQUALS,
        "escape": pygame.K_ESCAPE, "euro": pygame.K_EURO,
        "exclamation": pygame.K_EXCLAIM, "f1": pygame.K_F1, "f2": pygame.K_F2,
        "f3": pygame.K_F3, "f4": pygame.K_F4, "f5": pygame.K_F5,
        "f6": pygame.K_F6, "f7": pygame.K_F7, "f8": pygame.K_F8,
        "f9": pygame.K_F9, "f10": pygame.K_F10, "f11": pygame.K_F11,
        "f12": pygame.K_F12, "greater_than": pygame.K_GREATER,
        "hash": pygame.K_HASH, "help": pygame.K_HELP, "home": pygame.K_HOME,
        "hyphen": pygame.K_MINUS, "insert": pygame.K_INSERT,
        "kp_0": pygame.K_KP0, "kp1": pygame.K_KP1, "kp2": pygame.K_KP2,
        "kp3": pygame.K_KP3, "kp4": pygame.K_KP4, "kp5": pygame.K_KP5,
        "kp6": pygame.K_KP6, "kp7": pygame.K_KP7, "kp_8": pygame.K_KP8,
        "kp_9": pygame.K_KP9, "kp_divide": pygame.K_KP_DIVIDE,
        "kp_enter": pygame.K_KP_ENTER, "kp_equals": pygame.K_KP_EQUALS,
        "kp_minus": pygame.K_KP_MINUS, "kp_multiply": pygame.K_KP_MULTIPLY,
        "kp_plus": pygame.K_KP_PLUS, "kp_point": pygame.K_KP_PERIOD,
        "left": pygame.K_LEFT, "less_than": pygame.K_LESS,
        "menu": pygame.K_MENU, "meta_left": pygame.K_LMETA,
        "meta_right": pygame.K_RMETA, "mode": pygame.K_MODE,
        "num_lock": pygame.K_NUMLOCK, "pagedown": pygame.K_PAGEDOWN,
        "pageup": pygame.K_PAGEUP, "parenthesis_left": pygame.K_LEFTPAREN,
        "parenthesis_right": pygame.K_RIGHTPAREN, "pause": pygame.K_PAUSE,
        "period": pygame.K_PERIOD, "plus": pygame.K_PLUS,
        "power": pygame.K_POWER, "print_screen": pygame.K_PRINT,
        "question": pygame.K_QUESTION, "quote": pygame.K_QUOTEDBL,
        "right": pygame.K_RIGHT, "scroll_lock": pygame.K_SCROLLOCK,
        "semicolon": pygame.K_SEMICOLON, "shift_left": pygame.K_LSHIFT,
        "shift_right": pygame.K_RSHIFT, "slash": pygame.K_SLASH,
        "space": pygame.K_SPACE, "super_left": pygame.K_LSUPER,
        "super_right": pygame.K_RSUPER, "sysrq": pygame.K_SYSREQ,
        "tab": pygame.K_TAB, "underscore": pygame.K_UNDERSCORE,
        "up": pygame.K_UP}
KEYNAMES = {}
for pair in KEYS.items():
    KEYNAMES[pair[1]] = pair[0]

IMPLEMENTATION = "Pygame 1.9"
ALIGN_LEFT = 2
ALIGN_CENTER = 3
ALIGN_RIGHT = 1
ALIGN_TOP = 2
ALIGN_MIDDLE = 3
ALIGN_BOTTOM = 1

# Global variables
game = None


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
            using their
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
            movement during the last quarter of a second.

    Game methods:
        start: Start the game at the first room.
        end: Properly end the game.
        pause: Pause the game.
        unpause: Unpause the game.
        draw_dot: Draw a single-pixel dot.
        draw_line: Draw a line segment between the given points.
        draw_rectangle: Draw a rectangle at the given position.
        draw_ellipse: Draw an ellipse at the given position.
        draw_circle: Draw a circle at the given position.
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

    Game events are handled by special methods.  The time that they are
    called is based on the following events, which happen each frame in
    the following order and are synchronized among all objects which
    have them:
        event_step_begin
        event_step
        event_step_end

    The following events are not timed in any particular way, but are
    called immediately when the engine detects them occurring:
        event_game_start
        event_game_end
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

    The following events are always called (in no particular order)
    between calls of event_step_begin and event_step:
        event_key_press
        event_key_release
        event_mouse_move
        event_mouse_button_press
        event_mouse_button_release
        event_joystick_axis_move
        event_joystick_hat_move
        event_joystick_button_press
        event_joystick_button_release
        event_close

    The following events are always called (in no particular order)
    between calls of event_step and event_step_end:
        event_mouse_collision
        event_mouse_collision_left
        event_mouse_collision_right
        event_mouse_collision_top
        event_mouse_collision_bottom

    """

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value != self._width:
            self._width = value
            self._set_mode()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value != self._height:
            self._height = value
            self._set_mode()

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        if value != self._fullscreen:
            self._fullscreen = value
            self._set_mode()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if value != self._scale:
            self._scale = value
            self._set_mode()

    @property
    def scale_proportional(self):
        return self._scale_proportional

    @scale_proportional.setter
    def scale_proportional(self, value):
        if value != self._scale_proportional:
            self._scale_proportional = value
            self._set_mode()

    @property
    def scale_smooth(self):
        return self._scale_smooth

    @scale_smooth.setter
    def scale_smooth(self, value):
        if value != self._scale_smooth:
            self._scale_smooth = value
            self._set_mode()

    def __init__(self, width=DEFAULT_SCREENWIDTH, height=DEFAULT_SCREENHEIGHT,
                 fullscreen=DEFAULT_FULLSCREEN, scale=DEFAULT_SCALE,
                 scale_proportional=DEFAULT_SCALE_PROPORTIONAL,
                 scale_smooth=DEFAULT_SCALE_SMOOTH, fps=DEFAULT_FPS,
                 delta=DEFAULT_DELTA, delta_min=DEFAULT_DELTA_MIN):
        """Create a new Game object.

        Arguments set the properties of the game.  See Game.__doc__ for
        more information.

        """
        pygame.init()
        global game
        game = self

        self._width = width
        self._height = height
        self._window_width = width
        self._window_height = height
        self._fullscreen = fullscreen
        self._scale = scale
        self._scale_proportional = scale_proportional
        self._scale_smooth = scale_smooth
        self.fps = fps
        self.delta = delta
        self.delta_min = delta_min
        self._set_mode()

        self._music_queue = []
        self._running = False
        self._clock = pygame.time.Clock()
        self._joysticks = []
        self._pygame_sprites = pygame.sprite.LayeredDirty()

    def start(self):
        """Start the game at the first room.

        Can be called in the middle of a game to start the game over.
        If you do this, everything will be reset to its original state.

        """
        if self._running:
            for room in self.rooms:
                room._reset()

            self.rooms[0].start()
        else:
            self._running = True
            self.event_game_start()
            self.rooms[0].start()
            self._clock.tick()

            while self._running:
                # Begin Step event
                self.event_step_begin()
                for i in self.objects:
                    self.objects[i].event_step_begin()

                for event in pygame.events.get():
                    if event.type == pygame.KEYDOWN:
                        self.event_key_press(event.key)
                    elif event.type == pygame.KEYUP:
                        self.event_key_release(event.key)
                    elif event.type == pygame.MOUSEMOTION:
                        self.mouse.x, self.mouse.y = event.pos
                        self.event_mouse_move(*event.rel)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.event_mouse_button_press(event.button)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.event_mouse_button_release(event.button)
                    elif event.type == pygame.JOYAXISMOTION:
                        self.event_joystick_axis_move(event.joy, event.axis,
                                                      event.value)
                    elif event.type == pygame.JOYBALLMOTION:
                        # Limited support for trackballs by pretending
                        # they're axes.  Since they're acting like axes,
                        # they must be in the range [-1,1].
                        n = (self._joysticks[event.joy].get_numaxes() +
                             2 * event.ball)
                        xvalue = min(max(-1, event.rel[0]), 1)
                        yvalue = min(max(-1, event.rel[1]), 1)

                        if xvalue != 0:
                            self.event_joystick_axis_move(event.joy, n, xvalue)
                        if yvalue != 0:
                            self.event_joystick_axis_move(event.joy, n + 1,
                                                          yvalue)
                    elif event.type == pygame.JOYHATMOTION:
                        self.event_joystick_hat_move(event.joy, event.hat,
                                                     *event.value)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.event_joystick_button_press(event.joy,
                                                         event.button)
                    elif event.type == pygame.JOYBUTTONUP:
                        self.event_joystick_button_release(event.joy,
                                                           event.button)
                    elif event.type == pygame.QUIT:
                        self.event_close()

                # Step event
                self.event_step()
                for i in self.objects:
                    self.objects[i].event_step_begin()

                if self.delta:
                    time_passed = min(self._clock.tick(self.fps),
                                      1000 / self.delta_min)
                else:
                    self._clock.tick(self.fps)
                    time_passed = 1000 / self.fps

                for i in self.objects:
                    obj = self.objects[i]

                    if obj.xvelocity or obj.yvelocity:
                        obj.x += obj.xvelocity
                        obj.y += obj.yvelocity

                        # Detect collisions
                        for j in self.objects:
                            other = self.objects[j]
                            if obj.collides(other)
                                xcollision = not obj.collides(other,
                                                              x=obj.xprevious)
                                ycollision = not obj.collides(other,
                                                              y=obj.yprevious)

                                if xcollision and ycollision:
                                    # Corner collision; determine
                                    # direction by distance.
                                    if obj.xvelocity > 0:
                                        xdepth = (
                                            obj.bbox_right - other.bbox_left)
                                    else:
                                        xdepth = (
                                            other.bbox_right - obj.bbox_left)

                                    if obj.yvelocity > 0:
                                        ydepth = (
                                            obj.bbox_bottom - other.bbox_top)
                                    else:
                                        ydepth = (
                                            other.bbox_bottom - obj.bbox_top)

                                    if xdepth > ydepth:
                                        if obj.xvelocity > 0:
                                            obj.event_collision_right(other)
                                            other.event_collision_left(obj)
                                        else:
                                            obj.event_collision_left(other)
                                            other.event_collision_right(obj)
                                    else:
                                        if obj.yvelocity > 0:
                                            obj.event_collision_bottom(other)
                                            other.event_collision_top(obj)
                                        else:
                                            obj.event_collision_top(other)
                                            other.event_collision_bottom(obj)

                                elif xcollision:
                                    # Horizontal collision only.
                                    if obj.xvelocity > 0:
                                        obj.event_collision_right(other)
                                        other.event_collision_left(obj)
                                    else:
                                        obj.event_collision_left(other)
                                        other.event_collision_right(obj)

                                elif ycollision:
                                    # Vertical collision only.
                                    if obj.yvelocity > 0:
                                        obj.event_collision_bottom(other)
                                        other.event_collision_top(obj)
                                    else:
                                        obj.event_collision_top(other)
                                        other.event_collision_bottom(obj)

                                elif not obj.collides(other, obj.xprevious,
                                                      obj.yprevious):
                                    # Wedge collision (both vertical and
                                    # horizontal collisions).
                                    if obj.xvelocity > 0:
                                        obj.event_collision_right(other)
                                        other.event_collision_left(obj)
                                    else:
                                        obj.event_collision_left(other)
                                        other.event_collision_right(obj)
                                    if obj.yvelocity > 0:
                                        obj.event_collision_bottom(other)
                                        other.event_collision_top(obj)
                                    else:
                                        obj.event_collision_top(other)
                                        other.event_collision_bottom(obj)

                                else:
                                    # No directional collision; this is
                                    # a continuous collision.
                                    obj.event_collision(other)
                                    other.event_collision(obj)

                # End Step event
                self.event_step_end()
                for i in self.objects:
                    self.objects[i].event_step_begin()

                # Redraw
                self._pygame_sprites.clear(self._window, self._background)
                self._pygame_sprites.update()
                dirty = self._pygame_sprites.draw(self._window)
                pygame.display.update(dirty)

            self.event_game_end()

    def end(self):
        """Properly end the game."""
        pygame.quit()
        self._running = False
        global game
        game = None

    def pause(self, image=None):
        """Pause the game.

        ``image`` is the image to show when the game is paused.  If set
        to None, the default image will be shown.  The default image is
        at the discretion of the Stellar Game Engine implementation, as
        are any additional visual effects, with the stipulation that the
        following conditions are met:

            1. The default image must unambiguously demonstrate that the
                game is paused (the easiest way to do this is to include
                the word "paused" somewhere in the image).
            2. The view must stay in place.
            3. What was going on within the view before the game was
                paused must remain visible while the game is paused.

        While the game is paused, all game events will be halted, all
        objects will be treated like they don't exist, and all sounds
        and music will be stopped.  Game events whose names start with
        "event_paused_" will occur during this time.

        """
        pass

    def unpause(self):
        """Unpause the game."""
        pass

    def draw_dot(self, x, y, color):
        """Draw a single-pixel dot.

        ``x`` and ``y`` indicate the location in the room to draw the
        dot, where the left and top edges of the room are 0 and x and y
        increase toward the right and bottom.  ``color`` indicates the
        color of the dot.

        """
        pass

    def draw_line(self, x1, y1, x2, y2, color, thickness=1, anti_alias=False):
        """Draw a line segment between the given points.

        ``x1``, ``y1``, ``x2``, and ``y2`` indicate the location in the
        room of the points between which to draw the line segment, where
        the left and top edges of the room are 0 and x and y increase
        toward the right and bottom.  ``color`` indicates the color of
        the line segment.  ``thickness`` indicates the thickness of the
        line segment in pixels.  ``anti_alias`` indicates whether or not
        anti-aliasing should be used.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is
        False.

        """
        pass

    def draw_rectangle(self, x, y, width, height, fill=None, outline=None,
                       outline_thickness=1):
        """Draw a rectangle at the given position.

        ``x`` and ``y`` indicate the location in the room to draw the
        rectangle, where the left and top edges of the room are 0 and x
        and y increase toward the right and bottom.  ``width`` and
        ``height`` indicate the size of the rectangle.  ``fill``
        indicates the color of the fill of the rectangle; set to None
        for no fill.  ``outline`` indicates the color of the outline of
        the rectangle; set to None for no outline.
        ``outline_thickness`` indicates the thickness of the outline in
        pixels (ignored if there is no outline).

        """
        pass

    def draw_ellipse(self, x, y, width, height, fill=None, outline=None,
                     outline_thickness=1, anti_alias=False):
        """Draw an ellipse at the given position.

        ``x`` and ``y`` indicate the location in the room to draw the
        ellipse, where the left and top edges of the room are 0 and x
        and
        y increase toward the right and bottom.  ``width`` and
        ``height`` indicate the size of the ellipse.  ``fill`` indicates
        the color of the fill of the ellipse; set to None for no fill.
        ``outline`` indicates the color of the outline of the ellipse;
        set to None for no outline.  ``outline_thickness`` indicates the
        thickness of the outline in pixels (ignored if there is no
        outline).  ``anti_alias`` indicates whether or not anti-aliasing
        should be used on the outline.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is
        False.

        """

    def draw_circle(self, x, y, radius, fill=None, outline=None,
                    outline_thickness=1):
        """Draw a circle at the given position.

        ``x`` and ``y`` indicate the location in the room to draw the
        circle, where the left and top edges of the room are 0 and x and
        y increase toward the right and bottom.  ``radius`` indicates
        the radius of the circle in pixels.  ``fill`` indicates the
        color of the fill of the circle; set to None for no fill.
        ``outline`` indicates the color of the outline of the circle;
        set to None for no outline.  ``outline_thickness`` indicates the
        thickness of the outline in pixels (ignored if there is no
        outline).  ``anti_alias`` indicates whether or not anti-aliasing
        should be used on the outline.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is
        False.

        """

    def sound_stop_all(self):
        """Stop playback of all sounds."""
        pass

    def get_key_pressed(self, key):
        """Return whether or not a given key is pressed.

        ``key`` is the key to check.

        """
        pass

    def get_mouse_button_pressed(self, button):
        """Return whether or not a given mouse button is pressed.

        ``button`` is the number of the mouse button to check, where 0
        is the first mouse button.

        """
        pass

    def get_joystick_axis(self, joystick, axis):
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
        pass

    def get_joystick_hat(self, joystick, hat):
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
        pass

    def get_joystick_button_pressed(self, joystick, button):
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
        pass

    def get_joysticks(self):
        """Return the number of joysticks available.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will always return 0.

        """
        pass

    def get_joystick_axes(self, joystick):
        """Return the number of axes available on the given joystick.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  If the given joystick does not exist, 0
        will be returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def get_joystick_hats(self, joystick):
        """Return the number of HATs available on the given joystick.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  If the given joystick does not exist, 0
        will be returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def get_joystick_buttons(self, joystick):
        """Return the number of buttons available on the given joystick.

        ``joystick`` is the number of the joystick to check, where 0 is
        the first joystick.  If the given joystick does not exist, 0
        will be returned.

        Support for joysticks in Stellar Game Engine implementations is
        optional.  If the implementation used does not support
        joysticks, this function will act like the joystick requested
        does not exist.

        """
        pass

    def event_game_start(self):
        """Game start event."""
        pass

    def event_game_end(self):
        """Game end event."""
        pass

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See event_mouse_button_press.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See event_mouse_button_release.__doc__ for more information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See event_joystick_axis_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See event_joystick_hat_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See event_joystick_button_press.__doc__ for more information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See event_joystick_button_release.__doc__ for more information.

        """
        pass

    def event_paused_close(self):
        """Close event (e.g. close button) when paused."""
        pass

    def event_step_begin(self):
        """Global begin step event."""
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

        ``button`` is the number of the mouse button that was pressed,
        where 0 is the first mouse button.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        ``button`` is the number of the mouse button that was released,
        where 0 is the first mouse button.

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
        """Close event (e.g. close button)."""
        pass

    def event_step(self):
        """Global step event."""
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

    def event_step_end(self):
        """Global end step event."""
        pass

    def _set_mode(self):
        # Set the mode of the screen based on self.width, self.height,
        # and self.fullscreen.
        info = pygame.display.Info()

        if self.scale != 0:
            self._xscale = self.scale
            self._yscale = self.scale

        if self.fullscreen or not info.wm:
            self._window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

            if self.scale == 0:
                self._xscale = info.current_w / self.width
                self._yscale = info.current_h / self.height

                if self.scale_proportional:
                    self._make_scale_proportional()
        else:
            # Decide window size
            if self.scale == 0:
                self._xscale = self._window_width / self.width
                self._yscale = self._window_height / self.height

                if self.scale_proportional:
                    self._make_scale_proportional()

            self._window = pygame.display.set_mode(
                (self.width * self._xscale, self.height * self._yscale))

        # Refresh sprites
        for sprite in self.sprites:
            sprite._refresh()

    def _make_scale_proportional(self):
        # Fix scaling to make it proportional.
        if self._xscale / self._yscale > self.width / self.height:
            # Too wide.
            self._xscale = self.width * self._yscale / self.height
        else:
            # Either just right or too tall.
            self._yscale = self.height * self._xscale / self.width


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

    """

    @property
    def width(self):
        return self._w

    @width.setter
    def width(self, value):
        if self._w != value:
            self._w = value
            self.refresh()

    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, value):
        if self._h != value:
            self._h = value
            self._refresh()

    @property
    def transparent(self):
        return self._transparent

    @transparent.setter
    def transparent(self, value):
        if self._transparent != value:
            self._transparent = value
            self._refresh()

    def __init__(self, name, width=None, height=None, origin_x=0, origin_y=0,
                 transparent=True, fps=DEFAULT_FPS, bbox_x=0, bbox_y=0,
                 bbox_width=None, bbox_height=None):
        """Create a new Sprite object.

        ``name`` indicates the base name of the image files.  Files are
        to be located in data/images, data/sprites, or data/backgrounds.
        If a file with the exact name plus image file extensions is not
        available, numbered images will be searched for which have names
        with one of the following formats, where "name" is replaced with
        the specified base file name and "0" can be replaced with any
        integer:

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

        If no image is found based on any of the above methods, a black
        rectangle will be created at the size specified by ``width`` and
        ``height``.  If either ``width`` or ``height`` is None, the
        respective size will default to 16 in this case.

        If ``width`` or ``height`` is set to None, the respective size
        will be taken from the largest animation frame.  If
        ``bbox_width`` or ``bbox_height`` is set to None, the respective
        size will be the respective size of the sprite.

        All remaining arguments set the initial properties of the
        sprite; see Sprite.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        assert name

        self._transparent = None
        self._baseimages = []
        self._images = []
        self._masks = {}

        fnames = os.listdir(os.path.join('data', 'images'))
        fnames.extend(os.listdir(os.path.join('data', 'sprites')))
        fnames.extend(os.listdir(os.path.join('data', 'backgrounds')))
        fname_single = None
        fname_frames = []
        fname_strip = None

        for fname in fnames:
            if fname.startswith(name) and os.path.isfile(fname):
                root, ext = os.path.splitext(fname)
                if root.rsplit('-', 1)[0] == name:
                    split = root.rsplit('-', 1)
                elif root.split('_', 1)[0] == name:
                    split = root.rsplit('_', 1)
                else:
                    split = (name, '')

                if root == name:
                    fname_single = fname
                elif split[1].isdigit():
                    n = int(split[1])
                    while len(fname_frames) - 1 < n:
                        fname_frames.append(None)
                    fname_frames[n] = fname
                elif (split[1].startswith('strip') and split[1][5:].isdigit()):
                    fname_strip = fname

        if fname_single:
            # Load the single image
            try:
                img = pygame.image.load(fname_single)
                self._baseimages.append(img)
            except pygame.error:
                print("Ignored {0}; not a valid image.".format(fname_single))

        if not self._baseimages and any(fname_frames):
            # Load the multiple images
            for fname in fname_frames:
                if fname:
                    try:
                        self._baseimages.append(pygame.image.load(fname))
                    except pygame.error:
                        print("Ignored {0}; not a valid image.".format(fname))

        if not self._baseimages and fname_strip:
            # Load the strip (sprite sheet)
            root, ext = os.path.splitext(fname)
            assert '-' in root or '_' in root
            assert (root.rsplit('-', 1)[0] == name or
                    root.rsplit('_', 1)[0] == name)
            if root.rsplit('-', 1)[0] == name:
                split = root.rsplit('-', 1)
            else:
                split = root.rsplit('_', 1)

            try:
                sheet = pygame.image.load(fname_strip)
                assert split[1][5:].isdigit()
                n = int(split[1][5:])

                img_w = sheet.get_width() // n
                img_h = sheet.get_height()
                for x in xrange(0, img_w * n, img_w):
                    rect = pygame.Rect(x, 0, img_w, img_h)
                    img = sheet.subsurface(rect)
                    self._baseimages.append(img)
            except pygame.error:
                print("Ignored {0}; not a valid image.".format(fname_strip))

        if not self._baseimages:
            # Generate placeholder image
            img = pygame.Surface((16, 16))
            self._baseimages.append(img)

        if width is None:
            width = 0
            for image in self._baseimages:
                width = max(width, image.get_width())

        if height is None:
            height = 0
            for image in self._baseimages:
                height = max(height, image.get_height())

        self._w = width
        self._h = height
        self.origin_x = origin_x
        self.origin_y = origin_y
        self._transparent = transparent
        self.fps = fps
        self.bbox_x = bbox_x
        self.bbox_y = bbox_y
        self.bbox_width = bbox_width
        self.bbox_height = bbox_height
        self._refresh()

    def _refresh(self):
        # Set the _images list based on the variables.
        self._images = []
        for image in self._baseimages:
            img = self._set_transparency(image)
            img = _scale(img, self.width, self.height)
            self._images.append({(1, 1):img})

    def _set_transparency(self, image):
        # Return a copy of the surface with transparency properly set
        # for this sprite's settings.
        if self.transparent:
            if image.get_flags() & pygame.SRCALPHA:
                return image.convert_alpha()
            else:
                colorkey_img = image.convert()
                color = image.get_at((image.get_width() - 1, 0))
                colorkey_img.set_colorkey(color, pygame.RLEACCEL)
                return colorkey_img
        else:
            return image.convert()

    def _get_image(self, num, xscale=1, yscale=1):
        # Return the properly sized surface.
        if (xscale, yscale) in self._images[num]:
            return self._images[num][(xscale, yscale)]
        else:
            # Hasn't been scaled to this size yet
            img = self._set_transparency(self._baseimages[num])

            if xscale < 0:
                xscale = abs(xscale)
                xflip = True
            else:
                xflip = False

            if yscale < 0:
                yscale = abs(yscale)
                yflip = True
            else:
                yflip = False

            img = pygame.transform.flip(img, xflip, yflip)
            img = _scale(img, self.width * xscale, self.height * yscale)

    def _get_precise_mask(self, num):
        # Return a precise mask (2D list of True/False values) for the
        # given image index.
        if num in self._masks:
            return self._masks[num]
        else:
            image = self._get_image(num)
            image.lock()
            mask = []
            if image.get_flags() & pygame.SRCALPHA:
                for x in xrange(image.get_width()):
                    mask.append([])
                    for y in xrange(image.get_height()):
                        mask[x].append(image.get_at((x, y)).a > 0)
            else:
                colorkey = image.get_colorkey()
                for x in xrange(image.get_width()):
                    mask.append([])
                    for y in xrange(image.get_height()):
                        mask[x].append(image.get_at((x, y)) == colorkey)

            self._masks[num] = mask
            return mask


class BackgroundLayer(object):

    """Special class used for background layers.

    All BackgroundLayer objects have the following attributes:
        sprite: The Sprite object used for this layer.  Can also be the
            name of a sprite.
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
        self.sprite = sprite
        self.x = x
        self.y = y
        self.z = z
        self.xscroll_rate = xscroll_rate
        self.yscroll_rate = yscroll_rate
        self.xrepeat = xrepeat
        self.yrepeat = yrepeat


class Background(object):

    """Background class.

    All Background objects have the following attributes:
        color: A Stellar Game Engine color used in parts of the
            background where there is no layer.
        id: The unique identifier for this background.

    The following read-only attributes are also available:
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
        if 'id' in kwargs:
            id_ = kwargs['id']

        self.color = color
        self.id = id_
        self.layers = []

        for layer in layers:
            if isinstance(layer, BackgroundLayer):
                self.layers.append(layer)
            else:
                if layer in game.background_layers:
                    self.layers.append(game.background_layers[layer])


class Font(object):

    """Font handling class.

    All Font objects have the following attributes:
        name: The name of the font.  Set to None for the default font.
        size: The height of the font in pixels.
        underline: Whether or not underlined rendering is enabled.
        bold: Whether or not bold rendering is enabled.
        italic: Whether or not italic rendering is enabled.

    """

    def __init__(self, name=None, size=12, underline=False, bold=False,
                 italic=False):
        """Create a new Font object.

        Arguments set the properties of the font.  See
        Font.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        pass

    def render(self, text, x, y, width=None, height=None, color="black",
               halign=ALIGN_LEFT, valign=ALIGN_TOP, anti_alias=True):
        """Render the given text to the screen.

        ``text`` indicates the text to render.  ``x`` and ``y`` indicate
        the location in the room to render the text, where the left and
        top edges of the room are 0 and x and y increase toward the
        right and bottom.  ``width`` and ``height`` indicate the size of
        the imaginary box the text is drawn in; set to None for no
        imaginary box.  ``color`` indicates the color of the text.
        ``halign`` indicates the horizontal alignment and can be
        ALIGN_LEFT, ALIGN_CENTER, or ALIGN_RIGHT. ``valign`` indicates
        the vertical alignment and can be ALIGN_TOP, ALIGN_MIDDLE, or
        ALIGN_BOTTOM.  ``anti_alias`` indicates whether or not
        anti-aliasing should be used.

        If the text does not fit in the imaginary box specified,
        ``height`` will be treated as None (i.e. the imaginary box will
        be vertically resized to fit the text).

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is False.

        """
        pass

    def get_size(self, text, x, y, width=None, height=None):
        """Return the size of the given rendered text.

        All arguments correspond with the same arguments in Font.render,
        and the size returned reflects rendering rules therein; see
        Font.render.__doc__ for more information.  Returned value is a
        tuple in the form (width, height).

        """
        pass


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
        length: The length of the sound in milliseconds.
        playing: The number of instances of this sound playing.

    The following read-only attributes are also available:
        fname: The file name of the sound given when it was created.
            See Sound.__init__.__doc__ for more information.

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
        data/sounds.

        All remaining arguments set the initial properties of the sound.
        See Sound.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        self.volume = volume
        self.balance = balance
        self.max_play = max_play
        self.length = 0
        self.playing = False

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
        pass

    def stop(self, fade_time=None):
        """Stop the sound.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the sound.

        """
        pass

    def pause(self):
        """Pause playback of the sound."""
        pass

    def unpause(self):
        """Resume playback of the sound if paused."""
        pass


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
        length: The length of the music in milliseconds.
        playing: Whether or not the music is playing.
        position: The current position (time) on the music in
            milliseconds.

    The following read-only attributes are also available:
        fname: The file name of the music given when it was created.
            See Music.__init__.__doc__ for more information.

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

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if self._volume != value:
            self._volume = value

            if self.playing:
                pygame.mixer.music.set_volume(value)

    @property
    def length(self):
        return self._length

    @property
    def playing(self):
        return self._playing

    @property
    def position(self):
        if self.playing:
            return self._start + pygame.mixer.music.get_pos()
        else:
            return 0

    def __init__(self, fname, volume=100, balance=0):
        """Create a new music object.

        ``fname`` indicates the name of the sound file, to be located in
        data/music.

        All remaining arguments set the initial properties of the music.
        See Music.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        self._music = fname
        self.volume = volume
        self.balance = balance
        self._timeout = None
        self._fade_time = None
        self._start = 0

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
        if not self.playing:
            pygame.mixer.music.load(self._music)

        self._timeout = maxtime
        self._fade_time = fade_time

        if self._music.lower().endswith(".mod"):
            # MOD music is handled differently in Pygame: it uses the
            # pattern order number rather than the time to indicate the
            # start time.
            self._start = 0
            pygame.mixer.music.play(loops, start)
        else:
            self._start = start
            try:
                pygame.mixer.music.play(loops, start / 1000)
            except NotImplementedError:
                pygame.mixer.music.play(loops)

    def queue(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        See Music.play.__doc__ for information about the arguments.

        """
        glob.music_queue.append((self, start, loops, maxtime, fade_time))

    def stop(self, fade_time=None):
        """Stop the music.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the music.

        """
        if self.playing:
            if fade_time:
                pygame.mixer.music.fadeout(fade_time)
            else:
                pygame.mixer.music.stop()

    def pause(self):
        """Pause playback of the music."""
        if self.playing:
            pygame.mixer.music.pause()

    def unpause(self):
        """Resume playback of the music if paused."""
        if self.playing:
            pygame.mixer.music.unpause()


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
        id: The unique identifier for this object.
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
        xstart: The initial value of x when the object was created.
        ystart: The initial value of y when the object was created.
        xprevious: The previous value of x.
        yprevious: The previous value of y.

    StellarClass methods:
        collides: Return whether or not this object collides with
            another.
        set_alarm: Set an alarm.
        destroy: Destroy the object.

    StellarClass events are handled by special methods.  The time that
    they are called is based on the following events, which happen each
    frame in the following order and are synchronized among all objects
    which have them:
        event_step_begin
        event_step
        event_step_end

    The following events are not timed in any particular way, but are
    called immediately when the engine detects them occurring:
        event_create
        event_animation_end
        event_destroy
        event_alarm

    The following events are always called (in no particular order)
    between calls of event_step and event_step_end:
        event_collision
        event_collision_left
        event_collision_right
        event_collision_top
        event_collision_bottom

    """

    def __init__(self, x, y, z, sprite=None, visible=True,
                 detects_collisions=True, bbox_x=None, bbox_y=None,
                 bbox_width=None, bbox_height=None, collision_ellipse=False,
                 collision_precise=False, id_=None, **kwargs):
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
        if 'id' in kwargs:
            id_ = kwargs['id']

        self.x = x
        self.y = y
        self.z = z
        self.sprite = sprite
        self.visible = visible
        self.detects_collisions = detects_collisions
        self.bbox_x = bbox_x if bbox_x is not None else sprite.bbox_x
        self.bbox_y = bbox_y if bbox_y is not None else sprite.bbox_y
        self.bbox_width = (bbox_width if bbox_width is not None else
                           sprite.bbox_width)
        self.bbox_height = (bbox_height if bbox_height is not None else
                            sprite.bbox_height)
        self.collision_ellipse = collision_ellipse
        self.collision_precise = collision_precise
        self.id = id_

        self._rect = pygame.Rect(self.bbox_x, self.bbox_y, self.bbox_width,
                                 self.bbox_height)
        self._set_mask()

    def collides(self, other, x=None, y=None):
        """Return whether or not this object collides with another.

        ``other`` indicates the object to check for a collision with, or
        the name of said object.  ``other`` can also be a class to check
        for collisions with.

        ``x`` and ``y``, indicate the position to check for collisions
        at.  If unspecified or None, this object's current position will
        be used.

        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        # Change x and y to be offset values; these are easier to use.
        x -= self.x
        y -= self.y

        if (self.collision_precise or self.collision_ellipse or
                other.collision_precise or other.collision_ellipse):
            # Use masks.
            self_rect = pygame.Rect(round(self.bbox_left + x),
                                    round(self.bbox_top + y),
                                    self.bbox_width, self.bbox_height)
            other_rect = pygame.Rect(round(other.bbox_left),
                                     round(other.bbox_top),
                                     other.bbox_width, other.bbox_height)
            collide_rect = self_rect.clip(other_rect)

            self_xoffset = collide_rect.left - self_rect.left
            self_yoffset = collide_rect.top - self_rect.top
            other_xoffset = collide_rect.left - other_rect.left
            other_yoffset = collide_rect.top - other_rect.top

            for a in xrange(collide_rect.w):
                for b in xrange(collide_rect.h):
                    if (self._hitmask[a + self_xoffset][b + self_yoffset] and
                        other._hitmask[a + other_xoffset][b + other_yoffset]):
                        return True

            return False
                    
        else:
            # Use bounding boxes.
            return (self.bbox_left + x < other.bbox_right and
                    self.bbox_right + x > other.bbox_left and
                    self.bbox_top + y < other.bbox_bottom and
                    self.bbox_bottom + y > other.bbox_top)

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Set the alarm with the given ``alarm_id`` with the given
        ``value``.  The alarm will then count down until it reaches 0
        and set off the alarm event with the same ID.  ``alarm_id`` can
        be any value.  ``value`` should be a number greater than 0.  You
        can also set ``value`` to None to disable the alarm.

        """
        pass

    def destroy(self):
        """Destroy the object."""
        pass

    def event_create(self):
        """Create event."""
        pass

    def event_animation_end(self):
        """Animation End event."""
        pass

    def event_destroy(self):
        """Destroy event."""
        pass

    def event_step_begin(self):
        """Begin Step event."""
        pass

    def event_alarm(self, alarm_id):
        """Alarm event.

        ``alarm_id`` is the ID of the alarm that was set off.

        """
        pass

    def event_step(self):
        """Step event."""
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

    def event_step_end(self):
        """End step event."""
        pass

    def event_draw(self):
        """Draw event."""
        pass

    def _set_mask(self):
        # Properly set the hit mask based on the collision settings.
        if self.collision_ellipse:
            # Elliptical mask based on bounding box.
            # TODO
            pass
        elif self.collision_precise:
            # Mask based on opacity of the current image.
            left = self.bbox_x + self.sprite.origin_x
            right = left + self.bbox_width
            top = self.bbox_y + self.sprite.origin_y
            bottom = top + self.bbox_height

            mask = self.sprite._get_precise_mask(self.image_index)[left:right]
            for i in xrange(len(mask)):
                mask[i] = mask[i][top:bottom]

            self._hitmask = mask
        else:
            # Mask is all pixels in the bounding box.
            self._hitmask = [[True for j in xrange(self.bbox_height)]
                             for i in xrange(self.bbox_width)]


class Mouse(StellarClass):

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

    Room events are handled by special methods.  The following events
    happen each frame in the following order and are synchronized among
    all objects which have them:
        event_step_begin
        event_step
        event_step_end

    The following events are not timed in any particular way, but are
    called immediately when the engine detects them occurring:
        event_room_start
        event_room_end

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
        self.width = width
        self.height = height
        self._start_width = width
        self._start_height = height

        if views is not None:
            self.views = list(views)
        else:
            self.views = [View(0, 0)]
        self._start_views = self.views

        if background is not None:
            self.background = background
        else:
            self.background = Background((), 'black')
        self._start_background = self.background

        real_objects = []
        for obj in objects:
            if isinstance(obj, StellarClass):
                real_objects.append(obj)
            else:
                real_objects.append(game.objects[obj])
        self.objects = tuple(real_objects)
        self._start_objects = self.objects

        self.room_number = len(game.rooms)
        game.rooms.append(self)

        self._started = False

    def add(self, obj):
        """Add a StellarClass object to the room.

        ``obj`` is the StellarClass object to add.  It can also be an
        object's ID.

        """
        pass

    def start(self):
        """Start the room.

        If the room has been changed, reset it to its original state.

        """
        self._reset()
        self.event_room_start()
        self.resume()

    def resume(self):
        """Continue the room from where it left off.

        If the room is unchanged (e.g. has not been started yet), this
        method behaves in the same way that Room.start does.

        """
        game.current_room = self
        game.pygame_sprites.kill()

        for obj in self.objects:
            game.pygame_sprites.add(obj.pygame_sprite)
            if self._started:
                obj.event_create()

        self._started = True

    def end(self):
        """Go to the next room.

        If this room is the last room, the game is ended.  Note that
        this does not reset the state of the room.

        """
        pass

    def event_room_start(self):
        """Room start event."""
        pass

    def event_room_end(self):
        """Room end event."""
        pass

    def event_step_begin(self):
        """Room begin step event."""
        pass

    def event_step(self):
        """Room step event."""
        pass

    def event_step_end(self):
        """Room end step event."""
        pass

    def _reset(self):
        # Reset the room to its original state.
        self._started = False
        self.width = self._start_width
        self.height = self._start_height
        self.views = self._start_views
        self.background = self._start_background
        self.objects = self._start_objects

        for view in self.views:
            view._reset()

        for obj in self.objects:
            obj._reset()


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
        self.x = x
        self.y = y
        self.xport = xport
        self.yport = yport
        self.width = width if width else game.width - xport
        self.height = height if height else game.height - yport


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
        self.image = parent.sprite._get_image(
            parent.image_index, parent.image_xscale, parent.image_yscale)
        self.rect = self.image.get_rect()
        self._update_rect()
        self.dirty = 1

    def update(self):
        if self.parent() is not None:
            new_image = self.parent().sprite._get_image(
                self.parent().image_index, self.parent().image_xscale,
                self.parent().image_yscale)
            if self.image != new_image:
                self.image = new_image
                self.dirty = 1

            self._update_rect()
        else:
            self.kill()

    def _update_rect(self):
        views = game.current_room.views
        if (len(views) == 1 and views[0].xport == 0 and views[0].yport == 0 and
                views[0].width == game.width and
                views[0].height == game.height):
            # There is only one view that takes up the whole screen, so
            # we don't need to worry about it.
            x = self.parent().x - views[0].x - self.parent().sprite.origin_x
            y = self.parent().y - views[0].y - self.parent().sprite.origin_y
            new_rect = self.image.get_rect()
            new_rect.left = round(x * game._xscale)
            new_rect.top = round(y * game._yscale)

            if self.rect != new_rect:
                self.rect = new_rect
                self.dirty = 1
        else:
            # There is something more complicated.  Have to account for
            # the possibility of edges or multiple appearances.
            original_used = False
            self.dirty = 1
            for view in views:
                x = self.parent().x - view.x - self.parent().sprite.origin_x
                y = self.parent().y - view.y - self.parent().sprite.origin_y
                w = self.image.get_width()
                h = self.image.get_height()
                new_rect = self.image.get_rect()
                new_rect.left = round(x * game._xscale)
                new_rect.top = round(y * game._yscale)
                inside_view = (x >= view.xport and
                               x + w <= view.xport + view.width and
                               y >= view.yport and
                               y + h <= view.yport + view.height)

                if not original_used and inside_view:
                    original_used = True
                    if self.rect == new_rect:
                        self.dirty = 0
                    else:
                        self.rect = new_rect
                else:
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

                        x = round(x * game._xscale)
                        y = round(y * game._yscale)
                        cut_x = round(cut_x * game._xscale)
                        cut_y = round(cut_y * game._yscale)
                        w = round(w * game._xscale)
                        h = round(h * game._yscale)
                        cut_rect = pygame.Rect(cut_x, cut_y, w, h)
                        img.self.image.subsurface(cut_rect)
                        rect = pygame.Rect(x, y, w, h)

                    # Create proxy one-time sprite
                    proxy = _PygameOneTimeSprite(img, rect)
                    game._pygame_sprites.add(proxy, layer=self.parent().z)


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


def _scale(surface, width, height):
    # Scale the given surface to the given width and height, taking the
    # scale factor of the screen into account.
    width *= game._xscale
    height *= game._yscale

    if game.scale_smooth:
        try:
            new_surf = pygame.transform.smoothscale(surface, (width, height))
        except pygame.error:
            new_surf = pygame.transform.scale(surface, (width, height))
    else:
        new_surf = pygame.transform.scale(surface, (width, height))

    return new_surf

