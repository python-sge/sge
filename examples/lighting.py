#!/usr/bin/env python3

# Lighting Example
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


class glob(object):

    darkness_sprite = None


class Game(sge.Game):
    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.StellarClass):
    def __init__(self, x, y, player=0):
        super(Circle, self).__init__(x, y, 5, sprite='circle',
              collision_precise=True)
        self.player = player

    def event_create(self):
        self.image_alpha = 200
        self.image_blend = sge.Color('blue')

        self.darkness = sge.StellarClass(0, 0, 10000, sprite='darkness',
                                         tangible=False)
        sge.game.current_room.add(self.darkness)

    def event_step(self, time_passed, delta_mult):
        left_key = ['left', 'a', 'j', 'kp_4'][self.player]
        right_key = ['right', 'd', 'l', 'kp_6'][self.player]
        up_key = ['up', 'w', 'i', 'kp_8'][self.player]
        down_key = ['down', 's', 'k', 'kp_5'][self.player]

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

        # Light up part of the room
        glob.darkness_sprite.draw_rectangle(0, 0, sge.game.width,
                                            sge.game.height,
                                            fill=sge.Color("black"))
        glob.darkness_sprite.draw_sprite('light', 0, self.x, self.y,
                                         blend_mode=sge.BLEND_RGBA_SUBTRACT)

def main():
    # Create Game object
    game = Game(collision_events_enabled=False)

    # Load sprites
    circle_sprite = sge.Sprite('circle', width=32, height=32, origin_x=16,
                               origin_y=16)
    fence_sprite = sge.Sprite('fence')
    light_sprite = sge.Sprite('light', width=128, height=128, origin_x=64,
                              origin_y=64)

    glob.darkness_sprite = sge.Sprite(ID='darkness', width=sge.game.width,
                                      height=sge.game.height)
    glob.darkness_sprite.draw_rectangle(0, 0, sge.game.width, sge.game.height,
                                        fill=sge.Color("black"))

    # Load backgrounds
    layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False),)
    background = sge.Background(layers, sge.Color(0xffffff))

    # Create objects
    circle = Circle(game.width // 2, game.height // 2)
    objects = [circle]

    # Create view
    views = (sge.View(0, 0),)

    # Create rooms
    room1 = sge.Room(tuple(objects), views=views, background=background)

    game.start()


if __name__ == '__main__':
    main()
