#!/usr/bin/env python

# Copyright 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

"""Stellar Game Engine example

This is a simple example of a possible game in Stellar Game Engine, just
to give a general idea of how it will be used.

"""

import sge
import random


class glob(object):
    font = None
    pop_sound = None
    music = None


class Game(sge.Game):
    def event_key_press(self, key):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.StellarClass):
    def __init__(self, x, y, player=0):
        super(Circle, self).__init__(x, y, 5, 'circle', collision_precise=True)
        self.player = player

    def event_create(self):
        self.image_alpha = 200
        self.image_blend = 'blue'

    def event_step(self, time_passed):
        left_key = ['left', 'a', 'j', 'kp_4'][self.player]
        right_key = ['right', 'd', 'l', 'kp_6'][self.player]
        up_key = ['up', 'w', 'i', 'kp_8'][self.player]
        down_key = ['down', 's', 'k', 'kp_5'][self.player]

        self.xvelocity = (sge.game.get_key_pressed(right_key) -
                          sge.game.get_key_pressed(left_key))
        self.yvelocity = (sge.game.get_key_pressed(down_key) -
                          sge.game.get_key_pressed(up_key))

        self.x += self.xvelocity
        self.y += self.yvelocity

        # Limit the circles to inside the room.
        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right >= sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width - 1
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom >= sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height - 1

def main():
    # Create Game object
    game = Game()

    # Load sprites
    circle_sprite = sge.Sprite('circle', 64, 64, 32, 32, True, bbox_x=-32,
                               bbox_y=-32)
    fence_sprite = sge.Sprite('fence', transparent=True)

    # Load backgrounds
    layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False),)
    background = sge.Background(layers, 0xffffff)

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
