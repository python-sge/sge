#!/usr/bin/env python

# Circle Popper
# Written in 2012, 2013 by Julian Marchant <onpon4@lavabit.com>
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.


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
    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.StellarClass):
    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 5, sprite='circle',
                                     collision_precise=True)

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
        if button == 'left':
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
    def event_room_start(self):
        glob.music.play(loops=None)

    def event_step(self, time_passed):
        text = "I am amazing text!\n\nYaaaaaaaaaaay~!"
        self.project_text(glob.font, text, 320, 0, 3, color="black",
                          halign=sge.ALIGN_CENTER)


def main():
    # Create Game object
    game = Game(delta=True)

    # Load sprites
    circle_sprite = sge.Sprite('circle', width=64, height=64, origin_x=32,
                               origin_y=32)
    circle_pop_sprite = sge.Sprite('circle_pop', width=64, height=64,
                                   origin_x=32, origin_y=32, fps=60)
    fence_sprite = sge.Sprite('fence')

    # Load backgrounds
    layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False),)
    background = sge.Background(layers, 0xffffff)

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
    objects = (circle, circle2, circle3, circle4)

    # Create view
    views = (sge.View(0, 0),)

    # Create rooms
    room1 = Room(objects, views=views, background=background)

    game.start()


if __name__ == '__main__':
    main()
