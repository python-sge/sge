***********************
Tutorial 3: Better Pong
***********************

.. This file has been dedicated to the public domain, to the extent
   possible under applicable law, via CC0. See
   http://creativecommons.org/publicdomain/zero/1.0/ for more
   information. This file is offered as-is, without any warranty.

.. contents::

In the last tutorial, we made a simple Pong game that was kind of
boring.  We're going to make it better by adding scores, sounds, and
joystick support.

Adding Scoring
==============

Adding a score system will make our Pong game feel more like a game and
less like a toy.  Every time a player wins a round, they will get one
point.  When a player gets ten points, they will win the game, and a new
game can be started by pressing the Enter key.

Making Enter Restart the Game
-----------------------------

We are going to need a new global variable: :data:`game_in_progress`.
This variable will indicate whether or not a game is currently going and
will be used to determine whether to start a new game or pause when the
Enter key is pressed.  Set it to :const:`True` by default.

To make pressing Enter start a new game, we will check
:data:`game_in_progress`.  If a game is in progress, we will pause the
game, as we had it do previously.  Otherwise, we will set
:data:`game_in_progress` to :const:`True` and restart the room.

If you look through the documentation for :class:`sge.dsp.Room`, you may
notice that no "restart" method exists. In fact, this is a design
choice; earlier versions of the SGE did have a method to restart rooms,
but it was removed because this feature is overly difficult to maintain
properly.  But how do we restart the room, then? Well, we technically
don't.  Instead, we create a new room which is exactly like the one we
wanted to restart, and immediately start it.  We will put the creation
of the room into a new function, :func:`create_room`.  Our definition of
:meth:`Game.event_key_press` becomes::

    def event_key_press(self, key, char):
        global game_in_progress

        if key == 'f8':
            sge.gfx.Sprite.from_screenshot().save('screenshot.jpg')
        elif key == 'f11':
            self.fullscreen = not self.fullscreen
        elif key == 'escape':
            self.event_close()
        elif key in ('p', 'enter'):
            if game_in_progress:
                self.pause()
            else:
                game_in_progress = True
                create_room().start()

Now, we need to define :func:`create_room`.  This is very simple; we
just copy and paste the code we used at the bottom to create the room
into it, but specify that :data:`player` and :data:`player2` are global.
Our function is as follows::

    def create_room():
        global player1
        global player2
        player1 = Player(1)
        player2 = Player(2)
        ball = Ball()
        return sge.dsp.Room([player1, player2, ball], background=background)

Of course, this makes the identical code at the bottom redundant, so we
will replace it with a call to :func:`create_room`.

Giving Points to the Players
----------------------------

We now need to add score attributes to the :class:`Player` objects.  We
will initialize the new attribute, :attr:`score`, in
:meth:`Player.event_create` as ``0``.

Now, in :meth:`Ball.event_step`, add lines to increase
:attr:`player1.score` and :attr:`player2.score` whenever the respective
player wins a round.

Displaying the Scores
---------------------

The players have points, but can't see the score!  We need to add a HUD
(heads-up display) to show the score to the players.

There are a couple of ways we can do this.  Most obviously, we can use
:meth:`sge.dsp.Game.project_text` or :meth:`sge.dsp.Room.project_text`.
However, there is a much better way: have a dynamically generated sprite
that represents the look of the HUD at any given time, and displaying
that sprite.

New Resources
~~~~~~~~~~~~~

We need to add a new global variable called :data:`hud_sprite`.  Assign
a new sprite to this variable with a :attr:`width` of ``320``, a
:attr:`height` of ``120``, an :attr:`origin_x` of ``160``, and an
:attr:`origin_y` of ``0``.

To draw text, we need a font.  Create a new :class:`sge.gfx.Font` object
and assign it to :data:`hud_font`.  For now, we will use a system font.
I am choosing ``"Droid Sans Mono"``, but you can choose whatever font
you prefer.  Pass your choice as the first argument to
:meth:`sge.gfx.Font.__init__`.  Set the ``size`` keyword argument to
``48``.

