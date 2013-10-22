#!/usr/bin/env python2

# Stellarly-Encompassing Level Editor
# Copyright (C) 2013 Julian Marchant <onpon4@riseup.net>
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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys

import wx

import stj

MAIN_WINDOW_TITLE = "Stellarly-Encompassing Level Editor"
MAIN_WINDOW_SIZE = (640, 480)


class Frame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__(*args, **kwargs)

        status_bar = self.CreateStatusBar()
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        edit_menu = wx.Menu()
        view_menu = wx.Menu()
        help_menu = wx.Menu()

        m = file_menu.Append(wx.ID_NEW, text='&New Room',
                             help="Create a new room in the current game file")
        self.Bind(wx.EVT_MENU, self.OnNew, m)

        m = file_menu.Append(wx.ID_OPEN, text='&Open Rooms',
                             help="Open the rooms from a game file")
        self.Bind(wx.EVT_MENU, self.OnOpen, m)

        file_menu.AppendSeparator()

        m = file_menu.Append(wx.ID_SAVE, text='&Save Rooms',
                             help="Save the rooms of the current game file")
        self.Bind(wx.EVT_MENU, self.OnSave, m)

        m = file_menu.Append(wx.ID_REVERT)

        file_menu.AppendSeparator()

        m = file_menu.Append(wx.ID_CLOSE, help="Close the current game file")
        self.Bind(wx.EVT_MENU, self.OnClose, m)

        m = file_menu.Append(wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnQuit, m)

        m = edit_menu.Append(wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, self.OnUndo, m)

        m = edit_menu.Append(wx.ID_REDO)
        self.Bind(wx.EVT_MENU, self.OnRedo, m)

        edit_menu.AppendSeparator()

        m = edit_menu.Append(wx.ID_CUT)
        self.Bind(wx.EVT_MENU, self.OnCut, m)

        m = edit_menu.Append(wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self.OnCopy, m)

        m = edit_menu.Append(wx.ID_PASTE)
        self.Bind(wx.EVT_MENU, self.OnPaste, m)

        m = edit_menu.Append(wx.ID_DELETE)
        self.Bind(wx.EVT_MENU, self.OnDelete, m)

        edit_menu.AppendSeparator()

        m = edit_menu.Append(wx.ID_SELECTALL)
        self.Bind(wx.EVT_MENU, self.OnSelectAll, m)

        edit_menu.AppendSeparator()

        m = edit_menu.Append(wx.ID_PROPERTIES)
        self.Bind(wx.EVT_MENU, self.OnProperties, m)

        m = view_menu.Append(wx.ID_ANY, text="Zoom &Out")
        self.Bind(wx.EVT_MENU, self.OnZoomOut, m)

        m = view_menu.Append(wx.ID_ANY, text="Zoom &In")
        self.Bind(wx.EVT_MENU, self.OnZoomIn, m)

        m = view_menu.Append(wx.ID_ANY, text="Zoom &Reset")
        self.Bind(wx.EVT_MENU, self.OnZoomReset, m)

        m = help_menu.Append(wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnAbout, m)

        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(edit_menu, '&Edit')
        menu_bar.Append(view_menu, '&View')
        menu_bar.Append(help_menu, '&Help')
        self.SetMenuBar(menu_bar)

        self.Show()

    def OnNew(self, event):
        pass

    def OnOpen(self, event):
        pass

    def OnSave(self, event):
        pass

    def OnRevert(self, event):
        pass

    def OnClose(self, event):
        pass

    def OnQuit(self, event):
        self.Close()

    def OnUndo(self, event):
        pass

    def OnRedo(self, event):
        pass

    def OnCut(self, event):
        pass

    def OnCopy(self, event):
        pass

    def OnPaste(self, event):
        pass

    def OnDelete(self, event):
        pass

    def OnSelectAll(self, event):
        pass

    def OnProperties(self, event):
        pass

    def OnZoomOut(self, event):
        pass

    def OnZoomIn(self, event):
        pass

    def OnZoomReset(self, event):
        pass

    def OnAbout(self, event):
        pass


def main(*args):
    app = wx.PySimpleApp()
    Frame(None, id=wx.ID_ANY, title=MAIN_WINDOW_TITLE, size=MAIN_WINDOW_SIZE)
    app.MainLoop()


if __name__ == '__main__':
    main(*sys.argv)
