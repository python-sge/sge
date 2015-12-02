# Copyright (C) 2012, 2013, 2014, 2015 Julian Marchant <onpon4@riseup.net>
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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import math
import warnings

import pygame
import six

import sge
from sge import r
from sge.r import (_scale, _get_blend_flags, _screen_blend, _set_mode,
                   _handle_music, _get_dot_sprite, _get_line_sprite,
                   _get_rectangle_sprite, _get_ellipse_sprite,
                   _get_circle_sprite, _get_polygon_sprite, bl_update,
                   bl_get_image, o_update, o_detect_collisions,
                   o_update_collision_lists, o_update_object_areas,
                   s_get_image, r_set_object_areas)


__all__ = ['Game']


class Game(object):

    """
    This class handles most parts of the game which operate on a global
    scale, such as global game events.  Before anything else is done
    with the SGE, an object either of this class or of a class derived
    from it must be created.

    When an object of this class is created, it is automatically
    assigned to :data:`sge.game`.

    .. note::

       Do not create multiple :class:`sge.Game` objects.  Doing so is
       unsupported and may cause errors.

    .. attribute:: width

       The width of the game's display.

    .. attribute:: height

       The height of the game's display.

    .. attribute:: fullscreen

       Whether or not the game should be in fullscreen.

    .. attribute:: scale

       A number indicating a fixed scale factor (e.g. ``1`` for no
       scaling, ``2`` for doubled size).  If set to :const:`None` or
       ``0``, scaling is automatic (causes the game to fit the window or
       screen).

    .. attribute:: scale_proportional

       If set to :const:`True`, scaling is always proportional.  If set
       to :const:`False`, the image will be distorted to completely fill
       the game window or screen.  This has no effect unless
       :attr:`scale` is :const:`None` or ``0``.

    .. attribute:: scale_smooth

       Whether or not a smooth scaling algorithm (as opposed to a simple
       scaling algorithm such as nearest-neighbor) should be used.

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
       specified does not exist, :exc:`IOError` is raised.

    .. attribute:: collision_events_enabled

       Whether or not collision events should be executed.  Setting this
       to :const:`False` will improve performence if collision events
       are not needed.

    .. attribute:: alarms

       A dictionary containing the global alarms of the game.  Each
       value decreases by 1 each frame (adjusted for delta timing if it
       is enabled).  When a value is at or below 0,
       :meth:`sge.Game.event_alarm` is executed with ``alarm_id`` set to
       the respective key, and the item is deleted from this dictionary.

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

       A :class:`sge.Object` object which represents the mouse
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
    def scale_smooth(self):
        return r.game_scale_smooth

    @scale_smooth.setter
    def scale_smooth(self, value):
        if value != r.game_scale_smooth:
            r.game_scale_smooth = value
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
                raise IOError(e)
            else:
                pygame.display.set_icon(image)

    def __init__(self, width=640, height=480, fullscreen=False, scale=None,
                 scale_proportional=True, scale_smooth=False, fps=60,
                 delta=False, delta_min=15, delta_max=None, grab_input=False,
                 window_text=None, window_icon=None,
                 collision_events_enabled=True):
        """
        Arguments set the respective initial attributes of the game.
        See the documentation for :class:`sge.Game` for more
        information.

        The created :class:`sge.Game` object is automatically assigned
        to :data:`sge.game`.
        """
        # Settings use a smaller buffer size for less lag.
        pygame.mixer.pre_init(channels=2, buffer=1024)
        pygame.init()

        pygame.mixer.music.set_endevent(sge.MUSIC_END_EVENT)

        sge.game = self

        r.game_width = width
        r.game_height = height
        r.game_window_width = width
        r.game_window_height = height
        r.game_fullscreen = fullscreen
        r.game_scale = scale
        r.game_scale_proportional = scale_proportional
        r.game_scale_smooth = scale_smooth
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
        self.mouse = sge.Mouse()

        # Setup sound channels
        r.game_available_channels = []
        if pygame.mixer.get_init():
            for i in six.moves.range(pygame.mixer.get_num_channels()):
                r.game_available_channels.append(pygame.mixer.Channel(i))

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

                    r_set_object_areas(new_room)
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
            try:
                sprite = sge.Sprite("pause", os.path.dirname(__file__))
            except IOError:
                font = sge.Font("Droid Sans", size=24)
                sprite = sge.Sprite(width=320, height=240)
                sprite.draw_text(font, "Paused", 160, 120, halign="center",
                                 valign="middle")

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
                    w = "Don't know how to handle the key, ``{}``.".format(
                        event.key)
                    warnings.warn(w)
                else:
                    input_event = sge.input.KeyPress(k, event.unicode)
                    self.input_events.append(input_event)
            elif event.type == pygame.KEYUP:
                try:
                    k = sge.KEY_NAMES[event.key]
                except KeyError:
                    w = "Don't know how to handle the key, ``{}``.".format(
                        event.key)
                else:
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
                input_event = sge.input.JoystickAxisMove(
                    jsname, event.joy, event.axis, event.value)
                self.input_events.append(input_event)
            elif event.type == pygame.JOYHATMOTION:
                jsname = r.game_js_names[event.joy]
                input_event = sge.input.JoystickHatMove(
                    jsname, event.joy, event.hat, event.value[0],
                    -event.value[1])
                self.input_events.append(input_event)
            elif event.type == pygame.JOYBALLMOTION:
                jsname = r.game_js_names[event.joy]
                input_event = sge.input.JoystickTrackballMove(
                    jsname, event.joy, event.ball, *event.rel)
                self.input_events.append(input_event)
            elif event.type == pygame.JOYBUTTONDOWN:
                jsname = r.game_js_names[event.joy]
                input_event = sge.input.JoystickButtonPress(jsname, event.joy,
                                                            event.button)
                self.input_events.append(input_event)
            elif event.type == pygame.JOYBUTTONUP:
                jsname = r.game_js_names[event.joy]
                input_event = sge.input.JoystickButtonRelease(
                    jsname, event.joy, event.button)
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

        # Clear display surface
        r.game_display_surface.fill((0, 0, 0))

        # Draw views
        for view in self.current_room.views:
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
                x = layer.x - (vx * layer.xscroll_rate)
                y = layer.y - (vy * layer.yscroll_rate)
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
                    hrange = six.moves.range(int(x),
                                             int(view.width + img_w), img_w)
                elif layer.repeat_left and x + img_w > 0:
                    hrange = six.moves.range(int(x), -img_w, -img_w)
                else:
                    hrange = [x]

                if layer.repeat_down and (layer.repeat_up or y < view_height):
                    vrange = six.moves.range(int(y),
                                             int(view_height + img_h), img_h)
                elif layer.repeat_up and y + img_h > 0:
                    vrange = six.moves.range(int(y), -img_h, -img_h)
                else:
                    vrange = [y]

                for y in vrange:
                    for x in hrange:
                        images.append((img, x + view_x, y + view_y, layer.z,
                                       None))

            for obj in self.current_room.get_objects_at(
                    view.x, view.y, view.width, view.height):
                if (obj.visible and obj.sprite is not None and
                        obj is not self.mouse):
                    img = s_get_image(obj.sprite, obj.image_index,
                                      obj.image_xscale, obj.image_yscale,
                                      obj.image_rotation, obj.image_alpha,
                                      obj.image_blend)
                    w = img.get_width()
                    h = img.get_height()
                    x = obj.x - obj.image_origin_x
                    y = obj.y - obj.image_origin_y
                    if (x + w >= view_x and x <= view_x + view_width and
                            y + h >= view_y and y <= view_y + view_height):
                        nimg = s_get_image(obj.sprite, obj.image_index,
                                           obj.image_xscale, obj.image_yscale)
                        nw = nimg.get_width()
                        nh = nimg.get_height()
                        xoff = (w - nw) / 2
                        yoff = (h - nh) / 2
                        images.append((img, x - xoff, y - yoff,
                                       obj.z, None))

            images.extend(self.current_room.rd["projections"])

            images.sort(key=lambda img: img[3])

            for img in images:
                x = img[1] - view.x
                y = img[2] - view.y
                blend_mode = img[4]
                if blend_mode == sge.BLEND_RGB_SCREEN:
                    _screen_blend(view_surf, img[0], x, y, False)
                elif blend_mode == sge.BLEND_RGBA_SCREEN:
                    _screen_blend(view_surf, img[0], x, y, True)
                else:
                    flags = _get_blend_flags(blend_mode)
                    view_surf.blit(img[0], (x, y), None, flags)

            r.game_display_surface.blit(
                _scale(view_surf, view.wport, view.hport),
                (view.xport, view.yport))

        self.current_room.rd["projections"] = []

        # Window projections
        self.mouse.project_cursor()
        r.game_window_projections.sort(key=lambda img: img[3])
        for projection in r.game_window_projections:
            (image, x, y, z, blend_mode) = projection
            if blend_mode == sge.BLEND_RGB_SCREEN:
                _screen_blend(r.game_display_surface, image, x, y, False)
            elif blend_mode == sge.BLEND_RGBA_SCREEN:
                _screen_blend(r.game_display_surface, image, x, y, True)
            else:
                flags = _get_blend_flags(blend_mode)
                r.game_display_surface.blit(image, (x, y), None, flags)

        r.game_window_projections = []

        # Scale/blit display surface
        r.game_window.blit(
            _scale(r.game_display_surface, self.width * r.game_xscale,
                   self.height * r.game_yscale), (r.game_x, r.game_y))

        pygame.display.flip()

    def project_dot(self, x, y, color, z=0):
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
           :class:`sge.Object` objects.  Window projections are always
           positioned in front of such things.

        See the documentation for :meth:`sge.Sprite.draw_dot` for more
        information.
        """
        if not isinstance(color, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(color))
            raise TypeError(e)

        sprite = _get_dot_sprite(color)
        self.project_sprite(sprite, 0, x, y, z)

    def project_line(self, x1, y1, x2, y2, color, z=0, thickness=1,
                     anti_alias=False):
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

        See the documentation for :meth:`sge.Sprite.draw_line` and
        :meth:`sge.Game.project_dot` for more information.
        """
        if not isinstance(color, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(color))
            raise TypeError(e)

        thickness = abs(thickness)
        x = min(x1, x2) - thickness // 2
        y = min(y1, y2) - thickness // 2
        x1 -= x
        y1 -= y
        x2 -= x
        y2 -= y

        sprite = _get_line_sprite(x1, y1, x2, y2, color, thickness, anti_alias)
        self.project_sprite(sprite, 0, x, y, z)

    def project_rectangle(self, x, y, width, height, z=0, fill=None,
                          outline=None, outline_thickness=1):
        """
        Project a rectangle onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the rectangle.
        - ``y`` -- The vertical location relative to the window to
          project the rectangle.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.Sprite.draw_rectangle` and
        :meth:`sge.Game.project_dot` for more information.
        """
        if fill is not None and not isinstance(fill, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(outline))
            raise TypeError(e)

        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = _get_rectangle_sprite(width, height, fill, outline,
                                       outline_thickness)
        self.project_sprite(sprite, 0, x, y, z)

    def project_ellipse(self, x, y, width, height, z=0, fill=None,
                        outline=None, outline_thickness=1, anti_alias=False):
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

        See the documentation for :meth:`sge.Sprite.draw_ellipse` and
        :meth:`sge.Game.project_dot` for more information.
        """
        if fill is not None and not isinstance(fill, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(outline))
            raise TypeError(e)

        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = _get_ellipse_sprite(width, height, fill, outline,
                                     outline_thickness, anti_alias)
        self.project_sprite(sprite, 0, x, y, z)

    def project_circle(self, x, y, radius, z=0, fill=None, outline=None,
                       outline_thickness=1, anti_alias=False):
        """
        Project a circle onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          position the center of the circle.
        - ``y`` -- The vertical location relative to the window to
          position the center of the circle.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.Sprite.draw_circle` and
        :meth:`sge.Game.project_dot` for more information.
        """
        if fill is not None and not isinstance(fill, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(outline))
            raise TypeError(e)

        sprite = _get_circle_sprite(radius, fill, outline, outline_thickness,
                                    anti_alias)
        self.project_sprite(sprite, 0, x - radius, y - radius, z)

    def project_polygon(self, points, z=0, fill=None, outline=None,
                        outline_thickness=1, anti_alias=False):
        """
        Draw a polygon on the sprite.

        Arguments:

        - ``points`` -- A list of points relative to the room to
          position each of the polygon's angles.  Each point should be a
          tuple in the form ``(x, y)``, where x is the horizontal
          location and y is the vertical location.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.Sprite.draw_polygon` and
        :meth:`sge.Game.project_dot` for more information.
        """
        if fill is not None and not isinstance(fill, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(outline))
            raise TypeError(e)

        xlist = []
        ylist = []
        for point in points:
            xlist.append(point[0])
            ylist.append(point[1])
        x = min(xlist)
        y = min(ylist)

        sprite = _get_polygon_sprite(points, fill, outline, outline_thickness,
                                     anti_alias)
        self.project_sprite(sprite, 0, x, y, z)

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

        See the documentation for :meth:`sge.Sprite.draw_sprite` and
        :meth:`sge.Game.project_dot` for more information.
        """
        img = s_get_image(sprite, image)
        x -= sprite.origin_x
        y -= sprite.origin_y
        r.game_window_projections.append((img, x, y, z, blend_mode))

    def project_text(self, font, text, x, y, z=0, width=None, height=None,
                    color=sge.Color("black"), halign="left",
                    valign="top", anti_alias=True):
        """
        Project text onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the text.
        - ``y`` -- The vertical location relative to the window to
          project the text.
        - ``z`` -- The Z-axis position of the projection in relation to
          other window projections.

        See the documentation for :meth:`sge.Sprite.draw_text` and
        :meth:`sge.Game.project_dot` for more information.
        """
        if not isinstance(color, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(color))
            raise TypeError(e)

        sprite = sge.Sprite.from_text(font, text, width, height, color, halign,
                                      valign, anti_alias)
        self.project_sprite(sprite, 0, x, y, z)

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

        See the documentation for :attr:`sge.Game.alarms` for more
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

        This is always called after any :meth:`sge.Room.event_close`
        occurring at the same time.
        """
        pass

    def event_mouse_collision(self, other, xdirection, ydirection):
        """
        Proxy for :meth:`sge.game.mouse.event_collision`.  See the
        documentation for :meth:`sge.Object.event_collision` for more
        information.
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
        See the documentation for :meth:`sge.Game.event_close` for more
        information.
        """
        pass
