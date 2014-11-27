# The SGE Specification
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
# Apache License.

__all__ = ['View']


class View(object):

    """Class for room views.

    This class controls what the player sees in a room at any given
    time.  Multiple views can exist in a room, and this can be used to
    create a split-screen effect.

    .. attribute:: x

       The horizontal position of the view in the room.  When set, if it
       brings the view outside of the room it is in, it will be
       re-adjusted so that the view is completely inside the room.

    .. attribute:: y

       The vertical position of the view in the room.  When set, if it
       brings the view outside of the room it is in, it will be
       re-adjusted so that the view is completely inside the room.

    .. attribute:: xport

       The horizontal position of the view port on the window.

    .. attribute:: yport

       The vertical position of the view port on the window.

    .. attribute:: width

       The width of the view.  When set, if it results in the view being
       outside of the room it is in, :attr:`x` will be adjusted so that
       the view is completely inside the room.

    .. attribute:: height

       The height of the view.  When set, if it results in the view
       being outside the room it is in, :attr:`y` will be adjusted so
       that the view is completely inside the room.

    .. attribute:: wport

       The width of the view port.  Set to :const:`None` to make it the
       same as :attr:`width`.  If this value differs from :attr:`width`,
       the image will be horizontally scaled so that it fills the port.

    .. attribute:: hport

       The height of the view port.  Set to :const:`None` to make it the
       same as :attr:`height`.  If this value differs from
       :attr:`height`, the image will be vertically scaled so that it
       fills the port.

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)

    """

    def __init__(self, x, y, xport=0, yport=0, width=None, height=None,
                 wport=None, hport=None):
        """Constructor method.

        Arguments:

        - ``width`` -- The width of the view.  If set to :const:`None`,
          it will become ``sge.game.width - xport``.
        - ``height`` -- The height of the view.  If set to
          :const:`None`, it will become ``sge.game.height - yport``.

        All other arugments set the respective initial attributes of the
        view.  See the documentation for :class:`sge.View` for more
        information.

        """
        # TODO