.. note::

   We are using system fonts for simplicity, but it is generally a bad
   idea to rely on them.  There is no standard for what fonts are
   available on the system, and the set of fonts available on the system
   varies widely.  In real projects, it is better to distribute a font
   file with the game and use that.

Drawing the HUD
~~~~~~~~~~~~~~~

There are a few times we need to redraw the HUD: when the game starts,
when player 1 scores, and when player 2 scores.  Therefore, we will put
the redrawing code into a function, :func:`refresh_hud`.  This function
needs to clear the HUD sprite, draw Player 1's score, and then draw
Player 2's score.

Another constant is needed: :const:`TEXT_OFFSET`, which we will define
as ``16``.

We clear the HUD sprite with :meth:`sge.gfx.Sprite.draw_clear`.

To draw the text, we use :meth:`sge.gfx.Sprite.draw_text`.  Both calls
have a few arguments in common: ``font`` is set to ``hud_font``, ``y``
is set to ``TEXT_OFFSET``, ``color`` is set to white, and ``valign`` is
set to ``"top"``.

The rest of the arguments are different between the two.  ``text`` is
set to the respective player's score, converted to a string.  ``x`` is
set to ``hud_sprite.width / 2 - TEXT_OFFSET`` for player 1's score, and
``hud_sprite.width / 2 + TEXT_OFFSET`` for player 2's score.  ``halign``
is set to ``"right"`` for player 1's score, and ``"left"`` for
player 2's score.

:func:`refresh_hud` ends up something like this::

    def refresh_hud():
        # This fixes the HUD sprite so that it displays the correct score.
        hud_sprite.draw_clear()
        x = hud_sprite.width / 2
        hud_sprite.draw_text(hud_font, str(player1.score), x - TEXT_OFFSET,
                             TEXT_OFFSET, color=sge.gfx.Color("white"),
                             halign="right", valign="top")
        hud_sprite.draw_text(hud_font, str(player2.score), x + TEXT_OFFSET,
                             TEXT_OFFSET, color=sge.gfx.Color("white"),
                             halign="left", valign="top")

Add calls to :func:`refresh_hud` in the three places where a
:attr:`Player.score` value changes, right after the change.  These
places are in :meth:`Player.event_create` and :meth:`Ball.event_step`.

we have one more problem.  :func:`refresh_hud` requires :data:`player1`
and :data:`player2` to each have an attribute called :attr:`score`, but
the first time it is called, one of the player objects has not had a
chance to initialize this attribute.  To work around this, add a class
attribute to :class:`Player` called :attr:`score`, and set it to ``0``.
This will cause :attr:`player1.score` and :attr:`player2.score` to be
``0`` in the event that the respective object's :attr:`score` has not
been initialized yet.

Displaying the HUD
~~~~~~~~~~~~~~~~~~

At this point, we have our HUD, but it isn't displayed.  We will fix
this simply by adding a step event to :class:`Game` which projects the
HUD sprite onto the screen::

    def event_step(self, time_passed, delta_mult):
        self.project_sprite(hud_sprite, 0, self.width / 2, 0)

Unlike :class:`sge.dsp.Room` projections, :class:`sge.dsp.Game`
projections are relative to the screen.  Additionally, these projections
are always on top of everything else on the screen.  This is usually how
we want a HUD to be displayed, which is why we are using a
:class:`sge.dsp.Game` projection instead of a :class:`sge.dsp.Room`
projection or :class:`sge.dsp.Object` object.

.. note::

   You may notice that, when you pause the game, the HUD disappears.
   This is *not* a bug! This happens because the step event doesn't
   occur while the game is paused.  If you want the HUD to show up while
   the game is paused, project it in the paused step event, defined by
   :meth:`sge.dsp.Game.event_paused_step`, as well.

