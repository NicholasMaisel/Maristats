import configparser
import json
import os
import csv
import shutil

class DataManager():
    def __init__(self):
        self.configfile = 'config.ini'

        self.config = self.read_config()
        self.player_path = self.config['default']['player_path']
        self.team_path = self.config['default']['team_path']
        self.team_directory = self.config['default']['team_directory']
        self.gamelogs_path = self.config['default']['gamelogs_path']
        self.player_template_path = self.config['default']['player_template_path']
        self.team_template_path = self.config['default']['team_template_path']
        self.game_template_path = self.config['default']['game_template_path']


    def load_players_dict(self):
        """ Reads PlayerData directory and returns a dictionary of player name
        to player file"""
        player_dict = {}
        for player_file in os.listdir(self.player_path):
            player_name = player_file.split(sep='.')[0]
            player_dict[player_name] = player_file
        return(player_dict)

    def read_config(self):
        """ Reads the config.ini file"""
        config = configparser.ConfigParser()
        config.read(self.configfile)
        return config

    def load_teams_dict(self):
        """ Opens up the team directory file to find a list of team names to team file locations
            Returns a dictionary of team name to file name
        """
        with open(self.team_directory, 'r') as f:
            teams_data = json.load(f)
            f.close()
        return(teams_data)

    def read_team_data(self,team_file):
        """ Reads team files and returns the team json object"""
        with open(self.team_path + team_file, 'r') as f:
            data = json.load(f)
            f.close()
        return(data)

    def read_player_data(self, player_file):
        """Reads an individual player data file"""

        #read a single players file
        with open(self.player_path + player_file, 'r') as f:
            data = json.load(f)
            f.close()
        return(data)

    def update_calculated_stats(self, player_data):
        """ Used in update_player_stats() to recalculate player statistics"""
        # Updates calculated statistics
        fga = player_data['FGA']
        fgm = player_data['FGM']
        pa3 = player_data['3FGA']
        pm3 = player_data['3FGM']
        try:
            player_data['FG%'] = fgm/fga
        except:
            player_data['FG%'] = "err: division by 0. FGA is 0"
        try:
            player_data['3FG%'] = pm3/pa3
        except:
            player_data['3FG%'] = "err: division by 0. 3FGA is 0"
        return(player_data)

    def update_player_attribute(self, player_file, updates):
        try:
            with open(self.player_path + player_file, 'r') as f:
                data = json.load(f)
                f.close()

            with open(self.player_path + player_file, 'w') as f:
                for update in updates:
                    self.update_calculated_stats(updates)
                    data[update] = updates[update]
                json.dump(data, f)
                f.close()
            return(True)
        except:
            return(False)

    def add_team_player(self, team_file, player_file):
        """ Adds a player file to the team_file's player_files list"""

        team_data = self.read_team_data(team_file)
        team_data['player_files'].append(player_file)
        self.update_team_data(team_file, team_data)

    def remove_team_player(self, team_file, player_file):
        team_data = self.read_team_data(team_file)
        print(team_data)
        team_data['player_files'].remove(player_file)
        print(team_data)
        self.update_team_data(team_file, team_data)

    def read_player_template(self):
        with open(self.player_template_path, 'r') as f:
            data = json.load(f)
            f.close()
        return(data)

    def create_player(self,player_name, attr = None, team_file = None):
        """ Creates a player file built from PlayerTemplate.json, with the name Player_name.json,
        returns False if file name already exists, and True if successfull"""
        player_first, player_last = player_name.split(" ")
        player_file = player_name.replace(" ", "") + '.json'
        if(os.path.exists(self.player_path + player_file)):
            return(False)
        else:
            with open(self.player_path + player_file, 'x') as new_file:
                with open(self.player_template_path, 'r') as template:
                    data = json.load(template)
                    data['player_name'] = player_first + ' ' + player_last
                    json.dump(data, new_file)
                    template.close()
                new_file.close()


        if attr: # If the user inputed new data, add the data, else use template
            try:
                self.update_player_attribute(player_file, attr)
            except:
                os.remove(player_file)

        if team_file: #if the user selected a team, add the player to the team
            self.add_team_player(team_file, player_file)

        return(True)

    def create_team(self, school_name, school_abbreviation):
        short_school_name = school_name.replace(" ", "")
        if(os.path.exists(self.team_path + short_school_name + '.json')):
            return(False)
        else:
            with open(self.team_path + short_school_name+ '.json', 'x') as new_file:
                with open(self.team_template_path, 'r') as template:
                    data = json.load(template)
                    data['school_name'] = school_name
                    data['school_abbreviation'] = school_abbreviation
                    json.dump(data, new_file)
                    new_file.close()
                    template.close()

            with open(self.team_directory, 'r') as f:
                data = json.load(f)
                print(data)
                f.close()
            with open(self.team_directory, 'w') as f:
                data[school_name] = short_school_name + '.json'
                json.dump(data, f)
                f.close()
            return(True)

    def update_team_data(self, team_file, team_updates):
        """ opens team_file and updates the team_file JSON with team_updates
         parameter changes"""
        data = self.read_team_data(team_file)
        with open(self.team_path + team_file, 'w') as f:
            for update in team_updates:
                data[update] = team_updates[update]
            json.dump(team_updates,f)
            f.close()
        return True

    def load_roster_dict(self, team_file):
        """ reads the team_file and returns a dictionary with player name to player file"""
        team_data = self.read_team_data(team_file)
        data = {}
        for player_file in team_data['player_files']:
            player_name = self.read_player_data(player_file)['player_name']
            data[player_name] = player_file

        return(data)

    def load_player_list(self, team_file):
        """ reads the team file and returns a list of all players' data
        in a single list"""

        # Returns a player object list

        team_data = self.read_team_data(team_file)
        data = []
        for player_file in team_data['player_files']:
            data.append(self.read_player_data(player_file))
        return(data)

    def create_log_file(self, file_name):
        """ Checks to see if a log file with that name already exists,
        if not it creates one"""
        if(os.path.exists(self.gamelogs_path + file_name + 'csv')):
            return(False)
        else:
            with open(self.gamelogs_path + file_name + '.csv', 'x') as f:
                f.close()
            shutil.copy(self.game_template_path, self.gamelogs_path + file_name + '.csv')

            return(True)

    def write_to_log(self, log_file, log_data):
        """ Writes lines of log data to the log_file"""
        with open(self.gamelogs_path + log_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(log_data)
            f.close()

    def push_log(self, log_file):
        player_dict = self.load_players_dict()
        with open(self.gamelogs_path + log_file) as f:
            data = csv.DictReader(f)
            for row in data:
                player_file = player_dict[row['player_name'].replace(" ", "")]
                player_data = self.read_player_data(player_file)
                row.pop('player_name')
                if row['stat'] in ['3PT', '2PT']:
                    shot = {'shot_type' : row['stat'],
                            'abs_x' : row.pop('abs_x'),
                            'abs_y' : row.pop('abs_y'),
                            'grid_x' : row.pop('grid_x'),
                            'grid_y' : row.pop('grid_y'),
                            'status' : row['status']}
                    player_data['shots'].append(shot)

                    if row['stat'] == '2PT':
                        player_data['FGA'] += 1
                        if row['status'] == 1:
                            player_data['FGM'] += 1
                    if row['stat'] == '3PT':
                        player_data['3FGA'] += 1
                        print(row['status'])
                        if row['status'] == 1:
                            player_data['3FGM'] += 1

                elif row['stat'] == 'FT':
                    shot = {'shot_type':'FT',
                            'status': row.pop('status')}
                    if row['status'] == 1:
                        player_data['FGM'] += 1

                    player_data['shots'].append(shot)
                    player_data[row['stat']] += 1

                else:
                    player_data[row['stat']] += 1

                self.update_player_attribute(player_file, player_data)
            f.close()





# TESTS
a = DataManager()
##print(a.read_team_data('SampleTeam.json'))
#print(a.load_player_list('SampleTeam.json'))
#print(a.read_player_data('NicholasMaisel.json'))
#a.update_player_stats('NicholasMaisel.json', {"3FGA":4, "3FGM":3})
#print(a.read_player_data('NicholasMaisel.json'))
#a.create_team('Joe School', 'JOE')
#print(a.load_roster_dict('MaristCollege.json'))
