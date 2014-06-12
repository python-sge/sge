# Copyright (C) 2012, 2013, 2014 Julian Marchant <onpon4@riseup.net>
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

import os
import warnings

import pygame

import sge


__all__ = ['Sprite']


class Sprite:

    """Class which holds information for images and animations.

    This class stores images and information about how the SGE is to use
    those images.

    What image formats are supported depends on the implementation of
    the SGE, but image formats that are generally a good choice are PNG
    and JPEG.  See the implementation-specific information for a full
    list of supported formats.

    .. attribute:: width

       The width of the sprite.

       .. note::

          Changing this attribute is a destructive transformation: it
          can result in loss of pixel information, especially if it is
          done repeatedly.  Because of this, it is advised that you do
          not adjust this value for routine scaling.  Use the
          :attr:`image_xscale` attribute of a :class:`sge.StellarClass`
          object instead.

    .. attribute:: height

       The height of the sprite.

       .. note::

          Changing this attribute is a destructive transformation: it
          can result in loss of pixel information, especially if it is
          done repeatedly.  Because of this, it is advised that you do
          not adjust this value for routine scaling.  Use the
          :attr:`image_yscale` attribute of a :class:`sge.StellarClass`
          object instead.

    .. attribute:: transparent

       Whether or not the image should be partially transparent.  If an
       image does not have an alpha channel, a colorkey will be used,
       with the transparent color being the color of the top-rightmost
       pixel.

    .. attribute:: origin_x

       The suggested horizontal location of the origin relative to the
       left edge of the images.

    .. attribute:: origin_y

       The suggested vertical location of the origin relative to the top
       edge of the images.

    .. attribute:: fps

       The suggested rate in frames per second to animate the image at.

    .. attribute:: speed

       The suggested rate to animate the image at as a factor of
       :attr:`sge.game.fps`.

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

    .. attribute:: frames

       The number of animation frames in the sprite.  (Read-only)

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
    def speed(self):
        return self.fps / sge.game.fps

    @speed.setter
    def speed(self, value):
        self.fps = value * sge.game.fps

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

    @property
    def frames(self):
        return len(self._baseimages)

    def __init__(self, name=None, ID=None, width=None, height=None,
                 transparent=True, origin_x=0, origin_y=0, fps=60,
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
            print('Creating sprite "{}"'.format(name))

        sprites = sge.game.sprites.copy()

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
                while self.id in sprites:
                    i += 1
                    self.id = "{}{}".format(self.name, i)

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
                except pygame.error:
                    if sge.DEBUG:
                        print("Ignored {}; not a valid image.".format(fname_single))
                else:
                    self._baseimages.append(img)

            if not self._baseimages and any(fname_frames):
                # Load the multiple images
                for fname in fname_frames:
                    if fname:
                        try:
                            img = pygame.image.load(fname)
                        except pygame.error:
                            if sge.DEBUG:
                                print("Ignored {}; not a valid image.".format(fname))
                        else:
                            self._baseimages.append(img)

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
                except pygame.error:
                    if sge.DEBUG:
                        print("Ignored {}; not a valid image.".format(fname_strip))
                else:
                    assert split[1][5:].isdigit()
                    n = int(split[1][5:])

                    img_w = max(1, sheet.get_width()) // n
                    img_h = max(1, sheet.get_height())
                    for x in range(0, img_w * n, img_w):
                        rect = pygame.Rect(x, 0, img_w, img_h)
                        img = sheet.subsurface(rect)
                        self._baseimages.append(img)

            if not self._baseimages:
                print("Directories searched:")
                for d in sge.image_directories:
                    print(os.path.normpath(os.path.abspath(d)))
                msg = 'Files for sprite name "{}" not found.'.format(name)
                raise IOError(msg)
        else:
            # Name is None; default to a blank rectangle.
            if width is None:
                width = 32
            if height is None:
                height = 32

            self._w = width
            self._h = height

            # Choose name
            self.name = "sge-pygame-dynamicsprite"
            if ID is not None:
                self.id = ID
            else:
                self.id = 0
                while self.id in sprites:
                    self.id += 1

            self.append_frame()
            if sge.DEBUG:
                print("renamed to {}, ID is {}".format(self.name, self.id))

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
        self._locked = False
        self._refresh()
        sprites[self.id] = self
        sge.game.sprites = sprites

    def append_frame(self):
        """Append a new blank frame to the end of the sprite."""
        img = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        img.fill(pygame.Color(0, 0, 0, 0))
        self._baseimages.append(img)

    def insert_frame(self, frame):
        """Insert a new blank frame into the sprite.

        Arguments:

        - ``frame`` -- The frame of the sprite to insert the new frame
          in front of, where ``0`` is the first frame.

        """
        img = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        img.fill(pygame.Color(0, 0, 0, 0))
        self._baseimages.insert(frame, img)

    def delete_frame(self, frame):
        """Delete a frame from the sprite.

        Arguments:

        - ``frame`` -- The frame of the sprite to delete, where ``0`` is
          the first frame.

        """
        del self._baseimages[frame]

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
        if color.a == 255:
            for i in range(self.frames):
                if frame is None or frame % self.frames == i:
                    self._baseimages[i].set_at((x, y), color)
        else:
            rect = pygame.Rect(x, y, 1, 1)
            for i in range(self.frames):
                if frame is None or frame % self.frames == i:
                    self._baseimages[i].set_at((x, y), color)
                    pygame.draw.rect(self._baseimages[i], color, rect)

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

        for i in range(self.frames):
            if frame is None or frame % self.frames == i:
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

        for i in range(self.frames):
            if frame is None or frame % self.frames == i:
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

        for i in range(self.frames):
            if frame is None or frame % self.frames == i:
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

        for i in range(self.frames):
            if frame is None or frame % self.frames == i:
                if fill is not None:
                    c = sge._get_pygame_color(fill)
                    pygame.draw.circle(self._baseimages[i], c, (x, y), radius)

                if outline is not None:
                    c = sge._get_pygame_color(outline)
                    pygame.draw.circle(self._baseimages[i], c, (x, y), radius,
                                       outline_thickness)

        self._refresh()

    def draw_sprite(self, sprite, image, x, y, frame=None, blend_mode=None):
        """Draw another sprite on the sprite.

        Arguments:

        - ``sprite`` -- The sprite to draw with.
        - ``image`` -- The frame of ``sprite`` to draw with, where ``0``
          is the first frame.
        - ``x`` -- The horizontal location relative to ``self`` to
          position the origin of ``sprite``.
        - ``y`` -- The vertical location relative to ``self`` to
          position the origin of ``sprite``.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.
        - ``blend_mode`` -- The blend mode to use.  Possible blend modes
          are:

          - :data:`sge.BLEND_NORMAL`
          - :data:`sge.BLEND_RGBA_ADD`
          - :data:`sge.BLEND_RGBA_SUBTRACT`
          - :data:`sge.BLEND_RGBA_MULTIPLY`
          - :data:`sge.BLEND_RGBA_SCREEN`
          - :data:`sge.BLEND_RGBA_MINIMUM`
          - :data:`sge.BLEND_RGBA_MAXIMUM`
          - :data:`sge.BLEND_RGB_ADD`
          - :data:`sge.BLEND_RGB_SUBTRACT`
          - :data:`sge.BLEND_RGB_MULTIPLY`
          - :data:`sge.BLEND_RGB_SCREEN`
          - :data:`sge.BLEND_RGB_MINIMUM`
          - :data:`sge.BLEND_RGB_MAXIMUM`

          :const:`None` is treated as :data:`sge.BLEND_NORMAL`.

        """
        if not isinstance(sprite, sge.Sprite):
            sprite = sge.game.sprites[sprite]

        x -= sprite.origin_x
        y -= sprite.origin_y
        image %= len(sprite._baseimages)

        if blend_mode is not None and blend_mode & sge.BLEND_SCREEN:
            w = "Screen blend mode not supported. Normal blending used instead."
            warnings.warn(w)

        pygame_flags = {
            sge.BLEND_RGBA_ADD: pygame.BLEND_RGBA_ADD,
            sge.BLEND_RGBA_SUBTRACT: pygame.BLEND_RGBA_SUB,
            sge.BLEND_RGBA_MULTIPLY: pygame.BLEND_RGBA_MULT,
            sge.BLEND_RGBA_MINIMUM: pygame.BLEND_RGBA_MIN,
            sge.BLEND_RGBA_MAXIMUM: pygame.BLEND_RGBA_MAX,
            sge.BLEND_RGB_ADD: pygame.BLEND_RGB_ADD,
            sge.BLEND_RGB_SUBTRACT: pygame.BLEND_RGB_SUB,
            sge.BLEND_RGB_MULTIPLY: pygame.BLEND_RGB_MULT,
            sge.BLEND_RGB_MINIMUM: pygame.BLEND_RGB_MIN,
            sge.BLEND_RGB_MAXIMUM: pygame.BLEND_RGB_MAX
            }.setdefault(blend_mode, 0)

        for i in range(self.frames):
            if frame is None or frame % self.frames == i:
                self._baseimages[i].blit(sprite._baseimages[image], (x, y),
                                         None, pygame_flags)

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

        for i in range(len(lines)):
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

        for i in range(self.frames):
            if frame is None or frame % self.frames == i:
                self._baseimages[i].blit(box_surf, box_rect)

        self._refresh()

    def draw_erase(self, x, y, width, height, frame=None):
        """Erase part of the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite of the
          area to erase.
        - ``y`` -- The vertical location relative to the sprite of the
          area to erase.
        - ``width`` -- The width of the area to erase.
        - ``height`` -- The height of the area to erase.
        - ``frame`` -- The frame of the sprite to erase from, where
          ``0`` is the first frame; set to :const:`None` to erase from
          all frames.

        """
        for i in range(self.frames):
            if frame is None or frame % self.frames == i:
                if self._baseimages[i].get_flags() & pygame.SRCALPHA:
                    color = pygame.Color(0, 0, 0, 0)
                else:
                    color = self._baseimages[i].get_colorkey()

                rect = pygame.Rect(x, y, width, height)
                self._baseimages[i].fill(color, rect)

        self._refresh()

    def draw_clear(self, frame=None):
        """Erase everything from the sprite.

        Arguments:

        - ``frame`` -- The frame of the sprite to clear, where ``0`` is
          the first frame; set to :const:`None` to clear all frames.

        """
        self.draw_erase(0, 0, self.width, self.height, frame)

    def draw_lock(self):
        """Lock the sprite for continuous drawing.

        Use this method to "lock" the sprite for being drawn on several
        times in a row.  What exactly this does depends on the
        implementation and it may even do nothing at all, but calling
        this method before doing several draw actions on the sprite in a
        row gives the SGE a chance to make the drawing more efficient.

        After you are done with continuous drawing, call
        :meth:`sge.Sprite.draw_unlock` to let the SGE know that you are
        done drawing.

        .. warning::

           Do not cause a sprite to be used while it's locked.  For
           example, don't leave it locked for the duration of a frame,
           and don't draw it or project it on anything.  The effect of
           using a locked sprite could be as minor as graphical errors
           and as severe as crashing the program, depending on the SGE
           implementation.  Always call :meth:`sge.Sprite.draw_unlock`
           immediately after you're done drawing for a while.

        """
        if not self._locked:
            self._locked = True
            for img in self._baseimages:
                img.lock()

    def draw_unlock(self):
        """Unlock the sprite.

        Use this method to "unlock" the sprite after it has been
        "locked" for continuous drawing by :meth:`sge.Sprite.draw_lock`.

        """
        if self._locked:
            self._locked = False
            for img in self._baseimages:
                img.unlock()
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
        w = self.width * self.frames
        h = self.height
        reel = pygame.Surface((w, h), pygame.SRCALPHA)
        reel.fill(pygame.Color(0, 0, 0, 0))

        for i in range(self.frames):
            reel.blit(self._baseimages[i], (self.width * i, 0))

        try:
            pygame.image.save(reel, fname)
        except pygame.error:
            m = 'Couldn\'t save to "{}"'.format(
                os.path.normpath(os.path.realpath(fname)))
            raise IOError(m)

    def destroy(self):
        """Destroy the sprite.

        .. note::

           If the sprite is being used, for example, by a
           :class:`sge.StellarClass` object, it will not be completely
           destroyed until this use stops.

        """
        sprites = sge.game.sprites.copy()
        if self.id in sprites:
            del sprites[self.id]
        sge.game.sprites = sprites

    @classmethod
    def from_tileset(cls, name, ID=None, x=0, y=0, columns=1, rows=1, xsep=0,
                     ysep=0, width=1, height=1, origin_x=0, origin_y=0,
                     transparent=True, fps=0, bbox_x=None, bbox_y=None,
                     bbox_width=None, bbox_height=None):
        """Return a sprite based on the tiles in a tileset.

        Arguments:

        - ``name`` -- The base name of the image file containing the
          tileset, not including the file extension, to be found in one
          of the paths specified in :data:`sge.image_directories`.
        - ``x`` -- The horizontal location relative to the image of the
          top-leftmost tile in the tileset.
        - ``y`` -- The vertical location relative to the image of the
          top-leftmost tile in the tileset.
        - ``columns`` -- The number of columns in the tileset.
        - ``rows`` -- The number of rows in the tileset.
        - ``xsep`` -- The spacing between columns in the tileset.
        - ``ysep`` -- The spacing between rows in the tileset.
        - ``width`` -- The width of the tiles.
        - ``height`` -- The height of the tiles.

        For all other arguments, see the documentation for
        :meth:`Sprite.__init__`.

        Each tile in the tileset becomes a subimage of the returned
        sprite, ordered first from left to right and then from top to
        bottom.

        """
        self = cls(name, ID=ID, width=width, height=height, origin_x=origin_x,
                   origin_y=origin_y, transparent=transparent, fps=fps,
                   bbox_x=bbox_x, bbox_y=bbox_y, bbox_width=bbox_width,
                   bbox_height=bbox_height)
        tileset = Sprite(name, origin_x=x, origin_y=y)

        for i in range(1, rows):
            for j in range(1, columns):
                self.append_frame()

        self.draw_clear()

        for i in range(rows):
            for j in range(columns):
                frame = i * columns + j
                x_ = (width + xsep) * j
                y_ = (height + ysep) * i
                self.draw_sprite(tileset, 0, -x_ - self.origin_x,
                                 -y_ - self.origin_y, frame=frame)

        tileset.destroy()
        return self

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
        width = int(round(self.width))
        height = int(round(self.height))
        for i in range(self.frames):
            if sge.game.scale_smooth:
                try:
                    self._baseimages[i] = pygame.transform.smoothscale(
                        self._baseimages[i], (width, height))
                except pygame.error:
                    self._baseimages[i] = pygame.transform.scale(
                        self._baseimages[i], (width, height))
            else:
                self._baseimages[i] = pygame.transform.scale(
                    self._baseimages[i], (width, height))

    def _refresh(self):
        # Set the _images list based on the variables.
        if not self._locked:
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
        t = (sge.game._xscale, sge.game._yscale, xscale, yscale, rotation,
             alpha, blend)
        if t in self._images[num]:
            return self._images[num][t]
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

            self._images[num][t] = img
            return img

    def _get_precise_mask(self, num, xscale, yscale, rotation):
        # Return a precise mask (2D list of True/False values) for the
        # given image index.
        mask_id = (num, xscale, yscale, rotation)
        if mask_id in self._masks:
            return self._masks[mask_id]
        else:
            #image = self._get_image(num, xscale, yscale, rotation)
            image = self._set_transparency(self._baseimages[num])
            xflip = xscale < 0
            yflip = yscale < 0
            image = pygame.transform.flip(image, xflip, yflip)
            image = pygame.transform.scale(image, (self.width * abs(xscale),
                                                   self.height * abs(yscale)))
            if rotation:
                image = pygame.transform.rotate(image, rotation)

            image.lock()
            mask = []
            if image.get_flags() & pygame.SRCALPHA:
                for x in range(image.get_width()):
                    mask.append([])
                    for y in range(image.get_height()):
                        mask[x].append(image.get_at((x, y)).a > 0)
            else:
                colorkey = image.get_colorkey()
                for x in range(image.get_width()):
                    mask.append([])
                    for y in range(image.get_height()):
                        mask[x].append(image.get_at((x, y)) == colorkey)

            image.unlock()
            self._masks[mask_id] = mask
            return mask
