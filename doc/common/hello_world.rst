First Example: Hello, world!
============================

The easiest way to learn something new is with an example.  We will
start with a very basic example: the traditional "Hello, world!"
program.  This example will just project "Hello, world!" onto the
screen.

Setting Up the Project
----------------------

First, we must create our project directory.  I will use "~/hello".
Copy an implementation to "~/hello"; I'm choosing sge-pygame, and rename
it to just "sge" (so in my example, I now have "~/hello/sge").

Next, create the game source file inside "~/hello".  I am calling it
"hello.py".

Open hello.py so you can start editing it.

Shebang
-------

All Python files which are supposed to be executed should start with
a shebang, which is a line that tells POSIX systems how to execute the
file.  In my case, the shebang is::

    #!/usr/bin/env python2

The shebang should be the very first line of the file.  You should also
make sure that the file itself uses Unix-style line endings ("\n").
Windows-style line endings ("\r\n") are often interpreted wrongly by
POSIX systems, which defeats the purpose of the shebang.

License
-------

The file is copyrighted by default, so if you do not give the file a
license, it will be illegal for anyone to copy and share the program.
You should always choose a free software license for your programs.  In
this example, I will use CC0, which is a public domain dedication
license.  You can use CC0 if you want, or you can choose another.
You can learn about various free software licenses at
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
