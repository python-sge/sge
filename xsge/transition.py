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

    def event_room_start(self):
        self.transition_update = None
        self.transition_sprite = None
        self.transition_duration = 0
        self.transition_time_passed = 0
        self.transition_complete_last = 0

    def update_fade(self, complete):
        w = self.transition_sprite.width
        h = self.transition_sprite.height
        if complete < 0.5:
            complete *= 2
            diff = complete - self.transition_complete_last
            c = (0, 0, 0, int(round(diff * 255)))
            self.transition_sprite.draw_rectangle(0, 0, w, h, fill=c)
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
            swidth = max(1, int(round(w * (1 - complete))))
            sheight = max(1, int(round(h * (1 - complete))))
            self.transition_sprite.width = swidth
            self.transition_sprite.height = sheight
            self.transition_sprite.width = w
            self.transition_sprite.height = h
        else:
            complete = (complete - 0.5) * 2
            swidth = max(1, int(round(w * complete)))
            sheight = max(1, int(round(h * complete)))
            self.transition_sprite.destroy()
            self.transition_sprite = sge.Sprite.from_screenshot()
            self.transition_sprite.width = swidth
            self.transition_sprite.height = sheight
            self.transition_sprite.width = w
            self.transition_sprite.height = h

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
            room, then un-pixelate the second room.  If
            :attr:`sge.game.scale_smooth` is :const:`True`, the effect
            will instead be to blur and unblur the rooms.

        - ``sprite`` -- The sprite to use as the first image (the one
          being transitioned out of).  Generally should be a screenshot
          of the previous room.

        - ``duration`` -- The time the transition should take in
          milliseconds.

        """
        self.transition_update = {
            FADE: self.update_fade, DISSOLVE: self.update_dissolve,
            PIXELATE: self.update_pixelate
            }.setdefault(transition, lambda: None)
        self.transition_sprite = sprite
        self.transition_duration = duration
        self.transition_complete_last = 0

    def transition_start(self, transition=FADE, duration=3000):
        """Start the room, using a transition.

        See the documentation for :meth:`sge.Room.start` and
        :meth:`xsge.transition.Room.show_transition` for more
        information.

        """
        screenshot = sge.Sprite.from_screenshot()
        self.show_transition(transition, screenshot, duration)
        self.add(transition_obj)
        self.start()

    def transition_resume(self, transition=FADE, duration=3000):
        """Resume the room, using a transition.

        See the documentation for :meth:`sge.Room.resume` and
        :meth:`xsge.transition.Room.show_transition` for more
        information.

        """
        screenshot = sge.Sprite.from_screenshot()
        self.show_transition(transition, screenshot, duration)
        self.add(transition_obj)
        self.resume()

    def event_step(self, time_passed):
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
