****************
Tutorial 2: Pong
****************

.. This file has been dedicated to the public domain, to the extent
   possible under applicable law, via CC0. See
   http://creativecommons.org/publicdomain/zero/1.0/ for more
   information. This file is offered as-is, without any warranty.

.. contents::

Now that you've seen the basics of the SGE, it's time to create an
actual game. Although Pong might seem extremely simple, it will give you
a great foundation for developing more complex games in the future.

Start out by setting up the project like we did in the Hello World
tutorial.

Adding Game Logic
=================

The Game Class
--------------

For our :class:`sge.dsp.Game` class, we want to of course provide a way
to exit the game, and in this case, we are also going to provide a way
to pause the game.  Just for the heck of it, let's also allow the player
to take a screenshot by pressing F8 and toggle fullscreen by pressing
F11.

Let's take it one event at a time. Our close event is simple enough::

    def event_close(self):
        self.end()

Our key press event is slightly more involved.  To take a screenshot, we
simply use a combination of :meth:`sge.gfx.Sprite.from_screenshot` and
:meth:`sge.gfx.Sprite.save`.  To toggle fullscreen, we simply change the
value of :attr:`sge.dsp.Game.fullscreen`.  To pause the game, we use
:meth:`sge.dsp.Game.pause`.  We end up with this::

    def event_key_press(self, key, char):
        if key == 'f8':
            sge.gfx.Sprite.from_screenshot().save('screenshot.jpg')
        elif key == 'f11':
            self.fullscreen = not self.fullscreen
        elif key == 'escape':
            self.event_close()
        elif key in ('p', 'enter'):
            self.pause()

This is incomplete, though.  When :meth:`sge.dsp.Game.pause` is called,
the game enters a special loop where normal events are ignored.  In
their place, we need to use "paused" events to give the player a chance
to unpause.  We also should allow the player to quit the game while it
is paused.  To achieve these goals, we add the special events,
:meth:`sge.dsp.Game.event_paused_key_pressed` and
:meth:`sge.dsp.Game.event_paused_close`::

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

In this case, we are defining the paused key press event to unpause the
game when any key except for the Esc key is pressed.

The Object Classes
------------------

:class:`sge.dsp.Object` objects are things in a game that we want to be
displayed in a room.  These objects tend to represent players, enemies,
tiles, decorations, and pretty much anything else you can think of.

For Pong, we need three objects: the two players, and the ball.  We will
define two sub-classes of :class:`sge.dsp.Object` for this purpose:
:class:`Player` and :class:`Ball`.

Player
~~~~~~

:class:`Player` is used for the paddles.  These are what the players
control.

For :class:`Player`, the difference between different objects is which
player controls it. Every other difference (the position, the controls,
and the direction it hits the ball) can be easily derived from that.  We
are therefore going to define :meth:`Player.__init__` to reflect this.

:meth:`Player.__init__` will take a single argument, ``player``.  This
argument will indicate which player the object is for: ``1`` for player
1, or ``2`` for player 2.  We will set a few attributes based on this:

- :attr:`up_key` will indicate the key that moves the paddle up.  We
  will set it to ``"w"`` for player 1, or ``"up"`` for player 2.

- :attr:`down_key` will indicate the key that moves the paddle down.  We
  will set it to ``"s"`` for player 1, or ``"down"`` for player 2.

