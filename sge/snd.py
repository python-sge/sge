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
This module provides classes related to the sound system.
"""


import os
import random
import warnings

import pygame

import sge
from sge import r
from sge.r import _get_channel, _release_channel


__all__ = ["Sound", "Music", "stop_all"]


class Sound(object):

    """
    This class stores and plays sound effects.  Note that this is
    inefficient for large music files; for those, use
    :class:`sge.snd.Music` instead.

    What sound formats are supported depends on the implementation of
    the SGE, but sound formats that are generally a good choice are Ogg
    Vorbis and uncompressed WAV.  See the implementation-specific
    information for a full list of supported formats.

    .. attribute:: volume

       The volume of the sound as a value from ``0`` to ``1`` (``0`` for
       no sound, ``1`` for maximum volume).

    .. attribute:: max_play

       The maximum number of instances of this sound playing permitted.
       If a sound is played while this number of the instances of the
       same sound are already playing, one of the already playing sounds
       will be stopped before playing the new instance.  Set to ``None``
       for no limit.

    .. attribute:: parent

       Indicates another sound which is treated as being the same sound
       as this one for the purpose of determining whether or not, and
       how many times, the sound is playing.  Set to ``None`` for no
       parent.

       If the sound has a parent, :attr:`max_play` will have no effect
       and instead the parent sound's :attr:`max_play` will apply to
       both the parent sound and this sound.

       .. warning::

          It is acceptable for a sound to both be a parent and have a
          parent.  However, there MUST be a parent at the top which has
          no parent.  The behavior of circular parenting, such as making
          two sounds parents of each other, is undefined.

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
        return len(self.rd["channels"]) if self.rd["channels"] else None

    @max_play.setter
    def max_play(self, value):
        self.__max_play = value

        if value is None:
            value = 0

        if self.__sound is not None and self.parent is None:
            value = max(0, value)
            while len(self.rd["channels"]) < value:
                self.rd["channels"].append(_get_channel())
            while len(self.rd["channels"]) > value:
                _release_channel(self.rd["channels"].pop(-1))

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        if value != self.__parent:
            self.__parent = value
            if value is None:
                self.rd["channels"] = []
                self.max_play = self.__max_play
            else:
                while self.rd["channels"]:
                    _release_channel(self.rd["channels"].pop(-1))
                self.rd["channels"] = value.rd["channels"]

    @property
    def length(self):
        if self.__sound is not None:
            return self.__sound.get_length() * 1000
        else:
            return 0

    @property
    def playing(self):
        n = 0
        for channel in self.rd["channels"] + self.__temp_channels:
            if channel.get_busy():
                n += 1

        return n

    def __init__(self, fname, volume=1, max_play=1, parent=None):
        """
        Arguments:

        - ``fname`` -- The path to the sound file.  If set to
          ``None``, this object will not actually play any sound. If
          this is neither a valid sound file nor ``None``,
          :exc:`FileNotFoundError` is raised.

        All other arguments set the respective initial attributes of the
        sound.  See the documentation for :class:`sge.snd.Sound` for
        more information.
        """
        self.rd = {}
        errlist = []

        if fname is not None and pygame.mixer.get_init():
            try:
                self.__sound = pygame.mixer.Sound(fname)
            except pygame.error as e:
                raise FileNotFoundError(e)

        else:
            self.__sound = None

        self.rd["channels"] = []
        self.__temp_channels = []
        self.fname = fname
        self.volume = volume
        self.__parent = None
        if parent is None:
            self.max_play = max_play
        else:
            self.__max_play = max_play
            self.parent = parent

    def play(self, loops=1, volume=1, balance=0, maxtime=None,
             fade_time=None, force=True):
        """
        Play the sound.

        Arguments:

        - ``loops`` -- The number of times to play the sound; set to
          ``None`` or ``0`` to loop indefinitely.
        - ``volume`` -- The volume to play the sound at as a factor
          of :attr:`self.volume` (``0`` for no sound, ``1`` for
          :attr:`self.volume`).
        - ``balance`` -- The balance of the sound effect on stereo
          speakers as a float from ``-1`` to ``1``, where ``0`` is
          centered (full volume in both speakers), ``1`` is entirely in
          the right speaker, and ``-1`` is entirely in the left speaker.
        - ``maxtime`` -- The maximum amount of time to play the sound in
          milliseconds; set to ``None`` for no limit.
        - ``fade_time`` -- The time in milliseconds over which to fade
          the sound in; set to ``None`` or ``0`` to immediately play the
          sound at full volume.
        - ``force`` -- Whether or not the sound should be played even if
          it is already playing the maximum number of times.  If set to
          :const:`True` and the sound is already playing the maximum
          number of times, one of the instances of the sound already
          playing will be stopped.
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
            left_volume = min(1, self.volume * volume)
            right_volume = left_volume
            if balance < 0:
                right_volume *= 1 - abs(balance)
            elif balance > 0:
                left_volume *= 1 - abs(balance)

            if self.max_play:
                for channel in self.rd["channels"]:
                    if not channel.get_busy():
                        channel.play(self.__sound, loops, maxtime, fade_time)
                        channel.set_volume(left_volume, right_volume)
                        break
                else:
                    if force:
                        channel = random.choice(self.rd["channels"])
                        channel.play(self.__sound, loops, maxtime, fade_time)
                        channel.set_volume(left_volume, right_volume)
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
          the sound out before stopping; set to ``None`` or ``0`` to
          immediately stop the sound.
        """
        if self.__sound is not None:
            self.__sound.stop()

    def pause(self):
        """Pause playback of the sound."""
        for channel in self.rd["channels"]:
            channel.pause()

    def unpause(self):
        """Resume playback of the sound if paused."""
        for channel in self.rd["channels"]:
            channel.unpause()


