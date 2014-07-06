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

.. data:: window_background_color
.. data:: keyboard_focused_box_color
.. data:: text_color
.. data:: button_text_color
.. data:: textbox_text_color
.. data:: textbox_text_selected_color
.. data:: textbox_highlight_color
.. data:: title_text_color

   The colors used by this module.  They can be safely changed, but be
   sure to call :meth:`redraw` on all windows and widgets that would be
   affected; some changes might not become visible until you do.

.. data:: default_font
.. data:: button_font
.. data:: textbox_font
.. data:: title_font

   The fonts used by this module.  They can be safely changed, but be
   sure to call :meth:`redraw` on all windows and widgets that would be
   affected; some changes might not become visible until you do.

.. data:: button_sprite
.. data:: button_left_sprite
.. data:: button_right_sprite
.. data:: button_pressed_sprite
.. data:: button_pressed_left_sprite
.. data:: button_pressed_right_sprite
.. data:: button_selected_sprite
.. data:: button_selected_left_sprite
.. data:: button_selected_right_sprite
.. data:: checkbox_off_sprite
.. data:: checkbox_on_sprite
.. data:: progressbar_sprite
.. data:: progressbar_left_sprite
.. data:: progressbar_right_sprite
.. data:: progressbar_container_sprite
.. data:: progressbar_container_left_sprite
.. data:: progressbar_container_right_sprite
.. data:: radiobutton_off_sprite
.. data:: radiobutton_on_sprite
.. data:: textbox_sprite
.. data:: textbox_left_sprite
.. data:: textbox_right_sprite
.. data:: window_border_left_sprite
.. data:: window_border_right_sprite
.. data:: window_border_bottom_sprite
.. data:: window_border_bottomleft_sprite
.. data:: window_border_bottomright_sprite
.. data:: window_border_top_sprite
.. data:: window_border_topleft_sprite
.. data:: window_border_topright_sprite

   The sprites used by this module.  They can be safely changed, but be
   sure to call :meth:`redraw` on all windows and widgets that would be
   affected; some changes might not become visible until you do.
"""

import os
import weakref

try:
    from tkinter import Tk
except ImportError:
    class Tk:
        def withdraw(self): pass
        def clipboard_clear(self): pass
        def clipboard_append(self, *args, **kwargs): pass
        def selection_get(self, *args, **kwargs): return ''
        def destroy(self): pass

import sge


__all__ = ["Handler", "Window", "Dialog", "Widget", "Button", "CheckBox",
           "RadioButton", "ProgressBar", "TextBox", "MessageDialog",
           "TextEntryDialog", "FileSelectionDialog"]

DATADIR = os.path.join(os.path.dirname(__file__), "gui_data")
TEXTBOX_MIN_EDGE = 4
TEXTBOX_CURSOR_BLINK_TIME = 500
DIALOG_PADDING = 8

window_background_color = "#A4A4A4"
keyboard_focused_box_color = (0, 0, 0, 170)
text_color = "black"
button_text_color = "black"
textbox_text_color = "black"
textbox_text_selected_color = "white"
textbox_highlight_color = "blue"
title_text_color = "white"
default_font = None
button_font = None
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

    .. attribute:: windows

       A list of all windows that are currently handled by this handler.

       You don't need to modify this list manually. Instead, use
       :meth:`xsge.gui.Window.show` and :meth:`xsge.gui.Window.hide` to
       add and remove windows from this list, respectively.

    """

    def __init__(self):
        super().__init__(0, 0, visible=False, tangible=False)
        self.windows = []
        self.keyboard_focused_window = None

    def get_mouse_focused_window(self):
        """Return the window that currently has mouse focus.

        The window with mouse focus is the one which is closest to the front
        that is touching the mouse cursor.

        Return :const:`None` if no window has focus.

        """
        x = sge.mouse.get_x()
        y = sge.mouse.get_y()
        for window in reversed(self.windows):
            border_x = window.x
            border_y = window.y
            if window.border:
                border_x -= window_border_left_sprite.width
                border_y -= window_border_top_sprite.height

            if (border_x <= x < border_x + window.sprite.width and
                    border_y <= y < border_y + window.sprite.height):
                return window

        return None

    def event_step(self, time_passed, delta_mult):
        for window in self.windows[:]:
            window.event_step(time_passed, delta_mult)
            for widget in window.widgets:
                widget.event_step(time_passed, delta_mult)
            window.refresh()

    def event_key_press(self, key, char):
        window = self.keyboard_focused_window
        if window is not None:
            window.event_key_press(key, char)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_key_press(key, char)

        for window in self.windows[:]:
            window.event_global_key_press(key, char)
            for widget in window.widgets:
                widget.event_global_key_press(key, char)

    def event_key_release(self, key):
        window = self.keyboard_focused_window
        if window is not None:
            window.event_key_release(key)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_key_release(key)

        for window in self.windows[:]:
            window.event_global_key_release(key)
            for widget in window.widgets:
                widget.event_global_key_release(key)

    def event_mouse_button_press(self, button):
        window = self.get_mouse_focused_window()
        if window is not None:
            self.keyboard_focused_window = window
            window.move_to_front()
            if window.get_mouse_on_titlebar():
                window.event_titlebar_mouse_button_press(button)
            else:
                window.event_mouse_button_press(button)
                widget = window.get_mouse_focused_widget()
                if widget is not None:
                    widget.event_mouse_button_press(button)

        for window in self.windows[:]:
            window.event_global_mouse_button_press(button)
            for widget in window.widgets:
                widget.event_global_mouse_button_press(button)

    def event_mouse_button_release(self, button):
        window = self.get_mouse_focused_window()
        if window is not None:
            if window.get_mouse_on_titlebar():
                window.event_titlebar_mouse_button_release(button)
            else:
                window.event_mouse_button_release(button)
                widget = window.get_mouse_focused_widget()
                if widget is not None:
                    widget.event_mouse_button_release(button)

        for window in self.windows[:]:
            window.event_global_mouse_button_release(button)
            for widget in window.widgets:
                widget.event_global_mouse_button_release(button)


