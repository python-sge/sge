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

import math

import sge


class glob(object):

    player = None
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
        glob.player = self
        super(Player, self).__init__(x, y, 10, 'player', '1945_playerplane',
                                     collision_precise=True)

    def event_create(self):
        self.can_shoot = True
        self.upgrade_level = 0
        self.shield = 10
        self.exploding = False

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
        if not self.exploding:
            if isinstance(other, Enemy):
                self.hurt()
                other.kill()

    def event_animation_end(self):
        if self.exploding:
            self.exploding = False
            self.sprite = '1945_playerplane'
            self.x = self.xstart
            self.y = self.ystart
            self.shield = 10

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
            self.exploding = True
            self.sprite = '1945_explosion_large'
            self.image_index = 0
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

    def kill(self):
        pass


class EnemyBullet(Enemy):

    def __init__(self, x, y, xvelocity=0, yvelocity=12):
        super(EnemyBullet, self).__init__(x, y, 2, sprite='1945_enemybullet',
                                          collision_precise=True)


class EnemyPlane(Enemy):

    sprite_normal = "1945_enemyplane_green"
    sprite_flipping = "1945_enemyplane_green_flip"
    sprite_flipped = "1945_enemyplane_green_flipped"
    retreats = True
    follows_player = False
    directional_guns = False
    shoot_delay = 45

    def __init__(self, x, y):
        super(EnemyPlane, self).__init__(x, y, 5, sprite=self.sprite_normal,
                                         collision_precise=True, yvelocity=8)

    def retreat(self):
        self.retreating = True
        self.turning = True
        self.sprite = self.sprite_flipping
        self.image_index = 0
        self.image_rotation = 0
        self.xvelocity = 0
        self.yvelocity = 0

    def event_create(self):
        self.retreating = False
        self.turning = False
        self.set_alarm('shoot', self.shoot_delay)

    def event_step(self, time_passed):
        if not self.retreating:
            if self.retreats and self.y >= game.height - 32:
                self.retreat()
            elif self.follows_player:
                if self.y < glob.player.y and self.x != glob.player.x:
                    d = (glob.player.x - self.x) / abs(glob.player.x - self.x)
                    self.image_rotation = 45 * d
                    self.xvelocity = 5.7 * d
                    self.yvelocity = 5.7
                else:
                    self.image_rotation = 0
                    self.xvelocity = 0
                    self.yvelocity = 8

    def event_alarm(self, alarm_id):
        if alarm.id == 'shoot':
            self.shoot()
            self.set_alarm('shoot', self.shoot_delay)

    def event_animation_end(self):
        if self.turning:
            self.turning = False
            self.sprite = self.sprite_flipped
            self.image_index = 0
            self.yvelocity = -8

    def shoot(self):
        if self.directional_guns:
            xdistance = glob.player.x - self.x
            ydistance = glob.player.y - self.y
            h = math.sqrt(xdistance ** 2 + ydistance ** 2)
            xvelocity = 12 * xdistance / h
            yvelocity = 12 * ydistance / h
        else:
            xvelocity = 0
            yvelocity = 12

        EnemyBullet.create(self.x, self.y, xvelocity, yvelocity)
