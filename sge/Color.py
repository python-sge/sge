# Copyright (c) 2014 Edwin O Marshall <edwin@directemployers.org>
# Copyright (c) 2014, 2015 Julian Marchant <onpon4@riseup.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import six

COLORS = {'white': '#ffffff', 'silver': '#c0c0c0', 'gray': '#808080',
          'black': '#000000', 'red': '#ff0000', 'maroon': '#800000',
          'yellow': '#ffff00', 'olive': '#808000', 'lime': '#00ff00',
          'green': '#008000', 'aqua': '#00ffff', 'teal': '#008080',
          'blue': '#0000ff', 'navy': '#000080', 'fuchsia': '#ff00ff',
          'purple': '#800080'}
COLOR_NAMES = {}
for pair in COLORS.items():
    COLOR_NAMES[pair[1]] = pair[0]


def _check_input(value):
    if value in six.moves.range(256):
        return value
    else:
        raise ValueError("Color values must be between 0 and 255.")


class Color(object):

    """
    This class stores color information.

    Objects of this class can be converted to iterables indicating the
    object's :attr:`red`, :attr:`green`, :attr:`blue`, and :attr:`alpha`
    values, respectively; to integers which can be interpreted as a
    hexadecimal representation of the color, excluding alpha
    transparency; and to strings which indicate the English name of the
    color (in all lowercase) if possible, and :attr:`hex_string`
    otherwise.

    .. attribute:: red

       The red component of the color as an integer, where ``0``
       indicates no red intensity and ``255`` indicates full red
       intensity.

    .. attribute:: green

       The green component of the color as an integer, where ``0``
       indicates no green intensity and ``255`` indicates full green
       intensity.

    .. attribute:: blue

       The blue component of the color as an integer, where ``0``
       indicates no blue intensity and ``255`` indicates full blue
       intensity.

    .. attribute:: alpha

       The alpha transparency of the color as an integer, where ``0``
       indicates full transparency and ``255`` indicates full opacity.

    .. attribute:: hex_string

       An HTML hex string representation of the color.  (Read-only)
    """

    def __init__(self, value):
        """
        Arguments:

        - ``value`` -- The value indicating the color represented by
          this object.  Should be one of the following:

          - One of the 16 HTML color names (case-insensitive).
          - An HTML-style hex string containing 3, 4, 6, or 8 digits
            which indicate the red, green, blue, and alpha components of
            the color, respectively, as pairs of hexadecimal digits.  If
            the string contains 3 or 4 digits, each digit is duplicated;
            for example, ``"#F80"`` is equivalent to ``"#FF8800"``.
          - An integer which, when written as a hexadecimal number,
            specifies the components of the color in the same way as an
            HTML-style hex string containing 6 digits.
          - A list or tuple indicating the red, green, and blue
            components, and optionally the alpha component, in that
            order.
        """
        self.alpha = 255
        if isinstance(value, six.string_types):
            value = COLORS.get(value, value)[1:]
            if len(value) == 3:
                r, g, b = [int(value[i] * 2, 16) for i in six.moves.range(3)]
                self.red, self.green, self.blue = r, g, b
            elif len(value) == 4:
                r, g, b, a = [int(value[i] * 2, 16) for i in range(4)]
                self.red, self.green, self.blue, self.alpha = r, g, b, a
            elif len(value) == 6:
                r, g, b = [int(value[i:(i + 2)], 16)
                           for i in six.moves.range(0, 6, 2)]
                self.red, self.green, self.blue = r, g, b
            elif len(value) == 8:
                r, g, b, a = [int(value[i:(i + 2)], 16) for i in range(0, 8, 2)]
                self.red, self.green, self.blue, self.alpha = r, g, b, a
            else:
                raise ValueError("Invalid color string.")
        elif isinstance(value, six.integer_types):
            b, g, r = [(value & 256 ** (i + 1) - 1) // 256 ** i
                       for i in six.moves.range(3)]
            self.red, self.green, self.blue = r, g, b
        elif isinstance(value, (list, tuple)):
            if len(value) >= 3:
                self.red, self.green, self.blue = value[:3]
                if len(value) >= 4:
                    self.alpha = value[3]
            else:
                raise ValueError("Invalid color tuple.")
        else:
            raise ValueError("Invalid color value.")

    @property
    def red(self):
        return self._r

    @red.setter
    def red(self, value):
        self._r = _check_input(value)

    @property
    def green(self):
        return self._g

    @green.setter
    def green(self, value):
        self._g = _check_input(value)

    @property
    def blue(self):
        return self._b

    @blue.setter
    def blue(self, value):
        self._b = _check_input(value)

    @property
    def alpha(self):
        return self._a

    @alpha.setter
    def alpha(self, value):
        self._a = _check_input(value)

    @property
    def hex_string(self):
        if self.alpha == 255:
            r, g, b = [hex(c)[2:].zfill(2) for c in self[:3]]
            return "#{}{}{}".format(r, g, b)
        else:
            r, g, b, a = [hex(c)[2:].zfill(2) for c in self]
            return "#{}{}{}{}".format(r, g, b, a)

    def __iter__(self):
        return iter([self.red, self.green, self.blue, self.alpha])

    def __int__(self):
        return self.red * 256 ** 2 | self.green * 256 | self.blue

    def __repr__(self):
        return 'sge.Color("{}")'.format(str(self))

    def __str__(self):
        return COLOR_NAMES.get(self.hex_string, self.hex_string)

    def __getitem__(self, index):
        return tuple(self)[index]

    def __setitem__(self, index, value):
        c = list(self)
        c[index] = value
        self.red, self.green, self.blue, self.alpha = c
