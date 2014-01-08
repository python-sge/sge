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


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'f11':
            self.fullscreen = not self.fullscreen
        elif key == 'escape':
            self.event_close()

    def event_close(self):
        # TODO: Make a check for saving changes first.
        self.end()


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
