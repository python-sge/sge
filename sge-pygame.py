#!/usr/bin/env python

# Stellar Game Engine - Pygame
# Copyright (C) 2012 Julian Marchant <onpon4@lavabit.com>
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
    ALIGN_LEFT: Flag indicating alignment to the left.
    ALIGN_CENTER: Flag indicating alignment to the horizontal center.
    ALIGN_RIGHT: Flag indicating alignment to the right.
    ALIGN_TOP: Flag indicating alignment to the top.
    ALIGN_MIDDLE: Flag indicating alignment to the vertical middle.
    ALIGN_BOTTOM: Flag indicating alignment to the bottom.
    KEYS: A dictionary containing the keycodes of all keys.
    KEYNAMES: A dictionary containing the key names of all keycodes
        (i.e. the reverse of KEYS).

Global variables are stored in the container ``glob``.  See glob.__doc__
for more information.

Classes:
    Sprite: Class used to store images and animations.
    BackgroundLayer: Class used to store a background layer.
    Background: Class used to store parallax-scrolling backgrounds.
    Font: Class used to store and handle fonts.
    Sound: Class used to store and play sound effects.
    Music: Class used to store and play music.
    StellarClass: Class used for game objects.
    Room: Class used for game rooms, e.g. levels.

Stellar Game Engine uses "events" to let you know when something has
happened.  They are implemented as functions.  Global events available
are:
    event_game_start
    event_game_end
    event_step
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

Other functions:
    init: Initialize Stellar Game Engine.
    restart_game: Restart the game.
    end_game: End the game.
    set_mode: Set the display mode.
    sound_stop_all: Stop all sounds that are currently playing.
    pause: Pause the game.
    unpause: Unpause the game.

Implementation-specific information:
Music supports MP3 and MOD music as well as Ogg.  For starting position
in MOD music, the pattern order number is used instead of a number of
milliseconds.  Other formats may also be accepted depending on the
system.

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.0.1"

import sys
import os
import math
import json

import pygame

# Except in extreme cases, these constants should not be modified.
DEFAULT_SCREENSIZE = (640, 480)
DEFAULT_FULLSCREEN = False
DEFAULT_SCALE = 0
DEFAULT_SCALE_PROPORTIONAL = True
DEFAULT_SCALE_SMOOTH = False
DEFAULT_FPS = 60
DEFAULT_DELTA = False
DEFAULT_DELTA_MIN = 15
COLORS = {'white':'#ffffff', 'silver':'#c0c0c0', 'gray':'#808080',
          'black':'#000000', 'red':'#ff0000', 'maroon':'#800000',
          'yellow':'#ffff00', 'olive':'#808000', 'lime':'#00ff00',
          'green':'#008000', 'aqua':'#00ffff', 'teal':'#008080',
          'blue':'#0000ff', 'navy':'#000080', 'fuchsia':'#ff00ff',
          'purple':'#800080'}

