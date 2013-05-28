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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


__all__ = ['Music']


class Music(object):

    """Music handling class.

    This class stores and plays music.  Music is very similar to sound
    effects, but only one music file can be played at a time, and it is
    more efficient for larger files than sge.Sound.

    What music formats are supported depends on the implementation of
    SGE, but Ogg Vorbis is generally a good choice.  See the
    implementation's readme for a full list of supported formats.  You
    should avoid the temptation to use MP3 files; MP3 is a
    patent-encumbered format, so many systems do not support it and
    royalties to the patent holders may be required for commercial use.
    There are many programs which can convert your MP3 files to the free
    Ogg Vorbis format.

    Attributes:
    * volume: The volume of the music in percent (0 for no sound, 100
      for maximum volume).
    * balance: The balance of the music on stereo speakers.  A value of
      0 means centered (an equal amount of play on both speakers), -1
      means entirely in the left speaker, and 1 means entirely in the
      right speaker.

    Read-Only Attributes:
    * fname: The file name of the music given when it was created.
    * length: The length of the music in milliseconds.
    * playing: Whether or not the music is playing.
    * position: The current position (time) on the music in milliseconds.

    Methods:
    * Music.play: Play the music.
    * Music.queue: Queue the music for playback.

    Static methods:
    * Music.stop: Stop the currently playing music.
    * Music.pause: Pause playback of the currently playing music.
    * Music.unpause: Resume playback of the currently playing music if
      paused.
    * Music.clear_queue: Clear the music queue.

    """

    def __init__(self, fname, volume=100, balance=0):
        """Create a new music object.

        ``fname`` indicates the name of the sound file, to be located in
        one of the directories specified in ``music_directories``.  If
        set to None, this object will not actually play any music
        (useful as a placeholder, for example).  If ``fname`` is neither
        a valid sound file nor None, IOError will be raised.

        All remaining arguments set the respective initial attributes of
        the music.  See the documentation for sge.Music for more
        information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def play(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Play the music.

        ``start`` indicates the number of milliseconds from the
        beginning to start at.  ``loops`` indicates the number of extra
        times to play the sound after it is played the first time; set
        to -1 or None to loop indefinitely.  ``maxtime`` indicates the
        maximum amount of time to play the sound in milliseconds; set to
        0 or None for no limit.  ``fade_time`` indicates the time in
        milliseconds over which to fade the sound in; set to 0 or None
        to immediately play the music at full volume.

        If some music was already playing when this is called, it will
        be stopped.

        """
        # TODO

    def queue(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        All arguments are the same as the respective arguments for
        sge.Music.play; see the documentation for sge.Music.play for
        more information.

        """
        # TODO

    @staticmethod
    def stop(fade_time=None):
        """Stop the currently playing music.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the music.

        """
        # TODO

    @staticmethod
    def pause():
        """Pause playback of the currently playing music."""
        # TODO

    @staticmethod
    def unpause():
        """Resume playback of the currently playing music if paused."""
        # TODO

    @staticmethod
    def clear_queue():
        """Clear the music queue."""
        # TODO
