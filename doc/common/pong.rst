Second Example: Pong
====================

Now that you've seen the basics of the SGE, it's time to create an
actual game. Although Pong might seem extremely simple, it will give you
a great foundation for developing more complex games in the future.

Setting Up the Project
----------------------

I am going to set up my project in "~/pong", and the game script is
going to be called "pong.py".  I am using Python 2.

I am going to open pong.py and add the appropriate shebang, my copyright
notice (I am choosing the CC0 license), and my imports.  This is what I
have so far::

    #!/usr/bin/env python2

    # Pong
    # Written in 2013 by Julian Marchant <onpon4@riseup.net>
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

    import sge

Global Variables
----------------

For our implementation of Pong, we are going to store a few variables
that can be accessed conveniently by everybody: in a word, "global"
variables.

Of course, one way we could do this is to actually use global variables.
However, using this approach has a significant disadvantage: in Python,
local variables take precedence over global variables, so to assign to
a global variable within a function, you have to declare it with the
``global`` keyword.  If we forget to do this, the resulting bugs can be
difficult to solve.

So we are going to use a different approach: a container class.  Put
simply, this is a class that contains only class attributes that we will
use as variables.  Our container class looks like this::

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

I call the class "glob" as a shorthand for "global" (the shorthand is
necessary since ``global`` is a keyword in Python).  It is derived from
:class:`object`, which ensures that :class:`glob` is a new-style class
in Python 2; if you are using Python 3, all classes are new-style
classes, so this can be omitted.

The reason for having all of these variables will be explained later
when we actually use them.

The Game Class
--------------

For our :class:`Game` class, we want to of course provide a way to exit
the game, and in this case, we are also going to provide a way to pause
the game.  Just for the heck of it, let's also allow the player to take
a screenshot by pressing F8.  With those goals in mind, our Game class
is defined as follows::

    class Game(sge.Game):

        def event_key_press(self, key, char):
            if key == 'f8':
                sge.Sprite.from_screenshot().save('screenshot.jpg')
            elif key == 'escape':
                self.event_close()
            elif key in ('p', 'enter'):
                self.pause()

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

The first event we define is the key press event.  When the F8 key is
pressed, we create a sprite from a screenshot using the
:meth:`sge.Sprite.from_screenshot` class method, then save that sprite
as "screenshot.jpg".  When the Esc key is pressed, we close the game by
calling the close event.  When the "P" or Enter key is pressed, we use
:meth:`sge.Game.pause` to pause the game.  "P" and Enter are checked
together by grouping them in a tuple and then using the ``in`` operator,
rather than checking them separately, because it's easier to read and
less verbose.

The next event we define is the close event.  Unlike our last example,
here, we first ask the player to confirm whether or not they want to
close before actually closing.  :func:`sge.show_message` returns a
number representing what button was pressed, with ``0`` as the first
number, so we are able to simplify the check of what button was pressed
with a simple hack: the first button (button 0) is the "No" button, and
the second button (button 1) is the "Yes" button.  The numbers these
buttons return correspond to :const:`False` and :const:`True`,
respectively.

Next, we need to define "paused" events, because normal events are
suspended while the game is paused. The "paused" close event just does
the same thing as the regular "close" event, to allow the game to be
exited without unpausing the game first.  The "paused" key event, on the
other hand, unpauses the game if any key other than the Esc key (which
ends the game) is pressed.

The Player Class
----------------

The Player class is going to be a subclass of :class:`sge.StellarClass`,
which is the class that represents individual objects in the SGE.  This
class is used for players, bullets, floors, walls, and pretty much
anything else you can think of.

For the Player class, we are actually going to do something a bit
unusual: we are going to extend :meth:`sge.StellarClass.__init__` (the
constructor method)::

    class Player(sge.StellarClass):

        def __init__(self, player=1):
            if player == 1:
                self.up_key = "w"
                self.down_key = "s"
                x = 32
                glob.player1 = self
                self.hit_direction = 1
            else:
                self.up_key = "up"
                self.down_key = "down"
                x = sge.game.width - 32
                glob.player2 = self
                self.hit_direction = -1

            y = sge.game.height / 2
            super(Player, self).__init__(x, y, 0, sprite="paddle")

