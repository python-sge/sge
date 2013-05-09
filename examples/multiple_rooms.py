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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

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
    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 5, sprite='circle', collision_precise=True)

    def event_create(self):
        self.image_alpha = 200
        if self.collides(sge.game.mouse):
            self.image_blend = '#ff0000'
        else:
            self.image_blend = 'blue'

    def event_mouse_move(self, x, y):
        if self.collides(sge.game.mouse):
            self.image_blend = "red"
        else:
            self.image_blend = (0, 0, 255)

    def event_mouse_button_press(self, button):
        if button == sge.MOUSE_BUTTON_LEFT:
            if self.collides(sge.game.mouse):
                self.destroy()

    def event_destroy(self):
        pop = CirclePop(self.x, self.y)
        pop.image_blend = self.image_blend
        sge.game.current_room.add(pop)
        assert glob.pop_sound is not None
        glob.pop_sound.play()


class CirclePop(sge.StellarClass):
    def __init__(self, x, y):
        super(CirclePop, self).__init__(x, y, 5, sprite='circle_pop')

    def event_animation_end(self):
        self.destroy()

    def event_destroy(self):
        circle = Circle(random.randint(0, sge.game.width),
                        random.randint(0, sge.game.height))
        sge.game.current_room.add(circle)


class Room(sge.Room):
    def __init__(self, text, objects=(), views=None, background=None):
        self.text = text
        super(Room, self).__init__(objects, views=views, background=background)

    def event_room_start(self):
        glob.music.play(loops=None)

    def event_key_press(self, key):
        if key == 'space':
            self.end()


def main():
    # Create Game object
    game = Game()

    # Load sprites
    circle_sprite = sge.Sprite('circle', 64, 64, 32, 32, True, bbox_x=-32,
                               bbox_y=-32)
    circle_pop_sprite = sge.Sprite('circle_pop', 64, 64, 32, 32, True,
                                   bbox_x=-16, bbox_y=-16, fps=60)
    fence_sprite = sge.Sprite('fence', transparent=True)

    # Load backgrounds
    layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False),)
    layers2 = (sge.BackgroundLayer(fence_sprite, 0, 0, 0),)
    background = sge.Background(layers, 0xffffff)
    background2 = sge.Background(layers2, 'white')

    # Load fonts
    glob.font = sge.Font('Liberation Serif', 20)

    # Load sounds
    glob.pop_sound = sge.Sound('pop.ogg')
    
    # Load music
    glob.music = sge.Music('WhereWasI.ogg')

    # Create objects
    circle = Circle(game.width // 2, game.height // 2)
    circle2 = Circle(22, 48)
    circle3 = Circle(486, 301)
    circle4 = Circle(50, 400)
    circle5 = Circle(game.width // 2, game.height // 2)
    circle6 = Circle(52, 120)
    objects = (circle, circle2, circle3, circle4)
    objects2 = (circle5, circle6)

    # Create view
    views = (sge.View(0, 0),)

    # Create rooms
    room1 = Room('I am the first room!', objects, views=views, background=background)
    room2 = Room('Second room on the house!', objects2, background=background2)

    game.start()


if __name__ == '__main__':
    main()
