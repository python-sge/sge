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


__all__ = ['Font']


class Font(object):

    """Font handling class.

    This class stores a font for use by `sge.Sprite.draw_text` and
    `sge.Room.render_text`.

    Note that bold and italic rendering could be ugly.  It is better to
    choose a bold or italic font rather than enabling bold or italic
    rendering, if possible.

    Attributes:

    - ``size`` -- The height of the font in pixels.

    - ``underline`` -- Whether or not underlined rendering is enabled.

    - ``bold`` -- Whether or not bold rendering is enabled.

    - ``italic`` -- Whether or not italic rendering is enabled.

    Read-Only Attributes:

    - ``name`` -- The name of the font as specified when it was created.

    - ``id`` -- The unique identifier of the font.

    """

    def __init__(self, name=None, id_=None, size=12, underline=False,
                 bold=False, italic=False, **kwargs):
        """Create a new Font object.

        Arguments:

        - ``name`` -- The name of the font.  Can be one of the
          following:

          - A string indicating the name of a font file located in one
            of the paths specified in ``sge.font_directories``, e.g.
            ``"MyFont.ttf"``.

          - A string indicating the case-insensitive name of a system
            font, e.g. ``"Liberation Serif"``.

          - A list or tuple of strings indicating either a font file or
            a system font to choose from in order of preference.

          If none of the above methods return a valid font, SGE will
          choose the font.

        - ``id`` -- The unique identifier of the font.  If set to None,
          ``name`` will be used, modified by SGE if it is already the
          unique identifier of another font.

        All other arguments set the respective initial attributes of the
        font.  See the documentation for `Font` for more information.

        Note that it is generally not a good practice to rely on system
        fonts.  A font which you have on your system is probably not on
        everyone's system.  For example, most Windows systems have a
        font called Times New Roman, but this font is rarely found on
        GNU/Linux systems.  On the other hand, most GNU/Linux systems
        have the Liberation fonts included by default, but these fonts
        are uncommon on Windows systems.  Rather than relying on system
        fonts, choose a font which is under a free license (such as the
        GNU General Public License or the SIL Open Font License) and
        distribute it with your game; this will ensure that everyone
        sees text rendered the same way you do.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        # TODO

    def get_size(self, text, width=None, height=None):
        """Return the size of a certain string of text when rendered.

        See the documentation for `sge.Sprite.draw_text` for information
        about the arguments.

        """
        # TODO
