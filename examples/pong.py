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
    hud_sprite = None
    hud_font = None


class Game(sge.Game):

    def event_key_press(self, key):
        if key == 'escape':
            self.end()

        def event_close(self):
        self.end()


class Player(sge.StellarClass):

    @property
    def score(self):
        return self.v_score

    @score.setter
    def score(self, value):
        if value != self.v_score:
            self.v_score = value
            refresh_hud()

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
        self.v_score = 0
        super(Player, self).__init__(x, y, 0, glob.paddle_sprite, id=objname)

    def event_step(self, time_passed):
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

    def event_create(self):
        self.serve()

    def event_step(self, time_passed):
        if self.bbox_right < -16:
            glob.player2.score += 1
            self.serve(1)
        elif self.bbox_left > sge.game.width + 16:
            glob.player1.score += 1
            self.serve(-1)

    def event_collision(self, other):
        if other is glob.player1:
            self.xvelocity = abs(xvelocity) + 0.5
        elif other is glob.player2:
            self.xvelocity = -abs(xvelocity) - 0.5

        self.yvelocity += (self.y - other.y) / 2

    def serve(self, direction=1):
        self.x = self.xstart
        self.y = self.ystart
        self.xvelocity = 3 * direction
        self.yvelocity = 0


def refresh_hud():
    glob.hud_sprite.draw_clear()
    x = glob.hud_sprite.width / 2
    glob.hud_sprite.draw_text(glob.hud_font, str(glob.player1.score), x - 8, 8,
                              color="white", halign=sge.ALIGN_RIGHT,
                              valign=sge.ALIGN_TOP)
    glob.hud_sprite.draw_text(glob.hud_font, str(glob.player2.score), x + 8, 8,
                              color="white", halign=sge.ALIGN_LEFT,
                              valign=sge.ALIGN_TOP)


def main():
    # Create Game object
    Game(640, 480, False, 0, True, False, 60, False)

    # Load sprites
    glob.paddle_sprite = sge.Sprite(width=8, height=48, origin_x=4,
                                    origin_y=24)
    glob.paddle_sprite.draw_rectangle(0, 0, 8, 48, "white")
    glob.ball_sprite = sge.Sprite(width=8, height=8, origin_x=4, origin_y=4)
    glob.ball_sprite.draw_rectangle(0, 0, 8, 8, "white")
    glob.hud_sprite = sge.Sprite(width=320, height=160, origin_x=160,
                                 origin_y=0)

    # Load backgrounds
    layers = (sge.BackgroundLayer(glob.ball_sprite, 320, 0, -10000,
                                  xrepeat=False),)
    background = sge.Background (layers, "black")

    # Load fonts
    glob.hud_font = sge.Font('Liberation Mono', 80)

    # Load sounds
    #TODO

    # Create objects
    Player(1)
    Player(2)
    glob.ball = Ball()
    hud = sge.StellarClass(320, 0, -10, glob.hud_sprite,
                           detects_collisions=False)
    objects = (glob.player1, glob.player2, glob.ball, hud)

    # Create view
    views = (sge.View(0, 0),)

    # Create rooms
    room1 = Room(objects, views=views, background=background)

    game.start()


if __name__ == '__main__':
    main()
