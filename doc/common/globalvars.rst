Global Variables and Constants
==============================

.. data:: sge.IMPLEMENTATION

   A string indicating the name of the SGE implementation.

.. data:: sge.ALIGN_LEFT

   Flag indicating horizontal alignment to the left.

.. data:: sge.ALIGN_CENTER

   Flag indicating horizontal alignment to the center.

.. data:: sge.ALIGN_RIGHT

   Flag indicating horizontal alignment to the right.

.. data:: sge.ALIGN_TOP

   Flag indicating vertical alignment to the top

.. data:: sge.ALIGN_MIDDLE

   Flag indicating vertical alignment to the middle.

.. data:: sge.ALIGN_BOTTOM

   Flag indicating vertical alignment to the bottom.

.. data:: sge.game

   Stores the current :class:`sge.Game` object.  If there is no
   :class:`sge.Game` object currently, this variable is set to
   :const:`None`.

.. data:: sge.image_directories

   A list of directories where images can be found.  Default is
   ``./data/images``, ``./data/sprites``, or ``./data/backgrounds``,
   where ``.`` is the program directory.

.. data:: sge.font_directories

   A list of directories where font files can be found.  Default is
   ``./data/fonts``, where ``.`` is the program directory.

.. data:: sge.sound_directories

   A list of directories where sounds can be found.  Default is
   ``./data/sounds``, where ``.`` is the program directory.

.. data:: sge.music_directories

   A list of directories where music files can be found.  Default is
   ``./data/music``, where ``.`` is the program directory.
