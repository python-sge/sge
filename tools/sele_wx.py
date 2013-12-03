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

__version__ = "0.0.1"

import sys
import os

import wx

import stj

PROGRAM_NAME = "Stellarly-Encompassing Level Editor"
PROGRAM_VERSION = __version__
PROGRAM_DESCRIPTION = "Universal level editor for SGE games."
PROGRAM_COPYRIGHT = "(C) 2013 Julian Marchant <onpon4@riseup.net>"
MAIN_WINDOW_TITLE = "Stellarly-Encompassing Level Editor"
MAIN_WINDOW_SIZE = (800, 600)


class Frame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__(*args, **kwargs)

        self.games = []

        status_bar = self.CreateStatusBar()
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        edit_menu = wx.Menu()
        view_menu = wx.Menu()
        zoom_menu = wx.Menu()
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

        m = file_menu.Append(wx.ID_REVERT_TO_SAVED)
        self.Bind(wx.EVT_MENU, self.OnRevert, m)

        file_menu.AppendSeparator()

        m = file_menu.Append(
            wx.ID_REFRESH, text="Reload Resources",
            help="Reload the non-room resources of the current game file")
        self.Bind(wx.EVT_MENU, self.OnReload, m)

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

        m = view_menu.Append(wx.ID_ZOOM_OUT)
        self.Bind(wx.EVT_MENU, self.OnZoomOut, m)

        m = view_menu.Append(wx.ID_ZOOM_IN)
        self.Bind(wx.EVT_MENU, self.OnZoomIn, m)

        m = view_menu.Append(wx.ID_ZOOM_100)
        self.Bind(wx.EVT_MENU, self.OnZoomReset, m)

        edit_menu.AppendSeparator()

        m = zoom_menu.AppendRadioItem(wx.ID_ANY, text="&No Grid",
                                      help="Show no grid")
        self.Bind(wx.EVT_MENU, self.OnNoGrid, m)

        m = zoom_menu.AppendRadioItem(wx.ID_ANY, text="&Rectangular Grid",
                                      help="Show a rectangular grid")
        self.Bind(wx.EVT_MENU, self.OnRectangularGrid, m)

        m = zoom_menu.AppendRadioItem(wx.ID_ANY, text="&Isometric Grid",
                                      help="Show an isometric (diagonal) grid")
        self.Bind(wx.EVT_MENU, self.OnIsometricGrid, m)

        view_menu.AppendSubMenu(zoom_menu, text="&Grid")

        m = help_menu.Append(wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnAbout, m)

        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(edit_menu, '&Edit')
        menu_bar.Append(view_menu, '&View')
        menu_bar.Append(help_menu, '&Help')
        self.SetMenuBar(menu_bar)

        # TODO: Get a toolbar working
        #toolbar = self.CreateToolBar(style=wx.TB_HORIZONTAL)

        #toolbar.AddLabelTool(wx.ID_NEW, label="New Room")

        #toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.games_notebook = wx.Notebook(self, style=wx.NB_TOP)
        sizer.Add(self.games_notebook, proportion=1, flag=wx.EXPAND)

        self.SetSizer(sizer)
        self.Refresh()
        self.load_game('test.json')
        self.load_game('test2.json')
        self.load_game('test.json')
        self.Show()

    def load_game(self, fname):
        # fname: The name of the JSON file to pass to stj.StellarJSON.
        """Load a game, storing it in self.games, and create a tab."""
        for i in xrange(len(self.games)):
            i_fname = os.path.realpath(self.games[i].fname)
            if i_fname == os.path.realpath(fname):
                # This is the same file.  Open its tab.
                self.games_notebook.SetSelection(i)
                return

        game = stj.StellarJSON(fname)
        self.games.append(game)
        panel = GamePanel(game, self.games_notebook)
        self.games_notebook.AddPage(panel, os.path.realpath(game.fname))

        self.Refresh()

    def Refresh(self, *args, **kwargs):
        assert len(self.games) == self.games_notebook.GetPageCount()

        for i in xrange(len(self.games)):
            self.games_notebook.SetPageText(i, os.path.realpath(
                self.games[i].fname))

        super(Frame, self).Refresh(*args, **kwargs)

    def OnNew(self, event):
        pass

    def OnOpen(self, event):
        pass

    def OnSave(self, event):
        pass

    def OnRevert(self, event):
        pass

    def OnReload(self, event):
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

    def OnNoGrid(self, event):
        print("No grid")

    def OnRectangularGrid(self, event):
        print("Rectangular grid")

    def OnIsometricGrid(self, event):
        print("Isometric grid")

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.SetName(PROGRAM_NAME)
        info.SetVersion(PROGRAM_VERSION)
        info.SetDescription(PROGRAM_DESCRIPTION)
        info.SetCopyright(PROGRAM_COPYRIGHT)
        icon = wx.Icon("sge_logo_alpha_black.png", wx.BITMAP_TYPE_PNG)
        info.SetIcon(icon)

        wx.AboutBox(info)


