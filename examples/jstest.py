#!/usr/bin/env python2

# Joystick Tester
# Written in 2014 by Julian Marchant <onpon4@riseup.net>
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sge


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.event_close()

    def event_close(self):
        self.end()


class Room(sge.Room):

    def set_joystick(self):
        self.joystick_axes = []
        for i in xrange(sge.get_joystick_axes(self.current_joystick)):
            self.joystick_axes.append(sge.get_joystick_axis(
                self.current_joystick, i))

        self.joystick_hats = []
        for i in xrange(sge.get_joystick_hats(self.current_joystick)):
            self.joystick_hats.append(sge.get_joystick_hat(
                self.current_joystick, i))

        self.joystick_balls = []
        for i in xrange(sge.get_joystick_trackballs(self.current_joystick)):
            self.joystick_balls.append(0)

        self.joystick_buttons = []
        for i in xrange(sge.get_joystick_buttons(self.current_joystick)):
            self.joystick_buttons.append(sge.get_joystick_button_pressed(
                self.current_joystick, i))
    
    def event_room_start(self):
        self.current_joystick = 0
        self.set_joystick()