As you can see, our extended :meth:`__init__` now only takes one
argument indicating the player: ``1`` for the left player, and any other
value (such as ``2``) for the right player.  Everything else is then
inferred from that: the controls (you will see why we are storing the
controls like this in a minute), the horizontal location, and the
direction the paddle hits (``1`` for right, ``-1`` for left).  As a
bonus, we also use this information to decide what "global" variable to
assign the player to: :attr:`glob.player1` if it is the left player, or
:attr:`glob.player2` if it is the right player.

Keep in mind that you must never *override*
:meth:`sge.StellarClass.__init__`; you should only extend it.  This is
why we have the last line.  The :func:`super` function allows us to call
the corresponding method in the parent class, making our new
:meth:`__init__` an extension rather than an override.  If you are using
Python 3, the arguments I specified do not need to be passed to
:func:`super`; in that case, replace ``super(Player, self)`` with just
``super()``.

Next up, we need to add code to allow the paddles to move.  The easiest
place to do this is in the step event::

    def event_step(self, time_passed):
        # Movement
        key_motion = (sge.get_key_pressed(self.down_key) -
                      sge.get_key_pressed(self.up_key))

        self.yvelocity = key_motion * PADDLE_SPEED

        # Keep the paddle inside the window
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom > sge.game.height:
            self.bbox_bottom = sge.game.height

The first thing we do is check whether the paddle's assigned down key is
pressed and whether the assigned up key is pressed.  The simplest way to
do this is to use an if statement, but instead, I subtracted the result
for the up key from the result for the down key.  Since the returned
values are equivalent to ``1`` and ``0`` in subtraction, key_motion will
become ``-1`` if only the up key is pressed, ``1`` if only the down key
is pressed, and ``0`` if neither or both of the keys are pressed.  This
method of figuring out the desired direction not only is a lot simpler
than an if statement, but also handles the condition of opposite
directions being pressed at the same time properly.

Since ``-1`` is up, ``1`` is down, and ``0`` is no movement, I now just
need to multiply ``key_motion`` by some constant value (the paddle speed
I wish to use) to get the desired vertical velocity.  The name I have
chosen for this constant is :const:`PADDLE_SPEED`.  Attempting to use an
undefined constant will cause an error, so let's define it now::

    PADDLE_SPEED = 4

This should be placed in the global namespace, probably right after your
imports.  I chose ``4`` to be the value of this constant because I found
it to be the best balance between precision and speed.

As you may have figured out, :attr:`sge.StellarClass.yvelocity` is a
special attribute.  In simple terms, the SGE automatically adds this
number to the vertical position of the object every frame, creating an
illusion of continuous movement.

With just this, the players will be able to move the paddles off of the
screen, and we don't want this.  To prevent it, we check the paddle's
:attr:`sge.StellarClass.bbox_top` and
:attr:`sge.StellarClass.bbox_bottom` attributes to see if they are above
or below the screen, respectively, and then set them to the respective
edge of the screen if they are.

The Ball Class
--------------

Once again, the Ball class is going to be a subclass of
:class:`sge.StellarClass`.  Once again, we are going to start by
extending the constructor method::

    class Ball(sge.StellarClass):

        def __init__(self):
            x = sge.game.width / 2
            y = sge.game.height / 2
            super(Ball, self).__init__(x, y, 1, sprite="ball")

This extension is more simple than :class:`Player`'s: our extension
simply removes all arguments from the constructor method and hard-codes
values to pass on to :meth:`sge.StellarClass.__init__`.

When the ball is created, we want to immediately serve it to a player.
To achieve that, we are going to define the create event, which occurs
whenever an object of the class is created::

    def event_create(self):
        self.serve()

We are defining :func:`Ball.serve` to achieve serving the ball because
there are other situations when the ball needs to be served, namely
whenever a player scores.  This will be our serve method::

    def serve(self, direction=1):
        self.x = self.xstart
        self.y = self.ystart

        # Next round
        self.xvelocity = BALL_START_SPEED * direction
        self.yvelocity = 0

