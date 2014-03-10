SGE Concepts
============

Naming Conventions
------------------

There are many cases where you will want to derive a class from a SGE
class.  Since there can be multiple implementations of the SGE, it can
be easy when doing so to overwrite a special variable used by some
implementations internally, which can be disastrous.  To avoid such
occasions, implementations are expected to never introduce any attribute
names which are not explicitly mentioned in the documentation for a
class unless the new attribute names are preceded by an underscore, as
in the hypothetical attribute name ``_foo``.  This naming convention
will protect users of the SGE from unexpected errors provided that they
do not use such names themselves.

A suggested convention for users of the SGE to use for "private"
attributes in place of the usual leading underscore  is to precede these
attributes with ``v_`` or ``p_``.

Events
------

The SGE uses an event-based system.  When an event occurs, a certain
event method (with a name that begins with ``event_``) is called. To
define actions triggered by events, simply override the appropriate
event method.

The Mouse
---------

functions or variables report the mouse position relative to the screen,
the mouse position within the room, calculated based on its position on
the screen by the SGE, is recorded in a special
:class:`sge.StellarClass` object which represents the mouse.  This mouse
object can be found as :attr:`sge.game.mouse`, and it has the special
object ID, ``"mouse"``.

The mouse object differs from most :class:`sge.StellarClass` objects in
a few ways.  Its speed variables cannot be manually set, and they always
report numbers which correspond to the average motion of the mouse
during the last quarter of a second.  Setting
:attr:`sge.game.mouse.visible` toggles whether or not the mouse cursor
itself is visible, and setting :attr:`sge.game.mouse.sprite` sets the
mouse cursor to the sprite assigned.

In all other ways, the mouse object is exactly the same as all other
:class:`sge.StellarClass` objects.

Colors
------

The SGE accepts a few different formats for defining colors.

The sixteen basic HTML colors, provided as strings, are accepted.  These
are case-insensitive, so ``"red"`` is interpreted the same as ``"Red"``
or ``"rEd"``.  The colors are:

- ``"white"``
- ``"silver"``
- ``"gray``
- ``"black"``
- ``"red"``
- ``"maroon"``
- ``"yellow"``
- ``"olive"``
- ``"lime"``
- ``"green"``
- ``"aqua"``
- ``"teal"``
- ``"blue"``
- ``"navy"``
- ``"fuchsia"``
- ``"purple"``

Tuples containing three or four integers are accepted.  Each index
represents a component of a color: first red, then green, then blue,
with the values being integers from ``0`` to ``255``.  For example,
``(255, 128, 0)`` indicates a color with full red intensity, 50% green
intensity, and no blue intensity, which is a shade of orange.  Note that
the components are colors of light, not colors of pigment.

The fourth value of the tuple, if specified, indicates the alpha
transparency of the color, with the possible values again being integers
from ``0`` to ``255``.  ``255`` is fully opaque, ``0`` is fully
transparent, and any value in between indicates the amount of opacity;
for example, 128 is 50% transparent.  If the fourth value is
unspecified, it is assumed that the color is fully opaque.

RGBA tuples are the only way to specify alpha transparency of colors in
SGE.  All other methods for indicating color assume full opacity.

HTML hex strings and integers are accepted.  HTML hex strings are in the
format ``"#RRGGBB"``, where ``RR``, ``GG``, and ``BB`` are replaced with
the red, green, and blue components of the color, respectively, in
hexadecimal form.  ``FF`` (equivalent to 255 in decimal form) is full
intensity of the respective color, and ``00`` (equivalent to 0 in
decimal form) is no intensity of the respective color.  For example,
``"#FF8000"`` is the same as ``(255, 128, 0)``, or orange.

Integers, treated as hexadecimals, are accepted in the same form as HTML
hex strings, but integral.  For example, ``0xFF8000`` is the same as
``"#FF8000"``.

Position
--------

In all cases of positioning for the SGE, it is based on a
two-dimensional graph with each unit being a pixel.  This graph is not
quite like regular graphs.  The horizontal direction, normally called
``x``, is the same as the x-axis on a regular graph; ``0`` is the
origin, positive numbers are to the right of the origin, and negative
numbers are to the left of the origin.  However, in the vertical
direction, normally called ``y``, ``0`` is the origin, positive numbers
are below the origin, and negative numbers are above the origin.  While
slightly jarring if you are used to normal graphs, this is in fact
common in 2-D game development and is so how pixels in most image
formats are indexed.

Except where otherwise specified, the origin is always located at the
top-leftmost position of an object.

In addition to integers, position variables are allowed by the SGE to be
floating-point numbers.

Z-Axis
------

The SGE uses a Z-axis to determine where objects are placed in the third
dimension.  Objects with a higher Z value are considered to be closer to
the viewer and thus will be placed over objects which have a lower Z
value.  Note that the Z-axis does not allow 3-D gameplay or effects; it
is only used to tell the SGE what to do with objects that overlap.  For
example, if an object called ``spam`` has a Z value of ``5`` while an
object called ``eggs`` has a Z value of ``2``, ``spam`` will obscure
part or all of ``eggs`` when the two objects overlap.

If two objects with the same Z-axis value overlap, the SGE arbitrarily
chooses which one is considered to be closer to the viewer.  The SGE is
allowed to change this decision, but only while the objects in question
are not overlapping, since changing the decision while the two objects
are overlapping would cause an undesirable flicker effect.
