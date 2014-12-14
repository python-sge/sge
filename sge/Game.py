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
       to :const:`None`, the SGE chooses the icon.

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

    def __init__(self, width=640, height=480, fullscreen=False, scale=None,
                 scale_proportional=True, scale_smooth=False, fps=60,
                 delta=False, delta_min=15, grab_input=False,
                 window_text=None, window_icon=None,
                 collision_events_enabled=True):
        """
        Arguments set the respective initial attributes of the game.
        See the documentation for :class:`sge.Game` for more
        information.

        The created :class:`sge.Game` object is automatically assigned
        to :data:`sge.game`.
        """
        # TODO

    def start(self):
        """
        Start the game at the first room.  Can be called in the middle
        of a game to start the game over.  If you do this, everything
        will be reset to its original state.
        """
        # TODO

    def end(self):
        """Properly end the game."""
        # TODO

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
        # TODO

    def unpause(self):
        """Unpause the game."""
        # TODO

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
        # TODO

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
        # TODO

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
        # TODO

    def project_dot(self, x, y, color):
        """
        Project a single-pixel dot onto the game window.

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

        See the documentation for :meth:`sge.Sprite.draw_line` for more
        information.
        """
        # TODO

    def project_rectangle(self, x, y, width, height, fill=None, outline=None,
                          outline_thickness=1):
        """
        Project a rectangle onto the game window.

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
        """
        Project an ellipse onto the game window.

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
        """
        Project a circle onto the game window.

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
        """
        Draw a polygon on the sprite.

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
        """
        Project a sprite onto the game window.

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
        """
        Project text onto the game window.

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
        """
        Called when the game starts.  This is only called once (it is
        not called again when the game restarts), and it is always the
        very first event method called.
        """
        pass

    def event_game_end(self):
        """
        Called when the game ends.  This is only called once, and it is
        always the very last event method called.
        """
        pass

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

        See the documentation for :meth:`sge.Game.alarms` for more
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

    def event_mouse_collision(self, other):
        """
        Proxy for :meth:`sge.game.mouse.event_collision`.  See the
        documentation for :meth:`sge.Object.event_collision` for
        more information.
        """
        pass

    def event_mouse_collision_left(self, other):
        """
        Proxy for :meth:`sge.game.mouse.event_collision_left`.  See the
        documentation for :meth:`sge.Object.event_collision_left`
        for more information.
        """
        self.event_mouse_collision(other)

    def event_mouse_collision_right(self, other):
        """
        Proxy for :meth:`sge.game.mouse.event_collision_right`.  See the
        documentation for :meth:`sge.Object.event_collision_right`
        for more information.
        """
        self.event_mouse_collision(other)

    def event_mouse_collision_top(self, other):
        """
        Proxy for :meth:`sge.game.mouse.event_collision_top`.  See the
        documentation for :meth:`sge.Object.event_collision_top`
        for more information.
        """
        self.event_mouse_collision(other)

    def event_mouse_collision_bottom(self, other):
        """
        Proxy for :meth:`sge.game.mouse.event_collision_bottom`.  See
        the documentation for
        :meth:`sge.Object.event_collision_bottom` for more
        information.
        """
        self.event_mouse_collision(other)

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