In a nutshell, we set the ball back to the its starting position (which
is the center of the screen) and reset its movement based on an argument
called ``direction``, which will be 1 (for right) or -1 (for left).  We
multiply this by a constant called BALL_START_SPEED; let's define this
constant now, right below our definition of the PADDLE_SPEED constant::

    BALL_START_SPEED = 2

As it is, the ball will pass through the paddles, which is not what we
want; we want the ball to bounce off of the paddles.  We will achieve
that with a collision event::

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

We also need to define three more constants::

    BALL_ACCELERATION = 0.2
    BALL_MAX_SPEED = 15
    PADDLE_VERTICAL_FORCE = 1 / 12

The collision event occurs whenever another object touches this object.
when this happens, we check if the other object is an instance of the
:class:`Player` class; if it is, we check the other object's
:attr:`hit_direction`; if it's ``1``, we place the left side of the
ball's bounding box just to the right of the right side of the paddle's
bounding box, then we make the ball's horizontal velocity positive and
add a constant, ``BALL_ACCELERATION``, to it; this will cause the ball
to slowly speed up as the game progresses.  If :attr:`hit_direction` is
something other than ``1``, we assume that the paddle hits to the left;
the behavior is identical to the behavior of hitting to the right, but
opposite.

Although accelerating the ball makes the gameplay more fun, we must not
let the ball go too fast.  Remember that movement is much like an
animation; the ball changes its position from one position to another;
the greater the speed, the bigger the difference.  Movement perceived is
only an illusion.  As a result, if the ball goes too fast, it can
pass right through a paddle without a collision ever being detected.  To
prevent this, we limit the speed the ball can go at by a constant; in
general, a good value to choose is one that is slightly less than the
width (in the case of horizontal movement) or height (in the case of
vertical movement) of the two objects that need to detect collisions
with each other added together.  This method only works reliably if one
of the objects is not moving; if both of the objects are moving, what
maximum speed they should be moving at is more complicated, but in this
case, the paddle is horizontally stationary.  We are later going to set
the width of both the paddle and the ball to ``8``, so we will set the
maximum ball speed to ``15`` (i.e. ``8 + 8 - 1``).

Since the game would be rather dull if the players couldn't control the
direction of the ball, so we allow the players to control the ball by
adding the difference between the ball and paddle's vertical positions
(which are going to be their centers) multiplied by a constant to the
ball's vertical velocity.

There are two remaining problems with our ball class: first, if the ball
passes a player, it doesn't return.  Second, if the ball reaches the
edge of the screen, it will just float off and be impossible to retrieve
by the receiving player.  This actually would be realistic behavior, but
it wouldn't be very fun.  We will fix both of these problems in the step
event::

    def event_step(self, time_passed):
        # Scoring
        if self.bbox_right < 0:
            self.serve(-1)
        elif self.bbox_left > sge.game.width:
            self.serve(1)

        # Bouncing off of the edges
        if self.bbox_bottom > sge.game.height:
            self.bbox_bottom = sge.game.height
            self.yvelocity = -abs(self.yvelocity)
        elif self.bbox_top < 0:
            self.bbox_top = 0
            self.yvelocity = abs(self.yvelocity)

Since we have our :meth:`serve` method, we simply need to call it when
the ball passes one of the players and goes horizontally outside the
screen.  For bouncing off the edges, we use a similar method to the
method we used to keep the paddles inside the view; the main difference
is we also set the ball's vertical velocity to move away from the edge;
if it collided with the bottom, the vertical velocity is made negative,
and if it collided with the top, the vertical velocity is made positive.

The main Function
-----------------

Let's make our Pong game playable now by defining the :func:`main`
function::

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

        # Load backgrounds
        layers = (sge.BackgroundLayer("ball", sge.game.width / 2, 0, -10000,
                                      xrepeat=False),)
        background = sge.Background (layers, "black")

        # Create objects
        Player(1)
        Player(2)
        glob.ball = Ball()
        objects = (glob.player1, glob.player2, glob.ball)

        # Create rooms
        room1 = sge.Room(objects, background=background)

        sge.game.start()


    if __name__ == '__main__':
        main()