- :attr:`x` is an attribute inherited from :class:`sge.dsp.Object` which
  indicates the horizontal position of the object.  We will set this
  based on a constant we will define (technically just a variable, since
  Python doesn't support constants) called :const:`PADDLE_XOFFSET`:
  ``PADDLE_XOFFSET`` for player 1, or
  ``sge.game.width - PADDLE_XOFFSET`` for player 2.  We will define
  :const:`PADDLE_XOFFSET` near the top of our code file, beneath
  imports, as ``32``.

- :attr:`hit_direction` will indicate the direction the paddle hits the
  ball.  We will set it to ``1`` for player 1, and ``-1`` for player 2.

Additionally, certain attributes inherited from :class:`sge.dsp.Object`
will be the same for both :class:`Player` objects.  :attr:`y` will
always be ``sge.game.height / 2`` (vertically centered).  :attr:`sprite`
will always be ``paddle_sprite`` (a sprite we will create later).
:attr:`checks_collisions` will always be :const:`False`, since player
objects don't need to check for collisions with each other; we can
therefore leave all collision checking to the ball object.

All attributes inherited from :class:`sge.dsp.Object` will be defined by
passing their values to :meth:`sge.dsp.Object.__init__`, which we will
call with ``super().__init__(*args, **kwargs)``.  This makes our
:meth:`Player.__init__` defintion an extension, rather than an override,
of :meth:`sge.dsp.Object.__init__`, which is important; overriding this
method would be likely to break something.

Our definition of :meth:`Player.__init__`` ends up looking something
like this::

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

We need to allow the players to move the paddles.  We could do this by
using key press events, but since we would like the players to be able
to continuously move the paddles by holding down the key, the proper way
to do this is to check for the state of the keys every frame and move
accordingly.

:func:`sge.keyboard.get_pressed` returns the state of a key on the
keyboard.  We will check this in the step event to decide how the paddle
should move on any given frame.  The step event, defined by
:meth:`sge.dsp.Object.event_step`, is an event which always executes
every frame.

What we will do is subtract the state of :attr:`up_key` from the state
of :attr:`down_key`.  This will give us ``-1`` if only :attr:`up_key` is
pressed, ``1`` if only :attr:`down_key` is pressed, and ``0`` if neither
or both keys are pressed.  We can multiply this result by a constant,
which we will call :const:`PADDLE_SPEED`, to get the amount that the
paddle should move this frame, and assign this value to the player's
:attr:`sge.dsp.Object.yvelocity`, an attribute which indicates the
number of pixels an object will move vertically each frame.  We will
define :const:`PADDLE_SPEED` as ``4``.

This isn't quite enough, though.  With just this, the paddle can be
moved off-screen!  To prevent this from happening, we will check the
player object's :attr:`bbox_top` and :attr:`bbox_bottom` values; these
indicate the current location of the object's bounding box.  If
:attr:`bbox_top` is less than ``0``, we will set it to ``0``.  If
:attr:`bbox_bottom` is greater than ``sge.game.current_room.height``, we
will set it to ``sge.game.current_room.height``.
:attr:`sge.game.current_room`, as its name implies, indicates the
currently running :class:`sge.game.Room` object.

Our step event ends up looking something like this::

    def event_step(self, time_passed, delta_mult):
        # Movement
        key_motion = (sge.keyboard.get_pressed(self.down_key) -
                      sge.keyboard.get_pressed(self.up_key))

        self.yvelocity = key_motion * PADDLE_SPEED

        # Keep the paddle inside the window
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom > sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height

Ball
~~~~

:class:`Ball` is the ball.  It is bounced back and forth by the players.
If it touches the top or bottom edge of the screen, it bounces off.  If
it passes one of the players, the other player gets a point and the ball
is returned to the playing field.

Any :class:`Ball` object is always going to have the same initial
attributes as any other :class:`Ball` object, so much like what we did
with :class:`Player`, we are going to define a custom
:meth:`Ball.__init__`.

In this case, it's much simpler: :attr:`x` and :attr:`y` are going to
start at the center of the screen, and :attr:`sprite` is going to be
``ball_sprite``.  These are attributes inherited from
:class:`sge.dsp.Object`, so we indicate them in a call to
``super().__init__``.  :meth:`Ball.__init__` ends up as::

    def __init__(self):
        x = sge.game.width / 2
        y = sge.game.height / 2
        super().__init__(x, y, sprite=ball_sprite)

Since we want to serve the ball both at the start of the game and every
time the ball passes a player, we should define a :meth:`Ball.serve`
method.  This method needs to do two things: first, it needs to return
the ball to its original position in the center.  Second, it needs to
set the speed so that it moves either straight to the left or straight
to the right.  If a direction isn't specified, it needs to choose a
direction at random.

For the first task, we can use :attr:`sge.dsp.Object.xstart` and
:attr:`sge.dsp.Object.ystart`.  These attributes indicate the original
position of an object when it was first created, which in the case of
:class:`Ball` objects is in the center of the screen.

For the second task, we have an argument called ``direction``.  If it is
``None``, it randomly becomes either ``1`` or ``-1``.  The value is then
multiplied by a constant called :const:`BALL_START_SPEED`, which we will
set to ``2``, and this becomes the ball's
:attr:`sge.dsp.Object.xvelocity` value.  The ball's
:attr:`sge.dsp.Object.yvelocity` value is then set to ``0``.

The result looks like this::

    def serve(self, direction=None):
        if direction is None:
            direction = random.choice([-1, 1])

        self.x = self.xstart
        self.y = self.ystart

        # Next round
        self.xvelocity = BALL_START_SPEED * direction
        self.yvelocity = 0

.. note::

   Since we are now using the :mod:`random` module, we need to also
   import it at the top of our code file.

When the ball is created, we want to serve it immediately.  we will put
this in the create event, which is defined by
:meth:`sge.dsp.Object.event_create`.  The create event happens whenever
the object is created in the room.  This is the create event of
:class:`Ball`::

    def event_create(self):
        self.serve()

For :class:`Ball`'s step event, we need to do two things: cause the ball
to bounce off of the top and bottom edges of the screen, and serve the
ball when it passes the left or right edge of the screen.

For the first task, we do the same thing we did with :class:`Player`,
but we also set whether :attr:`yvelocity` is positive or negative; we
make it negative when the ball touches the bottom, and positive when the
ball touches the top.

For the second task, we do a similar check, but we phrase the check such
that the ball needs to be completely outside of the room, rather than
just touching the edge.  We do this by checking :attr:`bbox_right`
against the left edge, and :attr:`bbox_left` against the right edge.
When the ball is outside the screen, we serve it in the direction of the
player it passed (so that the player who lost the round gets initial
control of the ball).

Our step event for :class:`Ball` ends up looking something like this::

    def event_step(self, time_passed, delta_mult):
        # Scoring
        if self.bbox_right < 0:
            self.serve(-1)
        elif self.bbox_left > sge.game.current_room.width:
            self.serve(1)

        # Bouncing off of the edges
        if self.bbox_bottom > sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height
            self.yvelocity = -abs(self.yvelocity)
        elif self.bbox_top < 0:
            self.bbox_top = 0
            self.yvelocity = abs(self.yvelocity)

Now, we need to allow the players to repel the ball.  We will do this
with a collision event.  Collision events, controlled by
:meth:`sge.dsp.Object.event_collision`, occur when two objects touch
each other.

We first need to verify what type of object we're colliding with.  The
most straightforward way is to use :func:`isinstance` to check whether
or not the object being collided with, which is passed on to the
``other`` argument, is an instance of :class:`Player`.  We write the
collision code for these two objects under this check.

The most straightforward way to do this is with directional collision
detection, but we are going to instead use :attr:`Player.hit_direction`
to determine what to do.  If the :attr:`other.hit_direction` is ``1``,
we bounce the ball to the right.  Otherwise, we bounce the ball to the
left.

We need to make the ball accelerate each time the ball hits a paddle, so
that the round goes faster over time.  We will store the amount of
acceleration in a constant called :const:`BALL_ACCELERATION`, which we
will define as ``0.2``.  We will then set :attr:`self.xvelocity` to
``(abs(self.xvelocity) + BALL_ACCELERATION) * other.hit_direction``.

We also need to make the ball's vertical movement change based on where
it hits the paddle.  To do this, we will subtract :attr:`other.y` from
:attr:`self.y` and multiply that by a constant called
:const:`PADDLE_VERTICAL_FORCE`, which we will define as ``1 / 12``; this
value will be added to :attr:`self.yvelocity`.

There is one problem left, though it is not particularly obvious.  The
way we have it set up at this point, the ball will eventually move so
fast that it will fail to collide with the paddles.  This is due to how
movement works; it's not actual movement, but rather a slight change of
position done every frame.  If that change of position is too much, the
ball can pass right over a paddle.

To prevent this, we need to set a limit for how fast the ball can move
horizontally.  Instead of just multiplying
``(abs(self.xvelocity) + BALL_ACCELERATION)`` by
:attr:`other.hit_direction`, we multiply the smallest out of that, and a
new constant called :const:`BALL_MAX_SPEED`, by
:attr:`other.hit_direction`.  We will define :const:`BALL_MAX_SPEED` as
``15``.

Our collision event ends up looking something like this::

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, Player):
            if other.hit_direction == 1:
                self.bbox_left = other.bbox_right + 1
            else:
                self.bbox_right = other.bbox_left - 1

            self.xvelocity = min(abs(self.xvelocity) + BALL_ACCELERATION,
                                 BALL_MAX_SPEED) * other.hit_direction
            self.yvelocity += (self.y - other.y) * PADDLE_VERTICAL_FORCE

Starting the Game
=================

It's time to get our game started.

We are going to pass some arguments to the creation of our :class:`Game`
object: we are going to define ``width`` as ``640``, ``height`` as
``480``, ``fps`` as ``120``, and ``window_text`` as ``"Pong"``.  Specify
them as keyword arguments.

Loading Sprites
---------------

We need two sprites: a paddle sprite and a ball sprite.  We also need a
black background with a line down the middle.  We could draw these in an
image editor and load them, but since they are so simple, we are going
to generate them dynamically instead.

Sprites are stored as :class:`sge.gfx.Sprite` objects, so we are going
to create two of them::

    paddle_sprite = sge.gfx.Sprite(width=8, height=48, origin_x=4, origin_y=24)
    ball_sprite = sge.gfx.Sprite(width=8, height=8, origin_x=4, origin_y=4)

:attr:`sge.gfx.Sprite.origin_x` and :attr:`sge.gfx.Sprite.origin_y`
indicate the origin of the sprite.  In this case, we are setting the
origins to the center of the sprites.  This is necessary for our method
of determining how the paddles affect vertical speed to work, and it
also makes symmetry easier.

Currently, both of these sprites are blank.  We need to draw the images
on them.  In this case, we will just draw white rectangles that fill the
entirety of the sprites, which can be done with
:meth:`sge.gfx.Sprite.draw_rectangle`::

    paddle_sprite.draw_rectangle(0, 0, paddle_sprite.width,
                                 paddle_sprite.height, fill=sge.gfx.Color("white"))
    ball_sprite.draw_rectangle(0, 0, ball_sprite.width, ball_sprite.height,
                               fill=sge.gfx.Color("white"))

Loading Backgrounds
-------------------

Now we need a background.  Our sprites are white, so we need a black
background.  We could of course leave it just at that, but that would be
boring, so we are also going to also have a white line in the middle.
We can do this easily by using the paddle sprite as a background layer.
Background layers are special objects that indicate sprites that are
used in a background.  We create the layer, put it in a list, and pass
that list onto :meth:`sge.gfx.Background.__init__`'s ``layers``
argument::

    layers = [sge.gfx.BackgroundLayer(paddle_sprite, sge.game.width / 2, 0, -10000,
                                      repeat_up=True, repeat_down=True)]
    background = sge.gfx.Background(layers, sge.gfx.Color("black"))

The fourth argument of :meth:`sge.BackgroudLayer.__init__` is the
layer's Z-axis value.  The Z-axis is used to determine what objects are
in front of what other objects; objects with a higher Z-axis value are
closer to the viewer.  The default Z-axis value is ``0``.  Since we want
all objects to be in front of the layer, we set its Z-axis value to a
very low negative value.

Creating Objects
----------------

Don't forget to create our objects!  In :data:`player1`, store a
:class:`Player` object with the ``player`` argument specified as ``1``.
In :data:`player2`, store a :class:`Player` object with the ``player``
argument specified as ``2``.  Finally, create a :class:`Ball` object and
store it in :data:`ball`.  Put all of these objects in a list and assign
this list to a variable called ``objects``.

Creating Rooms
--------------

Create a :class:`Room` object.  Specify the first argument as
``objects``, and specify the keyword argument ``background`` as
``background``.  Don't forget to assign it to
:attr:`sge.game.start_room`!

Making the Mouse Invisible
--------------------------

Since we don't need to see the mouse cursor, we will hide it.  To do
this, set :attr:`sge.game.mouse.visible` to :const:`False`.

Starting the Game
-----------------

Add a call to :meth:`sge.game.start` at the end, under a check for the
value of :data:`__name__`.

The Final Result
================

You should now have a script that looks something like this::

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

    import random

    import sge

    PADDLE_XOFFSET = 32
    PADDLE_SPEED = 4
    PADDLE_VERTICAL_FORCE = 1 / 12
    BALL_START_SPEED = 2
    BALL_ACCELERATION = 0.2
    BALL_MAX_SPEED = 15


    class Game(sge.dsp.Game):

        def event_key_press(self, key, char):
            global game_in_progress

            if key == 'f8':
                sge.gfx.Sprite.from_screenshot().save('screenshot.jpg')
            elif key == 'f11':
                self.fullscreen = not self.fullscreen
            elif key == 'escape':
                self.event_close()
            elif key in ('p', 'enter'):
                self.pause()

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

        def __init__(self, player):
            if player == 1:
                self.up_key = "w"
                self.down_key = "s"
                x = PADDLE_XOFFSET
                self.hit_direction = 1
            else:
                self.up_key = "up"
                self.down_key = "down"
                x = sge.game.width - PADDLE_XOFFSET
                self.hit_direction = -1

            y = sge.game.height / 2
            super().__init__(x, y, sprite=paddle_sprite, checks_collisions=False)

        def event_step(self, time_passed, delta_mult):
            # Movement
            key_motion = (sge.keyboard.get_pressed(self.down_key) -
                          sge.keyboard.get_pressed(self.up_key))

            self.yvelocity = key_motion * PADDLE_SPEED

            # Keep the paddle inside the window
            if self.bbox_top < 0:
                self.bbox_top = 0
            elif self.bbox_bottom > sge.game.current_room.height:
                self.bbox_bottom = sge.game.current_room.height


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
                self.serve(-1)
            elif self.bbox_left > sge.game.current_room.width:
                self.serve(1)

            # Bouncing off of the edges
            if self.bbox_bottom > sge.game.current_room.height:
                self.bbox_bottom = sge.game.current_room.height
                self.yvelocity = -abs(self.yvelocity)
            elif self.bbox_top < 0:
                self.bbox_top = 0
                self.yvelocity = abs(self.yvelocity)

        def event_collision(self, other, xdirection, ydirection):
            if isinstance(other, Player):
                if other.hit_direction == 1:
                    self.bbox_left = other.bbox_right + 1
                else:
                    self.bbox_right = other.bbox_left - 1

                self.xvelocity = min(abs(self.xvelocity) + BALL_ACCELERATION,
                                     BALL_MAX_SPEED) * other.hit_direction
                self.yvelocity += (self.y - other.y) * PADDLE_VERTICAL_FORCE

        def serve(self, direction=None):
            if direction is None:
                direction = random.choice([-1, 1])

            self.x = self.xstart
            self.y = self.ystart

            # Next round
            self.xvelocity = BALL_START_SPEED * direction
            self.yvelocity = 0


    # Create Game object
    Game(width=640, height=480, fps=120, window_text="Pong")

    # Load sprites
    paddle_sprite = sge.gfx.Sprite(width=8, height=48, origin_x=4, origin_y=24)
    ball_sprite = sge.gfx.Sprite(width=8, height=8, origin_x=4, origin_y=4)
    paddle_sprite.draw_rectangle(0, 0, paddle_sprite.width, paddle_sprite.height,
                                 fill=sge.gfx.Color("white"))
    ball_sprite.draw_rectangle(0, 0, ball_sprite.width, ball_sprite.height,
                               fill=sge.gfx.Color("white"))

    # Load backgrounds
    layers = [sge.gfx.BackgroundLayer(paddle_sprite, sge.game.width / 2, 0, -10000,
                                      repeat_up=True, repeat_down=True)]
    background = sge.gfx.Background(layers, sge.gfx.Color("black"))

    # Create objects
    player1 = Player(1)
    player2 = Player(2)
    ball = Ball()
    objects = [player1, player2, ball]

    # Create rooms
    sge.game.start_room = sge.dsp.Room(objects, background=background)

    sge.game.mouse.visible = False


    if __name__ == '__main__':
        sge.game.start()

This is a basically complete Pong game, but it lacks some features.
First, this game doesn't keep track of the score.  It is left up to the
players to keep track of who is winning.  Second, there is no sound.  We
should fix both of these problems.

Additionally, it would be nice if our game could support joystick input.

In the next tutorial, we will improve on these points to make a Pong
game more on par with Atari's original Pong.
