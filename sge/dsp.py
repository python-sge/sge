# Copyright (C) 2012-2017 Julie Marchant <onpon4@riseup.net>
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

"""
This module provides classes related to the graphical display.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import math
import os
import sys
import traceback
import warnings

import pygame
import six

import sge
from sge import gfx, r
from sge.r import (
    _check_color, _scale, _get_blend_flags, _screen_blend, _set_mode,
    _handle_music, _get_dot_sprite, _get_line_sprite, _get_rectangle_sprite,
    _get_ellipse_sprite, _get_circle_sprite, _get_polygon_sprite, bl_update,
    bl_get_image, o_update, o_detect_collisions, o_update_collision_lists,
    o_update_object_areas, o_is_other, o_get_origin_offset, o_set_speed,
    s_get_image, s_get_precise_mask, s_from_text, tg_blit,
    r_get_rectangle_object_areas, r_set_object_areas, r_update_fade,
    r_update_dissolve, r_update_pixelate, r_update_wipe_left,
    r_update_wipe_right, r_update_wipe_up, r_update_wipe_down,
    r_update_wipe_upleft, r_update_wipe_upright, r_update_wipe_downleft,
    r_update_wipe_downright, r_update_wipe_matrix, r_update_iris_in,
    r_update_iris_out, v_limit)


__all__ = ["Game", "Room", "View", "Object"]


class Game(object):

    """
    This class handles most parts of the game which operate on a global
    scale, such as global game events.  Before anything else is done
    with the SGE, an object either of this class or of a class derived
    from it must be created.

    When an object of this class is created, it is automatically
    assigned to :data:`sge.game`.

    .. note::

       This class is designed to be used as a singleton.  Do not create
       multiple :class:`sge.dsp.Game` objects.  Doing so is unsupported
       and may cause errors.

    .. attribute:: width

       The width of the game's display.

    .. attribute:: height

       The height of the game's display.

    .. attribute:: fullscreen

       Whether or not the game should be in fullscreen mode.

    .. attribute:: scale

       A number indicating a fixed scale factor (e.g. ``1`` for no
       scaling, ``2`` for doubled size).  If set to :const:`None` or
       ``0``, scaling is automatic (causes the game to fit the window or
       screen).

       If a fixed scale factor is defined and the game is in fullscreen
       mode, the scale factor multiplied by :attr:`width` and
       :attr:`height` is used to suggest what resolution to use.

    .. attribute:: scale_proportional

       If set to :const:`True`, scaling is always proportional.  If set
       to :const:`False`, the image will be distorted to completely fill
       the game window or screen.  This has no effect unless
       :attr:`scale` is :const:`None` or ``0``.

    .. attribute:: scale_method

       A string indicating the type of scaling method to use.  Can be
       one of the following:

       - ``"noblur"`` -- Request a non-blurry scale method, generally
         optimal for pixel art.
       - ``"smooth"`` -- Request a smooth scale method, generally
         optimal for images other than pixel art.

       Alternatively, this attribute can be set to one of the values in
       :data:`sge.SCALE_METHODS` to request an exact scale method to
       use.

       The value of this attribute is only a request.  If this value is
       either an unsupported value or :const:`None`, the fastest
       available scale method is chosen.

    .. attribute:: fps

       The rate the game should run in frames per second.

       .. note::

          This is only the maximum; if the computer is not fast enough,
          the game may run more slowly.

    .. attribute:: delta

       Whether or not delta timing should be used.  Delta timing affects
       object speeds, animation rates, and alarms.

    .. attribute:: delta_min

       Delta timing can cause the game to be choppy.  This attribute
       limits this by pretending that the frame rate is never lower than
       this amount, resulting in the game slowing down like normal if it
       is.

    .. attribute:: delta_max

       Indicates a higher frame rate cap than :attr:`fps` to allow the
       game to reach by using delta timing to slow object speeds,
       animation rates, and alarms down.  If set to :const:`None`, this
       feature is disabled and the game will not be permitted to run
       faster than :attr:`fps`.

       This attribute has no effect unless :attr:`delta` is
       :const:`True`.

    .. attribute:: grab_input

       Whether or not all input should be forcibly grabbed by the game.
       If this is :const:`True` and :attr:`sge.mouse.visible` is
       :const:`False`, the mouse will be in relative mode.  Otherwise,
       the mouse will be in absolute mode.

    .. attribute:: window_text

       The text for the OS to display as the window title, e.g. in the
       frame of the window.  If set to :const:`None`, the SGE chooses
       the text.

    .. attribute:: window_icon

       The path to the image file to use as the window icon.  If set
       to :const:`None`, the SGE chooses the icon.  If the file
       specified does not exist, :exc:`OSError` is raised.

    .. attribute:: collision_events_enabled

       Whether or not collision events should be executed.  Setting this
       to :const:`False` will improve performence if collision events
       are not needed.

    .. attribute:: alarms

       A dictionary containing the global alarms of the game.  Each
       value decreases by 1 each frame (adjusted for delta timing if it
       is enabled).  When a value is at or below 0,
       :meth:`sge.dsp.Game.event_alarm` is executed with ``alarm_id``
       set to the respective key, and the item is deleted from this
       dictionary.

    .. attribute:: input_events

       A list containing all input event objects which have not yet been
       handled, in the order in which they occurred.

       .. note::

          If you handle input events manually, be sure to delete them
          from this list, preferably by getting them with
          :meth:`list.pop`.  Otherwise, the event will be handled more
          than once, which is usually not what you want.

    .. attribute:: start_room

       The room which becomes active when the game first starts and when
       it restarts.  Must be set exactly once, before the game first
       starts, and should not be set again afterwards.

    .. attribute:: current_room

       The room which is currently active.  (Read-only)

    .. attribute:: mouse

       A :class:`sge.dsp.Object` object which represents the mouse
       cursor.  Its bounding box is a one-pixel square.  It is
       automatically added to every room's default list of objects.

       Some of this object's attributes control properties of the mouse.
       See the documentation for :mod:`sge.mouse` for more information.

       (Read-only)
    """

    @property
    def width(self):
        return r.game_width

    @width.setter
    def width(self, value):
        if value != r.game_width:
            r.game_width = value
            _set_mode()

    @property
    def height(self):
        return r.game_height

    @height.setter
    def height(self, value):
        if value != r.game_height:
            r.game_height = value
            _set_mode()

    @property
    def fullscreen(self):
        return r.game_fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        if value != r.game_fullscreen:
            r.game_fullscreen = value
            _set_mode()
            if not self.fullscreen and not self.scale:
                old_scale = self.scale
                self.scale = 1
                self.scale = old_scale

    @property
    def scale(self):
        return r.game_scale

    @scale.setter
    def scale(self, value):
        if value != r.game_scale:
            r.game_scale = value
            _set_mode()

    @property
    def scale_proportional(self):
        return r.game_scale_proportional

    @scale_proportional.setter
    def scale_proportional(self, value):
        if value != r.game_scale_proportional:
            r.game_scale_proportional = value
            _set_mode()

    @property
    def scale_method(self):
        return r.game_scale_method

    @scale_method.setter
    def scale_method(self, value):
        if value != r.game_scale_method:
            r.game_scale_method = value
            _set_mode()

    @property
    def grab_input(self):
        return pygame.event.get_grab()

    @grab_input.setter
    def grab_input(self, value):
        pygame.event.set_grab(value)

    @property
    def window_text(self):
        return pygame.display.get_caption()[0]

    @window_text.setter
    def window_text(self, value):
        if value is not None:
            pygame.display.set_caption(value)

    @property
    def window_icon(self):
        return r.game_window_icon

    @window_icon.setter
    def window_icon(self, value):
        r.game_window_icon = value
        if value is not None:
            try:
                image = pygame.image.load(value)
            except pygame.error as e:
                raise OSError(e)
            else:
                pygame.display.set_icon(image)

    def __init__(self, width=640, height=480, fullscreen=False, scale=None,
                 scale_proportional=True, scale_method=None, fps=60,
                 delta=False, delta_min=15, delta_max=None, grab_input=False,
                 window_text=None, window_icon=None,
                 collision_events_enabled=True):
        """
        Arguments set the respective initial attributes of the game.
        See the documentation for :class:`sge.dsp.Game` for more
        information.

        The created :class:`sge.dsp.Game` object is automatically
        assigned to :data:`sge.game`.
        """
        # Settings use a smaller buffer size for less lag.
        pygame.mixer.pre_init(22050, -16, 2, 1024)
        pygame.init()

        pygame.mixer.music.set_endevent(sge.MUSIC_END_EVENT)

        r._display_info = pygame.display.Info()

        sge.game = self

        r.game_width = width
        r.game_height = height
        r.game_window_width = width
        r.game_window_height = height
        r.game_fullscreen = fullscreen
        r.game_scale = scale
        r.game_scale_proportional = scale_proportional
        r.game_scale_method = scale_method
        r.game_new_room = None
        self.fps = fps
        self.delta = delta
        self.delta_min = delta_min
        self.delta_max = delta_max
        self.window_text = window_text
        self.window_icon = window_icon
        self.collision_events_enabled = collision_events_enabled
        self.alarms = {}
        self.start_room = None

        self.input_events = []
        self.current_room = None

        r.game_display_surface = pygame.Surface((self.width, self.height))
        _set_mode()

        r.music = None
        r.music_queue = []
        r.game_running = False
        r.game_clock = pygame.time.Clock()
        r.game_window_projections = []
        self.mouse = Mouse()

        # Setup sound channels
        r.game_available_channels = []
        if pygame.mixer.get_init():
            for i in six.moves.range(pygame.mixer.get_num_channels()):
                r.game_available_channels.append(pygame.mixer.Channel(i))
        else:
            w = "pygame.mixer module not initialized! Are you missing SDL_mixer?"
            warnings.warn(w)

        # Setup joysticks
        sge.joystick.refresh()

        if not pygame.font.get_init():
            w = "pygame.font module not initialized! Are you missing SDL_ttf?"
            warnings.warn(w)

        self.window_icon = None

    def start(self):
        """
        Start the game.  Should only be called once; the effect of any
        further calls is undefined.
        """
        if self.start_room is not None:
            r.game_running = True
            self.start_room.start()
            r.game_clock.tick()

            while r.game_running:
                # Switch to new room (if one has been started)
                new_room = r.game_new_room
                if new_room is not None:
                    r.game_new_room = None
                    self.unpause()
                    self.current_room = new_room

                    r._colliders = []
                    r._collision_checkers = []
                    r._active_objects = set()

                    r_set_object_areas(new_room, False)
                    for obj in new_room.objects:
                        obj.rd["object_areas"] = set()
                        o_update_object_areas(obj)
                        o_update_collision_lists(obj)
                        if obj.active:
                            r._active_objects.add(obj)

                    # This is stored in a variable to prevent problems
                    # with rd["started"] being False during the
                    # start/create events.
                    started = new_room.rd["started"]
                    new_room.rd["started"] = True
                    if not started:
                        new_room.event_room_start()
                    else:
                        new_room.event_room_resume()

                    while new_room.rd["new_objects"]:
                        new_room.rd["new_objects"].pop(0).event_create()

                    # Prevent sudden movements from happening at the
                    # start of a room due to delta timing, and make sure
                    # transitions happen fully.
                    r.game_clock.tick()

                # Input events
                self.pump_input()
                while self.input_events:
                    event = self.input_events.pop(0)

                    if isinstance(event, sge.input.KeyPress):
                        self.event_key_press(event.key, event.char)
                        self.current_room.event_key_press(event.key,
                                                          event.char)
                        for obj in r._active_objects.copy():
                            obj.event_key_press(event.key, event.char)
                    elif isinstance(event, sge.input.KeyRelease):
                        self.event_key_release(event.key)
                        self.current_room.event_key_release(event.key)
                        for obj in r._active_objects.copy():
                            obj.event_key_release(event.key)
                    elif isinstance(event, sge.input.MouseMove):
                        self.event_mouse_move(event.x, event.y)
                        self.current_room.event_mouse_move(event.x, event.y)
                        for obj in r._active_objects.copy():
                            obj.event_mouse_move(event.x, event.y)
                    elif isinstance(event, sge.input.MouseButtonPress):
                        self.event_mouse_button_press(event.button)
                        self.current_room.event_mouse_button_press(
                            event.button)
                        for obj in r._active_objects.copy():
                            obj.event_mouse_button_press(event.button)
                    elif isinstance(event, sge.input.MouseButtonRelease):
                        self.event_mouse_button_release(event.button)
                        self.current_room.event_mouse_button_release(
                            event.button)
                        for obj in r._active_objects.copy():
                            obj.event_mouse_button_release(event.button)
                    elif isinstance(event, sge.input.JoystickAxisMove):
                        self.event_joystick_axis_move(
                            event.js_name, event.js_id, event.axis,
                            event.value)
                        self.current_room.event_joystick_axis_move(
                            event.js_name, event.js_id, event.axis,
                            event.value)
                        for obj in r._active_objects.copy():
                            obj.event_joystick_axis_move(
                                event.js_name, event.js_id, event.axis,
                                event.value)
                    elif isinstance(event, sge.input.JoystickHatMove):
                        self.event_joystick_hat_move(
                            event.js_name, event.js_id, event.hat, event.x,
                            event.y)
                        self.current_room.event_joystick_hat_move(
                            event.js_name, event.js_id, event.hat, event.x,
                            event.y)
                        for obj in r._active_objects.copy():
                            obj.event_joystick_hat_move(
                                event.js_name, event.js_id, event.hat, event.x,
                                event.y)
                    elif isinstance(event, sge.input.JoystickTrackballMove):
                        self.event_joystick_trackball_move(
                            event.js_name, event.js_id, event.ball, event.x,
                            event.y)
                        self.current_room.event_joystick_trackball_move(
                            event.js_name, event.js_id, event.ball, event.x,
                            event.y)
                        for obj in r._active_objects.copy():
                            obj.event_joystick_trackball_move(
                                event.js_name, event.js_id, event.ball,
                                event.x, event.y)
                    elif isinstance(event, sge.input.JoystickButtonPress):
                        self.event_joystick_button_press(
                            event.js_name, event.js_id, event.button)
                        self.current_room.event_joystick_button_press(
                            event.js_name, event.js_id, event.button)
                        for obj in r._active_objects.copy():
                            obj.event_joystick_button_press(
                                event.js_name, event.js_id, event.button)
                    elif isinstance(event, sge.input.JoystickButtonRelease):
                        self.event_joystick_button_release(
                            event.js_name, event.js_id, event.button)
                        self.current_room.event_joystick_button_release(
                            event.js_name, event.js_id, event.button)
                        for obj in r._active_objects.copy():
                            obj.event_joystick_button_release(
                                event.js_name, event.js_id, event.button)
                    elif isinstance(event, sge.input.JoystickEvent):
                        self.event_joystick(
                            event.js_name, event.js_id, event.input_type,
                            event.input_id, event.value)
                        self.current_room.event_joystick(
                            event.js_name, event.js_id, event.input_type,
                            event.input_id, event.value)
                        for obj in r._active_objects.copy():
                            obj.event_joystick(
                                event.js_name, event.js_id, event.input_type,
                                event.input_id, event.value)
                    elif isinstance(event, sge.input.KeyboardFocusGain):
                        self.event_gain_keyboard_focus()
                        self.current_room.event_gain_keyboard_focus()
                    elif isinstance(event, sge.input.KeyboardFocusLose):
                        self.event_lose_keyboard_focus()
                        self.current_room.event_lose_keyboard_focus()
                    elif isinstance(event, sge.input.MouseFocusGain):
                        self.event_gain_mouse_focus()
                        self.current_room.event_gain_mouse_focus()
                    elif isinstance(event, sge.input.MouseFocusLose):
                        self.event_lose_mouse_focus()
                        self.current_room.event_lose_mouse_focus()
                    elif isinstance(event, sge.input.QuitRequest):
                        self.current_room.event_close()
                        self.event_close()

                # Regulate speed
                real_time_passed = self.regulate_speed()

                if self.delta:
                    time_passed = min(real_time_passed, 1000 / self.delta_min)
                    delta_mult = time_passed / (1000 / self.fps)
                else:
                    time_passed = 1000 / self.fps
                    delta_mult = 1

                # Alarms
                activated_alarms = []
                for a in self.alarms:
                    self.alarms[a] -= delta_mult
                    if self.alarms[a] <= 0:
                        activated_alarms.append(a)
                for a in activated_alarms:
                    del self.alarms[a]
                    self.event_alarm(a)

                activated_alarms = []
                for a in self.current_room.alarms:
                    self.current_room.alarms[a] -= delta_mult
                    if self.current_room.alarms[a] <= 0:
                        activated_alarms.append(a)
                for a in activated_alarms:
                    del self.current_room.alarms[a]
                    self.current_room.event_alarm(a)

                # Step events
                self.event_step(real_time_passed, delta_mult)
                self.current_room.event_step(real_time_passed, delta_mult)

                # Update background layers
                for layer in self.current_room.background.layers:
                    bl_update(layer, time_passed)

                # Update objects (including mouse)
                for obj in r._active_objects.copy():
                    obj.event_begin_step(real_time_passed, delta_mult)
                    o_update(obj, time_passed, delta_mult)
                    obj.event_step(real_time_passed, delta_mult)

                if self.collision_events_enabled:
                    # Set objects' colliders
                    room = self.current_room
                    for obj in r._colliders:
                        obj.rd["colliders"] = []
                        for area in obj.rd["object_areas"]:
                            if area is not None:
                                i, j = area
                                room_area = room.object_areas[i][j]
                            else:
                                room_area = room.object_area_void

                            for other in room_area:
                                if (other is not obj and other.tangible and
                                        other not in obj.rd["colliders"]):
                                    obj.rd["colliders"].append(other)

                    # Detect collisions
                    for obj in r._collision_checkers:
                        o_detect_collisions(obj)

                # End step event
                for obj in r._active_objects.copy():
                    obj.event_end_step(real_time_passed, delta_mult)

                # Set xprevious and yprevious
                for obj in self.current_room.objects:
                    obj.xprevious = obj.x
                    obj.yprevious = obj.y

                # Transition
                rd = self.current_room.rd
                if rd["t_update"] is not None:
                    rd["t_time_passed"] += real_time_passed

                    if rd["t_time_passed"] < rd["t_duration"]:
                        complete = rd["t_time_passed"] / rd["t_duration"]
                        rd["t_update"](self.current_room, complete)
                        rd["t_complete_last"] = complete
                        self.project_sprite(rd["t_sprite"], 0, 0, 0)
                    else:
                        rd["t_update"] = None

                # Refresh
                self.refresh()
            else:
                pygame.quit()
                sge.game = None
        else:
            raise AttributeError("sge.game.start_room is undefined.")

    def end(self):
        """Properly end the game."""
        if self.current_room is not None:
            self.current_room.event_room_end()
        r.game_running = False

    def pause(self, sprite=None):
        """
        Pause the game.

        Arguments:

        - ``sprite`` -- The sprite to show in the center of the screen
          while the game is paused.  If set to :const:`None`, the SGE
          chooses the image.

        Normal events are not executed while the game is paused.
        Instead, events with the same name, but prefixed with
        ``event_paused_`` instead of ``event_`` are executed.  Note that
        not all events have these alternative "paused" events associated
        with them.
        """
        if sprite is None:
            font = gfx.Font("Droid Sans", size=64)
            sprite = gfx.Sprite.from_text(font, "Paused")

        r.game_paused = True

        while r.game_paused and r.game_running:
            # Input events
            self.pump_input()
            while self.input_events:
                event = self.input_events.pop(0)

                if isinstance(event, sge.input.KeyPress):
                    self.event_paused_key_press(event.key, event.char)
                    self.current_room.event_paused_key_press(event.key,
                                                             event.char)
                    for obj in self.current_room.objects:
                        obj.event_paused_key_press(event.key, event.char)
                elif isinstance(event, sge.input.KeyRelease):
                    self.event_paused_key_release(event.key)
                    self.current_room.event_paused_key_release(event.key)
                    for obj in self.current_room.objects:
                        obj.event_paused_key_release(event.key)
                elif isinstance(event, sge.input.MouseMove):
                    self.event_paused_mouse_move(event.x, event.y)
                    self.current_room.event_paused_mouse_move(event.x, event.y)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_move(event.x, event.y)
                elif isinstance(event, sge.input.MouseButtonPress):
                    self.event_paused_mouse_button_press(event.button)
                    self.current_room.event_paused_mouse_button_press(
                        event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_button_press(event.button)
                elif isinstance(event, sge.input.MouseButtonRelease):
                    self.event_paused_mouse_button_release(event.button)
                    self.current_room.event_paused_mouse_button_release(
                        event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_button_release(event.button)
                elif isinstance(event, sge.input.JoystickAxisMove):
                    self.event_paused_joystick_axis_move(
                        event.js_name, event.js_id, event.axis, event.value)
                    self.current_room.event_paused_joystick_axis_move(
                        event.js_name, event.js_id, event.axis, event.value)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_axis_move(
                            event.js_name, event.js_id, event.axis,
                            event.value)
                elif isinstance(event, sge.input.JoystickHatMove):
                    self.event_paused_joystick_hat_move(
                        event.js_name, event.js_id, event.hat, event.x,
                        event.y)
                    self.current_room.event_paused_joystick_hat_move(
                        event.js_name, event.js_id, event.hat, event.x,
                        event.y)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_hat_move(
                            event.js_name, event.js_id, event.hat,
                            event.x, event.y)
                elif isinstance(event, sge.input.JoystickTrackballMove):
                    self.event_paused_joystick_trackball_move(
                        event.js_name, event.js_id, event.ball, event.x,
                        event.y)
                    self.current_room.event_paused_joystick_trackball_move(
                        event.js_name, event.js_id, event.ball, event.x,
                        event.y)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_trackball_move(
                            event.js_name, event.js_id, event.ball,
                            event.x, event.y)
                elif isinstance(event, sge.input.JoystickButtonPress):
                    self.event_paused_joystick_button_press(
                        event.js_name, event.js_id, event.button)
                    self.current_room.event_paused_joystick_button_press(
                        event.js_name, event.js_id, event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_button_press(
                            event.js_name, event.js_id, event.button)
                elif isinstance(event, sge.input.JoystickButtonRelease):
                    self.event_paused_joystick_button_release(
                        event.js_name, event.js_id, event.button)
                    self.current_room.event_paused_joystick_button_release(
                        event.js_name, event.js_id, event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_button_release(
                            event.js_name, event.js_id, event.button)
                elif isinstance(event, sge.input.JoystickEvent):
                    self.event_paused_joystick(
                        event.js_name, event.js_id, event.input_type,
                        event.input_id, event.value)
                    self.current_room.event_paused_joystick(
                        event.js_name, event.js_id, event.input_type,
                        event.input_id, event.value)
                    for obj in r._active_objects.copy():
                        obj.event_paused_joystick(
                            event.js_name, event.js_id, event.input_type,
                            event.input_id, event.value)
                elif isinstance(event, sge.input.KeyboardFocusGain):
                    self.event_paused_gain_keyboard_focus()
                    self.current_room.event_paused_gain_keyboard_focus()
                elif isinstance(event, sge.input.KeyboardFocusLose):
                    self.event_paused_lose_keyboard_focus()
                    self.current_room.event_paused_lose_keyboard_focus()
                elif isinstance(event, sge.input.MouseFocusGain):
                    self.event_paused_gain_mouse_focus()
                    self.current_room.event_paused_gain_mouse_focus()
                elif isinstance(event, sge.input.MouseFocusLose):
                    self.event_paused_lose_mouse_focus()
                    self.current_room.event_paused_lose_mouse_focus()
                elif isinstance(event, sge.input.QuitRequest):
                    self.current_room.event_paused_close()
                    self.event_paused_close()

            # Regulate speed
            time_passed = self.regulate_speed()

            if self.delta:
                t = min(time_passed, 1000 / self.delta_min)
                delta_mult = t / (1000 / self.fps)
            else:
                delta_mult = 1

            self.event_paused_step(time_passed, delta_mult)
            self.current_room.event_paused_step(time_passed, delta_mult)
            for obj in self.current_room.objects[:]:
                obj.event_paused_step(time_passed, delta_mult)

            # Project sprite
            x = (self.width - sprite.width) / 2
            y = (self.height - sprite.height) / 2
            self.project_sprite(sprite, 0, x, y)

            # Refresh
            self.refresh()

        self.pump_input()
        self.input_events = []

    def unpause(self):
        """Unpause the game."""
        r.game_paused = False

    def pump_input(self):
        """
        Cause the SGE to recieve input from the OS.

        This method needs to be called periodically for the SGE to
        recieve events from the OS, such as key presses and mouse
        movement, as well as to assure the OS that the program is not
        locked up.

        Upon calling this, each event is translated into the appropriate
        class in :mod:`sge.input` and the resulting object is appended
        to :attr:`input_events`.

        You normally don't need to use this function directly.  It is
        called automatically in each frame of the SGE's main loop.  You
        only need to use this function directly if you take control away
        from the SGE's main loop, e.g. to create your own loop.
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                try:
                    k = sge.KEY_NAMES[event.key]
                except KeyError:
                    k = "undef_{}".format(event.key)

                input_event = sge.input.KeyPress(k, event.unicode)
                self.input_events.append(input_event)
            elif event.type == pygame.KEYUP:
                try:
                    k = sge.KEY_NAMES[event.key]
                except KeyError:
                    k = "undef_{}".format(event.key)

                input_event = sge.input.KeyRelease(k)
                self.input_events.append(input_event)
            elif event.type == pygame.MOUSEMOTION:
                input_event = sge.input.MouseMove(*event.rel)
                self.input_events.append(input_event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    b = sge.MOUSE_BUTTON_NAMES[event.button]
                except KeyError:
                    w = "Don't know how to handle mouse button {}.".format(
                        event.button)
                else:
                    input_event = sge.input.MouseButtonPress(b)
                    self.input_events.append(input_event)
            elif event.type == pygame.MOUSEBUTTONUP:
                try:
                    b = sge.MOUSE_BUTTON_NAMES[event.button]
                except KeyError:
                    w = "Don't know how to handle mouse button {}.".format(
                        event.button)
                else:
                    input_event = sge.input.MouseButtonRelease(b)
                    self.input_events.append(input_event)
            elif event.type == pygame.JOYAXISMOTION:
                jsname = r.game_js_names[event.joy]
                value = max(-1.0, min(event.value, 1.0))
                a = abs(min(0, value))
                b = max(0, value)
                z = 1 - abs(value)

                axis_id = (event.joy, event.axis)
                valuep = r._prev_axes.get(axis_id, 0)
                r._prev_axes[axis_id] = value
                ap = abs(min(0, valuep))
                bp = max(0, valuep)
                zp = 1 - abs(valuep)

                input_event = sge.input.JoystickAxisMove(
                    jsname, event.joy, event.axis, value)
                self.input_events.append(input_event)

                if a != ap:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "axis-", event.axis, a)
                    self.input_events.append(input_event)
                if b != bp:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "axis+", event.axis, b)
                    self.input_events.append(input_event)
                if z != zp:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "axis0", event.axis, z)
                    self.input_events.append(input_event)
            elif event.type == pygame.JOYHATMOTION:
                jsname = r.game_js_names[event.joy]
                x, y = event.value
                y *= -1
                left = abs(min(0, x))
                right = max(0, x)
                center_x = 1 - abs(x)
                up = abs(min(0, y))
                down = max(0, y)
                center_y = 1 - abs(y)

                hat_id = (event.joy, event.hat)
                xp, yp = r._prev_hats.get(hat_id, (0, 0))
                r._prev_hats[hat_id] = (x, y)
                leftp = abs(min(0, xp))
                rightp = max(0, xp)
                center_xp = 1 - abs(xp)
                upp = abs(min(0, yp))
                downp = max(0, yp)
                center_yp = 1 - abs(yp)

                input_event = sge.input.JoystickHatMove(
                    jsname, event.joy, event.hat, x, y)
                self.input_events.append(input_event)

                if left != leftp:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "hat_left", event.hat, left)
                    self.input_events.append(input_event)
                if right != rightp:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "hat_right", event.hat, right)
                    self.input_events.append(input_event)
                if center_x != center_xp:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "hat_center_x", event.hat, center_x)
                    self.input_events.append(input_event)
                if up != upp:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "hat_up", event.hat, up)
                    self.input_events.append(input_event)
                if down != downp:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "hat_down", event.hat, down)
                    self.input_events.append(input_event)
                if center_y != center_yp:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "hat_center_y", event.hat, center_y)
                    self.input_events.append(input_event)
            elif event.type == pygame.JOYBALLMOTION:
                jsname = r.game_js_names[event.joy]
                x, y = event.rel

                input_event = sge.input.JoystickTrackballMove(
                    jsname, event.joy, event.ball, x, y)
                self.input_events.append(input_event)

                if x < 0:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "trackball_left", event.ball,
                        abs(x))
                    self.input_events.append(input_event)
                elif x > 0:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "trackball_right", event.ball,
                        abs(x))
                    self.input_events.append(input_event)
                if y < 0:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "trackball_up", event.ball,
                        abs(y))
                    self.input_events.append(input_event)
                elif y > 0:
                    input_event = sge.input.JoystickEvent(
                        jsname, event.joy, "trackball_down", event.ball,
                        abs(y))
                    self.input_events.append(input_event)
            elif event.type == pygame.JOYBUTTONDOWN:
                jsname = r.game_js_names[event.joy]

                input_event = sge.input.JoystickButtonPress(jsname, event.joy,
                                                            event.button)
                self.input_events.append(input_event)

                input_event = sge.input.JoystickEvent(
                    jsname, event.joy, "button", event.button, True)
                self.input_events.append(input_event)
            elif event.type == pygame.JOYBUTTONUP:
                jsname = r.game_js_names[event.joy]

                input_event = sge.input.JoystickButtonRelease(
                    jsname, event.joy, event.button)
                self.input_events.append(input_event)

                input_event = sge.input.JoystickEvent(
                    jsname, event.joy, "button", event.button, False)
                self.input_events.append(input_event)
            elif event.type == pygame.ACTIVEEVENT:
                if event.gain:
                    if 2 & event.state:
                        # Gain keyboard focus
                        self.input_events.append(sge.input.KeyboardFocusGain())
                    if 1 & event.state:
                        # Gain mouse focus
                        self.input_events.append(sge.input.KeyboardFocusLose())
                else:
                    if 2 & event.state:
                        # Lose keyboard focus
                        self.input_events.append(sge.input.MouseFocusGain())
                    if 1 & event.state:
                        # Lose mouse focus
                        self.input_events.append(sge.input.MouseFocusLose())
            elif event.type == pygame.QUIT:
                self.input_events.append(sge.input.QuitRequest())
            elif event.type == pygame.VIDEORESIZE:
                r.game_window_width = event.w
                r.game_window_height = event.h
                _set_mode()
            elif event.type == sge.MUSIC_END_EVENT:
                if r.music_queue:
                    music = r.music_queue.pop(0)
                    music[0].play(*music[1:])

    def regulate_speed(self, fps=None):
        """
        Regulate the SGE's running speed and return the time passed.

        Arguments:

        - ``fps`` -- The target frame rate in frames per second.  Set to
          :const:`None` to target the current value of :attr:`fps`.

        When this method is called, the program will sleep long enough
        so that the game runs at ``fps`` frames per second, then return
        the number of milliseconds that passed between the previous call
        and the current call of this method.

        You normally don't need to use this function directly.  It is
        called automatically in each frame of the SGE's main loop.  You
        only need to use this function directly if you want to create
        your own loop.
        """
        if fps is None:
            if self.delta and self.delta_max is not None:
                fps = self.delta_max
            else:
                fps = self.fps

        tp = r.game_clock.tick(fps)

        r.cache.prune_time += tp
        if r.cache.prune_time >= r.CACHE_PRUNE_TIME:
            r.cache.prune_time = 0
            r.cache.prune()

        return tp

    def refresh(self):
        """
        Refresh the screen.

        This method needs to be called for changes to the screen to be
        seen by the user.  It should be called every frame.

        You normally don't need to use this function directly.  It is
        called automatically in each frame of the SGE's main loop.  You
        only need to use this function directly if you take control away
        from the SGE's main loop, e.g. to create your own loop.
        """
        # Music control
        _handle_music()

        if (r.game_x == 0 and r.game_y == 0 and r.game_xscale == 1 and
                r.game_yscale == 1):
            display_surface = r.game_window
        else:
            display_surface = r.game_display_surface

        # Clear display surface
        display_surface.fill((0, 0, 0))

        # Draw views
        for view in self.current_room.views:
            if (view.xport == 0 and view.yport == 0 and
                    view.wport == view.width == self.width and
                    view.hport == view.height == self.height):
                view_surf = display_surface
            else:
                view_surf = pygame.Surface((view.width, view.height))
            view_surf.fill(pygame.Color(*self.current_room.background.color))
            view_x = view.x
            view_y = view.y
            view_width = view.width
            view_height = view.height
            vx = view_x - sge.game.current_room.background_x
            vy = view_y - sge.game.current_room.background_y

            images = []

            for layer in self.current_room.background.layers:
                img = bl_get_image(layer)
                x = layer.x - vx * layer.xscroll_rate
                y = layer.y - vy * layer.yscroll_rate
                if isinstance(img, sge.gfx.TileGrid):
                    img_w = max(1, img.width)
                    img_h = max(1, img.height)
                else:
                    img_w = max(1, img.get_width())
                    img_h = max(1, img.get_height())

                # Apply the origin so the positions are as expected.
                x -= layer.sprite.origin_x
                y -= layer.sprite.origin_y

                # Move to the best position for what we want to do
                if layer.repeat_right and (layer.repeat_left or x < 0):
                    x = (x % img_w) - img_w
                elif layer.repeat_left and x + img_w > view_width:
                    x = (x % img_w) + img_w * math.ceil(view_width / img_w)
                if layer.repeat_down and (layer.repeat_up or y < 0):
                    y = (y % img_h) - img_h
                elif layer.repeat_up and y + img_h > view_height:
                    y = (y % img_h) + img_h * math.ceil(view_height / img_h)

                if layer.repeat_right and (layer.repeat_left or x < view_width):
                    hrange = six.moves.range(int(math.floor(x)),
                                             int(view.width + img_w), img_w)
                elif layer.repeat_left and x + img_w > 0:
                    hrange = six.moves.range(int(math.floor(x)), -img_w, -img_w)
                else:
                    hrange = [int(math.floor(x))]

                if layer.repeat_down and (layer.repeat_up or y < view_height):
                    vrange = six.moves.range(int(math.floor(y)),
                                             int(view_height + img_h), img_h)
                elif layer.repeat_up and y + img_h > 0:
                    vrange = six.moves.range(int(math.floor(y)), -img_h, -img_h)
                else:
                    vrange = [int(math.floor(y))]

                for y in vrange:
                    for x in hrange:
                        images.append((img, x + math.floor(view_x),
                                       y + math.floor(view_y), layer.z, None))

            for obj in self.current_room.get_objects_at(
                    view_x, view_y, view_width, view_height):
                if obj.visible and obj is not self.mouse:
                    if isinstance(obj.sprite, sge.gfx.Sprite):
                        img = s_get_image(obj.sprite, obj.image_index,
                                          obj.image_xscale, obj.image_yscale,
                                          obj.image_rotation, obj.image_alpha,
                                          obj.image_blend,
                                          obj.image_blend_mode)
                        w = img.get_width()
                        h = img.get_height()
                        x = obj.x - obj.image_origin_x
                        y = obj.y - obj.image_origin_y
                        if (x + w >= view_x and x <= view_x + view_width and
                                y + h >= view_y and y <= view_y + view_height):
                            nimg = s_get_image(obj.sprite, obj.image_index,
                                               obj.image_xscale,
                                               obj.image_yscale)
                            nw = nimg.get_width()
                            nh = nimg.get_height()
                            xoff = (w - nw) / 2
                            yoff = (h - nh) / 2
                            images.append((img, x - xoff, y - yoff,
                                           obj.z, None))
                    elif isinstance(obj.sprite, sge.gfx.TileGrid):
                        x = obj.x - obj.image_origin_x
                        y = obj.y - obj.image_origin_y
                        images.append((obj.sprite, x, y, obj.z, None))

            images.extend(self.current_room.rd["projections"])

            images.sort(key=lambda img: img[3])

            for img in images:
                surf = img[0]
                x = img[1] - view.x
                y = img[2] - view.y
                if isinstance(surf, sge.gfx.TileGrid):
                    tg_blit(surf, view_surf, x, y)
                else:
                    blend_mode = img[4]
                    if blend_mode == sge.BLEND_RGB_SCREEN:
                        _screen_blend(view_surf, surf, x, y, False)
                    elif blend_mode == sge.BLEND_RGBA_SCREEN:
                        _screen_blend(view_surf, surf, x, y, True)
                    else:
                        flags = _get_blend_flags(blend_mode)
                        view_surf.blit(surf, (int(x), int(y)), None, flags)

            if view_surf is not display_surface:
                display_surface.blit(
                    _scale(view_surf, view.wport, view.hport),
                    (int(view.xport), int(view.yport)))

        self.current_room.rd["projections"] = []

        # Window projections
        self.mouse.project_cursor()
        r.game_window_projections.sort(key=lambda img: img[3])
        for projection in r.game_window_projections:
            image, x, y, z, blend_mode = projection
            x = int(x)
            y = int(y)
            if isinstance(image, sge.gfx.TileGrid):
                tg_blit(image, display_surface, x, y)
            else:
                if blend_mode == sge.BLEND_RGB_SCREEN:
                    _screen_blend(display_surface, image, x, y, False)
                elif blend_mode == sge.BLEND_RGBA_SCREEN:
                    _screen_blend(display_surface, image, x, y, True)
                else:
                    flags = _get_blend_flags(blend_mode)
                    display_surface.blit(image, (x, y), None, flags)

        r.game_window_projections = []

        # Scale/blit display surface
        if display_surface is not r.game_window:
            r.game_window.blit(
                _scale(display_surface, self.width * r.game_xscale,
                       self.height * r.game_yscale), (int(r.game_x),
                       int(r.game_y)))

        pygame.display.flip()

    def project_dot(self, x, y, color, z=0, blend_mode=None):
        """
        Project a single-pixel dot onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the dot.
        - ``y`` -- The vertical location relative to the window to
          project the dot.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        Window projections are projections made directly onto the game
        window, independent of the room or any views.

        .. note:: The Z-axis position of a window projection does not
           correlate with the Z-axis position of anything positioned
           within the room, such as room projections and
           :class:`sge.dsp.Object` objects.  Window projections are
           always positioned in front of such things.

        See the documentation for :meth:`sge.gfx.Sprite.draw_dot` for
        more information.
        """
        _check_color(color)
        sprite = _get_dot_sprite(color)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_line(self, x1, y1, x2, y2, color, z=0, thickness=1,
                     anti_alias=False, blend_mode=None):
        """
        Project a line segment onto the game window.

        Arguments:

        - ``x1`` -- The horizontal location relative to the window of
          the first endpoint of the projected line segment.
        - ``y1`` -- The vertical location relative to the window of the
          first endpoint of the projected line segment.
        - ``x2`` -- The horizontal location relative to the window of
          the second endpoint of the projected line segment.
        - ``y2`` -- The vertical location relative to the window of the
          second endpoint of the projected line segment.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.gfx.Sprite.draw_line` and
        :meth:`sge.dsp.Game.project_dot` for more information.
        """
        _check_color(color)

        thickness = abs(thickness)
        x = min(x1, x2) - thickness // 2
        y = min(y1, y2) - thickness // 2
        x1 -= x
        y1 -= y
        x2 -= x
        y2 -= y

        sprite = _get_line_sprite(x1, y1, x2, y2, color, thickness, anti_alias)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_rectangle(self, x, y, width, height, z=0, fill=None,
                          outline=None, outline_thickness=1, blend_mode=None):
        """
        Project a rectangle onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the rectangle.
        - ``y`` -- The vertical location relative to the window to
          project the rectangle.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.gfx.Sprite.draw_rectangle`
        and :meth:`sge.dsp.Game.project_dot` for more information.
        """
        _check_color(fill)
        _check_color(outline)
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = _get_rectangle_sprite(width, height, fill, outline,
                                       outline_thickness)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_ellipse(self, x, y, width, height, z=0, fill=None,
                        outline=None, outline_thickness=1, anti_alias=False,
                        blend_mode=None):
        """
        Project an ellipse onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          position the imaginary rectangle containing the ellipse.
        - ``y`` -- The vertical location relative to the window to
          position the imaginary rectangle containing the ellipse.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.
        - ``width`` -- The width of the ellipse.
        - ``height`` -- The height of the ellipse.
        - ``outline_thickness`` -- The thickness of the outline of the
          ellipse.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.

        See the documentation for :meth:`sge.gfx.Sprite.draw_ellipse`
        and :meth:`sge.dsp.Game.project_dot` for more information.
        """
        if fill is not None and not isinstance(fill, gfx.Color):
            e = "`{}` is not a Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, gfx.Color):
            e = "`{}` is not a Color object.".format(repr(outline))
            raise TypeError(e)

        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = _get_ellipse_sprite(width, height, fill, outline,
                                     outline_thickness, anti_alias)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_circle(self, x, y, radius, z=0, fill=None, outline=None,
                       outline_thickness=1, anti_alias=False, blend_mode=None):
        """
        Project a circle onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          position the center of the circle.
        - ``y`` -- The vertical location relative to the window to
          position the center of the circle.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.gfx.Sprite.draw_circle` and
        :meth:`sge.dsp.Game.project_dot` for more information.
        """
        _check_color(fill)
        _check_color(outline)
        sprite = _get_circle_sprite(radius, fill, outline, outline_thickness,
                                    anti_alias)
        self.project_sprite(sprite, 0, x - radius, y - radius, z, blend_mode)

    def project_polygon(self, points, z=0, fill=None, outline=None,
                        outline_thickness=1, anti_alias=False, blend_mode=None):
        """
        Draw a polygon on the sprite.

        Arguments:

        - ``points`` -- A list of points relative to the room to
          position each of the polygon's angles.  Each point should be a
          tuple in the form ``(x, y)``, where x is the horizontal
          location and y is the vertical location.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.gfx.Sprite.draw_polygon`
        and :meth:`sge.dsp.Game.project_dot` for more information.
        """
        _check_color(fill)
        _check_color(outline)

        xlist = []
        ylist = []
        for point in points:
            xlist.append(point[0])
            ylist.append(point[1])
        x = min(xlist)
        y = min(ylist)

        sprite = _get_polygon_sprite(points, fill, outline, outline_thickness,
                                     anti_alias)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_sprite(self, sprite, image, x, y, z=0, blend_mode=None):
        """
        Project a sprite onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project ``sprite``.
        - ``y`` -- The vertical location relative to the window to
          project ``sprite``.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.gfx.Sprite.draw_sprite` and
        :meth:`sge.dsp.Game.project_dot` for more information.
        """
        img = s_get_image(sprite, image)
        x -= sprite.origin_x
        y -= sprite.origin_y
        r.game_window_projections.append((img, x, y, z, blend_mode))

    def project_text(self, font, text, x, y, z=0, width=None, height=None,
                    color=gfx.Color("white"), halign="left",
                    valign="top", anti_alias=True, blend_mode=None):
        """
        Project text onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the text.
        - ``y`` -- The vertical location relative to the window to
          project the text.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.gfx.Sprite.draw_text` and
        :meth:`sge.dsp.Game.project_dot` for more information.
        """
        _check_color(color)
        sprite = s_from_text(gfx.Sprite, font, text, width, height, color,
                             halign, valign, anti_alias)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def event_step(self, time_passed, delta_mult):
        """
        Called once each frame.

        Arguments:

        - ``time_passed`` -- The number of milliseconds that have passed
          during the last frame.
        - ``delta_mult`` -- What speed and movement should be multiplied
          by this frame due to delta timing.  If :attr:`delta` is
          :const:`False`, this is always ``1``.
        """
        pass

    def event_alarm(self, alarm_id):
        """
        Called when the value of an alarm reaches 0.

        See the documentation for :attr:`sge.dsp.Game.alarms` for more
        information.
        """
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
        See the documentation for :class:`sge.input.JoystickHatMove`
        for more information.
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

    def event_joystick(self, js_name, js_id, input_type, input_id, value):
        """
        See the documentation for :class:`sge.input.JoystickEvent` for
        more information.
        """
        pass

    def event_gain_keyboard_focus(self):
        """
        See the documentation for :class:`sge.input.KeyboardFocusGain`
        for more information.
        """
        pass

    def event_lose_keyboard_focus(self):
        """
        See the documentation for :class:`sge.input.KeyboardFocusLose`
        for more information.
        """
        pass

    def event_gain_mouse_focus(self):
        """
        See the documentation for :class:`sge.input.MouseFocusGain` for
        more information.
        """
        pass

    def event_lose_mouse_focus(self):
        """
        See the documentation for :class:`sge.input.MouseFocusLose` for
        more information.
        """
        pass

    def event_close(self):
        """
        See the documentation for :class:`sge.input.QuitRequest` for
        more information.

        This is always called after any :meth:`sge.dsp.Room.event_close`
        occurring at the same time.
        """
        pass

    def event_mouse_collision(self, other, xdirection, ydirection):
        """
        Proxy for :meth:`sge.game.mouse.event_collision`.  See the
        documentation for :meth:`sge.dsp.Object.event_collision` for
        more information.
        """
        pass

    def event_paused_step(self, time_passed, delta_mult):
        """
        See the documentation for :meth:`sge.dsp.Game.event_step` for
        more information.
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

    def event_paused_joystick(self, js_name, js_id, input_type, input_id,
                              value):
        """
        See the documentation for :class:`sge.input.JoystickEvent` for
        more information.
        """
        pass

    def event_paused_gain_keyboard_focus(self):
        """
        See the documentation for :class:`sge.input.KeyboardFocusGain`
        for more information.
        """
        pass

    def event_paused_lose_keyboard_focus(self):
        """
        See the documentation for :class:`sge.input.KeyboardFocusLose`
        for more information.
        """
        pass

    def event_paused_gain_mouse_focus(self):
        """
        See the documentation for :class:`sge.input.MouseFocusGain` for
        more information.
        """
        pass

    def event_paused_lose_mouse_focus(self):
        """
        See the documentation for :class:`sge.input.MouseFocusLose` for
        more information.
        """
        pass

    def event_paused_close(self):
        """
        See the documentation for :meth:`sge.dsp.Game.event_close` for
        more information.
        """
        pass


class Room(object):

    """
    This class stores the settings and objects found in a room.  Rooms
    are used to create separate parts of the game, such as levels and
    menu screens.

    .. attribute:: width

       The width of the room in pixels.  If set to :const:`None`,
       :attr:`sge.game.width` is used.

    .. attribute:: height

       The height of the room in pixels.  If set to :const:`None`,
       :attr:`sge.game.height` is used.

    .. attribute:: views

       A list containing all :class:`sge.dsp.View` objects in the room.

    .. attribute:: background

       The :class:`sge.gfx.Background` object used.

    .. attribute:: background_x

       The horizontal position of the background in the room.

    .. attribute:: background_y

       The vertical position of the background in the room.

    .. attribute:: object_area_width

       The width of this room's object areas in pixels.  If set to
       :const:`None`, :attr:`sge.game.width` is used.  For optimum
       performance, this should generally be about the average width of
       objects in the room which check for collisions.

    .. attribute:: object_area_height

       The height of this room's object areas in pixels.  If set to
       :const:`None`, :attr:`sge.game.height` is used.  For optimum
       performance, this should generally be about the average height of
       objects in the room which check for collisions.

    .. attribute:: alarms

       A dictionary containing the alarms of the room.  Each value
       decreases by 1 each frame (adjusted for delta timing if it is
       enabled).  When a value is at or below 0,
       :meth:`event_alarm` is executed with ``alarm_id`` set to the
       respective key, and the item is deleted from this dictionary.

    .. attribute:: objects

       A list containing all :class:`sge.dsp.Object` objects in the
       room.  (Read-only)

    .. attribute:: object_areas

       A 2-dimensional list of object areas, indexed in the following
       way::

           object_areas[x][y]

       Where ``x`` is the horizontal location of the left edge of the
       area in the room divided by :attr:`object_area_width`, and ``y``
       is the vertical location of the top edge of the area in the room
       divided by :attr:`object_area_height`.

       For example, if :attr:`object_area_width` is ``32`` and
       :attr:`object_area_height` is ``48``, then
       ``object_areas[2][4]`` indicates the object area with an x
       location of 64 and a y location of 192.

       Each object area is a set containing :class:`sge.dsp.Object`
       objects whose sprites or bounding boxes reside within the object
       area.

       Object areas are only created within the room, i.e. the
       horizontal location of an object area will always be less than
       :attr:`width`, and the vertical location of an object area will
       always be less than :attr:`height`.  Depending on the size of
       collision areas and the size of the room, however, the last row
       and/or the last column of collision areas may partially reside
       outside of the room.

       .. note::

          It is generally easier to use :meth:`get_objects_at` than to
          access this list directly.

    .. attribute:: object_area_void

       A set containing :class:`sge.dsp.Object` objects whose sprites or
       bounding boxes reside within any area not covered by the room's
       object area.

       .. note::

          Depending on the size of object areas and the size of the
          room, the "void" area may not include the entirety of the
          outside of the room.  There may be some space to the right of
          and/or below the room which is covered by collision areas.

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def object_area_width(self):
        return self.__object_area_width

    @object_area_width.setter
    def object_area_width(self, value):
        if value is None:
            value = sge.game.width

        self.__object_area_width = value
        r_set_object_areas(self)

    @property
    def object_area_height(self):
        return self.__object_area_height

    @object_area_height.setter
    def object_area_height(self, value):
        if value is None:
            value = sge.game.height

        self.__object_area_height = value
        r_set_object_areas(self)

    def __init__(self, objects=(), width=None, height=None, views=None,
                 background=None, background_x=0, background_y=0,
                 object_area_width=None, object_area_height=None):
        """
        Arguments:

        - ``views`` -- A list containing all :class:`sge.dsp.View`
          objects in the room.  If set to :const:`None`, a new view will
          be created with ``x=0``, ``y=0``, and all other arguments
          unspecified, which will become the first view of the room.
        - ``background`` -- The :class:`sge.gfx.Background` object used.
          If set to :const:`None`, a new background will be created with
          no layers and the color set to black.

        All other arguments set the respective initial attributes of the
        room.  See the documentation for :class:`sge.dsp.Room` for more
        information.
        """
        self.rd = {}
        self.width = width if width is not None else sge.game.width
        self.height = height if height is not None else sge.game.height
        self.rd["swidth"] = self.width
        self.rd["sheight"] = self.height

        if object_area_width is None:
            object_area_width = sge.game.width
        if object_area_height is None:
            object_area_height = sge.game.height

        self.__object_area_width = object_area_width
        self.__object_area_height = object_area_height
        self.background_x = background_x
        self.background_y = background_y
        self.alarms = {}
        self.rd["new_objects"] = []
        self.rd["projections"] = []

        if views is not None:
            self.views = list(views)
        else:
            self.views = [View(0, 0)]

        if background is not None:
            self.background = background
        else:
            self.background = gfx.Background([], gfx.Color("black"))

        self.rd["started"] = False

        self.objects = []
        r_set_object_areas(self)

        self.add(sge.game.mouse)
        for obj in objects:
            self.add(obj)

    def add(self, obj):
        """
        Add an object to the room.

        Arguments:

        - ``obj`` -- The :class:`sge.dsp.Object` object to add.

        .. warning::

           This method modifies the contents of :attr:`objects`.  Do not
           call this method during a loop through :attr:`objects`; doing
           so may cause problems with the loop. To get around this, you
           can create a shallow copy of :attr:`objects` to iterate
           through instead, e.g.::

               for obj in self.objects[:]:
                   self.add(obj.friend)

        """
        obj.alive = True
        if obj not in self.objects:
            self.objects.append(obj)

            if self is sge.game.current_room and self.rd["started"]:
                obj.event_create()
                obj.rd["object_areas"] = set()
                o_update_object_areas(obj)
                o_update_collision_lists(obj)
                if obj.active:
                    r._active_objects.add(obj)
            else:
                self.rd["new_objects"].append(obj)

    def remove(self, obj):
        """
        Remove an object from the room.

        Arguments:

        - ``obj`` -- The :class:`sge.dsp.Object` object to remove.

        .. warning::

           This method modifies the contents of :attr:`objects`.  Do not
           call this method during a loop through :attr:`objects`; doing
           so may cause problems with the loop. To get around this, you
           can create a shallow copy of :attr:`objects` to iterate
           through instead, e.g.::

               for obj in self.objects[:]:
                   self.remove(obj)
        """
        while obj in self.objects:
            self.objects.remove(obj)

        while obj in self.rd["new_objects"]:
            self.rd["new_objects"].remove(obj)

        if self is sge.game.current_room:
            o_update_object_areas(obj)
            o_update_collision_lists(obj)
            r._active_objects.discard(obj)
            obj.event_destroy()

    def start(self, transition=None, transition_time=1500,
              transition_arg=None):
        """
        Start the room.

        Arguments:

        - ``transition`` -- The type of transition to use.  Should be
          one of the following:

          - :const:`None` (no transition)
          - ``"fade"`` (fade to black)
          - ``"dissolve"``
          - ``"pixelate"``
          - ``"wipe_left"`` (wipe right to left)
          - ``"wipe_right"`` (wipe left to right)
          - ``"wipe_up"`` (wipe bottom to top)
          - ``"wipe_down"`` (wipe top to bottom)
          - ``"wipe_upleft"`` (wipe bottom-right to top-left)
          - ``"wipe_upright"`` (wipe bottom-left to top-right)
          - ``"wipe_downleft"`` (wipe top-right to bottom-left)
          - ``"wipe_downright"`` (wipe top-left to bottom-right)
          - ``"wipe_matrix"``
          - ``"iris_in"``
          - ``"iris_out"``

          If an unsupported value is given, default to :const:`None`.

        - ``transition_time`` -- The time the transition should take in
          milliseconds.  Has no effect if ``transition`` is
          :const:`None`.

        - ``transition_arg`` -- An arbitrary argument that can be used
          by the following transitions:

          - ``"wipe_matrix"`` -- The size of each square in the matrix
            transition as a tuple in the form ``(w, h)``, where ``w`` is
            the width and ``h`` is the height.  Default is ``(4, 4)``.
          - ``"iris_in"`` and ``"iris_out"`` -- The position of the
            center of the iris as a tuple in the form ``(x, y)``, where
            ``x`` is the horizontal location relative to the window and
            ``y`` is the vertical location relative to the window.
            Default is the center of the window.
        """
        transitions = {
            "fade": r_update_fade, "dissolve": r_update_dissolve,
            "pixelate": r_update_pixelate, "wipe_left": r_update_wipe_left,
            "wipe_right": r_update_wipe_right, "wipe_up": r_update_wipe_up,
            "wipe_down": r_update_wipe_down,
            "wipe_upleft": r_update_wipe_upleft,
            "wipe_upright": r_update_wipe_upright,
            "wipe_downleft": r_update_wipe_downleft,
            "wipe_downright": r_update_wipe_downright,
            "wipe_matrix": r_update_wipe_matrix,
            "iris_in": r_update_iris_in, "iris_out": r_update_iris_out}

        if transition in transitions and transition_time > 0:
            self.rd["t_update"] = transitions[transition]
            self.rd["t_sprite"] = gfx.Sprite.from_screenshot()
            self.rd["t_duration"] = transition_time
            self.rd["t_arg"] = transition_arg
            self.rd["t_time_passed"] = 0
            self.rd["t_complete_last"] = 0
            self.rd["t_matrix_remaining"] = None
        else:
            self.rd["t_update"] = None

        r.game_new_room = self

    def get_objects_at(self, x, y, width, height):
        """
        Return a set of objects near a particular area.

        Arguments:

        - ``x`` -- The horizontal location relative to the room of the
          left edge of the area.
        - ``y`` -- The vertical location relative to the room of the
          top edge of the area.
        - ``width`` -- The width of the area in pixels.
        - ``height`` -- The height of the area in pixels.

        .. note::

           This function does not ensure that objects returned are
           actually *within* the given area.  It simply combines all
           object areas that need to be checked into a single set.  To
           ensure that an object is actually within the area, you must
           check the object manually, or use
           :func:`sge.collision.rectangle` instead.
        """
        area = set()
        for a in r_get_rectangle_object_areas(self, x, y, width, height):
            if a is None:
                area |= self.object_area_void
            else:
                area |= self.object_areas[a[0]][a[1]]

        return area
            

    def project_dot(self, x, y, z, color, blend_mode=None):
        """
        Project a single-pixel dot onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the dot.
        - ``y`` -- The vertical location relative to the room to project
          the dot.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.gfx.Sprite.draw_dot` for
        more information.
        """
        _check_color(color)
        sprite = _get_dot_sprite(color)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_line(self, x1, y1, x2, y2, z, color, thickness=1,
                     anti_alias=False, blend_mode=None):
        """
        Project a line segment onto the room.

        Arguments:

        - ``x1`` -- The horizontal location relative to the room of the
          first endpoint of the projected line segment.
        - ``y1`` -- The vertical location relative to the room of the
          first endpoint of the projected line segment.
        - ``x2`` -- The horizontal location relative to the room of the
          second endpoint of the projected line segment.
        - ``y2`` -- The vertical location relative to the room of the
          second endpoint of the projected line segment.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.gfx.Sprite.draw_line` for
        more information.
        """
        _check_color(color)

        thickness = abs(thickness)
        x = min(x1, x2) - thickness // 2
        y = min(y1, y2) - thickness // 2
        x1 -= x
        y1 -= y
        x2 -= x
        y2 -= y

        sprite = _get_line_sprite(x1, y1, x2, y2, color, thickness, anti_alias)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_rectangle(self, x, y, z, width, height, fill=None,
                          outline=None, outline_thickness=1, blend_mode=None):
        """
        Project a rectangle onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the rectangle.
        - ``y`` -- The vertical location relative to the room to project
          the rectangle.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.gfx.Sprite.draw_rectangle`
        for more information.
        """
        _check_color(fill)
        _check_color(outline)
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = _get_rectangle_sprite(width, height, fill, outline,
                                       outline_thickness)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_ellipse(self, x, y, z, width, height, fill=None,
                        outline=None, outline_thickness=1, anti_alias=False,
                        blend_mode=None):
        """
        Project an ellipse onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          position the imaginary rectangle containing the ellipse.
        - ``y`` -- The vertical location relative to the room to
          position the imaginary rectangle containing the ellipse.
        - ``z`` -- The Z-axis position of the projection in the room.
        - ``width`` -- The width of the ellipse.
        - ``height`` -- The height of the ellipse.
        - ``outline_thickness`` -- The thickness of the outline of the
          ellipse.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.

        See the documentation for :meth:`sge.gfx.Sprite.draw_ellipse`
        for more information.
        """
        _check_color(fill)
        _check_color(outline)
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = _get_ellipse_sprite(width, height, fill, outline,
                                     outline_thickness, anti_alias)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_circle(self, x, y, z, radius, fill=None, outline=None,
                       outline_thickness=1, anti_alias=False, blend_mode=None):
        """
        Project a circle onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          position the center of the circle.
        - ``y`` -- The vertical location relative to the room to
          position the center of the circle.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.gfx.Sprite.draw_circle` for
        more information.
        """
        _check_color(fill)
        _check_color(outline)
        sprite = _get_circle_sprite(radius, fill, outline, outline_thickness,
                                    anti_alias)
        self.project_sprite(sprite, 0, x - radius, y - radius, z, blend_mode)

    def project_polygon(self, points, z, fill=None, outline=None,
                        outline_thickness=1, anti_alias=False, blend_mode=None):
        """
        Draw a polygon on the sprite.

        Arguments:

        - ``points`` -- A list of points relative to the room to
          position each of the polygon's angles.  Each point should be a
          tuple in the form ``(x, y)``, where x is the horizontal
          location and y is the vertical location.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.gfx.Sprite.draw_polygon`
        for more information.
        """
        _check_color(fill)
        _check_color(outline)

        xlist = []
        ylist = []
        for point in points:
            xlist.append(point[0])
            ylist.append(point[1])
        x = min(xlist)
        y = min(ylist)

        sprite = _get_polygon_sprite(points, fill, outline, outline_thickness,
                                     anti_alias)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def project_sprite(self, sprite, image, x, y, z, blend_mode=None):
        """
        Project a sprite onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project ``sprite``.
        - ``y`` -- The vertical location relative to the room to project
          ``sprite``.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.gfx.Sprite.draw_sprite` for
        more information.
        """
        img = s_get_image(sprite, image)
        x -= sprite.origin_x
        y -= sprite.origin_y
        self.rd["projections"].append((img, x, y, z, blend_mode))

    def project_text(self, font, text, x, y, z, width=None, height=None,
                    color=sge.gfx.Color("white"), halign="left",
                    valign="top", anti_alias=True, blend_mode=None):
        """
        Project text onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the text.
        - ``y`` -- The vertical location relative to the room to project
          the text.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.gfx.Sprite.draw_text` for
        more information.
        """
        _check_color(color)
        sprite = s_from_text(gfx.Sprite, font, text, width, height, color,
                             halign, valign, anti_alias)
        self.project_sprite(sprite, 0, x, y, z, blend_mode)

    def event_room_start(self):
        """
        Called when the room is started for the first time.  It is
        always called after any :meth:`sge.dsp.Game.event_game_start`
        and before any :class:`sge.dsp.Object.event_create` occurring at
        the same time.
        """
        pass

    def event_room_resume(self):
        """
        Called when the room is started after it has already previously
        been started.  It is always called before any
        :meth:`sge.dsp.Object.event_create` occurring at the same time.
        """
        pass

    def event_room_end(self):
        """
        Called when another room is started or the game ends while this
        room is the current room.  It is always called before any
        :meth:`sge.dsp.Game.event_game_end` occurring at the same time.
        """
        pass

    def event_step(self, time_passed, delta_mult):
        """
        See the documentation for :meth:`sge.dsp.Game.event_step` for
        more information.
        """
        pass

    def event_alarm(self, alarm_id):
        """
        See the documentation for :attr:`sge.dsp.Room.alarms` for more
        information.
        """
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
        """Mouse button press event.

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

    def event_joystick(self, js_name, js_id, input_type, input_id, value):
        """
        See the documentation for :class:`sge.input.JoystickEvent` for
        more information.
        """
        pass

    def event_gain_keyboard_focus(self):
        """
        See the documentation for :class:`sge.input.KeyboardFocusGain`
        for more information.
        """
        pass

    def event_lose_keyboard_focus(self):
        """
        See the documentation for :class:`sge.input.KeyboardFocusLose`
        for more information.
        """
        pass

    def event_gain_mouse_focus(self):
        """
        See the documentation for :class:`sge.input.MouseFocusGain` for
        more information.
        """
        pass

    def event_lose_mouse_focus(self):
        """
        See the documentation for :class:`sge.input.MouseFocusLose` for
        more information.
        """
        pass

    def event_close(self):
        """
        This is always called before any
        :meth:`sge.dsp.Game.event_close` occurring at the same time.

        See the documentation for :class:`sge.input.QuitRequest` for
        more information.
        """
        pass

    def event_paused_step(self, time_passed, delta_mult):
        """
        See the documentation for :meth:`sge.dsp.Game.event_step` for
        more information.
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

    def event_paused_joystick(self, js_name, js_id, input_type, input_id,
                              value):
        """
        See the documentation for :class:`sge.input.JoystickEvent` for
        more information.
        """
        pass

    def event_paused_gain_keyboard_focus(self):
        """
        See the documentation for :class:`sge.input.KeyboardFocusGain`
        for more information.
        """
        pass

    def event_paused_lose_keyboard_focus(self):
        """
        See the documentation for :class:`sge.input.KeyboardFocusLose`
        for more information.
        """
        pass

    def event_paused_gain_mouse_focus(self):
        """
        See the documentation for :class:`sge.input.MouseFocusGain` for
        more information.
        """
        pass

    def event_paused_lose_mouse_focus(self):
        """
        See the documentation for :class:`sge.input.MouseFocusLose` for
        more information.
        """
        pass

    def event_paused_close(self):
        """
        See the documentation for :meth:`sge.dsp.Room.event_close` for
        more information.
        """
        pass


