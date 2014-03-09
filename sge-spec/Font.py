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
# Apache License 2.0.

__all__ = ['Font']


class Font(object):

    """Font handling class.

    This class stores a font for use by :meth:`sge.Sprite.draw_text` and
    :meth:`sge.Room.project_text`.

    .. attribute:: size

       The height of the font in pixels.

    .. attribute:: underline

       Whether or not underlined rendering is enabled.

    .. attribute:: bold

       Whether or not bold rendering is enabled.

       .. note::

          Using this option can be ugly.  It is better to choose a bold
          font rather than enabling bold rendering, if possible.

    .. attribute:: italic

       Whether or not italic rendering is enabled.

       .. note::

          Using this option can be ugly.  It is better to choose an
          italic font rather than enabling italic rendering, if
          possible.

    .. attribute:: name

       The name of the font as specified when it was created.
       (Read-only)

    .. attribute:: id

       The unique identifier of the font.  (Read-only)

    """

    def __init__(self, name=None, ID=None, size=12, underline=False,
                 bold=False, italic=False):
        """Constructor method.

        Arguments:

        - ``name`` -- The name of the font.  Can be one of the
          following:

          - A string indicating the name of a font file located in one
            of the paths specified in :data:`sge.font_directories`, e.g.
            ``"MyFont.ttf"``.
          - A string indicating the case-insensitive name of a system
            font, e.g. ``"Liberation Serif"``.
          - A list or tuple of strings indicating either a font file or
            a system font to choose from in order of preference.

          If none of the above methods return a valid font, the SGE will
          choose the font.

        - ``ID`` -- The value to set :attr:`id` to.  If set to
          :const:`None`, ``name`` will be used, modified by the SGE if
          it is already the unique identifier of another font.

        All other arguments set the respective initial attributes of the
        font.  See the documentation for :class:`sge.Font` for more
        information.

        .. note::

           It is generally not a good practice to rely on system fonts.
           A font which you have on your system is probably not on
           everyone's system.  For example, most Windows systems have a
           font called Times New Roman, but this font is not normally
           found on Debian systems.  On the other hand, Debian has the
           Liberation fonts installed by default, but these fonts are
           uncommon on Windows systems.  Rather than relying on system
           fonts, choose a font which is under a free license (such as
           the GNU General Public License or the SIL Open Font License)
           and distribute it with your game; this will ensure that
           everyone sees text rendered the same way you do.

        """
        # TODO

    def get_size(self, text, width=None, height=None):
        """Return the size of a certain string of text when rendered.

        See the documentation for :meth:`sge.Sprite.draw_text` for
        information about the arguments.

        """
        # TODO

    @classmethod
    def from_sprite(cls, sprite, chars, ID=None, hsep=0, vsep=0, size=12,
                    underline=False, bold=False, italic=False):
        """Return a font derived from a sprite.

        Arguments:

        - ``sprite`` -- The :class:`sge.Sprite` object to derive the
          font from.
        - ``chars`` -- A list of characters to set the sprite's frames
          to.  For example, ``['A', 'B', 'C']`` would assign the first
          frame to the letter "A", the second frame to the letter "B",
          and the third frame to the letter "C".  Any character not
          listed here will be rendered as its differently-cased
          counterpart if possible (e.g. "A" as "a") or as a blank space
          otherwise.
        - ``ID`` -- The value to set :attr:`id` to.  If set to
          :const:`None`, the name of the sprite will be used, modified
          by the SGE if it is already the unique identifier of another
          font.
        - ``hsep`` -- The amount of horizontal space to place between
          characters when text is rendered.
        - ``vsep`` -- The amount of vertical space to place between
          lines when text is rendered.

        All other arguments set the respective initial attributes of the
        font.  See the documentation for :class:`sge.Font` for more
        information.

        The font's :attr:`name` attribute will be set to the name of the
        sprite the font is derived from.

        The font's :attr:`size` attribute will indicate the height of
        the characters in pixels.  The width of the characters will be
        adjusted proportionally.

        """
        # TODO
