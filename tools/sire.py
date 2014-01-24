#!/usr/bin/env python2

# Stellar Imprudently Reduced Editor
# Copyright (C) 2014 Julian Marchant <onpon4@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.0.1"

import sge
import stj

MODE_MOVE = 1
MODE_STAMP = 2
MODE_PAINT = 3


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'f11':
            self.fullscreen = not self.fullscreen
        elif key == 'escape':
            self.event_close()

    def event_close(self):
        # TODO: Make a check for saving changes first.
        self.end()


class Room(sge.Room):

    def event_room_start(self):
        self.mode = MODE_MOVE
        self.selected_object = None
        self.held_object = None
        self.grid_width = None
        self.grid_height = None
        self.mouse_click_x = 0
        self.mouse_click_y = 0

    def event_step(self, time_passed):
        if self.held_object is not None:
            self.held_object.x = sge.game.mouse.x
            self.held_object.y = sge.game.mouse.y

            if self.grid_width:
                self.held_object.x = self.grid_width * (
                    self.held_object.x // self.grid_width)
            if self.grid_height:
                self.held_object.y = self.grid_height * (
                    self.held_object.y // self.grid_height)

        if self.selected_object is not None:
            self.project_rectangle(
                self.selected_object.bbox_left, self.selected_object.bbox_top,
                self.selected_object.z, self.selected_object.bbox_width,
                self.selected_object.bbox_height, outline="blue")

        if self.mode == MODE_PAINT and sge.get_mouse_button_pressed("left"):
            # TODO: Paint objects; only one per position
            pass

    def event_key_press(self, key, char):
        # Destroy preview image
        if (self.mode in (MODE_STAMP, MODE_PAINT) and
                self.held_object is not None):
            self.held_object.destroy()

        # Un-hold and un-select
        self.selected_object = None
        self.held_object = None

        # TODO: create preview image for Stamp and Paint modes.
        if key in ('1', 'kp_1'):
            print("Switched to Move mode.")
            self.mode = MODE_MOVE
        elif key in ('2', 'kp_2'):
            print("Switched to Stamp mode.")
            self.mode = MODE_STAMP
        elif key in ('3', 'kp_3'):
            print("Switched to Paint mode.")
            self.mode = MODE_PAINT
        elif key == 'g':
            m = "Please enter the new grid width:"
            self.grid_width = eval(get_text_entry(m, repr(self.grid_width)))
            m = "Please enter the new grid height:"
            self.grid_height = eval(get_text_entry(m, repr(self.grid_height)))

    def event_mouse_move(self, x, y):
        if (self.mode == MODE_MOVE and sge.get_mouse_button_pressed("left") and
                self.selected_object is not None and
                (abs(self.mouse.x - self.mouse_click_x) > 2 or
                 abs(self.mouse.y - self.mouse_click_y) > 2)):
            self.held_object = self.selected_object

    def event_mouse_button_press(self, button):
        if button == "left":
            if self.mode == MODE_MOVE:
                self.mouse_click_x = self.mouse.x
                self.mouse_click_y = self.mouse.y
                self.selected_object = None
                for obj in self.objects:
                    if obj.collides(sge.game.mouse):
                        self.selected_object = obj
                        break
            elif self.mode == MODE_STAMP:
                pass
            elif self.mode == MODE_PAINT:
                pass

    def event_mouse_button_release(self, button):
        if button == "left":
            if self.mode == MODE_MOVE:
                self.selected_object = None
                self.held_object = None
            elif self.mode == MODE_STAMP:
                self.selected_object = None
                self.held_object = None
                # TODO: Create next object


class Object(sge.StellarClass):

    def __init__(self, cls, *args, **kwargs):
        super(Object, self).__init__(0, 0, collision_precise=True)
        self.set_args(*args, **kwargs)

    def set_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.x = eval(args[0]) if len(args) > 0 else 0
        self.y = eval(args[1]) if len(args) > 1 else 0
        self.z = eval(kwargs.setdefault("z", "0"))
        self.sprite = eval(kwargs.setdefault("sprite", "None"))
        self.image_index = eval(kwargs.setdefault("image_index", "0"))
        self.image_xscale = eval(kwargs.setdefault("image_xscale", "1"))
        self.image_yscale = eval(kwargs.setdefault("image_yscale", "1"))
        self.image_rotation = eval(kwargs.setdefault("image_rotation", "0"))
        self.image_alpha = eval(kwargs.setdefault("image_alpha", "255"))
        self.image_blend = eval(kwargs.setdefault("image_blend", "None"))
