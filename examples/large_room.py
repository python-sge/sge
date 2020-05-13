#!/usr/bin/env python3

# Large Room Example
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
        elif key == "backspace":
            view = self.current_room.views[0]
            view.width = view.wport
            view.height = view.hport

    def event_close(self):
        self.end()


class Circle(sge.dsp.Object):
    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 1, sprite=circle_sprite,
                                     collision_precise=True,
                                     image_blend=sge.gfx.Color("red"),
                                     image_alpha=128)

    def event_step(self, time_passed, delta_mult):
        left_key = 'left'
        right_key = 'right'
        up_key = 'up'
        down_key = 'down'
        self.xvelocity = (sge.keyboard.get_pressed(right_key) -
                          sge.keyboard.get_pressed(left_key))
        self.yvelocity = (sge.keyboard.get_pressed(down_key) -
                          sge.keyboard.get_pressed(up_key))

        # Limit the circles to inside the room.
        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right >= sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width - 1
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom >= sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height - 1

        # Set view
        my_view = sge.game.current_room.views[0]
        zoom_add = (sge.keyboard.get_pressed("hyphen") -
                    sge.keyboard.get_pressed("equals"))
        my_view.width += zoom_add
        my_view.width = max(48, min(my_view.width, sge.game.current_room.width))
        my_view.height = my_view.width
        my_view.x = self.x - (my_view.width // 2)
        my_view.y = self.y - (my_view.height // 2)


def main():
    global circle_sprite

    # Create Game object
    Game(width=240, height=240, scale_method="smooth",
         collision_events_enabled=False)

    # Load sprites
    circle_sprite = sge.gfx.Sprite('circle', DATA, width=32, height=32,
                                   origin_x=16, origin_y=16)
    fence = sge.gfx.Sprite('fence', DATA)

    # Load backgrounds
    layers = [sge.gfx.BackgroundLayer(fence, 0, 0, 0, repeat_left=True,
                                      repeat_right=True, repeat_up=True,
                                      repeat_down=True)]
    background = sge.gfx.Background(layers, sge.gfx.Color('white'))

    # Create objects
    circle = Circle(random.randrange(0, 640), random.randrange(0, 480))
    objects =  [circle]

    # Create views
    views = [sge.dsp.View(0, 0, 0, 0, 240, 240, 240, 240)]

    # Create rooms
    sge.game.start_room = sge.dsp.Room(objects, 640, 640, views=views,
                                       background=background)

    sge.game.start()


if __name__ == '__main__':
    main()