Giving Victory
--------------

At this point, we have scores, but no one ever officially wins.  We need
to end the game when someone gets 10 points.  We will go a little
further and replace the scores with text that says "WIN" and "LOSE" for
the winner and loser, respectively.

Define a new constant called :const:`POINTS_TO_WIN` as ``10``.

In our case, the most convenient place to check for victory is within
:meth:`Ball.serve`.  Specifically, put the code that sets the speed of
the ball under a conditional that checks whether the :attr:`score`
values of both players are less than :const:`POINTS_TO_WIN`.  Add an
``else`` block below that.  This is where a player has won the game.

Since the game is over, stop the movement of the ball by setting
:attr:`xvelocity` and :attr:`yvelocity` to ``0``.  We don't want any
more scoring to happen.

Now, draw the new text onto the HUD.  We do this using the same call to
:meth:`sge.gfx.Sprite.draw_text` we used in :func:`refresh_hud`, except
instead of drawing the scores converted to strings, we draw ``"WIN"`` or
``"LOSE"`` depending on whether or not the respective player's score is
greater than the other player's score.

Finally, set :data:`game_in_progress` to :const:`False`.  Don't forget
to declare it with ``global`` first.

The new :meth:`Ball.serve` looks something like this::

    def serve(self, direction=None):
        global game_in_progress

        if direction is None:
            direction = random.choice([-1, 1])

        self.x = self.xstart
        self.y = self.ystart

        if (player1.score < POINTS_TO_WIN and
                player2.score < POINTS_TO_WIN):
            # Next round
            self.xvelocity = BALL_START_SPEED * direction
            self.yvelocity = 0
        else:
            # Game Over!
            self.xvelocity = 0
            self.yvelocity = 0
            hud_sprite.draw_clear()
            x = hud_sprite.width / 2
            p1text = "WIN" if player1.score > player2.score else "LOSE"
            p2text = "WIN" if player2.score > player1.score else "LOSE"
            hud_sprite.draw_text(hud_font, p1text, x - TEXT_OFFSET,
                                 TEXT_OFFSET, color=sge.gfx.Color("white"),
                                 halign="right", valign="top")
            hud_sprite.draw_text(hud_font, p2text, x + TEXT_OFFSET,
                                 TEXT_OFFSET, color=sge.gfx.Color("white"),
                                 halign="left", valign="top")
            game_in_progress = False

Adding Sounds
=============

We have a complete Pong game now, but it's still a little quiet.  Let's
make it more lively by adding some sounds.

Getting the Sounds
------------------

I would normally go to a database like `OpenGameArt
<http://opengameart.org>`_ for sound effects, but in this case, we are
instead going to use a nice free/libre program called `Sfxr
<http://www.drpetter.se/project_sfxr.html>`_.  This program makes it
easy to generate retro-sounding sound effects, so it's perfect for Pong
sounds.  Generate three sounds: one for the ball bouncing off a paddle
("bounce.wav"), one for the ball bouncing off a wall
("bounce_wall.wav"), and one for the ball passing by a player
("score.wav").  Alternatively, you can copy the sounds I generated from
examples/data.  Create a folder in your project directory with the name
"data" and put your sounds in this folder.

.. note::

   Some file systems, like FAT32 and NTFS, are case-insensitive and will
   allow you to treat "bounce.wav" and "Bounce.wav" as if they are the
   same file name, but some, such as pretty much every Linux file
   system, are case-sensitive, meaning that "bounce.wav" and
   "Bounce.wav" are two completely different names; requesting one will
   never give you the other.  If you have a case-insensitive file
   system, be careful to not get the case wrong, or some people who play
   the game will face a crash that will be completely invisible to you!

Loading the Sounds
------------------

