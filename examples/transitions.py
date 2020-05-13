#!/usr/bin/env python3

# Transitions example
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


class glob(object):

    font = None
    pop_sound = None
    music = None
    rooms = []


class Game(sge.dsp.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.dsp.Object):

    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 5, sprite=glob.circle_sprite,
                                     collision_precise=True)

    def event_create(self):
        self.image_alpha = 200
        if self.collision(sge.game.mouse):
            self.image_blend = sge.gfx.Color('#ff0000')
        else:
            self.image_blend = sge.gfx.Color('blue')

    def event_mouse_move(self, x, y):
        if self.collision(sge.game.mouse):
            self.image_blend = sge.gfx.Color("red")
        else:
            self.image_blend = sge.gfx.Color((0, 0, 255))

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


class CirclePop(sge.dsp.Object):

    def __init__(self, x, y):
        super(CirclePop, self).__init__(x, y, 5, sprite=glob.circle_pop_sprite,
                                        tangible=False)

    def event_animation_end(self):
        self.destroy()

    def event_destroy(self):
        circle = Circle(random.randint(0, sge.game.width),
                        random.randint(0, sge.game.height))
        sge.game.current_room.add(circle)


class Room(sge.dsp.Room):

    def __init__(self, text, objects=(), views=None, background=None):
        self.text = text
        super(Room, self).__init__(objects, views=views, background=background)

    def event_room_start(self):
        self.event_room_resume()

    def event_room_resume(self):
        sge.game.window_text = self.text
        glob.music.play(loops=None)

    def event_key_press(self, key, char):
        next_room = glob.rooms[(glob.rooms.index(self) + 1) % len(glob.rooms)]
        if key == "space":
            next_room.start()
        elif key == "1":
            next_room.start(transition="fade")
        elif key == "2":
            next_room.start(transition="dissolve")
        elif key == "3":
            next_room.start(transition="pixelate")
        elif key == "4":
            next_room.start(transition="wipe_left")
        elif key == "5":
            next_room.start(transition="wipe_right")
        elif key == "6":
            next_room.start(transition="wipe_up")
        elif key == "7":
            next_room.start(transition="wipe_down")
        elif key == "8":
            next_room.start(transition="wipe_upleft")
        elif key == "9":
            next_room.start(transition="wipe_upright")
        elif key == "0":
            next_room.start(transition="wipe_downleft")
        elif key == "q":
            next_room.start(transition="wipe_downright")
        elif key == "w":
            next_room.start(transition="wipe_matrix")
        elif key == "e":
            next_room.start(transition="iris_in")
        elif key == "r":
            next_room.start(transition="iris_out")


def main():
    # Create Game object
    game = Game(collision_events_enabled=False)

    # Load sprites
    glob.circle_sprite = sge.gfx.Sprite('circle', DATA, width=64, height=64,
                                        origin_x=32, origin_y=32)
    glob.circle_pop_sprite = sge.gfx.Sprite('circle_pop', DATA, width=64,
                                            height=64, origin_x=32,
                                            origin_y=32, fps=60)
    fence_sprite = sge.gfx.Sprite('fence', DATA)

    # Load backgrounds
    layers = [sge.gfx.BackgroundLayer(fence_sprite, 0, 380, repeat_left=True,
                                      repeat_right=True)]
    layers2 = [sge.gfx.BackgroundLayer(fence_sprite, 0, 0, repeat_left=True,
                                       repeat_right=True, repeat_up=True,
                                       repeat_down=True)]
    background = sge.gfx.Background(layers, sge.gfx.Color(0xffffff))
    background2 = sge.gfx.Background(layers2, sge.gfx.Color('white'))

    # Load fonts
    glob.font = sge.gfx.Font('Liberation Serif', 20)

    # Load sounds
    glob.pop_sound = sge.snd.Sound(os.path.join(DATA, 'pop.ogg'))
    
    # Load music
    glob.music = sge.snd.Music(os.path.join(DATA, 'WhereWasI.ogg'))

    # Create objects
    circle = Circle(game.width // 2, game.height // 2)
    circle2 = Circle(22, 48)
    circle3 = Circle(486, 301)
    circle4 = Circle(50, 400)
    circle5 = Circle(game.width // 2, game.height // 2)
    circle6 = Circle(52, 120)
    objects = [circle, circle2, circle3, circle4]
    objects2 = [circle5, circle6]

    # Create view
    views = [sge.dsp.View(0, 0)]

    # Create rooms
    room1 = Room('I am the first room!', objects, views=views, background=background)
    room2 = Room('Second room on the house!', objects2, background=background2)
    room3 = Room('I am the third room!', objects, views=views, background=background)
    room4 = Room('Fourth room on the house!', objects2, background=background2)
    room5 = Room('I am the fifth room!', objects, views=views, background=background)
    room6 = Room('Sixth room on the house!', objects2, background=background2)
    glob.rooms = [room1, room2, room3, room4, room5, room6]

    game.start_room = room1

    game.start()


if __name__ == '__main__':
    main()
