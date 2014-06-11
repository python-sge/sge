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
"""

import sge


__all__ = ["Frame", "Window", "Dialog", "MessageDialog", "TextEntryDialog",
           "FileSelectionDialog", "Widget", "Button", "CheckBox", "ComboBox",
           "ProgressBar", "RadioButton", "TextBox"]


class Frame(sge.StellarClass):

    pass


class Window(Frame):

    pass


class Dialog(Frame):

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
