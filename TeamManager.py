#!/usr/bin/env python
import wx
import DataManager


class AddTeam(wx.Panel):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # Create sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.data_manager = DataManager.DataManager()

        self.school_name = wx.TextCtrl(self, -1,"School Name")
        self.school_name_abrv = wx.TextCtrl(self, -1,"Team Name Abbreviation")
        self.submit_btn = wx.Button(self, wx.ID_OK, label="Submit")
        self.sizer.Add(self.school_name, flag=wx.ALL| wx.EXPAND, border = 15)
        self.sizer.Add(self.school_name_abrv, flag=wx.ALL| wx.EXPAND, border = 15)
        self.sizer.Add(self.submit_btn, flag=wx.ALL| wx.EXPAND, border = 15)
        self.SetSizerAndFit(self.sizer)

        self.submit_btn.Bind(wx.EVT_BUTTON, self.add_team)

    def add_team(self,e):
        try:
            self.data_manager.create_team(self.school_name.GetValue(), self.school_name_abrv.GetValue())
            self.GetTopLevelParent().Close()
        except:
            pass



    def team_chosen(self, e):
        self.player_remove_combo.Clear()
        print('a')
        team_file_p = self.teams_dict[self.team_combo.GetStringSelection()] # Gets the selected team file
        chosen_team_roster = self.data_manager.load_roster_dict(team_file_p)
        self.player_remove_combo.AppendItems(list(chosen_team_roster.keys()))




class TeamManager(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Team Manager")

        panel = wx.Panel(self)
        #DataManager = DataManager.DataManager()
        nb = wx.Notebook(panel)

        #Create tab windows

        add_team_tab = AddTeam(nb)

        # tabs
        nb.AddPage(add_team_tab, "Add Team")
        #nb.AddPage(edit_team_tab, "Edit Team")

        # Sizer
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        panel.SetSizer(sizer)
