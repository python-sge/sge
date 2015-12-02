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

import pygame
import six

import sge
from sge import r
from sge.r import (_get_dot_sprite, _get_line_sprite, _get_rectangle_sprite,
                   _get_ellipse_sprite, _get_circle_sprite,
                   _get_polygon_sprite, o_update_object_areas,
                   o_update_collision_lists, r_get_rectangle_object_areas,
                   r_set_object_areas, r_update_fade, r_update_dissolve,
                   r_update_pixelate, r_update_wipe_left, r_update_wipe_right,
                   r_update_wipe_up, r_update_wipe_down, r_update_wipe_upleft,
                   r_update_wipe_upright, r_update_wipe_downleft,
                   r_update_wipe_downright, r_update_wipe_matrix,
                   r_update_iris_in, r_update_iris_out, s_get_image)


__all__ = ['Room']


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

       A list containing all :class:`sge.View` objects in the room.

    .. attribute:: background

       The :class:`sge.Background` object used.

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
       :meth:`sge.Room.event_alarm` is executed with ``alarm_id`` set to
       the respective key, and the item is deleted from this dictionary.

    .. attribute:: objects

       A list containing all :class:`sge.Object` objects in the
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

       Each object area is a set containing :class:`sge.Object` objects
       whose sprites or bounding boxes reside within the object area.

       Object areas are only created within the room, i.e. the
       horizontal location of an object area will always be less than
       :attr:`width`, and the vertical location of an object area will
       always be less than :attr:`height`.  Depending on the size of
       collision areas and the size of the room, however, the last row
       and/or the last column of collision areas may partially reside
       outside of the room.

       .. note::

          It is generally easier to use :meth:`sge.Room.get_objects_at`
          than to access this list directly.

    .. attribute:: object_area_void

       A set containing :class:`sge.Object` objects whose sprites or
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

        - ``views`` -- A list containing all :class:`sge.View` objects
          in the room.  If set to :const:`None`, a new view will be
          created with ``x=0``, ``y=0``, and all other arguments
          unspecified, which will become the first view of the room.
        - ``background`` -- The :class:`sge.Background` object used.  If
          set to :const:`None`, a new background will be created with no
          layers and the color set to black.

        All other arguments set the respective initial attributes of the
        room.  See the documentation for :class:`sge.Room` for more
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
            self.views = [sge.View(0, 0)]

        if background is not None:
            self.background = background
        else:
            self.background = sge.Background((), sge.Color("black"))

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

        - ``obj`` -- The :class:`sge.Object` object to add.

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

        - ``obj`` -- The :class:`sge.Object` object to remove.

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
            self.rd["t_sprite"] = sge.Sprite.from_screenshot()
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
            

    def project_dot(self, x, y, z, color):
        """
        Project a single-pixel dot onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the dot.
        - ``y`` -- The vertical location relative to the room to project
          the dot.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_dot` for more
        information.
        """
        if not isinstance(color, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(color))
            raise TypeError(e)

        sprite = _get_dot_sprite(color)
        self.project_sprite(sprite, 0, x, y, z)

    def project_line(self, x1, y1, x2, y2, z, color, thickness=1,
                     anti_alias=False):
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

        See the documentation for :meth:`sge.Sprite.draw_line` for more
        information.
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

    def project_rectangle(self, x, y, z, width, height, fill=None,
                          outline=None, outline_thickness=1):
        """
        Project a rectangle onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the rectangle.
        - ``y`` -- The vertical location relative to the room to project
          the rectangle.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_rectangle` for
        more information.
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

    def project_ellipse(self, x, y, z, width, height, fill=None,
                        outline=None, outline_thickness=1, anti_alias=False):
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

        See the documentation for :meth:`sge.Sprite.draw_ellipse` for
        more information.
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

    def project_circle(self, x, y, z, radius, fill=None, outline=None,
                       outline_thickness=1, anti_alias=False):
        """
        Project a circle onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          position the center of the circle.
        - ``y`` -- The vertical location relative to the room to
          position the center of the circle.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_circle` for
        more information.
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

    def project_polygon(self, points, z, fill=None, outline=None,
                        outline_thickness=1, anti_alias=False):
        """
        Draw a polygon on the sprite.

        Arguments:

        - ``points`` -- A list of points relative to the room to
          position each of the polygon's angles.  Each point should be a
          tuple in the form ``(x, y)``, where x is the horizontal
          location and y is the vertical location.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_polygon` for
        more information.
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

    def project_sprite(self, sprite, image, x, y, z, blend_mode=None):
        """
        Project a sprite onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project ``sprite``.
        - ``y`` -- The vertical location relative to the room to project
          ``sprite``.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_sprite` for
        more information.
        """
        img = s_get_image(sprite, image)
        x -= sprite.origin_x
        y -= sprite.origin_y
        self.rd["projections"].append((img, x, y, z, blend_mode))

    def project_text(self, font, text, x, y, z, width=None, height=None,
                    color=sge.Color("black"), halign="left",
                    valign="top", anti_alias=True):
        """
        Project text onto the room.

        Arguments:

        - ``x`` -- The horizontal location relative to the room to
          project the text.
        - ``y`` -- The vertical location relative to the room to project
          the text.
        - ``z`` -- The Z-axis position of the projection in the room.

        See the documentation for :meth:`sge.Sprite.draw_text` for more
        information.
        """
        if not isinstance(color, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(color))
            raise TypeError(e)

        sprite = sge.Sprite.from_text(font, text, width, height, color, halign,
                                      valign, anti_alias)
        self.project_sprite(sprite, 0, x, y, z)

    def event_room_start(self):
        """
        Called when the room is started for the first time.  It is
        always called after any :meth:`sge.Game.event_game_start` and
        before any :class:`sge.Object.event_create` occurring at the
        same time.
        """
        pass

    def event_room_resume(self):
        """
        Called when the room is started after it has already previously
        been started.  It is always called before any
        :meth:`sge.Object.event_create` occurring at the same time.
        """
        pass

    def event_room_end(self):
        """
        Called when another room is started or the game ends while this
        room is the current room.  It is always called before any
        :meth:`sge.Game.event_game_end` occurring at the same time.
        """
        pass

    def event_step(self, time_passed, delta_mult):
        """
        See the documentation for :meth:`sge.Game.event_step` for more
        information.
        """
        pass

    def event_alarm(self, alarm_id):
        """
        See the documentation for :attr:`sge.Room.alarms` for more
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
        This is always called before any :meth:`sge.Game.event_close`
        occurring at the same time.

        See the documentation for :class:`sge.input.QuitRequest` for
        more information.
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
        See the documentation for :meth:`sge.Room.event_close` for more
        information.
        """
        pass
