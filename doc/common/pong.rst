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