Since the graphics of Pong are so simple, we are dynamically generating
them rather than loading existing images.  We are also generating a
background with a line in the middle by using a
:class:`sge.BackgroundLayer` object. Background layers basically tell a
background how to tile a particular sprite in order to decorate the
background.  In our case, we take the ball sprite (since it is just a
white square; no need to create an entirely new one) and tile it only
vertically in the horizontal center of the screen (vertically at y=0,
but this doesn't matter because the sprite is being tiled infinitely in
the vertical direction).

We set the game to run at 120 frames per second because it's hard to
play Pong with digital controls, and a higher frame rate helps minimize
this difficulty.

Pong Without Scoring or Sound
-----------------------------

This is what we have so far::

    #!/usr/bin/env python2

    # Pong
    # Written in 2013 by Julian Marchant <onpon4@riseup.net>
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

    import sge
    
    PADDLE_SPEED = 4
    PADDLE_VERTICAL_FORCE = 1 / 12
    BALL_START_SPEED = 2
    BALL_ACCELERATION = 0.2
    BALL_MAX_SPEED = 15


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

        def event_key_press(self, key, char):
            if key == 'f8':
                sge.Sprite.from_screenshot().save('screenshot.jpg')
            elif key == 'escape':
                self.event_close()
            elif key in ('p', 'enter'):
                self.pause()

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

        def __init__(self, player=1):
            if player == 1:
                self.up_key = "w"
                self.down_key = "s"
                x = 32
                glob.player1 = self
                self.hit_direction = 1
            else:
                self.up_key = "up"
                self.down_key = "down"
                x = sge.game.width - 32
                glob.player2 = self
                self.hit_direction = -1

            y = sge.game.height / 2
            super(Player, self).__init__(x, y, 0, sprite="paddle")

        def event_step(self, time_passed):
            # Movement
            key_motion = (sge.get_key_pressed(self.down_key) -
                          sge.get_key_pressed(self.up_key))

            self.yvelocity = key_motion * PADDLE_SPEED

            # Keep the paddle inside the window
            if self.bbox_top < 0:
                self.bbox_top = 0
            elif self.bbox_bottom > sge.game.height:
                self.bbox_bottom = sge.game.height


    class Ball(sge.StellarClass):

        def __init__(self):
            x = sge.game.width / 2
            y = sge.game.height / 2
            super(Ball, self).__init__(x, y, 1, sprite="ball")

        def event_create(self):
            self.serve()

        def event_step(self, time_passed):
            # Scoring
            if self.bbox_right < 0:
                self.serve(-1)
            elif self.bbox_left > sge.game.width:
                self.serve(1)

            # Bouncing off of the edges
            if self.bbox_bottom > sge.game.height:
                self.bbox_bottom = sge.game.height
                self.yvelocity = -abs(self.yvelocity)
            elif self.bbox_top < 0:
                self.bbox_top = 0
                self.yvelocity = abs(self.yvelocity)

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

        def serve(self, direction=1):
            self.x = self.xstart
            self.y = self.ystart

            # Next round
            self.xvelocity = BALL_START_SPEED * direction
            self.yvelocity = 0


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

        # Load backgrounds
        layers = (sge.BackgroundLayer("ball", sge.game.width / 2, 0, -10000,
                                      xrepeat=False),)
        background = sge.Background (layers, "black")

        # Create objects
        Player(1)
        Player(2)
        glob.ball = Ball()
        objects = (glob.player1, glob.player2, glob.ball)

        # Create rooms
        room1 = sge.Room(objects, background=background)

        sge.game.start()


    if __name__ == '__main__':
        main()

This is a playable Pong game; there are two paddles and a ball, and the
ball returns any time it leaves the left or right side of the screen.
Unfortunately, though, it is at this point less like Pong and more like
the Magnavox Odyssey; there is no scoring, so you have to keep track of
this manually, and there is no sound.  Let's fix those problems.

Adding Scoring
--------------

It's a little weird to have a video game that doesn't keep score, so we
will now add a proper scoring system to our Pong game.  Each player will
get one point whenever the ball passes by the other player, and whoever
gets 10 points first will win.

