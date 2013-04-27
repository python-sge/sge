#!/usr/bin/env python

# Copyright (C) 2013 Julian Marchant <onpon4@lavabit.com>
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

"""1945

A scrolling shooter in the style of 1943.

"""

import sge


class Game(sge.Game):

    def event_key_press(self, key):
        if key == 'escape':
            self.end()
        elif key == 'p':
            self.pause()

    def event_close(self):
        self.end()

    def event_paused_key_press(self, key):
        if key == 'escape':
            self.end()
        else:
            self.unpause()

    def event_paused_close(self):
        self.end()


class Player(sge.StellarClass):

    def __init__(self):
        self.up_key = 'up'
        self.down_key = 'down'
        self.left_key = 'left'
        self.right_key = 'right'
        x = sge.game.width / 2
        y = sge.game.height - 64
        super(Player, self).__init__(x, y, 10, 'player', '1945_playerplane')

    def event_step(self, time_passed):
        self.xvelocity = (sge.get_key_pressed(self.right_key) -
                          sge.get_key_pressed(self.left_key)) * 6
        self.yvelocity = (sge.get_key_pressed(self.down_key) -
                          sge.get_key_pressed(self.up_key))

        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right > sge.game.width:
            self.bbox_right = sge.game.width
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom > sge.game.height:
            self.bbox_bottom = sge.game.height
