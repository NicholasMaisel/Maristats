import wx
import wx.media
import wx.adv
import DataManager
import TeamManager


class GameLogger(wx.Frame):
    def __init__(self, parent, title):
        super(GameLogger, self).__init__(parent, title=title)
        self.SetSize((900,550))

        self.data_manager = DataManager.DataManager()

        self.InitUI()
        self.Centre()

        # Exact coordinates
        self.court_location_selected = 0,0
        # Gridified Coordinates
        self.court_grid_selected = (0,0)
        self.current_player_selected = ""
        self.current_log_file = ''
        self.shot_status = 0


    def InitUI(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("gray")
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.GridBagSizer(5,5)
        self.teams_list = self.load_teams()
        self.team_names = list(self.load_teams().keys())


    # Team Selection Elements
        self.team_selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.home_team_selector = wx.ComboBox(self.panel, -1, value=" ", choices=self.team_names)
        self.away_team_selector= wx.ComboBox(self.panel, -1, value=" ", choices=self.team_names)
        # Create Log file Button
        self.create_log_btn = wx.Button(self.panel, 125, label="Create Log")
        self.Bind(wx.EVT_BUTTON, self.create_log, self.create_log_btn)
        #Date Selection
        self.date_selector = wx.adv.DatePickerCtrl(self.panel, id=-1)

        # Add Elements to sizer
        self.team_selection_sizer.Add(self.home_team_selector, flag = wx.ALIGN_LEFT|wx.EXPAND)
        self.team_selection_sizer.Add(self.away_team_selector, flag = wx.ALIGN_CENTER|wx.EXPAND)
        self.team_selection_sizer.Add(self.date_selector, flag = wx.ALIGN_RIGHT|wx.EXPAND)
        self.team_selection_sizer.Add(self.create_log_btn, flag = wx.ALIGN_RIGHT|wx.EXPAND)

        # Event Bindings
        self.Bind(wx.EVT_COMBOBOX, self.select_team, self.home_team_selector)
        self.Bind(wx.EVT_COMBOBOX, self.select_team, self.away_team_selector)



        #Stat Box Options
        self.stat_sizer = wx.BoxSizer(wx.VERTICAL)
        self.stat_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.stats_radios = ["3PT", "2PT", "STL", "REB", "BLK","PF","FT"]
        self.stat_selector = wx.RadioBox(self.panel, label="Stat Selection", choices=self.stats_radios)
        self.submit_button = wx.Button(self.panel, 123, label="Submit")
        self.clear_button = wx.Button(self.panel, 124, label="clear")
        self.push_log_btn = wx.Button(self.panel, -1, label="Push Log Data")

        self.area_selected = wx.StaticText(self.panel, -1, label="0")
        self.area_label = wx.StaticText(self.panel, -1, label="Court Grid Selected")
        self.shot_status_label = wx.StaticText(self.panel, -1, label="Shot Made:")
        self.shot_status_value = wx.StaticText(self.panel, -1, label="Missed")
        self.stat_sizer.Add(self.stat_selector, flag=wx.EXPAND)
        self.stat_button_sizer.Add(self.submit_button,flag = wx.ALIGN_CENTER|wx.EXPAND)
        self.stat_button_sizer.Add(self.clear_button,flag = wx.EXPAND)
        self.stat_button_sizer.Add(self.push_log_btn,flag=wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.SubmitClicked, self.submit_button)
        self.Bind(wx.EVT_BUTTON, self.ClearClicked, self.clear_button)
        self.Bind(wx.EVT_BUTTON, self.push_clicked, self.push_log_btn)

    # Court and stats Box
        # Player Selection Lists
        self.home_player_list = wx.ListBox(self.panel, choices = [""])
        self.away_player_list = wx.ListBox(self.panel, choices = [""])
        self.input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.input_sizer.Add(self.home_player_list, flag=wx.EXPAND)
        self.input_sizer.Add(self.away_player_list, flag=wx.EXPAND)


        self.court_stat_sizer = wx.BoxSizer(wx.VERTICAL)
        self.court_image = wx.StaticBitmap(self.panel, -1,wx.BitmapFromImage(self.scale_bitmap()))
        self.court_image.Bind(wx.EVT_LEFT_DOWN, self.court_clicked, self.court_image)
        self.court_stat_sizer.Add(self.court_image, flag=wx.ALL, border = 10)
        self.court_stat_sizer.Add(self.area_label, flag=wx.EXPAND)
        self.court_stat_sizer.Add(self.area_selected, flag=wx.EXPAND)
        self.court_stat_sizer.Add(self.shot_status_label, flag=wx.EXPAND)
        self.court_stat_sizer.Add(self.shot_status_value, flag=wx.EXPAND)

        self.court_stat_sizer.Add(self.stat_sizer, flag=wx.ALL, border = 10)
        self.court_stat_sizer.Add(self.stat_button_sizer, flag=wx.ALL, border = 10)

        self.input_sizer.Add(self.court_stat_sizer, flag=wx.EXPAND)



        # Add Status status_bar
        self.status_bar = self.CreateStatusBar(1)
        self.status_bar.SetStatusText("Welcome to Maristat")

        self.main_sizer.Add(self.team_selection_sizer, flag=wx.ALL, border=10)
        self.main_sizer.Add(self.input_sizer, flag=wx.ALL, border = 10)





        # Bind Events
        self.Bind(wx.EVT_LISTBOX, self.OnPlayerSelection)
        self.Bind(wx.EVT_RADIOBUTTON, self.StatSelectionFunction)

        #Shot Status keys
        self.Bind(wx.EVT_CHAR_HOOK, self.shot_status_toggle)
        #self.Bind(wx.EVT_KEY_UP, self.shot_status_toggle)

        self.panel.SetSizerAndFit(self.main_sizer)

    def scale_bitmap(self):
        image = wx.ImageFromBitmap(wx.Bitmap('court.jpg', wx.BITMAP_TYPE_ANY))
        h = image.GetHeight()
        w = image.GetWidth()
        width, height = self.Size
        scale_factor = 2.6
        width, height = int(width/scale_factor), int(height/scale_factor)
        print(width)
        if w > h:
            new_w = width
            new_h = width*(h/w)
        else:
            new_w = width*(w/h)
            new_h = height

        image = image.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)

        return image

    def StatSelectionFunction(self, e):
        selection = e.GetEventObject().GetLabel()
        pass

    def court_clicked(self, e):
        img_w, img_h = self.court_image.GetSize()
        x, y = e.GetPosition()
        x, y = x/img_w, y/img_h
        self.court_location_selected = x,y
        self.court_grid_selected = (round(x*10), round(y*10))
        self.area_selected.SetLabel(str(self.court_grid_selected))
        print(x,y)

    def select_team(self,e):
        if(e.GetEventObject() == self.home_team_selector):
            team_selected = self.home_team_selector.GetValue()
            team_file = self.teams_list[team_selected]
            print(team_file)
            players = []
            for player in self.data_manager.load_player_list(team_file):
                players.append(player['player_name'])
            self.home_player_list.InsertItems(players,0)

        else:
            team_selected = self.away_team_selector.GetValue()
            team_file = self.teams_list[team_selected]
            players = []
            for player in self.data_manager.load_player_list(team_file):
                players.append(player['player_name'])
            self.away_player_list.InsertItems(players,0)

    def create_log(self,e):
        selected_home = self.home_team_selector.GetStringSelection()
        selected_away = self.away_team_selector.GetStringSelection()
        home_abv = self.data_manager.read_team_data(self.teams_list[selected_home])['school_abbreviation']
        away_abv = self.data_manager.read_team_data(self.teams_list[selected_away])['school_abbreviation']

        selected_year = str(self.date_selector.GetValue().year)
        selected_day = str(self.date_selector.GetValue().day)
        selected_month = str(self.date_selector.GetValue().month)
        log_file_name = home_abv + away_abv + selected_day + selected_month + selected_year
        # Check if file exists
        if(self.data_manager.create_log_file(log_file_name)):
            self.status_bar.SetStatusText("[*] Log File Created. Begin.")
        else:
            self.status_bar.SetStatusText("[*] Error, log file with same name exists!!!!")

        self.current_log_file = log_file_name + '.csv'

    def ClearClicked(self, e):
        a = TeamManager.TeamManager()
        #a = testing.MainFrame()
        a.Show()
    # Only allow one team/player to be selected at once
    def OnPlayerSelection(self,e):
        if(e.GetEventObject() == self.home_player_list):
            for x in range(0,self.away_player_list.GetCount()):
                self.away_player_list.Deselect(x)
            selected_index = self.home_player_list.GetSelection()
            player_selected = self.home_player_list.GetString(selected_index)

        elif(e.GetEventObject() == self.away_player_list):
            for x in range(0,self.home_player_list.GetCount()):
                self.home_player_list.Deselect(x)
            selected_index = self.away_player_list.GetSelection()
            player_selected = self.away_player_list.GetString(selected_index)

        self.current_player_selected = player_selected
        return(player_selected)

    def SubmitClicked(self, e):
        if (self.current_player_selected == ''):
            self.status_bar.SetStatusText("[*] You have not selected a player!")
            return None

        if(self.stat_selector.GetSelection() != "NOT_FOUND"):
            stat_selected = self.stat_selector.GetSelection()
            stat = self.stat_selector.GetString(stat_selected)
            to_log = [self.current_player_selected,
                    self.court_location_selected[0],
                    self.court_location_selected[1],
                    self.court_grid_selected[0],
                    self.court_grid_selected[1],
                    stat,
                    self.shot_status]

            self.data_manager.write_to_log(self.current_log_file, to_log)

    def push_clicked(self,e):
        print(self.current_log_file)
        self.data_manager.push_log(self.current_log_file)

    def load_teams(self):
        teams = self.data_manager.load_teams_dict()
        return(teams)

    def shot_status_toggle(self,e):

        shot_status_vals = {0:"Missed", 1:"Made"}
        if e.GetKeyCode() == 77:
            self.shot_status = 1 - self.shot_status
            self.shot_status_value.SetLabel(shot_status_vals[self.shot_status])

        e.Skip()