class View(object):

    """
    This class controls what the player sees in a room at any given
    time.  Multiple views can exist in a room, and this can be used to
    create a split-screen effect.

    .. attribute:: x

       The horizontal position of the view in the room.  When set, if it
       brings the view outside of the room it is in, it will be
       re-adjusted so that the view is completely inside the room.

    .. attribute:: y

       The vertical position of the view in the room.  When set, if it
       brings the view outside of the room it is in, it will be
       re-adjusted so that the view is completely inside the room.

    .. attribute:: xport

       The horizontal position of the view port on the window.

    .. attribute:: yport

       The vertical position of the view port on the window.

    .. attribute:: width

       The width of the view.  When set, if it results in the view being
       outside of the room it is in, :attr:`x` will be adjusted so that
       the view is completely inside the room.

    .. attribute:: height

       The height of the view.  When set, if it results in the view
       being outside the room it is in, :attr:`y` will be adjusted so
       that the view is completely inside the room.

    .. attribute:: wport

       The width of the view port.  Set to :const:`None` to make it the
       same as :attr:`width`.  If this value differs from :attr:`width`,
       the image will be horizontally scaled so that it fills the port.

    .. attribute:: hport

       The height of the view port.  Set to :const:`None` to make it the
       same as :attr:`height`.  If this value differs from
       :attr:`height`, the image will be vertically scaled so that it
       fills the port.

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def x(self):
        return self.rd["x"]

    @x.setter
    def x(self, value):
        self.rd["x"] = value
        v_limit(self)

    @property
    def y(self):
        return self.rd["y"]

    @y.setter
    def y(self, value):
        self.rd["y"] = value
        v_limit(self)

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value
        v_limit(self)

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value
        v_limit(self)

    @property
    def wport(self):
        return self.__wport if self.__wport is not None else self.width

    @wport.setter
    def wport(self, value):
        self.__wport = value

    @property
    def hport(self):
        return self.__hport if self.__hport is not None else self.height

    @hport.setter
    def hport(self, value):
        self.__hport = value

    def __init__(self, x, y, xport=0, yport=0, width=None, height=None,
                 wport=None, hport=None):
        """
        Arguments:

        - ``width`` -- The width of the view.  If set to :const:`None`,
          it will become ``sge.game.width - xport``.
        - ``height`` -- The height of the view.  If set to
          :const:`None`, it will become ``sge.game.height - yport``.

        All other arugments set the respective initial attributes of the
        view.  See the documentation for :class:`sge.dsp.View` for more
        information.
        """
        self.rd = {}
        self.rd["x"] = x
        self.rd["y"] = y
        self.xport = xport
        self.yport = yport
        self.__width = width if width else sge.game.width - xport
        self.__height = height if height else sge.game.height - yport
        v_limit(self)
        self.wport = wport
        self.hport = hport


class Object(object):

    """
    This class is used for game objects, such as the player, enemies,
    bullets, and the HUD.  Generally, each type of object has its own
    subclass of :class:`sge.dsp.Object`.

    .. attribute:: x

       The horizontal position of the object in the room.

    .. attribute:: y

       The vertical position of the object in the room.

    .. attribute:: z

       The Z-axis position of the object in the room.

    .. attribute:: sprite

       The sprite currently in use by this object.  Can be either a
       :class:`sge.gfx.Sprite` object or a :class:`sge.gfx.TileGrid`
       object.  Set to :const:`None` for no sprite.

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

          Inactive :class:`sge.dsp.Object` objects are still visible
          by default and continue to be involved in collisions.  In
          addition, collision events and destroy events still occur even
          if the object is inactive.  If you wish for the object to not
          be visible, set :attr:`visible` to :const:`False`.  If you
          wish for the object to not perform collision events, set
          :attr:`tangible` to :const:`False`.

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
       being clockwise.

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

       The horizontal scale factor of the sprite.  If this is negative,
       the sprite will also be mirrored horizontally.

    .. attribute:: image_yscale

       The vertical scale factor of the sprite.  If this is negative,
       the sprite will also be flipped vertically.

    .. attribute:: image_rotation

       The rotation of the sprite in degrees, with rotation in a
       positive direction being clockwise.

       If :attr:`regulate_origin` is :const:`True`, the image is rotated
       about the origin.  Otherwise, the image is rotated about its
       center.

    .. attribute:: image_alpha

       The alpha value applied to the entire image, where ``255`` is the
       original image, ``128`` is half the opacity of the original
       image, ``0`` is fully transparent, etc.

    .. attribute:: image_blend

       A :class:`sge.gfx.Color` object representing the color to blend
       with the sprite (using RGBA Multiply blending).  Set to
       :const:`None` for no color blending.

    .. attribute:: image_blend_mode

       The blend mode to use with :attr:`image_blend`.  Possible blend
       modes are:

       - :data:`sge.BLEND_NORMAL`
       - :data:`sge.BLEND_RGBA_ADD`
       - :data:`sge.BLEND_RGBA_SUBTRACT`
       - :data:`sge.BLEND_RGBA_MULTIPLY`
       - :data:`sge.BLEND_RGBA_SCREEN`
       - :data:`sge.BLEND_RGBA_MINIMUM`
       - :data:`sge.BLEND_RGBA_MAXIMUM`
       - :data:`sge.BLEND_RGB_ADD`
       - :data:`sge.BLEND_RGB_SUBTRACT`
       - :data:`sge.BLEND_RGB_MULTIPLY`
       - :data:`sge.BLEND_RGB_SCREEN`
       - :data:`sge.BLEND_RGB_MINIMUM`
       - :data:`sge.BLEND_RGB_MAXIMUM`

       :const:`None` is treated as :data:`sge.BLEND_RGB_MULTIPLY`.

    .. attribute:: image_left

       The horizontal position of the left edge of the object's sprite
       in the room.

    .. attribute:: image_right

       The horizontal position of the right edge of the object's sprite
       in the room.

    .. attribute:: image_xcenter

       The horizontal position of the center of the object's sprite in
       the room.

    .. attribute:: image_top

       The vertical position of the top edge of the object's sprite in
       the room.

    .. attribute:: image_bottom

       The vertical position of the bottom edge of the object's sprite
       in the room.

    .. attribute:: image_ycenter

       The vertical position of the center of the object's sprite in the
       room.

    .. attribute:: alarms

       A dictionary containing the alarms of the object.  Each value
       decreases by 1 each frame (adjusted for delta timing if it is
       enabled).  When a value is at or below 0, :meth:`event_alarm` is
       executed with ``alarm_id`` set to the respective key, and the
       item is deleted from this dictionary.

    .. attribute:: image_width

       The total width of the object's displayed image as it appears on
       the screen, including the effects of scaling and rotation.
       (Read-only)

    .. attribute:: image_height

       The total height of the object's displayed image as it appears on
       the screen, including the effects of scaling and rotation.
       (Read-only)

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

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if self.__x != value:
            self.__x = value
            o_update_object_areas(self)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if self.__y != value:
            self.__y = value
            o_update_object_areas(self)

    @property
    def sprite(self):
        return self.rd["sprite"]

    @sprite.setter
    def sprite(self, value):
        if self.rd["sprite"] != value:
            self.rd["sprite"] = value
            if value is not None:
                self.image_index %= value.frames
            o_update_object_areas(self)

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        if self.__active != value:
            self.__active = value
            if value:
                r._active_objects.add(self)
            else:
                r._active_objects.discard(self)

    @property
    def checks_collisions(self):
        return self.__checks_collisions

    @checks_collisions.setter
    def checks_collisions(self, value):
        if self.__checks_collisions != value:
            self.__checks_collisions = value
            o_update_collision_lists(self)

    @property
    def tangible(self):
        return self.rd["tangible"]

    @tangible.setter
    def tangible(self, value):
        if self.rd["tangible"] != value:
            self.rd["tangible"] = value
            o_update_collision_lists(self)

    @property
    def bbox_x(self):
        return self.__bbox_x

    @bbox_x.setter
    def bbox_x(self, value):
        if self.__bbox_x != value:
            if value is not None:
                self.__bbox_x = value
            else:
                if self.sprite is not None:
                    self.__bbox_x = self.sprite.bbox_x
                else:
                    self.__bbox_x = 0
            o_update_object_areas(self)

    @property
    def bbox_y(self):
        return self.__bbox_y

    @bbox_y.setter
    def bbox_y(self, value):
        if self.__bbox_y != value:
            if value is not None:
                self.__bbox_y = value
            else:
                if self.sprite is not None:
                    self.__bbox_y = self.sprite.bbox_y
                else:
                    self.__bbox_y = 0
            o_update_object_areas(self)

    @property
    def bbox_width(self):
        return self.__bbox_width

    @bbox_width.setter
    def bbox_width(self, value):
        if self.__bbox_width != value:
            if value is not None:
                self.__bbox_width = value
            else:
                if self.sprite is not None:
                    self.__bbox_width = self.sprite.bbox_width
                else:
                    self.__bbox_width = 1
            o_update_object_areas(self)

    @property
    def bbox_height(self):
        return self.__bbox_height

    @bbox_height.setter
    def bbox_height(self, value):
        if self.__bbox_height != value:
            if value is not None:
                self.__bbox_height = value
            else:
                if self.sprite is not None:
                    self.__bbox_height = self.sprite.bbox_height
                else:
                    self.__bbox_height = 1
            o_update_object_areas(self)

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
        return self.rd["xv"]

    @xvelocity.setter
    def xvelocity(self, value):
        if self.rd["xv"] != value:
            self.rd["xv"] = value
            o_set_speed(self)

    @property
    def yvelocity(self):
        return self.rd["yv"]

    @yvelocity.setter
    def yvelocity(self, value):
        if self.rd["yv"] != value:
            self.rd["yv"] = value
            o_set_speed(self)

    @property
    def speed(self):
        return self.rd["speed"]

    @speed.setter
    def speed(self, value):
        if self.rd["speed"] != value:
            self.rd["speed"] = value
            self.rd["xv"] = math.cos(math.radians(self.rd["mv_dir"])) * value
            self.rd["yv"] = math.sin(math.radians(self.rd["mv_dir"])) * value

    @property
    def move_direction(self):
        return self.rd["mv_dir"]

    @move_direction.setter
    def move_direction(self, value):
        if self.rd["mv_dir"] != value:
            self.rd["mv_dir"] = value
            self.rd["xv"] = math.cos(math.radians(value)) * self.rd["speed"]
            self.rd["yv"] = math.sin(math.radians(value)) * self.rd["speed"]

    @property
    def image_index(self):
        return self.rd["image_index"]

    @image_index.setter
    def image_index(self, value):
        if value != self.rd["image_index"]:
            self.rd["image_index"] = value
            self.rd["anim_count"] = 0

    @property
    def image_origin_x(self):
        if self.regulate_origin and self.sprite is not None:
            id_ = (self.sprite.width, self.sprite.height, self.sprite.origin_x,
                   self.sprite.origin_y, self.image_xscale, self.image_yscale,
                   self.image_rotation)

            if id_ not in self.__origins_x:
                x_offset, y_offset = o_get_origin_offset(self)
                self.__origins_x[id_] = self.sprite.origin_x + x_offset
                self.__origins_y[id_] = self.sprite.origin_y + y_offset

            self.__image_origin_x = self.__origins_x[id_]

        if self.__image_origin_x is None:
            return self.sprite.origin_x if self.sprite is not None else 0
        else:
            return self.__image_origin_x

    @image_origin_x.setter
    def image_origin_x(self, value):
        self.__image_origin_x = value

    @property
    def image_origin_y(self):
        if self.regulate_origin and self.sprite is not None:
            id_ = (self.sprite.width, self.sprite.height, self.sprite.origin_x,
                   self.sprite.origin_y, self.image_xscale, self.image_yscale,
                   self.image_rotation)

            if id_ not in self.__origins_y:
                x_offset, y_offset = o_get_origin_offset(self)
                self.__origins_x[id_] = self.sprite.origin_x + x_offset
                self.__origins_y[id_] = self.sprite.origin_y + y_offset

            self.__image_origin_y = self.__origins_y[id_]

        if self.__image_origin_y is None:
            return self.sprite.origin_y if self.sprite is not None else 0
        else:
            return self.__image_origin_y

    @image_origin_y.setter
    def image_origin_y(self, value):
        self.__image_origin_y = value

    @property
    def image_fps(self):
        return self.__fps

    @image_fps.setter
    def image_fps(self, value):
        if value is None:
            value = self.sprite.fps if self.sprite is not None else 0

        self.__fps = value
        if value and isinstance(self.sprite, sge.gfx.Sprite):
            self.rd["frame_time"] = 1000 / value
            if not self.rd["frame_time"]:
                # This would be caused by a round-off to 0 resulting
                # from a much too high frame rate.  It would cause a
                # division by 0 later, so this is meant to prevent that.
                self.rd["frame_time"] = 0.000001
                w = "Could not calculate timing for {:.2e} FPS.".format(
                    value)
                warnings.warn(w)
        else:
            self.rd["frame_time"] = None

    @property
    def image_speed(self):
        return self.image_fps / sge.game.fps

    @image_speed.setter
    def image_speed(self, value):
        if value is None:
            value = self.sprite.speed if self.sprite is not None else 0

        self.image_fps = value * sge.game.fps

    @property
    def image_blend(self):
        return self.__image_blend

    @image_blend.setter
    def image_blend(self, value):
        _check_color(value)
        self.__image_blend = value

    @property
    def image_left(self):
        return self.x - self.image_origin_x

    @image_left.setter
    def image_left(self, value):
        self.x = value + self.image_origin_x

    @property
    def image_right(self):
        return self.image_left + self.image_width

    @image_right.setter
    def image_right(self, value):
        self.image_left = value - self.image_width

    @property
    def image_xcenter(self):
        return self.image_left + int(self.image_width / 2)

    @image_xcenter.setter
    def image_xcenter(self, value):
        self.image_left = value - int(self.image_width / 2)

    @property
    def image_top(self):
        return self.y - self.image_origin_y

    @image_top.setter
    def image_top(self, value):
        self.y = value + self.image_origin_y

    @property
    def image_bottom(self):
        return self.image_top + self.image_height

    @image_bottom.setter
    def image_bottom(self, value):
        self.image_top = value - self.image_height

    @property
    def image_ycenter(self):
        return self.image_top + int(self.image_height / 2)

    @image_ycenter.setter
    def image_ycenter(self, value):
        self.image_top = value - int(self.image_height / 2)

    @property
    def image_width(self):
        img = s_get_image(self.sprite, self.image_index, self.image_xscale,
                          self.image_yscale, self.image_rotation)
        return img.get_width()

    @property
    def image_height(self):
        img = s_get_image(self.sprite, self.image_index, self.image_xscale,
                          self.image_yscale, self.image_rotation)
        return img.get_height()

    @property
    def mask(self):
        if self.collision_precise and isinstance(self.sprite, sge.gfx.Sprite):
            return s_get_precise_mask(
                self.sprite, self.image_index, self.image_xscale,
                self.image_yscale, self.image_rotation)
        else:
            i = ("o_mask", self.collision_ellipse, self.bbox_x, self.bbox_y,
                 self.bbox_width, self.bbox_height, self.image_xscale,
                 self.image_yscale)
            mask = r.cache.get(i)

            if mask is None:
                if self.collision_ellipse:
                    # Elliptical mask based on bounding box.
                    mask = [[False for y in six.moves.range(self.bbox_height)]
                            for x in six.moves.range(self.bbox_width)]
                    a = len(mask) / 2
                    b = len(mask[0]) / 2 if mask else 0

                    for x in six.moves.range(len(mask)):
                        for y in six.moves.range(len(mask[x])):
                            if ((x - a) / a) ** 2 + ((y - b) / b) ** 2 <= 1:
                                mask[x][y] = True
                else:
                    # Mask is all pixels in the bounding box.
                    mask = [[True for y in six.moves.range(self.bbox_height)]
                            for x in six.moves.range(self.bbox_width)]

            r.cache.add(i, mask)
            return mask

    @property
    def mask_x(self):
        if self.collision_precise:
            if (isinstance(self.sprite, sge.gfx.Sprite) and
                    self.image_rotation % 180):
                origin_x = self.image_origin_x
                i = ("o_mask_x_offset", self, self.sprite, origin_x,
                     self.image_origin_y, self.image_xscale, self.image_yscale,
                     self.image_rotation)
                offset = r.cache.get(i)
                if offset is None:
                    width = s_get_image(self.sprite, self.image_index,
                                        self.image_xscale, self.image_yscale,
                                        self.image_rotation).get_width()
                    normal_width = s_get_image(self.sprite, self.image_index,
                                               self.image_xscale,
                                               self.image_yscale).get_width()
                    offset = (width - normal_width) / 2

                r.cache.add(i, offset)
                return self.x - (origin_x + offset)
            else:
                return self.x - self.image_origin_x
        else:
            return self.bbox_left

    @property
    def mask_y(self):
        if self.collision_precise:
            if (isinstance(self.sprite, sge.gfx.Sprite) and
                    self.image_rotation % 180):
                origin_y = self.image_origin_y
                i = ("o_mask_y_offset", self, self.sprite, self.image_origin_x,
                     origin_y, self.image_xscale, self.image_yscale,
                     self.image_rotation)
                offset = r.cache.get(i)
                if offset is None:
                    height = s_get_image(self.sprite, self.image_index,
                                         self.image_xscale, self.image_yscale,
                                         self.image_rotation).get_height()
                    normal_height = s_get_image(self.sprite, self.image_index,
                                                self.image_xscale,
                                                self.image_yscale).get_height()
                    offset = (height - normal_height) / 2

                r.cache.add(i, offset)
                return self.y - (origin_y + offset)
            else:
                return self.y - self.image_origin_y
        else:
            return self.bbox_top

    def __init__(self, x, y, z=0, sprite=None, visible=True, active=True,
                 checks_collisions=True, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 xacceleration=0, yacceleration=0, xdeceleration=0,
                 ydeceleration=0, image_index=0, image_origin_x=None,
                 image_origin_y=None, image_fps=None, image_xscale=1,
                 image_yscale=1, image_rotation=0, image_alpha=255,
                 image_blend=None, image_blend_mode=None):
        """
        Arugments set the respective initial attributes of the object.
        See the documentation for :class:`sge.dsp.Object` for more
        information.
        """
        self.rd = {}
        self.__x = x
        self.__y = y
        self.z = z
        self.__active = active
        self.__checks_collisions = checks_collisions
        self.rd["tangible"] = tangible
        self.regulate_origin = regulate_origin
        self.collision_ellipse = collision_ellipse
        self.collision_precise = collision_precise
        self.rd["xv"] = xvelocity
        self.rd["yv"] = yvelocity
        self.rd["mv_dir"] = 0
        self.rd["speed"] = 0
        self.xacceleration = xacceleration
        self.yacceleration = yacceleration
        self.xdeceleration = xdeceleration
        self.ydeceleration = ydeceleration
        self.rd["image_index"] = None
        self.image_index = image_index
        self.image_origin_x = image_origin_x
        self.image_origin_y = image_origin_y
        self.image_xscale = image_xscale
        self.image_yscale = image_yscale
        self.image_rotation = image_rotation
        self.image_alpha = image_alpha
        self.image_blend = image_blend
        self.image_blend_mode = image_blend_mode
        self.alarms = {}
        self.xstart = x
        self.ystart = y
        self.xprevious = x
        self.yprevious = y
        self.rd["anim_count"] = 0
        self.__origins_x = {}
        self.__origins_y = {}
        self.rd["object_areas"] = set()
        self.rd["colliders"] = []
        self.__masks = {}

        self.rd["sprite"] = sprite
        if sprite is not None:
            self.image_index %= sprite.frames
            sprite_bbox_x = self.sprite.bbox_x
            sprite_bbox_y = self.sprite.bbox_y
            sprite_bbox_width = self.sprite.bbox_width
            sprite_bbox_height = self.sprite.bbox_height
        else:
            sprite_bbox_x = 0
            sprite_bbox_y = 0
            sprite_bbox_width = 1
            sprite_bbox_height = 1
        self.__bbox_x = bbox_x if bbox_x is not None else sprite_bbox_x
        self.__bbox_y = bbox_y if bbox_y is not None else sprite_bbox_y
        self.__bbox_width = (bbox_width if bbox_width is not None else
                             sprite_bbox_width)
        self.__bbox_height = (bbox_height if bbox_height is not None else
                              sprite_bbox_height)

        self.visible = visible
        self.image_fps = image_fps

        o_set_speed(self)

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

          - A :class:`sge.dsp.Object` object.
          - A list of :class:`sge.dsp.Object` objects.
          - A class derived from :class:`sge.dsp.Object`.
          - :const:`None`: Check for collisions with all objects.

        - ``x`` -- The horizontal position to pretend this object is at
          for the purpose of the collision detection.  If set to
          :const:`None`, :attr:`x` will be used.
        - ``y`` -- The vertical position to pretend this object is at
          for the purpose of the collision detection.  If set to
          :const:`None`, :attr:`y` will be used.
        """
        room = sge.game.current_room
        if self.tangible and self in room.objects:
            collisions = []

            # Change x and y to be offset values; these are easier to use.
            if x is not None:
                x -= self.x
            else:
                x = 0

            if y is not None:
                y -= self.y
            else:
                y = 0

            if self.collision_precise:
                ax = self.mask_x + x
                ay = self.mask_y + y
                w = len(self.mask)
                h = len(self.mask[0]) if self.mask else 0
            else:
                ax = self.bbox_left + x
                ay = self.bbox_top + y
                w = self.bbox_width
                h = self.bbox_height

            others = room.get_objects_at(ax, ay, w, h)

            for obj in others:
                if obj is not self and obj.tangible and o_is_other(obj, other):
                    if (self.collision_precise or self.collision_ellipse or
                            obj.collision_precise or obj.collision_ellipse):
                        # Use masks.
                        if sge.collision.masks_collide(
                                self.mask_x + x, self.mask_y + y, self.mask,
                                obj.mask_x, obj.mask_y, obj.mask):
                            collisions.append(obj)
                    else:
                        # Use bounding boxes.
                        if sge.collision.rectangles_collide(
                                self.bbox_left + x, self.bbox_top + y,
                                self.bbox_width, self.bbox_height,
                                obj.bbox_left, obj.bbox_top, obj.bbox_width,
                                obj.bbox_height):
                            collisions.append(obj)

            return collisions
        else:
            return []

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

        See the documentation for :meth:`sge.dsp.Game.event_step` for
        more information.
        """
        pass

    def event_step(self, time_passed, delta_mult):
        """
        Called each frame after automatic updates to objects (such as
        the effects of the speed variables), but before collision
        events.

        See the documentation for :meth:`sge.dsp.Game.event_step` for
        more information.
        """
        pass

    def event_end_step(self, time_passed, delta_mult):
        """
        Called each frame after collision events.

        See the documentation for :meth:`sge.dsp.Game.event_step` for
        more information.
        """
        pass

    def event_alarm(self, alarm_id):
        """
        See the documentation for :attr:`sge.dsp.Object.alarms` for more
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

    def event_joystick(self, js_name, js_id, input_type, input_id, value):
        """
        See the documentation for :class:`sge.input.JoystickEvent` for
        more information.
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

        See the documentation for :meth:`sge.dsp.Game.event_step` for
        more information.
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
        See the documentation for :meth:`sge.dsp.Game.event_step` for
        more information.
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

    def event_paused_joystick(self, js_name, js_id, input_type, input_id,
                              value):
        """
        See the documentation for :class:`sge.input.JoystickEvent` for
        more information.
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

    @property
    def x(self):
        if (sge.game.current_room is not None and
                (not sge.game.grab_input or sge.game.mouse.visible)):
            mouse_x = sge.mouse.get_x()
            mouse_y = sge.mouse.get_y()
            for view in sge.game.current_room.views:
                if (view.xport <= mouse_x < view.xport + view.wport and
                        view.yport <= mouse_y < view.yport + view.hport):
                    return ((mouse_x - view.xport) *
                            (view.width / view.wport) + view.x)

        return -1

    @x.setter
    def x(self, value):
        pass

    @property
    def y(self):
        if (sge.game.current_room is not None and
                (not sge.game.grab_input or sge.game.mouse.visible)):
            mouse_x = sge.mouse.get_x()
            mouse_y = sge.mouse.get_y()
            for view in sge.game.current_room.views:
                if (view.xport <= mouse_x <= view.xport + view.wport and
                        view.yport <= mouse_y <= view.yport + view.hport):
                    return ((mouse_y - view.yport) *
                            (view.height / view.hport) + view.y)

        return -1

    @y.setter
    def y(self, value):
        pass

    @property
    def sprite(self):
        return self.rd["sprite"]

    @sprite.setter
    def sprite(self, value):
        self.rd["sprite"] = value
        self.set_cursor()

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.__visible = value
        self.set_cursor()

    @property
    def tangible(self):
        if self.x != -1 and self.y != -1:
            return self.rd["tangible"]
        else:
            return False

    @tangible.setter
    def tangible(self, value):
        self.rd["tangible"] = value

    def __init__(self):
        self.__visible = True
        super(Mouse, self).__init__(0, 0, 10000)

    def event_step(self, time_passed, delta_mult):
        o_update_object_areas(self)
        o_update_collision_lists(self)

    def event_collision(self, other, xdirection, ydirection):
        sge.game.event_mouse_collision(other, xdirection, ydirection)

    def set_cursor(self):
        # Set the mouse cursor and visibility state.
        if not sge.game.grab_input:
            pygame.mouse.set_visible(self.visible and self.sprite is None)
        else:
            pygame.mouse.set_visible(False)

    def project_cursor(self):
        if (not sge.game.grab_input and self.visible and
                self.sprite is not None):
            img = s_get_image(self.sprite, self.image_index, self.image_xscale,
                              self.image_yscale, self.image_rotation,
                              self.image_alpha, self.image_blend,
                              self.image_blend_mode)
            x = sge.mouse.get_x()
            y = sge.mouse.get_y()

            if x is not None and y is not None:
                x -= self.image_origin_x
                y -= self.image_origin_y
                r.game_window_projections.append((img, x, y, self.z, None))
