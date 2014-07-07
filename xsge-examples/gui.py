#!/usr/bin/env python3

# Multiple Rooms Example
# Written in 2014 by Julian Marchant <onpon4@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sge
from xsge import gui


class Game(sge.Game):

    def event_game_start(self):
        sge.keyboard.set_repeat(interval=10, delay=500)

    def event_close(self):
        self.end()


class Room(sge.Room):

    def event_room_start(self):
        self.handler = gui.Handler.create()

        window = gui.Window(self.handler, 8, 8, 240, 240, title="Test window 1")
        button = gui.Button(window, 8, 8, 0, "My button")
        gui.Label(window, 8, 32, 0, "My label")
        gui.Label(window, 8, 64, 0, "my label " * 50, width=224)
        button2 = gui.Button(window, 16, 100, 5, "Another button", width=150)

        def event_press(handler=self.handler):
            gui.show_message(handler, "You just pressed my buttons!")

        button.event_press = event_press

        def event_press(handler=self.handler):
            name = gui.get_text_entry(handler, "Who are you?!")
            if name:
                m = "{}? That's a suspicious name!".format(name)
            else:
                m = "Won't talk, eh? I've got my eye on you!"

            gui.show_message(handler, m)

        button2.event_press = event_press

        window.show()

        window2 = gui.Window(self.handler, 480, 200, 320, 320,
                             title="Test window 2")
        gui.CheckBox(window2, 16, 16, 0)
        gui.RadioButton(window2, 16, 48, 0)
        gui.RadioButton(window2, 16, 80, 0)
        gui.RadioButton(window2, 16, 112, 0)
        gui.ProgressBar(window2, 16, 144, 0, 288, progress=0.5)
        gui.TextBox(window2, 16, 176, 0, width=288, text="mytext")
        window2.show()


def main():
    Game(width=800, height=600)
    gui.init()

    Room()

    sge.game.start()


if __name__ == '__main__':
    main()
