#!/usr/bin/env python

# Copyright (C) 2013 Julian Marchant <onpon4@lavabit.com>
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

"""Pong

A simple two-player Pong game.

"""

import sge


class glob(object):

    player1 = None
    player2 = None
    ball = None
    paddle_sprite = None
    ball_sprite = None


class Game(sge.Game):

    def event_key_press(self, key):
        if key == 'escape':
            self.end()

        def event_close(self):
        self.end()


class Player(sge.StellarClass):

    def __init__(self, player=1):
        if player == 1:
            self.up_key = "w"
            self.down_key = "s"
            x = 32
            objname = "player1"
            glob.player1 = self
            self.hit_direction = 1
        else:
            self.up_key = "up"
            self.down_key = "down"
            x = sge.game.width - 32
            objname = "player2"
            glob.player2 = self
            self.hit_direction = -1

        y = sge.game.height / 2
        super(Player, self).__init__(x, y, 0, glob.paddle_sprite, id=objname)

    def event_step(self):
        self.yvelocity = (sge.game.get_key_pressed(self.down_key) -
                          sge.game.get_key_pressed(self.up_key)) * 5

        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom >= sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height - 1


class Ball(sge.StellarClass):

    def __init__(self):
        x = sge.game.width / 2
        y = sge.game.height / 2
        super(Ball, self).__init__(x, y, 1, glob.ball_sprite, id="ball")

    def serve(self, direction=1):
        self.x = self.xstart
        self.y = self.ystart
        self.xvelocity = 3 * direction
        self.yvelocity = 0

    def event_collision(self, other):
        if other is glob.player1:
            self.xvelocity = abs(xvelocity) + 0.5
        elif other is glob.player2:
            self.xvelocity = -abs(xvelocity) - 0.5




