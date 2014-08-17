*******
Classes
*******

sge.Game
========

.. autoclass:: sge.Game

sge.Game Methods
----------------

.. automethod:: sge.Game.__init__

.. automethod:: sge.Game.start

.. automethod:: sge.Game.end

.. automethod:: sge.Game.pause

.. automethod:: sge.Game.unpause

.. automethod:: sge.Game.pump_input

.. automethod:: sge.Game.regulate_speed

.. automethod:: sge.Game.refresh

.. automethod:: sge.Game.register_class

.. automethod:: sge.Game.set_alarm

.. automethod:: sge.Game.get_alarm

.. automethod:: sge.Game.project_dot

.. automethod:: sge.Game.project_line

.. automethod:: sge.Game.project_rectangle

.. automethod:: sge.Game.project_ellipse

.. automethod:: sge.Game.project_circle

.. automethod:: sge.Game.project_sprite

.. automethod:: sge.Game.project_text

sge.Game Event Methods
----------------------

.. automethod:: sge.Game.event_game_start

.. automethod:: sge.Game.event_game_end

.. automethod:: sge.Game.event_step

.. automethod:: sge.Game.event_alarm

.. automethod:: sge.Game.event_key_press

.. automethod:: sge.Game.event_key_release

.. automethod:: sge.Game.event_mouse_move

.. automethod:: sge.Game.event_mouse_button_press

.. automethod:: sge.Game.event_mouse_button_release

.. automethod:: sge.Game.event_joystick_axis_move

.. automethod:: sge.Game.event_joystick_hat_move

.. automethod:: sge.Game.event_joystick_trackball_move

.. automethod:: sge.Game.event_joystick_button_press

.. automethod:: sge.Game.event_joystick_button_release

.. automethod:: sge.Game.event_gain_keyboard_focus

.. automethod:: sge.Game.event_lose_keyboard_focus

.. automethod:: sge.Game.event_gain_mouse_focus

.. automethod:: sge.Game.event_lose_mouse_focus

.. automethod:: sge.Game.event_close

.. automethod:: sge.Game.event_mouse_collision

.. automethod:: sge.Game.event_mouse_collision_left

.. automethod:: sge.Game.event_mouse_collision_right

.. automethod:: sge.Game.event_mouse_collision_top

.. automethod:: sge.Game.event_mouse_collision_bottom

.. automethod:: sge.Game.event_paused_key_press

.. automethod:: sge.Game.event_paused_key_release

.. automethod:: sge.Game.event_paused_mouse_move

.. automethod:: sge.Game.event_paused_mouse_button_press

.. automethod:: sge.Game.event_paused_mouse_button_release

.. automethod:: sge.Game.event_paused_joystick_axis_move

.. automethod:: sge.Game.event_paused_joystick_hat_move

.. automethod:: sge.Game.event_paused_joystick_trackball_move

.. automethod:: sge.Game.event_paused_joystick_button_press

.. automethod:: sge.Game.event_paused_joystick_button_release

.. automethod:: sge.Game.event_paused_gain_keyboard_focus

.. automethod:: sge.Game.event_paused_lose_keyboard_focus

.. automethod:: sge.Game.event_paused_gain_mouse_focus

.. automethod:: sge.Game.event_paused_lose_mouse_focus

.. automethod:: sge.Game.event_paused_close

sge.Sprite
==========

.. autoclass:: sge.Sprite

sge.Sprite Methods
------------------

.. automethod:: sge.Sprite.__init__

.. automethod:: sge.Sprite.append_frame

.. automethod:: sge.Sprite.insert_frame

.. automethod:: sge.Sprite.delete_frame

.. automethod:: sge.Sprite.draw_dot

.. automethod:: sge.Sprite.draw_line

.. automethod:: sge.Sprite.draw_rectangle

.. automethod:: sge.Sprite.draw_ellipse

.. automethod:: sge.Sprite.draw_circle

.. automethod:: sge.Sprite.draw_sprite