class Music(object):

    """
    This class stores and plays music.  Music is very similar to sound
    effects, but only one music file can be played at a time, and it is
    more efficient for larger files than :class:`sge.snd.Sound`.

    What music formats are supported depends on the implementation of
    the SGE, but Ogg Vorbis is generally a good choice.  See the
    implementation-specific information for a full list of supported
    formats.

    .. attribute:: volume

       The volume of the music as a value from ``0`` to ``1`` (``0`` for
       no sound, ``1`` for maximum volume).

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
        self.__volume = min(value, 1)

        if self.playing:
            pygame.mixer.music.set_volume(value)

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

    def __init__(self, fname, volume=1):
        """
        Arguments:

        - ``fname`` -- The path to the sound file.  If set to ``None``,
          this object will not actually play any music.  If this is
          neither a valid sound file nor ``None``,
          :exc:`FileNotFoundError` is raised.

        All other arguments set the respective initial attributes of the
        music.  See the documentation for :class:`sge.snd.Music` for
        more information.
        """
        self.rd = {}
        if fname is None or os.path.isfile(fname):
            self.fname = fname
        else:
            raise FileNotFoundError('File "{}" not found.'.format(fname))
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

        See the documentation for :meth:`sge.snd.Sound.play` for more
        information.
        """
        if self.fname is not None:
            if not self.playing:
                try:
                    pygame.mixer.music.load(self.fname)
                except pygame.error as e:
                    warnings.warn(str(e))
                    return

            if not loops:
                loops = -1

            r.music = self
            self.rd["timeout"] = maxtime
            self.rd["fade_time"] = fade_time

            if fade_time is not None and fade_time > 0:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(self.volume)

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

        See the documentation for :meth:`sge.snd.Music.play` for more
        information.
        """
        r.music_queue.append((self, start, loops, maxtime, fade_time))

    @staticmethod
    def stop(fade_time=None):
        """
        Stop the currently playing music.

        See the documentation for :meth:`sge.snd.Sound.stop` for more
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


def stop_all():
    """Stop playback of all sounds."""
    pygame.mixer.stop()

