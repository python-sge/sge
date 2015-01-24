#!/usr/bin/env python3

# Circle Popper
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

import os
import random

import sge


DATA = os.path.join(os.path.dirname(__file__), "data")


class glob(object):

    circle_sprite = None
    circle_pop_sprite = None
    font = None
    pop_sound = None
    music = None


class Game(sge.Game):

    def event_game_start(self):
        self.fps_time = 0
        self.fps_frames = 0
        self.fps_text = ""

    def event_step(self, time_passed, delta_mult):
        self.fps_time += time_passed
        self.fps_frames += 1
        if self.fps_time >= 250:
            self.fps_text = str(round((1000 * self.fps_frames) /
                                      self.fps_time))
            self.fps_time = 0
            self.fps_frames = 0

        self.project_text(glob.font, self.fps_text, self.width - 8, 8,
                          halign="right")

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Circle(sge.Object):

    def __init__(self, x, y):
        super(Circle, self).__init__(x, y, 5, sprite=glob.circle_sprite,
                                     collision_precise=True)

    def event_create(self):
        self.image_alpha = 200
        if self.collision(sge.game.mouse):
            self.image_blend = sge.Color('#ff0000')
        else:
            self.image_blend = sge.Color('blue')

    def event_mouse_move(self, x, y):
        if self.collision(sge.game.mouse):
            self.image_blend = sge.Color("red")
        else:
            self.image_blend = sge.Color((0, 0, 255))

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


class CirclePop(sge.Object):

    def __init__(self, x, y):
        super(CirclePop, self).__init__(x, y, 5, sprite=glob.circle_pop_sprite,
                                        tangible=False)

    def event_animation_end(self):
        self.destroy()

    def event_destroy(self):
        circle = Circle(random.randint(0, sge.game.width),
                        random.randint(0, sge.game.height))
        sge.game.current_room.add(circle)


class Room(sge.Room):

    def event_room_start(self):
        self.shake = 0
        self.event_room_resume()

    def event_room_resume(self):
        glob.music.play(loops=None)

    def event_step(self, time_passed, delta_mult):
        self.project_rectangle(5, 5, 3, 32, 32, fill=sge.Color("red"),
                               outline=sge.Color("green"), outline_thickness=3)
        self.project_ellipse(16, 100, 3, 64, 64, fill=sge.Color("yellow"),
                             outline=sge.Color("fuchsia"), outline_thickness=4)
        self.project_line(64, 64, 78, 100, 3, sge.Color("black"), thickness=2)
        self.project_dot(90, 32, 3, sge.Color("maroon"))
        self.project_dot(91, 32, 3, sge.Color("maroon"))
        self.project_dot(92, 32, 3, sge.Color("maroon"))
        self.project_dot(93, 32, 3, sge.Color("maroon"))
        self.project_dot(90, 33, 3, sge.Color("maroon"))
        self.project_dot(91, 33, 3, sge.Color("maroon"))
        self.project_dot(92, 33, 3, sge.Color("maroon"))
        self.project_dot(90, 34, 3, sge.Color("maroon"))
        self.project_dot(91, 34, 3, sge.Color("maroon"))
        self.project_dot(90, 35, 3, sge.Color("maroon"))
        text = "I am amazing text!\n\nYaaaaaaaaaaay~!"
        self.project_text(glob.font, text, 320, 0, 3, color=sge.Color("black"),
                          halign="center")

        if sge.keyboard.get_pressed("left"):
            self.views[0].xport -= 1
        if sge.keyboard.get_pressed("right"):
            self.views[0].xport += 1
        if sge.keyboard.get_pressed("up"):
            self.views[0].yport -= 1
        if sge.keyboard.get_pressed("down"):
            self.views[0].yport += 1

    def event_alarm(self, alarm_id):
        if alarm_id == "shake":
            self.views[0].xport += random.uniform(-2, 2)
            self.views[0].yport += random.uniform(-2, 2)
            self.shake -= 1
            if self.shake > 0:
                self.alarms["shake"] = 1
            else:
                self.views[0].xport = 0
                self.views[0].yport = 0
        elif alarm_id == "shake_down":
            self.views[0].yport = 3
            self.alarms["shake_up"] = 1
        elif alarm_id == "shake_up":
            self.views[0].yport = 0
            self.shake -= 1
            if self.shake > 0:
                self.alarms["shake_down"] = 1

    def event_key_press(self, key, char):
        if key in ("ctrl_left", "ctrl_right"):
            self.shake = 20
            self.event_alarm("shake_down")
        elif key in ("shift_left", "shift_right"):
            self.shake = 20
            self.event_alarm("shake")


def main():
    # Create Game object
    game = Game(delta=True, collision_events_enabled=False)

    # Load sprites
    glob.circle_sprite = sge.Sprite('circle', DATA, width=64, height=64,
                                    origin_x=32, origin_y=32)
    glob.circle_pop_sprite = sge.Sprite('circle_pop', DATA, width=64,
                                        height=64, origin_x=32, origin_y=32,
                                        fps=60)
    fence_sprite = sge.Sprite('fence', DATA)

    # Load backgrounds
    layers = [sge.BackgroundLayer(fence_sprite, 0, 380, 0, repeat_left=True,
                                  repeat_right=True)]
    background = sge.Background(layers, sge.Color(0xffffff))

    # Load fonts
    glob.font = sge.Font('Liberation Serif', 20)

    # Load sounds
    glob.pop_sound = sge.Sound(os.path.join(DATA, 'pop.ogg'))
    
    # Load music
    glob.music = sge.Music(os.path.join(DATA, 'WhereWasI.ogg'))

    # Create objects
    circle = Circle(game.width // 2, game.height // 2)
    circle2 = Circle(22, 48)
    circle3 = Circle(486, 301)
    circle4 = Circle(50, 400)
    objects = [circle, circle2, circle3, circle4]

    # Create view
    views = [sge.View(0, 0)]

    # Create rooms
    game.start_room = Room(objects, views=views, background=background)

    game.start()


if __name__ == '__main__':
    main()
