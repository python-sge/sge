Copyright (C) 2013, 2014 Julian Marchant <onpon4@riseup.net>

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.

========================================================================

0.7.0-dev
------------------------------------------------------------------------

Specification additions:
+ sge.Sprite.frames
+ sge.Sprite.append_frame
+ sge.Sprite.insert_frame
+ sge.Sprite.delete_frame
+ sge.Sprite.from_tileset
+ sge.Sprite.destroy
+ sge.BackgroundLayer.destroy
+ sge.Background.destroy
+ sge.Sound.destroy
+ sge.Music.destroy
+ sge.Room.destroy
+ sge.Room.move

Specification misc changes:
* room_number argument added to sge.Room.__init__


0.7.0
------------------------------------------------------------------------

Specification additions:
+ sge.get_joystick_name
+ sge.get_joystick_id
+ sge.get_joystick_trackballs
+ sge.Game.register_class
+ sge.Game.registered_classes
+ sge.Room.objects_by_class
+ sge.StellarClass.event_begin_step
+ sge.StellarClass.event_end_step
+ sge.StellarClass.event_inactive_end_step
+ sge.Sprite.speed
+ sge.StellarClass.image_speed

Specification misc changes:
* Joystick handling functions now accept joystick names for "joystick" argument.
* Joystick events' "joystick" argument renamed to "ID".
* Joystick events now have a "name" argument indicating the joystick name.
* sge.Room.objects changed from a tuple to a list.
* xprevious and yprevious of StellarClass now indicate the x and y
  values of the previous frame rather than the last x and y values
  different from the current ones.
* Changing sge.Sprite.width and sge.Sprite.height is now officially destructive.


0.6.0
------------------------------------------------------------------------

Specification additions:
+ sge.Font.from_sprite
+ sge.Room.event_room_resume

Specification misc changes:
* sge.Sprite.draw_sprite and sge.Room.project_sprite now support blend modes.
* sge.Sound.play and sge.Music.play "loops" argument tweaked.

Specification bugfixes:
- Argument for Font.__init__ being the old "id_" rather than "ID"
- Small problems with the documentation


0.5.0
------------------------------------------------------------------------

Specification additions:
+ sge.Game.event_gain_keyboard_focus
+ sge.Game.event_lose_keyboard_focus
+ sge.Game.event_gain_mouse_focus
+ sge.Game.event_lose_mouse_focus
+ sge.Game.event_paused_gain_keyboard_focus
+ sge.Game.event_paused_lose_keyboard_focus
+ sge.Game.event_paused_gain_mouse_focus
+ sge.Game.event_paused_lose_mouse_focus
+ sge.Room.event_gain_keyboard_focus
+ sge.Room.event_lose_keyboard_focus
+ sge.Room.event_gain_mouse_focus
+ sge.Room.event_lose_mouse_focus
+ sge.Room.event_paused_gain_keyboard_focus
+ sge.Room.event_paused_lose_keyboard_focus
+ sge.Room.event_paused_gain_mouse_focus
+ sge.Room.event_paused_lose_mouse_focus

Specification misc changes:
* Documentation reformatted.
* "id"/"id_" argument in many constructor methods changed to "ID".


0.4.0
------------------------------------------------------------------------

Specification additions:
+ sge.Sprite.from_screenshot
+ sge.Sprite.save
+ sge.show_message
+ sge.get_text_entry
+ sge.Room.background_x
+ sge.Room.background_y
+ sge.Sprite.id
+ sge.BackgroundLayer.id
+ sge.Font.id
+ sge.Sound.id
+ sge.Music.id

Specification removals:
- sge.Music.stop_all (replaced by sge.Music.stop, now a static method)
- sge.Music.balance (nonsensical; should be controlled by the music file)
- sge.Sound.balance (replaced by a balance argument when the sound is played)
- sge.Background.x (replaced by sge.Room.background_x)
- sge.Background.y (replaced by sge.Room.background_y)

Specification misc changes:
* bbox_x and bbox_y of sge.Sprite now default to the top-left of the image.
* sge.Music.stop is now a static method.
* sge.Music.pause is now a static method.
* sge.Music.unpause is now a static method.
* Key press events now have a third argument, char.
* sge.Sound.play now has a balance argument.
* Docstrings reformatted to reStructuredText.
* sge.Sprite.__init__ now has an id attribute.
* sge.BackgroundLayer.__init__ now has an id attribute.
* sge.Font.__init__ now has an id attribute.
* Sprites can be referenced by id rather than by name now.
* Background layers can be referenced by id rather than by sprite name now.
* Fonts can be referenced by id rather than by name now.

Specification misc changes:
* Released to the public domain via CC0.


0.3.0
------------------------------------------------------------------------

Specification additions:
+ sge.Room.project_dot
+ sge.Room.project_line
+ sge.Room.project_rectangle
+ sge.Room.project_ellipse
+ sge.Room.project_circle
+ sge.Room.project_sprite
+ sge.Room.project_text
+ sge.Background.x
+ sge.Background.y
+ Trackball support
+ sge.StellarClass.active

Specification misc changes:
* Trying to load invalid sound files now raises an exception.
* The file name for sounds and music can now be set to None for null sounds.
* Mouse buttons are now identified by strings instead of constants.


0.2.1
------------------------------------------------------------------------

Specification misc changes:
* sge.Game.window_icon is now a file name instead of a sprite.
* The default room size is now the game window size.


0.2.0
------------------------------------------------------------------------

Specification additions:
+ sge.Sprite.draw_dot
+ sge.Sprite.draw_line
+ sge.Sprite.draw_rectangle
+ sge.Sprite.draw_ellipse
+ sge.Sprite.draw_circle
+ sge.Sprite.draw_text
+ sge.Sprite.draw_clear
+ sge.Game.grab_input
+ sge.Sprite.draw_sprite
+ sge.Music.clear_queue
+ sge.Music.stop_all
+ sge.Sound.stop_all
+ sge.StellarClass.create
+ sge.Game.window_text
+ sge.Game.window_icon

Specification removals:
- sge.Game.draw_dot (replaced by sge.Sprite.draw_dot)
- sge.Game.draw_line (replaced by sge.Sprite.draw_line)
- sge.Game.draw_rectangle (replaced by sge.Sprite.draw_rectangle)
- sge.Game.draw_ellipse (replaced by sge.Sprite.draw_ellipse)
- sge.Game.draw_circle (replaced by sge.Sprite.draw_circle)
- sge.Game.sound_stop_all (replaced by sge.sound_stop_all)

Specification misc changes:
* A list or tuple of possible font choices can now be specified.
* Sprites now use a transparent image by default, not a black image.
* Added arguments to sge.Room.end.
* Implementations no longer required to support Ogg Vorbis and WAV.
* Removed unnecessary arguments from sge.Font.get_size.
* Split SGE in to multiple files.


0.1.0
------------------------------------------------------------------------

First release