ALIGN_LEFT = 2
ALIGN_CENTER = 3
ALIGN_RIGHT = 1
ALIGN_TOP = 2
ALIGN_MIDDLE = 3
ALIGN_BOTTOM = 1
KEYS = {"0":pygame.K_0, "1":pygame.K_1, "2":pygame.K_2, "3":pygame.K_3, "4":pygame.K_4, "5":pygame.K_5, "6":pygame.K_6, "7":pygame.K_7, "8":pygame.K_8, "9":pygame.K_9, "a":pygame.K_a, "b":pygame.K_b, "c":pygame.K_c, "d":pygame.K_d, "e":pygame.K_e, "f":pygame.K_f, "g":pygame.K_g, "h":pygame.K_h, "i":pygame.K_i, "j":pygame.K_j, "k":pygame.K_k, "l":pygame.K_l, "m":pygame.K_m, "n":pygame.K_n, "o":pygame.K_o, "p":pygame.K_p, "q":pygame.K_q, "r":pygame.K_r, "s":pygame.K_s, "t":pygame.K_t, "u":pygame.K_u, "v":pygame.K_v, "w":pygame.K_w, "x":pygame.K_x, "y":pygame.K_y, "z":pygame.K_z, "alt_left":pygame.K_LALT, "alt_right":pygame.K_RALT, "ampersand":pygame.K_AMPERSAND, "apostrophe":pygame.K_QUOTE, "asterisk":pygame.K_ASTERISK, "at":pygame.K_AT, "backslash":pygame.K_BACKSLASH, "backspace":pygame.K_BACKSPACE, "backtick":pygame.K_BACKQUOTE, "bracket_left":pygame.K_LEFTBRACKET, "bracket_right":pygame.K_RIGHTBRACKET, "break":pygame.K_BREAK, "caps_lock":pygame.K_CAPSLOCK, "caret":pygame.K_CARET, "clear":pygame.K_CLEAR, "colon":pygame.K_COLON, "comma":pygame.K_COMMA, "ctrl_left":pygame.K_LCTRL, "ctrl_right":pygame.K_RCTRL, "delete":pygame.K_DELETE, "dollar":pygame.K_DOLLAR, "down":pygame.K_DOWN, "end":pygame.K_END, "enter":pygame.K_RETURN, "equals":pygame.K_EQUALS, "escape":pygame.K_ESCAPE, "euro":pygame.K_EURO, "exclamation":pygame.K_EXCLAIM, "f1":pygame.K_F1, "f2":pygame.K_F2, "f3":pygame.K_F3, "f4":pygame.K_F4, "f5":pygame.K_F5, "f6":pygame.K_F6, "f7":pygame.K_F7, "f8":pygame.K_F8, "f9":pygame.K_F9, "f10":pygame.K_F10, "f11":pygame.K_F11, "f12":pygame.K_F12, "greater_than":pygame.K_GREATER, "hash":pygame.K_HASH, "help":pygame.K_HELP, "home":pygame.K_HOME, "hyphen":pygame.K_MINUS, "insert":pygame.K_INSERT, "kp_0":pygame.K_KP_0, "kp_1":pygame.K_KP_1, "kp_2":pygame.K_KP_2, "kp_3":pygame.K_KP_3, "kp_4":pygame.K_KP_4, "kp_5":pygame.K_KP_5, "kp_6":pygame.K_KP_6, "kp_7":pygame.K_KP_7, "kp_8":pygame.K_KP_8, "kp_9":pygame.K_KP_9, "kp_divide":pygame.K_KP_DIVIDE, "kp_enter":pygame.K_KP_ENTER, "kp_equals":pygame.K_KP_EQUALS, "kp_minus":pygame.K_KP_MINUS, "kp_multiply":pygame.K_KP_MULTIPLY, "kp_plus":pygame.K_KP_PLUS, "kp_point":pygame.K_KP_PERIOD, "left":pygame.K_LEFT, "less_than":pygame.K_LESS, "menu":pygame.K_MENU, "meta_left":pygame.K_LMETA, "meta_right":pygame.K_RMETA, "mode":pygame.K_MODE, "num_lock":pygame.K_NUMLOCK, "pagedown":pygame.K_PAGEDOWN, "pageup":pygame.K_PAGEUP, "parenthesis_left":pygame.K_LEFTPAREN, "parenthesis_right":pygame.K_RIGHTPAREN, "pause":pygame.K_PAUSE, "period":pygame.K_PERIOD, "plus":pygame.K_PLUS, "power":pygame.K_POWER, "print_screen":pygame.K_PRINT, "question":pygame.K_QUESTION, "quote":pygame.K_QUOTEDBL, "right":pygame.K_RIGHT, "scroll_lock":pygame.K_SCROLLOCK, "semicolon":pygame.K_SEMICOLON, "shift_left":pygame.K_LSHIFT, "shift_right":pygame.K_RSHIFT, "slash":pygame.K_SLASH, "space":pygame.K_SPACE, "super_left":pygame.K_LSUPER, "super_right":pygame.K_RSUPER, "sysrq":pygame.K_SYSREQ, "tab":pygame.K_TAB, "underscore":pygame.K_UNDERSCORE, "up":pygame.K_UP}
KEYNAMES = {}
for pair in KEYS.items():
    KEYNAMES[pair[1]] = pair[0]


