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

    """
    This class stores the layers that make up the background (which
    contain the information about what images to use and where) as well
    as the color to use where no image is shown.

    .. attribute:: layers

       A list containing all :class:`sge.BackgroundLayer` objects used
       in this background.  (Read-only)

    .. attribute:: color

       A :class:`sge.Color` object representing the color used in parts
       of the background where no layer is shown.

    .. attribute:: rd

       Reserved dictionary for internal use by the SGE.  (Read-only)
    """

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if isinstance(value, sge.Color):
            self.__color = value
        else:
            e = "`{}` is not a sge.Color object.".format(repr(value))
            raise TypeError(e)

    def __init__(self, layers, color):
        """
        Arguments set the respective initial attributes of the
        background.  See the documentation for :class:`sge.Background`
        for more information.
        """
        self.rd = {}
        self.color = color

        sorted_layers = []

        for layer in layers:
            i = 0
            while i < len(sorted_layers) and layer.z >= sorted_layers[i].z:
                i += 1

            sorted_layers.insert(i, layer)

        self.layers = sorted_layers
