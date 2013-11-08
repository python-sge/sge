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


__all__ = ['Sprite']


class Sprite(object):

    """Class which holds information for images and animations.

    This class stores images and information about how the SGE is to use
    those images.

    What image formats are supported depends on the implementation of
    the SGE, but image formats that are generally a good choice are PNG
    and JPEG.  See the implementation-specific information for a full
    list of supported formats.

    .. attribute:: width

       The width of the sprite.

    .. attribute:: height

       The height of the sprite.

    .. attribute:: origin_x

       The horizontal location of the origin relative to the left edge
       of the images.

    .. attribute:: origin_y

       The vertical location of the origin relative to the top edge of
       the images.

    .. attribute:: transparent

       Whether or not the image should be partially transparent.  If an
       image does not have an alpha channel, a colorkey will be used,
       with the transparent color being the color of the top-rightmost
       pixel.

    .. attribute:: fps

       The suggested rate in frames per second to animate the image at.

    .. attribute:: bbox_x

       The horizontal location relative to the sprite of the suggested
       bounding box to use with it.  If set to :const:`None`, it will
       become equal to ``-origin_x`` (which is always the left edge of
       the image).

    .. attribute:: bbox_y

       The vertical location relative to the sprite of the suggested
       bounding box to use with it.  If set to :const:`None`, it will
       become equal to ``-origin_y`` (which is always the top edge of
       the image).

    .. attribute:: bbox_width

       The width of the suggested bounding box.

    .. attribute:: bbox_height

       The height of the suggested bounding box.

    .. attribute:: name

       The name of the sprite given when it was created.  (Read-only)

    .. attribute:: id

       The unique identifier of the sprite.  (Read-only)

    """

    @property
    def width(self):
        return self._w

    @width.setter
    def width(self, value):
        if self._w != value:
            self._w = value
            self._set_size()
            self._refresh()

    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, value):
        if self._h != value:
            self._h = value
            self._set_size()
            self._refresh()

    @property
    def transparent(self):
        return self._transparent

    @transparent.setter
    def transparent(self, value):
        if self._transparent != value:
            self._transparent = value
            self._refresh()

    @property
    def bbox_x(self):
        return self._bbox_x

    @bbox_x.setter
    def bbox_x(self, value):
        if value is not None:
            self._bbox_x = value
        else:
            self._bbox_x = -self.origin_x

    @property
    def bbox_y(self):
        return self._bbox_y

    @bbox_y.setter
    def bbox_y(self, value):
        if value is not None:
            self._bbox_y = value
        else:
            self._bbox_y = -self.origin_y

    def __init__(self, name=None, ID=None, width=None, height=None,
                 origin_x=0, origin_y=0, transparent=True, fps=60,
                 bbox_x=None, bbox_y=None, bbox_width=None,
                 bbox_height=None):
        """Constructor method.

        Arguments:

        - ``name`` -- The base name of the image files, used to find all
          individual image files that make up the sprite's animation in
          the paths specified in :data:`sge.image_directories`.  One of
          the following rules will be used to find the images:

          - The base name plus a valid image extension.  If this rule is
            used, the image will be loaded as a single-frame sprite.
          - The base name and an integer separated by either a hyphen
            (``-``) or an underscore (``_``) and followed by a valid
            image extension.  If this rule is used, all images with
            names like this are loaded and treated as an animation, with
            the lower-numbered images being earlier frames.
          - The base name and an integer separated by either ``-strip``
            or ``_strip`` and followed by a valid image extension.  If
            this rule is used, the image will be treated as an animation
            read as a horizontal reel from left to right, split into the
            number of frames indicated by the integer.
          - If the base name is :const:`None`, the sprite will be a
            fully transparent rectangle at the specified size (with both
            ``width`` and ``height`` defaulting to 32 if they are set to
            :const:`None`).  The SGE decides what to assign to the
            sprite's :attr:`name` attribute in this case, but it will
            always be a string.

          If none of the above rules can be used, :exc:`IOError` is
          raised.

        - ``ID`` -- The value to assign :attr:`id` to.  If set to
          :const:`None`, ``name`` will be used, modified by the SGE if
          it is already the unique identifier of another sprite.

        All other arguments set the respective initial attributes of the
        sprite.  See the documentation for :class:`Sprite` for more
        information.

        """
        if sge.DEBUG:
            print('Creating sprite "{0}"'.format(name))

        self.name = name
        self._transparent = None
        self._baseimages = []
        self._images = []
        self._masks = {}

        fname_single = None
        fname_frames = []
        fname_strip = None

        if name is not None:
            if ID is not None:
                self.id = ID
            else:
                self.id = self.name

                i = 0
                while self.id in sge.game.sprites:
                    i += 1
                    self.id = "{0}{1}".format(self.name, i)

            for path in sge.image_directories:
                if os.path.isdir(path):
                    fnames = os.listdir(path)
                    for fname in fnames:
                        full_fname = os.path.join(path, fname)
                        if fname.startswith(name) and os.path.isfile(full_fname):
                            root, ext = os.path.splitext(fname)
                            if root == name:
                                split = [name, '']
                            elif root.rsplit('-', 1)[0] == name:
                                split = root.rsplit('-', 1)
                            elif root.rsplit('_', 1)[0] == name:
                                split = root.rsplit('_', 1)
                            else:
                                continue

                            if root == name:
                                fname_single = full_fname
                            elif split[1].isdigit():
                                n = int(split[1])
                                while len(fname_frames) - 1 < n:
                                    fname_frames.append(None)
                                fname_frames[n] = full_fname
                            elif (split[1].startswith('strip') and
                                  split[1][5:].isdigit()):
                                fname_strip = full_fname

            if fname_single:
                # Load the single image
                try:
                    img = pygame.image.load(fname_single)
                    self._baseimages.append(img)
                except pygame.error:
                    if sge.DEBUG:
                        print("Ignored {0}; not a valid image.".format(fname_single))

            if not self._baseimages and any(fname_frames):
                # Load the multiple images
                for fname in fname_frames:
                    if fname:
                        try:
                            self._baseimages.append(pygame.image.load(fname))
                        except pygame.error:
                            if sge.DEBUG:
                                print("Ignored {0}; not a valid image.".format(fname))

            if not self._baseimages and fname_strip:
                # Load the strip (sprite sheet)
                root, ext = os.path.splitext(os.path.basename(fname_strip))
                assert '-' in root or '_' in root
                assert (root.rsplit('-', 1)[0] == name or
                        root.rsplit('_', 1)[0] == name)
                if root.rsplit('-', 1)[0] == name:
                    split = root.rsplit('-', 1)
                else:
                    split = root.rsplit('_', 1)

                try:
                    sheet = pygame.image.load(fname_strip)
                    assert split[1][5:].isdigit()
                    n = int(split[1][5:])

                    img_w = max(1, sheet.get_width()) // n
                    img_h = max(1, sheet.get_height())
                    for x in xrange(0, img_w * n, img_w):
                        rect = pygame.Rect(x, 0, img_w, img_h)
                        img = sheet.subsurface(rect)
                        self._baseimages.append(img)
                except pygame.error:
                    if sge.DEBUG:
                        print("Ignored {0}; not a valid image.".format(fname_strip))

            if not self._baseimages:
                print("Directories searched:")
                for d in sge.image_directories:
                    print(os.path.normpath(os.path.abspath(d)))
                msg = 'Files for sprite name "{0}" not found.'.format(name)
                raise IOError(msg)
        else:
            # Name is None; default to a blank rectangle.
            if width is None:
                width = 32
            if height is None:
                height = 32

            # Choose name
            self.name = "sge-pygame-dynamicsprite"
            if ID is not None:
                self.id = ID
            else:
                self.id = 0
                while self.id in sge.game.sprites:
                    self.id += 1

            img = pygame.Surface((width, height), pygame.SRCALPHA)
            img.fill(pygame.Color(0, 0, 0, 0))
            self._baseimages.append(img)
            if sge.DEBUG:
                print("renamed to {0}, ID is {1}".format(self.name, self.id))

        if width is None:
            width = 1
            for image in self._baseimages:
                width = max(width, image.get_width())

        if height is None:
            height = 1
            for image in self._baseimages:
                height = max(height, image.get_height())

        if bbox_width is None:
            bbox_width = width

        if bbox_height is None:
            bbox_height = height

        self._w = width
        self._h = height
        self._set_size()
        self.origin_x = origin_x
        self.origin_y = origin_y
        self._transparent = transparent
        self.fps = fps
        self.bbox_x = bbox_x
        self.bbox_y = bbox_y
        self.bbox_width = bbox_width
        self.bbox_height = bbox_height
        self._refresh()
        sge.game.sprites[self.id] = self

    def draw_dot(self, x, y, color, frame=None):
        """Draw a single-pixel dot on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          draw the dot.
        - ``y`` -- The vertical location relative to the sprite to draw
          the dot.
        - ``color`` -- The color of the dot.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.

        """
        color = sge._get_pygame_color(color)
        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                self._baseimages[i].set_at((x, y), color)

        self._refresh()

    def draw_line(self, x1, y1, x2, y2, color, thickness=1, anti_alias=False,
                  frame=None):
        """Draw a line segment on the sprite.

        Arguments:

        - ``x1`` -- The horizontal location relative to the sprite of
          the first end point of the line segment.
        - ``y1`` -- The vertical location relative to the sprite of the
          first end point of the line segment.
        - ``x2`` -- The horizontal location relative to the sprite of
          the second end point of the line segment.
        - ``y2`` -- The vertical location relative to the sprite of the
          second end point of the line segment.
        - ``color`` -- The color of the line segment.
        - ``thickness`` -- The thickness of the line segment.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.

        """
        color = sge._get_pygame_color(color)
        thickness = abs(thickness)

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if anti_alias and thickness == 1:
                    pygame.draw.aaline(self._baseimages[i], color, (x1, y1),
                                       (x2, y2))
                else:
                    pygame.draw.line(self._baseimages[i], color, (x1, y1),
                                     (x2, y2), thickness)

        self._refresh()

    def draw_rectangle(self, x, y, width, height, fill=None, outline=None,
                       outline_thickness=1, frame=None):
        """Draw a rectangle on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          draw the rectangle.
        - ``y`` -- The vertical location relative to the sprite to draw
          the rectangle.
        - ``width`` -- The width of the rectangle.
        - ``height`` -- The height of the rectangle.
        - ``fill`` -- The color of the fill of the rectangle.
        - ``outline`` -- The color of the outline of the rectangle.
        - ``outline_thickness`` -- The thickness of the outline of the
          rectangle.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.

        """
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        rect = pygame.Rect(x, y, width, height)

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if fill is not None:
                    pygame.draw.rect(self._baseimages[i],
                                     sge._get_pygame_color(fill), rect, 0)

                if outline is not None:
                    pygame.draw.rect(self._baseimages[i],
                                     sge._get_pygame_color(outline), rect,
                                     outline_thickness)

        self._refresh()

    def draw_ellipse(self, x, y, width, height, fill=None, outline=None,
                     outline_thickness=1, anti_alias=False, frame=None):
        """Draw an ellipse on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          position the imaginary rectangle containing the ellipse.
        - ``y`` -- The vertical location relative to the sprite to
          position the imaginary rectangle containing the ellipse.
        - ``width`` -- The width of the ellipse.
        - ``height`` -- The height of the ellipse.
        - ``fill`` -- The color of the fill of the ellipse.
        - ``outline`` -- The color of the outline of the ellipse.
        - ``outline_thickness`` -- The thickness of the outline of the
          ellipse.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.

        """
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        rect = pygame.Rect(x, y, width, height)

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if fill is not None:
                    c = sge._get_pygame_color(fill)
                    pygame.draw.ellipse(self._baseimages[i], c, rect)

                if outline is not None:
                    c = sge._get_pygame_color(outline)
                    pygame.draw.ellipse(self._baseimages[i], c, rect,
                                        outline_thickness)

        self._refresh()

    def draw_circle(self, x, y, radius, fill=None, outline=None,
                    outline_thickness=1, anti_alias=False, frame=None):
        """Draw a circle on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          position the center of the circle.
        - ``y`` -- The vertical location relative to the sprite to
          position the center of the circle.
        - ``radius`` -- The radius of the circle.
        - ``fill`` -- The color of the fill of the circle.
        - ``outline`` -- The color of the outline of the circle.
        - ``outline_thickness`` -- The thickness of the outline of the
          circle.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.

        """
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if fill is not None:
                    c = sge._get_pygame_color(fill)
                    pygame.draw.circle(self._baseimages[i], c, (x, y), radius)

                if outline is not None:
                    c = sge._get_pygame_color(outline)
                    pygame.draw.circle(self._baseimages[i], c, (x, y), radius,
                                       outline_thickness)

        self._refresh()

    def draw_sprite(self, sprite, image, x, y, frame=None):
        """Draw another sprite on the sprite.

        Arguments:

        - ``sprite`` -- The sprite to draw with.
        - ``image`` -- The frame of ``sprite`` to draw with, where ``0``
          is the first frame.
        - ``x`` -- The horizontal location relative to ``self`` to draw
          ``sprite``.
        - ``y`` -- The vertical location relative to ``self`` to draw
          ``sprite``.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.

        """
        if not isinstance(sprite, sge.Sprite):
            sprite = sge.game.sprites[sprite]

        x -= sprite.origin_x
        y -= sprite.origin_y
        image %= len(sprite._baseimages)

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                self._baseimages[i].blit(sprite._baseimages[i], (x, y))

        self._refresh()

    def draw_text(self, font, text, x, y, width=None, height=None,
                  color="black", halign=sge.ALIGN_LEFT, valign=sge.ALIGN_TOP,
                  anti_alias=True, frame=None):
        """Draw text on the sprite.

        Arguments:

        - ``font`` -- The font to use to draw the text.
        - ``text`` -- The text (as a string) to draw.
        - ``x`` -- The horizontal location relative to the sprite to
          draw the text.
        - ``y`` -- The vertical location relative to the sprite to draw
          the text.
        - ``width`` -- The width of the imaginary rectangle the text is
          drawn in; set to :const:`None` to make the rectangle as wide
          as needed to contain the text without additional line breaks.
          If set to something other than :const:`None`, a line which
          does not fit will be automatically split into multiple lines
          that do fit.
        - ``height`` -- The height of the imaginary rectangle the text
          is drawn in; set to :const:`None` to make the rectangle as
          tall as needed to contain the text.
        - ``color`` -- The color of the text.
        - ``halign`` -- The horizontal alignment of the text and the
          horizontal location of the origin of the imaginary rectangle
          the text is drawn in.  Can be set to one of the following:

          - :data:`sge.ALIGN_LEFT` -- Align the text to the left of the
            imaginary rectangle the text is drawn in.  Set the origin of
            the imaginary rectangle to its left edge.
          - :data:`sge.ALIGN_CENTER` -- Align the text to the center of
            the imaginary rectangle the text is drawn in.  Set the
            origin of the imaginary rectangle to its center.
          - :data:`sge.ALIGN_RIGHT` -- Align the text to the right of
            the imaginary rectangle the text is drawn in.  Set the
            origin of the imaginary rectangle to its right edge.

        - ``valign`` -- The vertical alignment of the text and the
          vertical location of the origin of the imaginary rectangle the
          text is drawn in.  Can be set to one of the following:

          - :data:`sge.ALIGN_TOP` -- Align the text to the top of the
            imaginary rectangle the text is drawn in.  Set the origin of
            the imaginary rectangle to its top edge.  If the imaginary
            rectangle is not tall enough to contain all of the text, cut
            text off from the bottom.
          - :data:`sge.ALIGN_MIDDLE` -- Align the the text to the middle
            of the imaginary rectangle the text is drawn in.  Set the
            origin of the imaginary rectangle to its middle.  If the
            imaginary rectangle is not tall enough to contain all of the
            text, cut text off equally from the top and bottom.
          - :data:`sge.ALIGN_BOTTOM` -- Align the text  to the bottom of
            the imaginary rectangle the text is drawn in.  Set the
            origin of the imaginary rectangle to its top edge.  If the
            imaginary rectangle is not tall enough to contain all of the
            text, cut text off from the top.

        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.

        """
        if not isinstance(font, sge.Font):
            font = sge.game.fonts[font]

        lines = font._split_text(text, width)
        width, height = font.get_size(text, width, height)
        fake_height = font.get_size(text, width)[1]
        color = sge._get_pygame_color(color)

        text_surf = pygame.Surface((width, fake_height), pygame.SRCALPHA)
        box_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        text_rect = text_surf.get_rect()
        box_rect = box_surf.get_rect()

        for i in xrange(len(lines)):
            rendered_text = font._font.render(lines[i], anti_alias, color)
            rect = rendered_text.get_rect()
            rect.top = i * font._font.get_linesize()

            if halign == sge.ALIGN_LEFT:
                rect.left = text_rect.left
            elif halign == sge.ALIGN_RIGHT:
                rect.right = text_rect.right
            elif halign == sge.ALIGN_CENTER:
                rect.centerx = text_rect.centerx

            text_surf.blit(rendered_text, rect)

        if valign == sge.ALIGN_TOP:
            text_rect.top = box_rect.top
        elif valign == sge.ALIGN_BOTTOM:
            text_rect.bottom = box_rect.bottom
        elif valign == sge.ALIGN_MIDDLE:
            text_rect.centery = box_rect.centery

        box_surf.blit(text_surf, text_rect)

        if halign == sge.ALIGN_LEFT:
            box_rect.left = x
        elif halign == sge.ALIGN_RIGHT:
            box_rect.right = x
        elif halign == sge.ALIGN_CENTER:
            box_rect.centerx = x
        else:
            box_rect.left = x

        if valign == sge.ALIGN_TOP:
            box_rect.top = y
        elif valign == sge.ALIGN_BOTTOM:
            box_rect.bottom = y
        elif valign == sge.ALIGN_MIDDLE:
            box_rect.centery = y
        else:
            box_rect.top = y

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                self._baseimages[i].blit(box_surf, box_rect)

        self._refresh()

    def draw_clear(self, frame=None):
        """Erase everything from the sprite.

        Arguments:

        - ``frame`` -- The frame of the sprite to clear, where ``0`` is
          the first frame; set to :const:`None` to clear all frames.

        """
        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if self._baseimages[i].get_flags() & pygame.SRCALPHA:
                    color = pygame.Color(0, 0, 0, 0)
                else:
                    color = self._baseimages[i].get_colorkey()

                self._baseimages[i].fill(color)

        self._refresh()

    def save(self, fname):
        """Save the sprite to an image file.

        Arguments:

        - ``fname`` -- The path of the file to save the sprite to.  If
          it is not a path that can be saved to, :exc:`IOError` is
          raised.

        If the sprite has multiple frames, the image file saved will be
        a horizontal reel of each of the frames from left to right with
        no space in between the frames.

        """
        # Assuming self.width and self.height are the size of all
        # surfaces in _baseimages (this should be the case).
        w = self.width * len(self._baseimages)
        h = self.height
        reel = pygame.Surface((w, h), pygame.SRCALPHA)
        reel.fill(pygame.Color(0, 0, 0, 0))

        for i in xrange(len(self._baseimages)):
            reel.blit(self._baseimages[i], (self.width * i, 0))

        try:
            pygame.image.save(reel, fname)
        except pygame.error:
            m = 'Couldn\'t save to "{0}"'.format(
                os.path.normpath(os.path.realpath(fname)))
            raise IOError(m)

    @classmethod
    def from_screenshot(cls, x=0, y=0, width=None, height=None):
        """Return the current display on the screen as a sprite.

        Arguments:

        - ``x`` -- The horizontal location of the rectangular area to
          take a screenshot of.
        - ``y`` -- The vertical location of the rectangular area to take
          a screenshot of.
        - ``width`` -- The width of the area to take a screenshot of;
          set to None for all of the area to the right of ``x`` to be
          included.
        - ``height`` -- The height of the area to take a screenshot of;
          set to :const:`None` for all of the area below ``y`` to be
          included.

        If you only wish to save a screenshot (of the entire screen) to
        a file, the easiest way to do that is::

            sge.Sprite.from_screenshot().save("foo.png")

        """
        window = pygame.display.get_surface()
        w = sge.game.width * sge.game._xscale
        h = sge.game.height * sge.game._yscale
        display_surf = pygame.Surface((w, h))
        display_surf.blit(window, (-sge.game._x, -sge.game._y))

        if sge.game.scale_smooth:
            try:
                display_surf = pygame.transform.smoothscale(
                    display_surf, (sge.game.width, sge.game.height))
            except pygame.error:
                display_surf = pygame.transform.scale(
                    display_surf, (sge.game.width, sge.game.height))
        else:
            display_surf = pygame.transform.scale(
                display_surf, (sge.game.width, sge.game.height))

        if width is None:
            width = display_surf.get_width() - x
        if height is None:
            height = display_surf.get_height() - y

        sprite = cls(width=width, height=height)
        sprite._baseimages[0].blit(display_surf, (-x, -y))
        sprite._refresh()
        return sprite

    def _set_size(self):
        # Adjust the size of the base images.  Note: this change is
        # destructive and irreversible.  It is necessary for the drawing
        # methods to work properly, specifically whenever ``width`` and
        # ``height`` are set.  As a result, setting ``width`` and
        # ``height`` is destructive in this implementation.
        for i in xrange(len(self._baseimages)):
            if sge.game.scale_smooth:
                try:
                    self._baseimages[i] = pygame.transform.smoothscale(
                        self._baseimages[i], (self.width, self.height))
                except pygame.error:
                    self._baseimages[i] = pygame.transform.scale(
                        self._baseimages[i], (self.width, self.height))
            else:
                self._baseimages[i] = pygame.transform.scale(
                    self._baseimages[i], (self.width, self.height))

    def _refresh(self):
        # Set the _images list based on the variables.
        sge.game._background_changed = True
        self._images = []
        for image in self._baseimages:
            img = self._set_transparency(image)
            img = sge._scale(img, self.width, self.height)
            self._images.append({(1, 1, 0, 255, None):img})

    def _set_transparency(self, image):
        # Return a copy of the surface with transparency properly set
        # for this sprite's settings.
        if self.transparent and image.get_width() > 0:
            if image.get_flags() & pygame.SRCALPHA:
                return image.convert_alpha()
            else:
                colorkey_img = image.convert()
                color = image.get_at((image.get_width() - 1, 0))
                colorkey_img.set_colorkey(color, pygame.RLEACCEL)
                return colorkey_img
        else:
            return image.convert()

    def _get_image(self, num, xscale=1, yscale=1, rotation=0, alpha=255,
                   blend=None):
        num %= len(self._images)
        # Return the properly sized surface.
        if (xscale, yscale, rotation, alpha, blend) in self._images[num]:
            return self._images[num][(xscale, yscale, rotation, alpha, blend)]
        else:
            # Hasn't been scaled to this size yet
            if xscale != 0 and yscale != 0:
                img = self._set_transparency(self._baseimages[num])
                xflip = xscale < 0
                yflip = yscale < 0
                img = pygame.transform.flip(img, xflip, yflip)
                img = sge._scale(img, self.width * abs(xscale),
                             self.height * abs(yscale))

                if rotation != 0:
                    img = pygame.transform.rotate(img, rotation)

                if alpha < 255:
                    if img.get_flags() & pygame.SRCALPHA:
                        # Have to do this the more difficult way.
                        img.fill((0, 0, 0, 255 - alpha), None,
                                 pygame.BLEND_RGBA_SUB)
                    else:
                        img.set_alpha(alpha, pygame.RLEACCEL)

                if blend is not None:
                    img.fill(sge._get_pygame_color(blend), None,
                             pygame.BLEND_RGB_MULT)
            else:
                img = pygame.Surface((1, 1))
                img.set_colorkey((0, 0, 0), pygame.RLEACCEL)

            self._images[num][(xscale, yscale, rotation, alpha, blend)] = img
            return img

    def _get_precise_mask(self, num):
        # Return a precise mask (2D list of True/False values) for the
        # given image index.
        if num in self._masks:
            return self._masks[num]
        else:
            image = self._get_image(num)
            image.lock()
            mask = []
            if image.get_flags() & pygame.SRCALPHA:
                for x in xrange(image.get_width()):
                    mask.append([])
                    for y in xrange(image.get_height()):
                        mask[x].append(image.get_at((x, y)).a > 0)
            else:
                colorkey = image.get_colorkey()
                for x in xrange(image.get_width()):
                    mask.append([])
                    for y in xrange(image.get_height()):
                        mask[x].append(image.get_at((x, y)) == colorkey)

            image.unlock()
            self._masks[num] = mask
            return mask
