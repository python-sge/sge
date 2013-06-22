# SGE Template
# Written in 2012, 2013 by Julian Marchant <onpon4@lavabit.com> 
# 
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty. 
# 
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

# INSTRUCTIONS FOR DEVELOPING AN IMPLEMENTATION: Replace  the notice
# above as well as the notices contained in other source files with your
# own copyright notice.  Recommended free  licenses are  the GNU General
# Public License, GNU Lesser General Public License, Expat License, or
# Apache License 2.0.

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