class Window:

    """Window class.

    Window objects are used to contain widgets.  They can be moved
    around the game window by the user.

    .. attribute:: parent

       A weak reference to this window's parent handler object, which is
       used to display it when it is supposed to be visible.

       If a strong reference is assigned to this attribute, it will
       automatically be changed to a weak reference.

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
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if isinstance(value, weakref.ref):
            self._parent = value
        else:
            self._parent = weakref.ref(value)

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        if value is not None:
            self._background_color = value
        else:
            self._background_color = window_background_color

    def __init__(self, parent, x, y, width, height, title="",
                 background_color=None, border=True):
        self.parent = parent
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
        """Add this window to its parent handler."""
        parent = self.parent()
        if parent is not None:
            if self not in parent.windows:
                parent.windows.append(self)
            else:
                self.move_to_front()

    def hide(self):
        """Remove this window from its parent handler."""
        parent = self.parent()
        if parent is not None:
            if self in parent.windows:
                parent.windows.remove(self)

    def move_to_front(self):
        """Move this window in front of all other windows."""
        parent = self.parent()
        if parent is not None:
            if self in parent.windows:
                i = parent.windows.index(self)
                parent.windows.append(parent.windows.pop(i))

    def move_to_back(self):
        """Move this window behind all other windows."""
        parent = self.parent()
        if parent is not None:
            if self in parent.windows:
                i = parent.windows.index(self)
                parent.windows.insert(0, parent.windows.pop(i))

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
        """Return whether or not the mouse is on the title bar."""
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

    def event_step(self, time_passed, delta_mult):
        """Step event.

        Called once every frame, before refreshing.  See the
        documentation for :meth:`sge.Game.event_step` for more
        information.

        """
        pass

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
                    i = -1

                while True:
                    i += 1

                    if i >= len(self.widgets):
                        self.keyboard_focused_widget = None
                        break
                    elif self.widgets[i].tab_focus:
                        self.keyboard_focused_widget = self.widgets[i]
                        break

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
                    self.x = x + self._border_grab[0]
                    self.y = y + self._border_grab[1]

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
    They are used for tasks that must be completed before the main
    program continues, such as pop-up messages.

    See the documentation for :class:`xsge.gui.Window` for more
    information.

    """

    def show(self):
        """Show this dialog and start its loop.

        Like :meth:`xsge.gui.Window.show`, this method adds the dialog
        to its parent.  It then starts this dialog's loop.  Call
        :meth:`xsge.gui.Dialog.hide` on this dialog to end the loop.

        """
        parent = self.parent()
        if parent is not None:
            super().show()
            parent.keyboard_focused_window = self
            while self in parent.windows:
                self.move_to_front()

                # Input events
                sge.game.pump_input()
                while sge.game.input_events:
                    event = sge.game.input_events.pop(0)

                    if isinstance(event, sge.input.KeyPress):
                        self.event_key_press(event.key, event.char)
                        widget = self.keyboard_focused_widget
                        if widget is not None:
                            widget.event_key_press(event.key, event.char)
                        self.event_global_key_press(event.key, event.char)
                        for widget in self.widgets:
                            widget.event_global_key_press(event.key,
                                                          event.char)
                    elif isinstance(event, sge.input.KeyRelease):
                        self.event_key_release(event.key)
                        widget = self.keyboard_focused_widget
                        if widget is not None:
                            widget.event_key_release(event.key)
                        self.event_global_key_release(event.key)
                        for widget in self.widgets:
                            widget.event_global_key_release(event.key)
                    elif isinstance(event, sge.input.MouseButtonPress):
                        if parent.get_mouse_focused_window() is self:
                            if self.get_mouse_on_titlebar():
                                self.event_titlebar_mouse_button_press(
                                    event.button)
                            else:
                                self.event_mouse_button_press(event.button)
                                widget = self.get_mouse_focused_widget()
                                if widget is not None:
                                    widget.event_mouse_button_press(
                                        event.button)

                        self.event_global_mouse_button_press(event.button)
                        for widget in self.widgets:
                            widget.event_global_mouse_button_press(
                                event.button)
                    elif isinstance(event, sge.input.MouseButtonRelease):
                        if parent.get_mouse_focused_window() is self:
                            if self.get_mouse_on_titlebar():
                                self.event_titlebar_mouse_button_release(
                                    event.button)
                            else:
                                self.event_mouse_button_release(event.button)
                                widget = self.get_mouse_focused_widget()
                                if widget is not None:
                                    widget.event_mouse_button_release(
                                        event.button)

                        self.event_global_mouse_button_release(event.button)
                        for widget in self.widgets:
                            widget.event_global_mouse_button_release(
                                event.button)
                    elif isinstance(event, sge.input.QuitRequest):
                        sge.game.input_events.insert(0, event)
                        self.hide()
                        return

                # Regulate speed
                time_passed = sge.game.regulate_speed()

                if sge.game.delta:
                    t = min(time_passed, 1000 / sge.game.delta_min)
                    delta_mult = t / (1000 / sge.game.fps)
                else:
                    delta_mult = 1

                # Project windows
                self.event_step(time_passed, delta_mult)
                for widget in self.widgets:
                    widget.event_step(time_passed, delta_mult)

                for window in parent.windows[:]:
                    window.refresh()

                # Refresh
                sge.game.refresh()

            sge.game.pump_input()
            sge.game.input_events = []


