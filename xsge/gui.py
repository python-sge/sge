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
import weakref

import sge


__all__ = ["Frame", "Window", "Dialog", "MessageDialog", "TextEntryDialog",
           "FileSelectionDialog", "Widget", "Button", "CheckBox", "ComboBox",
           "ProgressBar", "RadioButton", "TextBox"]

DATADIR = os.path.join(os.path.dirname(__file__), "gui_data")

windows = []
keyboard_focused_window = None
window_background_color = "#A4A4A4"
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
window_border_top_sprite = None
window_border_topleft_sprite = None
window_border_topright_sprite = None


class Handler(sge.StellarClass):

    """GUI handler class.

    An object of this class needs to exist in any room where windows are
    to be used.  It feeds SGE events to the windows so they can react to
    user input.  It also refreshes all windows every frame.

    """

    def __init__(self):
        super().__init__(0, 0, visible=False, tangible=False)

    def event_step(self, time_passed, delta_mult):
        for window in windows[:]:
            window.refresh()

    def event_key_press(self, key, char):
        window = keyboard_focused_window
        if window is not None:
            window.event_key_press(key, char)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_key_press(key, char)

        for window in windows:
            window.event_global_key_press(key, char)
            for widget in window.widgets:
                widget.event_global_key_press(key, char)

    def event_key_release(self, key):
        window = keyboard_focused_window
        if window is not None:
            window.event_key_release(key)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_key_release(key)

        for window in windows:
            window.event_global_key_release(key)
            for widget in window.widgets:
                widget.event_global_key_release(key)

    def event_mouse_button_press(self, button):
        global keyboard_focused_window
        window = get_mouse_focused_window()
        if window is not None:
            keyboard_focused_window = window
            window.move_to_front()
            if window.get_mouse_on_titlebar():
                window.event_titlebar_mouse_button_press(button)
            else:
                window.event_mouse_button_press(button)
                widget = window.get_mouse_focused_widget()
                if widget is not None:
                    widget.event_mouse_button_press(button)

        for window in windows:
            window.event_global_mouse_button_press(button)
            for widget in window.widgets:
                widget.event_global_mouse_button_press(button)

    def event_mouse_button_release(self, button):
        window = get_mouse_focused_window()
        if window is not None:
            if window.get_mouse_on_titlebar():
                window.event_titlebar_mouse_button_release(button)
            else:
                window.event_mouse_button_release(button)
                widget = window.get_mouse_focused_widget()
                if widget is not None:
                    widget.event_mouse_button_release(button)

        for window in windows:
            window.event_global_mouse_button_release(button)
            for widget in window.widgets:
                widget.event_global_mouse_button_release(button)


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

    .. attribute:: background_color

       The color of this window's background.  If set to :const:`None`,
       it becomes the same value as
       :data:`xsge.gui.window_background_color`.

    .. attribute:: border

       Whether or not the window has a border.  If this is
       :const:`False`, the window cannot be moved or resized by the
       user, and :attr:`title` will not be displayed.

    .. attribute:: widgets

       A list of this window's widgets.

    .. attribute:: keyboard_focused_widget

       The widget which currently has keyboard focus within this window,
       or :const:`None` if no widget has keyboard focus within this
       window.

    .. attribute:: sprite

       The sprite this window currently displays as itself.

    """

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        if value is not None:
            self._background_color = value
        else:
            self._background_color = window_background_color

    def __init__(self, x, y, width, height, title="", background_color=None,
                 border=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.background_color = background_color
        self.border = border
        self.widgets = []
        self.keyboard_focused_widget = None
        self._border_grab = None
        self._close_button_pressed = False

        self.sprite = sge.Sprite(width=1, height=1)
        self.redraw()

    def show(self):
        """Add this window to :data:`xsge.gui.windows`."""
        global windows
        if self not in windows:
            windows.append(self)
        else:
            self.move_to_front()

    def hide(self):
        """Remove this window from :data:`xsge.gui.windows`."""
        global windows
        if self in windows:
            windows.remove(self)

    def move_to_front(self):
        """Move this window in front of all other windows."""
        global windows
        if self in windows:
            windows.append(windows.pop(windows.index(self)))

    def move_to_back(self):
        """Move this window behind all other windows."""
        global windows
        if self in windows:
            windows.insert(0, windows.pop(windows.index(self)))

    def destroy(self):
        """Destroy this window."""
        self.hide()
        self.sprite.destroy()

    def redraw(self):
        """Re-draw this window's sprite.

        Call this method if you change any variables that should affect
        this window's appearance. For performance reasons, the changes
        won't show up in an existing window until this method is called.

        """
        if self.border:
            self.sprite.width = (self.width + window_border_left_sprite.width +
                                 window_border_right_sprite.width)
            self.sprite.height = (self.height +
                                  window_border_top_sprite.height +
                                  window_border_bottom_sprite.height)
            self.sprite.draw_lock()
            self.sprite.draw_clear()

            self.sprite.draw_rectangle(window_border_left_sprite.width,
                                       window_border_top_sprite.height,
                                       self.width, self.height,
                                       fill=self.background_color)

            start = window_border_topleft_sprite.width
            end = self.sprite.width - window_border_topright_sprite.width
            for i in range(start, end, window_border_top_sprite.width):
                self.sprite.draw_sprite(window_border_top_sprite, 0, i, 0)

            start = window_border_bottomleft_sprite.width
            end = self.sprite.width - window_border_bottomright_sprite.width
            y = self.sprite.height - window_border_bottom_sprite.height
            for i in range(start, end, window_border_bottom_sprite.width):
                self.sprite.draw_sprite(window_border_bottom_sprite, 0, i, y)

            start = window_border_topleft_sprite.height
            end = self.sprite.height - window_border_bottomleft_sprite.height
            for i in range(start, end, window_border_left_sprite.height):
                self.sprite.draw_sprite(window_border_left_sprite, 0, 0, i)

            start = window_border_topright_sprite.height
            end = self.sprite.height - window_border_bottomright_sprite.height
            x = self.sprite.width - window_border_right_sprite.width
            for i in range(start, end, window_border_right_sprite.height):
                self.sprite.draw_sprite(window_border_right_sprite, 0, x, i)

            self.sprite.draw_sprite(window_border_topleft_sprite, 0, 0, 0)
            x = self.sprite.width - window_border_topright_sprite.width
            self.sprite.draw_sprite(window_border_topright_sprite, 0, x, 0)
            y = self.sprite.height - window_border_bottomleft_sprite.height
            self.sprite.draw_sprite(window_border_bottomleft_sprite, 0, 0, y)
            x = self.sprite.width - window_border_bottomright_sprite.width
            y = self.sprite.height - window_border_bottomright_sprite.height
            self.sprite.draw_sprite(window_border_bottomright_sprite, 0, x, y)

            x = self.sprite.width / 2
            y = window_border_top_sprite.height / 2
            self.sprite.draw_text(title_font, self.title, x, y,
                                  width=self.sprite.width,
                                  height=window_border_top_sprite.height,
                                  color=title_text_color,
                                  halign=sge.ALIGN_CENTER,
                                  valign=sge.ALIGN_MIDDLE)

            self.sprite.draw_unlock()
        else:
            self.sprite.width = self.width
            self.sprite.height = self.height
            self.sprite.draw_clear()
            self.sprite.draw_rectangle(0, 0, self.width, self.height,
                                       fill=self.background_color)

    def refresh(self):
        """Project this window onto the game window.

        This method must be called every frame for the window to be
        visible.

        """
        if self.border:
            target_width = (self.width + window_border_left_sprite.width +
                            window_border_right_sprite.width)
            target_height = (self.height + window_border_top_sprite.height +
                             window_border_bottom_sprite.height)
        else:
            target_width = self.width
            target_height = self.height

        if self._border_grab is not None:
            self.x = sge.mouse.get_x() + self._border_grab[0]
            self.y = sge.mouse.get_y() + self._border_grab[1]

        if (self.sprite.width != target_width or
                self.sprite.height != target_height):
            self.redraw()

        x = self.x - window_border_left_sprite.width
        y = self.y - window_border_top_sprite.height

        if x < 0:
            x = 0
        elif x + self.sprite.width >= sge.game.width:
            x = sge.game.width - self.sprite.width
        if y < 0:
            y = 0
        elif y + self.sprite.height >= sge.game.height:
            y = sge.game.height - self.sprite.height

        self.x = x + window_border_left_sprite.width
        self.y = y + window_border_top_sprite.height

        sge.game.project_sprite(self.sprite, 0, x, y)

        for widget in self.widgets:
            widget.refresh()

    def get_mouse_on_titlebar(self):
        if self.border:
            mouse_x = sge.mouse.get_x()
            mouse_y = sge.mouse.get_y()
            border_x = self.x - window_border_left_sprite.width
            border_y = self.y - window_border_top_sprite.height
            return (border_x <= mouse_x < border_x + self.sprite.width and
                    border_y <= mouse_y < self.y)
        else:
            return False

    def get_mouse_focused_widget(self):
        """Return the widget in this window with mouse focus.

        The widget with mouse focus is the one which is closest to the
        front that is touching the mouse cursor.

        Return :const:`None` if no window has focus.

        """
        x = sge.mouse.get_x()
        y = sge.mouse.get_y()
        for widget in self.widgets[::-1]:
            widget_x = self.x + widget.x
            widget_y = self.y + widget.y
            if (widget_x <= x < widget_x + widget.sprite.width and
                    widget_y <= y < widget_y + widget.sprite.height):
                return widget

        return None

    def event_key_press(self, key, char):
        """Key press event.

        Called when a key is pressed while this window has keyboard
        focus.  See the documentation for :class:`sge.input.KeyPress`
        for more information.

        """
        if key == "tab":
            if self.widgets:
                try:
                    i = self.widgets.index(self.keyboard_focused_widget)
                except ValueError:
                    self.keyboard_focused_widget = self.widgets[0]
                else:
                    i = (i + 1) % len(self.widgets)
                    self.keyboard_focused_widget = self.widgets[i]

    def event_key_release(self, key):
        """Key release event.

        Called when a key is released while this window has keyboard
        focus.  See the documentation for :class:`sge.input.KeyRelease`
        for more information.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        Called when a mouse button is pressed while this window has
        mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        Called when a mouse button is released while this window has
        mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.

        """
        pass

    def event_titlebar_mouse_button_press(self, button):
        """Mouse button press event.

        Called when a mouse button is pressed on top of this window's
        title bar (top border).  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.

        """
        x = sge.mouse.get_x()
        y = sge.mouse.get_y()
        border_x = self.x - window_border_left_sprite.width
        close_button_w = window_border_topright_sprite.width
        close_button_x = (border_x + self.sprite.width - close_button_w)
        if close_button_x <= x < close_button_x + close_button_w:
            if button == "left":
                self._close_button_pressed = True
        else:
            if button == "left":
                self._border_grab = (self.x - x, self.y - y)
            elif button == "middle":
                self.move_to_back()

    def event_titlebar_mouse_button_release(self, button):
        """Mouse button release event.

        Called when a mouse button is released on top of this window's
        title bar (top border).  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.

        """
        x = sge.mouse.get_x()
        y = sge.mouse.get_y()
        border_x = self.x - window_border_left_sprite.width
        close_button_w = window_border_topright_sprite.width
        close_button_x = (border_x + self.sprite.width - close_button_w)
        if close_button_x <= x < close_button_x + close_button_w:
            if button == "left":
                if self._close_button_pressed:
                    self.event_close()
        else:
            if button == "left":
                if self._border_grab is not None:
                    self.x = sge.mouse.get_x() + self._border_grab[0]
                    self.y = sge.mouse.get_y() + self._border_grab[1]

        self.event_global_mouse_button_release(button)

    def event_global_key_press(self, key, char):
        """Global key press event.

        Called when a key is pressed, regardless of which window has
        keyboard focus.  See the documentation for
        :class:`sge.input.KeyPress` for more information.

        """
        pass

    def event_global_key_release(self, key):
        """Global key release event.

        Called when a key is released, regardless of which window has
        keyboard focus.  See the documentation for
        :class:`sge.input.KeyRelease` for more information.

        """
        pass

    def event_global_mouse_button_press(self, button):
        """Global mouse button press event.

        Called when a mouse button is pressed, regardless of which
        window has mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.

        """
        pass

    def event_global_mouse_button_release(self, button):
        """Global mouse button release event.

        Called when a mouse button is released, regardless of which
        window has mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.

        """
        if button == "left":
            self._close_button_pressed = False
            self._border_grab = None

    def event_close(self):
        """Close event.

        Called when the "X" button in the top-right corner of the window
        is pressed.

        By default, this calls :meth:`xsge.gui.Window.destroy`.

        """
        self.destroy()


class Dialog(Window):

    """Dialog class.

    Dialogs are windows with their own loops, also called modal windows.
    They are used to display messages outside of regular windows.

    See the documentation for :class:`xsge.gui.Window` for more
    information.

    """

    def show(self):
        """Show this dialog and start its loop.

        Like :meth:`xsge.gui.Window.show`, this method adds the dialog
        to :data:`xsge.gui.windows`.  It then starts this dialog's loop.
        Call :meth:`xsge.gui.Dialog.hide` on this dialog to end the
        loop.

        """
        super().show()
        handler = Handler()
        while self in windows:
            # Input events
            sge.game.pump_input()
            while sge.game.input_events:
                event = sge.game.input_events.pop(0)

                if isinstance(event, sge.input.KeyPress):
                    handler.event_key_press(event.key, event.char)
                elif isinstance(event, sge.input.KeyRelease):
                    handler.event_key_release(event.key)
                elif isinstance(event, sge.input.MouseButtonPress):
                    handler.event_mouse_button_press(event.button)
                elif isinstance(event, sge.input.MouseButtonRelease):
                    handler.event_mouse_button_release(event.button)
                elif isinstance(event, sge.input.QuitRequest):
                    sge.game.input_events.insert(0, event)
                    self.hide()
                    handler.destroy()
                    return

            # Regulate speed
            time_passed = sge.game.regulate_speed()

            # Project windows
            handler.event_step(time_passed, 1)

            # Refresh
            sge.game.refresh()

        self.hide()
        handler.destroy()
        sge.game.pump_input()
        sge.game.input_events = []


class MessageDialog(Dialog):

    pass


class TextEntryDialog(Dialog):

    pass


class FileSelectionDialog(Dialog):

    pass


class Widget:

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        parent = self.parent()
        if parent is not None:
            if self in parent.widgets:
                parent.widgets.remove(self)

            i = 0
            while i < len(parent.widgets) and parent.widgets[i].z <= value:
                i += 1

            parent.widgets.insert(i, self)

    def __init__(self, parent, x, y, z, sprite=None):
        self.parent = weakref.ref(parent)
        self.x = x
        self.y = y
        self.z = z
        if sprite is not None:
            self.sprite = sprite
        else:
            self.sprite = sge.Sprite(width=1, height=1)
            self.sprite.destroy()

    def destroy(self):
        """Destroy this widget."""
        parent = self.parent()
        if parent is not None and self in parent.widgets:
            parent.widgets.remove(self)

    def redraw(self):
        """Re-draw this widget's sprite.

        Call this method if you change any variables that should affect
        this widget's appearance.  This method automatically makes any
        changes necessary to :attr:`self.sprite`.

        """
        pass

    def refresh(self):
        """Project this widget onto the game window.

        This method must be called every frame for the widget to be
        visible.

        """
        parent = self.parent()
        if parent is not None:
            sge.game.project_sprite(self.sprite, 0, parent.x + self.x,
                                    parent.y + self.y)
        else:
            self.destroy()

    def event_key_press(self, key, char):
        """Key press event.

        Called when a key is pressed while this widget has keyboard
        focus.  See the documentation for :class:`sge.input.KeyPress`
        for more information.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        Called when a key is released while this widget has keyboard
        focus.  See the documentation for :class:`sge.input.KeyRelease`
        for more information.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        Called when a mouse button is pressed while this widget has
        mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        Called when a mouse button is released while this widget has
        mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.

        """
        pass

    def event_global_key_press(self, key, char):
        """Global key press event.

        Called when a key is pressed, regardless of which widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.KeyPress` for more information.

        """
        pass

    def event_global_key_release(self, key):
        """Global key release event.

        Called when a key is released, regardless of which widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.KeyRelease` for more information.

        """
        pass

    def event_global_mouse_button_press(self, button):
        """Global mouse button press event.

        Called when a mouse button is pressed, regardless of which
        widget has mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.

        """
        pass

    def event_global_mouse_button_release(self, button):
        """Global mouse button release event.

        Called when a mouse button is released, regardless of which
        widget has mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.

        """
        pass


class Label(Widget):

    """Label widget.

    This widget simply displays some text.

    .. attribute:: text

       The text this label should display.

    .. attribute:: font

       The font this label's text should be rendered with.  If set to
       :const:`None`, the value of :data:`xsge.gui.default_font` is
       used.

    .. attribute:: width

       The width of the imaginary rectangle the text is drawn in.  See
       the documentation for :meth:`sge.Sprite.draw_text` for more
       information.

    .. attribute:: height

       The height of the imaginary rectangle the text is drawn in.  See
       the documentation for :meth:`sge.Sprite.draw_text` for more
       information.

    .. attribute:: halign

       The horizontal alignment of the text.  See the documentation for
       :meth:`sge.Sprite.draw_text` for more information.

    .. attribute:: valign

       The vertical alignment of the text.  See the documentation for
       :meth:`sge.Sprite.draw_text` for more information.

    See the documentation for :class:`xsge.gui.Widget` for more
    information.

    """

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value if value is not None else default_font

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value if value is not None else text_color

    def __init__(self, parent, x, y, z, text, font=None, width=None,
                 height=None, color=None, halign=sge.ALIGN_LEFT,
                 valign=sge.ALIGN_TOP):
        super().__init__(parent, x, y, z)
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        self.color = color
        self.halign = halign
        self.valign = valign

    def refresh(self):
        parent = self.parent()
        if parent is not None:
            sge.game.project_text(self.font, self.text, parent.x + self.x,
                                  parent.y + self.y, width=self.width,
                                  height=self.height, color=self.color,
                                  halign=self.halign, valign=self.valign)
        else:
            self.destroy()


class Button(Widget):

    def __init__(self, parent, x, y, z, text, width=None):
        super().__init__(parent, x, y, z, sge.Sprite(width=1, height=1))
        self.text = text
        self.width = width
        self._pressed = False
        self.sprite_normal = None
        self.sprite_selected = None
        self.sprite_pressed = None
        self.redraw()

    def destroy(self):
        super().destroy()
        self.sprite_normal.destroy()
        self.sprite_selected.destroy()
        self.sprite_pressed.destroy()

    def redraw(self):
        h = button_sprite.height
        if self.width is None:
            w = button_font.get_width(self.text, height=h)
        else:
            w = self.width

        sprite_w = w + button_left_sprite.width + button_right_sprite.width
        left = button_left_sprite.width
        right = sprite_w - button_right_sprite.width
        self.sprite_normal = sge.Sprite(width=sprite_w, height=h)
        self.sprite_normal.draw_lock()
        for i in range(left, right, button_sprite.width):
            self.sprite_normal.draw_sprite(button_sprite, 0, i, 0)
        self.sprite_normal.draw_sprite(button_left_sprite, 0, 0, 0)
        self.sprite_normal.draw_sprite(button_right_sprite, 0, right, 0)
        self.sprite_normal.draw_text(button_font, self.text, sprite_w / 2,
                                     h / 2, width=w, height=h,
                                     color=button_text_color,
                                     halign=sge.ALIGN_CENTER,
                                     valign=sge.ALIGN_MIDDLE)
        self.sprite_normal.draw_unlock()

        sprite_w = (w + button_selected_left_sprite.width +
                    button_selected_right_sprite.width)
        left = button_selected_left_sprite.width
        right = sprite_w - button_selected_right_sprite.width
        self.sprite_selected = sge.Sprite(width=sprite_w, height=h)
        self.sprite_selected.draw_lock()
        for i in range(left, right, button_selected_sprite.width):
            self.sprite_selected.draw_sprite(button_selected_sprite, 0, i, 0)
        self.sprite_selected.draw_sprite(button_selected_left_sprite, 0, 0, 0)
        self.sprite_selected.draw_sprite(button_selected_right_sprite, 0,
                                         right, 0)
        self.sprite_selected.draw_text(button_font, self.text, sprite_w / 2,
                                       h / 2, width=w, height=h,
                                       color=button_text_color,
                                       halign=sge.ALIGN_CENTER,
                                       valign=sge.ALIGN_MIDDLE)
        self.sprite_selected.draw_unlock()

        sprite_w = (w + button_pressed_left_sprite.width +
                    button_pressed_right_sprite.width)
        left = button_pressed_left_sprite.width
        right = sprite_w - button_pressed_right_sprite.width
        self.sprite_pressed = sge.Sprite(width=sprite_w, height=h)
        self.sprite_pressed.draw_lock()
        for i in range(left, right, button_pressed_sprite.width):
            self.sprite_pressed.draw_sprite(button_pressed_sprite, 0, i, 0)
        self.sprite_pressed.draw_sprite(button_pressed_left_sprite, 0, 0, 0)
        self.sprite_pressed.draw_sprite(button_pressed_right_sprite, 0, right,
                                        0)
        self.sprite_pressed.draw_text(button_font, self.text, sprite_w / 2,
                                      h / 2, width=w, height=h,
                                      color=button_text_color,
                                      halign=sge.ALIGN_CENTER,
                                      valign=sge.ALIGN_MIDDLE)
        self.sprite_pressed.draw_unlock()

    def refresh(self):
        parent = self.parent()
        if parent is not None:
            if ((keyboard_focused_window is parent and
                 parent.keyboard_focused_widget is self) or
                    (get_mouse_focused_window() is parent and
                     parent.get_mouse_focused_widget() is self)):
                if self._pressed:
                    self.sprite = self.sprite_pressed
                else:
                    self.sprite = self.sprite_selected
            else:
                self.sprite = self.sprite_normal

        super().refresh()

    def event_key_press(self, key, char):
        if key in ("enter", "kp_enter"):
            self._pressed = True

    def event_key_release(self, key):
        if key in ("enter", "kp_enter"):
            if self._pressed:
                self.event_press()

    def event_mouse_button_press(self, button):
        if button == "left":
            self._pressed = True

    def event_mouse_button_release(self, button):
        if button == "left":
            if self._pressed:
                self.event_press()

    def event_global_key_release(self, key):
        if key in ("enter", "kp_enter"):
            self._pressed = False

    def event_global_mouse_button_release(self, button):
        if button == "left":
            self._pressed = False

    def event_press(self):
        """Press event.

        Called when this button is clicked on, or when the Enter key is
        pressed while this button is selected.

        """
        pass


class CheckBox(Widget):

    def __init__(self, parent, x, y, z, enabled=False):
        super().__init__(parent, x, y, z)
        self.enabled = enabled
        self._pressed = False

    def refresh(self):
        if self.enabled:
            self.sprite = checkbox_on_sprite
        else:
            self.sprite = checkbox_off_sprite

        super().refresh()

    def event_key_press(self, key, char):
        if key in ("enter", "kp_enter"):
            self._pressed = True

    def event_key_release(self, key):
        if key in ("enter", "kp_enter"):
            if self._pressed:
                self.enabled = not self.enabled
                self.event_toggle()

    def event_mouse_button_press(self, button):
        if button == "left":
            self._pressed = True

    def event_mouse_button_release(self, button):
        if button == "left":
            if self._pressed:
                self.enabled = not self.enabled
                self.event_toggle()

    def event_global_key_release(self, key):
        if key in ("enter", "kp_enter"):
            self._pressed = False

    def event_global_mouse_button_release(self, button):
        if button == "left":
            self._pressed = False

    def event_toggle(self):
        """Toggle event.

        Called when the state of the checkbox is toggled by the user.

        """
        pass


class RadioButton(CheckBox):

    def refresh(self):
        if self.enabled:
            self.sprite = radiobutton_on_sprite
        else:
            self.sprite = radiobutton_off_sprite

        Widget.refresh(self)

    def _enable(self):
        # Enable the radiobutton, disable any others, and call
        # event_toggle.
        if not self.enabled:
            self.enabled = True
            parent = self.parent()
            if parent is not None:
                for widget in parent.widgets:
                    if widget is not self and isinstance(widget, RadioButton):
                        if widget.enabled:
                            widget.enabled = False
                            widget.event_toggle()

            self.event_toggle()

    def event_key_release(self, key):
        if key in ("enter", "kp_enter"):
            if self._pressed:
                self._enable()

    def event_mouse_button_release(self, button):
        if button == "left":
            if self._pressed:
                self._enable()

    def event_toggle(self):
        """Toggle event.

        Called when the state of the checkbox is toggled by the user.

        """
        pass


class ProgressBar(Widget):

    def __init__(self, parent, x, y, z, width=128, progress=0):
        super().__init__(parent, x, y, z, sge.Sprite(width=1, height=1))
        self.width = width
        self.progress = progress
        self.redraw()

    def redraw(self):
        self.progress = max(0, min(self.progress, 1))
        self.sprite.width = self.width
        self.sprite.height = progressbar_container_sprite.height
        left = progressbar_container_left_sprite.width
        right = self.width - progressbar_container_right_sprite.width
        y = int(round((progressbar_container_sprite.height -
                       progressbar_sprite.height) / 2))
        pixels = int(round(self.progress * (right - left)))

        self.sprite.draw_lock()

        for x in range(left, right, progressbar_container_sprite.width):
            self.sprite.draw_sprite(progressbar_container_sprite, 0, x, 0)

        for x in range(left, left + pixels, progressbar_sprite.width):
            self.sprite.draw_sprite(progressbar_sprite, 0, x, y)

        self.sprite.draw_sprite(progressbar_container_left_sprite, 0, 0, 0)
        self.sprite.draw_erase(right, 0, self.sprite.width - right,
                               self.sprite.height)
        self.sprite.draw_sprite(progressbar_container_right_sprite, 0, right,
                                0)
        self.sprite.draw_sprite(progressbar_left_sprite, 0,
                                left - progressbar_left_sprite.width, y)
        self.sprite.draw_sprite(progressbar_right_sprite, 0, left + pixels, y)

        self.sprite.draw_unlock()


class TextBox(Widget):

    pass


class ComboBox(TextBox):

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

    orig_image_directories = sge.image_directories
    orig_font_directories = sge.font_directories
    sge.image_directories = [DATADIR]
    sge.font_directories = [DATADIR]

    default_font = sge.Font(["DroidSans.ttf", "Droid Sans"], size=12)
    button_font = sge.Font(["DroidSans-Bold.ttf", "Droid Sans"], size=12)
    combobox_item_font = default_font
    textbox_font = default_font
    title_font = sge.Font(["DroidSans-Bold.ttf", "Droid Sans"], size=14)

    try:
        button_sprite = sge.Sprite("_gui_button")
        button_left_sprite = sge.Sprite("_gui_button_left")
        button_right_sprite = sge.Sprite("_gui_button_right")
        button_pressed_sprite = sge.Sprite("_gui_button_pressed")
        button_pressed_left_sprite = sge.Sprite("_gui_button_pressed_left")
        button_pressed_right_sprite = sge.Sprite("_gui_button_pressed_right")
        button_selected_sprite = sge.Sprite("_gui_button_selected")
        button_selected_left_sprite = sge.Sprite("_gui_button_selected_left")
        button_selected_right_sprite = sge.Sprite("_gui_button_selected_right")
        checkbox_off_sprite = sge.Sprite("_gui_checkbox_off")
        checkbox_on_sprite = sge.Sprite("_gui_checkbox_on")
        combobox_closed_sprite = sge.Sprite("_gui_combobox_closed")
        combobox_closed_left_sprite = sge.Sprite("_gui_combobox_closed_left")
        combobox_closed_right_sprite = sge.Sprite("_gui_combobox_closed_right")
        combobox_item_sprite = sge.Sprite("_gui_combobox_item")
        combobox_itemsep_sprite = sge.Sprite("_gui_combobox_itemsep")
        combobox_itemsep_left_sprite = sge.Sprite(
            "_gui_combobox_itemsep_right")
        combobox_open_left_sprite = sge.Sprite("_gui_combobox_open_left")
        combobox_open_right_sprite = sge.Sprite("_gui_combobox_open_right")
        combobox_open_bottom_sprite = sge.Sprite("_gui_combobox_open_bottom")
        combobox_open_bottomleft_sprite = sge.Sprite(
            "_gui_combobox_open_bottomleft")
        combobox_open_bottomright_sprite = sge.Sprite(
            "_gui_combobox_open_bottomright")
        combobox_open_top_sprite = sge.Sprite("_gui_combobox_open_top")
        combobox_open_topleft_sprite = sge.Sprite("_gui_combobox_open_topleft")
        combobox_open_topright_sprite = sge.Sprite(
            "_gui_combobox_open_topright")
        progressbar_sprite = sge.Sprite("_gui_progressbar")
        progressbar_left_sprite = sge.Sprite("_gui_progressbar_left")
        progressbar_right_sprite = sge.Sprite("_gui_progressbar_right")
        progressbar_container_sprite = sge.Sprite("_gui_progressbar_container")
        progressbar_container_left_sprite = sge.Sprite(
            "_gui_progressbar_container_left")
        progressbar_container_right_sprite = sge.Sprite(
            "_gui_progressbar_container_right")
        radiobutton_off_sprite = sge.Sprite("_gui_radiobutton_off")
        radiobutton_on_sprite = sge.Sprite("_gui_radiobutton_on")
        textbox_sprite = sge.Sprite("_gui_textbox")
        textbox_left_sprite = sge.Sprite("_gui_textbox_left")
        textbox_right_sprite = sge.Sprite("_gui_textbox_right")
        window_border_left_sprite = sge.Sprite("_gui_window_border_left")
        window_border_right_sprite = sge.Sprite("_gui_window_border_right")
        window_border_bottom_sprite = sge.Sprite("_gui_window_border_bottom")
        window_border_bottomleft_sprite = sge.Sprite(
            "_gui_window_border_bottomleft")
        window_border_bottomright_sprite = sge.Sprite(
            "_gui_window_border_bottomright")
        window_border_top_sprite = sge.Sprite("_gui_window_border_top")
        window_border_topleft_sprite = sge.Sprite("_gui_window_border_topleft")
        window_border_topright_sprite = sge.Sprite(
            "_gui_window_border_topright")
    except IOError:
        button_sprite = sge.Sprite(width=1, height=24)
        button_sprite.draw_rectangle(0, 0, 1, 24, fill="black")
        button_sprite.draw_rectangle(0, 1, 1, 22, fill="white")
        button_left_sprite = sge.Sprite(width=10, height=24)
        button_left_sprite.draw_rectangle(0, 0, 10, 24, fill="black")
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
        combobox_closed_right_sprite = sge.Sprite(width=25, height=24)
        combobox_closed_right_sprite.draw_rectangle(0, 0, 25, 24, fill="black")
        combobox_closed_right_sprite.draw_circle(12, 12, 5, fill="white")
        combobox_item_sprite = sge.Sprite(width=1, height=20)
        combobox_item_sprite.draw_rectangle(0, 0, 1, 20, fill="white")
        combobox_itemsep_sprite = sge.Sprite(width=1, height=2)
        combobox_itemsep_sprite.draw_rectangle(0, 0, 1, 2, fill="gray")
        combobox_itemsep_left_sprite = combobox_itemsep_sprite
        combobox_itemsep_right_sprite = combobox_itemsep_sprite
        combobox_open_left_sprite = sge.Sprite(width=4, height=1)
        combobox_open_left_sprite.draw_rectangle(0, 0, 4, 1, fill="black")
        combobox_open_right_sprite = combobox_open_left_sprite
        combobox_open_bottom_sprite = sge.Sprite(width=1, height=4)
        combobox_open_bottom_sprite.draw_rectangle(0, 0, 1, 4, fill="black")
        combobox_open_bottomleft_sprite = sge.Sprite(width=4, height=4)
        combobox_open_bottomleft_sprite.draw_rectangle(0, 0, 4, 4,
                                                       fill="black")
        combobox_open_bottomright_sprite = combobox_open_bottomleft_sprite
        combobox_open_top_sprite = sge.Sprite(width=1, height=25)
        combobox_open_top_sprite.draw_rectangle(0, 0, 1, 25, fill="black")
        combobox_open_top_sprite.draw_rectangle(0, 1, 1, 22, fill="white")
        combobox_open_topleft_sprite = sge.Sprite(width=4, height=25)
        combobox_open_topleft_sprite.draw_rectangle(0, 0, 4, 25, fill="black")
        combobox_open_topright_sprite = sge.Sprite(width=25, height=25)
        combobox_open_topright_sprite.draw_rectangle(0, 0, 25, 25,
                                                     fill="black")
        combobox_open_topright_sprite.draw_circle(12, 12, 5, fill="white")
        progressbar_sprite = sge.Sprite(width=1, height=18)
        progressbar_sprite.draw_rectangle(0, 0, 1, 18, fill="white")
        progressbar_left_sprite = sge.Sprite(width=2, height=18)
        progressbar_left_sprite.draw_rectangle(0, 0, 2, 18, fill="white")
        progressbar_right_sprite = progressbar_left_sprite
        progressbar_container_sprite = sge.Sprite(width=1, height=24)
        progressbar_container_sprite.draw_rectangle(0, 0, 1, 24, fill="black")
        progressbar_container_left_sprite = sge.Sprite(width=5, height=24)
        progressbar_container_left_sprite.draw_rectangle(0, 0, 5, 24,
                                                         fill="black")
        progressbar_container_right_sprite = progressbar_container_left_sprite
        radiobutton_off_sprite = checkbox_off_sprite
        radiobutton_on_sprite = checkbox_on_sprite
        textbox_sprite = combobox_closed_sprite
        textbox_left_sprite = combobox_closed_left_sprite
        textbox_right_sprite = textbox_left_sprite
        window_border_left_sprite = combobox_open_left_sprite
        window_border_right_sprite = window_border_left_sprite
        window_border_bottom_sprite = combobox_open_bottom_sprite
        window_border_bottomleft_sprite = combobox_open_bottomleft_sprite
        window_border_bottomright_sprite = window_border_bottomleft_sprite
        window_border_top_sprite = sge.Sprite(width=1, height=28)
        window_border_top_sprite.draw_rectangle(0, 0, 1, 28, fill="black")
        window_border_topleft_sprite = sge.Sprite(width=11, height=28)
        window_border_topleft_sprite.draw_rectangle(0, 0, 11, 28, fill="black")
        window_border_topright_sprite = sge.Sprite(width=23, height=28)
        window_border_topright_sprite.draw_rectangle(0, 0, 23, 28,
                                                     fill="black")
        window_border_topright_sprite.draw_line(0, 0, 23, 23, "red")
        window_border_topright_sprite.draw_line(0, 23, 23, 0, "red")

    sge.image_directories = orig_image_directories
    sge.font_directories = orig_font_directories


def get_mouse_focused_window():
    """Return the window that currently has mouse focus.

    The window with mouse focus is the one which is closest to the front
    that is touching the mouse cursor.

    Return :const:`None` if no window has focus.

    """
    x = sge.mouse.get_x()
    y = sge.mouse.get_y()
    for window in windows[::-1]:
        border_x = window.x
        border_y = window.y
        if window.border:
            border_x -= window_border_left_sprite.width
            border_y -= window_border_top_sprite.height

        if (border_x <= x < border_x + window.sprite.width and
                border_y <= y < border_y + window.sprite.height):
            return window

    return None


if __name__ == '__main__':
    # Test
    sge.Game(width=800, height=600)
    sge.game.event_close = sge.game.end
    init()
    handler = Handler()
    sge.Room(objects=[handler])

    window = Window(8, 8, 240, 240, title="Test window 1")
    button = Button(window, 8, 8, 0, "My button")
    label = Label(window, 8, 32, 0, "My label")
    label2 = Label(window, 8, 64, 0, "my label " * 50, width=224)
    button2 = Button(window, 16, 100, 5, "Another button", width=150)
    window.show()
    
    window2 = Window(480, 200, 320, 320, title="Test window 2")
    checkbox = CheckBox(window2, 16, 16, 0)
    radio = RadioButton(window2, 16, 48, 0)
    radio2 = RadioButton(window2, 16, 80, 0)
    radio3 = RadioButton(window2, 16, 112, 0)
    progress = ProgressBar(window2, 16, 144, 0, 288, progress=0.5)
    window2.show()

    sge.game.start()