class glob(object):

    """Container class for "global" variables.

    Display settings (do not take effect until set_mode is called):
        screensize: A two-part tuple indicating the size of the screen,
            with the first value indicating the horizontal size and the
            second value indicating the vertical size, in pixels.
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

    Frame rate settings:
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

    Read-only variables:
        mouse_x: The horizontal position of the mouse relative to the
            top-left corner of the display.
        mouse_y: The vertical position of the mouse relative to the
            top-left corner of the display.
        mouse_xprevious: The previous horizontal position of the mouse.
        mouse_yprevious: The previous vertical position of the mouse.

    """

    # Display settings
    screensize = DEFAULT_SCREENSIZE
    fullscreen = DEFAULT_FULLSCREEN
    scale = DEFAULT_SCALE
    scale_proportional = DEFAULT_SCALE_PROPORTIONAL
    scale_smooth = DEFAULT_SCALE_SMOOTH

    # Frame rate settings
    fps = DEFAULT_FPS
    delta = DEFAULT_DELTA
    delta_min = DEFAULT_DELTA_MIN

    # Controls
    mouse_x = 0
    mouse_y = 0
    mouse_xprevious = 0
    mouse_yprevious = 0

    # Implementation-specific variables
    music_queue = []


class Sprite(object):

    """Class which holds information for images and animations.

    All sprite objects have the following properties:
        size: A two-part tuple indicating the size of the sprite in the
            form (x, y).
        origin: A two-part tuple indicating the location of the origin
            (the pixel position in relation to the images to base
            rendering on) in the form (x, y).
        transparent: True if the image should support transparency,
            False otherwise.  If the image does not have an alpha
            channel or if the implementation used does not support alpha
            transparency, a colorkey will be used, with the transparent
            color being the color of the top-rightmost pixel.
        fps: The suggested rate in frames per second to animate the
            image at.
        bbox: A tuple in the form (x, y, width, height) indicating the
            suggested bounding box to use with this sprite.

    """

    def __init__(self, name, size=None, origin=(0, 0),
                 transparent=True, fps=DEFAULT_FPS, bbox=None):
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
        rectangle will be created at the size specified by ``size``.  If
        ``size`` is None, it will default to (16, 16) in this case.

        All remaining arguments set the initial properties of the
        sprite; see Sprite.__doc__ for more information.  If ``size``
        or ``bbox`` is set to None, the respective property will be
        the size of the largest animation frame.

        """
        self.size = size
        self.origin = origin
        self.transparent = transparent
        self.fps = fps
        self.bbox = bbox


class BackgroundLayer(object):

    """Special class used for background layers.

    All BackgroundLayer objects have the following properties:
        sprite: The Sprite object used for this layer.
        x: The horizontal offset of the background.
        y: The vertical offset of the background.
        xscroll_rate: The horizontal speed the layer scrolls as a factor
            of the view scroll speed.
        yscroll_rate: The vertical speed the layer scrolls as a factor
            of the view scroll speed.

    """

    def __init__(self, sprite, x, y, xscroll_rate=1, yscroll_rate=1):
        """Create a background layer object.

        Arguments set the properties of the layer.  See
        BackgroundLayer.__doc__ for more information.

        """
        self.sprite = sprite
        self.x = x
        self.y = y
        self.xscroll_rate = xscroll_rate
        self.yscroll_rate = yscroll_rate


class Background(object):

    """Background class.

    All Background objects have the following properties:

        layers: A tuple containing all BackgroundLayer objects used in
            this background.
        color: A Stellar Game Engine color used in parts of the
            background where there is no layer.
        xrepeat: Whether or not the background should be repeated
            horizontally.
        yrepeat: Whether or not the background should be repeated
            vertically.

    """

    def __init__(self, layers, color, xrepeat=True, yrepeat=True):
        """Create a background with the given color and layers.

        Arguments set the properties of the background.  See
        Background.__doc__ for more information.

        """
        self.color = color
        self.layers = layers
        self.xrepeat = xrepeat
        self.yrepeat = yrepeat


class Font(object):

    """Font handling class.

    All Font objects have the following properties:
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

    All Sound objects have the following properties:
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

    All Music objects have the following properties:
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

    All StellarClass objects have the following properties:
        x: The horizontal position of the object in the room, where the
            left edge is 0 and x increases toward the right.
        y: The vertical position of the object in the room, where the
            top edge is 0 and y increases toward the bottom.
        sprite: The sprite currently in use by this object.  Set to None
            for no (visible) sprite.
        visible: Whether or not the object should be drawn.
        bbox: A tuple in the form (x, y, width, height) indicating the
            rectangle used for collisions, where x and y are relative to
            the object's ``x`` and ``y`` attributes.  If set to None,
            the sprite's suggested bounding box will be used.
        collision_ellipse: Whether or not an ellipse (rather than a
            rectangle) should be used for collision detection.
        collision_precise: Whether or not precise (pixel-perfect)
            collision detection should be used.
        bbox_left: The position of the left side of the bounding box.
        bbox_right: The position of the right side of the bounding box.
        bbox_top: The position of the top side of the bounding box.
        bbox_bottom: The position of the bottom side of the bounding
            box.
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

    StellarClass events are handled by special methods.  The event
    methods are:
        event_create
        event_animation_end
        event_destroy
        event_step_begin
        event_alarm
        event_step
        event_collision
        event_collision_left
        event_collision_right
        event_collision_top
        event_collision_bottom
        event_step_end
        event_draw

    Other methods of StellarClass:
        set_alarm: Set an alarm.
        destroy: Destroy the object.

    """

    def __init__(self, x, y, sprite=None, visible=True, bbox=None,
                 collision_ellipse=False, collision_precise=False):
        """Create a new StellarClass object.

        Arguments set the properties of the object.  See
        StellarClass.__doc__ for more information.

        """
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

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Set the alarm with the given ``alarm_id`` with the given
        ``value``.  The alarm will then count down until it reaches 0
        and set off the alarm event with the same ID.  ``alarm_id`` can
        be any value.  ``value`` should be a number greater than 0.  You
        can also set ``value`` to None to disable the alarm.

        """
        pass


