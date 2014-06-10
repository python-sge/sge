# The SGE Specification
# Written in 2012, 2013, 2014 by Julian Marchant <onpon4@riseup.net> 
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

import sge


__all__ = ['show_message', 'get_text_entry']


def show_message(text, buttons=('OK',), default=0):
    """Show a dialog box and return the button pressed.

    Arguments:

    - ``text`` -- The message to show in the dialog box as a string.
    - ``buttons`` -- A list or tuple of strings to put in each of the
      buttons from left to right.
    - ``default`` -- The number of the button to select by default,
      where ``0`` is the first button.

    While the dialog box is being shown, all events are stopped.

    The return value is the number of the button which was pressed,
    where ``0`` is the first button.  If the dialog box was closed in
    any way other than clicking on one of the buttons (including by
    clicking an "X" button or similar), :const:`None` is returned.

    """
    # TODO


def get_text_entry(text, default=''):
    """Show a text entry dialog box and return the text entered.

    Arguments:

    - ``text`` -- The message to show in the dialog box as a string.
    - ``default`` -- The text to put in the text entry field initially.

    The text entry dialog box is mostly the same as the regular dialog
    box -- see the documentation for :func:`sge.show_message` for more
    information -- but there are some key differences:

    There is always an OK button and a Cancel button.  If the OK button
    is clicked, the text in the text entry field is returned.  If the
    Cancel button is clicked, :const:`None` is returned.

    """
    # TODO