.. automethod:: sge.Sprite.draw_text

.. automethod:: sge.Sprite.draw_erase

.. automethod:: sge.Sprite.draw_clear

.. automethod:: sge.Sprite.draw_lock

.. automethod:: sge.Sprite.draw_unlock

.. automethod:: sge.Sprite.save

.. automethod:: sge.Sprite.destroy

.. automethod:: sge.Sprite.from_tileset

.. automethod:: sge.Sprite.from_screenshot

sge.BackgroundLayer
===================

.. autoclass:: sge.BackgroundLayer

sge.BackgroundLayer Methods
---------------------------

.. automethod:: sge.BackgroundLayer.__init__

.. automethod:: sge.BackgroundLayer.destroy

sge.Background
==============

.. autoclass:: sge.Background

sge.Background Methods
----------------------

.. automethod:: sge.Background.__init__

sge.Sound
=========

.. autoclass:: sge.Sound

sge.Sound Methods
-----------------

.. automethod:: sge.Sound.__init__

.. automethod:: sge.Sound.play

.. automethod:: sge.Sound.stop

.. automethod:: sge.Sound.pause

.. automethod:: sge.Sound.unpause

.. automethod:: sge.Sound.destroy

.. automethod:: sge.Sound.stop_all

sge.Music
=========

.. autoclass:: sge.Music

sge.Music Methods
-----------------

.. automethod:: sge.Music.__init__

.. automethod:: sge.Music.play

.. automethod:: sge.Music.queue

.. automethod:: sge.Music.destroy

.. automethod:: sge.Music.stop

.. automethod:: sge.Music.pause

.. automethod:: sge.Music.unpause

.. automethod:: sge.Music.clear_queue

sge.Font
========

.. autoclass:: sge.Font

sge.Font Methods
----------------

.. automethod:: sge.Font.__init__

.. automethod:: sge.Font.get_width

.. automethod:: sge.Font.get_height

.. automethod:: sge.Font.from_sprite

sge.Object
==========

.. autoclass:: sge.Object

sge.Object Methods
------------------

.. automethod:: sge.Object.__init__

.. automethod:: sge.Object.collision

.. automethod:: sge.Object.set_alarm

.. automethod:: sge.Object.get_alarm

.. automethod:: sge.Object.destroy

.. automethod:: sge.Object.create

sge.Object Event Methods
------------------------

.. automethod:: sge.Object.event_create

.. automethod:: sge.Object.event_destroy

.. automethod:: sge.Object.event_step

.. automethod:: sge.Object.event_alarm

.. automethod:: sge.Object.event_animation_end

.. automethod:: sge.Object.event_key_press

.. automethod:: sge.Object.event_key_release

.. automethod:: sge.Object.event_mouse_move

.. automethod:: sge.Object.event_mouse_button_press

.. automethod:: sge.Object.event_mouse_button_release

.. automethod:: sge.Object.event_joystick_axis_move

.. automethod:: sge.Object.event_joystick_hat_move

.. automethod:: sge.Object.event_joystick_trackball_move

.. automethod:: sge.Object.event_joystick_button_press

.. automethod:: sge.Object.event_joystick_button_release

.. automethod:: sge.Object.event_update_position

.. automethod:: sge.Object.event_collision

.. automethod:: sge.Object.event_collision_left

.. automethod:: sge.Object.event_collision_right

.. automethod:: sge.Object.event_collision_top

.. automethod:: sge.Object.event_collision_bottom

.. automethod:: sge.Object.event_inactive_step

.. automethod:: sge.Object.event_inactive_key_press

.. automethod:: sge.Object.event_inactive_key_release

.. automethod:: sge.Object.event_inactive_mouse_move

.. automethod:: sge.Object.event_inactive_mouse_button_press

.. automethod:: sge.Object.event_inactive_mouse_button_release

.. automethod:: sge.Object.event_inactive_joystick_axis_move