Let's start by defining some constants::

    POINTS_TO_WIN = 10
    TEXT_OFFSET = 16

There are a couple of ways to display the score.  The most obvious way
is to project the score each frame, but we are instead going to create a
custom sprite, an object to display that sprite, and re-draw to it as
needed.  The reason for this is actually because of the implementation
I'm using; the information specific to the Pygame SGE warns that
projection methods are inefficient.  (In fact, the Pygame SGE implements
these methods by creating a whole new sprite and object every single
frame, which is an incredibly wasteful method.)  Other than that, using
this method for more complicated HUDs can prove to be much easier and
more organized than projecting directly onto the room, so it's good to
know how to do it.

HUD sprite and object
~~~~~~~~~~~~~~~~~~~~~

First, we need to create the HUD sprite and the HUD object.  We will do
this in the :func:`main` function.

Add one more sprite to the list of sprites::

    glob.hud_sprite = sge.Sprite(width=320, height=160, origin_x=160,
                                 origin_y=0)

Create a HUD object::

    hud = sge.StellarClass(sge.game.width / 2, 0, -10, sprite=glob.hud_sprite,
                           detects_collisions=False)

And finally, add the HUD object to the list of initial objects::

    objects = (glob.player1, glob.player2, glob.ball, hud)

We want to put the HUD sprite in a globally-accessible variable because
we are going to change the score table by changing the sprite directly.
The HUD object, on the other hand, never needs to be changed; it just
needs to be in the room.

The size of the HUD sprite is arbitrary. Most of it is going to be
invisible, so our only requirement for it is that it needs to be large
enough to fit the rendered text.

Font
~~~~

