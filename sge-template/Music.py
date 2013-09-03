# The SGE Template
# Written in 2012, 2013 by Julian Marchant <onpon4@riseup.net> 
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


__all__ = ['Music']


class Music(object):

    """Music handling class.

    This class stores and plays music.  Music is very similar to sound
    effects, but only one music file can be played at a time, and it is
    more efficient for larger files than :class:`sge.Sound`.

    What music formats are supported depends on the implementation of
    the SGE, but Ogg Vorbis is generally a good choice.  See the
    implementation-specific information for a full list of supported
    formats.

    You should avoid the temptation to use MP3 files; MP3 is a
    patent-encumbered format, so many systems do not support it and
    royalties to the patent holders may be required for commercial use.
    There are many programs which can convert your MP3 files to the free
    Ogg Vorbis format.

    .. attribute:: volume

       The volume of the music in percent from ``0`` to ``100`` (``0``
       for no sound, ``100`` for maximum volume).

    .. attribute:: fname

       The file name of the music given when it was created.
       (Read-only)

    .. attribute:: id

       The unique identifier of the music.  (Read-only)

    .. attribute:: length

       The length of the music in milliseconds.  (Read-only)

    .. attribute:: playing

       Whether or not the music is playing.  (Read-only)

    .. attribute:: position

       The current position (time) playback of the music is at in
       milliseconds.  (Read-only)

    """

    def __init__(self, fname, id_=None, volume=100, **kwargs):
        """Constructor method.

        Arguments:

        - ``fname`` -- The name of the sound file in one of the paths
          specified in :data:`sge.music_directories`.  If set to
          :const:`None`, this object will not actually play any music.
          If this is neither a valid sound file nor :const:`None`,
          :exc:`IOError` is raised.
        - ``id`` -- The unique identifier of the music.  If set to
          :const:`None`, ``fname`` minus the extension will be used,
          modified by the SGE if it is already the unique idenfifier of
          another music object.

        All other arguments set the respective initial attributes of the
        music.  See the documentation for :class:`Music` for more
        information.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        # TODO

    def play(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Play the music.

        Arguments:

        - ``start`` -- The number of milliseconds from the beginning to
          start playing at.

        See the documentation for :meth:`sge.Sound.play` for more
        information.

        """
        # TODO

    def queue(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        See the documentation for :meth:`Music.play` for more
        information.

        """
        # TODO

    @staticmethod
    def stop(fade_time=None):
        """Stop the currently playing music.

        See the documentation for :meth:`sge.Sound.stop` for more
        information.

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
