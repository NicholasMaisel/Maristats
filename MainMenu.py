import wx
import TeamManager
import GameLogger
import PlayerManager

class MainMenu(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Maristats")

        panel = wx.Panel(self)

        team_btn = wx.Button(panel,-1, label="Team Manager")
        player_btn = wx.Button(panel,-1, label="Player Manager")
        game_btn = wx.Button(panel, -1, label="Create Game")


        team_btn.Bind(wx.EVT_BUTTON, self.open_team_manager)
        player_btn.Bind(wx.EVT_BUTTON, self.open_player_manager)
        game_btn.Bind(wx.EVT_BUTTON, self.open_game_logger)

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(team_btn, 1, wx.EXPAND)
        sizer.Add(player_btn, 1, wx.EXPAND)
        sizer.Add(game_btn, 1, wx.EXPAND)
        panel.SetSizerAndFit(sizer)


    def open_team_manager(self,e):
        team_manager = TeamManager.TeamManager()
        team_manager.Show()

    def open_player_manager(self, e):
        player_manager = PlayerManager.PlayerManager()
        player_manager.Show()

    def open_game_logger(self, e):
        game_logger = GameLogger.GameLogger(self,title="Game Log")
        game_logger.Show()


def main():
    app = wx.App()


    window = MainMenu()
    window.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()
