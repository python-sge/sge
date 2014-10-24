# The SGE Specification
# Written in 2012, 2013, 2014 by Julian Marchant <onpon4@riseup.net> 
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

import sge


class Game(object):

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
       If this is :const:`True` and :attr:`sge.mouse.visible` is
       :const:`False`, the mouse will be in relative mode.  Otherwise,
       the mouse will be in absolute mode.

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

       A dictionary containing all :class:`sge.Object` objects in
       the game, indexed by the objects' :attr:`sge.Object.id`
       attributes.  (Read-only)

    .. attribute:: rooms

       A list containing all rooms in order of their creation.
       (Read-only)

    .. attribute:: current_room

       The room which is currently active.  (Read-only)

    .. attribute:: mouse

       A :class:`sge.Object` object which represents the mouse
       cursor.  Its :attr:`sge.Object.id` attribute is ``"mouse"``
       and its bounding box is a one-pixel square.

       Some of this object's attributes control properties of the mouse.
       See the documentation for :mod:`sge.mouse` for more information.

    """

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
        # TODO

    def unpause(self):
        """Unpause the game."""
        # TODO

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
        # TODO

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
        # TODO

    def refresh(self):
        """Refresh the screen.

        This method needs to be called for changes to the screen to be
        seen by the user.  It should be called every frame.

        You normally don't need to use this function directly.  It is
        called automatically in each frame of the SGE's main loop.  You
        only need to use this function directly if you take control away
        from the SGE's main loop, e.g. to create your own loop.

        """
        # TODO

    def register_class(self, cls):
        """Register a class with the SGE.

        Registered classes can be used to index objects by, e.g. for
        :attr:`sge.Room.objects_by_class`.  A list of all currently
        registered classes can be found in :attr:`registered_classes`.

        """
        # TODO

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
        # TODO

    def get_alarm(self, alarm_id):
        """Return the value of an alarm.

        Arguments:

        - ``alarm_id`` -- The unique identifier of the alarm to check.

        If the alarm has not been set, :const:`None` will be returned.

        """
        # TODO

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
        # TODO

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
        # TODO

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
        # TODO

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
        - ``outline_thickness`` -- The thickness of the outline of the
          ellipse.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.

        See the documentation for :meth:`sge.Sprite.draw_ellipse` for
        more information.

        """
        # TODO

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
        # TODO

    def project_polygon(self, points, fill=None, outline=None,
                        outline_thickness=1, anti_alias=False):
        """Draw a polygon on the sprite.

        Arguments:

        - ``points`` -- A list of points relative to the room to
          position each of the polygon's angles.  Each point should be a
          tuple in the form ``(x, y)``, where x is the horizontal
          location and y is the vertical location.

        See the documentation for :meth:`sge.Sprite.draw_polygon` for
        more information.

        """
        # TODO

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
        # TODO

    def project_text(self, font, text, x, y, width=None, height=None,
                    color=sge.Color("black"), halign=sge.ALIGN_LEFT,
                    valign=sge.ALIGN_TOP, anti_alias=True):
        """Project text onto the game window.

        Arguments:

        - ``x`` -- The horizontal location relative to the window to
          project the text.
        - ``y`` -- The vertical location relative to the window to
          project the text.

        See the documentation for :meth:`sge.Sprite.draw_text` for more
        information.

        """
        # TODO

    def event_game_start(self):
        """Game start event.

        Called when the game starts.  This is only called once (it is
        not called again when the game restarts) and it is always the
        very first event method called.

        """
        pass

    def event_game_end(self):
        """Game end event.

        Called when the game ends.  It is only called once and it is
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
        pass

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
        pass

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
        documentation for :meth:`sge.Object.event_collision` for
        more information.

        """
        pass

    def event_mouse_collision_left(self, other):
        """Left mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision_left`.  See the
        documentation for :meth:`sge.Object.event_collision_left`
        for more information.

        """
        self.event_mouse_collision(other)

    def event_mouse_collision_right(self, other):
        """Right mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision_right`.  See the
        documentation for :meth:`sge.Object.event_collision_right`
        for more information.

        """
        self.event_mouse_collision(other)

    def event_mouse_collision_top(self, other):
        """Top mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision_top`.  See the
        documentation for :meth:`sge.Object.event_collision_top`
        for more information.

        """
        self.event_mouse_collision(other)

    def event_mouse_collision_bottom(self, other):
        """Bottom mouse collision event.

        Proxy for :meth:`sge.game.mouse.event_collision_bottom`.  See
        the documentation for
        :meth:`sge.Object.event_collision_bottom` for more
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
        pass

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
        pass

    def event_paused_close(self):
        """Close event when paused.

        See the documentation for :meth:`sge.Game.event_close` for more
        information.

        """
        pass
