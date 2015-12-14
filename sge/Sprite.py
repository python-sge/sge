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
import warnings

import pygame
import six

import sge
from sge import r
from sge.r import (_get_blend_flags, _screen_blend, f_split_text, s_set_size,
                   s_refresh, s_set_transparency)


__all__ = ['Sprite']


class Sprite(object):

    """
    This class stores images and information about how the SGE is to use
    those images.

    What image formats are supported depends on the implementation of
    the SGE, but image formats that are generally a good choice are PNG
    and JPEG.  See the implementation-specific information for a full
    list of supported formats.

    .. attribute:: width

       The width of the sprite.

       .. note::

          Changing this attribute will cause the sprite to be scaled
          horizontally.  This is a destructive transformation: it can
          result in loss of pixel information, especially if it is done
          repeatedly.  Because of this, it is advised that you do not
          adjust this value for routine scaling.  Use the
          :attr:`image_xscale` attribute of a :class:`sge.Object`
          object instead.

    .. attribute:: height

       The height of the sprite.

       .. note::

          Changing this attribute will cause the sprite to be scaled
          vertically.  This is a destructive transformation: it can
          result in loss of pixel information, especially if it is done
          repeatedly.  Because of this, it is advised that you do not
          adjust this value for routine scaling.  Use the
          :attr:`image_yscale` attribute of a :class:`sge.Object`
          object instead.

    .. attribute:: transparent

       Whether or not the image should be partially transparent.  If an
       image does not have an alpha channel, a colorkey will be used,
       with the transparent color being the color of the top-rightmost
       pixel of the respective frame.

    .. attribute:: origin_x

       The suggested horizontal location of the origin relative to the
       left edge of the images.

    .. attribute:: origin_y

       The suggested vertical location of the origin relative to the top
       edge of the images.

    .. attribute:: fps

       The suggested rate in frames per second to animate the image at.
       Can be negative, in which case animation will be reversed.

    .. attribute:: speed

       The suggested rate to animate the image at as a factor of
       :attr:`sge.game.fps`.  Can be negative, in which case animation
       will be reversed.

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

    .. attribute:: frames

       The number of animation frames in the sprite.  (Read-only)

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def width(self):
        return self.__w

    @width.setter
    def width(self, value):
        if self.__w != value:
            self.__w = int(round(value))
            s_set_size(self)
            s_refresh(self)

    @property
    def height(self):
        return self.__h

    @height.setter
    def height(self, value):
        if self.__h != value:
            self.__h = int(round(value))
            s_set_size(self)
            s_refresh(self)

    @property
    def transparent(self):
        return self.__transparent

    @transparent.setter
    def transparent(self, value):
        if self.__transparent != value:
            self.__transparent = value
            s_refresh(self)

    @property
    def speed(self):
        return self.fps / sge.game.fps

    @speed.setter
    def speed(self, value):
        self.fps = value * sge.game.fps

    @property
    def bbox_x(self):
        return self.__bbox_x

    @bbox_x.setter
    def bbox_x(self, value):
        if value is not None:
            self.__bbox_x = value
        else:
            self.__bbox_x = -self.origin_x

    @property
    def bbox_y(self):
        return self.__bbox_y

    @bbox_y.setter
    def bbox_y(self, value):
        if value is not None:
            self.__bbox_y = value
        else:
            self.__bbox_y = -self.origin_y

    @property
    def frames(self):
        return len(self.rd["baseimages"])

    def __init__(self, name=None, directory="", width=None, height=None,
                 transparent=True, origin_x=0, origin_y=0, fps=60, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None):
        """
        Arguments:

        - ``name`` -- The base name of the image files, used to find all
          individual image files that make up the sprite's animation`.
          One of the following rules will be used to find the images:

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

        - ``directory`` -- The directory to search for image files in.

        All other arguments set the respective initial attributes of the
        sprite.  See the documentation for :class:`Sprite` for more
        information.
        """
        self.rd = {}
        self.name = name
        self.__transparent = None
        self.rd["baseimages"] = []
        self.rd["drawcycle"] = 0

        fname_single = []
        fname_frames = []
        fname_strip = []
        errlist = []

        if name is not None:
            if not directory:
                directory = os.curdir
            for fname in os.listdir(directory):
                full_fname = os.path.join(directory, fname)
                if (fname.startswith(name) and
                        os.path.isfile(full_fname)):
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
                        fname_single.append(full_fname)
                    elif split[1].isdigit():
                        n = int(split[1])
                        while len(fname_frames) - 1 < n:
                            fname_frames.append(None)
                        fname_frames[n] = full_fname
                    elif (split[1].startswith('strip') and
                          split[1][5:].isdigit()):
                        fname_strip.append(full_fname)

            if any(fname_single):
                # Load the single image
                for fname in fname_single:
                    try:
                        img = pygame.image.load(fname)
                    except pygame.error as e:
                        errlist.append(e)
                    else:
                        self.rd["baseimages"].append(img)

            if not self.rd["baseimages"] and any(fname_frames):
                # Load the multiple images
                for fname in fname_frames:
                    if fname:
                        try:
                            img = pygame.image.load(fname)
                        except pygame.error as e:
                            errlist.append(e)
                        else:
                            self.rd["baseimages"].append(img)

            if not self.rd["baseimages"] and any(fname_strip):
                # Load the strip (sprite sheet)
                for fname in fname_strip:
                    root, ext = os.path.splitext(os.path.basename(fname))
                    assert '-' in root or '_' in root
                    assert (root.rsplit('-', 1)[0] == name or
                            root.rsplit('_', 1)[0] == name)
                    if root.rsplit('-', 1)[0] == name:
                        split = root.rsplit('-', 1)
                    else:
                        split = root.rsplit('_', 1)

                    try:
                        sheet = pygame.image.load(fname)
                    except pygame.error as e:
                        errlist.append(e)
                    else:
                        assert split[1][5:].isdigit()
                        n = int(split[1][5:])

                        img_w = max(1, sheet.get_width()) // n
                        img_h = max(1, sheet.get_height())
                        for x in six.moves.range(0, img_w * n, img_w):
                            rect = pygame.Rect(x, 0, img_w, img_h)
                            img = sheet.subsurface(rect)
                            self.rd["baseimages"].append(img)

            if not self.rd["baseimages"]:
                print("Pygame errors during search:")
                if errlist:
                    for e in errlist:
                        print(e)
                else:
                    print("None")
                msg = 'Supported file(s) for sprite name "{}" not found in {}'.format(name, directory)
                raise IOError(msg)
        else:
            # Name is None; default to a blank rectangle.
            if width is None:
                width = 32
            if height is None:
                height = 32

            self.__w = width
            self.__h = height

            # Choose name
            self.name = "sge-pygame-dynamicsprite"

            self.append_frame()

        if width is None:
            width = 1
            for image in self.rd["baseimages"]:
                width = max(width, image.get_width())

        if height is None:
            height = 1
            for image in self.rd["baseimages"]:
                height = max(height, image.get_height())

        if bbox_width is None:
            bbox_width = width

        if bbox_height is None:
            bbox_height = height

        self.__w = width
        self.__h = height
        s_set_size(self)
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.__transparent = transparent
        self.fps = fps
        self.bbox_x = bbox_x
        self.bbox_y = bbox_y
        self.bbox_width = bbox_width
        self.bbox_height = bbox_height
        self.rd["locked"] = False
        s_refresh(self)

    def append_frame(self):
        """Append a new blank frame to the end of the sprite."""
        img = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        img.fill(pygame.Color(0, 0, 0, 0))
        self.rd["baseimages"].append(img)

    def insert_frame(self, frame):
        """
        Insert a new blank frame into the sprite.

        Arguments:

        - ``frame`` -- The frame of the sprite to insert the new frame
          in front of, where ``0`` is the first frame.
        """
        img = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        img.fill(pygame.Color(0, 0, 0, 0))
        self.rd["baseimages"].insert(frame, img)

    def delete_frame(self, frame):
        """
        Delete a frame from the sprite.

        Arguments:

        - ``frame`` -- The frame of the sprite to delete, where ``0`` is
          the first frame.
        """
        del self.rd["baseimages"][frame]

    def draw_dot(self, x, y, color, frame=None):
        """
        Draw a single-pixel dot on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          draw the dot.
        - ``y`` -- The vertical location relative to the sprite to draw
          the dot.
        - ``color`` -- A :class:`sge.Color` object representing the
          color of the dot.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.
        """
        if not isinstance(color, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(color))
            raise TypeError(e)

        x = int(round(x))
        y = int(round(y))
        pg_color = pygame.Color(*color)
        if color.alpha == 255:
            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    self.rd["baseimages"][i].set_at((x, y), pg_color)
        else:
            stamp = pygame.Surface((1, 1), pygame.SRCALPHA)
            stamp.fill(pg_color)
            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    self.rd["baseimages"][i].blit(stamp, (x, y))

        s_refresh(self)

    def draw_line(self, x1, y1, x2, y2, color, thickness=1, anti_alias=False,
                  frame=None):
        """
        Draw a line segment on the sprite.

        Arguments:

        - ``x1`` -- The horizontal location relative to the sprite of
          the first end point of the line segment.
        - ``y1`` -- The vertical location relative to the sprite of the
          first end point of the line segment.
        - ``x2`` -- The horizontal location relative to the sprite of
          the second end point of the line segment.
        - ``y2`` -- The vertical location relative to the sprite of the
          second end point of the line segment.
        - ``color`` -- A :class:`sge.Color` object representing the
          color of the line segment.
        - ``thickness`` -- The thickness of the line segment.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.
        """
        if not isinstance(color, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(color))
            raise TypeError(e)

        x1 = int(round(x1))
        y1 = int(round(y1))
        x2 = int(round(x2))
        y2 = int(round(y2))
        thickness = int(round(thickness))
        pg_color = pygame.Color(*color)
        thickness = abs(thickness)

        if color.alpha == 255:
            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    if anti_alias and thickness == 1:
                        pygame.draw.aaline(self.rd["baseimages"][i], pg_color,
                                           (x1, y1), (x2, y2))
                    else:
                        pygame.draw.line(self.rd["baseimages"][i], pg_color,
                                         (x1, y1), (x2, y2), thickness)
        else:
            stamp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            stamp.fill(pygame.Color(0, 0, 0, 0))
            if anti_alias and thickness == 1:
                pygame.draw.aaline(stamp, pg_color, (x1, y1), (x2, y2))
            else:
                pygame.draw.line(stamp, pg_color, (x1, y1), (x2, y2),
                                 thickness)

            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    self.rd["baseimages"][i].blit(stamp, (0, 0))

        s_refresh(self)

    def draw_rectangle(self, x, y, width, height, fill=None, outline=None,
                       outline_thickness=1, frame=None):
        """
        Draw a rectangle on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          draw the rectangle.
        - ``y`` -- The vertical location relative to the sprite to draw
          the rectangle.
        - ``width`` -- The width of the rectangle.
        - ``height`` -- The height of the rectangle.
        - ``fill`` -- A :class:`sge.Color` object representing the color
          of the fill of the rectangle.
        - ``outline`` -- A :class:`sge.Color` object representing the
          color of the outline of the rectangle.
        - ``outline_thickness`` -- The thickness of the outline of the
          rectangle.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.
        """
        if fill is not None and not isinstance(fill, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(outline))
            raise TypeError(e)

        x = int(round(x))
        y = int(round(y))
        width = int(round(width))
        height = int(round(height))
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        rect = pygame.Rect(x, y, width, height)
        if fill is not None:
            pg_fill = pygame.Color(*fill)
        if outline is not None:
            pg_outl = pygame.Color(*outline)

        if ((fill is None or fill.alpha == 255) and
                (outline is None or outline.alpha == 255)):
            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    if fill is not None:
                        self.rd["baseimages"][i].fill(pg_fill, rect)

                    if outline is not None:
                        pygame.draw.rect(self.rd["baseimages"][i], pg_outl,
                                         rect, outline_thickness)
        else:
            stamp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            stamp.fill(pygame.Color(0, 0, 0, 0))
            if fill is not None:
                stamp.fill(pg_fill, rect)
            if outline is not None:
                pygame.draw.rect(stamp, pg_outl, rect, outline_thickness)

            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    self.rd["baseimages"][i].blit(stamp, (0, 0))

        s_refresh(self)

    def draw_ellipse(self, x, y, width, height, fill=None, outline=None,
                     outline_thickness=1, anti_alias=False, frame=None):
        """
        Draw an ellipse on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          position the imaginary rectangle containing the ellipse.
        - ``y`` -- The vertical location relative to the sprite to
          position the imaginary rectangle containing the ellipse.
        - ``width`` -- The width of the ellipse.
        - ``height`` -- The height of the ellipse.
        - ``fill`` -- A :class:`sge.Color` object representing the color
          of the fill of the ellipse.
        - ``outline`` -- A :class:`sge.Color` object representing the
          color of the outline of the ellipse.
        - ``outline_thickness`` -- The thickness of the outline of the
          ellipse.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.
        """
        if fill is not None and not isinstance(fill, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(outline))
            raise TypeError(e)

        x = int(round(x))
        y = int(round(y))
        width = int(round(width))
        height = int(round(height))
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        rect = pygame.Rect(x, y, width, height)
        if fill is not None:
            pg_fill = pygame.Color(*fill)
        if outline is not None:
            pg_outl = pygame.Color(*outline)

        if ((fill is None or fill.alpha == 255) and
                (outline is None or outline.alpha == 255)):
            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    if fill is not None:
                        pygame.draw.ellipse(self.rd["baseimages"][i], pg_fill,
                                            rect)

                    if outline is not None:
                        pygame.draw.ellipse(self.rd["baseimages"][i], pg_outl,
                                            rect, outline_thickness)
        else:
            stamp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            stamp.fill(pygame.Color(0, 0, 0, 0))
            if fill is not None:
                pygame.draw.ellipse(stamp, pg_fill, rect)
            if outline is not None:
                pygame.draw.ellipse(stamp, pg_outl, rect, outline_thickness)

            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    self.rd["baseimages"][i].blit(stamp, (0, 0))

        s_refresh(self)

    def draw_circle(self, x, y, radius, fill=None, outline=None,
                    outline_thickness=1, anti_alias=False, frame=None):
        """
        Draw a circle on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          position the center of the circle.
        - ``y`` -- The vertical location relative to the sprite to
          position the center of the circle.
        - ``radius`` -- The radius of the circle.
        - ``fill`` -- A :class:`sge.Color` object representing the color
          of the fill of the circle.
        - ``outline`` -- A :class:`sge.Color` object representing the
          color of the outline of the circle.
        - ``outline_thickness`` -- The thickness of the outline of the
          circle.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.
        """
        if fill is not None and not isinstance(fill, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(outline))
            raise TypeError(e)

        x = int(round(x))
        y = int(round(y))
        radius = int(round(radius))
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        if fill is not None:
            pg_fill = pygame.Color(*fill)
        if outline is not None:
            pg_outl = pygame.Color(*outline)

        if ((fill is None or fill.alpha == 255) and
                (outline is None or outline.alpha == 255)):
            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    if fill is not None:
                        pygame.draw.circle(self.rd["baseimages"][i], pg_fill,
                                           (x, y), radius)

                    if outline is not None:
                        pygame.draw.circle(self.rd["baseimages"][i], pg_outl,
                                           (x, y), radius, outline_thickness)
        else:
            stamp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            stamp.fill(pygame.Color(0, 0, 0, 0))
            if fill is not None:
                pygame.draw.circle(stamp, pg_fill, (x, y), radius)
            if outline is not None:
                pygame.draw.circle(stamp, pg_outl, (x, y), radius,
                                   outline_thickness)

            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    self.rd["baseimages"][i].blit(stamp, (0, 0))

        s_refresh(self)

    def draw_polygon(self, points, fill=None, outline=None,
                     outline_thickness=1, anti_alias=False, frame=None):
        """
        Draw a polygon on the sprite.

        Arguments:

        - ``points`` -- A list of points relative to the sprite to
          position each of the polygon's angles.  Each point should be a
          tuple in the form ``(x, y)``, where x is the horizontal
          location and y is the vertical location.
        - ``fill`` -- A :class:`sge.Color` object representing the color
          of the fill of the polygon.
        - ``outline`` -- A :class:`sge.Color` object representing the
          color of the outline of the polygon.
        - ``outline_thickness`` -- The thickness of the outline of the
          polygon.
        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.
        """
        if fill is not None and not isinstance(fill, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(fill))
            raise TypeError(e)
        if outline is not None and not isinstance(outline, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(outline))
            raise TypeError(e)

        points = [(int(round(x)), int(round(y))) for (x, y) in points]
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        if fill is not None:
            pg_fill = pygame.Color(*fill)
        if outline is not None:
            pg_outl = pygame.Color(*outline)

        if ((fill is None or fill.alpha == 255) and
                (outline is None or outline.alpha == 255)):
            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    if fill is not None:
                        pygame.draw.polygon(self.rd["baseimages"][i], pg_fill,
                                            points, 0)

                    if outline is not None:
                        if anti_alias and outline_thickness == 1:
                            pygame.draw.aalines(self.rd["baseimages"][i],
                                                pg_outl, True, points)
                        else:
                            pygame.draw.polygon(self.rd["baseimages"][i],
                                                pg_outl, points,
                                                outline_thickness)
        else:
            stamp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            stamp.fill(pygame.Color(0, 0, 0, 0))
            if fill is not None:
                pygame.draw.polygon(stamp, pg_fill, points, 0)
            if outline is not None:
                if anti_alias and outline_thickness == 1:
                    pygame.draw.aalines(stamp, pg_outl, True, points)
                else:
                    pygame.draw.polygon(stamp, pg_outl, points,
                                        outline_thickness)

            for i in six.moves.range(self.frames):
                if frame is None or frame % self.frames == i:
                    self.rd["baseimages"][i].blit(stamp, (0, 0))

        s_refresh(self)

    def draw_sprite(self, sprite, image, x, y, frame=None, blend_mode=None):
        """
        Draw another sprite on the sprite.

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
        x = int(round(x - sprite.origin_x))
        y = int(round(y - sprite.origin_y))

        image %= sprite.frames

        pygame_flags = _get_blend_flags(blend_mode)

        for i in six.moves.range(self.frames):
            if frame is None or frame % self.frames == i:
                dsurf = self.rd["baseimages"][i]
                ssurf = s_set_transparency(sprite,
                                           sprite.rd["baseimages"][image])
                if blend_mode == sge.BLEND_RGB_SCREEN:
                    _screen_blend(dsurf, ssurf, x, y, False)
                elif blend_mode == sge.BLEND_RGBA_SCREEN:
                    _screen_blend(dsurf, ssurf, x, y, True)
                else:
                    dsurf.blit(ssurf, (x, y), None, pygame_flags)

        s_refresh(self)

    def draw_text(self, font, text, x, y, width=None, height=None,
                  color=sge.Color("black"), halign="left", valign="top",
                  anti_alias=True, frame=None):
        """
        Draw text on the sprite.

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
        - ``color`` -- A :class:`sge.Color` object representing the
          color of the text.
        - ``halign`` -- The horizontal alignment of the text and the
          horizontal location of the origin of the imaginary rectangle
          the text is drawn in.  Can be set to one of the following:

          - ``"left"`` -- Align the text to the left of the imaginary
            rectangle the text is drawn in.  Set the origin of the
            imaginary rectangle to its left edge.
          - ``"center"`` -- Align the text to the center of the
            imaginary rectangle the text is drawn in.  Set the origin of
            the imaginary rectangle to its center.
          - ``"right"`` -- Align the text to the right of the imaginary
            rectangle the text is drawn in.  Set the origin of the
            imaginary rectangle to its right edge.

        - ``valign`` -- The vertical alignment of the text and the
          vertical location of the origin of the imaginary rectangle the
          text is drawn in.  Can be set to one of the following:

          - ``"top"`` -- Align the text to the top of the imaginary
            rectangle the text is drawn in.  Set the origin of the
            imaginary rectangle to its top edge.  If the imaginary
            rectangle is not tall enough to contain all of the text, cut
            text off from the bottom.
          - ``"middle"`` -- Align the the text to the middle of the
            imaginary rectangle the text is drawn in.  Set the origin of
            the imaginary rectangle to its middle.  If the imaginary
            rectangle is not tall enough to contain all of the text, cut
            text off equally from the top and bottom.
          - ``"bottom"`` -- Align the text  to the bottom of the
            imaginary rectangle the text is drawn in.  Set the origin of
            the imaginary rectangle to its top edge.  If the imaginary
            rectangle is not tall enough to contain all of the text, cut
            text off from the top.

        - ``anti_alias`` -- Whether or not anti-aliasing should be used.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to :const:`None` to draw on all
          frames.
        """
        if not isinstance(color, sge.Color):
            e = "`{}` is not a sge.Color object.".format(repr(color))
            raise TypeError(e)

        x = int(round(x))
        y = int(round(y))

        lines = f_split_text(font, text, width)
        width = font.get_width(text, width, height)
        height = font.get_height(text, width, height)
        fake_height = font.get_height(text, width)

        text_surf = pygame.Surface((width, fake_height), pygame.SRCALPHA)
        box_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        text_rect = text_surf.get_rect()
        box_rect = box_surf.get_rect()

        for i in six.moves.range(len(lines)):
            rendered_text = font.rd["font"].render(lines[i], anti_alias,
                                                   pygame.Color(*color))
            rect = rendered_text.get_rect()
            rect.top = i * font.rd["font"].get_linesize()

            if halign.lower() == "left":
                rect.left = text_rect.left
            elif halign.lower() == "right":
                rect.right = text_rect.right
            elif halign.lower() == "center":
                rect.centerx = text_rect.centerx

            text_surf.blit(rendered_text, rect)

        if valign.lower() == "top":
            text_rect.top = box_rect.top
        elif valign.lower() == "bottom":
            text_rect.bottom = box_rect.bottom
        elif valign.lower() == "middle":
            text_rect.centery = box_rect.centery

        box_surf.blit(text_surf, text_rect)

        if halign.lower() == "left":
            box_rect.left = x
        elif halign.lower() == "right":
            box_rect.right = x
        elif halign.lower() == "center":
            box_rect.centerx = x
        else:
            box_rect.left = x

        if valign.lower() == "top":
            box_rect.top = y
        elif valign.lower() == "bottom":
            box_rect.bottom = y
        elif valign.lower() == "middle":
            box_rect.centery = y
        else:
            box_rect.top = y

        for i in six.moves.range(self.frames):
            if frame is None or frame % self.frames == i:
                self.rd["baseimages"][i].blit(box_surf, box_rect)

        s_refresh(self)

    def draw_erase(self, x, y, width, height, frame=None):
        """
        Erase part of the sprite.

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
        for i in six.moves.range(self.frames):
            if frame is None or frame % self.frames == i:
                if self.rd["baseimages"][i].get_flags() & pygame.SRCALPHA:
                    color = pygame.Color(0, 0, 0, 0)
                else:
                    color = self.rd["baseimages"][i].get_colorkey()

                rect = pygame.Rect(x, y, width, height)
                self.rd["baseimages"][i].fill(color, rect)

        s_refresh(self)

    def draw_clear(self, frame=None):
        """
        Erase everything from the sprite.

        Arguments:

        - ``frame`` -- The frame of the sprite to clear, where ``0`` is
          the first frame; set to :const:`None` to clear all frames.
        """
        self.draw_erase(0, 0, self.width, self.height, frame)

    def draw_lock(self):
        """
        Lock the sprite for continuous drawing.

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
        if not self.rd["locked"]:
            self.rd["locked"] = True

    def draw_unlock(self):
        """
        Unlock the sprite.

        Use this method to "unlock" the sprite after it has been
        "locked" for continuous drawing by :meth:`sge.Sprite.draw_lock`.
        """
        if self.rd["locked"]:
            self.rd["locked"] = False
            s_refresh(self)

    def mirror(self):
        """Mirror the sprite horizontally."""
        for i in six.moves.range(self.frames):
            img = self.rd["baseimages"][i]
            self.rd["baseimages"][i] = pygame.transform.flip(img, True, False)

        s_refresh(self)

    def flip(self):
        """Flip the sprite vertically."""
        for i in six.moves.range(self.frames):
            img = self.rd["baseimages"][i]
            self.rd["baseimages"][i] = pygame.transform.flip(img, False, True)

        s_refresh(self)

    def rotate(self, x, adaptive_resize=True):
        """
        Rotate the sprite about the center.

        Arguments:

        - ``x`` -- The rotation amount in degrees, with rotation in a
          positive direction being counter-clockwise.
        - ``adaptive_resize`` -- Whether or not the sprite should be
          resized to accomodate rotation.  If this is :const:`True`,
          rotation amounts other than multiples of 180 will result in
          the size of the sprite being adapted to fit the whole rotated
          image.  The origin will also be adjusted so that the rotation
          is about the center.

        .. note::

           This is a destructive transformation: it can result in loss
           of pixel information, especially if it is done repeatedly.
           Because of this, it is advised that you do not adjust this
           value for routine rotation.  Use the :attr:`image_rotation`
           attribute of a :class:`sge.Object` object instead.
        """
        new_w = self.width
        new_h = self.height
        for i in six.moves.range(self.frames):
            img = pygame.transform.rotate(self.rd["baseimages"][i], x)
            new_w = img.get_width()
            new_h = img.get_height()
            if adaptive_resize:
                self.rd["baseimages"][i] = img
            else:
                x = -(new_w - self.__w) / 2
                y = -(new_h - self.__h) / 2
                self.rd["baseimages"][i].fill(pygame.Color(0, 0, 0, 0))
                self.rd["baseimages"][i].blit(img, (x, y))

        if adaptive_resize:
            self.origin_x += (new_w - self.__w) / 2
            self.origin_y += (new_h - self.__h) / 2
            self.__w = new_w
            self.__h = new_h

        s_refresh(self)

    def copy(self):
        """Return a copy of the sprite."""
        new_copy = Sprite(width=self.width, height=self.height,
                          transparent=self.transparent, origin_x=self.origin_x,
                          origin_y=self.origin_y, fps=self.fps,
                          bbox_x=self.bbox_x, bbox_y=self.bbox_y,
                          bbox_width=self.bbox_width,
                          bbox_height=self.bbox_height)
        for i in range(1, self.frames):
            new_copy.append_frame()
        for i in range(self.frames):
            new_copy.draw_sprite(self, i, self.origin_x, self.origin_y, i)

        return new_copy

    def save(self, fname):
        """
        Save the sprite to an image file.

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

        for i in six.moves.range(self.frames):
            reel.blit(self.rd["baseimages"][i], (self.width * i, 0))

        try:
            pygame.image.save(reel, fname)
        except pygame.error:
            m = 'Couldn\'t save to "{}"'.format(
                os.path.normpath(os.path.realpath(fname)))
            raise IOError(m)

    @classmethod
    def from_text(cls, font, text, width=None, height=None,
                  color=sge.Color("black"), halign="left", valign="top",
                  anti_alias=True):
        """
        Create a sprite, draw the given text on it, and return the
        sprite.  See the documentation for :meth:`sge.Sprite.draw_text`
        for more information.

        The sprite's origin is set based on ``halign`` and ``valign``.
        """
        f_name = tuple(font.name) if font.name is not None else None
        i = ("text_sprite", cls, f_name, font.size, font.underline, font.bold,
             font.italic, text, width, height, str(color), halign, valign,
             anti_alias)
        s = r.cache.get(i)
        if s is None:
            w = font.get_width(text, width, height)
            h = font.get_height(text, width, height)
            x = {"left": 0, "right": w, "center": w / 2}.get(halign.lower(), 0)
            y = {"top": 0, "bottom": h, "middle": h / 2}.get(valign.lower(), 0)
            s = cls(width=w, height=h, origin_x=x, origin_y=y)
            s.draw_text(font, text, x, y, width, height, color, halign, valign)

        r.cache.add(i, s)
        return s.copy()

    @classmethod
    def from_tileset(cls, fname, x=0, y=0, columns=1, rows=1, xsep=0, ysep=0,
                     width=1, height=1, origin_x=0, origin_y=0,
                     transparent=True, fps=0, bbox_x=None, bbox_y=None,
                     bbox_width=None, bbox_height=None):
        """
        Return a sprite based on the tiles in a tileset.

        Arguments:

        - ``fname`` -- The path to the image file containing the
          tileset.
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
        self = cls(width=width, height=height, origin_x=origin_x,
                   origin_y=origin_y, transparent=transparent, fps=fps,
                   bbox_x=bbox_x, bbox_y=bbox_y, bbox_width=bbox_width,
                   bbox_height=bbox_height)

        try:
            tileset = pygame.image.load(fname)
        except pygame.error as e:
            raise IOError(e)

        for i in six.moves.range(1, rows * columns):
            self.append_frame()

        for i in six.moves.range(rows):
            for j in six.moves.range(columns):
                frame = i * columns + j
                x_ = x + (width + xsep) * j
                y_ = y + (height + ysep) * i
                self.rd["baseimages"][frame].blit(
                    s_set_transparency(self, tileset), (-x_, -y_))

        s_refresh(self)
        return self

    @classmethod
    def from_screenshot(cls, x=0, y=0, width=None, height=None):
        """
        Return the current display on the screen as a sprite.

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
        if width is None:
            width = sge.game.width - x
        if height is None:
            height = sge.game.height - y

        sprite = cls(width=width, height=height)
        sprite.rd["baseimages"][0].blit(r.game_display_surface, (-x, -y))
        s_refresh(sprite)
        return sprite

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.copy()
