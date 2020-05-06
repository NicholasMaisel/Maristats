# Maristats
A Simple Basketball Stat Tracking Application.

Run MainMenu.py with Python3+.

To Create Teams, open the Team Manager.
To Add Players and add them to teams, use the player manager.

Creating Game Logs:
Once you have teams and players entered into the application you are ready to start logging games.
To Log a game:
  - Open up the Game Logger
  - Choose the home and away teams along with the game date at the top. Then click create log.
    + If the status bar (bottom of the window) says all is good, you are ready to begin logging stats.
  - Select the player, the court location by simply clicking on the court, and the shot type.
    + To toggle between a made and a missed shot click the "m" key on the keyboard.
  - Finally, once all of the shots and stats are entered for the game simply click the "Push to Log" Button.
    + This button will read the log file and update the individual player files with the stats entered.


To export stats:
  To use the export script, open up a command line interface in the project folder.\n
  use python to run export.py with the following argument options:
      - To get a csv of all player stats
        export.py -p -o [FILENAME]
      - To export all shots from all players
        export.py -s -o [FIELDNAME]

  The exported reports can be found in the DataExports folder.
