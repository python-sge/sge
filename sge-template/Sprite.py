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

import sge


__all__ = ['Sprite']


class Sprite(object):

    """Class which holds information for images and animations.

    All Sprite objects have the following attributes:
        width: The width of the sprite in pixels.
        height: The height of the sprite in pixels.
        origin_x: The horizontal location of the origin (the pixel
            position in relation to the images to base rendering on),
            where the left edge of the image is 0 and origin_x increases
            toward the right.
        origin_y: The vertical location of the origin (the pixel
            position in relation to the images to base rendering on),
            where the top edge of the image is 0 and origin_y increases
            toward the bottom.
        transparent: True if the image should support transparency,
            False otherwise.  If the image does not have an alpha
            channel or if the implementation used does not support alpha
            transparency, a colorkey will be used, with the transparent
            color being the color of the top-rightmost pixel.
        fps: The suggested rate in frames per second to animate the
            image at.
        bbox_x: The horizontal location of the top-left corner of the
            suggested bounding box to use with this sprite, where
            origin_x is 0 and bbox_x increases toward the right.  If
            set to None, it will become equal to -origin_x (which is
            always the left edge of the image).
        bbox_y: The vertical location of the top-left corner of the
            suggested bounding box to use with this sprite, where
            origin_y is 0 and bbox_y increases toward the bottom.  If
            set to None, it will become equal to -origin_y (which is
            always the top edge of the image).
        bbox_width: The width of the suggested bounding box in pixels.
        bbox_height: The height of the suggested bounding box in pixels.

    The following read-only attributes are also available:
        name: The name of the sprite given when it was created.  See
            Sprite.__init__.__doc__ for more information.

    Sprite methods:
        draw_dot: Draw a single-pixel dot.
        draw_line: Draw a line segment between the given points.
        draw_rectangle: Draw a rectangle at the given position.
        draw_ellipse: Draw an ellipse at the given position.
        draw_circle: Draw a circle at the given position.
        draw_sprite: Draw the given sprite at the given position.
        draw_text: Draw the given text at the given position.
        draw_clear: Erase everything from the sprite.

    """

    def __init__(self, name=None, width=None, height=None, origin_x=0,
                 origin_y=0, transparent=True, fps=60, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None):
        """Create a new Sprite object.

        ``name`` indicates the base name of the image files.  Files are
        to be located in one of the directories specified in
        ``image_directories``.  If a file with the exact name plus image
        file extensions is not available, numbered images will be
        searched for which have names with one of the following formats,
        where "name" is replaced with the specified base file name and
        "0" can be replaced with any integer:

            name-0
            name_0

        If images are found with names like those, all such images will
        be loaded and become frames of animation.  If not, sprite sheets
        will be searched for which have names with one of the following
        formats, where "name" is replaced with the specified base file
        name and "2" can be replaced with any integer:

            name-strip2
            name_strip2

        The number indicates the number of animation frames in the
        sprite sheet. The sprite sheet will be read like a horizontal
        reel, with the first frame on the far left and the last frame on
        the far right, and no space in between frames.

        ``name`` can also be None, in which case the sprite will be a
        transparent rectangle at the specified size (with both ``width``
        and ``height`` defaulting to 32 if they are set to None).  The
        implementation decides what to assign to the sprite's ``name``
        attribute, but it is always a string.

        If no image is found based on any of the above methods and
        ``name`` is not None, IOError will be raised.

        If ``width`` or ``height`` is set to None, the respective size
        will be taken from the largest animation frame.  If
        ``bbox_width`` or ``bbox_height`` is set to None, the respective
        size will be the respective size of the sprite.

        All remaining arguments set the initial properties of the
        sprite; see Sprite.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def draw_dot(self, x, y, color, frame=None):
        """Draw a single-pixel dot.

        ``x`` and ``y`` indicate the location in the sprite to draw the
        dot, where x=0, y=0 is the origin and x and y increase toward
        the right and bottom, respectively.  ``color`` indicates the
        color of the dot.  ``frame`` indicates the frame of the sprite
        to draw on, where 0 is the first frame; set to None to draw on
        all frames.

        """
        # TODO

    def draw_line(self, x1, y1, x2, y2, color, thickness=1, anti_alias=False,
                  frame=None):
        """Draw a line segment between the given points.

        ``x1``, ``y1``, ``x2``, and ``y2`` indicate the location in the
        sprite of the points between which to draw the line segment,
        where x=0, y=0 is the origin and x and y increase toward the
        right and bottom, respectively.  ``color`` indicates the color
        of the line segment.  ``thickness`` indicates the thickness of
        the line segment in pixels.  ``anti_alias`` indicates whether or
        not anti-aliasing should be used.  ``frame`` indicates the frame
        of the sprite to draw on, where 0 is the first frame; set to
        None to draw on all frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def draw_rectangle(self, x, y, width, height, fill=None, outline=None,
                       outline_thickness=1, frame=None):
        """Draw a rectangle at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the top-left corner of the rectangle, where x=0, y=0 is the
        origin and x and y increase toward the right and bottom,
        respectively.  ``width`` and ``height`` indicate the size of the
        rectangle.  ``fill`` indicates the color of the fill of the
        rectangle; set to None for no fill.  ``outline`` indicates the
        color of the outline of the rectangle; set to None for no
        outline.  ``outline_thickness`` indicates the thickness of the
        outline in pixels (ignored if there is no outline).  ``frame``
        indicates the frame of the sprite to draw on, where 0 is the
        first frame; set to None to draw on all frames.

        """
        # TODO

    def draw_ellipse(self, x, y, width, height, fill=None, outline=None,
                     outline_thickness=1, anti_alias=False, frame=None):
        """Draw an ellipse at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the top-left corner of the imaginary rectangle containing the
        ellipse, where x=0, y=0 is the origin and x and y increase
        toward the right and bottom, respectively.  ``width`` and
        ``height`` indicate the size of the ellipse.  ``fill`` indicates
        the color of the fill of the ellipse; set to None for no fill.
        ``outline`` indicates the color of the outline of the ellipse;
        set to None for no outline.  ``outline_thickness`` indicates the
        thickness of the outline in pixels (ignored if there is no
        outline).  ``anti_alias`` indicates whether or not anti-aliasing
        should be used on the outline.  ``frame`` indicates the frame of
        the sprite to draw on, where 0 is the first frame; set to None
        to draw on all frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def draw_circle(self, x, y, radius, fill=None, outline=None,
                    outline_thickness=1, anti_alias=False, frame=None):
        """Draw a circle at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the center of the circle, where x=0, y=0 is the origin and x and
        y increase toward the right and bottom, respectively.
        ``radius`` indicates the radius of the circle in pixels.
        ``fill`` indicates the color of the fill of the circle; set to
        None for no fill.  ``outline`` indicates the color of the
        outline of the circle; set to None for no outline.
        ``outline_thickness`` indicates the thickness of the outline in
        pixels (ignored if there is no outline).  ``anti_alias``
        indicates whether or not anti-aliasing should be used on the
        outline.  ``frame`` indicates the frame of the sprite to draw
        on, where 0 is the first frame; set to None to draw on all
        frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        # TODO

    def draw_sprite(self, sprite, image, x, y, frame=None):
        """Draw the given sprite at the given position.

        ``sprite`` indicates the sprite to draw.  ``image`` indicates
        the frame of ``sprite`` to draw, where 0 is the first frame.
        ``x`` and ``y`` indicate the location in the sprite being drawn
        on to position ``sprite``.  ``frame`` indicates the frame of the
        sprite to draw on, where 0 is the first frame; set to None to
        draw on all frames.

        """
        # TODO

    def draw_text(self, font, text, x, y, width=None, height=None,
                  color="black", halign=sge.ALIGN_LEFT, valign=sge.ALIGN_TOP,
                  anti_alias=True, frame=None):
        """Draw the given text at the given position.

        ``font`` indicates the font to use to draw the text.  ``text``
        indicates the text to draw.  ``x`` and ``y`` indicate the
        location in the sprite to position the text, where x=0, y=0 is
        the origin and x and y increase toward the right and bottom,
        respectively.  ``width`` and ``height`` indicate the size of the
        imaginary box the text is drawn in; set to None for no imaginary
        box.  ``color`` indicates the color of the text.  ``halign``
        indicates the horizontal alignment of the text and can be
        ALIGN_LEFT, ALIGN_CENTER, or ALIGN_RIGHT.  ``valign`` indicates
        the vertical alignment and can be ALIGN_TOP, ALIGN_MIDDLE, or
        ALIGN_BOTTOM.  ``anti_alias`` indicates whether or not anti-
        aliasing should be used.  ``frame`` indicates the frame of the
        sprite to draw on, where 0 is the first frame; set to None to
        draw on all frames.

        If the text does not fit into the imaginary box specified, the
        text that doesn't fit will be cut off at the bottom if valign is
        ALIGN_TOP, the top if valign is ALIGN_BOTTOM, or equally the top
        and bottom if valign is ALIGN_MIDDLE.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is False.

        """
        # TODO

    def draw_clear(self, frame=None):
        """Erase everything from the sprite.

        ``frame`` indicates the frame of the sprite to clear, where 0 is
        the first frame; set to None to clear all frames.

        """
        # TODO

    def save(self, fname):
        """Save the sprite to an image file.

        ``fname`` indicates the file to save the sprite to.

        If the sprite has multiple frames, the image file saved will be
        a horizontal reel of each of the frames with no space in between
        them; the leftmost image is the first frame.

        If ``fname`` is not a file name that can be saved to, IOError
        will be raised.

        """
        # TODO

    @classmethod
    def from_screenshot(cls, x=0, y=0, width=None, height=None):
        """Return the current display on the screen as a sprite.

        ``x`` and ``y`` indicate the location of the rectangular area to
        take a screenshot of.  ``width`` and ``height`` indicate the
        size of the area to take a screenshot of; set to None for all of
        the screen to the right of ``x`` and below ``y``.

        """
        # TODO
