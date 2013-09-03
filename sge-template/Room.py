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


__all__ = ['Room']


class Room(object):

    """Class for rooms.

    This class stores the settings and objects found in a room.  Rooms
    are used to create separate parts of the game, such as levels and
    menu screens.

    Every game must have at least one room.

    .. attribute:: width

       The width of the room in pixels.  If set to :const:`None`,
       :attr:`sge.game.width` is used.

    .. attribute:: height

       The height of the room in pixels.  If set to :const:`None`,
       :attr:`sge.game.height` is used.

    .. attribute:: views

       A list containing all :class:`sge.View` objects in the room.

    .. attribute:: background

       The :class:`sge.Background` object used.

    .. attribute:: background_x

       The horizontal position of the background in the room.

    .. attribute:: background_y

       The vertical position of the background in the room.

    .. attribute:: objects

       A tuple containing all :class:`sge.StellarClass` objects in the
       room.  (Read-only)

    .. attribute:: room_number

       The index of this room in the game, where ``0`` is the first
       room, or :const:`None` if this room has not been added to a game.
       (Read-only)

    """

    def __init__(self, objects=(), width=None, height=None, views=None,
                 background=None, background_x=0, background_y=0):
        """Constructor method.

        Arguments:

        - ``views`` -- A list containing all :class:`sge.View` objects
          in the room.  If set to :const:`None`, a new view will be
          created with ``x=0``, ``y=0``, and all other arguments
          unspecified, which will become the first view of the room.
        - ``background`` -- The :class:`sge.Background` object used.  If
          set to :const:`None`, a new background will be created with no
          layers and the color set to ``"black"``.

        All other arguments set the respective initial attributes of the
        room.  See the documentation for :class:`Room` for more
        information.

        """
        # TODO

    def add(self, obj):
        """Add a StellarClass object to the room.

        Arguments:

        - ``obj`` -- The :class:`sge.StellarClass` object to add.

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
        method behaves in the same way that :meth:`Room.start` does.

        """
        # TODO

    def end(self, next_room=None, resume=True):
        """End the current room.

        Arguments:

        - ``next_room`` -- The room number of the room to go to next.
          If set to :const:`None`, the room after this one is chosen.
        - ``resume`` -- Whether or not to resume the next room instead
          of restarting it.

        If the room chosen as the next room does not exist, the game is
        ended.

        This triggers this room's :meth:`Room.event_room_end` and resets
        the state of this room.

        """
        # TODO

    def project_dot(self, x, y, z, color):
        """Project a single-pixel dot onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the dot.
        - ``y`` -- The vertical location relative to the room to project
          the dot.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_dot` for more
        information.

        """
        # TODO

    def project_line(self, x1, y1, x2, y2, z, color, thickness=1,
                     anti_alias=False):
        """Project a line segment onto the room.

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

        See the documentation for :meth:`sge.Sprite.draw_line` for more
        information.

        """
        # TODO

    def project_rectangle(self, x, y, z, width, height, fill=None,
                          outline=None, outline_thickness=1):
        """Project a rectangle onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the rectangle.
        - ``y`` -- The vertical location relative to the room to project
          the rectangle.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_rectangle` for
        more information.

        """
        # TODO

    def project_ellipse(self, x, y, z, width, height, fill=None,
                        outline=None, outline_thickness=1, anti_alias=False):
        """Project an ellipse onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          position the imaginary rectangle containing the ellipse.
        - ``y`` -- The vertical location relative to the room to
          position the imaginary rectangle containing the ellipse.
        - ``z`` -- The Z-axis position of the projection in the room.
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
        # TODO

    def project_circle(self, x, y, z, radius, fill=None, outline=None,
                       outline_thickness=1, anti_alias=False):
        """Project a circle onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          position the center of the circle.
        - ``y`` -- The vertical location relative to the room to
          position the center of the circle.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_circle` for
        more information.

        """
        # TODO

    def project_sprite(self, sprite, image, x, y, z):
        """Project a sprite onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project ``sprite``.
        - ``y`` -- The vertical location relative to the room to project
          ``sprite``.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_sprite` for
        more information.

        """
        # TODO

    def project_text(self, font, text, x, y, z, width=None, height=None,
                    color="black", halign=sge.ALIGN_LEFT, valign=sge.ALIGN_TOP,
                    anti_alias=True):
        """Project text onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the text.
        - ``y`` -- The vertical location relative to the room to project
          the text.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_text` for more
        information.

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

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        """
        pass

    def event_key_press(self, key, char):
        """Key press event.

        See the documentation for :meth:`sge.Game.event_key_press` for
        more information.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        See the documentation for :meth:`sge.Game.event_key_release` for
        more information.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        See the documentation for :meth:`sge.Game.event_mouse_move` for
        more information.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_press` for more information.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        See the documentation for
        :meth:`sge.Game.event_mouse_button_release` for more
        information.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        See the documentation for
        :meth:`sge.Game.event_joystick_axis_move` for more information.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        See the documentation for
        :meth:`sge.Game.event_joystick_hat_move` for more information.

        """
        pass

    def event_joystick_trackball_move(self, joystick, ball, x, y):
        """Joystick trackball move event.

        See the documentation for
        :meth:`sge.Game.event_joystick_trackball_move` for more
        information.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_press` for more
        information.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        See the documentation for
        :meth:`sge.Game.event_joystick_button_release` for more
        information.

        """
        pass

    def event_close(self):
        """Close event.

        See the documentation for :meth:`sge.Game.event_close` for more
        information.  This is always called before any game close events
        occurring at the same time.

        """
        pass

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

    def event_paused_close(self):
        """Close event when paused.

        See the documentation for :meth:`Room.event_close` for more
        information.

        """
        pass
