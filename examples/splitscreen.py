#!/usr/bin/env python

# Copyright 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

"""Split-screen Example

This is an example of split-screening being used, where two players see
two different parts of the room.

"""

import sge
import random


class Game(sge.Game):
    def event_key_press(self, key):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.StellarClass):
    def __init__(self, x, y, player=0):
        super(Circle, self).__init__(x, y, 1, sprite='circle', collision_precise=True)
        self.player = player
        self.normal_image_blend = ['red', 'blue', 'yellow', 'green'][self.player]
        self.image_alpha = 128

    def set_color(self):
        self.image_blend = self.normal_image_blend
        for obj in sge.game.current_room.objects:
            if (obj is not self and isinstance(obj, Circle) and
                    self.collides(obj)):
                self.image_blend = 'olive'
                break

    def event_create(self):
        self.set_color()

    def event_step(self, time_passed):
        left_key = ['left', 'a', 'j', 'kp_4'][self.player]
        right_key = ['right', 'd', 'l', 'kp_6'][self.player]
        up_key = ['up', 'w', 'i', 'kp_8'][self.player]
        down_key = ['down', 's', 'k', 'kp_5'][self.player]
        self.xvelocity = (sge.game.get_key_pressed(right_key) -
                          sge.game.get_key_pressed(left_key))
        self.yvelocity = (sge.game.get_key_pressed(down_key) -
                          sge.game.get_key_pressed(up_key))

        # Limit the circles to inside the room.
        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right >= sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width - 1
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom >= sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height - 1

        self.set_color()

        # Set view
        my_view = sge.game.current_room.views[self.player]
        my_view.x = self.x - (my_view.width // 2)
        my_view.y = self.y - (my_view.height // 2)


def main():
    # Create Game object
    Game(width=640, height=480)

    # Load sprites
    sge.Sprite('circle', 32, 32, 16, 16, transparent=True, bbox_x=-16, bbox_y=-16)
    fence = sge.Sprite('fence', transparent=True)

    # Load backgrounds
    layers = (sge.BackgroundLayer(fence, 0, 0, 0),)
    background = sge.Background(layers, 'white')

    # Create objects
    objects = []
    for i in xrange(4):
        circle = Circle(64, 64, i)
        objects.append(circle)

    # Create views
    views = []
    for x in xrange(2):
        for y in xrange(2):
            views.append(sge.View(0, 0, 320 * x, 240 * y, 320, 240))

    # Create rooms
    sge.Room(tuple(objects), 1280, 1024, tuple(views), background)

    sge.game.start()


if __name__ == '__main__':
    main()