Next, we need to load a font.  To do so, we will add this (I am putting
it between the background and object creations, but you can put them
anywhere in :func:`main` as long as it's before the game is started)::

    # Load fonts
    sge.Font('Liberation Mono', ID="hud", size=48)

For the first argument of :meth:`sge.Font.__init__`, we specify one of
two things: either the name of a system font, or the name of a font file
that we are distributing with our game in our data folder.  For
simplicity, we will use a system font for now.  I chose Liberation Mono,
but you can choose any font you like.

.. note::

   What system fonts are available on a given system is not standardized
   in any way.  If you specify a system font and that system font is not
   available, the SGE will choose what font to use arbitrarily.  For
   this reason, you should never use system fonts in your games except
   as a temporary placeholder.

Score property
~~~~~~~~~~~~~~

Now let's add score attributes to the players.  Because we want to
refresh the HUD every time the score changes, we are going to make these
score attributes a property of the :class:`Player` class::

    @property
    def score(self):
        return self.v_score

    @score.setter
    def score(self, value):
        if value != self.v_score:
            self.v_score = value
            refresh_hud()

:func:`refresh_hud` will be the function we define later on to refresh
the HUD.

Next, we need to initialize :attr:`v_score`.  We will do this in the
create event::

    def event_create(self):
        self.v_score = 0

The reason we initialize :attr:`v_score` directly is because
:func:`refresh_hud` is going to need both player's scores; if we call it
before both players' scores are initialized, we will get an error.

Refresh HUD Function
~~~~~~~~~~~~~~~~~~~~

Now that the score property is defined, let's add that function::

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

First we clear the sprite with :meth:`sge.Sprite.draw_clear`, then we
draw both player's scores on it; player 1's score goes on the left, and
player 2's score goes on the right.  We use :const:`TEXT_OFFSET` to make
it look nicer; if you set TEXT_OFFSET to ``0``, you will notice that it
looks a little ugly because the text is right next to the line and right
below the top of the screen.

The way it is now, the score won't start being displayed until someone
scores, which is not what we want.  To prevent this, we want to call
:func:`refresh_hud` somewhere when the game starts.  I am choosing the
create event of :class:`Ball`, because the ball is created after both of
the players (and so its create event will always execute after both of
the player objects').

Adding Points
~~~~~~~~~~~~~

We need to make the players actually get points for the scoring system
to be of any use.  This is what we currently have in the step event
of :class:`Ball`::

    # Scoring
    if self.bbox_right < 0:
        self.serve(-1)
    elif self.bbox_left > sge.game.width:
        self.serve(1)

Let's add some lines to increase the players' score::

    # Scoring
    if self.bbox_right < 0:
        glob.player2.score += 1
        self.serve(-1)
    elif self.bbox_left > sge.game.width:
        glob.player1.score += 1
        self.serve(1)

Now, every time the ball passes a player, the opposite player will get a
point.

Win Condition
~~~~~~~~~~~~~

At this point, the game will go on forever until the players decide to
stop.  That's not what we want; we want the first player to get 10
points to be declared the winner.  We will handle this in
:meth:`Ball.serve`.  This is what we have so far::

    def serve(self, direction=1):
        self.x = self.xstart
        self.y = self.ystart

        # Next round
        self.xvelocity = BALL_START_SPEED * direction
        self.yvelocity = 0

Replace that with this::

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

That's a lot of extra code.  First, we check if both players' scores are
less than :const:`POINTS_TO_WIN`.  If it is, that means the game is
still in progress, so we start the next round as the function did
previously.  Otherwise, we stop the ball, and then we draw "WIN" on the
winner's side, and "LOSE" on the loser's side.  I used two conditional
expressions to achieve this because it's quick, and if by some freak
accident (perhaps the result of a "2-balls mod" or something) both
players get 10 points at the same time, it will be considered a loss for
both players.

We will also set :attr:`glob.game_in_progress` to False, so that it can
be understood by other functions and methods that a game is not
currently in progress.  We will use this later to give the pause keys a
secondary function of starting a new game.

Adding Sound
------------

There are three sounds we want to add: one for when the ball hits a
paddle, one for when the ball hits a wall, and one for when a player
scores.

There are many ways you can get these sounds.  The easiest way is to
find them on a website that has free culture sound effects available.
A good place to search for such assets is `OpenGameArt.org
<http://opengameart.org>`_.  Another easy way if you only need simple
sound effects, and the method I used, is to generate them with a free
software program called `sfxr
<http://www.drpetter.se/project_sfxr.html>`_.  Whatever method you use,
once you have your three sound effects, set their file names to
"bounce", "bounce_wall", and "score", plus whatever extension is
appropriate.  Make sure to use a format supported by the SGE
implementation used; in my case, I can use WAV and Ogg Vorbis sound
effects, and my sound files are all WAV format.

Create a folder in the same location as pong.py called "data".  Within
the "data" folder, create another folder called "sounds".

.. note::

   Directories are not case-sensitive on all systems (most notably, they
   are not case-sensitive on Windows), but on POSIX systems in
   particular (such as Debian and Apple OS X), "data" is different from
   "Data".  Because of this, don't get into the habit of capitalizing
   the names of these folders; it's "data", not "Data", and it's
   "sounds", not "Sounds".

Put your three sound effects, which in my case are now named
"bounce.wav", "bounce_wall.wav", and "score.wav", into data/sounds.

Loading The Sounds
~~~~~~~~~~~~~~~~~~

To use sound effects, we first need to load them.  We will do so in the
:func:`main` function.  I am putting this code after the code that loads
the font and before the code that creates the objects::

    # Load sounds
    glob.bounce_sound = sge.Sound('bounce.wav')
    glob.bounce_wall_sound = sge.Sound('bounce_wall.wav')
    glob.score_sound = sge.Sound('score.wav')

Playing The Sounds
~~~~~~~~~~~~~~~~~~

This part is extremely simple.  Just call :meth:`sge.Sound.play` in the
proper places.

Here::

    # Scoring
    if self.bbox_right < 0:
        glob.player2.score += 1
        glob.score_sound.play()
        self.serve(-1)
    elif self.bbox_left > sge.game.width:
        glob.player1.score += 1
        glob.score_sound.play()
        self.serve(1)

Here::

    # Bouncing off of the edges
    if self.bbox_bottom > sge.game.height:
        self.bbox_bottom = sge.game.height
        self.yvelocity = -abs(self.yvelocity)
        glob.bounce_wall_sound.play()
    elif self.bbox_top < 0:
        self.bbox_top = 0
        self.yvelocity = abs(self.yvelocity)
        glob.bounce_wall_sound.play()

And here::

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

Restarting The Game
-------------------

One last touch: we're going to allow the game to be restarted.  We do
this by modifying the key press event for :class:`Game`, specifically
the keys that normally pause the game::

    elif key in ('p', 'enter'):
        if glob.game_in_progress:
            self.pause()
        else:
            glob.game_in_progress = True
            self.current_room.start()

If the game is in progress, we pause the game, as before.  Otherwise, we
set :attr:`glob.game_in_progres` to :const:`True` and call the current
room's :meth:`start` method, which resets and starts the room.

The Final Result
----------------

Congratulations! You have completed your first real game.  This is the
final result if you are using Python 2::

    #!/usr/bin/env python2

    # Pong
    # Written in 2013 by Julian Marchant <onpon4@riseup.net>
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

        def event_key_press(self, key, char):
            if key == 'f8':
                sge.Sprite.from_screenshot().save('screenshot.jpg')
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
                self.up_key = "w"
                self.down_key = "s"
                x = 32
                glob.player1 = self
                self.hit_direction = 1
            else:
                self.up_key = "up"
                self.down_key = "down"
                x = sge.game.width - 32
                glob.player2 = self
                self.hit_direction = -1

            y = sge.game.height / 2
            super(Player, self).__init__(x, y, 0, sprite="paddle")

        def event_step(self, time_passed):
            # Movement
            key_motion = (sge.get_key_pressed(self.down_key) -
                          sge.get_key_pressed(self.up_key))

            self.yvelocity = key_motion * PADDLE_SPEED

            # Keep the paddle inside the window
            if self.bbox_top < 0:
                self.bbox_top = 0
            elif self.bbox_bottom > sge.game.height:
                self.bbox_bottom = sge.game.height


    class Ball(sge.StellarClass):

        def __init__(self):
            x = sge.game.width / 2
            y = sge.game.height / 2
            super(Ball, self).__init__(x, y, 1, sprite="ball")

        def event_create(self):
            refresh_hud()
            self.serve()

        def event_step(self, time_passed):
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

And this is the final result if you are using Python 3::

    #!/usr/bin/env python3

    # Pong
    # Written in 2013 by Julian Marchant <onpon4@riseup.net>
    #
    # To the extent possible under law, the author(s) have dedicated all
    # copyright and related and neighboring rights to this software to the
    # public domain worldwide. This software is distributed without any
    # warranty.
    #
    # You should have received a copy of the CC0 Public Domain Dedication
    # along with this software. If not, see
    # <http://creativecommons.org/publicdomain/zero/1.0/>.

    import sge
    
    PADDLE_SPEED = 4
    PADDLE_VERTICAL_FORCE = 1 / 12
    BALL_START_SPEED = 2
    BALL_ACCELERATION = 0.2
    BALL_MAX_SPEED = 15
    POINTS_TO_WIN = 10
    TEXT_OFFSET = 16


    class glob:

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

        def event_key_press(self, key, char):
            if key == 'f8':
                sge.Sprite.from_screenshot().save('screenshot.jpg')
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
                self.up_key = "w"
                self.down_key = "s"
                x = 32
                glob.player1 = self
                self.hit_direction = 1
            else:
                self.up_key = "up"
                self.down_key = "down"
                x = sge.game.width - 32
                glob.player2 = self
                self.hit_direction = -1

            y = sge.game.height / 2
            super().__init__(x, y, 0, sprite="paddle")

        def event_step(self, time_passed):
            # Movement
            key_motion = (sge.get_key_pressed(self.down_key) -
                          sge.get_key_pressed(self.up_key))

            self.yvelocity = key_motion * PADDLE_SPEED

            # Keep the paddle inside the window
            if self.bbox_top < 0:
                self.bbox_top = 0
            elif self.bbox_bottom > sge.game.height:
                self.bbox_bottom = sge.game.height


    class Ball(sge.StellarClass):

        def __init__(self):
            x = sge.game.width / 2
            y = sge.game.height / 2
            super().__init__(x, y, 1, sprite="ball")

        def event_create(self):
            refresh_hud()
            self.serve()

        def event_step(self, time_passed):
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
