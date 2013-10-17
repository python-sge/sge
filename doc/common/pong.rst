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
