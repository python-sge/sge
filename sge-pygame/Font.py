# Copyright (C) 2012, 2013 Julian Marchant <onpon4@riseup.net>
# 
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

    This class stores a font for use by :meth:`sge.Sprite.draw_text` and
    :meth:`sge.Room.project_text`.

    Note that bold and italic rendering could be ugly.  It is better to
    choose a bold or italic font rather than enabling bold or italic
    rendering, if possible.

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

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if self._font is not None:
            # Preserve underline, bold, and italic settings.
            underline = self.underline
            bold = self.bold
            italic = self.italic
        else:
            underline = False
            bold = False
            italic = False

        self._size = value
        self._font = None

        for path in sge.font_directories:
            path = os.path.join(path, self.name)
            if os.path.isfile(path):
                self._font = pygame.font.Font(path, self._size)

        if self._font is None:
            self._font = pygame.font.SysFont(self.name, self._size)

        # Restore underline, bold, and italic settings.
        self.underline = underline
        self.bold = bold
        self.italic = italic

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

        self._font = None
        self.name = self.name[1:]
        self.size = size
        self.underline = underline
        self.bold = bold
        self.italic = italic

        if ID is not None:
            self.id = ID
        else:
            self.id = self.name

            while self.id in sge.game.fonts:
                self.id += "_"

        sge.game.fonts[self.id] = self

    def get_size(self, text, width=None, height=None):
        """Return the size of a certain string of text when rendered.

        See the documentation for :meth:`sge.Sprite.draw_text` for
        information about the arguments.

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

    @classmethod
    def from_sprite(cls, sprite, chars, ID=None, size=12, underline=False,
                    bold=False, italic=False):
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

    def _split_text(self, text, width=None):
        # Split the text into lines of the proper size for ``width`` and
        # return a list of the lines.  If ``width`` is None, only
        # newlines split the text.
        lines = text.splitlines()

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
                        while (words and self._font.size(' '.join(
                                (current_line, words[0])))[0] <= width):
                            current_line = ' '.join((current_line,
                                                     words.pop(0)))
                        split_text.append(current_line)
            return split_text


class _PygameSpriteFont(pygame.font.Font):

    # Special font class that returns good values for a sprite font.

    @property
    def vsize(self):
        return self._vsize

    @vsize.setter
    def vsize(self, value):
        if self.height != 0:
            scale_factor = vsize / self.height
            if scale_factor != 1:
                self.width *= scale_factor
                self.height *= scale_factor
        else:
            # Protection against division by zero.
            self.width = vsize
            self.height = vsize

    def __init__(self, sprite, chars, size):
        self.sprite = sprite
        self.chars = {}

        for i in xrange(len(chars)):
            self.chars[chars[i]] = i

        self.width = self.sprite.width
        self.height = self.sprite.height
        self.vsize = size
        self.underline = False
        self.bold = False
        self.italic = False

    def render(self, text, antialias, color, background=None):
        w = self.width * len(text)
        h = self.height
        xscale = (self.width / self.sprite.width if self.sprite.width > 0
                  else 1)
        yscale = (self.height / self.sprite.height if self.sprite.height > 0
                  else 1)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill(pygame.Color(0, 0, 0, 0))
        pg_color = pygame.Color(color)
        sge_color = (pg_color.r, pg_color.g, pg_color.b, pg_color.a)

        for i in xrange(len(text)):
            if text[i] in self.chars:
                cimg = self.sprite._get_image(self.chars[text[i]],
                                              xscale=xscale,
                                              yscale=yscale, blend=sge_color)
                surf.blit(cimg, (i * self.width, 0))

        if background is None:
            return surf
        else:
            rsurf = pygame.Surface((w, h), pygame.SRCALPHA)
            rsurf.fill(background)
            rsurf.blit(surf, (0, 0))
            return rsurf

    def size(self, text):
        return (self.sprite.width * len(text), self.sprite.height)

    def set_underline(self, bool_):
        self.underline = bool_

    def get_underline(self):
        return self.underline

    def set_bold(self, bool_):
        self.bold = bool_

    def get_bold(self):
        return self.bold

    def set_italic(self, bool_):
        self.italic = bool_

    def get_italic(self):
        return self.italic

    def metrics(self, text):
        m = (0, self.width, 0, self.height, self.width)
        return [m for char in text]

    def get_linesize(self):
        return self.height

    def get_height(self):
        return self.height

    def get_ascent(self):
        return self.height

    def get_descent(self):
        return 0


class _SpriteFont(Font):

    # Special sprite font class for Font.from_sprite.

    @property
    def size(self):
        return self._font.vsize

    @size.setter
    def size(self, value):
        self._font.vsize = value

    def __init__(self, sprite, chars, ID=None, size=12, underline=False, bold=False,
                 italic=False):
        self.name = sprite.name
        self._font = _PygameSpriteFont(sprite, chars, size)
        self.underline = underline
        self.bold = bold
        self.italic = italic

        if ID is not None:
            self.id = ID
        else:
            self.id = self.name

            while self.id in sge.game.fonts:
                self.id += "_"

        sge.game.fonts[self.id] = self