class GamePanel(wx.Panel):

    def __init__(self, game, *args, **kwargs):
        # game: The stj.StellarJSON file representing this game.
        super(GamePanel, self).__init__(*args, **kwargs)

        self.game = game
        self.room_selection = wx.NOT_FOUND

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.rooms_listbox = wx.ListBox(self, size=(128, -1),
                                        style=wx.LB_SINGLE | wx.LB_HSCROLL |
                                        wx.LB_NEEDED_SB)
        self.Bind(wx.EVT_LISTBOX, self.OnRoomsListBox, self.rooms_listbox)
        sizer.Add(self.rooms_listbox, proportion=25, flag=wx.EXPAND)

        # Room area
        room_area_panel = wx.Panel(self)
        room_area_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)

        room_area = wx.ScrolledWindow(room_area_panel)
        room_area.SetScrollbars(32, 32, 1, 1)
        room_area_panel_sizer.Add(room_area, proportion=1, flag=wx.EXPAND)

        room_area_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.room_panel = RoomPanel(room_area)
        room_area_sizer.Add(self.room_panel, proportion=1, flag=wx.EXPAND)

        room_area.SetSizer(room_area_sizer)
        room_area_panel.SetSizer(room_area_panel_sizer)

        sizer.Add(room_area_panel, proportion=75, flag=wx.EXPAND)

        # TODO: Add room properties thing (like Visual Studio) to the right

        self.SetSizer(sizer)
        self.Refresh()

    def Refresh(self, *args, **kwargs):
        # List Box
        selection = self.rooms_listbox.GetSelection()
        room_names = [str(room.name) for room in self.game.rooms]
        self.rooms_listbox.Set(room_names)

        if (selection < self.rooms_listbox.GetCount() or
                selection == wx.NOT_FOUND):
            self.rooms_listbox.SetSelection(selection)

        super(GamePanel, self).Refresh(*args, **kwargs)

    def OnRoomsListBox(self, event):
        assert len(self.game.rooms) == self.rooms_listbox.GetCount()

        selection = event.GetSelection()
        if selection != self.room_selection or selection == wx.NOT_FOUND:
            self.room_selection = selection

            # TODO: Clear the panel
            self.room_panel.SetBackgroundColour(wx.NullColour)

            if selection != wx.NOT_FOUND:
                room = self.game.rooms[selection]

                # Room width
                warg = room.keyword_arguments.setdefault("width")

                if warg is None or warg.value == "None":
                    if "width" in self.game.game_kwargs:
                        warg = self.game.game_kwargs["width"]

                invalid = True
                willfix = True
                while invalid and willfix:
                    try:
                        width = stj.get_eval(self.game, warg)
                        invalid = False
                    except NameError:
                        message = ' '.join((
                            'The value of the keyword argument "width" of',
                            'room {0} could not be interpreted. Please enter',
                            'a new value for "width".')).format(selection)
                        dialog = wx.TextEntryDialog(
                            self, message, caption="Could not determine width",
                            defaultValue=warg)
                        button = dialog.ShowModal()

                        if button == wx.ID_OK:
                            warg = dialog.GetValue()
                        elif button == wx.ID_CANCEL:
                            willfix = False
                            width = 1

                if invalid:
                    self.rooms_listbox.SetSelection(wx.NOT_FOUND)
                    return

                # Room height
                harg = room.keyword_arguments.setdefault("height")

                if harg is None or harg.value == "None":
                    if "height" in self.game.game_kwargs:
                        harg = self.game.game_kwargs["height"]

                invalid = True
                willfix = True
                while invalid and willfix:
                    try:
                        height = stj.get_eval(self.game, harg)
                        invalid = False
                    except NameError:
                        message = ' '.join((
                            'The value of the keyword argument "height" of',
                            'room {0} could not be interpreted. Please enter',
                            'a new value for "height".')).format(selection)
                        dialog = wx.TextEntryDialog(
                            self, message,
                            caption="Could not determine height",
                            defaultValue=warg)
                        button = dialog.ShowModal()

                        if button == wx.ID_OK:
                            warg = dialog.GetValue()
                        elif button == wx.ID_CANCEL:
                            willfix = False
                            height = 1

                if invalid:
                    self.rooms_listbox.SetSelection(wx.NOT_FOUND)
                    return

                # Room background color
                self.room_panel.SetBackgroundColour(wx.Colour(0, 0, 0))

                bgarg = room.keyword_arguments.setdefault("background")

                if bgarg is not None:
                    for background in self.game.backgrounds:
                        if "ID" in background.kwargs:
                            ID = background.kwargs["ID"].value
                            if ID == bgarg.value and len(background.args) > 1:
                                c = background.args[1]
                                # TODO: Convert that to wxColour


class RoomPanel(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(RoomPanel, self).__init__(*args, **kwargs)


def create_room():
    pass


def main(*args):
    app = wx.PySimpleApp()
    Frame(None, title=MAIN_WINDOW_TITLE, size=MAIN_WINDOW_SIZE)
    app.MainLoop()


if __name__ == '__main__':
    main(*sys.argv)
