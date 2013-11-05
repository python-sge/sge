First Example: Hello, world!
============================

The easiest way to learn something new is with an example.  We will
start with a very basic example: the traditional "Hello, world!"
program.  This example will just project "Hello, world!" onto the
screen.

Setting Up the Project
----------------------

First, we must create our project directory.  I will use "~/hello".

Next, we need to get the SGE to work with our project.  There are two
ways to do this: the most obvious way is to run the included steup.py
script from the terminal::

    ./setup.py install

This will install the SGE system-wide.

The second way, which I will use, is to simply copy the "sge" folder to
"~/hello".  This will enable the SGE to work only with this project.

Be sure to use an implementation that is compatible with the version of
Python you are using.

Next, create the game source file inside "~/hello".  I am calling it
"hello.py".

Open hello.py so you can start editing it.

Shebang
-------

All Python files which are supposed to be executed should start with
a shebang, which is a line that tells POSIX systems (such as Debian) how
to execute the file.  In my case, the shebang is::

    #!/usr/bin/env python2

The above shebang should be used if you are writing code for Python 2.
If you are using Python 3, instead use::

    #!/usr/bin/env python3

The shebang should be the very first line of the file.  You should also
make sure that the file itself uses Unix-style line endings ("\n"); this
can be done in most text editors via a drop-down list available when you
save, and is done by IDLE automatically.  Windows-style line endings
("\r\n") are often interpreted wrongly in POSIX systems, which defeats
the purpose of the shebang.

License
-------

The file is copyrighted by default, so if you do not give the file a
license, it will be illegal for anyone to copy and share the program.
You should always choose a free software license for your programs.  In
this example, I will use CC0, which is a public domain dedication
license.  You can use CC0 if you want, or you can choose another
license.  You can learn about various free software licenses at
`http://gnu.org/licenses/ <http://gnu.org/licenses/>`_.

The license text I am using for CC0 is::

    # Hello, world!
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

Place your license text just under the shebang so that it is prominent.

Imports
-------

If you are using Python 2, you should include the following lines which
replace some Python 2 behaviors with Python 3 behaviors::

    from __future__ import division
    from __future__ import absolute_import
    from __future__ import print_function
    from __future__ import unicode_literals

This collection of statements must not be preceded by any code other
than comments and the module docstring, so put them right under the
license text, or the module docstring if you have one.

Because we are using the SGE, we must import the ``sge`` library.  Add
the following line::

    import sge

With that, you should be good to go.

The Game Class
--------------

In SGE games, everything is controlled by a "game" object.  The game
object controls everything at the global level, including global events.
To define global events, we need to subclass :class:`sge.Game` and
create our own game class.  Because only one :class:`sge.Game` object is
allowed to exist in any one game, we can just call this class ``Game``::

    class Game(sge.Game):

        def event_key_press(self, key, char):
            if key == 'escape':
                self.event_close()

        def event_close(self):
            self.end()

Because our example is simple, we only need to define two events: the
close event, which occurs when the OS tells the game to close (most
typically when a close button is clicked on), and the key press event,
which occurs when a key is pressed.  We want the game to end if either
the OS tells it to close or the Esc key is pressed.

As you may have noticed, we define events by defining certain methods;
in our case, we defined methods to override the
:meth:`sge.Game.event_key_press` and :meth:`sge.Game.event_close`
methods.

Our definition of :meth:`event_close` is simple enough: we just call
:meth:`sge.Game.end`, which ends the game.  Our definition of
:meth:`event_key_press` is slightly more complicated; first we have to
check what key was pressed, indicated by the ``key`` argument.  If the
key is the Esc key, we call our :meth:`event_close` method.  The reason
for calling :meth:`event_close` instead of just calling :meth:`end` is
simple: in the future, we might want to do more than just call
:meth:`end`; perhaps, for example, we decide that we want to add a
confirmation dialog before actually quitting. By connecting the key
press event to the close event, if we do change what the close event
does, that change will also translate to the pressing of the Esc key,
avoiding needless duplication of work.

The Room Class
--------------

Next, we need to define a room class.  In the SGE, rooms are
distinguished places where things happen; for example, each level in a
game would typically be its own room, the title screen might be a room,
the credits screen might be a room, and the options menu might be a
room.  In this example, we are only going to have one room, and this
room is going to serve only one function: display "Hello, world!" in the
center of the screen.  This will be our room class::

    class Room(sge.Room):

        def event_step(self, time_passed):
            self.project_text("my_font", "Hello, world!", sge.game.width / 2,
                              sge.game.height / 2, 0, color="black",
                              halign=sge.ALIGN_CENTER, valign=sge.ALIGN_MIDDLE)

You can see that the room class is defined very similar to the game
class.  We subclass :class:`sge.Room` and add a method to override
:meth:`sge.Room.event_step`, which defines the step event of our room
class.  The step event happens over and over again, once every "frame".
You can think of frames as being like the frames in a video; each frame
makes small changes to the image on the screen and then gives you the
new image in a fraction of a second, providing an illusion of movement.

