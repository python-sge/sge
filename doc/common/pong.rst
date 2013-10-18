Second Example: Pong
====================

Now that you've seen the basics of the SGE, it's time to create an
actual game. Although Pong might seem extremely simple, it will give you
a great foundation for developing more complex games in the future.

Setting Up the Project
----------------------

I am going to set up my project in "~/pong", and the game script is
going to be called "pong.py".  I am using Python 2, and the sge-pygame
SGE implementation.

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
necessary since "global" is a keyword in Python).  It is derived from
:class:`object`, which ensures that :class:`glob` is a new-style class
in Python 2; if you are using Python 3, all classes are new-style
classes, so this can be omitted.

The reason for having all of these variables will be explained later
when we actually use them.

The Game Class
--------------

For our Game class, we want to of course provide a way to exit the game,
and in this case, we are also going to provide a way to pause the game.
Just for the heck of it, let's also allow the player to take a
screenshot by pressing F8.  With those goals in mind, our Game class is
defined as follows::

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
number representing what button was pressed, with 0 as the first number,
so we are able to simplify the check of what button was pressed with a
simple hack: the first button (button 0) is the "No" button, and the
second button (button 1) is the "Yes" button.  The numbers these buttons
return correspond to :const:`False` and :const:`True`, respectively.

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
assign the player to: glob.player1 if it is the left player, or
glob.player2 if it is the right player.

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

Since -1 is up, 1 is down, and 0 is no movement, I now just need to
multiply ``key_motion`` by some constant value (the paddle speed I wish
to use) to get the desired vertical velocity.  The name I have chosen
for this constant is ``PADDLE_SPEED``.  Attempting to use an undefined
constant will cause an error, so let's define it now::

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
