# Copyright (C) 2012, 2013 Julian Marchant <onpon4@riseup.net>
# 
# This file is part of SGE Pygame.
# 
# SGE Pygame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# SGE Pygame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with SGE Pygame.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import pygame

import sge


__all__ = ['Sound']


class Sound(object):

    """Sound handling class.

    This class stores and plays sound effects.  Note that this is
    inefficient for large music files; for those, use sge.Music instead.

    What sound formats are supported depends on the implementation of
    SGE, but sound formats that are generally a good choice are Ogg
    Vorbis and uncompressed WAV.  See the implementation-specific
    information for a full list of supported formats.

    Attributes:
    - ``volume`` -- The volume of the sound in percent from 0 to 100 (0
      for no sound, 100 for max sound).
    - ``max_play`` -- The maximum number of instances of this sound
      playing permitted.  If a sound is played while this number of the
      instances of the same sound are already playing, one of the
      already playing sounds will be stopped before playing the new
      instance.  Set to None or 0 for no limit.

    Read-Only Attributes:
    - ``fname`` -- The file name of the sound given when it was created.
    - ``length`` -- The length of the sound in milliseconds.
    - ``playing`` -- The number of instances of this sound playing.

    """

    @property
    def max_play(self):
        return len(self._channels)

    @max_play.setter
    def max_play(self, value):
        if value is None:
            value = 0

        if self._sound is not None:
            value = max(0, value)
            while len(self._channels) < value:
                self._channels.append(sge.game._get_channel())
            while len(self._channels) > value:
                sge.game._release_channel(self._channels.pop(-1))

    @property
    def length(self):
        if self._sound is not None:
            return self._sound.get_length() * 1000
        else:
            return 0

    @property
    def playing(self):
        if self._sound is not None:
            return self._sound.get_num_channels()
        else:
            return 0

    def __init__(self, fname, id_=None, volume=100, max_play=1, **kwargs):
        """Create a new sound object.

        Arguments:
        - ``fname`` -- The name of the sound file in one of the paths
          specified in ``sound_directories``.  If set to None, this
          object will not actually play any sound.  If this is neither a
          valid sound file nor None, IOError is raised.
        - ``id`` -- The unique identifier of the sound.  If set to None,
          ``fname`` minus the extension will be used, modified by SGE if
          it is already the unique identifier of another music object.

        All other arguments set the respective initial attributes of the
        sound.  See the documentation for `Sound` for more information.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        if fname is not None and pygame.mixer.get_init():
            self._sound = None
            for path in sge.sound_directories:
                path = os.path.join(path, fname)
                try:
                    self._sound = pygame.mixer.Sound(path)
                    break
                except pygame.error:
                    pass

            if self._sound is None:
                print("Directories searched:")
                for d in sge.music_directories:
                    print(os.path.normpath(os.path.abspath(d)))
                msg = 'File "{0}" not found.'.format(self.fname)
                raise IOError(msg)
        else:
            self._sound = None

        self._channels = []
        self._temp_channels = []
        self.fname = fname
        self.volume = volume
        self.max_play = max_play

    def play(self, loops=0, volume=100, balance=0, maxtime=None,
             fade_time=None):
        """Play the sound.

        Arguments:
        - ``loops`` -- The number of extra times to play the sound after
          it is played the first time; set to None or -1 to loop
          indefinitely.
        - ``volume`` -- The volume to play the sound at as a percentage
          of ``self.volume`` from 0 to 100 (0 for no sound, 100 for
          ``self.volume``).
        - ``balance`` -- The balance of the sound effect on stereo
          speakers as a float from -1 to 1, where 0 is centered (full
          volume in both speakers), 1 is entirely in the right speaker,
          and -1 is entirely in the left speaker.
        - ``maxtime`` -- The maximum amount of time to play the sound in
          milliseconds; set to None or 0 for no limit.
        - ``fade_time`` -- The time in milliseconds over which to fade
          the sound in; set to None or 0 to immediately play the sound
          at full volume.

        """
        if self._sound is not None:
            if loops is None:
                loops = -1
            if maxtime is None:
                maxtime = 0
            if fade_time is None:
                fade_time = 0

            # Calculate volume for each speaker
            left_volume = volume / 100
            right_volume = left_volume
            if balance < 0:
                right_volume *= 1 - abs(balance)
            elif balance > 0:
                left_volume *= 1 - abs(balance)

            if self.max_play:
                for channel in self._channels:
                    if not channel.get_busy():
                        channel.play(self._sound, loops, maxtime, fade_time)
                        channel.set_volume(left_volume, right_volume)
                        break
                else:
                    self._channels[0].play(self._sound, loops, maxtime,
                                           fade_time)
                    self._channels[0].set_volume(left_volume, right_volume)
            else:
                channel = sge.game._get_channel()
                channel.play(self._sound, loops, maxtime, fade_time)
                channel.set_volume(left_volume, right_volume)
                self._temp_channels.append(channel)

            # Clean up old temporary channels
            while (self._temp_channels and
                   not self._temp_channels[0].get_busy()):
                sge.game._release_channel(self._temp_channels.pop(0))

    def stop(self, fade_time=None):
        """Stop the sound.

        Arguments:
        - ``fade_time`` -- The time in milliseconds over which to fade
          the sound out before stopping; set to None or 0 to immediately
          stop the sound.

        """
        if self._sound is not None:
            self._sound.stop()

    def pause(self):
        """Pause playback of the sound."""
        for channel in self._channels:
            channel.pause()

    def unpause(self):
        """Resume playback of the sound if paused."""
        for channel in self._channels:
            channel.unpause()

    @staticmethod
    def stop_all():
        """Stop playback of all sounds."""
        for i in sge.game.sounds:
            sge.game.sounds[i].stop()    
