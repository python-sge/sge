# This file is part of the Pygame SGE.
#
# The Pygame SGE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The Pygame SGE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the Pygame SGE.  If not, see <http://www.gnu.org/licenses/>.

"""
This module provides several variables which represent particular
important strings.  The purpose of these variables (listed below) is to
make typos more obvious.

The values of all of these variables are their names as strings.  If a
variable name starts with an underscore, its value excludes this
preceding underscore.  For example, a variable called ``spam`` would
have a value of ``"spam"``, and a variable called ``_1984`` would have a
value of ``"1984"``.

This module only contains these variable assignments and nothing else,
so if it is useful to you, you can add assignments to this module as
long as said assignments conform with the specification above.

.. note::

   This module does not use the convention of marking "private" members
   with a leading underscore; rather, a leading underscore is used to
   ensure that strings starting with numeric characters can be
   supported.  All variables in this module are available for use.

.. data:: sge.s._0
.. data:: sge.s._1
.. data:: sge.s._2
.. data:: sge.s._3
.. data:: sge.s._4
.. data:: sge.s._5
.. data:: sge.s._6
.. data:: sge.s._7
.. data:: sge.s._8
.. data:: sge.s._9
.. data:: sge.s.a
.. data:: sge.s.b
.. data:: sge.s.c
.. data:: sge.s.d
.. data:: sge.s.e
.. data:: sge.s.f
.. data:: sge.s.g
.. data:: sge.s.h
.. data:: sge.s.i
.. data:: sge.s.j
.. data:: sge.s.k
.. data:: sge.s.l
.. data:: sge.s.m
.. data:: sge.s.n
.. data:: sge.s.o
.. data:: sge.s.p
.. data:: sge.s.q
.. data:: sge.s.r
.. data:: sge.s.s
.. data:: sge.s.t
.. data:: sge.s.u
.. data:: sge.s.v
.. data:: sge.s.w
.. data:: sge.s.x
.. data:: sge.s.y
.. data:: sge.s.z
.. data:: sge.s._break
.. data:: sge.s.alt_left
.. data:: sge.s.alt_right
.. data:: sge.s.ampersand
.. data:: sge.s.apostrophe
.. data:: sge.s.aqua
.. data:: sge.s.asterisk
.. data:: sge.s.at
.. data:: sge.s.axis0
.. data:: sge.s.backslash
.. data:: sge.s.backspace
.. data:: sge.s.backtick
.. data:: sge.s.black
.. data:: sge.s.blue
.. data:: sge.s.bottom
.. data:: sge.s.brace_left
.. data:: sge.s.brace_right
.. data:: sge.s.bracket_left
.. data:: sge.s.bracket_right
.. data:: sge.s.button
.. data:: sge.s.caps_lock
.. data:: sge.s.carat
.. data:: sge.s.center
.. data:: sge.s.colon
.. data:: sge.s.comma
.. data:: sge.s.ctrl_left
.. data:: sge.s.ctrl_right
.. data:: sge.s.delete
.. data:: sge.s.dissolve
.. data:: sge.s.dollar
.. data:: sge.s.down
.. data:: sge.s.end
.. data:: sge.s.enter
.. data:: sge.s.equals
.. data:: sge.s.escape
.. data:: sge.s.euro
.. data:: sge.s.exclamation
.. data:: sge.s.f0
.. data:: sge.s.f1
.. data:: sge.s.f2
.. data:: sge.s.f3
.. data:: sge.s.f4
.. data:: sge.s.f5
.. data:: sge.s.f6
.. data:: sge.s.f7
.. data:: sge.s.f8
.. data:: sge.s.f9
.. data:: sge.s.f10
.. data:: sge.s.f11
.. data:: sge.s.f12
.. data:: sge.s.fade
.. data:: sge.s.fuchsia
.. data:: sge.s.gray
.. data:: sge.s.greater_than
.. data:: sge.s.green
.. data:: sge.s.hash
.. data:: sge.s.hat_center_x
.. data:: sge.s.hat_center_y
.. data:: sge.s.hat_down
.. data:: sge.s.hat_left
.. data:: sge.s.hat_right
.. data:: sge.s.hat_up
.. data:: sge.s.home
.. data:: sge.s.hyphen
.. data:: sge.s.insert
.. data:: sge.s.iris_in
.. data:: sge.s.iris_out
.. data:: sge.s.isometric
.. data:: sge.s.kp_0
.. data:: sge.s.kp_1
.. data:: sge.s.kp_2
.. data:: sge.s.kp_3
.. data:: sge.s.kp_4
.. data:: sge.s.kp_5
.. data:: sge.s.kp_6
.. data:: sge.s.kp_7
.. data:: sge.s.kp_8
.. data:: sge.s.kp_9
.. data:: sge.s.kp_divide
.. data:: sge.s.kp_enter
.. data:: sge.s.kp_equals
.. data:: sge.s.kp_minus
.. data:: sge.s.kp_multiply
.. data:: sge.s.kp_plus
.. data:: sge.s.kp_point
.. data:: sge.s.left
.. data:: sge.s.less_than
.. data:: sge.s.lime
.. data:: sge.s.maroon
.. data:: sge.s.meta_left
.. data:: sge.s.meta_right
.. data:: sge.s.middle
.. data:: sge.s.navy
.. data:: sge.s.noblur
.. data:: sge.s.num_lock
.. data:: sge.s.olive
.. data:: sge.s.orthogonal
.. data:: sge.s.pagedown
.. data:: sge.s.pageup
.. data:: sge.s.parenthesis_left
.. data:: sge.s.parenthesis_right
.. data:: sge.s.pause
.. data:: sge.s.percent
.. data:: sge.s.period
.. data:: sge.s.pixelate
.. data:: sge.s.plus
.. data:: sge.s.print_screen
.. data:: sge.s.purple
.. data:: sge.s.question
.. data:: sge.s.quote
.. data:: sge.s.red
.. data:: sge.s.right
.. data:: sge.s.scroll_lock
.. data:: sge.s.semicolon
.. data:: sge.s.shift_left
.. data:: sge.s.shift_right
.. data:: sge.s.silver
.. data:: sge.s.slash
.. data:: sge.s.smooth
.. data:: sge.s.space
.. data:: sge.s.sysrq
.. data:: sge.s.tab
.. data:: sge.s.teal
.. data:: sge.s.top
.. data:: sge.s.trackball_down
.. data:: sge.s.trackball_left
.. data:: sge.s.trackball_right
.. data:: sge.s.trackball_up
.. data:: sge.s.underscore
.. data:: sge.s.up
.. data:: sge.s.wheel_down
.. data:: sge.s.wheel_left
.. data:: sge.s.wheel_right
.. data:: sge.s.wheel_up
.. data:: sge.s.white
.. data:: sge.s.wipe_down
.. data:: sge.s.wipe_downleft
.. data:: sge.s.wipe_downright
.. data:: sge.s.wipe_left
.. data:: sge.s.wipe_matrix
.. data:: sge.s.wipe_right
.. data:: sge.s.wipe_up
.. data:: sge.s.wipe_upleft
.. data:: sge.s.wipe_upright
.. data:: sge.s.yellow
"""


