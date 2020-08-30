*******
sge.dsp
*******

.. This file has been dedicated to the public domain, to the extent
   possible under applicable law, via CC0. See
   http://creativecommons.org/publicdomain/zero/1.0/ for more
   information. This file is offered as-is, without any warranty.

.. contents::

.. automodule:: sge.dsp

sge.dsp Classes
===============

sge.dsp.Game
------------

.. autoclass:: sge.dsp.Game

.. automethod:: sge.dsp.Game.__init__

sge.dsp.Game Methods
~~~~~~~~~~~~~~~~~~~~

.. automethod:: sge.dsp.Game.start

.. automethod:: sge.dsp.Game.end

.. automethod:: sge.dsp.Game.pause

.. automethod:: sge.dsp.Game.unpause

.. automethod:: sge.dsp.Game.pump_input

.. automethod:: sge.dsp.Game.regulate_speed

.. automethod:: sge.dsp.Game.refresh

.. automethod:: sge.dsp.Game.project_dot

.. automethod:: sge.dsp.Game.project_line

.. automethod:: sge.dsp.Game.project_rectangle

.. automethod:: sge.dsp.Game.project_ellipse

.. automethod:: sge.dsp.Game.project_circle

.. automethod:: sge.dsp.Game.project_polygon

.. automethod:: sge.dsp.Game.project_sprite

.. automethod:: sge.dsp.Game.project_text

sge.dsp.Game Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: sge.dsp.Game.event_step

.. automethod:: sge.dsp.Game.event_alarm

.. automethod:: sge.dsp.Game.event_key_press

.. automethod:: sge.dsp.Game.event_key_release

.. automethod:: sge.dsp.Game.event_mouse_move

.. automethod:: sge.dsp.Game.event_mouse_button_press

.. automethod:: sge.dsp.Game.event_mouse_button_release

.. automethod:: sge.dsp.Game.event_joystick

.. automethod:: sge.dsp.Game.event_joystick_axis_move

.. automethod:: sge.dsp.Game.event_joystick_hat_move

.. automethod:: sge.dsp.Game.event_joystick_trackball_move

.. automethod:: sge.dsp.Game.event_joystick_button_press

.. automethod:: sge.dsp.Game.event_joystick_button_release

.. automethod:: sge.dsp.Game.event_gain_keyboard_focus

.. automethod:: sge.dsp.Game.event_lose_keyboard_focus

.. automethod:: sge.dsp.Game.event_gain_mouse_focus

.. automethod:: sge.dsp.Game.event_lose_mouse_focus

.. automethod:: sge.dsp.Game.event_close

.. automethod:: sge.dsp.Game.event_mouse_collision

.. automethod:: sge.dsp.Game.event_paused_step

.. automethod:: sge.dsp.Game.event_paused_key_press

.. automethod:: sge.dsp.Game.event_paused_key_release

.. automethod:: sge.dsp.Game.event_paused_mouse_move

.. automethod:: sge.dsp.Game.event_paused_mouse_button_press

.. automethod:: sge.dsp.Game.event_paused_mouse_button_release

.. automethod:: sge.dsp.Game.event_paused_joystick

.. automethod:: sge.dsp.Game.event_paused_joystick_axis_move

.. automethod:: sge.dsp.Game.event_paused_joystick_hat_move

.. automethod:: sge.dsp.Game.event_paused_joystick_trackball_move

.. automethod:: sge.dsp.Game.event_paused_joystick_button_press

.. automethod:: sge.dsp.Game.event_paused_joystick_button_release

.. automethod:: sge.dsp.Game.event_paused_gain_keyboard_focus

.. automethod:: sge.dsp.Game.event_paused_lose_keyboard_focus

.. automethod:: sge.dsp.Game.event_paused_gain_mouse_focus

.. automethod:: sge.dsp.Game.event_paused_lose_mouse_focus

.. automethod:: sge.dsp.Game.event_paused_close

sge.dsp.Room
------------

.. autoclass:: sge.dsp.Room

.. automethod:: sge.dsp.Room.__init__

sge.dsp.Room Methods
~~~~~~~~~~~~~~~~~~~~

.. automethod:: sge.dsp.Room.add

.. automethod:: sge.dsp.Room.remove

.. automethod:: sge.dsp.Room.start

.. automethod:: sge.dsp.Room.get_objects_at

.. automethod:: sge.dsp.Room.project_dot

.. automethod:: sge.dsp.Room.project_line

.. automethod:: sge.dsp.Room.project_rectangle

.. automethod:: sge.dsp.Room.project_ellipse

.. automethod:: sge.dsp.Room.project_circle

.. automethod:: sge.dsp.Room.project_polygon

.. automethod:: sge.dsp.Room.project_sprite

.. automethod:: sge.dsp.Room.project_text

sge.dsp.Room Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: sge.dsp.Room.event_room_start

.. automethod:: sge.dsp.Room.event_room_resume

.. automethod:: sge.dsp.Room.event_room_end