class Room(object):

    """Class for rooms.

    All Room objects have the following properties:
        objects: A tuple containing all StellarClass objects in the
            room.
        width: The width of the room in pixels.
        height: The height of the room in pixels.
        background: The Background object used.
        persistent: Whether or not the room should remember its state
            when it is left.

    Room events are handled by special methods. The event methods are:
        event_room_start
        event_room_end

    Other methods of Room:
        add: Add a StellarClass object to the room.
        restart: Reset the room to its original state.

    """

    def __init__(self, objects=(), width=DEFAULT_SCREENSIZE[0],
                 height=DEFAULT_SCREENSIZE[1], view=None, background=None,
                 persistent=False):
        """Create a new Room object.

        Arguments set the properties of the room.  See Room.__doc__ for
        more information.

        """
        self.objects = objects
        self.width = width
        self.height = height
        self.view = view
        self.background = background
        self.persistent = persistent

    def event_room_start(self):
        """Room start event."""
        pass

    def event_room_end(self):
        """Room end event."""
        pass

    def add(self, obj):
        """Add a StellarClass object to the room.

        ``obj`` is the StellarClass object to add.

        """
        pass

    def restart(self):
        """Reset the room to its original state."""
        pass


class View(object):

    """Class for room views.

    All View objects have the following properties:
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

        """
        pass


def event_game_start():
    """Game start event."""
    pass


def event_game_end():
    """Game end event."""
    pass


def event_step():
    """Global step event."""
    pass


def event_key_press(key):
    """Key press event.

    ``key`` is the key that was pressed.

    """
    pass


def event_key_release(key):
    """Key release event.

    ``key`` is the key that was pressed.

    """
    pass


def event_mouse_move(x, y):
    """Mouse move event.

    ``x`` and ``y`` indicate the relative movement of the mouse.

    """
    pass


def event_mouse_button_press(button):
    """Mouse button press event.

    ``button`` is the number of the mouse button that was pressed, where
    0 is the first mouse button.

    """
    pass


def event_mouse_button_release(button):
    """Mouse button release event.

    ``button`` is the number of the mouse button that was released,
    where 0 is the first mouse button.

    """
    pass


def event_joystick_axis_move(joystick, axis, value):
    """Joystick axis move event.

    ``joystick`` is the number of the joystick, where 0 is the first
    joystick.  ``axis`` is the number of the axis, where 0 is the first
    axis.  ``value`` is the tilt of the axis, where 0 is in the center,
    -1 is tilted all the way to the left or up, and 1 is tilted all the
    way to the right or down.

    Support for joysticks in Stellar Game Engine implementations is
    optional.

    """
    pass


def event_joystick_hat_move(joystick, hat, x, y):
    """Joystick HAT move event.

    ``joystick`` is the number of the joystick, where 0 is the first
    joystick.  ``hat`` is the number of the HAT, where 0 is the first
    HAT.  ``x`` and ``y`` indicate the position of the HAT, where 0 is
    in the center, -1 is left or up, and 1 is right or down.

    Support for joysticks in Stellar Game Engine implementations is
    optional.

    """
    pass


