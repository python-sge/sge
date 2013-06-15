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

    def __init__(self, fname, volume=100, max_play=1):
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
        # TODO

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
        # TODO

    def stop(self, fade_time=None):
        """Stop the sound.

        Arguments:
        - ``fade_time`` -- The time in milliseconds over which to fade
          the sound out before stopping; set to None or 0 to immediately
          stop the sound.

        """
        # TODO

    def pause(self):
        """Pause playback of the sound."""
        # TODO

    def unpause(self):
        """Resume playback of the sound if paused."""
        # TODO

    @staticmethod
    def stop_all():
        """Stop playback of all sounds."""
        for i in sge.game.sounds:
            sge.game.sounds[i].stop() 
