#!/usr/bin/env python3

# Rotation Example
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.


import os
import random

import sge


DATA = os.path.join(os.path.dirname(__file__), "data")


class Game(sge.dsp.Game):
    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.dsp.Object):
    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 5, sprite=rotator_sprite,
                                     regulate_origin=True,
                                     collision_precise=True)

    def event_create(self):
        self.image_alpha = 200
        if self.collision(sge.game.mouse):
            self.image_blend = sge.gfx.Color('#ff0000')
        else:
            self.image_blend = sge.gfx.Color('blue')

        if random.random() < 0.5:
            self.image_xscale = 2
            self.image_yscale = 2

    def event_step(self, time_passed, delta_mult):
        self.image_rotation += delta_mult
        sge.game.current_room.project_circle(self.x, self.y, self.z + 1, 8,
                                             outline=sge.gfx.Color("green"))

        if self.collision(sge.game.mouse):
            self.image_blend = sge.gfx.Color("red")
        else:
            self.image_blend = sge.gfx.Color((0, 0, 255))


def main():
    global rotator_sprite

    # Create Game object
    game = Game(delta=True, collision_events_enabled=False)

    # Load sprites
    rotator_sprite = sge.gfx.Sprite('rotator', DATA)
    fence_sprite = sge.gfx.Sprite('fence', DATA)

    # Load backgrounds
    layers = [sge.gfx.BackgroundLayer(fence_sprite, 0, 380, 0,
                                      repeat_left=True, repeat_right=True)]
    background = sge.gfx.Background(layers, sge.gfx.Color(0xffffff))

    # Create objects
    circle = Circle(game.width // 2, game.height // 2)
    circle2 = Circle(22, 48)
    circle3 = Circle(486, 301)
    circle4 = Circle(50, 400)
    objects = (circle, circle2, circle3, circle4)

    # Create view
    views = [sge.dsp.View(0, 0)]

    # Create rooms
    game.start_room = sge.dsp.Room(objects, views=views, background=background)

    game.start()


if __name__ == '__main__':
    main()
