# xSGE GUI Toolkit
# Copyright (C) 2014 Julian Marchant <onpon4@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This module provides a simple toolkit for adding GUIs to a SGE game as
well as support for modal dialog boxes.

.. data:: DATADIR

   The directory this module searches for data files in.

.. data:: windows

   A list of all windows that are currently supposed to be visible.
   Windows in this list will be displayed when :func:`xsge.gui.refresh`
   is called.

   You don't need to modify this list manually. Instead, use
   :meth:`xsge.gui.Window.show` and :meth:`xsge.gui.Window.hide` to add
   and remove windows from this list, respectively.
"""

import os

import sge


__all__ = ["Frame", "Window", "Dialog", "MessageDialog", "TextEntryDialog",
           "FileSelectionDialog", "Widget", "Button", "CheckBox", "ComboBox",
           "ProgressBar", "RadioButton", "TextBox"]

DATADIR = os.path.join(os.path.dirname(__file__), "gui_data")

windows = []
window_color = "#A4A4A4"
text_color = "black"
button_text_color = "black"
combobox_item_text_color = "black"
textbox_text_color = "black"
title_text_color = "white"
default_font = None
button_font = None
combobox_item_font = None
textbox_font = None
title_font = None
button_sprite = None
button_left_sprite = None
button_right_sprite = None
button_pressed_sprite = None
button_pressed_left_sprite = None
button_pressed_right_sprite = None
button_selected_sprite = None
button_selected_left_sprite = None
button_selected_right_sprite = None
checkbox_off_sprite = None
checkbox_on_sprite = None
combobox_closed_sprite = None
combobox_closed_left_sprite = None
combobox_closed_right_sprite = None
combobox_item_sprite = None
combobox_itemsep_sprite = None
combobox_itemsep_left_sprite = None
combobox_itemsep_right_sprite = None
combobox_open_left_sprite = None
combobox_open_right_sprite = None
combobox_open_bottom_sprite = None
combobox_open_bottomleft_sprite = None
combobox_open_bottomright_sprite = None
combobox_open_top_sprite = None
combobox_open_topleft_sprite = None
combobox_open_topright_sprite = None
progressbar_sprite = None
progressbar_left_sprite = None
progressbar_right_sprite = None
progressbar_container_sprite = None
progressbar_container_left_sprite = None
progressbar_container_right_sprite = None
radiobutton_off_sprite = None
radiobutton_on_sprite = None
textbox_sprite = None
textbox_left_sprite = None
textbox_right_sprite = None
window_border_left_sprite = None
window_border_right_sprite = None
window_border_bottom_sprite = None
window_border_bottomleft_sprite = None
window_border_bottomright_sprite = None
window_border_bottomright_resizable_sprite = None
window_border_top_sprite = None
window_border_topleft_sprite = None
window_border_topright_sprite = None


class Window:

    """Window class.

    Window objects are used to contain widgets.  They can be moved
    around the game window by the user.

    .. attribute:: x

       The horizontal position of the window relative to the game
       window.

    .. attribute:: y

       The vertical position of the window relative to the game window.

    .. attribute:: width

       The width of the window.

    .. attribute:: height

       The height of the window.

    .. attribute:: title

       The text that shows up in the title bar of the window.

    .. attribute:: widget_area_width

       The width of the area that widgets reside in.  If set to
       :cosnt:`None`, it becomes the same value as :attr:`width`.

    .. attribute:: widget_area_height

       The height of the area that widgets reside in.  If set to
       :cosnt:`None`, it becomes the same value as :attr:`height`.

    .. attribute:: resizable

       Whether or not the window can be resized by the user.

    .. attribute:: border

       Whether or not the window has a border.  If this is
       :const:`False`, the window cannot be moved or resized by the
       user, and :attr:`title` will not be displayed.

    """

    @property
    def widget_area_width(self):
        return self.v_widget_area_width

    @widget_area_width.setter
    def widget_area_width(self, value):
        if value is not None:
            self.v_widget_area_width = value
        else:
            self.v_widget_area_width = self.width

    @property
    def widget_area_height(self):
        return self.v_widget_area_height

    @widget_area_height.setter
    def widget_area_height(self, value):
        if value is not None:
            self.v_widget_area_height = value
        else:
            self.v_widget_area_height = self.height

    def __init__(self, x, y, width, height, title="", widget_area_width=None,
                 widget_area_height=None, resizable=True, border=True):
        self.sprite = sge.Sprite(width=self.width, height=self.height)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.widget_area_width = widget_area_width
        self.widget_area_height = widget_area_height
        self.resizable = resizable
        self.border = border

    def show(self):
        """Add this window to :data:`xsge.gui.windows`."""
        global windows
        if self not in windows:
            windows.append(self)

    def hide(self):
        """Remove this window from :data:`xsge.gui.windows`."""
        global windows
        if self in windows:
            windows.remove(self)

    def destroy(self):
        """Destroy this window."""
        self.hide()
        self.sprite.destroy()

    def refresh(self):
        """Project this window onto the game window.

        This method must be called every frame for the window to be
        visible.

        """
        # TODO


class Dialog(Window):

    pass


class MessageDialog(Dialog):

    pass


class TextEntryDialog(Dialog):

    pass


class FileSelectionDialog(Dialog):

    pass


class Widget(sge.StellarClass):

    pass


class Button(Widget):

    pass


class CheckBox(Widget):

    pass


class ComboBox(Widget):

    pass


class ProgressBar(Widget):

    pass


class RadioButton(Widget):

    pass


class TextBox(Widget):

    pass


def init():
    """Prepare this module for use.

    This function in particular creates the sprites and fonts it uses
    for windows and widgets.  Because of this, it must not be called
    until after a :class:`sge.Game` object has been created.

    """
    global default_font
    global button_font
    global combobox_item_font
    global textbox_font
    global title_font
    global button_sprite
    global button_left_sprite
    global button_right_sprite
    global button_pressed_sprite
    global button_pressed_left_sprite
    global button_pressed_right_sprite
    global button_selected_sprite
    global button_selected_left_sprite
    global button_selected_right_sprite
    global checkbox_off_sprite
    global checkbox_on_sprite
    global combobox_closed_sprite
    global combobox_closed_left_sprite
    global combobox_closed_right_sprite
    global combobox_item_sprite
    global combobox_itemsep_sprite
    global combobox_itemsep_left_sprite
    global combobox_itemsep_right_sprite
    global combobox_open_left_sprite
    global combobox_open_right_sprite
    global combobox_open_bottom_sprite
    global combobox_open_bottomleft_sprite
    global combobox_open_bottomright_sprite
    global combobox_open_top_sprite
    global combobox_open_topleft_sprite
    global combobox_open_topright_sprite
    global progressbar_sprite
    global progressbar_left_sprite
    global progressbar_right_sprite
    global progressbar_container_sprite
    global progressbar_container_left_sprite
    global progressbar_container_right_sprite
    global radiobutton_off_sprite
    global radiobutton_on_sprite
    global textbox_sprite
    global textbox_left_sprite
    global textbox_right_sprite
    global window_border_left_sprite
    global window_border_right_sprite
    global window_border_bottom_sprite
    global window_border_bottomleft_sprite
    global window_border_bottomright_sprite
    global window_border_bottomright_resizable_sprite
    global window_border_top_sprite
    global window_border_topleft_sprite
    global window_border_topright_sprite

    default_font = sge.Font(["DroidSans.ttf", "Droid Sans"], size=10)
    button_font = sge.Font(["DroidSans-Bold.ttf", "Droid Sans"], size=10)
    combobox_item_font = default_font
    textbox_font = default_font
    title_font = sge.Font(["DroidSans-Bold.ttf", "Droid Sans"], size=11)

    orig_image_directories = sge.image_directories
    orig_font_directories = sge.font_directories
    sge.image_directories = [DATADIR]
    sge.font_directories = [DATADIR]

    try:
        button_sprite = sge.Sprite("_gui_button")
        button_left_sprite = sge.Sprite("_gui_button_left")
        button_right_sprite = sge.Sprite("_gui_button_right")
    except IOError:
        button_sprite = sge.Sprite(width=1, height=24)
        button_sprite.draw_rectangle(0, 0, 1, 24, fill="black")
        button_sprite.draw_rectangle(0, 1, 1, 22, fill="white")
        button_left_sprite = sge.Sprite(width=8, height=24)
        button_left_sprite.draw_rectangle(0, 0, 8, 24, fill="black")
        button_right_sprite = button_left_sprite
        button_selected_sprite = sge.Sprite(width=1, height=24)
        button_selected_sprite.draw_rectangle(0, 0, 1, 24, fill="black")
        button_selected_sprite.draw_rectangle(0, 1, 1, 22, fill="aqua")
        button_selected_left_sprite = button_left_sprite
        button_selected_right_sprite = button_right_sprite
        button_pressed_sprite = button_selected_sprite
        button_pressed_left_sprite = button_selected_left_sprite
        button_pressed_right_sprite = button_selected_right_sprite
        checkbox_off_sprite = sge.Sprite(width=16, height=16)
        checkbox_off_sprite.draw_rectangle(0, 0, 16, 16, fill="white",
                                           outline="black")
        checkbox_on_sprite = sge.Sprite(width=16, height=16)
        checkbox_on_sprite.draw_sprite(checkbox_off_sprite, 0, 0, 0)
        checkbox_on_sprite.draw_line(0, 0, 15, 15, "black")
        checkbox_on_sprite.draw_line(0, 15, 15, 0, "black")
        combobox_closed_sprite = button_sprite
        combobox_closed_left_sprite = sge.Sprite(width=4, height=24)
        combobox_closed_left_sprite.draw_rectangle(0, 0, 4, 24, fill="black")
        combobox_closed_right_sprite = combobox_closed_left_sprite

    sge.image_directories = orig_image_directories
    sge.font_directories = orig_font_directories


def refresh():
    """Project all current GUI windows onto the game window.

    This function simply calls :meth:`xsge.gui.Window.refresh` on all
    objects in :data:`xsge.gui.windows`.  Call this every frame to keep
    the windows visible.

    """
    for window in windows:
        window.refresh()
