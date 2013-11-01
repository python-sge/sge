# Copyright (C) 2012, 2013 Julian Marchant <onpon4@riseup.net>
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
        self.width = width if width is not None else sge.game.width
        self.height = height if height is not None else sge.game.height
        self._start_width = self.width
        self._start_height = self.height
        self.background_x = background_x
        self.background_y = background_y

        if views is not None:
            self.views = list(views)
        else:
            self.views = [sge.View(0, 0)]
        self._start_views = self.views[:]

        if background is not None:
            self.background = background
        else:
            self.background = sge.Background((), 'black')
        self._start_background = self.background

        self.room_number = len(sge.game.rooms)
        sge.game.rooms.append(self)

        self._started = False

        self.objects = ()
        self.add(sge.game.mouse)
        for obj in objects:
            self.add(obj)
        self._start_objects = self.objects

    def add(self, obj):
        """Add a StellarClass object to the room.

        Arguments:

        - ``obj`` -- The :class:`sge.StellarClass` object to add.

        """
        if not isinstance(obj, sge.StellarClass):
            obj = sge.game.objects[obj]

        if obj not in self.objects:
            new_objects = list(self.objects)
            new_objects.append(obj)
            self.objects = tuple(new_objects)
            if self is sge.game.current_room:
                sge.game._pygame_sprites.add(obj._pygame_sprite, layer=obj.z)
                if self._started:
                    obj.event_create()

    def start(self):
        """Start the room.

        If the room has been changed, reset it to its original state.

        """
        self._reset()
        self.resume()

    def resume(self):
        """Continue the room from where it left off.

        If the room is unchanged (e.g. has not been started yet), this
        method behaves in the same way that :meth:`Room.start` does.

        """
        for sprite in sge.game._pygame_sprites:
            sprite.kill()

        self._limit_views()
        sge.game.current_room = self
        sge.game._background_changed = True

        for obj in self.objects:
            sge.game._pygame_sprites.add(obj._pygame_sprite, layer=obj.z)

        if not self._started:
            self.event_room_start()
            for obj in self.objects:
                obj.event_create()

        self._started = True

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
        sprite = sge.Sprite(None, width=1, height=1)
        sprite.draw_dot(0, 0, color)
        p = _Projection(x, y, z, sprite=sprite, detects_collisions=False)
        self.add(p)

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
        w = abs(x2 - x1) + thickness
        h = abs(y2 - y1) + thickness
        x1 -= x
        y1 -= y
        x2 -= x
        y2 -= y
        sprite = sge.Sprite(None, width=w, height=h)
        sprite.draw_line(x1, y1, x2, y2, color, thickness, anti_alias)
        p = _Projection(x, y, z, sprite=sprite, detects_collisions=False)
        self.add(p)

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
        w = width + outline_thickness
        h = height + outline_thickness
        sprite = sge.Sprite(None, width=w, height=h)
        sprite.draw_rectangle(draw_x, draw_y, w, h, fill, outline,
                              outline_thickness)
        p = _Projection(x, y, z, sprite=sprite, detects_collisions=False)
        self.add(p)

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
        w = width + outline_thickness
        h = height + outline_thickness
        sprite = sge.Sprite(None, width=w, height=h)
        sprite.draw_ellipse(draw_x, draw_y, w, h, fill, outline,
                            outline_thickness)
        p = _Projection(x, y, z, sprite=sprite, detects_collisions=False)
        self.add(p)

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
        outline_thickness = abs(outline_thickness)
        xy = radius + outline_thickness // 2
        wh = 2 * radius + outline_thickness
        sprite = sge.Sprite(None, width=wh, height=wh)
        sprite.draw_circle(xy, xy, radius, fill, outline, outline_thickness,
                           anti_alias)
        p = _Projection(x - radius, y - radius, z, sprite=sprite,
                        detects_collisions=False)
        self.add(p)

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
        p = _Projection(x, y, z, sprite=sprite, detects_collisions=False,
                        image_index=image, image_fps=0)
        self.add(p)

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
        w, h = font.get_size(text, width, height)
        draw_x = {sge.ALIGN_LEFT: 0, sge.ALIGN_CENTER: w / 2,
                  sge.ALIGN_RIGHT: w}.setdefault(halign, w / 2)
        draw_y = {sge.ALIGN_TOP: 0, sge.ALIGN_MIDDLE: h / 2,
                  sge.ALIGN_BOTTOM: h}.setdefault(valign, h / 2)
        sprite = sge.Sprite(None, width=w, height=h)
        sprite.draw_text(font, text, draw_x, draw_y, width, height, color,
                         halign, valign, anti_alias)
        p = _Projection(x, y, z, sprite=sprite, detects_collisions=False)
        self.add(p)

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

    def event_gain_keyboard_focus(self):
        """Gain keyboard focus event.

        See the documentation for
        :meth:`sge.Game.event_gain_keyboard_focus` for more information.

        """
        pass

    def event_lose_keyboard_focus(self):
        """Lose keyboard focus event.

        See the documentation for
        :meth:`sge.Game.event_lose_keyboard_focus` for more information.

        """
        if sge.DEBUG:
            bad_name = "event_loose_keyboard_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

    def event_gain_mouse_focus(self):
        """Gain mouse focus event.

        See the documentation for
        :meth:`sge.Game.event_gain_mouse_focus` for more information.

        """
        pass

    def event_lose_mouse_focus(self):
        """Lose mouse focus event.

        See the documentation for
        :meth:`sge.Game.event_lose_mouse_focus` for more information.

        """
        if sge.DEBUG:
            bad_name = "event_loose_mouse_focus"
            if hasattr(self, bad_name):
                sge._scold_user_on_lose_vs_loose(bad_name)

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
        self.objects = self._start_objects

        for view in self.views:
            view._reset()

        for obj in self.objects:
            obj._reset()


class _Projection(sge.StellarClass):

    # Object which destroys itself after being shown for one frame.

    def event_create(self):
        self.detects_collisions = False
        self.death_alarm = 2

    def event_step(self, time_passed):
        self.death_alarm -= 1
        if self.death_alarm <= 0:
            self.destroy()

    def event_destroy(self):
        if self.sprite is not None:
            del sge.game.sprites[self.sprite.id]
