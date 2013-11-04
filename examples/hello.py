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