def event_joystick_button_press(joystick, button):
    """Joystick button press event.

    ``joystick`` is the number of the joystick, where 0 is the first
    joystick.  ``button`` is the number of the button pressed, where 0
    is the first button.

    Support for joysticks in Stellar Game Engine implementations is
    optional.

    """
    pass


def event_joystick_button_release(joystick, button):
    """Joystick button release event.

    ``joystick`` is the number of the joystick, where 0 is the first
    joystick.  ``button`` is the number of the button pressed, where 0
    is the first button.

    Support for joysticks in Stellar Game Engine implementations is
    optional.

    """
    pass


def event_close():
    """Close event (e.g. close button)."""
    pass


def init(screensize=DEFAULT_SCREENSIZE, fullscreen=DEFAULT_FULLSCREEN,
         scale=DEFAULT_SCALE, scale_proportional=DEFAULT_SCALE_PROPORTIONAL,
         scale_smooth=DEFAULT_SCALE_SMOOTH, fps=DEFAULT_FPS,
         delta=DEFAULT_DELTA, delta_min=DEFAULT_DELTA_MIN):
    """Initialize the Stellar Game Engine.  Must be called first.

    Arguments indicate the initial settings used.  See glob.__doc__ for
    information about the settings.

    """
    pygame.init()


def restart_game():
    """Restart the game."""
    pass


def end_game():
    """Properly end the game"""
    pygame.quit()


def set_mode(screensize=None, fullscreen=None, scale=None,
             scale_proportional=None, scale_smooth=None):
    """Set the mode of the screen.

    Use any arguments specified that are not None to change the display
    settings and then do whatever is necessary to cause those changes to
    take effect on the screen.  Arguments which are not set or are set
    to None are unchanged.

    See glob.__doc__ for information about the settings.

    """
    pass


def draw_dot(x, y, color):
    """Draw a single-pixel dot.

    ``x`` and ``y`` indicate the location in the room to draw the dot,
    where the left and top edges of the room are 0 and x and y increase
    toward the right and bottom.  ``color`` indicates the color of the
    dot.

    """


def draw_line(x1, y1, x2, y2, color, thickness=1, anti_alias=False):
    """Draw a line segment between the given points.

    ``x1``, ``y1``, ``x2``, and ``y2`` indicate the location in the
    room of the points between which to draw the line segment, where
    the left and top edges of the room are 0 and x and y increase
    toward the right and bottom.  ``color`` indicates the color of the
    line segment.  ``thickness`` indicates the thickness of the line
    segment in pixels.  ``anti_alias`` indicates whether or not
    anti-aliasing should be used.

    Support for anti-aliasing is optional in Stellar Game Engine
    implementations.  If the implementation used does not support
    anti-aliasing, this function will act like ``anti_alias`` is False.

    """
    pass


def draw_rectangle(x, y, width, height, fill=None, outline=None,
                   outline_thickness=1):
    """Draw a rectangle at the given position.

    ``x`` and ``y`` indicate the location in the room to draw the
    rectangle, where the left and top edges of the room are 0 and x and
    y increase toward the right and bottom.  ``width`` and ``height``
    indicate the size of the rectangle.  ``fill`` indicates the color
    of the fill of the rectangle; set to None for no fill.  ``outline``
    indicates the color of the outline of the rectangle; set to None for
    no outline.  ``outline_thickness`` indicates the thickness of the
    outline in pixels (ignored if there is no outline).  ``anti_alias``
    indicates whether or not anti-aliasing should be used on the
    outline.

    Support for anti-aliasing is optional in Stellar Game Engine
    implementations.  If the implementation used does not support
    anti-aliasing, this function will act like ``anti_alias`` is False.

    """


def draw_ellipse(x, y, width, height, fill=None, outline=None,
                 outline_thickness=1):
    """Draw an ellipse at the given position.

    ``x`` and ``y`` indicate the location in the room to draw the
    ellipse, where the left and top edges of the room are 0 and x and
    y increase toward the right and bottom.  ``width`` and ``height``
    indicate the size of the ellipse.  ``fill`` indicates the color
    of the fill of the ellipse; set to None for no fill.  ``outline``
    indicates the color of the outline of the ellipse; set to None for
    no outline.  ``outline_thickness`` indicates the thickness of the
    outline in pixels (ignored if there is no outline).  ``anti_alias``
    indicates whether or not anti-aliasing should be used on the
    outline.

    Support for anti-aliasing is optional in Stellar Game Engine
    implementations.  If the implementation used does not support
    anti-aliasing, this function will act like ``anti_alias`` is False.

    """