# Alignment indicators
left = "left"
right = "right"
center = "center"
top = "top"
bottom = "bottom"
middle = "middle"

# Color names
white = "white"
silver = "silver"
gray = "gray"
black = "black"
red = "red"
lime = "lime"
blue = "blue"
maroon = "maroon"
green = "green"
navy = "navy"
yellow = "yellow"
fuchsia = "fuchsia"
aqua = "aqua"
olive = "olive"
purple = "purple"
teal = "teal"

# Scale methods
noblur = "noblur"
smooth = "smooth"

# Key names
_0 = "0"
_1 = "1"
_2 = "2"
_3 = "3"
_4 = "4"
_5 = "5"
_6 = "6"
_7 = "7"
_8 = "8"
_9 = "9"
a = "a"
b = "b"
c = "c"
d = "d"
e = "e"
f = "f"
g = "g"
h = "h"
i = "i"
j = "j"
k = "k"
l = "l"
m = "m"
n = "n"
o = "o"
p = "p"
q = "q"
r = "r"
s = "s"
t = "t"
u = "u"
v = "v"
w = "w"
x = "x"
y = "y"
z = "z"
period = "period"
comma = "comma"
less_than = "less_than"
greater_than = "greater_than"
slash = "slash"
question = "question"
apostrophe = "apostrophe"
quote = "quote"
colon = "colon"
semicolon = "semicolon"
exclamation = "exclamation"
at = "at"
hash = "hash"
dollar = "dollar"
percent = "percent"
carat = "carat"
ampersand = "ampersand"
asterisk = "asterisk"
parenthesis_left = "parenthesis_left"
parenthesis_right = "parenthesis_right"
hyphen = "hyphen"
underscore = "underscore"
plus = "plus"
equals = "equals"
bracket_left = "bracket_left"
bracket_right = "bracket_right"
brace_left = "brace_left"
brace_right = "brace_right"
backslash = "backslash"
backtick = "backtick"
euro = "euro"
kp_0 = "kp_0"
kp_1 = "kp_1"
kp_2 = "kp_2"
kp_3 = "kp_3"
kp_4 = "kp_4"
kp_5 = "kp_5"
kp_6 = "kp_6"
kp_7 = "kp_7"
kp_8 = "kp_8"
kp_9 = "kp_9"
kp_point = "kp_point"
kp_plus = "kp_plus"
kp_minus = "kp_minus"
kp_multiply = "kp_multiply"
kp_divide = "kp_divide"
kp_equals = "kp_equals"
kp_enter = "kp_enter"
left = "left"
right = "right"
up = "up"
down = "down"
home = "home"
end = "end"
pageup = "pageup"
pagedown = "pagedown"
tab = "tab"
space = "space"
enter = "enter"
backspace = "backspace"
delete = "delete"
shift_left = "shift_left"
shift_right = "shift_right"
ctrl_left = "ctrl_left"
ctrl_right = "ctrl_right"
alt_left = "alt_left"
alt_right = "alt_right"
meta_left = "meta_left"
meta_right = "meta_right"
caps_lock = "caps_lock"
escape = "escape"
num_lock = "num_lock"
scroll_lock = "scroll_lock"
_break = "break"
insert = "insert"
pause = "pause"
print_screen = "print_screen"
sysrq = "sysrq"
f0 = "f0"
f1 = "f1"
f2 = "f2"
f3 = "f3"
f4 = "f4"
f5 = "f5"
f6 = "f6"
f7 = "f7"
f8 = "f8"
f9 = "f9"
f10 = "f10"
f11 = "f11"
f12 = "f12"

# Mouse buttons
left = "left"
right = "right"
middle = "middle"
wheel_up = "wheel_up"
wheel_down = "wheel_down"
wheel_left = "wheel_left"
wheel_right = "wheel_right"

# Joystick input types
# "axis+" and "axis-" unfortunately must be excluded.
axis0 = "axis0"
hat_left = "hat_left"
hat_right = "hat_right"
hat_center_x = "hat_center_x"
hat_up = "hat_up"
hat_down = "hat_down"
hat_center_y = "hat_center_y"
trackball_left = "trackball_left"
trackball_right = "trackball_right"
trackball_up = "trackball_up"
trackball_down = "trackball_down"
button = "button"

# Transitions
fade = "fade"
dissolve = "dissolve"
pixelate = "pixelate"
wipe_left = "wipe_left"
wipe_right = "wipe_right"
wipe_up = "wipe_up"
wipe_down = "wipe_down"
wipe_upleft = "wipe_upleft"
wipe_upright = "wipe_upright"
wipe_downleft = "wipe_downleft"
wipe_downright = "wipe_downright"
wipe_matrix = "wipe_matrix"
iris_in = "iris_in"
iris_out = "iris_out"

# Tile grids
isometric = "isometric"
orthogonal = "orthogonal"

