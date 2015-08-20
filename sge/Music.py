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
from sge import r


__all__ = ['Music']


class Music(object):

    """
    This class stores and plays music.  Music is very similar to sound
    effects, but only one music file can be played at a time, and it is
    more efficient for larger files than :class:`sge.Sound`.

    What music formats are supported depends on the implementation of
    the SGE, but Ogg Vorbis is generally a good choice.  See the
    implementation-specific information for a full list of supported
    formats.

    .. note::

       You should avoid the temptation to use MP3 files; MP3 is a
       patent-encumbered format, so many systems do not support it and
       royalties to the patent holders may be required for commercial
       use.  There are many programs which can convert your MP3 files to
       the free Ogg Vorbis format.

    .. attribute:: volume

       The volume of the music in percent from ``0`` to ``100`` (``0``
       for no sound, ``100`` for maximum volume).

    .. attribute:: fname

       The file name of the music given when it was created.
       (Read-only)

    .. attribute:: length

       The length of the music in milliseconds.  (Read-only)

    .. attribute:: playing

       Whether or not the music is playing.  (Read-only)

    .. attribute:: position

       The current position (time) playback of the music is at in
       milliseconds.  (Read-only)

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value):
        self.__volume = min(value, 100)

        if self.playing:
            pygame.mixer.music.set_volume(value / 100)

    @property
    def length(self):
        if self.__length is None:
            if self.fname is not None:
                snd = pygame.mixer.Sound(self.fname)
                self.__length = snd.get_length() * 1000
            else:
                self.__length = 0

        return self.__length

    @property
    def playing(self):
        return r.music is self and pygame.mixer.music.get_busy()

    @property
    def position(self):
        if self.playing:
            return self.__start + pygame.mixer.music.get_pos()
        else:
            return 0

    def __init__(self, fname, volume=100):
        """
        Arguments:

        - ``fname`` -- The path to the sound file.  If set to
          :const:`None`, this object will not actually play any music.
          If this is neither a valid sound file nor :const:`None`,
          :exc:`IOError` is raised.

        All other arguments set the respective initial attributes of the
        music.  See the documentation for :class:`sge.Music` for more
        information.
        """
        self.rd = {}
        if fname is None or os.path.isfile(fname):
            self.fname = fname
        else:
            raise IOError('File "{}" not found.'.format(fname))
        self.volume = volume
        self.rd["timeout"] = None
        self.rd["fade_time"] = None
        self.__start = 0
        self.__length = None

    def play(self, start=0, loops=1, maxtime=None, fade_time=None):
        """
        Play the music.

        Arguments:

        - ``start`` -- The number of milliseconds from the beginning to
          start playing at.

        See the documentation for :meth:`sge.Sound.play` for more
        information.
        """
        if self.fname is not None:
            if not self.playing:
                pygame.mixer.music.load(self.fname)

            if not loops:
                loops = -1

            r.music = self
            self.rd["timeout"] = maxtime
            self.rd["fade_time"] = fade_time

            if fade_time is not None and fade_time > 0:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(self.volume / 100)

            if self.fname.lower().endswith(".mod"):
                # MOD music is handled differently in Pygame: it uses
                # the pattern order number rather than the time to
                # indicate the start time.
                self._start = 0
                pygame.mixer.music.play(loops, start)
            else:
                self.__start = start
                try:
                    pygame.mixer.music.play(loops, start / 1000)
                except NotImplementedError:
                    pygame.mixer.music.play(loops)

    def queue(self, start=0, loops=1, maxtime=None, fade_time=None):
        """
        Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        See the documentation for :meth:`sge.Music.play` for more
        information.
        """
        r.music_queue.append((self, start, loops, maxtime, fade_time))

    @staticmethod
    def stop(fade_time=None):
        """
        Stop the currently playing music.

        See the documentation for :meth:`sge.Sound.stop` for more
        information.
        """
        if fade_time:
            pygame.mixer.music.fadeout(fade_time)
        else:
            pygame.mixer.music.stop()

    @staticmethod
    def pause():
        """Pause playback of the currently playing music."""
        pygame.mixer.music.pause()

    @staticmethod
    def unpause():
        """Resume playback of the currently playing music if paused."""
        pygame.mixer.music.unpause()

    @staticmethod
    def clear_queue():
        """Clear the music queue."""
        r.music_queue = []
