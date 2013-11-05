# The SGE Template
# Written in 2012, 2013 by Julian Marchant <onpon4@riseup.net> 
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
# Apache License 2.0.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


__all__ = ['Game']


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
       scaling algorith such as pixel doubling) should be used.

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

    def __init__(self, width=640, height=480, fullscreen=False, scale=None,
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

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        Called when an axis on a joystick changes position.

        Arguments:

        - ``value`` -- The tilt of the axis as a float from ``-1`` to
          ``1``, where ``0`` is centered, ``-1`` is all the way to the
          left or up, and ``1`` is all the way to the right or down.

        See the documentation for :func:`sge.get_joystick_axis` for more
        information.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        Called when a HAT switch (also called the POV hat, POV switch,
        or d-pad) changes position.

        Arguments:

        - ``x`` -- The horizontal position of the HAT, where ``0`` is
          centered, ``-1`` is left, and ``1`` is right.
        - ``y`` -- The vertical position of the HAT, where ``0`` is
          centered, ``-1`` is up, and ``1`` is down.

        See the documentation for :func:`sge.get_joystick_hat` for more
        information.

        """
        pass

    def event_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event.

        Called when a trackball on a joystick moves.

        Arguments:

        - ``joystick`` -- The number of the joystick, where ``0`` is the
          first joystick.
        - ``ball`` -- The number of the trackball, where ``0`` is the
          first trackball on the joystick.
        - ``x`` -- The horizontal relative movement of the trackball.
        - ``y`` -- The vertical relative movement of the trackball.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        Called when a joystick button is pressed.

        See the documentation for
        :func:`sge.get_joystick_button_pressed` for more information.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        Called when a joystick button is pressed.

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
        pass

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
        pass

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

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_axis_move` for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_hat_move` for more information.

        """
        pass

    def event_paused_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_trackball_move` for more
        information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_press` for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
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
        pass

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
        pass

    def event_paused_close(self):
        """Close event when paused.

        See the documentation for :meth:`sge.Game.event_close` for more
        information.

        """
        pass
