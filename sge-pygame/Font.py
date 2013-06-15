# Stellar Game Engine - Pygame 1.9
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

import os

import pygame

import sge


__all__ = ['Font', '_FakeFont']


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

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._font = None

        for path in sge.font_directories:
            path = os.path.join(path, self.name)
            if os.path.isfile(path):
                self._font = pygame.font.Font(path, self._size)

        if self._font is None:
            self._font = pygame.font.SysFont(self.name, self._size)

    @property
    def underline(self):
        return self._font.get_underline()

    @underline.setter
    def underline(self, value):
        self._font.set_underline(bool(value))

    @property
    def bold(self):
        return self._font.get_bold()

    @bold.setter
    def bold(self, value):
        self._font.set_bold(bool(value))

    @property
    def italic(self):
        return self._font.get_italic()

    @italic.setter
    def italic(self, value):
        self._font.set_italic(bool(value))

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

        assert pygame.font.get_init()

        if isinstance(name, basestring):
            name = (name,)

        self.name = ''
        compatible_fonts = (
            ("liberation serif", "tinos", "times new roman",
             "nimbus roman no9 l", "nimbus roman", "freeserif",
             "dejavu serif"),
            ("liberation sans", "arimo", "arial", "nimbus sans l", "freesans",
             "dejavu sans"),
            ("liberation sans narrow", "arial narrow"),
            ("liberation mono", "cousine", "courier new", "courier",
             "nimbus mono l", "freemono", "texgyrecursor", "courier prime",
             "dejavu sans mono"))

        try:
            for n in name:
                for fonts in compatible_fonts:
                    if n.lower() in fonts:
                        n = ','.join((n, ','.join(fonts)))
                        break

                self.name = ','.join((self.name, n))
        except TypeError:
            # Most likely a non-iterable value, such as None, so we
            # assume the default font is to be used.
            self.name = ''

        self.name = self.name[1:]
        self.size = size
        self.underline = underline
        self.bold = bold
        self.italic = italic

        if id_ is not None:
            self.id = id_
        else:
            self.id = self.name

            while self.id in sge.game.fonts:
                self.id += "_"

        sge.game.fonts[self.id] = self

    def get_size(self, text, width=None, height=None):
        """Return the size of a certain string of text when rendered.

        See the documentation for `sge.Sprite.draw_text` for information
        about the arguments.

        """
        lines = self._split_text(text, width)
        text_width = 0
        text_height = self._font.get_linesize() * len(lines)

        for line in lines:
            text_width = max(text_width, self._font.size(line)[0])

        if width is not None:
            text_width = min(text_width, width)

        if height is not None:
            text_height = min(text_height, height)

        return (text_width, text_height)

    def _split_text(self, text, width=None):
        # Split the text into lines of the proper size for ``width`` and
        # return a list of the lines.  If ``width`` is None, only
        # newlines split the text.
        lines = text.split('\n')

        if width is None:
            return lines
        else:
            split_text = []
            for line in lines:
                if self._font.size(line)[0] <= width:
                    split_text.append(line)
                else:
                    words = line.split(' ')
                    while words:
                        current_line = words.pop(0)
                        while (words and self._font.size(
                                ' '.join((current_line, words[0]))) < width):
                            current_line = ' '.join((current_line,
                                                     words.pop(0)))
                        split_text.append(current_line)
            return split_text
