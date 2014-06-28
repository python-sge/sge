# Copyright (C) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
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

import os
import warnings

import pygame

import sge


__all__ = ['Game']


class Game:

    """Class which handles the game.

    This class handles most parts of the game which operate on a global
    scale, such as global game events.  Before anything else is done
    with the SGE, an object either of this class or of a class derived
    from it must be created.

    When an object of this class is created, it is automatically
    assigned to :data:`sge.game`.

    Note: Do not create multiple :class:`sge.Game` objects.  Doing so
    may cause errors.

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

    .. attribute:: grab_input

       Whether or not all input should be forcibly grabbed by the game.
       If this is :const:`True` and the mouse cursor is invisible, the
       mouse will enter relative mode.

    .. attribute:: window_text

       The text for the OS to display as the window title, e.g. in the
       frame of the window.  If set to :const:`None`, the SGE chooses
       the text.

    .. attribute:: window_icon

       The name of the image file located in one of the directories
       specified in :data:`sge.image_directories` to use as the window
       icon.  If set to :const:`None`, the SGE chooses the icon.

    .. attribute:: collision_events_enabled

       Whether or not collision events should be executed.  Setting this
       to :const:`False` will improve performence if collision events
       are not needed.

    .. attribute:: input_events

       A list containing all input event objects which have not yet been
       handled, in the order in which they occurred.

       .. note::

          If you handle input events manually, be sure to delete them
          from this list, preferably by getting them with
          :meth:`list.pop`.  Otherwise, the event will be handled more
          than once, which is usually not what you want.

    .. attribute:: registered_classes

       A list containing all classes which have been registered with
       :meth:`sge.Game.register_class`.  (Read-only)

    .. attribute:: sprites

       A dictionary containing all loaded sprites, indexed by the
       sprites' :attr:`sge.Sprite.id` attributes.  (Read-only)

    .. attribute:: background_layers

       A dictionary containing all loaded background layers, indexed by
       the layers' :attr:`sge.BackgroundLayer.id` attributes.
       (Read-only)

    .. attribute:: backgrounds

       A dictionary containing all loaded backgrounds, indexed by the
       backgrounds' :attr:`sge.Background.id` attributes.  (Read-only)

    .. attribute:: fonts

       A dictionary containing all loaded fonts, indexed by the fonts'
       :attr:`sge.Font.id` attributes.  (Read-only)

    .. attribute:: sounds

       A dictionary containing all loaded sounds, indexed by the sounds'
       :attr:`sge.Sound.id` attributes.  (Read-only)

    .. attribute:: music

       A dictionary containing all loaded music, indexed by the music
       objects' :attr:`sge.Music.id` attributes.  (Read-only)

    .. attribute:: objects

       A dictionary containing all :class:`sge.StellarClass` objects in
       the game, indexed by the objects' :attr:`sge.StellarClass.id`
       attributes.  (Read-only)

    .. attribute:: rooms

       A list containing all rooms in order of their creation.
       (Read-only)

    .. attribute:: current_room

       The room which is currently active.  (Read-only)

    .. attribute:: mouse

       A :class:`sge.StellarClass` object which represents the mouse
       cursor.  Its :attr:`sge.StellarClass.id` attribute is ``"mouse"``
       and its bounding box is a one-pixel square.  Speed variables are
       determined by averaging all mouse movement during the last
       quarter of a second.  Assigning to its
       :attr:`sge.StellarClass.visible` attribute controls whether or
       not the mouse cursor is shown.  Setting its sprite sets the mouse
       cursor to that sprite.

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
            if not self.fullscreen and not self.scale:
                old_scale = self.scale
                self.scale = 1
                self.scale = old_scale

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
        return self._window_icon

    @window_icon.setter
    def window_icon(self, value):
        self._window_icon = value
        if value is not None:
            for path in sge.image_directories:
                try:
                    image = pygame.image.load(os.path.join(path, value))
                except pygame.error:
                    continue
                else:
                    pygame.display.set_icon(image)
                    break

    def __init__(self, width=640, height=480, fullscreen=False, scale=None,
                 scale_proportional=True, scale_smooth=False, fps=60,
                 delta=False, delta_min=15, grab_input=False,
                 window_text=None, window_icon=None,
                 collision_events_enabled=True):
        """Constructor method.

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
        self.window_text = window_text
        self.window_icon = window_icon
        self.collision_events_enabled = collision_events_enabled

        self.input_events = []
        self.registered_classes = []
        self.sprites = {}
        self.background_layers = {}
        self.backgrounds = {}
        self.fonts = {}
        self.sounds = {}
        self.music = {}
        self.objects = {}
        self.rooms = []
        self.current_room = None

        self._set_mode()

        self._background_changed = False
        self._colliders = []
        self._music = None
        self._music_queue = []
        self._running = False
        self._clock = pygame.time.Clock()
        self._pygame_sprites = pygame.sprite.LayeredDirty()
        self._numviews = 0
        self._background = None
        self._cleanup_rects = []
        self._window_projections = []
        self.mouse = sge.Mouse()

        # Setup sound channels
        self._available_channels = []
        if pygame.mixer.get_init():
            for i in range(pygame.mixer.get_num_channels()):
                self._available_channels.append(pygame.mixer.Channel(i))

        # Setup joysticks
        sge.joystick.refresh()

        if not pygame.font.get_init():
            w = "pygame.font module not initialized! Are you missing SDL_ttf?"
            warnings.warn(w)

        self.window_icon = None

        self._alarms = {}

        self._start_sprites = {}
        self._start_background_layers = {}
        self._start_backgrounds = {}
        self._start_fonts = {}
        self._start_sounds = {}
        self._start_music = {}
        self._start_objects = {}
        self._start_rooms = []

        self._object_start_x = {}
        self._object_start_y = {}
        self._object_start_z = {}
        self._object_start_sprite = {}
        self._object_start_visible = {}
        self._object_start_checks_collisions = {}
        self._object_start_tangible = {}
        self._object_start_bbox_x = {}
        self._object_start_bbox_y = {}
        self._object_start_bbox_width = {}
        self._object_start_bbox_height = {}
        self._object_start_collision_ellipse = {}
        self._object_start_collision_precise = {}

        self._dot_cache = {}
        self._line_cache = {}
        self._rectangle_cache = {}
        self._ellipse_cache = {}
        self._circle_cache = {}
        self._text_cache = {}

    def start(self):
        """Start the game at the first room.

        Can be called in the middle of a game to start the game over.
        If you do this, everything will be reset to its original state.

        """
        if self._running:
            if sge.DEBUG:
                print("Restarting the game.")

            self.sprites = self._start_sprites
            self.background_layers = self._start_background_layers
            self.backgrounds = self._start_backgrounds
            self.fonts = self._start_fonts
            self.sounds = self._start_sounds
            self.music = self._start_music
            self.objects = self._start_objects
            self.rooms = self._start_rooms

            for i in self.objects:
                obj = self.objects[i]
                if obj is not sge.game.mouse:
                    obj.x = self._object_start_x[obj.id]
                    obj.y = self._object_start_y[obj.id]

                obj.z = self._object_start_z[obj.id]
                obj.sprite = self._object_start_sprite[obj.id]
                obj.visible = self._object_start_visible[obj.id]
                obj.checks_collisions = self._object_start_checks_collisions[obj.id]
                obj.tangible = self._object_start_tangible[obj.id]
                obj.bbox_x = self._object_start_bbox_x[obj.id]
                obj.bbox_y = self._object_start_bbox_y[obj.id]
                obj.bbox_width = self._object_start_bbox_width[obj.id]
                obj.bbox_height = self._object_start_bbox_height[obj.id]
                obj.collision_ellipse = self._object_start_collision_ellipse[obj.id]
                obj.collision_precise = self._object_start_collision_precise[obj.id]

            for room in self.rooms:
                room._reset()

            self.rooms[0].start()
        else:
            if sge.DEBUG:
                print("Starting the game.")
            self._running = True
            self._background_changed = True
            self.event_game_start()

            # Store the initial state of objects
            self._start_sprites = self.sprites
            self._start_background_layers = self.background_layers
            self._start_backgrounds = self.backgrounds
            self._start_fonts = self.fonts
            self._start_sounds = self.sounds
            self._start_music = self.music
            self._start_objects = self.objects
            self._start_rooms = self.rooms

            for i in self.objects:
                obj = self.objects[i]
                self._object_start_x[obj.id] = obj.x
                self._object_start_y[obj.id] = obj.y
                self._object_start_z[obj.id] = obj.z
                self._object_start_sprite[obj.id] = obj.sprite
                self._object_start_visible[obj.id] = obj.visible
                self._object_start_checks_collisions[obj.id] = obj.checks_collisions
                self._object_start_tangible[obj.id] = obj.tangible
                self._object_start_bbox_x[obj.id] = obj.bbox_x
                self._object_start_bbox_y[obj.id] = obj.bbox_y
                self._object_start_bbox_width[obj.id] = obj.bbox_width
                self._object_start_bbox_height[obj.id] = obj.bbox_height
                self._object_start_collision_ellipse[obj.id] = obj.collision_ellipse
                self._object_start_collision_precise[obj.id] = obj.collision_precise

            self._display_surface = self._window.copy()

            self.rooms[0].start()
            _fps_time = 0
            self._clock.tick()

            while self._running:
                # Input events
                self.pump_input()
                while self.input_events:
                    event = self.input_events.pop(0)

                    if isinstance(event, sge.input.KeyPress):
                        self.event_key_press(event.key, event.char)
                        self.current_room.event_key_press(event.key,
                                                          event.char)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_key_press(event.key, event.char)
                            else:
                                obj.event_inactive_key_press(event.key,
                                                             event.char)
                    elif isinstance(event, sge.input.KeyRelease):
                        self.event_key_release(event.key)
                        self.current_room.event_key_release(event.key)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_key_release(event.key)
                            else:
                                obj.event_inactive_key_release(event.key)
                    elif isinstance(event, sge.input.MouseMove):
                        self.event_mouse_move(event.x, event.y)
                        self.current_room.event_mouse_move(event.x, event.y)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_mouse_move(event.x, event.y)
                            else:
                                obj.event_inactive_mouse_move(event.x, event.y)
                    elif isinstance(event, sge.input.MouseButtonPress):
                        self.event_mouse_button_press(event.button)
                        self.current_room.event_mouse_button_press(
                            event.button)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_mouse_button_press(event.button)
                            else:
                                obj.event_inactive_mouse_button_press(
                                    event.button)
                    elif isinstance(event, sge.input.MouseButtonRelease):
                        self.event_mouse_button_release(event.button)
                        self.current_room.event_mouse_button_release(
                            event.button)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_mouse_button_release(event.button)
                            else:
                                obj.event_inactive_mouse_button_release(
                                    event.button)
                    elif isinstance(event, sge.input.JoystickAxisMove):
                        self.event_joystick_axis_move(
                            event.js_name, event.js_id, event.axis,
                            event.value)
                        self.current_room.event_joystick_axis_move(
                            event.js_name, event.js_id, event.axis,
                            event.value)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_axis_move(
                                    event.js_name, event.js_id, event.axis,
                                    event.value)
                            else:
                                obj.event_inactive_joystick_axis_move(
                                    event.js_name, event.js_id, event.axis,
                                    event.value)
                    elif isinstance(event, sge.input.JoystickHatMove):
                        self.event_joystick_hat_move(
                            event.js_name, event.js_id, event.hat, event.x,
                            event.y)
                        self.current_room.event_joystick_hat_move(
                            event.js_name, event.js_id, event.hat, event.x,
                            event.y)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_hat_move(
                                    event.js_name, event.js_id, event.hat,
                                    event.x, event.y)
                            else:
                                obj.event_inactive_joystick_hat_move(
                                    event.js_name, event.js_id, event.hat,
                                    event.x, event.y)
                    elif isinstance(event, sge.input.JoystickTrackballMove):
                        self.event_joystick_trackball_move(
                            event.js_name, event.js_id, event.ball, event.x,
                            event.y)
                        self.current_room.event_joystick_trackball_move(
                            event.js_name, event.js_id, event.ball, event.x,
                            event.y)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_trackball_move(
                                    event.js_name, event.js_id, event.ball,
                                    event.x, event.y)
                            else:
                                obj.event_inactive_joystick_trackball_move(
                                    event.js_name, event.js_id, event.ball,
                                    event.x, event.y)
                    elif isinstance(event, sge.input.JoystickButtonPress):
                        self.event_joystick_button_press(
                            event.js_name, event.js_id, event.button)
                        self.current_room.event_joystick_button_press(
                            event.js_name, event.js_id, event.button)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_button_press(
                                    event.js_name, event.js_id, event.button)
                            else:
                                obj.event_inactive_joystick_button_press(
                                    event.js_name, event.js_id, event.button)
                    elif isinstance(event, sge.input.JoystickButtonRelease):
                        self.event_joystick_button_release(
                            event.js_name, event.js_id, event.button)
                        self.current_room.event_joystick_button_release(
                            event.js_name, event.js_id, event.button)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_button_release(
                                    event.js_name, event.js_id, event.button)
                            else:
                                obj.event_inactive_joystick_button_release(
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

                if sge.DEBUG:
                    _fps_time += real_time_passed
                    if _fps_time >= 250:
                        _fps_time = 0
                        self.window_text = "FPS: {}; Delta: {}".format(
                            int(1000 / real_time_passed), delta_mult)

                # Alarms
                activated_alarms = []
                for a in self._alarms:
                    self._alarms[a] -= delta_mult
                    if self._alarms[a] <= 0:
                        activated_alarms.append(a)
                for a in activated_alarms:
                    del self._alarms[a]
                    self.event_alarm(a)

                activated_alarms = []
                for a in self.current_room._alarms:
                    self.current_room._alarms[a] -= delta_mult
                    if self.current_room._alarms[a] <= 0:
                        activated_alarms.append(a)
                for a in activated_alarms:
                    del self.current_room._alarms[a]
                    self.current_room.event_alarm(a)

                # Step events
                self.event_step(real_time_passed, delta_mult)
                self.current_room.event_step(real_time_passed, delta_mult)

                # Update background layers
                for i in self.background_layers:
                    self.background_layers[i]._update(time_passed)

                # Update objects (including mouse)
                for obj in self.current_room.objects:
                    if obj.active:
                        obj.event_begin_step(real_time_passed, delta_mult)
                        obj._update(time_passed, delta_mult)
                        obj.event_step(real_time_passed, delta_mult)
                    else:
                        obj.event_inactive_step(real_time_passed, delta_mult)

                    obj._update_collision_areas()

                if self.collision_events_enabled:
                    # Set objects' colliders
                    room = self.current_room
                    for ref in self._colliders:
                        obj = ref()
                        if obj is not None:
                            obj._colliders = []
                            for area in obj._collision_areas:
                                if area is not None:
                                    i, j = area
                                    room_area = room._collision_areas[i][j]
                                else:
                                    room_area = room._collision_area_void

                                for other in room_area:
                                    if (other is not obj and
                                            other not in obj._colliders):
                                        obj._colliders.append(other)

                    # Detect collisions
                    for ref in self._colliders:
                        obj = ref()
                        if obj is not None:
                            obj._detect_collisions()

                # End step event
                for obj in self.current_room.objects:
                    if obj.active:
                        obj.event_end_step(real_time_passed, delta_mult)
                    else:
                        obj.event_inactive_end_step(real_time_passed,
                                                    delta_mult)

                # Set xprevious and yprevious
                for obj in self.current_room.objects:
                    obj.xprevious = obj.x
                    obj.yprevious = obj.y

                # Refresh
                self.refresh()

            self.event_game_end()
            pygame.quit()
            sge.game = None
            if sge.DEBUG:
                print("Game ended normally.")

    def end(self):
        """Properly end the game."""
        self._running = False

    def pause(self, sprite=None):
        """Pause the game.

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
            sge.image_directories.append(os.path.dirname(__file__))
            try:
                sprite = sge.Sprite("_pygame_sge_pause")
            except IOError:
                font = sge.Font("Droid Sans", size=24)
                sprite = sge.Sprite(width=320, height=240)
                sprite.draw_text(font, "Paused", 160, 120,
                                 halign=sge.ALIGN_CENTER,
                                 valign=sge.ALIGN_MIDDLE)
                font.destroy()

            del sge.image_directories[-1]

        self._paused = True

        while self._paused and self._running:
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
            self.regulate_speed()

            # Project sprite
            x = (self.width - sprite.width) / 2
            y = (self.height - sprite.height) / 2
            self.project_sprite(sprite, 0, x, y)

            # Refresh
            self.refresh()

        sprite.destroy()
        self.pump_input()
        self.input_events = []

    def unpause(self):
        """Unpause the game."""
        self._paused = False

    def pump_input(self):
        """Cause the SGE to recieve input from the OS.

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
                mx, my = event.pos
                self.mouse.mouse_x = mx - self._x
                self.mouse.mouse_y = my - self._y
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
                jsname = self._js_names[event.joy]
                input_event = sge.input.JoystickAxisMove(
                    jsname, event.joy, event.axis, event.value)
                self.input_events.append(input_event)
            elif event.type == pygame.JOYHATMOTION:
                jsname = self._js_names[event.joy]
                input_event = sge.input.JoystickHatMove(
                    jsname, event.joy, event.hat, *event.value)
                self.input_events.append(input_event)
            elif event.type == pygame.JOYBALLMOTION:
                jsname = self._js_names[event.joy]
                input_event = sge.input.JoystickTrackballMove(
                    jsname, event.joy, event.ball, *event.rel)
                self.input_events.append(input_event)
            elif event.type == pygame.JOYBUTTONDOWN:
                jsname = self._js_names[event.joy]
                input_event = sge.input.JoystickButtonPress(jsname, event.joy,
                                                            event.button)
                self.input_events.append(input_event)
            elif event.type == pygame.JOYBUTTONUP:
                jsname = self._js_names[event.joy]
                input_event = sge.input.JoystickButtonRelease(
                    jsname, event.joy, event.button)
                self.input_events.append(input_event)
            elif event.type == pygame.ACTIVEEVENT:
                if event.gain:
                    if 2 & event.state:
                        # Gain keyboard focus
                        if sge.DEBUG:
                            print('Gained keyboard focus.')
                        self.input_events.append(sge.input.KeyboardFocusGain())
                    if 1 & event.state:
                        # Gain mouse focus
                        if sge.DEBUG:
                            print('Gained mouse focus.')
                        self.input_events.append(sge.input.KeyboardFocusLose())
                else:
                    if 2 & event.state:
                        # Lose keyboard focus
                        if sge.DEBUG:
                            print('Lost keyboard focus.')
                        self.input_events.append(sge.input.MouseFocusGain())
                    if 1 & event.state:
                        # Lose mouse focus
                        if sge.DEBUG:
                            print('Lost mouse focus.')
                        self.input_events.append(sge.input.MouseFocusLose())
            elif event.type == pygame.QUIT:
                if sge.DEBUG:
                    print('Quit requested by the system.')
                self.input_events.append(sge.input.QuitRequest())
            elif event.type == pygame.VIDEORESIZE:
                if sge.DEBUG:
                    print('Video resize detected.')
                self._window.blit(self._display_surface, (0, 0))
                self._window_width = event.w
                self._window_height = event.h
                self._set_mode()
            elif event.type == sge.MUSIC_END_EVENT:
                if self._music_queue:
                    music = self._music_queue.pop(0)
                    music[0].play(*music[1:])

    def regulate_speed(self, fps=None):
        """Regulate the SGE's running speed and return the time passed.

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
            fps = self.fps

        return self._clock.tick(fps)

    def refresh(self):
        """Refresh the screen.

        This method needs to be called for changes to the screen to be
        seen by the user.  It should be called every frame.

        You normally don't need to use this function directly.  It is
        called automatically in each frame of the SGE's main loop.  You
        only need to use this function directly if you take control away
        from the SGE's main loop, e.g. to create your own loop.

        """
        # Music control
        self._handle_music()

        # Check for changes in views
        if self._numviews != len(self.current_room.views):
            self._numviews = len(self.current_room.views)
            self._background_changed = True

        # Redraw
        w = max(1, self._display_surface.get_width())
        h = max(1, self._display_surface.get_height())
        if self._background_changed or self._background is None:
            self._background = pygame.Surface((w, h))
            b = self.current_room.background._get_background()
            self._background.blit(b, (self._x, self._y))
            self._display_surface.blit(self._background, (0, 0))
            self._background_changed = False
            self._pygame_sprites.clear(self._display_surface, self._background)
            for sprite in self._pygame_sprites:
                sprite.rect = pygame.Rect(0, 0, 1, 1)
                sprite.image = pygame.Surface((1, 1))
                sprite.image.set_colorkey((0, 0, 0))
            self._pygame_sprites.update()
            self._pygame_sprites.draw(self._display_surface)
            dirty = [self._display_surface.get_rect()]
        else:
            self._pygame_sprites.clear(self._display_surface, self._background)
            self._pygame_sprites.update()
            dirty = self._pygame_sprites.draw(self._display_surface)

        self._window.blit(self._display_surface, (0, 0))

        # Window projections
        self.mouse.project_cursor()
        dirty.extend(self._cleanup_rects)
        self._cleanup_rects = self._show_projections()
        dirty.extend(self._cleanup_rects)

        # Letterbox/pillarbox
        top_bar = pygame.Rect(0, 0, w, self._y)
        bottom_bar = pygame.Rect(0, h - self._y, w, self._y)
        left_bar = pygame.Rect(0, 0, self._x, h)
        right_bar = pygame.Rect(w - self._x, 0, self._x, h)
        if top_bar.h > 0:
            self._window.fill((0, 0, 0), top_bar)
            dirty.append(top_bar)
        if bottom_bar.h > 0:
            self._window.fill((0, 0, 0), bottom_bar)
            dirty.append(bottom_bar)
        if left_bar.w > 0:
            self._window.fill((0, 0, 0), left_bar)
            dirty.append(left_bar)
        if right_bar.w > 0:
            self._window.fill((0, 0, 0), right_bar)
            dirty.append(right_bar)

        if sge.hardware_rendering:
            pygame.display.flip()
        else:
            pygame.display.update(dirty)

    def register_class(self, cls):
        """Register a class with the SGE.

        Registered classes can be used to index objects by, e.g. for
        :attr:`sge.Room.objects_by_class`.  A list of all currently
        registered classes can be found in :attr:`registered_classes`.

        """
        if cls not in self.registered_classes:
            self.registered_classes.append(cls)

            for room in self.rooms:
                room.objects_by_class[cls] = []
                for obj in room.objects:
                    if isinstance(obj, cls):
                        room.objects_by_class[cls].append(obj)

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Arguments:

        - ``alarm_id`` -- The unique identifier of the alarm to set.
          Any value can be used as a unique identifier for an alarm.
        - ``value`` -- The value to set the alarm to.  Set to
          :const:`None` to disable the alarm.

        After this method is called, ``value`` will reduce by 1 each
        frame (adjusted for delta timing if it is enabled) until it
        reaches 0, at which point :meth:`sge.Game.event_alarm` will be
        executed with ``alarm_id``.

        """
        if value is not None:
            self._alarms[alarm_id] = value
        elif alarm_id in self._alarms:
            del self._alarms[alarm_id]

    def get_alarm(self, alarm_id):
        """Return the value of an alarm.

        Arguments:

        - ``alarm_id`` -- The unique identifier of the alarm to check.

        If the alarm has not been set, :const:`None` will be returned.

        """
        if alarm_id in self._alarms:
            return self._alarms[alarm_id]
        else:
            return None

    def project_dot(self, x, y, color):
        """Project a single-pixel dot onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the dot.
        - ``y`` -- The vertical location relative to the window to
          project the dot.

        See the documentation for :meth:`sge.Sprite.draw_dot` for more
        information.

        """
        sprite = self._get_dot_sprite(color)
        self.project_sprite(sprite, 0, x, y)

    def project_line(self, x1, y1, x2, y2, color, thickness=1,
                     anti_alias=False):
        """Project a line segment onto the game window.

        Arguments:

        - ``x1`` -- The horizontal location relative to the window of
          the first endpoint of the projected line segment.
        - ``y1`` -- The vertical location relative to the window of the
          first endpoint of the projected line segment.
        - ``x2`` -- The horizontal location relative to the window of
          the second endpoint of the projected line segment.
        - ``y2`` -- The vertical location relative to the window of the
          second endpoint of the projected line segment.

        See the documentation for :meth:`sge.Sprite.draw_line` for more
        information.

        """
        thickness = abs(thickness)
        x = min(x1, x2) - thickness // 2
        y = min(y1, y2) - thickness // 2
        x1 -= x
        y1 -= y
        x2 -= x
        y2 -= y

        sprite = self._get_line_sprite(x1, y1, x2, y2, color, thickness,
                                       anti_alias)
        self.project_sprite(sprite, 0, x, y)

    def project_rectangle(self, x, y, width, height, fill=None, outline=None,
                          outline_thickness=1):
        """Project a rectangle onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the rectangle.
        - ``y`` -- The vertical location relative to the window to
          project the rectangle.

        See the documentation for :meth:`sge.Sprite.draw_rectangle` for
        more information.

        """
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = self._get_rectangle_sprite(width, height, fill, outline,
                                            outline_thickness)
        self.project_sprite(sprite, 0, x, y)

    def project_ellipse(self, x, y, width, height, fill=None, outline=None,
                        outline_thickness=1, anti_alias=False):
        """Project an ellipse onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          position the imaginary rectangle containing the ellipse.
        - ``y`` -- The vertical location relative to the window to
          position the imaginary rectangle containing the ellipse.
        - ``width`` -- The width of the ellipse.
        - ``height`` -- The height of the ellipse.
        - ``fill`` -- The color of the fill of the ellipse.
        - ``outline`` -- The color of the outline of the ellipse.
        - ``outline_thickness`` -- The thickness of the outline of the
          ellipse.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.

        See the documentation for :meth:`sge.Sprite.draw_ellipse` for
        more information.

        """
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = self._get_ellipse_sprite(width, height, fill, outline,
                                          outline_thickness, anti_alias)
        self.project_sprite(sprite, 0, x, y)

    def project_circle(self, x, y, radius, fill=None, outline=None,
                       outline_thickness=1, anti_alias=False):
        """Project a circle onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          position the center of the circle.
        - ``y`` -- The vertical location relative to the window to
          position the center of the circle.

        See the documentation for :meth:`sge.Sprite.draw_circle` for
        more information.

        """
        sprite = self._get_circle_sprite(radius, fill, outline,
                                         outline_thickness, anti_alias)
        self.project_sprite(sprite, 0, x - radius, y - radius)

    def project_sprite(self, sprite, image, x, y, blend_mode=None):
        """Project a sprite onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project ``sprite``.
        - ``y`` -- The vertical location relative to the window to
          project ``sprite``.

        See the documentation for :meth:`sge.Sprite.draw_sprite` for
        more information.

        """
        if not isinstance(sprite, sge.Sprite):
            sprite = self.sprites[sprite]

        img = sprite._get_image(image)
        x -= sprite.origin_x
        y -= sprite.origin_y
        self._window_projections.append((img, x, y, blend_mode))

    def project_text(self, font, text, x, y, width=None, height=None,
                    color="black", halign=sge.ALIGN_LEFT, valign=sge.ALIGN_TOP,
                    anti_alias=True):
        """Project text onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the text.
        - ``y`` -- The vertical location relative to the window to
          project the text.

        See the documentation for :meth:`sge.Sprite.draw_text` for more
        information.

        """
        sprite = self._get_text_sprite(font, text, width, height, color,
                                       halign, valign, anti_alias)
        self.project_sprite(sprite, 0, x, y)

    def event_game_start(self):
        """Game start event.

        Called when the game starts.  This is only called once (it is
        not called again when the game restarts) and it is always the
        very first event method called.

        """
        pass

    def event_game_end(self):
        """Game end event.

        Called when the game ends.  This is only called once and it is
        always the very last event method called.

        """
        pass

    def event_step(self, time_passed, delta_mult):
        """Global step event.

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
        """Alarm event.

        Called when the value of an alarm reaches 0.

        Arguments:

        - ``alarm_id`` -- The unique identifier of the alarm which was
          set off.

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

        See the documentation for :class:`sge.input.JoystickHatMove`
        for more information.

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

    def event_gain_keyboard_focus(self):
        """Gain keyboard focus event.

        See the documentation for :class:`sge.input.KeyboardFocusGain`
        for more information.

        """
        pass

    def event_lose_keyboard_focus(self):
        """Lose keyboard focus event.

        See the documentation for :class:`sge.input.KeyboardFocusLose`
        for more information.

        """
        if sge.DEBUG:
            bad_name = "event_loose_keyboard_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

    def event_gain_mouse_focus(self):
        """Gain mouse focus event.

        See the documentation for :class:`sge.input.MouseFocusGain` for
        more information.

        """
        pass

    def event_lose_mouse_focus(self):
        """Lose mouse focus event.

        See the documentation for :class:`sge.input.MouseFocusLose` for
        more information.

        """
        if sge.DEBUG:
            bad_name = "event_loose_mouse_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

    def event_close(self):
        """Close event.

        This is always called after any :meth:`sge.Room.event_close`
        occurring at the same time.

        See the documentation for :class:`sge.input.QuitRequest` for
        more information.

        """
        pass

    def event_mouse_collision(self, other):
        """Default mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision`.  See the
        documentation for :meth:`sge.StellarClass.event_collision` for
        more information.

        """
        pass

    def event_mouse_collision_left(self, other):
        """Left mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision_left`.  See the
        documentation for :meth:`sge.StellarClass.event_collision_left`
        for more information.

        """
        self.event_mouse_collision(other)

    def event_mouse_collision_right(self, other):
        """Right mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision_right`.  See the
        documentation for :meth:`sge.StellarClass.event_collision_right`
        for more information.

        """
        self.event_mouse_collision(other)

    def event_mouse_collision_top(self, other):
        """Top mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision_top`.  See the
        documentation for :meth:`sge.StellarClass.event_collision_top`
        for more information.

        """
        self.event_mouse_collision(other)

    def event_mouse_collision_bottom(self, other):
        """Bottom mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision_bottom`.  See
        the documentation for
        :meth:`sge.StellarClass.event_collision_bottom` for more
        information.

        """
        self.event_mouse_collision(other)

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

    def event_paused_gain_keyboard_focus(self):
        """Gain keyboard focus event when paused.

        See the documentation for :class:`sge.input.KeyboardFocusGain`
        for more information.

        """
        pass

    def event_paused_lose_keyboard_focus(self):
        """Lose keyboard focus event when paused.

        See the documentation for :class:`sge.input.KeyboardFocusLose`
        for more information.

        """
        if sge.DEBUG:
            bad_name = "event_paused_loose_keyboard_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

    def event_paused_gain_mouse_focus(self):
        """Gain mouse focus event when paused.

        See the documentation for :class:`sge.input.MouseFocusGain` for
        more information.

        """
        pass

    def event_paused_lose_mouse_focus(self):
        """Lose mouse focus event when paused.

        See the documentation for :class:`sge.input.MouseFocusLose` for
        more information.

        """
        if sge.DEBUG:
            bad_name = "event_paused_loose_mouse_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

    def event_paused_close(self):
        """Close event when paused.

        See the documentation for :meth:`sge.Game.event_close` for more
        information.

        """
        pass

    def _set_mode(self):
        # Set the mode of the screen based on self.width, self.height,
        # and self.fullscreen.
        info = pygame.display.Info()

        if self.scale:
            self._xscale = self.scale
            self._yscale = self.scale

        if self.fullscreen or not info.wm:
            flags = pygame.FULLSCREEN
            if sge.hardware_rendering:
                flags |= pygame.HWSURFACE | pygame.DOUBLEBUF

            modes = pygame.display.list_modes()
            if modes != -1 and modes:
                self._window_width, self._window_height = modes[0]
            else:
                w = "Couldn't find out the maximum resolution! Assuming 640x480."
                warnings.warn(w)
                self._window_width = 640
                self._window_height = 480

            self._background_changed = True
            self._window = pygame.display.set_mode(
                (self._window_width, self._window_height), flags)

            if not self.scale:
                ##self._xscale = info.current_w / self.width
                ##self._yscale = info.current_h / self.height
                self._xscale = self._window_width / self.width
                self._yscale = self._window_height / self.height

                if self.scale_proportional:
                    self._xscale = min(self._xscale, self._yscale)
                    self._yscale = self._xscale

            w = max(1, self._window.get_width())
            h = max(1, self._window.get_height())
            self._x = int(round((w - self.width * self._xscale) / 2))
            self._y = int(round((h - self.height * self._yscale) / 2))
        else:
            self._x = 0
            self._y = 0
            flags = 0

            # Decide window size
            if self.scale:
                self._window_width = self.width * self.scale
                self._window_height = self.height * self.scale
            else:
                self._xscale = self._window_width / self.width
                self._yscale = self._window_height / self.height

                if self.scale_proportional:
                    self._xscale = min(self._xscale, self._yscale)
                    self._yscale = self._xscale

                flags |= pygame.RESIZABLE

            if sge.hardware_rendering:
                flags |= pygame.HWSURFACE | pygame.DOUBLEBUF

            self._window = pygame.display.set_mode(
                (self._window_width, self._window_height), flags)

            w = max(1, self._window.get_width())
            h = max(1, self._window.get_height())
            self._x = int(round((w - self.width * self._xscale) / 2))
            self._y = int(round((h - self.height * self._yscale) / 2))

        self._display_surface = self._window.copy()
        self._background_changed = True

    def _get_dot_sprite(self, color):
        # Return a sprite for the given dot.
        i = (color,)
        if i in self._dot_cache:
            sprite = self._dot_cache[i]
        else:
            sprite = sge.Sprite(None, width=1, height=1)
            sprite.draw_dot(0, 0, color)
            self._dot_cache[i] = sprite
            sprite.destroy()

        return sprite

    def _get_line_sprite(self, x1, y1, x2, y2, color, thickness, anti_alias):
        # Return a sprite for the given line.
        w = int(round(abs(x2 - x1) + thickness))
        h = int(round(abs(y2 - y1) + thickness))
        i = (x1, y1, x2, y2, color, thickness, anti_alias)
        if i in self._line_cache:
            sprite = self._line_cache[i]
        else:
            sprite = sge.Sprite(None, width=w, height=h)
            sprite.draw_line(x1, y1, x2, y2, color, thickness, anti_alias)
            self._line_cache[i] = sprite
            sprite.destroy()

        return sprite

    def _get_rectangle_sprite(self, width, height, fill, outline,
                              outline_thickness):
        # Return a sprite for the given rectangle.
        i = (width, height, fill, outline, outline_thickness)
        if i in self._rectangle_cache:
            sprite = self._rectangle_cache[i]
        else:
            outline_thickness = abs(outline_thickness)
            draw_x = outline_thickness // 2
            draw_y = outline_thickness // 2
            w = width + outline_thickness
            h = height + outline_thickness
            sprite = sge.Sprite(None, width=w, height=h)
            sprite.draw_rectangle(draw_x, draw_y, width, height, fill, outline,
                                  outline_thickness)
            self._rectangle_cache[i] = sprite
            sprite.destroy()

        return sprite

    def _get_ellipse_sprite(self, width, height, fill, outline,
                            outline_thickness, anti_alias):
        # Return a sprite for the given ellipse.
        i = (width, height, fill, outline, outline_thickness, anti_alias)
        if i in self._ellipse_cache:
            sprite = self._ellipse_cache[i]
        else:
            outline_thickness = abs(outline_thickness)
            draw_x = outline_thickness // 2
            draw_y = outline_thickness // 2
            w = width + outline_thickness
            h = height + outline_thickness
            sprite = sge.Sprite(None, width=w, height=h)
            sprite.draw_ellipse(draw_x, draw_y, width, height, fill, outline,
                                outline_thickness)
            self._ellipse_cache[i] = sprite
            sprite.destroy()

        return sprite

    def _get_circle_sprite(self, radius, fill, outline, outline_thickness,
                           anti_alias):
        # Return a sprite for the given circle.
        i = (radius, fill, outline, outline_thickness, anti_alias)
        if i in self._circle_cache:
            sprite = self._circle_cache[i]
        else:
            outline_thickness = abs(outline_thickness)
            xy = radius + outline_thickness // 2
            wh = 2 * radius + outline_thickness
            sprite = sge.Sprite(None, width=wh, height=wh)
            sprite.draw_circle(xy, xy, radius, fill, outline, outline_thickness,
                               anti_alias)
            self._circle_cache[i] = sprite
            sprite.destroy()

        return sprite

    def _get_text_sprite(self, font, text, width, height, color, halign,
                         valign, anti_alias):
        # Return a sprite for the given text.
        i = (font, text, width, height, color, halign, valign, anti_alias)
        if i in sge.game._text_cache:
            sprite = sge.game._text_cache[i]
        else:
            if not isinstance(font, sge.Font):
                font = sge.game.fonts[font]

            w = font.get_width(text, width, height)
            h = font.get_height(text, width, height)
            draw_x = {sge.ALIGN_LEFT: 0, sge.ALIGN_CENTER: w / 2,
                      sge.ALIGN_RIGHT: w}.setdefault(halign, w / 2)
            draw_y = {sge.ALIGN_TOP: 0, sge.ALIGN_MIDDLE: h / 2,
                      sge.ALIGN_BOTTOM: h}.setdefault(valign, h / 2)
            sprite = sge.Sprite(None, width=w, height=h)
            sprite.draw_text(font, text, draw_x, draw_y, width, height, color,
                             halign, valign, anti_alias)
            sge.game._text_cache[i] = sprite
            sprite.destroy()

        return sprite

    def _show_projections(self):
        # Show the window projections and return the area rects list.
        rects = []
        for projection in self._window_projections:
            (image, x, y, blend_mode) = projection
            rect = image.get_rect(left=(self._x + x * self._xscale),
                                  top=(self._y + y * self._yscale))
            self._window.blit(image, rect)
            rects.append(rect)

        self._window_projections = []
        return rects

    def _get_channel(self):
        # Return a channel for a sound effect to use.
        assert pygame.mixer.get_init()

        if not self._available_channels:
            self._add_channels()

        return self._available_channels.pop(0)

    def _release_channel(self, channel):
        # Release the given channel for other sounds to use.
        assert pygame.mixer.get_init()
        self._available_channels.append(channel)

    def _add_channels(self):
        # Add four channels for playing sounds.
        assert pygame.mixer.get_init()

        old_num_channels = pygame.mixer.get_num_channels()
        new_num_channels = old_num_channels + 4
        pygame.mixer.set_num_channels(new_num_channels)

        for i in range(old_num_channels, new_num_channels):
            self._available_channels.append(pygame.mixer.Channel(i))

    def _handle_music(self):
        # Call each frame to control the music playback.
        if self._music is not None:
            if pygame.mixer.music.get_busy():
                time_played = pygame.mixer.music.get_pos()
                fade_time = self._music._fade_time
                timeout = self._music._timeout

                if fade_time:
                    real_volume = self._music.volume / 100
                    if time_played < fade_time:
                        volume = real_volume * time_played / fade_time
                        pygame.mixer.music.set_volume(volume)
                    else:
                        pygame.mixer.music.set_volume(real_volume)

                if timeout and time_played >= timeout:
                    self._music.stop()
