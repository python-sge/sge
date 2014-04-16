Information specific to the Pygame SGE
======================================

License
-------

The Pygame SGE is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The Pygame SGE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with the Pygame SGE.  If not, see <http://www.gnu.org/licenses/>.

Dependencies
------------

- Python 3.1 or later <http://www.python.org>
- Pygame 1.9.2 or later <http://pygame.org>

Formats Support
---------------

:class:`sge.Sprite` supports the following image formats:

- PNG
- JPEG
- Non-animated GIF
- BMP
- PCX
- Uncompressed Truevision TGA
- TIFF
- ILBM
- Netpbm
- X Pixmap

:class:`sge.Sound` supports the following audio formats:

- Uncompressed WAV
- Ogg Vorbis

:class:`sge.Music` supports the following audio formats:

- Ogg Vorbis
- MP3 (support limited; use not recommended)
- MOD
- XM
- MIDI

For starting position in MOD files, the pattern order number is used
instead of the number of milliseconds.

If Pygame is built without full image support, :class:`sge.Sprite` will
only be able to load uncompressed BMP images.

The pygame.mixer module, which is used for all audio playback, is
optional and depends on SDL_mixer; if pygame.mixer is unavailable,
sounds and music will not play.

On some systems, :class:`sge.Music` attempting to load an unsupported
format can crash the game.  Since MP3 support is limited, it is best to
avoid using it; consider using Ogg Vorbis instead.

Missing Features
----------------

:meth:`sge.Sprite.draw_line`, :meth:`sge.Room.project_line`, and
:meth:`sge.Game.project_line` support anti-aliasing for lines with a
thickness of 1 only.  :meth:`sge.Sprite.draw_text`,
:meth:`sge.Room.project_text`, and :meth:`sge.Game.project_text` support
anti-aliasing in all cases.  No other drawing or projecting methods
support anti-aliasing.

:data:`sge.BLEND_RGBA_SCREEN` and :data:`sge.BLEND_RGB_SCREEN` are
unsupported. If one of these blend modes is attempted, normal blending
will be used instead.

Speed Improvements
------------------

The Pygame SGE supports hardware rendering, which can improve
performance in some cases.  It is not enabled by default.  To enable it,
set :data:`sge.hardware_rendering` to :const:`True`.  The benefit of
hardware acceleration is usually negligible, which is why it is disabled
by default.
