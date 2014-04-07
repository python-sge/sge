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
                    pygame.display.set_icon(image)
                    break
                except pygame.error:
                    continue

    def __init__(self, width=640, height=480, fullscreen=False, scale=0,
                 scale_proportional=True, scale_smooth=False, fps=60,
                 delta=False, delta_min=15, grab_input=False,
                 window_text=None, window_icon=None):
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
        self._joysticks = []
        self._js_names = {}
        self._js_ids = {}
        self._pygame_sprites = pygame.sprite.LayeredDirty()
        self._window_projections = []
        self.mouse = sge.Mouse()

        # Setup sound channels
        self._available_channels = []
        self._all_channels = []
        if pygame.mixer.get_init():
            for i in range(pygame.mixer.get_num_channels()):
                channel = pygame.mixer.Channel(i)
                channel.set_endevent(sge.SOUND_END_EVENT)
                self._available_channels.append(channel)
                self._all_channels.append(channel)

        # Setup joysticks
        if pygame.joystick.get_init():
            for i in range(pygame.joystick.get_count()):
                joy = pygame.joystick.Joystick(i)
                joy.init()
                n = joy.get_name()
                self._js_names[i] = n
                self._js_ids[n] = i
                self._joysticks.append(joy)

        if not pygame.font.get_init():
            global Font
            Font = _FakeFont

        self.window_icon = None

        self._object_start_x = {}
        self._object_start_y = {}
        self._object_start_z = {}
        self._object_start_sprite = {}
        self._object_start_visible = {}
        self._object_start_detects_collisions = {}
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

            for room in self.rooms:
                room._reset()

            for i in self.objects:
                obj = self.objects[i]
                if obj is not sge.game.mouse:
                    obj.x = self._object_start_x[obj.id]
                    obj.y = self._object_start_y[obj.id]

                obj.z = self._object_start_z[obj.id]
                obj.sprite = self._object_start_sprite[obj.id]
                obj.visible = self._object_start_visible[obj.id]
                obj.detects_collisions = self._object_start_detects_collisions[obj.id]
                obj.bbox_x = self._object_start_bbox_x[obj.id]
                obj.bbox_y = self._object_start_bbox_y[obj.id]
                obj.bbox_width = self._object_start_bbox_width[obj.id]
                obj.bbox_height = self._object_start_bbox_height[obj.id]
                obj.collision_ellipse = self._object_start_collision_ellipse[obj.id]
                obj.collision_precise = self._object_start_collision_precise[obj.id]

            self.rooms[0].start()
        else:
            if sge.DEBUG:
                print("Starting the game.")
            self._running = True
            self._background_changed = True
            self.event_game_start()

            # Store the initial state of objects
            for i in self.objects:
                obj = self.objects[i]
                self._object_start_x[obj.id] = obj.x
                self._object_start_y[obj.id] = obj.y
                self._object_start_z[obj.id] = obj.z
                self._object_start_sprite[obj.id] = obj.sprite
                self._object_start_visible[obj.id] = obj.visible
                self._object_start_detects_collisions[obj.id] = obj.detects_collisions
                self._object_start_bbox_x[obj.id] = obj.bbox_x
                self._object_start_bbox_y[obj.id] = obj.bbox_y
                self._object_start_bbox_width[obj.id] = obj.bbox_width
                self._object_start_bbox_height[obj.id] = obj.bbox_height
                self._object_start_collision_ellipse[obj.id] = obj.collision_ellipse
                self._object_start_collision_precise[obj.id] = obj.collision_precise

            self._display_surface = self._window.copy()

            self.rooms[0].start()
            background = None
            cleanup_rects = []
            numviews = 0
            _fps_time = 0
            self._clock.tick()

            while self._running:
                # Pygame events
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        k = sge.KEY_NAMES[event.key]
                        self.event_key_press(k, event.unicode)
                        self.current_room.event_key_press(k, event.unicode)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_key_press(k, event.unicode)
                            else:
                                obj.event_inactive_key_press(k, event.unicode)
                    elif event.type == pygame.KEYUP:
                        k = sge.KEY_NAMES[event.key]
                        self.event_key_release(k)
                        self.current_room.event_key_release(k)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_key_release(k)
                            else:
                                obj.event_inactive_key_release(k)
                    elif event.type == pygame.MOUSEMOTION:
                        mx, my = event.pos
                        self.mouse.mouse_x = mx - self._x
                        self.mouse.mouse_y = my - self._y
                        self.event_mouse_move(*event.rel)
                        self.current_room.event_mouse_move(*event.rel)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_mouse_move(*event.rel)
                            else:
                                obj.event_inactive_mouse_move(*event.rel)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        b = sge.MOUSE_BUTTON_NAMES[event.button]
                        self.event_mouse_button_press(b)
                        self.current_room.event_mouse_button_press(b)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_mouse_button_press(b)
                            else:
                                obj.event_inactive_mouse_button_press(b)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        b = sge.MOUSE_BUTTON_NAMES[event.button]
                        self.event_mouse_button_release(b)
                        self.current_room.event_mouse_button_release(b)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_mouse_button_release(b)
                            else:
                                obj.event_inactive_mouse_button_release(b)
                    elif event.type == pygame.JOYAXISMOTION:
                        jsname = self._js_names[event.joy]
                        self.event_joystick_axis_move(jsname, event.joy,
                                                      event.axis, event.value)
                        self.current_room.event_joystick_axis_move(
                            jsname, event.joy, event.axis, event.value)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_axis_move(
                                    jsname, event.joy, event.axis, event.value)
                            else:
                                obj.event_inactive_joystick_axis_move(
                                    jsname, event.joy, event.axis, event.value)
                    elif event.type == pygame.JOYHATMOTION:
                        jsname = self._js_names[event.joy]
                        self.event_joystick_hat_move(jsname, event.joy,
                                                     event.hat, *event.value)
                        self.current_room.event_joystick_hat_move(
                            jsname, event.joy, event.hat, *event.value)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_hat_move(
                                    jsname, event.joy, event.hat, *event.value)
                            else:
                                obj.event_inactive_joystick_hat_move(
                                    jsname, event.joy, event.hat, *event.value)
                    elif event.type == pygame.JOYBALLMOTION:
                        jsname = self._js_names[event.joy]
                        self.event_joystick_trackball_move(
                            jsname, event.joy, event.ball, *event.rel)
                        self.current_room.event_joystick_trackball_move(
                            jsname, event.joy, event.ball, *event.rel)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_trackball_move(
                                    jsname, event.joy, event.ball, *event.rel)
                            else:
                                obj.event_inactive_joystick_trackball_move(
                                    jsname, event.joy, event.ball, *event.rel)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        jsname = self._js_names[event.joy]
                        self.event_joystick_button_press(jsname, event.joy,
                                                         event.button)
                        self.current_room.event_joystick_button_press(
                            jsname, event.joy, event.button)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_button_press(
                                    jsname, event.joy, event.button)
                            else:
                                obj.event_inactive_joystick_button_press(
                                    jsname, event.joy, event.button)
                    elif event.type == pygame.JOYBUTTONUP:
                        jsname = self._js_names[event.joy]
                        self.event_joystick_button_release(jsname, event.joy,
                                                           event.button)
                        self.current_room.event_joystick_button_release(
                            jsname, event.joy, event.button)
                        for obj in self.current_room.objects:
                            if obj.active:
                                obj.event_joystick_button_release(
                                    jsname, event.joy, event.button)
                            else:
                                obj.event_inactive_joystick_button_release(
                                    jsname, event.joy, event.button)
                    elif event.type == pygame.ACTIVEEVENT:
                        if event.gain:
                            if 2 & event.state:
                                # Gain keyboard focus
                                if sge.DEBUG:
                                    print('Gained keyboard focus.')
                                self.event_gain_keyboard_focus()
                                self.current_room.event_gain_keyboard_focus()
                            if 1 & event.state:
                                # Gain mouse focus
                                if sge.DEBUG:
                                    print('Gained mouse focus.')
                                self.event_gain_mouse_focus()
                                self.current_room.event_gain_mouse_focus()
                        else:
                            if 2 & event.state:
                                # Lose keyboard focus
                                if sge.DEBUG:
                                    print('Lost keyboard focus.')
                                self.event_lose_keyboard_focus()
                                self.current_room.event_lose_keyboard_focus()
                            if 1 & event.state:
                                # Lose mouse focus
                                if sge.DEBUG:
                                    print('Lost mouse focus.')
                                self.event_lose_mouse_focus()
                                self.current_room.event_lose_mouse_focus()
                    elif event.type == pygame.QUIT:
                        if sge.DEBUG:
                            print('Quit requested by the system.')
                        self.current_room.event_close()
                        self.event_close()
                    elif event.type == pygame.VIDEORESIZE:
                        if sge.DEBUG:
                            print('Video resize detected.')
                        self._window.blit(self._display_surface, (0, 0))
                        self._window_width = event.w
                        self._window_height = event.h
                        self._set_mode()
                    elif event.type == sge.SOUND_END_EVENT:
                        for i in self.sounds:
                            for channel in (self.sounds[i]._channels +
                                            self.sounds[i]._temp_channels):
                                if channel is self._all_channels[event.code]:
                                    self.sounds[i].playing -= 1
                                    if self.sounds[i].playing < 0:
                                        self.sounds[i].playing = 0
                                        if sge.DEBUG:
                                            print("Hey, I'm playing less than none?!")

                real_time_passed = self._clock.tick(self.fps)

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

                # Step events
                self.event_step(real_time_passed)
                self.current_room.event_step(real_time_passed)

                # Update background layers
                for i in self.background_layers:
                    self.background_layers[i]._update(time_passed)

                # Update objects (including mouse)
                for obj in self.current_room.objects:
                    if obj.active:
                        obj.event_begin_step(real_time_passed)
                        obj._update(time_passed, delta_mult)
                        obj.event_step(real_time_passed)
                    else:
                        obj.event_inactive_step(real_time_passed)

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
                        obj.event_end_step(real_time_passed)
                    else:
                        obj.event_inactive_end_step(real_time_passed)

                # Music control
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
                            
                    elif self._music_queue:
                        music = self._music_queue.pop(0)
                        music[0].play(*music[1:])

                if numviews != len(self.current_room.views):
                    numviews = len(self.current_room.views)
                    self._background_changed = True

                # Set xprevious and yprevious
                for obj in self.current_room.objects:
                    obj.xprevious = obj.x
                    obj.yprevious = obj.y

                # Redraw
                if self._background_changed or background is None:
                    w = max(1, self._display_surface.get_width())
                    h = max(1, self._display_surface.get_height())
                    background = pygame.Surface((w, h))
                    b = self.current_room.background._get_background()
                    background.blit(b, (self._x, self._y))
                    self._display_surface.blit(background, (0, 0))
                    self._background_changed = False
                    self._pygame_sprites.clear(self._display_surface,
                                               background)
                    for sprite in self._pygame_sprites:
                        sprite.rect = pygame.Rect(0, 0, 1, 1)
                        sprite.image = pygame.Surface((1, 1))
                        sprite.image.set_colorkey((0, 0, 0))
                    self._pygame_sprites.update()
                    self._pygame_sprites.draw(self._display_surface)
                    dirty = [self._display_surface.get_rect()]
                else:
                    self._pygame_sprites.clear(self._display_surface,
                                               background)
                    self._pygame_sprites.update()
                    dirty = self._pygame_sprites.draw(self._display_surface)

                self._window.blit(self._display_surface, (0, 0))

                # Window projections
                self.mouse.project_cursor()
                dirty.extend(cleanup_rects)
                cleanup_rects = self._show_projections()
                dirty.extend(cleanup_rects)

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
        if sprite is not None:
            image = sprite._get_image(0)
        else:
            try:
                image = pygame.image.load(
                    os.path.join(os.path.dirname(__file__),
                                 'sge_pause.png')).convert_alpha()
            except pygame.error:
                image = pygame.Surface((16, 16))
                image.fill((255, 255, 255), pygame.Rect(0, 0, 4, 16))
                image.fill((255, 255, 255), pygame.Rect(12, 0, 4, 16))
                image.set_colorkey((0, 0, 0))

        rect = image.get_rect(center=self._window.get_rect().center)

        self._paused = True
        screenshot = self._window.copy()
        background = screenshot.copy()
        dimmer = pygame.Surface(self._window.get_size(), pygame.SRCALPHA)
        dimmer.fill(pygame.Color(0, 0, 0, 128))
        background.blit(dimmer, (0, 0))
        background.blit(image, rect)
        orig_screenshot = screenshot
        orig_background = background
        self._clock.tick()

        while self._paused and self._running:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    k = sge.KEY_NAMES[event.key]
                    self.event_paused_key_press(k, event.unicode)
                    self.current_room.event_paused_key_press(k, event.unicode)
                    for obj in self.current_room.objects:
                        obj.event_paused_key_press(k, event.unicode)
                elif event.type == pygame.KEYUP:
                    k = sge.KEY_NAMES[event.key]
                    self.event_paused_key_release(k)
                    self.current_room.event_paused_key_release(k)
                    for obj in self.current_room.objects:
                        obj.event_paused_key_release(k)
                elif event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    self.mouse.mouse_x = mx - self._x
                    self.mouse.mouse_y = my - self._y
                    self.event_paused_mouse_move(*event.rel)
                    self.current_room.event_paused_mouse_move(*event.rel)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_move(*event.rel)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    b = sge.MOUSE_BUTTON_NAMES[event.button]
                    self.event_paused_mouse_button_press(b)
                    self.current_room.event_paused_mouse_button_press(b)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_button_press(b)
                elif event.type == pygame.MOUSEBUTTONUP:
                    b = sge.MOUSE_BUTTON_NAMES[event.button]
                    self.event_paused_mouse_button_release(b)
                    self.current_room.event_paused_mouse_button_release(b)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_button_release(b)
                elif event.type == pygame.JOYAXISMOTION:
                    jsname = self._js_names[event.joy]
                    self.event_paused_joystick_axis_move(
                        jsname, event.joy, event.axis, event.value)
                    self.current_room.event_paused_joystick_axis_move(
                        jsname, event.joy, event.axis, event.value)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_axis_move(
                            jsname, event.joy, event.axis, event.value)
                elif event.type == pygame.JOYHATMOTION:
                    jsname = self._js_names[event.joy]
                    self.event_paused_joystick_hat_move(
                        jsname, event.joy, event.hat, *event.value)
                    self.current_room.event_paused_joystick_hat_move(
                        jsname, event.joy, event.hat, *event.value)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_hat_move(
                            jsname, event.joy, event.hat, *event.value)
                elif event.type == pygame.JOYBALLMOTION:
                    jsname = self._js_names[event.joy]
                    self.event_paused_joystick_trackball_move(
                        jsname, event.joy, event.ball, *event.rel)
                    self.current_room.event_paused_joystick_trackball_move(
                        jsname, event.joy, event.ball, *event.rel)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_trackball_move(
                            jsname, event.joy, event.ball, *event.rel)
                elif event.type == pygame.JOYBUTTONDOWN:
                    jsname = self._js_names[event.joy]
                    self.event_paused_joystick_button_press(
                        jsname, event.joy, event.button)
                    self.current_room.event_paused_joystick_button_press(
                        jsname, event.joy, event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_button_press(
                            jsname, event.joy, event.button)
                elif event.type == pygame.JOYBUTTONUP:
                    jsname = self._js_names[event.joy]
                    self.event_paused_joystick_button_release(
                        jsname, event.joy, event.button)
                    self.current_room.event_paused_joystick_button_release(
                        jsname, event.joy, event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_button_release(
                            jsname, event.joy, event.button)
                elif event.type == pygame.ACTIVEEVENT:
                    if event.gain:
                        if 2 & event.state:
                            # Gain keyboard focus
                            if sge.DEBUG:
                                print('Gained keyboard focus.')
                            self.event_paused_gain_keyboard_focus()
                            self.current_room.event_paused_gain_keyboard_focus()
                        if 1 & event.state:
                            # Gain mouse focus
                            if sge.DEBUG:
                                print('Gained mouse focus.')
                            self.event_paused_gain_mouse_focus()
                            self.current_room.event_paused_gain_mouse_focus()
                    else:
                        if 2 & event.state:
                            # Lose keyboard focus
                            if sge.DEBUG:
                                print('Lost keyboard focus.')
                            self.event_paused_lose_keyboard_focus()
                            self.current_room.event_paused_lose_keyboard_focus()
                        if 1 & event.state:
                            # Lose mouse focus
                            if sge.DEBUG:
                                print('Lost mouse focus.')
                            self.event_paused_lose_mouse_focus()
                            self.current_room.event_paused_lose_mouse_focus()
                elif event.type == pygame.QUIT:
                    if sge.DEBUG:
                        print('Quit requested by the system.')
                    self.current_room.event_paused_close()
                    self.event_paused_close()
                elif event.type == pygame.VIDEORESIZE:
                    if sge.DEBUG:
                        print('Video resize detected.')
                    self._window_width = event.w
                    self._window_height = event.h
                    self._set_mode()
                    screenshot = pygame.transform.scale(orig_screenshot,
                                                        (event.w, event.h))
                    background = pygame.transform.scale(orig_background,
                                                        (event.w, event.h))
                elif event.type == sge.SOUND_END_EVENT:
                    for i in self.sounds:
                        for channel in (self.sounds[i]._channels +
                                        self.sounds[i]._temp_channels):
                            if channel is self._all_channels[event.code]:
                                self.sounds[i].playing -= 1
                                if self.sounds[i].playing < 0:
                                    self.sounds[i].playing = 0
                                    if sge.DEBUG:
                                        print("Hey, I'm playing less than none?!")

            # Time management
            self._clock.tick(self.fps)
            
            # Redraw
            self._window.blit(background, (0, 0))

            self.mouse.project_cursor()
            self._show_projections()

            pygame.display.flip()

        # Restore the look of the screen from before it was paused
        self._window.blit(screenshot, (0, 0))
        pygame.display.update()
        self._background_changed = True

    def unpause(self):
        """Unpause the game."""
        self._paused = False

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
        img = sprite._get_image(image)
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

    def event_step(self, time_passed):
        """Global step event.

        Called once each frame.

        Arguments:

        - ``time_passed`` -- The number of milliseconds that have passed
          during the last frame.

        """
        pass

    def event_key_press(self, key, char):
        """Key press event.

        Called when a key on the keyboard is pressed.

        Arguments:

        - ``char`` -- The Unicode character associated with the key
          press, or an empty Unicode string if no Unicode character is
          associated with the key press.

        See the documentation for :func:`sge.get_key_pressed` for more
        information.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        Called when a key on the keyboard is released.

        See the documentation for :func:`sge.get_key_pressed` for more
        information.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        Called when the mouse moves.

        Arguments:

        - ``x`` -- The horizontal relative movement of the mouse.
        - ``y`` -- The vertical relative movement of the mouse.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        Called when a mouse button is pressed.

        See the documentation for :func:`sge.get_mouse_button_pressed`
        for more information.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        Called when a mouse button is released.

        See the documentation for :func:`sge.get_mouse_button_pressed`
        for more information.

        """
        pass

    def event_joystick_axis_move(self, name, ID, axis, value):
        """Joystick axis move event.

        Called when an axis on a joystick changes position.

        Arguments:

        - ``name`` -- The name of the joystick.
        - ``ID`` -- The number of the joystick, where ``0`` is the first
          joystick.
        - ``value`` -- The tilt of the axis as a float from ``-1`` to
          ``1``, where ``0`` is centered, ``-1`` is all the way to the
          left or up, and ``1`` is all the way to the right or down.

        See the documentation for :func:`sge.get_joystick_axis` for more
        information.

        """
        pass

    def event_joystick_hat_move(self, name, ID, hat, x, y):
        """Joystick HAT move event.

        Called when a HAT switch (also called the POV hat, POV switch,
        or d-pad) changes position.

        Arguments:

        - ``name`` -- The name of the joystick.
        - ``ID`` -- The number of the joystick, where ``0`` is the first
          joystick.
        - ``x`` -- The horizontal position of the HAT, where ``0`` is
          centered, ``-1`` is left, and ``1`` is right.
        - ``y`` -- The vertical position of the HAT, where ``0`` is
          centered, ``-1`` is up, and ``1`` is down.

        See the documentation for :func:`sge.get_joystick_hat` for more
        information.

        """
        pass

    def event_joystick_trackball_move(self, name, ID, ball, x, y):
        """Joystick trackball move event.

        Called when a trackball on a joystick moves.

        Arguments:

        - ``name`` -- The name of the joystick.
        - ``ID`` -- The number of the joystick, where ``0`` is the first
          joystick.
        - ``ball`` -- The number of the trackball, where ``0`` is the
          first trackball on the joystick.
        - ``x`` -- The horizontal relative movement of the trackball.
        - ``y`` -- The vertical relative movement of the trackball.

        """
        pass

    def event_joystick_button_press(self, name, ID, button):
        """Joystick button press event.

        Called when a joystick button is pressed.

        Arguments:

        - ``name`` -- The name of the joystick.
        - ``ID`` -- The number of the joystick, where ``0`` is the first
          joystick.

        See the documentation for
        :func:`sge.get_joystick_button_pressed` for more information.

        """
        pass

    def event_joystick_button_release(self, name, ID, button):
        """Joystick button release event.

        Called when a joystick button is released.

        Arguments:

        - ``name`` -- The name of the joystick.
        - ``ID`` -- The number of the joystick, where ``0`` is the first
          joystick.

        See the documentation for
        :func:`sge.get_joystick_button_pressed` for more information.

        """
        pass

    def event_gain_keyboard_focus(self):
        """Gain keyboard focus event.

        Called when the game gains keyboard focus.  Keyboard focus is
        normally needed for key press and release events to be received.

        .. note::

           On some window systems, such as the one used by Windows, no
           distinction is made between keyboard and mouse focus, but on
           some other window systems, such as the X Window System, a
           distinction is made: one window can have keyboard focus while
           another has mouse focus.  Be careful to observe the
           difference; failing to do so may result in annoying bugs,
           and you won't notice these bugs if you are testing on a
           window manager that doesn't recognize the difference.

        """
        pass

    def event_lose_keyboard_focus(self):
        """Lose keyboard focus event.

        Called when the game loses keyboard focus.  Keyboard focus is
        normally needed for key press and release events to be received.

        .. note::

           See the note in the documentation for
           :meth:`event_gain_keyboard_focus`.

        """
        if sge.DEBUG:
            bad_name = "event_loose_keyboard_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

    def event_gain_mouse_focus(self):
        """Gain mouse focus event.

        Called when the game gains mouse focus.  Mouse focus may be
        needed for mouse motion, button press, and button release events
        to be received.

        .. note::

           See the note in the documentation for
           :meth:`event_gain_keyboard_focus`.

        """
        pass

    def event_lose_mouse_focus(self):
        """Lose mouse focus event.

        Called when the game loses mouse focus.  Mouse focus may be
        needed for mouse motion, button press, and button release events
        to be received.

        .. note::

           See the note in the documentation for
           :meth:`event_gain_keyboard_focus`.

        """
        if sge.DEBUG:
            bad_name = "event_loose_mouse_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

    def event_close(self):
        """Close event.

        Called when the operating system tells the game to close, e.g.
        when the user presses the close button in the window frame.  It
        is always called after any :meth:`sge.Room.event_close`
        occurring at the same time.

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

        See the documentation for :meth:`sge.Game.event_key_press` for
        more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See the documentation for :meth:`sge.Game.event_key_release` for
        more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See the documentation for :meth:`sge.Game.event_mouse_move` for
        more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_press` for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_release` for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, name, ID, axis, value):
        """Joystick axis move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_axis_move` for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, name, ID, hat, x, y):
        """Joystick HAT move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_hat_move` for more information.

        """
        pass

    def event_paused_joystick_trackball_move(self, name, ID, ball, x, y):
        """Joystick trackball move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_trackball_move` for more
        information.

        """
        pass

    def event_paused_joystick_button_press(self, name, ID, button):
        """Joystick button press event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_press` for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, name, ID, button):
        """Joystick button release event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_release` for more
        information.

        """
        pass

    def event_paused_gain_keyboard_focus(self):
        """Gain keyboard focus event when paused.

        See the documentation for
        :meth:`sge.Game.event_gain_keyboard_focus` for more information.

        """
        pass

    def event_paused_lose_keyboard_focus(self):
        """Lose keyboard focus event when paused.

        See the documentation for
        :meth:`sge.Game.event_lose_keyboard_focus` for more information.

        """
        if sge.DEBUG:
            bad_name = "event_paused_loose_keyboard_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

    def event_paused_gain_mouse_focus(self):
        """Gain mouse focus event when paused.

        See the documentation for
        :meth:`sge.Game.event_gain_mouse_focus` for more information.

        """
        pass

    def event_paused_lose_mouse_focus(self):
        """Lose mouse focus event when paused.

        See the documentation for
        :meth:`sge.Game.event_lose_mouse_focus` for more information.

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
            # Decide window size
            if not self.scale:
                self._xscale = self._window_width / self.width
                self._yscale = self._window_height / self.height

                if self.scale_proportional:
                    self._xscale = min(self._xscale, self._yscale)
                    self._yscale = self._xscale

            flags = pygame.RESIZABLE
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
            x -= draw_x
            y -= draw_y
            w = width + outline_thickness
            h = height + outline_thickness
            sprite = sge.Sprite(None, width=w, height=h)
            sprite.draw_rectangle(draw_x, draw_y, w, h, fill, outline,
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
            x -= draw_x
            y -= draw_y
            w = width + outline_thickness
            h = height + outline_thickness
            sprite = sge.Sprite(None, width=w, height=h)
            sprite.draw_ellipse(draw_x, draw_y, w, h, fill, outline,
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

            w, h = font.get_size(text, width, height)
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
            new_channel = pygame.mixer.Channel(i)
            new_channel.set_endevent(sge.SOUND_END_EVENT)
            self._available_channels.append(new_channel)
            self._all_channels.append(new_channel)
