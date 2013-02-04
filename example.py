#!/usr/bin/env python

# Copyright 2012 Julian Marchant <onpon4@gmail.com>
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


class glob(object):
    circle = None
    pop_sound = None


class Game(sge.Game):
    def event_key_press(self, key):
        if key == 'escape':
            self.end()

    def event_mouse_move(self, x, y):
        for obj in self.objects:
            if isinstance(self.objects[obj], Circle):
                if self.mouse.collides(self.objects[obj], x, y):
                    self.objects[obj].image_blend = "red"
                else:
                    self.objects[obj].image_blend = (0, 0, 255)

    def event_close(self):
        self.end()


class Circle(sge.StellarClass):
    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 5, 'circle', collision_ellipse=True)

    def event_destroy(self):
        CirclePop(self.x, self.y)
        assert glob.pop_sound is not None
        glob.pop_sound.play()


class CirclePop(sge.StellarClass):
    def __init__(self, x, y):
        super(CirclePop, self).__init__(x, y, 5, 'circle_pop')

    def event_animation_end(self):
        self.destroy()


def main():
    # Create Game object
    game = Game()

    # Load sprites
    circle_sprite = sge.Sprite('circle', 32, 32, 16, 16, True, bbox_x=-16,
                               bbox_y=-16)
    circle_pop_sprite = sge.Sprite('circle_pop', 32, 32, 16, 16, True,
                                   bbox_x=-16, bbox_y=-16)
    fence_sprite = sge.Sprite('fence', transparent=True)

    # Load backgrounds
    layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=False),)
    background = sge.Background(layers, 0xffffff)

    # Load sounds
    glob.pop_sound = sge.Sound('pop.wav')

    # Create objects
    glob.circle = Circle(game.width // 2, game.height // 2)
    objects = (glob.circle,)

    # Create view
    views = (sge.View(0, 0),)

    # Create rooms
    room1 = sge.Room(objects, views=views, background=background)

    game.start()


if __name__ == '__main__':
    main()
