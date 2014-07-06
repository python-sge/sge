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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pygame

import sge


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

       A list containing all :class:`sge.StellarClass` objects in the
       room.  (Read-only)

    .. attribute:: objects_by_class

       A dictionary of lists containing all :class:`sge.StellarClass`
       objects in the room, separated by class.  The dictionary keys are
       classes that have been registered with
       :meth:`sge.Game.register_class`, and the lists contain only
       those objects which are instances of the class indicated by the
       respective key.  (Read-only)

    .. attribute:: room_number

       The index of this room in the game, where ``0`` is the first
       room.  (Read-only)

    """

    def __init__(self, objects=(), width=None, height=None, views=None,
                 background=None, background_x=0, background_y=0,
                 room_number=None):
        """Constructor method.

        Arguments:

        - ``views`` -- A list containing all :class:`sge.View` objects
          in the room.  If set to :const:`None`, a new view will be
          created with ``x=0``, ``y=0``, and all other arguments
          unspecified, which will become the first view of the room.
        - ``background`` -- The :class:`sge.Background` object used.  If
          set to :const:`None`, a new background will be created with no
          layers and the color set to ``"black"``.
        - ``room_number`` -- The position in :data:`sge.game.rooms` to
          insert this room into.  If set to :const:`None`, it will be
          appended to the end of the list.

        All other arguments set the respective initial attributes of the
        room.  See the documentation for :class:`sge.Room` for more
        information.

        """
        self.width = width if width is not None else sge.game.width
        self.height = height if height is not None else sge.game.height
        self._start_width = self.width
        self._start_height = self.height
        self.background_x = background_x
        self.background_y = background_y
        self._destroyed = False
        self._new_objects = []

        self._alarms = {}

        if views is not None:
            self.views = list(views)
        else:
            self.views = [sge.View(0, 0)]
        self._start_views = []

        self._view_start_x = {}
        self._view_start_y = {}
        self._view_start_xport = {}
        self._view_start_yport = {}
        self._view_start_width = {}
        self._view_start_height = {}

        if background is not None:
            self.background = background
        else:
            self.background = sge.Background((), 'black')
        self._start_background = self.background

        rooms = sge.game.rooms[:]
        if room_number is None or room_number >= len(rooms):
            self.room_number = len(rooms)
            rooms.append(self)
        else:
            self.room_number = room_number
            rooms.insert(room_number, self)
        sge.game.rooms = rooms

        self._started = False
        self._has_started = False

        self.objects = []
        self.objects_by_class = {}
        for cls in sge.game.registered_classes:
            self.objects_by_class[cls] = []

        self.add(sge.game.mouse)
        for obj in objects:
            self.add(obj)
        self._start_objects = []

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

        if self.views:
            self._collision_area_size = max(int(self.views[0].width / 10),
                                            int(self.views[0].height / 10))
        else:
            self._collision_area_size = sge.COLLISION_AREA_SIZE_DEFAULT

        size = self._collision_area_size
        self._collision_areas = []
        for i in range(0, self.width, size):
            column = [[] for j in range(0, self.height, size)]
            self._collision_areas.append(column)

        # The "Void" is the area outside the room.  This area is
        # infinite, so everything in the Void is checked against
        # everything else in the Void (otherwise an infinite grid, which
        # is impossible, would be needed).
        self._collision_area_void = []

    def add(self, obj):
        """Add a StellarClass object to the room.

        Arguments:

        - ``obj`` -- The :class:`sge.StellarClass` object to add.

        """
        if not isinstance(obj, sge.StellarClass):
            obj = sge.game.objects[obj]

        if obj not in self.objects:
            objects = self.objects[:]
            objects.append(obj)
            self.objects = objects

            objects_by_class = self.objects_by_class.copy()
            for cls in objects_by_class:
                if isinstance(obj, cls):
                    objects = objects_by_class[cls][:]
                    objects.append(obj)
                    objects_by_class[cls] = objects
            self.objects_by_class = objects_by_class

            if self is sge.game.current_room:
                sge.game._pygame_sprites.add(obj._pygame_sprite, layer=obj.z)
                if self._started:
                    obj.event_create()
            else:
                self._new_objects.append(obj)

    def start(self):
        """Start the room.

        If the room has been changed, reset it to its original state.

        """
        if self._has_started:
            self._reset()

        self.resume()

    def resume(self):
        """Continue the room from where it left off.

        If the room is unchanged (e.g. has not been started yet), this
        method behaves in the same way that :meth:`sge.Room.start` does.

        """
        for sprite in sge.game._pygame_sprites:
            sprite.kill()

        self._limit_views()
        sge.game.current_room = self
        sge.game._background_changed = True

        for obj in self.objects:
            sge.game._pygame_sprites.add(obj._pygame_sprite, layer=obj.z)

        if not self._has_started:
            self._start_objects = self.objects[:]
            for obj in self.objects:
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

            self._start_views = self.views[:]
            for view in self.views:
                self._view_start_x[id(view)] = view.x
                self._view_start_y[id(view)] = view.y
                self._view_start_xport[id(view)] = view.xport
                self._view_start_yport[id(view)] = view.yport
                self._view_start_width[id(view)] = view.width
                self._view_start_height[id(view)] = view.height

        if not self._started:
            self.event_room_start()
            for obj in self.objects:
                obj.event_create()
        else:
            while self._new_objects:
                self._new_objects[0].event_create()
                del self._new_objects[0]
            self.event_room_resume()

        self._started = True
        self._has_started = True

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        After this method is called, ``value`` will reduce by 1 each
        frame (adjusted for delta timing if it is enabled) until it
        reaches 0, at which point :meth:`sge.Room.event_alarm` will be
        executed with ``alarm_id``.

        See the documentation for :meth:`sge.Game.set_alarm` for more
        information.

        """
        if value is not None:
            self._alarms[alarm_id] = value
        elif alarm_id in self._alarms:
            del self._alarms[alarm_id]

    def get_alarm(self, alarm_id):
        """Return the value of an alarm.

        See the documentation for :meth:`sge.Game.get_alarm` for more
        information.

        """
        if alarm_id in self._alarms:
            return self._alarms[alarm_id]
        else:
            return None

    def end(self, next_room=None, resume=True):
        """End the current room.

        Arguments:

        - ``next_room`` -- The room number of the room to go to next.
          If set to :const:`None`, the room after this one is chosen.
        - ``resume`` -- Whether or not to resume the next room instead
          of restarting it.

        If the room chosen as the next room does not exist, the game is
        ended.

        This triggers this room's :meth:`sge.Room.event_room_end` and
        resets the state of this room.

        """
        self.event_room_end()
        self._reset()

        if next_room is None:
            next_room = self.room_number + 1

        if (next_room >= -len(sge.game.rooms) and
                next_room < len(sge.game.rooms)):
            if resume:
                sge.game.rooms[next_room].resume()
            else:
                sge.game.rooms[next_room].start()
        else:
            sge.game.end()

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
        sprite = sge.game._get_dot_sprite(color)
        self.project_sprite(sprite, 0, x, y, z)

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
        thickness = abs(thickness)
        x = min(x1, x2) - thickness // 2
        y = min(y1, y2) - thickness // 2
        x1 -= x
        y1 -= y
        x2 -= x
        y2 -= y

        sprite = sge.game._get_line_sprite(x1, y1, x2, y2, color, thickness,
                                           anti_alias)
        self.project_sprite(sprite, 0, x, y, z)

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
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = sge.game._get_rectangle_sprite(width, height, fill, outline,
                                                outline_thickness)
        self.project_sprite(sprite, 0, x, y, z)

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
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        x -= draw_x
        y -= draw_y
        sprite = sge.game._get_ellipse_sprite(width, height, fill, outline,
                                              outline_thickness, anti_alias)
        self.project_sprite(sprite, 0, x, y, z)

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
        sprite = sge.game._get_circle_sprite(radius, fill, outline,
                                             outline_thickness, anti_alias)
        self.project_sprite(sprite, 0, x - radius, y - radius, z)

    def project_sprite(self, sprite, image, x, y, z, blend_mode=None):
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
        if blend_mode is not None and blend_mode & sge.BLEND_SCREEN:
            w = "Screen blend mode not supported. Normal blending used instead."
            warnings.warn(w)

        pygame_flags = {
            sge.BLEND_RGBA_ADD: pygame.BLEND_RGBA_ADD,
            sge.BLEND_RGBA_SUBTRACT: pygame.BLEND_RGBA_SUB,
            sge.BLEND_RGBA_MULTIPLY: pygame.BLEND_RGBA_MULT,
            sge.BLEND_RGBA_MINIMUM: pygame.BLEND_RGBA_MIN,
            sge.BLEND_RGBA_MAXIMUM: pygame.BLEND_RGBA_MAX,
            sge.BLEND_RGB_ADD: pygame.BLEND_RGB_ADD,
            sge.BLEND_RGB_SUBTRACT: pygame.BLEND_RGB_SUB,
            sge.BLEND_RGB_MULTIPLY: pygame.BLEND_RGB_MULT,
            sge.BLEND_RGB_MINIMUM: pygame.BLEND_RGB_MIN,
            sge.BLEND_RGB_MAXIMUM: pygame.BLEND_RGB_MAX
            }.setdefault(blend_mode, 0)

        p = sge._PygameProjectionSprite(x, y, z, sprite, image)
        p.blendmode = pygame_flags
        sge.game._pygame_sprites.add(p, layer=z)

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
        sprite = sge.game._get_text_sprite(font, text, width, height, color,
                                           halign, valign, anti_alias)
        self.project_sprite(sprite, 0, x, y, z)

    def move(self, room_number):
        """Move the room.

        Arguments:

        - ``room_number`` -- The new position in :data:`sge.game.rooms` to
          insert this room into.

        """
        rooms = sge.game.rooms[:]
        if not self._destroyed and len(rooms) < self.room_number:
            del rooms[self.room_number]
            self.room_number = room_number
            rooms.insert(room_number, self)
            sge.game.rooms = rooms

    def destroy(self):
        """Destroy the room.

        .. note::

           If the room is being used, it will not be completely
           destroyed until this use stops.

        """
        rooms = sge.game.rooms[:]
        if not self._destroyed and len(rooms) < self.room_number:
            self._destroyed = True
            del rooms[self.room_number]
            sge.game.rooms = rooms

    def event_room_start(self):
        """Room start event.

        Called when the room starts.  It is always called after any game
        start events and before any object create events occurring at
        the same time.

        """
        pass

    def event_room_resume(self):
        """Room resume event.

        Called when the room resumes without being reset to its original
        state (i.e. via :meth:`sge.Room.resume`).

        """
        pass

    def event_room_end(self):
        """Room end event.

        Called when the room ends.  It is always called before any game
        end events occurring at the same time.

        """
        pass

    def event_step(self, time_passed, delta_mult):
        """Room step event.

        See the documentation for :meth:`sge.Game.event_step` for more
        information.

        """
        pass

    def event_alarm(self, alarm_id):
        """Alarm event.

        See the documentation for :meth:`sge.Game.event_alarm` for more
        information.

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

        See the documentation for :class:`sge.input.JoystickHatMove` for
        more information.

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

        This is always called before any :meth:`sge.Game.event_close`
        occurring at the same time.

        See the documentation for :class:`sge.input.QuitRequest` for
        more information.

        """
        pass

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

        See the documentation for :meth:`sge.Room.event_close` for more
        information.

        """
        pass

    def _limit_views(self):
        # Prevent the views from moving outside of the room.
        for view in self.views:
            if view.x < 0:
                view._x = 0
            elif view.x + view.width > self.width:
                view._x = self.width - view.width

            if view.y < 0:
                view._y = 0
            elif view.y + view.height > self.height:
                view._y = self.height - view.height

    def _reset(self):
        # Reset the room to its original state.
        self._started = False
        self.width = self._start_width
        self.height = self._start_height
        self.views = self._start_views
        self.background = self._start_background
        self.objects = self._start_objects[:]

        for view in self.views:
            view._reset()
            view.x = self._view_start_x[id(view)]
            view.y = self._view_start_y[id(view)]
            view.xport = self._view_start_xport[id(view)]
            view.yport = self._view_start_yport[id(view)]
            view.width = self._view_start_width[id(view)]
            view.height = self._view_start_height[id(view)]

        for obj in self.objects:
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
