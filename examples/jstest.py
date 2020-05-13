#!/usr/bin/env python3

# Joystick Tester
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

TITLE_HEIGHT = 48
UPDATE_DELAY = 10


class glob(object):

    js_selection_sprite = None
    js_state_sprite = None
    name_font = None
    state_font = None


class Game(sge.dsp.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.event_close()

    def event_close(self):
        self.end()


class Room(sge.dsp.Room):

    def set_joystick(self):
        self.joystick_axes = []
        for i in range(sge.joystick.get_axes(self.current_joystick)):
            self.joystick_axes.append(sge.joystick.get_axis(
                self.current_joystick, i))

        self.joystick_hats = []
        for i in range(sge.joystick.get_hats(self.current_joystick)):
            self.joystick_hats.append((
                sge.joystick.get_hat_x(self.current_joystick, i),
                sge.joystick.get_hat_y(self.current_joystick, i)))

        self.joystick_balls = []
        for i in range(sge.joystick.get_trackballs(self.current_joystick)):
            self.joystick_balls.append(0)

        self.joystick_buttons = []
        for i in range(sge.joystick.get_buttons(self.current_joystick)):
            self.joystick_buttons.append(sge.joystick.get_pressed(
                self.current_joystick, i))

        glob.js_selection_sprite.draw_clear()

        title_text = 'Joystick {0} ("{1}")'.format(
            sge.joystick.get_id(self.current_joystick),
            sge.joystick.get_name(self.current_joystick))

        x = glob.js_selection_sprite.width / 2
        y = glob.js_selection_sprite.height / 2
        glob.js_selection_sprite.draw_text(
            glob.name_font, title_text, x, y, color=sge.gfx.Color("white"),
            halign="center", valign="middle")

        self.print_state()

    def print_state(self):
        lines = []

        for i in range(len(self.joystick_axes)):
            lines.append("Axis {0}: {1}".format(i, self.joystick_axes[i]))

        for i in range(len(self.joystick_hats)):
            lines.append("HAT {0}: {1}".format(
                i, "{0} x {1}".format(*self.joystick_hats[i])))

        for i in range(len(self.joystick_balls)):
            lines.append("Trackball {0}: {1}".format(
                i, "{0} x {1}".format(*self.joystick_balls[i])))

        for i in range(len(self.joystick_buttons)):
            lines.append("Button {0}: {1}".format(
                i, "Pressed" if self.joystick_buttons[i] else "Released"))

        left_text = '\n'.join([lines[i] for i in range(0, len(lines), 2)])
        right_text = '\n'.join([lines[i] for i in range(1, len(lines), 2)])

        glob.js_state_sprite.draw_clear()
        glob.js_state_sprite.draw_text(glob.state_font, left_text, 0, 0,
                                       color=sge.gfx.Color("white"))
        x = glob.js_state_sprite.width / 2
        glob.js_state_sprite.draw_text(glob.state_font, right_text, x, 0,
                                       color=sge.gfx.Color("white"))

    def event_room_start(self):
        self.current_joystick = 0
        self.changed = False
        self.ball_nonzero = False
        self.set_joystick()

    def event_step(self, time_passed, delta_mult):
        if self.changed:
            self.changed = False
            self.print_state()

        if self.ball_nonzero:
            # Reset ball motion to 0
            for i in range(len(self.joystick_balls)):
                self.joystick_balls[i] = (0, 0)

            self.changed = True
            self.ball_nonzero = False

    def event_key_press(self, key, char):
        if key == "left":
            num = sge.joystick.get_joysticks()
            if num:
                self.current_joystick -= 1
                self.current_joystick %= num
                self.set_joystick()
        elif key == "right":
            num = sge.joystick.get_joysticks()
            if num:
                self.current_joystick += 1
                self.current_joystick %= num
                self.set_joystick()
        elif key == "space":
            sge.joystick.refresh()
            self.set_joystick()

    def event_joystick_axis_move(self, js_name, js_id, axis, value):
        if (self.current_joystick in (js_name, js_id) and
                axis < len(self.joystick_axes)):
            self.joystick_axes[axis] = value

        self.changed = True

    def event_joystick_hat_move(self, js_name, js_id, hat, x, y):
        if (self.current_joystick in (js_name, js_id) and
                hat < len(self.joystick_hats)):
            self.joystick_hats[hat] = (x, y)

        self.changed = True

    def event_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        if (self.current_joystick in (js_name, js_id) and
                ball < len(self.joystick_balls)):
            self.joystick_balls[ball] = (x, y)

        self.changed = True
        self.ball_nonzero = True

    def event_joystick_button_press(self, js_name, js_id, button):
        if (self.current_joystick in (js_name, js_id) and
                button < len(self.joystick_buttons)):
            self.joystick_buttons[button] = True

        self.changed = True

    def event_joystick_button_release(self, js_name, js_id, button):
        if (self.current_joystick in (js_name, js_id) and
                button < len(self.joystick_buttons)):
            self.joystick_buttons[button] = False

        self.changed = True


def main():
    # Create Game object
    Game(640, 480)

    # Load sprites
    glob.js_selection_sprite = sge.gfx.Sprite(width=sge.game.width,
                                              height=TITLE_HEIGHT)
    glob.js_state_sprite = sge.gfx.Sprite(
        width=sge.game.width, height=(sge.game.height - TITLE_HEIGHT))

    # Load fonts
    glob.name_font = sge.gfx.Font('Liberation Sans', size=18)
    glob.state_font = sge.gfx.Font('Liberation Sans', size=14)

    # Create objects
    selection_object = sge.dsp.Object(0, 0, sprite=glob.js_selection_sprite,
                                      tangible=False)
    state_object = sge.dsp.Object(0, TITLE_HEIGHT,
                                  sprite=glob.js_state_sprite,
                                  tangible=False)
    objects = (selection_object, state_object)

    # Create rooms
    sge.game.start_room = Room(objects)

    sge.game.start()


if __name__ == '__main__':
    main()
