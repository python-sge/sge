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


__all__ = ['Font']


class Font(object):

    """Font handling class.

    All Font objects have the following attributes:
        size: The height of the font in pixels.
        underline: Whether or not underlined rendering is enabled.
        bold: Whether or not bold rendering is enabled.
        italic: Whether or not italic rendering is enabled.

    The following read-only attributes are also available:
        name: The name of the font given when it was created.  See
            Sound.__init__.__doc__ for more information.

    Font methods:
        get_size: Return the size of the given rendered text.

    """

    def __init__(self, name=None, size=12, underline=False, bold=False,
                 italic=False):
        """Create a new Font object.

        ``name`` indicates the name of the font.  This can be either the
        name of a font file, to be located in one of the directories
        specified in ``font_directories``, or the name of a system
        font.  If the specified font does not exist in either form, a
        default, implementation-dependent font will be used.

        ``name`` can also be a list or tuple of fonts to choose from in
        order of preference.

        Implementations are supposed, but not required, to attempt to
        use a compatible font where possible.  For example, if the font
        specified is "Times New Roman" and Times New Roman is not
        available, compatible fonts such as Liberation Serif should be
        attempted as well.

        All remaining arguments set the initial properties of the font.
        See Font.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        # TODO

    def get_size(self, text, width=None, height=None):
        """Return the size of the given rendered text.

        All arguments correspond with the same arguments in Font.render,
        and the size returned reflects rendering rules therein; see
        Font.render.__doc__ for more information.  Returned value is a
        tuple in the form (width, height).

        """
        # TODO
