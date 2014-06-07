#!/usr/bin/env python3

# Multiple Rooms Example
# Written in 2012, 2013, 2014 by Julian Marchant <onpon4@riseup.net>
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

import random

import sge
from xsge import transition


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
        super().__init__(x, y, 5, sprite='circle', collision_precise=True)

    def event_create(self):
        self.image_alpha = 200
        if self.collision(sge.game.mouse):
            self.image_blend = '#ff0000'
        else:
            self.image_blend = 'blue'

    def event_mouse_move(self, x, y):
        if self.collision(sge.game.mouse):
            self.image_blend = "red"
        else:
            self.image_blend = (0, 0, 255)

    def event_mouse_button_press(self, button):
        if button == 'left':
            if self.collision(sge.game.mouse):
                self.destroy()

    def event_destroy(self):
        pop = CirclePop(self.x, self.y)
        pop.image_blend = self.image_blend
        sge.game.current_room.add(pop)
        assert glob.pop_sound is not None
        glob.pop_sound.play()


class CirclePop(sge.StellarClass):
    def __init__(self, x, y):
        super().__init__(x, y, 5, sprite='circle_pop')

    def event_animation_end(self):
        self.destroy()

    def event_destroy(self):
        circle = Circle(random.randint(0, sge.game.width),
                        random.randint(0, sge.game.height))
        sge.game.current_room.add(circle)


class Room(transition.Room):
    def __init__(self, text, objects=(), views=None, background=None):
        self.text = text
        super().__init__(objects, views=views, background=background)

    def event_room_start(self):
        super().event_room_start()
        self.event_room_resume()

    def event_room_resume(self):
        glob.music.play(loops=None)

    def event_key_press(self, key, char):
        if key == "1":
            self.transition_end(transition=transition.FADE)
        elif key == "2":
            self.transition_end(transition=transition.DISSOLVE)
        elif key == "3":
            self.transition_end(transition=transition.PIXELATE)


def main():
    # Create Game object
    game = Game()

    # Load sprites
    circle_sprite = sge.Sprite('circle', width=64, height=64, origin_x=32,
                               origin_y=32)
    circle_pop_sprite = sge.Sprite('circle_pop', width=64, height=64,
                                   origin_x=32, origin_y=32, fps=60)
    fence_sprite = sge.Sprite('fence')

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
