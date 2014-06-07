# SGE Transition Framework
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

"""
This module provides a framework for transition animations.
"""

import random

import sge

__all__ = []

FADE = 1
DISSOLVE = 2
PIXELATE = 3
WIPE_LEFT = 4
WIPE_RIGHT = 5
WIPE_TOP = 6
WIPE_BOTTOM = 7
WIPE_TOPLEFT = 8
WIPE_TOPRIGHT = 9
WIPE_BOTTOMLEFT = 10
WIPE_BOTTOMRIGHT = 11
WIPE_MATRIX = 12


class Room(sge.Room):

    transition_update = None
    transition_sprite = None
    transition_duration = 0

    def event_room_start(self):
        self.transition_time_passed = 0
        self.transition_complete_last = 0
        self.transition_variables = {}

    def update_fade(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        if complete < 0.5:
            diff = (complete - self.transition_complete_last) * 2
            c = [int(round(diff * 255))] * 3
            darkener = sge.Sprite(width=self.transition_sprite.width,
                                  height=self.transition_sprite.height)
            darkener.draw_rectangle(0, 0, w, h, c)
            self.transition_sprite.draw_sprite(
                darkener, 0, 0, 0, blend_mode=sge.BLEND_RGB_SUBTRACT)
            darkener.destroy()
        else:
            complete = (complete - 0.5) * 2
            c = (0, 0, 0, int(round(255 - complete * 255)))
            self.transition_sprite.draw_clear()
            self.transition_sprite.draw_rectangle(0, 0, w, h, fill=c)

    def update_dissolve(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        diff = complete - self.transition_complete_last
        c = (0, 0, 0, int(round(diff * 255)))
        eraser = sge.Sprite(width=self.transition_sprite.width,
                            height=self.transition_sprite.height)
        eraser.draw_rectangle(0, 0, w, h, c)
        self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                           blend_mode=sge.BLEND_RGBA_SUBTRACT)
        eraser.destroy()

    def update_pixelate(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        if complete < 0.5:
            complete *= 2
            swidth = max(1, w * (1 - complete))
            sheight = max(1, h * (1 - complete))
            self.transition_sprite.width = swidth
            self.transition_sprite.height = sheight
            self.transition_sprite.width = w
            self.transition_sprite.height = h
        else:
            diff = (complete - self.transition_complete_last) * 2
            c = (0, 0, 0, int(round(diff * 255)))
            eraser = sge.Sprite(width=self.transition_sprite.width,
                                height=self.transition_sprite.height)
            eraser.draw_rectangle(0, 0, w, h, c)
            self.transition_sprite.draw_sprite(eraser, 0, 0, 0,
                                               blend_mode=sge.BLEND_RGBA_SUBTRACT)
            eraser.destroy()

    def update_wipe_left(self, complete):
        w = self.transition_sprite.width * complete
        h = self.transition_sprite.height
        self.transition_sprite.draw_erase(0, 0, w, h)

    def update_wipe_right(self, complete):
        w = self.transition_sprite.width * complete
        x = self.transition_sprite.width - w
        h = self.transition_sprite.height
        self.transition_sprite.draw_erase(x, 0, w, h)

    def update_wipe_top(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height * complete
        self.transition_sprite.draw_erase(0, 0, w, h)

    def update_wipe_bottom(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height * complete
        y = self.transition_sprite.height - h
        self.transition_sprite.draw_erase(0, y, w, h)

    def update_wipe_matrix(self, complete):
        psize = 16
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        mw = int(round(w / psize))
        mh = int(round(h / psize))
        if "remaining" in self.transition_variables:
            remaining = self.transition_variables["remaining"]
        else:
            remaining = []
            for x in range(mw):
                for y in range(mh):
                    remaining.append((x, y))

        diff = complete - self.transition_complete_last
        new_erase = int(round(mw * mh * diff))
        while new_erase > 0 and remaining:
            new_erase -= 1
            x, y = remaining.pop(random.randrange(len(remaining)))
            self.transition_sprite.draw_erase(x * psize, y * psize, psize,
                                              psize)

        self.transition_variables["remaining"] = remaining

    def show_transition(self, transition, sprite, duration):
        """Show a transition.

        Arguments:

        - ``transition`` -- The type of transition to use.  Should be
          one of the following:

          - :const:`xsge.transition.FADE` -- Fade out (to black) and
            then fade in.

          - :const:`xsge.transition.DISSOLVE` -- Gradually replace the
            first room with the second room.

          - :const:`xsge.transition.PIXELATE` -- Pixelate the first
            room, then fade into the second room.  If
            :attr:`sge.game.scale_smooth` is :const:`True`, the effect
            will instead be to blur and unblur the rooms.  This relies
            on the destructiveness of changing :attr:`sge.Sprite.width`
            and :attr:`sge.Sprite.height`.

          - :const:`xsge.transition.WIPE_LEFT` -- Wipe transition from
            left to right.

          - :const:`xsge.transition.WIPE_RIGHT` -- Wipe transition from
            right to left.

          - :const:`xsge.transition.WIPE_TOP` -- Wipe transition from
            top to bottom.

          - :const:`xsge.transition.WIPE_BOTTOM` -- Wipe transition from
            bottom to top.

          - :const:`xsge.transition.WIPE_MATRIX` -- Matrix wipe
            transition.

        - ``sprite`` -- The sprite to use as the first image (the one
          being transitioned out of).  Generally should be a screenshot
          of the previous room.

        - ``duration`` -- The time the transition should take in
          milliseconds.

        """
        self.transition_update = {
            FADE: self.update_fade, DISSOLVE: self.update_dissolve,
            PIXELATE: self.update_pixelate, WIPE_LEFT: self.update_wipe_left,
            WIPE_RIGHT: self.update_wipe_right, WIPE_TOP: self.update_wipe_top,
            WIPE_BOTTOM: self.update_wipe_bottom,
            WIPE_MATRIX: self.update_wipe_matrix
            }.setdefault(transition, lambda c: None)
        self.transition_sprite = sprite
        self.transition_duration = duration
        self.transition_time_passed = 0
        self.transition_complete_last = 0
        self.transition_variables = {}

    def transition_start(self, transition=FADE, duration=1500):
        """Start the room, using a transition.

        See the documentation for :meth:`sge.Room.start` and
        :meth:`xsge.transition.Room.show_transition` for more
        information.

        """
        screenshot = sge.Sprite.from_screenshot()
        self.show_transition(transition, screenshot, duration)
        self.start()

    def transition_resume(self, transition=FADE, duration=1500):
        """Resume the room, using a transition.

        See the documentation for :meth:`sge.Room.resume` and
        :meth:`xsge.transition.Room.show_transition` for more
        information.

        """
        screenshot = sge.Sprite.from_screenshot()
        self.show_transition(transition, screenshot, duration)
        self.resume()

    def transition_end(self, transition=FADE, duration=1500, next_room=None,
                       resume=True):
        """End the room, using a transition for the next room.

        See the documentation for :meth:`sge.Room.end` and
        :meth:`xsge.transition.Room.show_transition` for more
        information.

        """
        if next_room is None:
            next_room = self.room_number + 1

        if (next_room >= -len(sge.game.rooms) and
                next_room < len(sge.game.rooms)):
            screenshot = sge.Sprite.from_screenshot()
            sge.game.rooms[next_room].show_transition(transition, screenshot,
                                                      duration)

        self.end(next_room=next_room, resume=resume)

    def event_step(self, time_passed, delta_mult):
        if (self.transition_update is not None and
                self.transition_sprite is not None and
                self.transition_duration > 0):
            self.transition_time_passed += time_passed

            if self.transition_time_passed < self.transition_duration:
                complete = (self.transition_time_passed /
                            self.transition_duration)
                self.transition_update(complete)
                self.transition_complete_last = complete
                sge.game.project_sprite(self.transition_sprite, 0, 0, 0)
            else:
                self.transition_sprite.destroy()
                self.transition_update = None
                self.transition_sprite = None
                self.transition_duration = 0
                self.transition_time_passed = 0
                self.transition_complete_last = 0
                self.transition_variables = {}