class Widget:

    """Widget class.

    Widget objects are things like controls and decorations that exist
    on windows.

    .. attribute:: parent

       A weak reference to this widget's parent window.

       If a strong reference is assigned to this attribute, it will
       automatically be changed to a weak reference.

    .. attribute:: x

       The horizontal position of the widget relative to its parent
       window.

    .. attribute:: y

       The vertical position of the widget relative to its parent
       window.

    .. attribute:: z

       The Z-axis position of the widget.  Widgets with a higher Z-axis
       value are in front of widgets with a lower Z-axis value.  This
       value is not connected in any way to Z-axis values in the SGE.

    .. attribute:: sprite

       The sprite this widget displays as itself.

    """

    tab_focus = True

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
            if parent.keyboard_focused_widget is self:
                sge.game.project_rectangle(
                    parent.x + self.x, parent.y + self.y, self.sprite.width,
                    self.sprite.height, outline=keyboard_focused_box_color)
        else:
            self.destroy()

    def event_step(self, time_passed, delta_mult):
        """Step event.

        Called once every frame, before refreshing.  See the
        documentation for :meth:`sge.Game.event_step` for more
        information.

        """
        pass

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

    tab_focus = False

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

    """Button widget.

    This widget contains some text and can be clicked on by the user.

    .. attribute:: text

       The text contained in the button.

    .. attribute:: width

       The width of the button.  If set to :const:`None`, the width is
       chosen based on the width of the rendered text.

    .. attribute:: halign

       The horizontal alignment of the text.  See the documentation for
       :meth:`sge.Sprite.draw_text` for more information.

    See the documentation for :class:`xsge.gui.Widget` for more
    information.

    """

    def __init__(self, parent, x, y, z, text, width=None,
                 halign=sge.ALIGN_CENTER):
        super().__init__(parent, x, y, z)
        self.text = text
        self.width = width
        self.halign = halign
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
            w = int(round(button_font.get_width(self.text, height=h)))
            sprite_w = w + button_left_sprite.width + button_right_sprite.width
        else:
            sprite_w = int(round(self.width))
            w = sprite_w - button_left_sprite.width - button_right_sprite.width

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
                                     halign=self.halign,
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
                                       halign=self.halign,
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
                                      halign=self.halign,
                                      valign=sge.ALIGN_MIDDLE)
        self.sprite_pressed.draw_unlock()

    def refresh(self):
        parent = self.parent()
        if parent is not None:
            sge.game.project_sprite(self.sprite, 0, parent.x + self.x,
                                    parent.y + self.y)
        else:
            self.destroy()

    def event_step(self, time_passed, delta_mult):
        parent = self.parent()
        if parent is not None:
            handler = parent.parent()
            if (handler is not None and
                ((handler.keyboard_focused_window is parent and
                  parent.keyboard_focused_widget is self) or
                 (handler.get_mouse_focused_window() is parent and
                  parent.get_mouse_focused_widget() is self))):
                if self._pressed:
                    self.sprite = self.sprite_pressed
                else:
                    self.sprite = self.sprite_selected
            else:
                self.sprite = self.sprite_normal

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

    """Check box widget.

    This widget can be toggled "on" or "off" by clicking on it.

    .. attribute:: enabled

       Whether or not the checkbox is on.

    See the documentation for :class:`xsge.gui.Widget` for more
    information.

    """

    def __init__(self, parent, x, y, z, enabled=False):
        super().__init__(parent, x, y, z)
        self.enabled = enabled
        self._pressed = False

    def event_step(self, time_passed, delta_mult):
        if self.enabled:
            self.sprite = checkbox_on_sprite
        else:
            self.sprite = checkbox_off_sprite

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

    """Radio button widget.

    This widget is mostly like :class:`xsge.gui.CheckBox`, but clicking
    on it while it is on will not turn it off, and only one radio button
    can be on at any given time (i.e. enabling one radio button on a
    window will disable all others on the same window).

    See the documentation for :class:`xsge.gui.CheckBox` for more
    information.

    """

    def event_step(self, time_passed, delta_mult):
        if self.enabled:
            self.sprite = radiobutton_on_sprite
        else:
            self.sprite = radiobutton_off_sprite

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

        Called when the state of the radiobutton is toggled by the user.

        """
        pass


class ProgressBar(Widget):

    """Progress bar widget.

    This widget displays a bar which can be used to show progress (e.g.
    of some task being done).

    .. attribute:: width

       The width of the progress bar.

    .. attribute:: progress

       The progress indicated by the progress bar as a factor (i.e.
       ``0`` is no completion, ``1`` is full completion, and ``0.5`` is
       half completion).

    """

    tab_focus = False

    def __init__(self, parent, x, y, z, width=128, progress=0):
        super().__init__(parent, x, y, z, sge.Sprite(width=1, height=1))
        self.width = width
        self.progress = progress
        self.redraw()

    def destroy(self):
        super().destroy()
        self.sprite.destroy()

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
        self.sprite.draw_clear()

        self.sprite.draw_sprite(progressbar_container_left_sprite, 0, 0, 0)

        for x in range(left, right, progressbar_container_sprite.width):
            self.sprite.draw_sprite(progressbar_container_sprite, 0, x, 0)

        for x in range(left, left + pixels, progressbar_sprite.width):
            self.sprite.draw_sprite(progressbar_sprite, 0, x, y)

        self.sprite.draw_erase(right, 0, self.sprite.width - right,
                               self.sprite.height)
        self.sprite.draw_sprite(progressbar_container_right_sprite, 0, right,
                                0)
        self.sprite.draw_sprite(progressbar_left_sprite, 0,
                                left - progressbar_left_sprite.width, y)
        self.sprite.draw_sprite(progressbar_right_sprite, 0, left + pixels, y)

        self.sprite.draw_unlock()


class TextBox(Widget):

    """Text box widget.

    This widget provides a place for the user to enter text.

    .. attribute:: width

       The width of the text box.

    .. attribute:: text

       The text in the text box by default.

    See the documentation for :class:`xsge.gui.Widget` for more
    information.

    """

    def __init__(self, parent, x, y, z, width=32, text=""):
        super().__init__(parent, x, y, z, sge.Sprite(width=1, height=1))
        self.width = width
        self.text = text
        self._cursor_pos = 0
        self._clicked_pos = None
        self._selected = None
        self._text_x = 0
        self._cursor_shown = True
        self._cursor_blink_time = TEXTBOX_CURSOR_BLINK_TIME
        self.redraw()

    def destroy(self):
        super().destroy()
        self.sprite.destroy()

    def redraw(self):
        self.sprite.width = self.width
        self.sprite.height = textbox_sprite.height
        self._cursor_h = textbox_font.get_height("|")
        left = textbox_left_sprite.width
        right = self.width - textbox_right_sprite.width

        self.sprite.draw_lock()
        self.sprite.draw_clear()

        self.sprite.draw_sprite(textbox_left_sprite, 0, 0, 0)

        for i in range(left, right, textbox_sprite.width):
            self.sprite.draw_sprite(textbox_sprite, 0, i, 0)

        self.sprite.draw_erase(right, 0, self.sprite.width - right,
                               self.sprite.height)
        self.sprite.draw_sprite(textbox_right_sprite, 0, right, 0)

        self.sprite.draw_unlock()

    def refresh(self):
        parent = self.parent()
        if parent is not None:
            sge.game.project_sprite(self.sprite, 0, parent.x + self.x,
                                    parent.y + self.y)

            self._cursor_pos = max(0, min(self._cursor_pos,
                                          len(self.text)))

            text_area_w = (self.width - textbox_right_sprite.width -
                           textbox_left_sprite.width)
            text_y = textbox_sprite.height / 2
            cursor_x = textbox_font.get_width(self.text[:self._cursor_pos])
            cursor_y = text_y - self._cursor_h / 2

            if 0 < self._cursor_pos < len(self.text):
                min_edge = TEXTBOX_MIN_EDGE
            else:
                min_edge = 0

            if self._text_x + cursor_x < min_edge:
                self._text_x = min_edge - cursor_x
            elif self._text_x + cursor_x > text_area_w - min_edge:
                self._text_x = text_area_w - min_edge - cursor_x

            text_sprite = sge.Sprite(width=text_area_w,
                                     height=textbox_sprite.height)
            text_sprite.draw_lock()

            text_sprite.draw_text(textbox_font, self.text, self._text_x,
                                  text_y, color=textbox_text_color,
                                  valign=sge.ALIGN_MIDDLE)

            if self._selected is None:
                if (self._cursor_shown and
                        parent.keyboard_focused_widget is self):
                    text_sprite.draw_line(cursor_x + self._text_x, cursor_y,
                                          cursor_x + self._text_x,
                                          cursor_y + self._cursor_h,
                                          textbox_text_color)
            else:
                a, b = self._selected
                x = textbox_font.get_width(self.text[:a])
                w = textbox_font.get_width(self.text[a:b])
                y = text_y - self._cursor_h / 2
                text_sprite.draw_rectangle(x + self._text_x, y, w,
                                           self._cursor_h,
                                           fill=textbox_highlight_color)
                text_sprite.draw_text(textbox_font, self.text[a:b],
                                      x + self._text_x, text_y,
                                      color=textbox_text_selected_color,
                                      valign=sge.ALIGN_MIDDLE)

            text_sprite.draw_unlock()

            sge.game.project_sprite(
                text_sprite, 0, parent.x + self.x + textbox_left_sprite.width,
                parent.y + self.y)
            text_sprite.destroy()
        else:
            self.destroy()

    def _show_cursor(self):
        # Forcibly show the cursor (restarting the animation).
        self._cursor_shown = True
        self._cursor_blink_time = TEXTBOX_CURSOR_BLINK_TIME

    def _get_previous_word(self):
        # Return the index of the start of the previous or current word.
        i = max(0, self._cursor_pos - 1)
        while i > 0 and not self.text[i].isalnum():
            i -= 1

        while i > 0 and self.text[i].isalnum():
            i -= 1

        return i

    def _get_next_word(self):
        # Return the index of the end of the next or current word.
        i = min(self._cursor_pos + 1, len(self.text))
        while i < len(self.text) and not self.text[i].isalnum():
            i += 1

        while i < len(self.text) and self.text[i].isalnum():
            i += 1

        return i

    def _move_selection(self, pos):
        # Move the selection so that the cursor is at ``pos``.
        if self._selected is not None:
            if self._selected[0] == self._cursor_pos:
                fixed_pos = self._selected[1]
            else:
                fixed_pos = self._selected[0]

            if fixed_pos > pos:
                self._selected = (pos, fixed_pos)
            elif pos > fixed_pos:
                self._selected = (fixed_pos, pos)
            else:
                self._selected = None
        else:
            if self._cursor_pos > pos:
                self._selected = (pos, self._cursor_pos)
            elif pos > self._cursor_pos:
                self._selected = (self._cursor_pos, pos)
            else:
                self._selected = None

        self._cursor_pos = pos

    def _delete_selection(self):
        # Delete the currently selected text.
        if self._selected is not None:
            a, b = self._selected
            self._cursor_pos = a
            self.text = ''.join([self.text[:a], self.text[b:]])
            self._selected = None

    def _get_cursor_position(self):
        # Get the cursor position from mouse position ``x``.
        parent = self.parent()
        if parent is not None:
            x = (sge.mouse.get_x() - parent.x - self.x - self._text_x -
                 textbox_left_sprite.width)
            i = 0
            while (i < len(self.text) and
                   textbox_font.get_width(self.text[:i]) < x):
                i += 1

            # FIXME: This feels inaccurate, but I can't think of any way
            # to reliably make it better.  Leaving it as-is for now.
            return i

        return 0

    def _update_selection(self):
        # Update the selection, for use when the mouse button is held
        # down.
        self._cursor_pos = self._get_cursor_position()
        if self._cursor_pos > self._clicked_pos:
            self._selected = (self._clicked_pos, self._cursor_pos)
        elif self._cursor_pos < self._clicked_pos:
            self._selected = (self._cursor_pos, self._clicked_pos)
        else:
            self._selected = None

    def event_step(self, time_passed, delta_mult):
        self._cursor_blink_time -= time_passed
        if self._cursor_blink_time <= 0:
            self._cursor_shown = not self._cursor_shown
            self._cursor_blink_time += TEXTBOX_CURSOR_BLINK_TIME

        if self._clicked_pos is not None:
            self._update_selection()

    def event_key_press(self, key, char):
        if sge.keyboard.get_modifier("ctrl"):
            if key == "left":
                if sge.keyboard.get_modifier("shift"):
                    self._move_selection(self._get_previous_word())
                else:
                    if self._selected is not None:
                        self._cursor_pos = self._selected[0]
                        self._selected = None
                    else:
                        self._cursor_pos = self._get_previous_word()

                    self._show_cursor()
            elif key == "right":
                if sge.keyboard.get_modifier("shift"):
                    self._move_selection(self._get_next_word())
                else:
                    if self._selected is not None:
                        self._cursor_pos = self._selected[0]
                        self._selected = None
                    else:
                        self._cursor_pos = self._get_next_word()

                    self._show_cursor()
            elif key == 'a':
                self._selected = (0, len(self.text))
                self._cursor_pos = len(self.text)
            elif key == 'x':
                if self._selected is not None:
                    a, b = self._selected
                    r = Tk()
                    r.withdraw()
                    r.clipboard_clear()
                    r.clipboard_append(self.text[a:b])
                    r.destroy()
                    self._delete_selection()
            elif key == 'c':
                if self._selected is not None:
                    a, b = self._selected
                    r = Tk()
                    r.withdraw()
                    r.clipboard_clear()
                    r.clipboard_append(self.text[a:b])
                    r.destroy()
            elif key == 'v':
                self._delete_selection()
                r = Tk()
                r.withdraw()
                new_text = r.selection_get(selection="CLIPBOARD")
                r.destroy()
                self.text = ''.join([self.text[:self._cursor_pos], new_text,
                                     self.text[self._cursor_pos:]])
                self._cursor_pos += len(new_text)
        else:
            if key == "left":
                if sge.keyboard.get_modifier("shift"):
                    pos = max(0, self._cursor_pos - 1)
                    self._move_selection(pos)
                else:
                    if self._selected is not None:
                        self._cursor_pos = self._selected[0]
                        self._selected = None
                    elif self._cursor_pos > 0:
                        self._cursor_pos -= 1

                    self._show_cursor()
            elif key == "right":
                if sge.keyboard.get_modifier("shift"):
                    pos = min(self._cursor_pos + 1, len(self.text))
                    self._move_selection(pos)
                else:
                    if self._selected is not None:
                        self._cursor_pos = self._selected[1]
                        self._selected = None
                    elif self._cursor_pos < len(self.text):
                        self._cursor_pos += 1

                    self._show_cursor()
            elif key == "home":
                self._cursor_pos = 0
                self._selected = None
                self._show_cursor()
            elif key == "end":
                self._cursor_pos = len(self.text)
                self._selected = None
                self._show_cursor()
            elif key == "backspace":
                if self._selected is None and self._cursor_pos > 0:
                    self._selected = (self._cursor_pos - 1, self._cursor_pos)

                self._delete_selection()
                self._show_cursor()
            elif key == "delete":
                if (self._selected is None and
                        self._cursor_pos < len(self.text)):
                    self._selected = (self._cursor_pos, self._cursor_pos + 1)

                self._delete_selection()
                self._show_cursor()
            elif char and char not in ('\n', '\t', '\b', '\r', '\x1b'):
                self._delete_selection()
                i = self._cursor_pos
                self.text = ''.join([self.text[:i], char, self.text[i:]])
                self._cursor_pos += 1
                self._show_cursor()

    def event_mouse_button_press(self, button):
        if button == "left":
            parent = self.parent()
            if parent is not None:
                parent.keyboard_focused_widget = self
                self._clicked_pos = self._get_cursor_position()
                self._show_cursor()

    def event_global_mouse_button_release(self, button):
        if button == "left":
            if self._clicked_pos is not None:
                self._update_selection()
                self._clicked_pos = None

    def event_change_text(self):
        """Change text event.

        Called when the user changes the text in the textbox.

        """
        pass


class MessageDialog(Dialog):

    """Message dialog.

    This dialog shows a message box and accepts button input.  All
    buttons cause the dialog to close and set :attr:`choice` to the
    button pressed.

    .. attribute:: choice

       The button clicked.  If a button hasn't been clicked (i.e. the
       dialog hasn't yet been closed or was closed by clicking on the
       close button), it is set to :const:`None`.

    See the documentation for :class:`xsge.gui.Dialog` for more
    information.

    """

    def __init__(self, parent, message, buttons=("Ok",), width=320, height=120,
                 title="Message"):
        """See :func:`xsge.gui.show_message`."""
        x = sge.game.width / 2 - width / 2
        y = sge.game.height / 2 - height / 2
        super().__init__(parent, x, y, width, height, title=title)
        button_w = max(1, int(round((width - DIALOG_PADDING *
                                     (len(buttons) + 1)) / len(buttons))))
        button_h = button_sprite.height
        label_w = max(1, width - DIALOG_PADDING * 2)
        label_h = max(1, height - button_h - DIALOG_PADDING * 3)
        Label(self, DIALOG_PADDING, DIALOG_PADDING, 0, message, width=label_w,
              height=label_h)

        y = height - button_h - DIALOG_PADDING
        for i in range(len(buttons)):
            x = i * (button_w + DIALOG_PADDING) + DIALOG_PADDING
            button = Button(self, x, y, 0, buttons[i], width=button_w)

            def event_press(self=button, x=i):
                parent = self.parent()
                if parent is not None:
                    parent._return_button(x)

            button.event_press = event_press

        self.keyboard_focused_widget = button
        self.choice = None

    def _return_button(self, x):
        # Return button with index ``x``.
        self.choice = x
        self.destroy()


class TextEntryDialog(Dialog):

    """Text entry dialog.

    This dialog shows a message and has the user enter some text.  Two
    buttons are shown: a "Cancel" button that closes the dialog, and an
    "Ok" button that sets :attr:`text` to the text entered and then
    closes the dialog.

    .. attribute:: text

       The text entered after the "Ok" button is clicked.  If the "Ok"
       button hasn't been clicked, this is :const:`None`.

    See the documentation for :class:`xsge.gui.Dialog` for more
    information.

    """

    def __init__(self, parent, message="", width=320, height=152, text="",
                 title="Text Entry"):
        """See :func:`xsge.gui.get_text_entry`."""
        x = sge.game.width / 2 - width / 2
        y = sge.game.height / 2 - height / 2
        super().__init__(parent, x, y, width, height, title=title)
        button_w = max(1, (width - DIALOG_PADDING * 3) / 2)
        button_h = button_sprite.height
        textbox_w = max(1, width - DIALOG_PADDING * 2)
        textbox_h = textbox_sprite.height
        label_w = textbox_w
        label_h = max(1, height - button_h - textbox_h - DIALOG_PADDING * 4)

        x = DIALOG_PADDING
        y = DIALOG_PADDING
        Label(self, x, y, 0, message, width=label_w, height=label_h)

        y = label_h + DIALOG_PADDING * 2
        self.textbox = TextBox(self, x, y, 0, width=textbox_w, text=text)
        if text:
            self.textbox._selected = (0, len(text))

        def event_key_press(key, char, self=self.textbox):
            if key in ("enter", "kp_enter"):
                parent = self.parent()
                if parent is not None:
                    parent._return_text(self.text)
            else:
                TextBox.event_key_press(self, key, char)

        self.textbox.event_key_press = event_key_press

        y = height - button_h - DIALOG_PADDING
        x = DIALOG_PADDING
        button = Button(self, x, y, 0, "Cancel", width=button_w)

        def event_press(self=button):
            parent = self.parent()
            if parent is not None:
                parent.destroy()

        button.event_press = event_press

        x = button_w + DIALOG_PADDING * 2
        button = Button(self, x, y, 0, "Ok", width=button_w)

        def event_press(self=button):
            parent = self.parent()
            if parent is not None:
                parent._return_text(parent.textbox.text)

        button.event_press = event_press

        self.text = None
        self.keyboard_focused_widget = self.textbox

    def _return_text(self, s):
        # Return ``s`` as this dialog's text.
        self.text = s
        self.destroy()


def init():
    """Prepare this module for use.

    This function in particular creates the sprites and fonts it uses
    for windows and widgets.  Because of this, it must not be called
    until after a :class:`sge.Game` object has been created.

    """
    global default_font
    global button_font
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
        textbox_sprite = button_sprite
        textbox_left_sprite = sge.Sprite(width=4, height=24)
        textbox_left_sprite.draw_rectangle(0, 0, 4, 24, fill="black")
        textbox_right_sprite = textbox_left_sprite
        window_border_left_sprite = sge.Sprite(width=4, height=1)
        window_border_left_sprite.draw_rectangle(0, 0, 4, 1, fill="black")
        window_border_right_sprite = window_border_left_sprite
        window_border_bottom_sprite = sge.Sprite(width=1, height=4)
        window_border_bottom_sprite.draw_rectangle(0, 0, 1, 4, fill="black")
        window_border_bottomleft_sprite = sge.Sprite(width=4, height=4)
        window_border_bottomleft_sprite.draw_rectangle(0, 0, 4, 4,
                                                       fill="black")
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


def show_message(parent, message, buttons=("Ok",), width=320, height=120,
                 title="Message"):
    """Show a message and return the button pressed.

    Arguments:

    - ``parent`` -- The parent handler of the :class:`MessageDialog`
      object created.
    - ``message`` -- The message shown to the user.
    - ``buttons`` -- A list of strings to put inside the buttons, from
      left to right.
    - ``width`` -- The width of the :class:`MessageDialog` created.
    - ``height`` -- The height of the :class:`MessageDialog` created.
    - ``title`` -- The window title of the :class:`MessageDialog`
      created.

    Value returned is the index of the button pressed, where ``0`` is
    the leftmost button, or :const:`None` if no button was pressed (i.e.
    the close button on the window frame was pressed instead).

    See the documentation for :class:`MessageDialog` for more
    information.

    """
    w = MessageDialog(parent, message, buttons=buttons, width=width,
                      height=height, title=title)
    w.show()
    w.destroy()
    return w.choice


def get_text_entry(parent, message="", width=320, height=152, text="",
                   title="Text Entry"):
    """Return text entered by the user.

    Arguments:

    - ``parent`` -- The parent handler of the :class:`MessageDialog`
      object created.
    - ``message`` -- The message shown to the user.
    - ``width`` -- The width of the :class:`MessageDialog` created.
    - ``height`` -- The height of the :class:`MessageDialog` created.
    - ``text`` -- The text in the text box by default.
    - ``title`` -- The window title of the :class:`MessageDialog`
      created.

    Value returned is the text entered if the "Ok" button is pressed, or
    :const:`None` otherwise.

    See the documentation for :class:`TextEntryDialog` for more
    information.

    """
    w = TextEntryDialog(parent, message=message, width=width, height=height,
                        text=text, title=title)
    w.show()
    w.destroy()
    return w.text