Sounds in the SGE are stored in :class:`sge.snd.Sound` objects.  As the
only argument, indicate the full path to the file.  There are two ways
to indicate the path: using the current working directory as a base, and
using the directory of pong.py as a base.  Both of methods require the
:mod:`os` module, so be sure to add this to your list of imports.

The easiest way to get the path of the file is to use the current
working directory as a base, on the assumption that the current working
directory is also the directory that the "data" folder is located in.
This method is very simple; assuming we want the file called "spam.wav",
we would use this code::

    os.path.join("data", "spam.wav")

However, it is not always the case that the current working directory is
the appropriate location to search for the "data" folder.  It could be
that the current working directory is the user's home directory, for
instance.  To prevent the game from crashing in this case, define a
constant called :const:`DATA`, indicating the "data" directory relative
to the location of pong.py::

    DATA = os.path.join(os.path.dirname(__file__), "data")

:data:`__file__` is a special variable indicating the full path to the
current file, i.e. pong.py in this case.  By getting the directory name
of the current file, we can be certain of where to look for the "data"
folder.  :const:`DATA` now indicates the appropriate path to the "data"
folder, so from now on, if we want a file called "spam.wav" located in
this directory, we use this code::

    os.path.join(DATA, "spam.wav")

Assign the appropriate :class:`sge.snd.Sound` objects to
:data:`bounce_sound`, :data:`bounce_wall_sound`, and
:data:`score_sound`.

Playing the Sounds
------------------

Sounds are played with :meth:`sge.snd.Sound.play`.  Call this method in
the appropriate places: when a player scores, when the ball bounces off
an edge of the screen, and when the ball hits a paddle.  There are five
places in total.

With that, our Pong game now has sound effects.

Adding Joystick Support
=======================

Joystick support is a nice thing to have in a game, so we are going to
add it.  We are going to support analog sticks and trackballs.  Mouse
control would actually be even better, but this would put one of the
players at an unfair advantage.

First, we will add an attribute to :class:`Player` indicating what
joystick to use, called :attr:`joystick`.  Set it to ``0`` (which is the
first joystick) for player 1, and ``1`` (which is the second joystick)
for player 2.

Axis Movement
-------------

Adding movement based on a joystick axis is easy.  For this, we use
:func:`sge.joystick.get_axis` in the step event of :class:`Player`.
Pass ``self.joystick`` as the first argument, and ``1`` (which is the
Y-axis) as the second argument.  Assign it to a variable called
``axis_motion``.  Later, we will be modifying the code that sets
:attr:`yvelocity` so that it is chosen based on axis position, trackball
movement, or key presses, whichever one would cause it to move fastest.

Trackball Movement
------------------

Since trackball motion is relative, it is a little trickier.  We need to
store the amount of movement it makes each frame.  We will use an
attribute called :attr:`trackball_motion` for that; initialize it as
``0`` in the create event.

We now need to define the trackball move event, which is defined by
:meth:`sge.dsp.Object.event_joystick_trackball_move`.  Within this
event, if the ``joystick`` argument is the same as ``self.joystick``,
add ``y`` to ``self.trackball_motion``.  We are adding to it, rather
than replacing it, because the trackball might move multiple times in
the same frame.

Applying the Joystick Controls
------------------------------

Currently, we have this line::

    self.yvelocity = key_motion * PADDLE_SPEED

This line uses the state of the keys to determine how to move the
paddle.  We need to change this so that the joystick controls we defined
can be used as well.  It will be replaced with the following:

- If the absolute value of ``axis_motion`` is greater than the absolute
  value of both ``key_motion`` and :attr:`trackball_motion`, set
  :attr:`yvelocity` to ``axis_motion * PADDLE_SPEED``.
- Otherwise, if :attr:`trackball_motion` is greater than ``key_motion``,
  set :attr:`yvelocity` to ``self.trackball_motion * PADDLE_SPEED``
- Otherwise, use the line we have been using up until this point.

After this, we must set :attr:`trackball_motion` to ``0``.

The Final Result
================

