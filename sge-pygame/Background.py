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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pygame

import sge


__all__ = ['Background']


class Background(object):

    """Background class.

    This class stores the layers that make up the background (which
    contain the information about what images to use and where) as well
    as the color to use where no image is shown.

    .. attribute:: color

       A :class:`sge.Color` object representing the color used in parts
       of the background where no layer is shown.

    .. attribute:: id

       The unique identifier for this background.  (Read-only)

    .. attribute:: layers

       A list containing all :class:`sge.BackgroundLayer` objects used
       in this background.  (Read-only)

    """

    def __init__(self, layers, color, ID=None):
        """Constructor method.

        Arguments:

        - ``ID`` -- The value to set :attr:`id` to.  If set to
          :const:`None`, the SGE chooses the value.

        All other arguments set the respective initial attributes of the
        background.  See the documentation for :class:`sge.Background`
        for more information.

        """
        self.color = color

        backgrounds = sge.game.backgrounds.copy()
        if ID is not None:
            self.id = ID
        else:
            ID = 0
            while ID in backgrounds:
                ID += 1
            self.id = ID

        backgrounds[self.id] = self
        sge.game.backgrounds = backgrounds

        unsorted_layers = []
        sorted_layers = []

        for layer in layers:
            if isinstance(layer, sge.BackgroundLayer):
                unsorted_layers.append(layer)
            else:
                if layer in sge.game.background_layers:
                    unsorted_layers.append(sge.game.background_layers[layer])

        for layer in unsorted_layers:
            i = 0
            while i < len(sorted_layers) and layer.z >= sorted_layers[i].z:
                i += 1

            sorted_layers.insert(i, layer)

        self.layers = sorted_layers

    def destroy(self):
        """Destroy the background."""
        backgrounds = sge.game.backgrounds.copy()
        if self.id in backgrounds:
            del backgrounds[self.id]
            sge.game.backgrounds = backgrounds

    def _get_background(self):
        # Return the static background this frame.
        background = pygame.Surface((round(sge.game.width * sge.game._xscale),
                                     round(sge.game.height * sge.game._yscale)))
        background.fill(sge._get_pygame_color(self.color))

        for view in sge.game.current_room.views:
            view_x = int(round(view.x * sge.game._xscale))
            view_y = int(round(view.y * sge.game._yscale))
            view_xport = max(0, min(int(round(view.xport * sge.game._xscale)),
                                    background.get_width() - 1))
            view_yport = max(0, min(int(round(view.yport * sge.game._yscale)),
                                    background.get_height() - 1))
            left_cutoff = abs(int(round(min(0, view.xport) *
                                        sge.game._xscale)))
            top_cutoff = abs(int(round(min(0, view.yport) * sge.game._yscale)))
            view_w = max(1, (min(view.width * sge.game._xscale,
                                background.get_width() - view_xport) -
                             left_cutoff))
            view_h = max(1, (min(view.height * sge.game._yscale,
                                 background.get_height() - view_yport) -
                             top_cutoff))
            surf = background.subsurface(view_xport, view_yport, view_w,
                                         view_h)
            for layer in self.layers:
                image = layer._get_image()
                x = int(round(
                    (sge.game.current_room.background_x + layer.x -
                     (view.x * layer.xscroll_rate)) *
                    sge.game._xscale)) - left_cutoff
                y = int(round(
                    (sge.game.current_room.background_y + layer.y -
                     (view.y * layer.yscroll_rate)) *
                    sge.game._yscale)) - top_cutoff
                image_w = max(1, image.get_width())
                image_h = max(1, image.get_height())

                # These equations bring the position to the largest
                # values possible while still being less than the
                # location we're getting the surface at.  This is to
                # minimize the number of repeat blittings.
                if layer.xrepeat:
                    x = (x % image_w) - image_w
                if layer.yrepeat:
                    y = (y % image_h) - image_h

                # Apply the origin so the positions are as expected.
                x -= int(round(layer.sprite.origin_x * sge.game._xscale))
                y -= int(round(layer.sprite.origin_y * sge.game._yscale))

                if layer.xrepeat and layer.yrepeat:
                    xstart = x
                    while y < surf.get_height():
                        x = xstart
                        while x < surf.get_width():
                            surf.blit(image, (x, y))
                            x += image_w
                        y += image_h
                elif (layer.xrepeat and y < view_y + view_h and
                      y + image_h > view_y):
                    while x < surf.get_width():
                        surf.blit(image, (x, y))
                        x += image_w
                elif (layer.yrepeat and x < view_x + view_w and
                      x + image_w > view_x):
                    while y < surf.get_height():
                        surf.blit(image, (x, y))
                        y += image_h
                elif (x < surf.get_width() and x + image_w > 0 and
                      y < surf.get_height() and y + image_h > 0):
                    surf.blit(image, (x, y))

        return background