.. automethod:: sge.dsp.Room.event_step

.. automethod:: sge.dsp.Room.event_alarm

.. automethod:: sge.dsp.Room.event_key_press

.. automethod:: sge.dsp.Room.event_key_release

.. automethod:: sge.dsp.Room.event_mouse_move

.. automethod:: sge.dsp.Room.event_mouse_button_press

.. automethod:: sge.dsp.Room.event_mouse_button_release

.. automethod:: sge.dsp.Room.event_joystick

.. automethod:: sge.dsp.Room.event_joystick_axis_move

.. automethod:: sge.dsp.Room.event_joystick_hat_move

.. automethod:: sge.dsp.Room.event_joystick_trackball_move

.. automethod:: sge.dsp.Room.event_joystick_button_press

.. automethod:: sge.dsp.Room.event_joystick_button_release

.. automethod:: sge.dsp.Room.event_gain_keyboard_focus

.. automethod:: sge.dsp.Room.event_lose_keyboard_focus

.. automethod:: sge.dsp.Room.event_gain_mouse_focus

.. automethod:: sge.dsp.Room.event_lose_mouse_focus

.. automethod:: sge.dsp.Room.event_close

.. automethod:: sge.dsp.Room.event_paused_step

.. automethod:: sge.dsp.Room.event_paused_key_press

.. automethod:: sge.dsp.Room.event_paused_key_release

.. automethod:: sge.dsp.Room.event_paused_mouse_move

.. automethod:: sge.dsp.Room.event_paused_mouse_button_press

.. automethod:: sge.dsp.Room.event_paused_mouse_button_release

.. automethod:: sge.dsp.Room.event_paused_joystick

.. automethod:: sge.dsp.Room.event_paused_joystick_axis_move

.. automethod:: sge.dsp.Room.event_paused_joystick_hat_move

.. automethod:: sge.dsp.Room.event_paused_joystick_trackball_move

.. automethod:: sge.dsp.Room.event_paused_joystick_button_press

.. automethod:: sge.dsp.Room.event_paused_joystick_button_release

.. automethod:: sge.dsp.Room.event_paused_gain_keyboard_focus

.. automethod:: sge.dsp.Room.event_paused_lose_keyboard_focus

.. automethod:: sge.dsp.Room.event_paused_gain_mouse_focus

.. automethod:: sge.dsp.Room.event_paused_lose_mouse_focus

.. automethod:: sge.dsp.Room.event_paused_close

sge.dsp.View
------------

.. autoclass:: sge.dsp.View

.. automethod:: sge.dsp.View.__init__

sge.dsp.Object
--------------

.. autoclass:: sge.dsp.Object

.. automethod:: sge.dsp.Object.__init__

sge.dsp.Object Methods
~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: sge.dsp.Object.move_x

.. automethod:: sge.dsp.Object.move_y

.. automethod:: sge.dsp.Object.collision

.. automethod:: sge.dsp.Object.destroy

.. automethod:: sge.dsp.Object.create

sge.dsp.Object Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: sge.dsp.Object.event_create

.. automethod:: sge.dsp.Object.event_destroy

.. automethod:: sge.dsp.Object.event_step

.. automethod:: sge.dsp.Object.event_alarm

.. automethod:: sge.dsp.Object.event_animation_end

.. automethod:: sge.dsp.Object.event_key_press

.. automethod:: sge.dsp.Object.event_key_release

.. automethod:: sge.dsp.Object.event_mouse_move

.. automethod:: sge.dsp.Object.event_mouse_button_press

.. automethod:: sge.dsp.Object.event_mouse_button_release

.. automethod:: sge.dsp.Object.event_joystick

.. automethod:: sge.dsp.Object.event_joystick_axis_move

.. automethod:: sge.dsp.Object.event_joystick_hat_move

.. automethod:: sge.dsp.Object.event_joystick_trackball_move

.. automethod:: sge.dsp.Object.event_joystick_button_press

.. automethod:: sge.dsp.Object.event_joystick_button_release

.. automethod:: sge.dsp.Object.event_update_position

.. automethod:: sge.dsp.Object.event_collision

.. automethod:: sge.dsp.Object.event_paused_step

.. automethod:: sge.dsp.Object.event_paused_key_press

.. automethod:: sge.dsp.Object.event_paused_key_release

.. automethod:: sge.dsp.Object.event_paused_mouse_move

.. automethod:: sge.dsp.Object.event_paused_mouse_button_press

.. automethod:: sge.dsp.Object.event_paused_mouse_button_release

.. automethod:: sge.dsp.Object.event_paused_joystick

.. automethod:: sge.dsp.Object.event_paused_joystick_axis_move

.. automethod:: sge.dsp.Object.event_paused_joystick_hat_move

.. automethod:: sge.dsp.Object.event_paused_joystick_trackball_move

.. automethod:: sge.dsp.Object.event_paused_joystick_button_press

.. automethod:: sge.dsp.Object.event_paused_joystick_button_release