def draw_circle(x, y, radius, fill=None, outline=None, outline_thickness=1):
    """Draw a circle at the given position.

    ``x`` and ``y`` indicate the location in the room to draw the
    circle, where the left and top edges of the room are 0 and x and
    y increase toward the right and bottom.  ``radius`` indicates the
    radius of the circle in pixels.  ``fill`` indicates the color of the
    fill of the circle; set to None for no fill.  ``outline`` indicates
    the color of the outline of the circle; set to None for no outline.
    ``outline_thickness`` indicates the thickness of the outline in
    pixels (ignored if there is no outline).  ``anti_alias`` indicates
    whether or not anti-aliasing should be used on the outline.

    Support for anti-aliasing is optional in Stellar Game Engine
    implementations.  If the implementation used does not support
    anti-aliasing, this function will act like ``anti_alias`` is False.

    """


def sound_stop_all():
    """Stop playback of all sounds."""
    pass


def pause(image=None):
    """Pause the game.

    ``image`` is the image to show when the game is paused.  If set to
    None, the default image will be shown.  The default image is at the
    discretion of the Stellar Game Engine implementation, as are any
    additional visual effects, with the stipulation that the following
    conditions are met:

        1. The default image must unambiguously demonstrate that the
            game is paused (the easiest way to do this is to include the
            word "paused" somewhere in the image).
        2. The view must stay in place.
        3. What was going on within the view before the game was paused
            must remain visible while the game is paused.

    """
    pass


def unpause():
    """Unpause the game."""
    pass


def set_mouse_cursor(sprite):
    """Set the mouse cursor.

    ``sprite`` is the sprite to set the mouse cursor as.

    """
    pass


def get_key_pressed(key):
    """Return whether or not a given key is pressed.

    ``key`` is the key to check.

    """
    return pygame.key.get_pressed()[key]


def get_mouse_button_pressed(button):
    """Return whether or not a given mouse button is pressed.

    ``button`` is the number of the mouse button to check, where 0 is
    the first mouse button.

    """
    pass


def get_joystick_axis(joystick, axis):
    """Return the position of the given axis.

    ``joystick`` is the number of the joystick to check, where 0 is the
    first joystick.  ``axis`` is the number of the axis to check, where
    0 is the first axis of the joystick.

    Returned value is a float from -1 to 1, where 0 is centered, -1 is
    all the way to the left or up, and 1 is all the way to the right or
    down.

    If the joystick or axis requested does not exist, 0 is returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support joysticks,
    this function will act like the joystick requested does not exist.

    """
    pass


def get_joystick_hat(joystick, hat):
    """Return the position of the given HAT.

    ``joystick`` is the number of the joystick to check, where 0 is the
    first joystick.  ``hat`` is the number of the HAT to check, where 0
    is the first HAT of the joystick.
    
    Returned value is a tuple in the form (x, y), where x is the
    horizontal position and y is the vertical position.  Both x and y
    are 0 (centered), -1 (left or up), or 1 (right or down).

    If the joystick or HAT requested does not exist, (0, 0) is returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support joysticks,
    this function will act like the joystick requested does not exist.

    """
    pass


def get_joystick_button_pressed(joystick, button):
    """Return whether or not the given button is pressed.

    ``joystick`` is the number of the joystick to check, where 0 is the
    first joystick.  ``button`` is the number of the button to check,
    where 0 is the first button of the joystick.

    If the joystick or button requested does not exist, False is
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support joysticks,
    this function will act like the joystick requested does not exist.

    """
    pass


def get_joysticks():
    """Return the number of joysticks available.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support joysticks,
    this function will always return 0.

    """
    pass


def get_joystick_axes(joystick):
    """Return the number of axes available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is the
    first joystick.  If the given joystick does not exist, 0 will be
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support joysticks,
    this function will act like the joystick requested does not exist.

    """
    pass


def get_joystick_hats(joystick):
    """Return the number of HATs available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is the
    first joystick.  If the given joystick does not exist, 0 will be
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support joysticks,
    this function will act like the joystick requested does not exist.

    """
    pass


def get_joystick_buttons(joystick):
    """Return whether or not the given joystick exists.

    ``joystick`` is the number of the joystick to check, where 0 is the
    first joystick.  If the given joystick does not exist, 0 will be
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support joysticks,
    this function will act like the joystick requested does not exist.

    """
    pass

