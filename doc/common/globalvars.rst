Global Variables and Constants
==============================

.. data:: IMPLEMENTATION

   A string indicating the name of the SGE implementation.

.. data:: ALIGN_LEFT

   Flag indicating horizontal alignment to the left.

.. data:: ALIGN_CENTER

   Flag indicating horizontal alignment to the center.

.. data:: ALIGN_RIGHT

   Flag indicating horizontal alignment to the right.

.. data:: ALIGN_TOP

   Flag indicating vertical alignment to the top

.. data:: ALIGN_MIDDLE

   Flag indicating vertical alignment to the middle.

.. data:: ALIGN_BOTTOM

   Flag indicating vertical alignment to the bottom.

.. data:: game

   Stores the current :class:`Game` object.  If there is no
   :class:`Game` object currently, this variable is set to
   :const:`None`.

.. data:: image_directories

   A list of directories where images can be found.  Default is
   ``./data/images``, ``./data/sprites``, or ``./data/backgrounds``,
   where ``.`` is the program directory.

.. data:: font_directories

   A list of directories where font files can be found.  Default is
   ``./data/fonts``, where ``.`` is the program directory.

.. data:: sound_directories

   A list of directories where sounds can be found.  Default is
   ``./data/sounds``, where ``.`` is the program directory.

.. data:: music_directories

   A list of directories where music files can be found.  Default is
   ``./data/music``, where ``.`` is the program directory.
