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

    Music is mostly the same as sound, but only one can be played at a
    time.

    All Music objects have the following attributes:
        volume: The volume of the music in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the music on stereo speakers.  A value
            of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all music will be played through both
            speakers equally (assuming stereo sound is used).

    The following read-only attributes are also available:
        fname: The file name of the music given when it was created.
            See Music.__init__.__doc__ for more information.
        length: The length of the music in milliseconds.
        playing: Whether or not the music is playing.
        position: The current position (time) on the music in
            milliseconds.

    Music methods:
        Music.play: Play the music.
        Music.queue: Queue the music for playback.
        Music.stop: Stop the music.
        Music.pause: Pause playback of the music.
        Music.unpause: Resume playback of the music if paused.

    """

    def __init__(self, fname, volume=100, balance=0):
        """Create a new music object.

        ``fname`` indicates the name of the sound file, to be located in
        one of the directories specified in ``music_directories``.

        All remaining arguments set the initial properties of the music.
        See Music.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def play(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Play the music.

        If music was already playing when this is called, it will be
        stopped.

        ``start`` indicates the number of milliseconds from the
        beginning to start at.  ``loops`` indicates the number of extra
        times to play the sound after it is played the first time; set
        to -1 or None to loop indefinitely.  ``maxtime`` indicates the
        maximum amount of time to play the sound in milliseconds; set to
        0 or None for no limit.  ``fade_time`` indicates the time in
        milliseconds over which to fade the sound in; set to 0 or None
        to immediately play the music at full volume.

        """
        # TODO

    def queue(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        See Music.play.__doc__ for information about the arguments.

        """
        # TODO

    def stop(self, fade_time=None):
        """Stop the music.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the music.

        """
        # TODO

    def pause(self):
        """Pause playback of the music."""
        # TODO

    def unpause(self):
        """Resume playback of the music if paused."""
        # TODO