.. automethod:: sge.Object.event_inactive_joystick_hat_move

.. automethod:: sge.Object.event_inactive_joystick_trackball_move

.. automethod:: sge.Object.event_inactive_joystick_button_press

.. automethod:: sge.Object.event_inactive_joystick_button_release

.. automethod:: sge.Object.event_paused_key_press

.. automethod:: sge.Object.event_paused_key_release

.. automethod:: sge.Object.event_paused_mouse_move

.. automethod:: sge.Object.event_paused_mouse_button_press

.. automethod:: sge.Object.event_paused_mouse_button_release

.. automethod:: sge.Object.event_paused_joystick_axis_move

.. automethod:: sge.Object.event_paused_joystick_hat_move

.. automethod:: sge.Object.event_paused_joystick_trackball_move

.. automethod:: sge.Object.event_paused_joystick_button_press

.. automethod:: sge.Object.event_paused_joystick_button_release

sge.Room
========

.. autoclass:: sge.Room

sge.Room Methods
----------------

.. automethod:: sge.Room.__init__

.. automethod:: sge.Room.add

.. automethod:: sge.Room.start

.. automethod:: sge.Room.resume

.. automethod:: sge.Room.set_alarm

.. automethod:: sge.Room.get_alarm

.. automethod:: sge.Room.end

.. automethod:: sge.Room.project_dot

.. automethod:: sge.Room.project_line

.. automethod:: sge.Room.project_rectangle

.. automethod:: sge.Room.project_ellipse

.. automethod:: sge.Room.project_circle

.. automethod:: sge.Room.project_sprite

.. automethod:: sge.Room.project_text

.. automethod:: sge.Room.move

.. automethod:: sge.Room.destroy

sge.Room Event Methods
----------------------

.. automethod:: sge.Room.event_room_start

.. automethod:: sge.Room.event_room_resume

.. automethod:: sge.Room.event_room_end

.. automethod:: sge.Room.event_step

.. automethod:: sge.Room.event_alarm

.. automethod:: sge.Room.event_key_press

.. automethod:: sge.Room.event_key_release

.. automethod:: sge.Room.event_mouse_move

.. automethod:: sge.Room.event_mouse_button_press

.. automethod:: sge.Room.event_mouse_button_release

.. automethod:: sge.Room.event_joystick_axis_move

.. automethod:: sge.Room.event_joystick_hat_move

.. automethod:: sge.Room.event_joystick_trackball_move

.. automethod:: sge.Room.event_joystick_button_press

.. automethod:: sge.Room.event_joystick_button_release

.. automethod:: sge.Room.event_gain_keyboard_focus

.. automethod:: sge.Room.event_lose_keyboard_focus

.. automethod:: sge.Room.event_gain_mouse_focus

.. automethod:: sge.Room.event_lose_mouse_focus

.. automethod:: sge.Room.event_close

.. automethod:: sge.Room.event_paused_key_press

.. automethod:: sge.Room.event_paused_key_release

.. automethod:: sge.Room.event_paused_mouse_move

.. automethod:: sge.Room.event_paused_mouse_button_press

.. automethod:: sge.Room.event_paused_mouse_button_release

.. automethod:: sge.Room.event_paused_joystick_axis_move

.. automethod:: sge.Room.event_paused_joystick_hat_move

.. automethod:: sge.Room.event_paused_joystick_trackball_move

.. automethod:: sge.Room.event_paused_joystick_button_press

.. automethod:: sge.Room.event_paused_joystick_button_release

.. automethod:: sge.Room.event_paused_gain_keyboard_focus

.. automethod:: sge.Room.event_paused_lose_keyboard_focus

.. automethod:: sge.Room.event_paused_gain_mouse_focus

.. automethod:: sge.Room.event_paused_lose_mouse_focus

.. automethod:: sge.Room.event_paused_close

sge.View
========

.. autoclass:: sge.View

sge.View Methods
----------------

.. automethod:: sge.View.__init__
