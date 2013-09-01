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

import sge


__all__ = ['Sprite']


class Sprite(object):

    """Class which holds information for images and animations.

    This class stores images and information about how the SGE is to use
    those images.

    What image formats are supported depends on the implementation of
    theSGE, but image formats that are generally a good choice are PNG
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
       bounding box to use with it.  If set to ``None``, it will become
       equal to ``-origin_x`` (which is always the left edge of the
       image).

    .. attribute:: bbox_y

       The vertical location relative to the sprite of the suggested
       bounding box to use with it.  If set to ``None``, it will become
       equal to ``-origin_y`` (which is always the top edge of the
       image).

    .. attribute:: bbox_width

       The width of the suggested bounding box.

    .. attribute:: bbox_height

       The height of the suggested bounding box.

    .. attribute:: name

       The name of the sprite given when it was created.  (Read-only)

    .. attribute:: id

       The unique identifier of the sprite.  (Read-only)

    """

    def __init__(self, name=None, id_=None, width=None, height=None,
                 origin_x=0, origin_y=0, transparent=True, fps=60,
                 bbox_x=None, bbox_y=None, bbox_width=None,
                 bbox_height=None, **kwargs):
        """Create a new Sprite object.

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
          - If the base name is ``None``, the sprite will be a fully
            transparent rectangle at the specified size (with both
            ``width`` and ``height`` defaulting to 32 if they are set to
            ``None``).  The SGE decides what to assign to the sprite's
            ``name`` attribute in this case, but it will always be a
            string.

          If none of the above rules can be used, :exc:`IOError` is
          raised.

        - ``id`` -- The unique identifier of the sprite.  If set to
          ``None``, ``name`` will be used, modified by the SGE if it is
          already the unique identifier of another sprite.

        All other arguments set the respective initial attributes of the
        sprite.  See the documentation for :class:`Sprite` for more
        information.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        # TODO

    def draw_dot(self, x, y, color, frame=None):
        """Draw a single-pixel dot on the sprite.

        Arguments:

        - ``x`` -- The horizontal location relative to the sprite to
          draw the dot.
        - ``y`` -- The vertical location relative to the sprite to draw
          the dot.
        - ``color`` -- The color of the dot.
        - ``frame`` -- The frame of the sprite to draw on, where ``0``
          is the first frame; set to ``None`` to draw on all frames.

        """
        # TODO

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
          is the first frame; set to ``None`` to draw on all frames.

        """
        # TODO

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
          is the first frame; set to ``None`` to draw on all frames.

        """
        # TODO

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
          is the first frame; set to ``None`` to draw on all frames.

        """
        # TODO

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
          is the first frame; set to ``None`` to draw on all frames.

        """
        # TODO

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
          is the first frame; set to ``None`` to draw on all frames.

        """
        # TODO

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
          drawn in; set to ``None`` to make the rectangle as wide as
          needed to contain the text without additional line breaks.  If
          set to something other than ``None``, a line which does not
          fit will be automatically split into multiple lines that do
          fit.
        - ``height`` -- The height of the imaginary rectangle the text
          is drawn in; set to ``None`` to make the rectangle as tall as
          needed to contain the text.
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
          is the first frame; set to ``None`` to draw on all frames.

        """
        # TODO

    def draw_clear(self, frame=None):
        """Erase everything from the sprite.

        Arguments:

        - ``frame`` -- The frame of the sprite to clear, where ``0`` is
          the first frame; set to ``None`` to clear all frames.

        """
        # TODO

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
        # TODO

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
          set to None for all of the area below ``y`` to be included.

        If you only wish to save a screenshot (of the entire screen) to
        a file, the easiest way to do that is::

            sge.Sprite.from_screenshot().save("foo.png")

        """
        # TODO