Our final Pong game now has scores, sounds, and even joystick support::

    #!/usr/bin/env python3

    # Pong Example
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
    PADDLE_XOFFSET = 32
    PADDLE_SPEED = 4
    PADDLE_VERTICAL_FORCE = 1 / 12
    BALL_START_SPEED = 2
    BALL_ACCELERATION = 0.2
    BALL_MAX_SPEED = 15
    POINTS_TO_WIN = 10
    TEXT_OFFSET = 16

    game_in_progress = True


    class Game(sge.dsp.Game):

        def event_step(self, time_passed, delta_mult):
            self.project_sprite(hud_sprite, 0, self.width / 2, 0)

        def event_key_press(self, key, char):
            global game_in_progress

            if key == 'f8':
                sge.gfx.Sprite.from_screenshot().save('screenshot.jpg')
            elif key == 'f11':
                self.fullscreen = not self.fullscreen
            elif key == 'escape':
                self.event_close()
            elif key in ('p', 'enter'):
                if game_in_progress:
                    self.pause()
                else:
                    game_in_progress = True
                    self.current_room.start()

        def event_close(self):
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


    class Player(sge.dsp.Object):

        score = 0

        def __init__(self, player):
            if player == 1:
                self.joystick = 0
                self.up_key = "w"
                self.down_key = "s"
                x = PADDLE_XOFFSET
                self.hit_direction = 1
            else:
                self.joystick = 1
                self.up_key = "up"
                self.down_key = "down"
                x = sge.game.width - PADDLE_XOFFSET
                self.hit_direction = -1

            y = sge.game.height / 2
            super().__init__(x, y, sprite=paddle_sprite, checks_collisions=False)

        def event_create(self):
            self.score = 0
            refresh_hud()
            self.trackball_motion = 0

        def event_step(self, time_passed, delta_mult):
            # Movement
            key_motion = (sge.keyboard.get_pressed(self.down_key) -
                          sge.keyboard.get_pressed(self.up_key))
            axis_motion = sge.joystick.get_axis(self.joystick, 1)

            if (abs(axis_motion) > abs(key_motion) and
                    abs(axis_motion) > abs(self.trackball_motion)):
                self.yvelocity = axis_motion * PADDLE_SPEED
            elif abs(self.trackball_motion) > abs(key_motion):
                self.yvelocity = self.trackball_motion * PADDLE_SPEED
            else:
                self.yvelocity = key_motion * PADDLE_SPEED

            self.trackball_motion = 0

            # Keep the paddle inside the window
            if self.bbox_top < 0:
                self.bbox_top = 0
            elif self.bbox_bottom > sge.game.current_room.height:
                self.bbox_bottom = sge.game.current_room.height

        def event_joystick_trackball_move(self, joystick, ball, x, y):
            if joystick == self.joystick:
                self.trackball_motion += y


    class Ball(sge.dsp.Object):

        def __init__(self):
            x = sge.game.width / 2
            y = sge.game.height / 2
            super().__init__(x, y, sprite=ball_sprite)

        def event_create(self):
            self.serve()

        def event_step(self, time_passed, delta_mult):
            # Scoring
            if self.bbox_right < 0:
                player2.score += 1
                refresh_hud()
                score_sound.play()
                self.serve(-1)
            elif self.bbox_left > sge.game.current_room.width:
                player1.score += 1
                refresh_hud()
                score_sound.play()
                self.serve(1)

            # Bouncing off of the edges
            if self.bbox_bottom > sge.game.current_room.height:
                self.bbox_bottom = sge.game.current_room.height
                self.yvelocity = -abs(self.yvelocity)
                bounce_wall_sound.play()
            elif self.bbox_top < 0:
                self.bbox_top = 0
                self.yvelocity = abs(self.yvelocity)
                bounce_wall_sound.play()

        def event_collision(self, other, xdirection, ydirection):
            if isinstance(other, Player):
                if other.hit_direction == 1:
                    self.bbox_left = other.bbox_right + 1
                else:
                    self.bbox_right = other.bbox_left - 1

                self.xvelocity = min(abs(self.xvelocity) + BALL_ACCELERATION,
                                     BALL_MAX_SPEED) * other.hit_direction
                self.yvelocity += (self.y - other.y) * PADDLE_VERTICAL_FORCE
                bounce_sound.play()

        def serve(self, direction=None):
            global game_in_progress

            if direction is None:
                direction = random.choice([-1, 1])

            self.x = self.xstart
            self.y = self.ystart

            if (player1.score < POINTS_TO_WIN and
                    player2.score < POINTS_TO_WIN):
                # Next round
                self.xvelocity = BALL_START_SPEED * direction
                self.yvelocity = 0
            else:
                # Game Over!
                self.xvelocity = 0
                self.yvelocity = 0
                hud_sprite.draw_clear()
                x = hud_sprite.width / 2
                p1text = "WIN" if player1.score > player2.score else "LOSE"
                p2text = "WIN" if player2.score > player1.score else "LOSE"
                hud_sprite.draw_text(hud_font, p1text, x - TEXT_OFFSET,
                                     TEXT_OFFSET, color=sge.gfx.Color("white"),
                                     halign="right", valign="top")
                hud_sprite.draw_text(hud_font, p2text, x + TEXT_OFFSET,
                                     TEXT_OFFSET, color=sge.gfx.Color("white"),
                                     halign="left", valign="top")
                game_in_progress = False


    def create_room():
        global player1
        global player2
        player1 = Player(1)
        player2 = Player(2)
        ball = Ball()
        return sge.dsp.Room([player1, player2, ball], background=background)


    def refresh_hud():
        # This fixes the HUD sprite so that it displays the correct score.
        hud_sprite.draw_clear()
        x = hud_sprite.width / 2
        hud_sprite.draw_text(hud_font, str(player1.score), x - TEXT_OFFSET,
                             TEXT_OFFSET, color=sge.gfx.Color("white"),
                             halign="right", valign="top")
        hud_sprite.draw_text(hud_font, str(player2.score), x + TEXT_OFFSET,
                             TEXT_OFFSET, color=sge.gfx.Color("white"),
                             halign="left", valign="top")


    # Create Game object
    Game(width=640, height=480, fps=120, window_text="Pong")

    # Load sprites
    paddle_sprite = sge.gfx.Sprite(width=8, height=48, origin_x=4, origin_y=24)
    ball_sprite = sge.gfx.Sprite(width=8, height=8, origin_x=4, origin_y=4)
    paddle_sprite.draw_rectangle(0, 0, paddle_sprite.width, paddle_sprite.height,
                                 fill=sge.gfx.Color("white"))
    ball_sprite.draw_rectangle(0, 0, ball_sprite.width, ball_sprite.height,
                               fill=sge.gfx.Color("white"))
    hud_sprite = sge.gfx.Sprite(width=320, height=120, origin_x=160, origin_y=0)

    # Load backgrounds
    layers = [sge.gfx.BackgroundLayer(paddle_sprite, sge.game.width / 2, 0, -10000,
                                      repeat_up=True, repeat_down=True)]
    background = sge.gfx.Background(layers, sge.gfx.Color("black"))

    # Load fonts
    hud_font = sge.gfx.Font("Droid Sans Mono", size=48)

    # Load sounds
    bounce_sound = sge.snd.Sound(os.path.join(DATA, 'bounce.wav'))
    bounce_wall_sound = sge.snd.Sound(os.path.join(DATA, 'bounce_wall.wav'))
    score_sound = sge.snd.Sound(os.path.join(DATA, 'score.wav'))

    # Create rooms
    sge.game.start_room = create_room()

    sge.game.mouse.visible = False


    if __name__ == '__main__':
        sge.game.start()
