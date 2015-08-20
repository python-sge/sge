# Copyright (C) 2012, 2013, 2014, 2015 Julian Marchant <onpon4@riseup.net>
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
import six

import sge
from sge.r import f_split_text, s_get_image


__all__ = ['Font']


class Font(object):

    """
    This class stores a font for use by text drawing methods.

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

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        if self.rd.get("font") is not None:
            # Preserve underline, bold, and italic settings.
            underline = self.underline
            bold = self.bold
            italic = self.italic
        else:
            underline = False
            bold = False
            italic = False

        self.__size = value
        self.rd["font"] = None

        name = self.name
        if isinstance(name, six.string_types):
            name = [name]

        names = []
        compatible_fonts = [
            ["liberation serif", "tinos", "nimbus roman no9 l", "nimbus roman",
             "freeserif", "dejavu serif", "droid serif", "bitstream charter",
             "times new roman"],
            ["droid sans", "liberation sans", "arimo", "nimbus sans l",
             "freesans", "dejavu sans", "droid sans fallback", "arial"],
            ["liberation sans narrow", "freecondensed",
             "sans condensed uralic", "arial narrow"],
            ["liberation mono", "cousine", "nimbus mono l", "freemono",
             "texgyrecursor", "courier prime", "dejavu sans mono",
             "droid sans mono", "courier new", "courier"]]

        try:
            for n in name:
                names.append(n)
                for fonts in compatible_fonts:
                    if n.lower() in fonts:
                        for font in fonts:
                            if font not in names:
                                names.append(font)
                        break
        except TypeError:
            # Most likely a non-iterable value, such as None, so we
            # assume the default font is to be used.
            names = ['']

        for name in names:
            if os.path.isfile(name):
                self.rd["font"] = pygame.font.Font(name, self.__size)
                break

        if self.rd.get("font") is None:
            self.rd["font"] = pygame.font.SysFont(','.join(names), self.__size)

        # Restore underline, bold, and italic settings.
        self.underline = underline
        self.bold = bold
        self.italic = italic

    @property
    def underline(self):
        return self.rd["font"].get_underline()

    @underline.setter
    def underline(self, value):
        self.rd["font"].set_underline(bool(value))

    @property
    def bold(self):
        return self.rd["font"].get_bold()

    @bold.setter
    def bold(self, value):
        self.rd["font"].set_bold(bool(value))

    @property
    def italic(self):
        return self.rd["font"].get_italic()

    @italic.setter
    def italic(self, value):
        self.rd["font"].set_italic(bool(value))

    def __init__(self, name=None, size=12, underline=False, bold=False,
                 italic=False):
        """
        Arguments:

        - ``name`` -- The name of the font.  Can be one of the
          following:

          - A string indicating the path to the font file.
          - A string indicating the case-insensitive name of a system
            font, e.g. ``"Liberation Serif"``.
          - A list or tuple of strings indicating either a font file or
            a system font to choose from in order of preference.

          If none of the above methods return a valid font, the SGE will
          choose the font.

        All other arguments set the respective initial attributes of the
        font.  See the documentation for :class:`sge.Font` for more
        information.

        .. note::

           It is generally not a good practice to rely on system fonts.
           There are no standard fonts; a font which you have on your
           system is probably not on everyone's system.  Rather than
           relying on system fonts, choose a font which is under a libre
           license (such as the GNU General Public License or the SIL
           Open Font License) and distribute it with your game; this
           will ensure that everyone sees text rendered the same way you
           do.
        """
        self.rd = {}
        self.name = name
        self.size = size
        self.underline = underline
        self.bold = bold
        self.italic = italic

    def get_width(self, text, width=None, height=None):
        """
        Return the width of a certain string of text when rendered.

        See the documentation for :meth:`sge.Sprite.draw_text` for
        more information.

        """
        lines = f_split_text(self, text, width)
        text_width = 0
        for line in lines:
            text_width = max(text_width, self.rd["font"].size(line)[0])

        if width is not None:
            text_width = min(text_width, width)

        return text_width

    def get_height(self, text, width=None, height=None):
        """
        Return the height of a certain string of text when rendered.

        See the documentation for :meth:`sge.Sprite.draw_text` for
        more information.

        """
        lines = f_split_text(self, text, width)
        if lines:
            text_height = self.rd["font"].get_linesize() * (len(lines) - 1)
            text_height += self.rd["font"].size(lines[-1])[1]
        else:
            text_height = 0

        if height is not None:
            text_height = min(text_height, height)

        return text_height

    @classmethod
    def from_sprite(cls, sprite, chars, hsep=0, vsep=0, size=12,
                    underline=False, bold=False, italic=False):
        """
        Return a font derived from a sprite.

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
        return _SpriteFont(sprite, chars, hsep, vsep, size, underline, bold,
                           italic)


class _PygameSpriteFont(pygame.font.Font):

    # Special font class that returns good values for a sprite font.

    @property
    def vsize(self):
        return self.height

    @vsize.setter
    def vsize(self, value):
        if self.height != 0:
            scale_factor = value / self.height
            if scale_factor != 1:
                self.width *= scale_factor
                self.height *= scale_factor
        else:
            # Protection against division by zero.
            self.width = value
            self.height = value

    def __init__(self, sprite, chars, hsep, vsep, size):
        self.sprite = sprite
        self.chars = {}
        self.hsep = hsep
        self.vsep = vsep

        for i in six.moves.range(len(chars)):
            self.chars[chars[i]] = i

        self.width = self.sprite.width
        self.height = self.sprite.height
        self.vsize = size
        self.underline = False
        self.bold = False
        self.italic = False

    def render(self, text, antialias, color, background=None):
        w = (self.width + self.hsep) * len(text)
        h = self.height + self.vsep
        xscale = (self.width / self.sprite.width if self.sprite.width > 0
                  else 1)
        yscale = (self.height / self.sprite.height if self.sprite.height > 0
                  else 1)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill(pygame.Color(0, 0, 0, 0))
        if not isinstance(color, pygame.Color):
            color = pygame.Color(color)
        sge_color = sge.Color((color.r, color.g, color.b, color.a))

        for i in six.moves.range(len(text)):
            if text[i] in self.chars:
                cimg = s_get_image(self.sprite, self.chars[text[i]],
                                   xscale=xscale, yscale=yscale,
                                   blend=sge_color)
                surf.blit(cimg, (i * (self.width + self.hsep), 0))
            elif text[i].swapcase() in self.chars:
                cimg = s_get_image(self.sprite, self.chars[text[i].swapcase()],
                                   xscale=xscale, yscale=yscale,
                                   blend=sge_color)
                surf.blit(cimg, (i * (self.width + self.hsep), 0))

        if background is None:
            return surf
        else:
            rsurf = pygame.Surface((w, h), pygame.SRCALPHA)
            rsurf.fill(background)
            rsurf.blit(surf, (0, 0))
            return rsurf

    def size(self, text):
        return ((self.width + self.hsep) * len(text), self.height + self.vsep)

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
        return self.height + self.vsep

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
        return self.rd["font"].vsize

    @size.setter
    def size(self, value):
        self.rd["font"].vsize = value

    def __init__(self, sprite, chars, hsep=0, vsep=0, size=12, underline=False,
                 bold=False, italic=False):
        self.rd = {}
        self.name = sprite.name
        self.rd["font"] = _PygameSpriteFont(sprite, chars, hsep, vsep, size)
        self.underline = underline
        self.bold = bold
        self.italic = italic
