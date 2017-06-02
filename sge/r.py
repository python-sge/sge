# Copyright (C) 2012-2017 Julie Marchant <onpon4@riseup.net>
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

"""
This module is a reserved namespace for internal use by the SGE, to
avoid cluttering up the sge namespace.  Use this for all non-standard
functions and variables.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import inspect
import math
import random
import time
import warnings
import weakref

import pygame
import six
from uniseg.linebreak import line_break_units

import sge


# How often to call cache.prune in milliseconds.
CACHE_PRUNE_TIME = 8000

# How long cached items should remain cached by default in seconds.
CACHE_DEFAULT_LIFE = 15

# Lists of objects that are tangible and objects that check for
# collisions; makes collision detection more efficient.
_colliders = []
_collision_checkers = []

# Set of objects that are active, to avoid looping through inactive
# objects needlessly.
_active_objects = set()

# Previous joystick states
_prev_axes = {}
_prev_hats = {}

# Display info
_display_info = None


class cache(object):

    prune_time = 0
    _cache = {}
    _prune = {}

    @classmethod
    def add(cls, i, value, prune_time=CACHE_DEFAULT_LIFE):
        # Add value with index ``i`` to cache as ``value``.
        # Automatically deleted after ``prune_time`` seconds.
        cls._cache[i] = value
        cls._prune[i] = time.time() + prune_time

    @classmethod
    def get(cls, i):
        # Get value with index ``i`` from cache, or ``None`` if it is
        # not in the cache.
        return cls._cache.get(i)

    @classmethod
    def clear(cls):
        # Clear all saved values from the cache.
        cls._cache = {}
        cls._prune = {}

    @classmethod
    def prune(cls):
        # Prune all expired values. Should be called infrequently (maybe
        # every 5 seconds or so), because it requires looping through
        # every cached value.
        p = []
        for i in cls._prune:
            if cls._prune[i] < time.time():
                p.append(i)

        for i in p:
            del cls._cache[i]
            del cls._prune[i]


def _check_color_input(value):
    # Make sure a color value is between 0 and 255.
    if value in six.moves.range(256):
        return value
    else:
        raise ValueError("Color values must be between 0 and 255.")


def _check_color(value):
    # Make sure a value is either None or a color.
    if value is not None and not isinstance(value, sge.gfx.Color):
        e = "`{}` is not a Color object.".format(repr(value))
        raise TypeError(e)


def _scale(surface, width, height):
    # Scale the given surface to the given width and height.
    if surface.get_width() == width and surface.get_height() == height:
        return surface.copy()

    width = int(round(width))
    height = int(round(height))
    if sge.game.scale_method == "smooth":
        try:
            new_surf = pygame.transform.smoothscale(surface, (width, height))
        except (pygame.error, ValueError):
            new_surf = pygame.transform.scale(surface, (width, height))
    elif sge.game.scale_method == "scale2x":
        new_surf = surface
        while (width > new_surf.get_width() or
               height > new_surf.get_height()):
            try:
                new_surf = pygame.transform.scale2x(new_surf)
            except pygame.error:
                break

        if new_surf.get_width() != width or new_surf.get_height() != height:
            new_surf = pygame.transform.scale(new_surf, (width, height))
    else:
        new_surf = pygame.transform.scale(surface, (width, height))

    return new_surf


def _get_blend_flags(blend_mode):
    # Return the appropriate Pygame flags for the given blend mode.
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
        }.get(blend_mode, 0)

    return pygame_flags


def _screen_blend(dest, source, dest_x, dest_y, alpha=False):
    dest.lock()
    source.lock()
    for y in six.moves.range(source.get_height()):
        if 0 <= dest_y + y < dest.get_height():
            for x in six.moves.range(source.get_width()):
                if 0 <= dest_x + x < dest.get_width():
                    dc = dest.get_at((dest_x + x, dest_y + y))
                    sc = source.get_at((x, y))

                    def blended_component(c1, c2):
                        return int(255 - (((255 - c1) / 255) *
                                          ((255 - c2) / 255) * 255))

                    r = blended_component(dc.r, sc.r)
                    g = blended_component(dc.g, sc.g)
                    b = blended_component(dc.b, sc.b)
                    a = blended_component(dc.a, sc.a) if alpha else dc.a

                    dest.set_at((dest_x + x, dest_y + y), pygame.Color(r, g, b, a))
    dest.unlock()
    source.unlock()


def _set_mode():
    # Set the mode of the screen based on self.width, self.height,
    # and self.fullscreen.
    global game_display_surface
    global game_xscale
    global game_yscale
    global game_window
    global game_window_width
    global game_window_height
    global game_x
    global game_y
    game = sge.game
    game_display_surface = _scale(game_display_surface, game.width, game.height)

    if game.scale:
        game_xscale = game.scale
        game_yscale = game.scale

    if game.fullscreen or not _display_info.wm:
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF

        modes = pygame.display.list_modes(0, flags)
        if modes == -1 or not modes:
            w = "Couldn't find out the maximum resolution! Assuming 1024x768."
            warnings.warn(w)
            modes = [(1024, 768)]

        force_auto_scale = False

        if game.scale:
            game_window_width = int(game.width * game.scale)
            game_window_height = int(game.height * game.scale)
            if not pygame.display.mode_ok(
                    (game_window_width, game_window_height), flags):
                game_window_width = _display_info.current_w
                game_window_height = _display_info.current_h
                force_auto_scale = True
        else:
            game_window_width = _display_info.current_w
            game_window_height = _display_info.current_h

        game_window = pygame.display.set_mode(
            (game_window_width, game_window_height), flags)

        if not game.scale or force_auto_scale:
            game_xscale = game_window_width / game.width
            game_yscale = game_window_height / game.height

            if game.scale_proportional:
                game_xscale = min(game_xscale, game_yscale)
                game_yscale = game_xscale

        w = max(1, game_window.get_width())
        h = max(1, game_window.get_height())
        game_x = int(round((w - game.width * game_xscale) / 2))
        game_y = int(round((h - game.height * game_yscale) / 2))
    else:
        game_x = 0
        game_y = 0
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF

        # Decide window size
        if game.scale:
            game_window_width = int(game.width * game.scale)
            game_window_height = int(game.height * game.scale)
        else:
            game_xscale = game_window_width / game.width
            game_yscale = game_window_height / game.height

            if game.scale_proportional:
                game_xscale = min(game_xscale, game_yscale)
                game_yscale = game_xscale

            flags |= pygame.RESIZABLE

        game_window = pygame.display.set_mode(
            (game_window_width, game_window_height), flags)

        w = max(1, game_window.get_width())
        h = max(1, game_window.get_height())
        game_x = int(round((w - game.width * game_xscale) / 2))
        game_y = int(round((h - game.height * game_yscale) / 2))


def _get_channel():
    # Return a channel for a sound effect to use.
    assert pygame.mixer.get_init()

    if not game_available_channels:
        _add_channels()

    return game_available_channels.pop(0)


def _release_channel(channel):
    # Release the given channel for other sounds to use.
    assert pygame.mixer.get_init()
    game_available_channels.append(channel)


def _add_channels():
    # Add four channels for playing sounds.
    assert pygame.mixer.get_init()

    old_num_channels = pygame.mixer.get_num_channels()
    new_num_channels = old_num_channels + 4
    pygame.mixer.set_num_channels(new_num_channels)

    for i in six.moves.range(old_num_channels, new_num_channels):
        game_available_channels.append(pygame.mixer.Channel(i))


def _handle_music():
    # Call each frame to control the music playback.
    if music is not None:
        if pygame.mixer.music.get_busy():
            time_played = pygame.mixer.music.get_pos()
            fade_time = music.rd["fade_time"]
            timeout = music.rd["timeout"]

            if fade_time:
                real_volume = music.volume / 100
                if time_played < fade_time:
                    volume = real_volume * time_played / fade_time
                    pygame.mixer.music.set_volume(volume)
                else:
                    pygame.mixer.music.set_volume(real_volume)

            if timeout and time_played >= timeout:
                music.stop()


def _get_dot_sprite(color):
    # Return a sprite for the given dot.
    i = ("dot_sprite", tuple(color))
    sprite = cache.get(i)
    if sprite is None:
        sprite = sge.gfx.Sprite(None, width=1, height=1)
        sprite.draw_dot(0, 0, color)

    cache.add(i, sprite)
    return sprite


def _get_line_sprite(x1, y1, x2, y2, color, thickness, anti_alias):
    # Return a sprite for the given line.
    w = int(round(abs(x2 - x1) + thickness))
    h = int(round(abs(y2 - y1) + thickness))
    i = ("line_sprite", x1, y1, x2, y2, tuple(color), thickness, anti_alias)
    sprite = cache.get(i)
    if sprite is None:
        sprite = sge.gfx.Sprite(None, width=w, height=h)
        sprite.draw_line(x1, y1, x2, y2, color, thickness, anti_alias)

    cache.add(i, sprite)
    return sprite


def _get_rectangle_sprite(width, height, fill, outline, outline_thickness):
    # Return a sprite for the given rectangle.
    i = ("rectangle_sprite", width, height,
         tuple(fill) if fill is not None else None,
         tuple(outline) if outline is not None else None,
         outline_thickness)
    sprite = cache.get(i)
    if sprite is None:
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        w = width + outline_thickness
        h = height + outline_thickness
        sprite = sge.gfx.Sprite(None, width=w, height=h)
        sprite.draw_rectangle(draw_x, draw_y, width, height, fill, outline,
                              outline_thickness)

    cache.add(i, sprite)
    return sprite


def _get_ellipse_sprite(width, height, fill, outline, outline_thickness,
                        anti_alias):
    # Return a sprite for the given ellipse.
    i = ("ellipse_sprite", width, height,
         tuple(fill) if fill is not None else None,
         tuple(outline) if outline is not None else None,
         outline_thickness, anti_alias)
    sprite = cache.get(i)
    if sprite is None:
        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        w = width + outline_thickness
        h = height + outline_thickness
        sprite = sge.gfx.Sprite(None, width=w, height=h)
        sprite.draw_ellipse(draw_x, draw_y, width, height, fill, outline,
                            outline_thickness)

    cache.add(i, sprite)
    return sprite


def _get_circle_sprite(radius, fill, outline, outline_thickness, anti_alias):
    # Return a sprite for the given circle.
    i = ("circle_sprite", radius, tuple(fill) if fill is not None else None,
         tuple(outline) if outline is not None else None,
         outline_thickness, anti_alias)
    sprite = cache.get(i)
    if sprite is None:
        outline_thickness = abs(outline_thickness)
        xy = radius + outline_thickness // 2
        wh = 2 * radius + outline_thickness
        sprite = sge.gfx.Sprite(None, width=wh, height=wh)
        sprite.draw_circle(xy, xy, radius, fill, outline, outline_thickness,
                           anti_alias)

    cache.add(i, sprite)
    return sprite


def _get_polygon_sprite(points, fill, outline, outline_thickness, anti_alias):
    # Return a sprite for the given polygon.
    i = ("poly_sprite", tuple(points),
         tuple(fill) if fill is not None else None,
         tuple(outline) if outline is not None else None,
         outline_thickness, anti_alias)
    sprite = cache.get(i)
    if sprite is None:
        xlist = []
        ylist = []
        for point in points:
            xlist.append(point[0])
            ylist.append(point[1])
        x = min(xlist)
        y = min(ylist)
        width = max(xlist) - x
        height = max(ylist) - y

        outline_thickness = abs(outline_thickness)
        draw_x = outline_thickness // 2
        draw_y = outline_thickness // 2
        dpoints = [(a - x + draw_x, b - y + draw_y) for (a, b) in points]
        w = width + outline_thickness
        h = height + outline_thickness
        sprite = sge.gfx.Sprite(None, width=w, height=h, origin_x=draw_x,
                                origin_y=draw_y)
        sprite.draw_polygon(dpoints, fill, outline, outline_thickness,
                            anti_alias)

    cache.add(i, sprite)
    return sprite


def _get_hat(joystick, hat):
    # Return the position of a joystick HAT.
    if (joystick is not None and joystick < len(game_joysticks) and
            hat < game_joysticks[joystick].get_numhats()):
        return game_joysticks[joystick].get_hat(hat)
    else:
        return (0, 0)


def bl_update(self, time_passed):
    # Update the animation frame.
    if self.rd["fps"] != self.sprite.fps:
        self.rd["fps"] = self.sprite.fps
        if self.sprite.fps:
            self.rd["frame_time"] = 1000 / self.sprite.fps
            if not self.rd["frame_time"]:
                # This would be caused by a round-off to 0 resulting
                # from a much too high frame rate.  It would cause a
                # division by 0 later, so this is meant to prevent that.
                self.rd["frame_time"] = 0.0000001
                w = "Could not calculate timing for {:.2e} FPS.".format(
                    self.sprite.fps)
                warnings.warn(w)
        else:
            self.rd["frame_time"] = None

    if self.rd["frame_time"] is not None:
        self.rd["count"] += time_passed
        self.rd["image_index"] += int(self.rd["count"] / self.rd["frame_time"])
        self.rd["count"] %= abs(self.rd["frame_time"])
        self.rd["image_index"] %= self.sprite.frames


def bl_get_image(self):
    return s_get_image(self.sprite, self.rd["image_index"])


def f_split_text(self, text, width=None):
    # Split the text into lines of the proper size for ``width`` and
    # return a list of the lines.  If ``width`` is None, only
    # newlines split the text.
    lines = text.splitlines()

    if width is None:
        return lines
    else:
        split_text = []
        for line in lines:
            if self.rd["font"].size(line)[0] <= width:
                split_text.append(line)
            else:
                words = list(line_break_units(line))
                while words:
                    current_line = words.pop(0)
                    while self.rd["font"].size(current_line)[0] > width:
                        start = ""
                        while self.rd["font"].size(
                                start + current_line[0])[0] <= width:
                            start += current_line[0]
                            current_line = current_line[1:]
                        split_text.append(start)

                    while (words and self.rd["font"].size(''.join(
                            [current_line, words[0]]).rstrip())[0] <= width):
                        current_line = ''.join([current_line,
                                                words.pop(0)])
                    split_text.append(current_line.rstrip())
                        
        return split_text


def o_update(self, time_passed, delta_mult):
    # Update this object (should be called each frame).
    # Update the animation frame.
    if self.image_fps and isinstance(self.sprite, sge.gfx.Sprite):
        self.rd["anim_count"] += time_passed
        self.rd["image_index"] += int(self.rd["anim_count"] / self.rd["frame_time"])
        self.rd["anim_count"] %= abs(self.rd["frame_time"])

        if self.sprite is not None:
            while self.rd["image_index"] >= self.sprite.frames:
                self.rd["image_index"] -= self.sprite.frames
                self.event_animation_end()
            while self.rd["image_index"] < 0:
                self.rd["image_index"] += self.sprite.frames
                self.event_animation_end()

    # Alarms
    activated_alarms = []
    for a in self.alarms:
        self.alarms[a] -= delta_mult
        if self.alarms[a] <= 0:
            activated_alarms.append(a)
    for a in activated_alarms:
        del self.alarms[a]
        self.event_alarm(a)

    # Movement
    if self is not sge.game.mouse:
        self.event_update_position(delta_mult)


def o_update_object_areas(self):
    room = sge.game.current_room
    if room is not None and self in room.objects:
        x = self.bbox_left
        y = self.bbox_top
        w = self.bbox_width
        h = self.bbox_height

        if self.sprite is not None:
            x = min(x, self.x - self.image_origin_x)
            y = min(y, self.y - self.image_origin_y)
            w = max(w, self.sprite.width)
            h = max(h, self.sprite.height)

        my_areas = r_get_rectangle_object_areas(room, x, y, w, h)
    else:
        my_areas = set()

    for area in my_areas ^ self.rd["object_areas"]:
        if area in my_areas:
            if area is None:
                area = (None, None)
            i, j = area
            if (i is not None and j is not None and
                    i < len(room.object_areas) and
                    j < len(room.object_areas[i])):
                oa = room.object_areas[i][j].copy()
                oa.add(self)
                room.object_areas[i][j] = oa
            else:
                if i is not None or j is not None:
                    e = "An object area existed in a {} object, but not in the room!".format(
                        self.__class__.__name__)
                    e += "\nAttempted area: ({}, {})".format(i, j)
                    x = len(room.object_areas)
                    y = len(room.object_areas[0]) if x else 0
                    e += "\nAvailable areas: {}x{}".format(x, y)
                    warnings.warn(e)

                oa = room.object_area_void.copy()
                oa.add(self)
                room.object_area_void = oa
        else:
            if area is None:
                area = (None, None)
            i, j = area
            if (i is not None and j is not None and
                    i < len(room.object_areas) and
                    j < len(room.object_areas[i])):
                oa = room.object_areas[i][j].copy()
                oa.discard(self)
                room.object_areas[i][j] = oa
            else:
                if i is not None or j is not None:
                    e = "An object area existed in a {} object, but not in the room!".format(
                        self.__class__.__name__)
                    e += "\nAttempted area: ({}, {})".format(i, j)
                    x = len(room.object_areas)
                    y = len(room.object_areas[0]) if x else 0
                    e += "\nAvailable areas: {}x{}".format(x, y)
                    warnings.warn(e)

                oa = room.object_area_void.copy()
                oa.discard(self)
                room.object_area_void = oa

    self.rd["object_areas"] = my_areas


def o_update_collision_lists(self):
    global _colliders
    global _collision_checkers
    if (self.tangible and sge.game.current_room is not None and
            self in sge.game.current_room.objects):
        if self not in _colliders:
            colliders = _colliders[:]
            colliders.append(self)
            _colliders = colliders

        if (self.checks_collisions and self not in _collision_checkers):
            collision_checkers = _collision_checkers[:]
            collision_checkers.append(self)
            _collision_checkers = collision_checkers
        else:
            collision_checkers = _collision_checkers[:]
            while self in collision_checkers:
                collision_checkers.remove(self)
            _collision_checkers = collision_checkers
    else:
        colliders = _colliders[:]
        while self in colliders:
            colliders.remove(self)
        _colliders = colliders

        collision_checkers = _collision_checkers[:]
        while self in collision_checkers:
            collision_checkers.remove(self)
        _collision_checkers = collision_checkers


def o_is_other(self, other=None):
    r = False

    if other is None:
        r = True
    elif isinstance(other, sge.dsp.Object):
        r = self is other
    elif isinstance(other, (list, tuple, set)):
        r = self in other
    elif inspect.isclass(other):
        r = isinstance(self, other)

    return r


def o_detect_collisions(self):
    assert self.checks_collisions
    for other in self.rd["colliders"]:
        if other is self:
            continue

        # Delete self from the other object's list of colliders to
        # prevent redundancy.
        while self in other.rd["colliders"]:
            other.rd["colliders"].remove(self)

        if self.collision(other):
            self_prev_bbox_left = self.xprevious + self.bbox_x
            self_prev_bbox_right = (self_prev_bbox_left +
                                    self.bbox_width)
            self_prev_bbox_top = self.yprevious + self.bbox_y
            self_prev_bbox_bottom = (self_prev_bbox_top +
                                     self.bbox_height)
            other_prev_bbox_left = other.xprevious + other.bbox_x
            other_prev_bbox_right = (other_prev_bbox_left +
                                     other.bbox_width)
            other_prev_bbox_top = other.yprevious + other.bbox_y
            other_prev_bbox_bottom = (other_prev_bbox_top +
                                      other.bbox_height)

            if self_prev_bbox_right <= other_prev_bbox_left:
                xdirection = 1
            elif self_prev_bbox_left >= other_prev_bbox_right:
                xdirection = -1
            else:
                xdirection = 0

            if self_prev_bbox_bottom <= other_prev_bbox_top:
                ydirection = 1
            elif self_prev_bbox_top >= other_prev_bbox_bottom:
                ydirection = -1
            else:
                ydirection = 0

            self.event_collision(other, xdirection, ydirection)
            other.event_collision(self, -xdirection, -ydirection)


def o_get_origin_offset(self):
    # Return the amount to offset the origin as (x, y).
    if isinstance(self.sprite, sge.gfx.Sprite):
        new_origin_x = self.sprite.origin_x
        new_origin_y = self.sprite.origin_y

        img = s_get_image(self.sprite, self.image_index, self.image_xscale,
                          self.image_yscale, self.image_rotation)
        nimg = s_get_image(self.sprite, self.image_index, self.image_xscale,
                           self.image_yscale)
        width = img.get_width() / abs(self.image_xscale)
        height = img.get_height() / abs(self.image_yscale)
        normal_width = nimg.get_width() / abs(self.image_xscale)
        normal_height = nimg.get_height() / abs(self.image_yscale)

        if self.image_rotation % 360:
            center_x = normal_width / 2
            center_y = normal_height / 2
            c_origin_x = new_origin_x - center_x
            c_origin_y = new_origin_y - center_y
            start_angle = math.atan2(c_origin_y, c_origin_x)
            radius = math.hypot(c_origin_x, c_origin_y)
            new_angle = start_angle + math.radians(self.image_rotation)
            new_c_origin_x = radius * math.cos(new_angle)
            new_c_origin_y = radius * math.sin(new_angle)
            new_origin_x = new_c_origin_x + center_x
            new_origin_y = new_c_origin_y + center_y

        if self.image_xscale < 0:
            new_origin_x = width - new_origin_x

        if self.image_yscale < 0:
            new_origin_y = height - new_origin_y

        new_origin_x *= abs(self.image_xscale)
        new_origin_y *= abs(self.image_yscale)

        x_offset = new_origin_x - self.sprite.origin_x
        y_offset = new_origin_y - self.sprite.origin_y
    else:
        x_offset = 0
        y_offset = 0

    return (x_offset, y_offset)


def o_set_speed(self):
    # Set the speed and move direction based on xvelocity and
    # yvelocity.
    self.rd["speed"] = math.hypot(self.rd["xv"], self.rd["yv"])
    self.rd["mv_dir"] = math.degrees(math.atan2(self.rd["yv"], self.rd["xv"]))


def r_get_rectangle_object_areas(self, x, y, width, height):
    # Get a set of object areas a rect is in.
    xis = int(math.floor(x / self.object_area_width))
    yis = int(math.floor(y / self.object_area_height))
    xie = int(math.ceil((x + width) / self.object_area_width))
    yie = int(math.ceil((y + height) / self.object_area_height))

    areas = set()

    if (self.object_areas and xis < len(self.object_areas) and
            yis < len(self.object_areas[0]) and xie > 0 and yie > 0):
        use_void = False

        if xis < 0:
            xis = 0
            use_void = True
        if yis < 0:
            yis = 0
            use_void = True
        if xie > len(self.object_areas):
            xie = len(self.object_areas)
            use_void = True
        if yie > len(self.object_areas[0]):
            yie = len(self.object_areas[0])
            use_void = True

        if use_void:
            areas.add(None)

        for xi in six.moves.range(xis, xie):
            for yi in six.moves.range(yis, yie):
                areas.add((xi, yi))
    else:
        areas.add(None)

    return areas


def r_set_object_areas(self, update_objects=True):
    self.object_areas = []
    for i in six.moves.range(0, self.width, self.object_area_width):
        column = [set() for j in six.moves.range(0, self.height,
                                                 self.object_area_height)]
        self.object_areas.append(column)

    self.object_area_void = set()

    if update_objects:
        for obj in self.objects:
            o_update_object_areas(obj)


def r_update_fade(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height
    if complete < 0.5:
        diff = (complete - self.rd["t_complete_last"]) * 2
        c = sge.gfx.Color([int(round(diff * 255))] * 3)
        darkener = sge.gfx.Sprite(width=w, height=h)
        darkener.draw_rectangle(0, 0, w, h, c)
        transition_sprite.draw_sprite(darkener, 0, 0, 0,
                                      blend_mode=sge.BLEND_RGB_SUBTRACT)
    else:
        complete = (complete - 0.5) * 2
        c = sge.gfx.Color((0, 0, 0, int(round(255 - complete * 255))))
        transition_sprite.draw_clear()
        transition_sprite.draw_rectangle(0, 0, w, h, fill=c)


def r_update_dissolve(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height
    diff = complete - self.rd["t_complete_last"]
    c = sge.gfx.Color((0, 0, 0, int(round(diff * 255))))
    eraser = sge.gfx.Sprite(width=w, height=h)
    eraser.draw_rectangle(0, 0, w, h, c)
    transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                  blend_mode=sge.BLEND_RGBA_SUBTRACT)


def r_update_pixelate(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height
    scale_method = sge.game.scale_method
    sge.game.scale_method = None

    if complete < 0.8:
        complete *= 1.25
        swidth = max(1, w * (1 - complete))
        sheight = max(1, h * (1 - complete))
        transition_sprite.width = swidth
        transition_sprite.height = sheight
        transition_sprite.width = w
        transition_sprite.height = h
    else:
        diff = (complete - self.rd["t_complete_last"]) * 5
        c = sge.gfx.Color((0, 0, 0, int(round(diff * 255))))
        eraser = sge.gfx.Sprite(width=w, height=h)
        eraser.draw_rectangle(0, 0, w, h, c)
        transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                      blend_mode=sge.BLEND_RGBA_SUBTRACT)

    sge.game.scale_method = scale_method


def r_update_wipe_left(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width * complete
    x = transition_sprite.width - w
    h = transition_sprite.height
    transition_sprite.draw_erase(x, 0, w, h)


def r_update_wipe_right(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width * complete
    h = transition_sprite.height
    transition_sprite.draw_erase(0, 0, w, h)


def r_update_wipe_up(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height * complete
    y = transition_sprite.height - h
    transition_sprite.draw_erase(0, y, w, h)


def r_update_wipe_down(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height * complete
    transition_sprite.draw_erase(0, 0, w, h)


def r_update_wipe_upleft(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height
    x = w - w * complete * 2
    y = h - h * complete * 2
    eraser = sge.gfx.Sprite(width=w, height=h)
    eraser.draw_polygon([(w, h), (x, h), (w, y)],
                        fill=sge.gfx.Color((0, 0, 0, 255)), anti_alias=True)
    transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                  blend_mode=sge.BLEND_RGBA_SUBTRACT)


def r_update_wipe_upright(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height
    x = w * complete * 2
    y = h - h * complete * 2
    eraser = sge.gfx.Sprite(width=w, height=h)
    eraser.draw_polygon([(0, h), (x, h), (0, y)],
                        fill=sge.gfx.Color((0, 0, 0, 255)), anti_alias=True)
    transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                  blend_mode=sge.BLEND_RGBA_SUBTRACT)


def r_update_wipe_downleft(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height
    x = w - w * complete * 2
    y = h * complete * 2
    eraser = sge.gfx.Sprite(width=w, height=h)
    eraser.draw_polygon([(w, 0), (x, 0), (w, y)],
                        fill=sge.gfx.Color((0, 0, 0, 255)), anti_alias=True)
    transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                  blend_mode=sge.BLEND_RGBA_SUBTRACT)


def r_update_wipe_downright(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height
    x = w * complete * 2
    y = w * complete * 2
    eraser = sge.gfx.Sprite(width=w, height=h)
    eraser.draw_polygon([(0, 0), (x, 0), (0, y)],
                        fill=sge.gfx.Color((0, 0, 0, 255)), anti_alias=True)
    transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                  blend_mode=sge.BLEND_RGBA_SUBTRACT)


def r_update_wipe_matrix(self, complete):
    transition_sprite = self.rd["t_sprite"]

    if self.rd["t_arg"]:
        pw, ph = self.rd["t_arg"]
    else:
        pw = 4
        ph = 4

    w = transition_sprite.width
    h = transition_sprite.height
    mw = int(w / pw)
    mh = int(h / ph)

    remaining = self.rd["t_matrix_remaining"]
    if remaining is None:
        remaining = []
        for x in six.moves.range(mw):
            for y in six.moves.range(mh):
                remaining.append((x, y))

    diff = complete - self.rd["t_complete_last"]
    new_erase = int(mw * mh * diff)
    transition_sprite.draw_lock()
    while new_erase > 0 and remaining:
        new_erase -= 1
        x, y = remaining.pop(random.randrange(len(remaining)))
        transition_sprite.draw_erase(x * pw, y * ph, pw, ph)
    transition_sprite.draw_unlock()
    self.rd["t_matrix_remaining"] = remaining


def r_update_iris_in(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height

    if self.rd["t_arg"]:
        x, y = self.rd["t_arg"]
    else:
        x = w / 2
        y = h / 2

    r = int(math.hypot(max(x, sge.game.width - x),
                       max(y, sge.game.height - y)) * (1 - complete))
    eraser = sge.gfx.Sprite(width=w, height=h)
    eraser_eraser = sge.gfx.Sprite(width=w, height=h)
    eraser_eraser.draw_circle(x, y, r, fill=sge.gfx.Color((0, 0, 0, 255)))

    eraser.draw_lock()
    eraser.draw_rectangle(0, 0, w, h, fill=sge.gfx.Color((0, 0, 0, 255)))
    eraser.draw_sprite(eraser_eraser, 0, 0, 0,
                       blend_mode=sge.BLEND_RGBA_SUBTRACT)
    eraser.draw_unlock()

    transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                  blend_mode=sge.BLEND_RGBA_SUBTRACT)


def r_update_iris_out(self, complete):
    transition_sprite = self.rd["t_sprite"]
    w = transition_sprite.width
    h = transition_sprite.height

    if self.rd["t_arg"]:
        x, y = self.rd["t_arg"]
    else:
        x = w / 2
        y = h / 2

    r = int(math.hypot(max(x, sge.game.width - x),
                       max(y, sge.game.height - y)) * complete)
    eraser = sge.gfx.Sprite(width=w, height=h)
    eraser.draw_circle(x, y, r, fill=sge.gfx.Color((0, 0, 0, 255)))
    transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                  blend_mode=sge.BLEND_RGBA_SUBTRACT)


def s_set_size(self):
    # Adjust the size of the base images.  Note: this change is
    # destructive and irreversible.  It is necessary for the drawing
    # methods to work properly, specifically whenever ``width`` and
    # ``height`` are set.
    width = int(round(self.width))
    height = int(round(self.height))
    for i in six.moves.range(self.frames):
        if sge.game.scale_method == "smooth":
            try:
                self.rd["baseimages"][i] = pygame.transform.smoothscale(
                    self.rd["baseimages"][i], (width, height))
            except (pygame.error, ValueError):
                self.rd["baseimages"][i] = pygame.transform.scale(
                    self.rd["baseimages"][i], (width, height))
        elif sge.game.scale_method == "scale2x":
            new_surf = self.rd["baseimages"][i]
            while (width > new_surf.get_width() or
                   height > new_surf.get_height()):
                try:
                    new_surf = pygame.transform.scale2x(new_surf)
                except pygame.error:
                    break

            if new_surf.get_width() != width or new_surf.get_height() != height:
                new_surf = pygame.transform.scale(self.rd["baseimages"][i],
                                                  (width, height))

            self.rd["baseimages"][i] = new_surf
        else:
            self.rd["baseimages"][i] = pygame.transform.scale(
                self.rd["baseimages"][i], (width, height))


def s_refresh(self):
    # Forget any cached values by moving to the next draw cycle.
    if not self.rd["locked"]:
        self.rd["drawcycle"] += 1
        self.rd["drawcycle"] %= 999999999999999


def s_set_transparency(self, image):
    # Return a copy of the surface with transparency properly set
    # for this sprite's settings.
    if isinstance(self.transparent, sge.gfx.Color):
        img = image.convert()
        color = pygame.Color(*self.transparent)
        img.set_colorkey(color, pygame.RLEACCEL)
        return img
    elif self.transparent:
        return image.convert_alpha()
    else:
        return image.convert()

    # Should not happen!
    warnings.warn("Failed to account for transparency")
    return image.convert()


def s_get_image(self, num, xscale=1, yscale=1, rotation=0, alpha=255,
                blend=None, blend_mode=None):
    if isinstance(self, sge.gfx.Sprite):
        num %= self.frames
        if blend_mode is None:
            blend_mode = sge.BLEND_RGB_MULTIPLY

        i = ("s_image", weakref.ref(self), self.rd["drawcycle"], num, xscale,
             yscale, rotation, alpha,
             tuple(blend) if blend is not None else None, blend_mode)
        img = cache.get(i)
        if img is None:
            if xscale != 0 and yscale != 0:
                img = s_set_transparency(self, self.rd["baseimages"][num])
                xflip = xscale < 0
                yflip = yscale < 0
                img = pygame.transform.flip(img, xflip, yflip)
                img = _scale(img, self.width * abs(xscale),
                             self.height * abs(yscale))

                if rotation != 0:
                    img = pygame.transform.rotate(img, -rotation)

                alpha = int(alpha)
                if alpha < 255:
                    if img.get_flags() & pygame.SRCALPHA:
                        # Have to do this the more difficult way.
                        img.fill((255, 255, 255, alpha), None,
                                 pygame.BLEND_RGBA_MULT)
                    else:
                        img.set_alpha(alpha, pygame.RLEACCEL)

                if blend is not None:
                    pygame_flags = _get_blend_flags(blend_mode)
                    if blend_mode == sge.BLEND_RGB_SCREEN:
                        ssurf = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                        ssurf.fill(pygame.Color(*blend))
                        _screen_blend(img, ssurf, 0, 0, False)
                    elif blend_mode == sge.BLEND_RGBA_SCREEN:
                        ssurf = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                        ssurf.fill(pygame.Color(*blend))
                        _screen_blend(img, ssurf, 0, 0, True)
                    else:
                        img.fill(pygame.Color(*blend), None, pygame_flags)
            else:
                img = pygame.Surface((1, 1))
                img.set_colorkey((0, 0, 0), pygame.RLEACCEL)

        cache.add(i, img)
        return img
    else:
        return self


def s_get_precise_mask(self, num, xscale, yscale, rotation):
    # Return a precise mask (2D list of True/False values) for the
    # given image index.
    i = ("s_mask", weakref.ref(self), self.width, self.height,
         self.rd["drawcycle"], num, xscale, yscale, rotation)
    mask = cache.get(i)
    if mask is None:
        image = s_set_transparency(self, self.rd["baseimages"][num])
        xflip = xscale < 0
        yflip = yscale < 0
        image = pygame.transform.flip(image, xflip, yflip)
        w = int(round(self.width * abs(xscale)))
        h = int(round(self.height * abs(yscale)))
        image = pygame.transform.scale(image, (w, h))
        if rotation:
            image = pygame.transform.rotate(image, -rotation)

        image.lock()
        mask = []
        if image.get_flags() & pygame.SRCALPHA:
            for x in six.moves.range(image.get_width()):
                mask.append([])
                for y in six.moves.range(image.get_height()):
                    mask[x].append(image.get_at((x, y)).a > 0)
        else:
            colorkey = image.get_colorkey()
            for x in six.moves.range(image.get_width()):
                mask.append([])
                for y in six.moves.range(image.get_height()):
                    mask[x].append(image.get_at((x, y)) == colorkey)
        image.unlock()

    cache.add(i, mask)
    return mask


def s_from_text(cls, font, text, width, height, color, halign, valign,
                anti_alias):
    # Version of gfx.Sprite.from_text which always returns the same
    # sprite, to avoid unnecessary duplication for things like
    # projections.
    f_name = tuple(font.name) if font.name is not None else None
    i = ("text_sprite", cls, f_name, font.size, font.underline, font.bold,
         font.italic, text, width, height, str(color), halign, valign,
         anti_alias)
    s = cache.get(i)
    if s is None:
        w = font.get_width(text, width, height)
        h = font.get_height(text, width, height)
        x = {"left": 0, "right": w, "center": w / 2}.get(halign.lower(), 0)
        y = {"top": 0, "bottom": h, "middle": h / 2}.get(valign.lower(), 0)
        s = cls(width=w, height=h, origin_x=x, origin_y=y)
        s.draw_text(font, text, x, y, width, height, color, halign, valign)

    cache.add(i, s)
    return s


def tg_blit(self, dest, x, y):
    # Blit the tile grid onto a Pygame surface.
    # Note: origin is NOT taken into account here!
    def get_tile(i, j):
        return self.tiles[i + j * self.section_length]

    sx = x
    sy = y

    if self.render_method == "isometric":
        x = -int(sx / self.tile_width)
        imin = max(0, x)
        imax = min(self.section_length,
                   x + int(math.ceil(dest.get_width() / self.tile_width)) + 1)

        h = self.tile_height / 2
        y = -int(sy / h)
        jmin = max(0, y)
        jmax = min(int(len(self.tiles) // self.section_length),
                   y + int(math.ceil(dest.get_height() / h)) + 1)
    else:
        x = -int(sx / self.tile_width)
        imin = max(0, x)
        imax = min(self.section_length,
                   x + int(math.ceil(dest.get_width() / self.tile_width)) + 1)

        y = -int(sy / self.tile_height)
        jmin = max(0, y)
        jmax = min(int(len(self.tiles) // self.section_length),
                   y + int(math.ceil(dest.get_height() / self.tile_height)) + 1)

    irng = six.moves.range(imin, imax)
    jrng = six.moves.range(jmin, jmax)

    for i in irng:
        for j in jrng:
            sprite = get_tile(i, j)
            if sprite is not None:
                if self.render_method == "isometric":
                    x = sx + i * self.tile_width
                    y = sx + j * self.tile_height / 2
                    if i / 2 != i // 2:
                        x += i * self.tile_width / 2
                else:
                    x = sx + i * self.tile_width
                    y = sy + j * self.tile_height

                ssurf = s_set_transparency(sprite, sprite.rd["baseimages"][0])
                dest.blit(ssurf, (int(x), int(y)))


def v_limit(self):
    # Keep the view within the room.
    if sge.game.current_room is not None:
        if self.x < 0:
            self.rd["x"] = 0
        elif self.x + self.width > sge.game.current_room.width:
            self.rd["x"] = sge.game.current_room.width - self.width

        if self.y < 0:
            self.rd["y"] = 0
        elif self.y + self.height > sge.game.current_room.height:
            self.rd["y"] = sge.game.current_room.height - self.height
