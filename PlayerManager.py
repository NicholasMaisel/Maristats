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



class PlayerManager(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Player Manager", size =(300,700))

        panel = wx.Panel(self)
        nb = wx.Notebook(panel)

        #Create tab windows
        create_player_tab = CreatePlayer(nb)
        #edit_player_tab = EditPlayer(nb)

        # tabs
        nb.AddPage(create_player_tab, "Add Player")
        #nb.AddPage(edit_player_tab, "Edit Player")
        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, flag=wx.EXPAND)
        panel.SetSizer(sizer)
