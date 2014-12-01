#!/usr/bin/env python3

# Rotation Example
# Written in 2012, 2013, 2014 by Julian Marchant <onpon4@riseup.net>
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
import random


class Game(sge.Game):
    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.Object):
    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 5, sprite=rotator_sprite,
                                     regulate_origin=True,
                                     collision_precise=True)

    def event_create(self):
        self.image_alpha = 200
        if self.collision(sge.game.mouse):
            self.image_blend = sge.Color('#ff0000')
        else:
            self.image_blend = sge.Color('blue')

        if random.random() < 0.5:
            self.image_xscale = 2
            self.image_yscale = 2

    def event_step(self, time_passed, delta_mult):
        self.image_rotation += 2 * delta_mult
        sge.game.current_room.project_circle(self.x, self.y, self.z + 1, 8,
                                             outline=sge.Color("green"))

        if self.collision(sge.game.mouse):
            self.image_blend = sge.Color("red")
        else:
            self.image_blend = sge.Color((0, 0, 255))


def main():
    global rotator_sprite

    # Create Game object
    game = Game(delta=True, collision_events_enabled=False)

    # Load sprites
    rotator_sprite = sge.Sprite('rotator')
    fence_sprite = sge.Sprite('fence')

    # Load backgrounds
    layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False),)
    background = sge.Background(layers, sge.Color(0xffffff))

    # Create objects
    circle = Circle(game.width // 2, game.height // 2)
    circle2 = Circle(22, 48)
    circle3 = Circle(486, 301)
    circle4 = Circle(50, 400)
    objects = (circle, circle2, circle3, circle4)

    # Create view
    views = (sge.View(0, 0),)

    # Create rooms
    game.start_room = sge.Room(objects, views=views, background=background)

    game.start()


if __name__ == '__main__':
    main()
