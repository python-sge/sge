#!/usr/bin/env python3

# Pong Example
# Written in 2013, 2014 by Julian Marchant <onpon4@riseup.net>
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""Pong

A simple two-player Pong game.

"""

import sge

PADDLE_SPEED = 4
PADDLE_VERTICAL_FORCE = 1 / 12
BALL_START_SPEED = 2
BALL_ACCELERATION = 0.2
BALL_MAX_SPEED = 15
POINTS_TO_WIN = 10
TEXT_OFFSET = 16


class glob(object):

    # This class is for global variables.  While not necessary, using a
    # container class like this is less potentially confusing than using
    # actual global variables.

    player1 = None
    player2 = None
    ball = None
    hud_sprite = None
    bounce_sound = None
    bounce_wall_sound = None
    score_sound = None
    game_in_progress = True


class Game(sge.Game):

    def event_game_start(self):
        self.mouse.visible = False

    def event_key_press(self, key, char):
        if key == 'f8':
            sge.Sprite.from_screenshot().save('screenshot.jpg')
        elif key == 'f11':
            self.fullscreen = not self.fullscreen
        elif key == 'escape':
            self.event_close()
        elif key in ('p', 'enter'):
            if glob.game_in_progress:
                self.pause()
            else:
                glob.game_in_progress = True
                self.current_room.start()

    def event_close(self):
        m = "Are you sure you want to quit?"
        if sge.show_message(m, ("No", "Yes")):
            self.end()

    def event_paused_key_press(self, key, char):
        if key == 'escape':
            # This allows the player to still exit while the game is
            # paused, rather than having to unpause first.
            self.event_close()
        else:
            self.unpause()

    def event_paused_close(self):
        # This allows the player to still exit while the game is paused,
        # rather than having to unpause first.
        self.event_close()


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
            self.joystick = 0
            self.up_key = "w"
            self.down_key = "s"
            x = 32
            glob.player1 = self
            self.hit_direction = 1
        else:
            self.joystick = 1
            self.up_key = "up"
            self.down_key = "down"
            x = sge.game.width - 32
            glob.player2 = self
            self.hit_direction = -1

        y = sge.game.height / 2
        super().__init__(x, y, 0, sprite="paddle")

    def event_create(self):
        self.v_score = 0
        self.trackball_motion = 0

    def event_step(self, time_passed, delta_mult):
        # Movement
        key_motion = (sge.get_key_pressed(self.down_key) -
                      sge.get_key_pressed(self.up_key))
        axis_motion = sge.get_joystick_axis(self.joystick, 1)

        if (abs(axis_motion) > abs(key_motion) and
                abs(axis_motion) > abs(self.trackball_motion)):
            self.yvelocity = axis_motion * PADDLE_SPEED
        elif (abs(self.trackball_motion) > abs(key_motion) and
              abs(self.trackball_motion) > abs(axis_motion)):
            self.yvelocity = self.trackball_motion * PADDLE_SPEED
        else:
            self.yvelocity = key_motion * PADDLE_SPEED

        self.trackball_motion = 0

        # Keep the paddle inside the window
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom > sge.game.height:
            self.bbox_bottom = sge.game.height

    def event_joystick_trackball_move(self, joystick, ball, x, y):
        if joystick == self.joystick:
            if abs(y) > abs(self.trackball_motion):
                self.trackball_motion = y


class Ball(sge.StellarClass):

    def __init__(self):
        x = sge.game.width / 2
        y = sge.game.height / 2
        super().__init__(x, y, 1, sprite="ball")

    def event_create(self):
        refresh_hud()
        self.serve()

    def event_step(self, time_passed, delta_mult):
        # Scoring
        if self.bbox_right < 0:
            glob.player2.score += 1
            glob.score_sound.play()
            self.serve(-1)
        elif self.bbox_left > sge.game.width:
            glob.player1.score += 1
            glob.score_sound.play()
            self.serve(1)

        # Bouncing off of the edges
        if self.bbox_bottom > sge.game.height:
            self.bbox_bottom = sge.game.height
            self.yvelocity = -abs(self.yvelocity)
            glob.bounce_wall_sound.play()
        elif self.bbox_top < 0:
            self.bbox_top = 0
            self.yvelocity = abs(self.yvelocity)
            glob.bounce_wall_sound.play()

    def event_collision(self, other):
        if isinstance(other, Player):
            if other.hit_direction == 1:
                self.bbox_left = other.bbox_right + 1
                self.xvelocity = min(abs(self.xvelocity) + BALL_ACCELERATION,
                                     BALL_MAX_SPEED)
            else:
                self.bbox_right = other.bbox_left - 1
                self.xvelocity = max(-abs(self.xvelocity) - BALL_ACCELERATION,
                                     -BALL_MAX_SPEED)

            self.yvelocity += (self.y - other.y) * PADDLE_VERTICAL_FORCE
            glob.bounce_sound.play()

    def serve(self, direction=1):
        self.x = self.xstart
        self.y = self.ystart

        if (glob.player1.score < POINTS_TO_WIN and
                glob.player2.score < POINTS_TO_WIN):
            # Next round
            self.xvelocity = BALL_START_SPEED * direction
            self.yvelocity = 0
        else:
            # Game Over!
            self.xvelocity = 0
            self.yvelocity = 0
            glob.hud_sprite.draw_clear()
            x = glob.hud_sprite.width / 2
            p1score = glob.player1.score
            p2score = glob.player2.score
            p1text = "WIN" if p1score > p2score else "LOSE"
            p2text = "WIN" if p2score > p1score else "LOSE"
            glob.hud_sprite.draw_text("hud", p1text, x - TEXT_OFFSET,
                                      TEXT_OFFSET, color="white",
                                      halign=sge.ALIGN_RIGHT,
                                      valign=sge.ALIGN_TOP)
            glob.hud_sprite.draw_text("hud", p2text, x + TEXT_OFFSET,
                                      TEXT_OFFSET, color="white",
                                      halign=sge.ALIGN_LEFT,
                                      valign=sge.ALIGN_TOP)
            glob.game_in_progress = False


def refresh_hud():
    # This fixes the HUD sprite so that it displays the correct score.
    glob.hud_sprite.draw_clear()
    x = glob.hud_sprite.width / 2
    glob.hud_sprite.draw_text("hud", str(glob.player1.score), x - TEXT_OFFSET,
                              TEXT_OFFSET, color="white",
                              halign=sge.ALIGN_RIGHT, valign=sge.ALIGN_TOP)
    glob.hud_sprite.draw_text("hud", str(glob.player2.score), x + TEXT_OFFSET,
                              TEXT_OFFSET, color="white",
                              halign=sge.ALIGN_LEFT, valign=sge.ALIGN_TOP)


def main():
    # Create Game object
    Game(640, 480, fps=120)

    # Load sprites
    paddle_sprite = sge.Sprite(ID="paddle", width=8, height=48, origin_x=4,
                               origin_y=24)
    paddle_sprite.draw_rectangle(0, 0, paddle_sprite.width,
                                 paddle_sprite.height, fill="white")
    ball_sprite = sge.Sprite(ID="ball", width=8, height=8, origin_x=4,
                             origin_y=4)
    ball_sprite.draw_rectangle(0, 0, ball_sprite.width, ball_sprite.height,
                               fill="white")
    glob.hud_sprite = sge.Sprite(width=320, height=160, origin_x=160,
                                 origin_y=0)

    # Load backgrounds
    layers = (sge.BackgroundLayer("ball", sge.game.width / 2, 0, -10000,
                                  xrepeat=False),)
    background = sge.Background (layers, "black")

    # Load fonts
    sge.Font('Liberation Mono', ID="hud", size=48)

    # Load sounds
    glob.bounce_sound = sge.Sound('bounce.wav')
    glob.bounce_wall_sound = sge.Sound('bounce_wall.wav')
    glob.score_sound = sge.Sound('score.wav')

    # Create objects
    Player(1)
    Player(2)
    glob.ball = Ball()
    hud = sge.StellarClass(sge.game.width / 2, 0, -10, sprite=glob.hud_sprite,
                           detects_collisions=False)
    objects = (glob.player1, glob.player2, glob.ball, hud)

    # Create rooms
    room1 = sge.Room(objects, background=background)

    sge.game.start()


if __name__ == '__main__':
    main()
