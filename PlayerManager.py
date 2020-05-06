import wx
import wx.grid
import DataManager




class CreatePlayer(wx.Panel):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # Create sizer
        self.data_manager = DataManager.DataManager()
        self.teams_dict = self.data_manager.load_teams_dict()
        self.teams_list = list(self.teams_dict.keys())

        self.init_ui()


    def init_ui(self):
        #Get stats template and create inputs
        self.info_grid = wx.GridSizer(cols=2, gap=wx.Size(5,5))
        self.input_widgets = []
        data_template = self.data_manager.read_player_template()
        for data_point in {k:v for k,v in data_template.items() if k not in ['shots']}:
            if data_point == "school":
                self.info_grid.Add(wx.StaticText(self, label = data_point))
                element = wx.ComboBox(self, value = " ", choices = self.teams_list, name = "school")
                self.info_grid.Add(element, flag = wx.EXPAND)
                self.input_widgets.append(element)

            else:
                self.info_grid.Add(wx.StaticText(self, label = data_point))
                element = wx.TextCtrl(self,value = str(data_template[data_point]), name = data_point)
                self.info_grid.Add(element, flag = wx.EXPAND)
                self.input_widgets.append(element)
        #Buttons
        create_btn = wx.Button(self, -1, label="Create Player")
        cancel_btn = wx.Button(self, -1, label="Cancel")
        create_btn.Bind(wx.EVT_BUTTON, self.create_player)

        submission_sizer = wx.BoxSizer(wx.HORIZONTAL)
        submission_sizer.Add(create_btn, flag=wx.EXPAND)
        submission_sizer.Add(cancel_btn, flag=wx.EXPAND)

        #Main Sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.info_grid)
        self.main_sizer.Add(submission_sizer, flag=wx.EXPAND)
        self.SetSizerAndFit(self.main_sizer)


    def create_player(self, e):
        player_data = {}
        for input in self.input_widgets:
            try: # if TextCrtl
                try: # If value is numeric
                    player_data[input.Name] = float(input.GetValue())
                except:
                    player_data[input.Name] = input.GetValue()

            except:
                #if ComboBox, the GetStringSelection() for values
                    player_data[input.Name] == input.GetStringSelection()
        try:

            if ("school" in list(player_data.keys())):
                team_file = self.teams_dict[player_data["school"]]
                self.data_manager.create_player(player_data['player_name'], player_data, team_file)
            else:
                self.data_manager.create_player(player_data['player_name'], player_data)

            self.GetTopLevelParent().Close()


        except:
            wx.MessageBox("Please ensure player name is formatted 'First Last' and all values are inputted.",
             "Could Not Create Player" ,wx.OK | wx.ICON_ERROR)


class ManagePlayer(wx.Panel):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # Create sizer
        self.data_manager = DataManager.DataManager()
        self.teams_dict = self.data_manager.load_teams_dict()
        self.teams_list = list(self.teams_dict.keys())
        self.player_dict = self.data_manager.load_players_dict()
        self.players_list = list(self.player_dict.keys())
        self.original_school = ""

        self.init_ui()

    def init_ui(self):
        #Get stats template and create inputs
        self.info_grid = wx.GridSizer(cols=2, gap=wx.Size(5,5))
        self.input_widgets = []
        data_template = self.data_manager.read_player_template()

        #Add player selector
        player_label = wx.StaticText(self, label="select Player")
        self.player_combo = wx.ComboBox(self, value = " ", choices = self.players_list)
        self.info_grid.Add(player_label, flag=wx.EXPAND)
        self.info_grid.Add(self.player_combo, flag=wx.EXPAND)
        self.player_combo.Bind(wx.EVT_COMBOBOX, self.load_stats)

        for data_point in {k:v for k,v in data_template.items() if k not in ['player_name','shots']}:
            if data_point == "school":
                self.info_grid.Add(wx.StaticText(self, label = data_point))
                element = wx.ComboBox(self, value = " ", choices = self.teams_list, name = "school")
                self.info_grid.Add(element, flag = wx.EXPAND)
                self.input_widgets.append(element)

            else:
                self.info_grid.Add(wx.StaticText(self, label = data_point))
                element = wx.TextCtrl(self,value = str(data_template[data_point]), name = data_point)
                self.info_grid.Add(element, flag = wx.EXPAND)
                self.input_widgets.append(element)
        #Buttons
        confirm_btn = wx.Button(self, -1, label="Confirm Changes")
        cancel_btn = wx.Button(self, -1, label="Cancel")
        confirm_btn.Bind(wx.EVT_BUTTON, self.update_player)

        submission_sizer = wx.BoxSizer(wx.HORIZONTAL)
        submission_sizer.Add(confirm_btn, flag=wx.EXPAND)
        submission_sizer.Add(cancel_btn, flag=wx.EXPAND)

        #Main Sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.info_grid)
        self.main_sizer.Add(submission_sizer, flag=wx.EXPAND)
        self.SetSizerAndFit(self.main_sizer)


    def load_stats(self, e):
        player_file = self.player_dict[self.player_combo.GetStringSelection()]
        player_data = self.data_manager.read_player_data(player_file)
        self.original_school=player_data['school']
        for input in self.input_widgets:
            input.Value = str(player_data[input.Name])

    def update_player(self,e):
        player_data = {}
        player_file = self.player_dict[self.player_combo.GetStringSelection()]
        player_data = self.data_manager.read_player_data(player_file)
        for input in self.input_widgets:
            try: # if TextCrtl
                try: # If value is numeric
                    player_data[input.Name] = float(input.GetValue())
                except:
                    player_data[input.Name] = input.GetValue()

            except:
                #if ComboBox, the GetStringSelection() for values
                    player_data[input.Name] == input.GetStringSelection()
        try:
            if self.original_school != player_data['school']:
                #remove player from old team
                self.data_manager.remove_team_player(self.teams_dict[self.original_school], player_file)
                #add player to new team_data
                self.data_manager.add_team_player(self.teams_dict[player_data['school']], player_file)
                self.data_manager.update_player_attribute(player_file, player_data)



        except:
            wx.MessageBox("Please ensure player name is formatted 'First Last' and all values are inputted.",
             "Could Not Create Player" ,wx.OK | wx.ICON_ERROR)




class PlayerManager(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Player Manager", size =(300,700))

        panel = wx.Panel(self)
        nb = wx.Notebook(panel)

        #Create tab windows
        create_player_tab = CreatePlayer(nb)
        manage_player_tab = ManagePlayer(nb)

        # tabs
        nb.AddPage(create_player_tab, "Add Player")
        nb.AddPage(manage_player_tab, "Manage Player")
        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, flag=wx.EXPAND)
        panel.SetSizer(sizer)