To display "Hello, world!" onto the screen, we use
:meth:`sge.Room.project_text`, which instantly displays any text we want
inside the room.  The first argument of this method is the font to use;
we don't have a font yet, but we are going to define one later and give
it the unique idetifier, ``"my_font"``.  Next is the text to display,
which for us is ``"Hello, world!"``.

The next arguments are the horizontal and vertical location of the text
in the room; we set these to half of the game's width and height,
respectively, to place the text in the center of the screen.
:data:`sge.game` is a variable that always points to the
:class:`sge.Game` object currently in use.

Following the position arguments is the Z-axis value of the projection,
which tells the SGE what to do if two objects overlap.  We don't have
anything else that the projection could overlap with, so it doesn't
matter what we set this to.  I chose ``0``, but you can choose any
number.

Now that all required arguments are defined, we are going to define the
color of the text as a keyword argument, setting it explicitly to black.

Finally, we define ``halign`` and ``valign`` as keyword arguments; these
arguments specify the horizontal and vertical alignment of the text,
respectively.

You might be wondering: why do we keep doing this every frame? Can't we
just do it once, since we're not changing the image? In fact, we can't.
:meth:`sge.Room.project_text` shows our text, but it only does so for
one frame.  You can think of it as working like a movie projector: if
you keep the projector on, you will continue to see the image, but as
soon as the projector stops projecting the image, you can no longer see
the image from the projector.  :meth:`sge.Game.project_text` and other
similar projection methods work the same way.

The main Function
-----------------

The :func:`main` function is where everything starts.  Technically,
Python doesn't require this to be a function, much less a function
called :func:`main`, but using a main function makes the code cleaner
and more well-defined.  This is what our main function will be::

    def main():
        # Create Game object
        Game()

        # Create backgrounds
        background = sge.Background((), "white")

        # Load fonts
        sge.Font(ID="my_font")

        # Create rooms
        Room(background=background)

        sge.game.start()

First, we create a :class:`Game` object; we don't need to store it in
anything since it is automatically stored in :data:`sge.game`.

Second, we create a :class:`sge.Background` object to specify what the
background looks like.  We make our background all white, with no
layers.

Third, we create our font. We don't really care what this font looks
like, so we allow the SGE to pick a font.  If you do care what font is
used, you can pass the name of a font onto the ``name`` keyword
argument.  Since we are referencing the font by ID rather than by a
variable, there is no need for us to assign the font to a variable.

Fourth, we create a room. Again, we don't need to assign it to a
variable. The only argument we pass is the background argument; we set
this to the background we created earlier.

Finally, with everything in place, we call the :meth:`sge.Game.start`
method of our game object.

If you try to run the file at this point, you won't get any results.
That's because we never called the main function.  To fix that problem,
add this to the bottom of the file, after the definition of the main
function::

    if __name__ == '__main__':
        main()

:data:`__name__` is a special Python variable; if it is set to
``"__main__"``, that means that the current module is the main module,
i.e. this file was executed rather than imported.  It is a good practice
to include this distinction between being executed and being imported in
all of your Python scripts.

The Final Result
----------------

That's it!  If you execute the script now, you will see a white screen
with black text in the center reading "Hello, world!" Pressing the Esc
key or clicking on the close button in the window will close the
program.  Congratulations on writing your first SGE program!

This is the completed Hello World program for Python 2::

    #!/usr/bin/env python2

    # Hello, world!
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


    class Game(sge.Game):

        def event_key_press(self, key, char):
            if key == 'escape':
                self.event_close()

        def event_close(self):
            self.end()


    class Room(sge.Room):

        def event_step(self, time_passed):
            self.project_text("my_font", "Hello, world!", sge.game.width / 2,
                              sge.game.height / 2, 0, color="black",
                              halign=sge.ALIGN_CENTER, valign=sge.ALIGN_MIDDLE)


    def main():
        # Create Game object
        Game()

        # Create backgrounds
        background = sge.Background((), "white")

        # Load fonts
        sge.Font(ID="my_font")

        # Create rooms
        Room(background=background)

        sge.game.start()


    if __name__ == '__main__':
        main()

Or, if you're using Python 3, this is the final result::

    #!/usr/bin/env python3

    # Hello, world!
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


    class Game(sge.Game):

        def event_key_press(self, key, char):
            if key == 'escape':
                self.event_close()

        def event_close(self):
            self.end()


    class Room(sge.Room):

        def event_step(self, time_passed):
            self.project_text("my_font", "Hello, world!", sge.game.width / 2,
                              sge.game.height / 2, 0, color="black",
                              halign=sge.ALIGN_CENTER, valign=sge.ALIGN_MIDDLE)


    def main():
        # Create Game object
        Game()

        # Create backgrounds
        background = sge.Background((), "white")

        # Load fonts
        sge.Font(ID="my_font")

        # Create rooms
        Room(background=background)

        sge.game.start()


    if __name__ == '__main__':
        main()

Now that you have built your first basic program, you are ready to make
a real game: Pong.
