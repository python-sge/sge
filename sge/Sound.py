# Copyright (C) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
# 
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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import pygame

import sge
from sge.r import _get_channel, _release_channel


__all__ = ['Sound']


class Sound(object):

    """
    This class stores and plays sound effects.  Note that this is
    inefficient for large music files; for those, use :class:`sge.Music`
    instead.

    What sound formats are supported depends on the implementation of
    the SGE, but sound formats that are generally a good choice are Ogg
    Vorbis and uncompressed WAV.  See the implementation-specific
    information for a full list of supported formats.

    .. attribute:: volume

       The volume of the sound in percent from ``0`` to ``100`` (``0``
       for no sound, ``100`` for max sound).

    .. attribute:: max_play

       The maximum number of instances of this sound playing permitted.
       If a sound is played while this number of the instances of the
       same sound are already playing, one of the already playing sounds
       will be stopped before playing the new instance.  Set to
       :const:`None` for no limit.

    .. attribute:: fname

       The file name of the sound given when it was created.
       (Read-only)

    .. attribute:: length

       The length of the sound in milliseconds.  (Read-only)

    .. attribute:: playing

       The number of instances of this sound playing.  (Read-only)

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def max_play(self):
        return len(self.__channels)

    @max_play.setter
    def max_play(self, value):
        if value is None:
            value = 0

        if self.__sound is not None:
            value = max(0, value)
            while len(self.__channels) < value:
                self.__channels.append(_get_channel())
            while len(self.__channels) > value:
                _release_channel(self.__channels.pop(-1))

    @property
    def length(self):
        if self.__sound is not None:
            return self.__sound.get_length() * 1000
        else:
            return 0

    @property
    def playing(self):
        n = 0
        for channel in self.__channels + self.__temp_channels:
            if channel.get_busy():
                n += 1

        return n

    def __init__(self, fname, volume=100, max_play=1):
        """
        Arguments:

        - ``fname`` -- The path to the sound file.  If set to
          :const:`None`, this object will not actually play any sound.
          If this is neither a valid sound file nor :const:`None`,
          :exc:`IOError` is raised.

        All other arguments set the respective initial attributes of the
        sound.  See the documentation for :class:`sge.Sound` for more
        information.
        """
        self.rd = {}
        errlist = []

        if fname is not None and pygame.mixer.get_init():
            try:
                self.__sound = pygame.mixer.Sound(fname)
            except pygame.error as e:
                raise IOError(e)

        else:
            self.__sound = None

        self.__channels = []
        self.__temp_channels = []
        self.fname = fname
        self.volume = volume
        self.max_play = max_play

    def play(self, loops=1, volume=100, balance=0, maxtime=None,
             fade_time=None):
        """
        Play the sound.

        Arguments:

        - ``loops`` -- The number of times to play the sound; set to
          :const:`None` or ``0`` to loop indefinitely.
        - ``volume`` -- The volume to play the sound at as a percentage
          of :attr:`self.volume` from ``0`` to ``100`` (``0`` for no
          sound, ``100`` for :attr:`self.volume`).
        - ``balance`` -- The balance of the sound effect on stereo
          speakers as a float from ``-1`` to ``1``, where ``0`` is
          centered (full volume in both speakers), ``1`` is entirely in
          the right speaker, and ``-1`` is entirely in the left speaker.
        - ``maxtime`` -- The maximum amount of time to play the sound in
          milliseconds; set to :const:`None` for no limit.
        - ``fade_time`` -- The time in milliseconds over which to fade
          the sound in; set to :const:`None` or ``0`` to immediately
          play the sound at full volume.
        """
        if self.__sound is not None:
            if not loops:
                loops = 0
            if maxtime is None:
                maxtime = 0
            if fade_time is None:
                fade_time = 0

            # Adjust for the way Pygame does repeats
            loops -= 1

            # Calculate volume for each speaker
            left_volume = (self.volume / 100) * (volume / 100)
            right_volume = left_volume
            if balance < 0:
                right_volume *= 1 - abs(balance)
            elif balance > 0:
                left_volume *= 1 - abs(balance)

            if self.max_play:
                for channel in self.__channels:
                    if not channel.get_busy():
                        channel.play(self.__sound, loops, maxtime, fade_time)
                        channel.set_volume(left_volume, right_volume)
                        break
                else:
                    self.__channels[0].play(self.__sound, loops, maxtime,
                                            fade_time)
                    self.__channels[0].set_volume(left_volume, right_volume)
            else:
                channel = _get_channel()
                channel.play(self.__sound, loops, maxtime, fade_time)
                channel.set_volume(left_volume, right_volume)
                self.__temp_channels.append(channel)

            # Clean up old temporary channels
            while (self.__temp_channels and
                   not self.__temp_channels[0].get_busy()):
                _release_channel(self.__temp_channels.pop(0))

    def stop(self, fade_time=None):
        """
        Stop the sound.

        Arguments:

        - ``fade_time`` -- The time in milliseconds over which to fade
          the sound out before stopping; set to :const:`None` or ``0``
          to immediately stop the sound.
        """
        if self.__sound is not None:
            self.__sound.stop()

    def pause(self):
        """Pause playback of the sound."""
        for channel in self.__channels:
            channel.pause()

    def unpause(self):
        """Resume playback of the sound if paused."""
        for channel in self.__channels:
            channel.unpause()

    @staticmethod
    def stop_all():
        """Stop playback of all sounds."""
        pygame.mixer.stop()
