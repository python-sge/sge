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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sge


class glob(object):

    lives = 3
    score = 0


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
        super(Player, self).__init__(x, y, 10, 'player', '1945_playerplane',
                                     collision_precise=True)

    def event_create(self):
        self.can_shoot = True
        self.upgrade_level = 0
        self.shield = 10

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

        if self.can_shoot and sge.get_key_pressed('space'):
            self.shoot()

    def event_key_press(self, key):
        if key == 'space':
            # can_shoot is ignored, allowing a player to shoot faster by
            # pressing the space bar repeatedly.
            self.shoot()

    def event_alarm(self, alarm_id):
        if alarm_id == 'shoot':
            self.can_shoot = True

    def event_collision(self, other):
        if isinstance(other, Enemy):
            self.hurt()

    def shoot(self):
        self.can_shoot = False
        self.set_alarm('shoot', 30)

        sge.create_object(PlayerBullet, self.x - 5, self.y, 0)
        sge.create_object(PlayerBullet, self.x + 5, self.y, 0)

        if self.upgrade_level >= 1:
            sge.create_object(PlayerBullet, self.x, self.y, 90)
            sge.create_object(PlayerBullet, self.x, self.y, -90)

        if self.upgrade_level >= 2:
            sge.create_object(PlayerBullet, self.x, self.y, 180)

        if self.upgrade_level >= 3:
            sge.create_object(PlayerBullet, self.x, self.y, 45)
            sge.create_object(PlayerBullet, self.x, self.y, -45)

    def hurt(self):
        if self.shield > 0:
            self.shield -= 1
        else:
            self.kill()

    def kill(self):
        if self.lives > 0:
            self.lives -= 1
            # TODO: Destroy ship
        else:
            # TODO: game over
            pass


class PlayerBullet(sge.StellarClass):

    def __init__(self, x, y, rotation=0):
        super(PlayerBullet, self).__init__(x, y, 3, sprite='1945_playerbullet',
                                           collision_precise=True)
        self.speed = 12
        self.move_direction = rotation + 90
        self.image_rotation = rotation


class Enemy(sge.StellarClass):

    pass
