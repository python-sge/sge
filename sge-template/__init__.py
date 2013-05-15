#!/usr/bin/env python

# Stellar Game Engine Template
# Copyright (C) 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Stellar Game Engine - [insert implementation name here]

Stellar Game Engine is a library for Stellar.  It is a game engine
loosely based on Game Maker.

Except where otherwise noted, all documented features are required to be
offered by all implementations.  Any implementation failing to do so is
incomplete.

Constants:
    IMPLEMENTATION: A string identifying the how the engine is
        implemented (e.g. the name of the graphics library used).
    ALIGN_LEFT: Flag indicating alignment to the left.
    ALIGN_CENTER: Flag indicating alignment to the horizontal center.
    ALIGN_RIGHT: Flag indicating alignment to the right.
    ALIGN_TOP: Flag indicating alignment to the top.
    ALIGN_MIDDLE: Flag indicating alignment to the vertical middle.
    ALIGN_BOTTOM: Flag indicating alignment to the bottom.

Global variables:
    game: Stores the current game.  If there is no game currently, this
        variable is set to None.
    image_directories: A list of directories where images can be found.
        Default is ./data/images, ./data/sprites, or ./data/backgrounds.
    font_directories: A list of directories where font files can be
        found.  Default is ./data/fonts.
    sound_directories: A list of directories where sounds can be found.
        Default is ./data/sounds.
    music_directories: A list of directories where music files can be
        found.  Default is ./data/music.

Classes:
    Game: Class which handles the game.
    Sprite: Class used to store images and animations.
    BackgroundLayer: Class used to store a background layer.
    Background: Class used to store parallax-scrolling backgrounds.
    Font: Class used to store and handle fonts.
    Sound: Class used to store and play sound effects.
    Music: Class used to store and play music.
    StellarClass: Class used for game objects.
    Room: Class used for game rooms, e.g. levels.
    View: Class used for views in rooms.

Functions:
    get_key_pressed: Return whether or not a given key is pressed.
    get_mouse_button_pressed: Return whether or not a given mouse
        button is pressed.
    get_joystick_axis: Return the position of the given axis.
    get_joystick_hat: Return the position of the given HAT.
    get_joystick_button_pressed: Return whether or not the given
        joystick button is pressed.
    get_joysticks: Return the number of joysticks available.
    get_joystick_axes: Return the number of axes on the given
        joystick.
    get_joystick_hats: Return the number of HATs on the given
        joystick.
    get_joystick_buttons: Return the number of buttons on the
        given joystick.

Implementation-specific information:
[insert info here]

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.2.1.6"

import sys
import os
import math

# Import implementation-specific libraries like Pygame here

from .constants import *
from .Game import Game
from .Sprite import Sprite
from .BackgroundLayer import BackgroundLayer
from .Background import Background
from .Font import Font
from .Sound import Sound
from .Music import Music
from .StellarClass import StellarClass, Mouse
from .Room import Room
from .View import View
from .functions import *


__all__ = [
    # Constants
    'IMPLEMENTATION', 'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT', 'ALIGN_TOP',
    'ALIGN_MIDDLE', 'ALIGN_BOTTOM',

    # Classes
    'Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font', 'Sound',
    'Music', 'StellarClass', 'Room', 'View',

    # Functions
    'create_object', 'sound_stop_all', 'music_clear_queue', 'music_stop_all',
    'get_key_pressed', 'get_mouse_button_pressed', 'get_joystick_axis',
    'get_joystick_hat', 'get_joystick_button_pressed', 'get_joysticks',
    'get_joystick_axes', 'get_joystick_hats', 'get_joystick_buttons'
    ]

# Global variables
game = None
image_directories = [os.path.join(PROGRAM_DIR, 'data', 'images'),
                     os.path.join(PROGRAM_DIR, 'data', 'sprites'),
                     os.path.join(PROGRAM_DIR, 'data', 'backgrounds')]
font_directories = [os.path.join(PROGRAM_DIR, 'data', 'fonts')]
sound_directories = [os.path.join(PROGRAM_DIR, 'data', 'sounds')]
music_directories = [os.path.join(PROGRAM_DIR, 'data', 'music')]
