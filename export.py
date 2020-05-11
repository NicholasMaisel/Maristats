import argparse
import json
import csv
import DataManager

def main():
    dm = DataManager.DataManager()
    text = "This is a tool to export data from the Maristats applicaiton."
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("-p", help="""Export player stats""", action="store_true")
    parser.add_argument("-s", help="Export Shots file", action='store_true')
    parser.add_argument("-o", "--output", help="file name of export")

    args = parser.parse_args()
    print(args)
    if args.p:
        stats_list = []
        pd = dm.load_players_dict()
        for player in pd:
            if player != "":
                data = dict(dm.read_player_data(pd[player]))
                data.pop('shots')
                stats_list.append(data)

        if args.output:
            file_name = 'DataExports/'+args.output + '.csv'
        else:
            file_name = 'DataExports/' + 'playerStats.csv'
        with open(file_name, 'w') as f:
            writer = csv.DictWriter(f, stats_list[0])
            writer.writeheader()
            for i in stats_list:
                writer.writerow(i)
            f.close()


    elif args.s:
        stats_list = []
        pd = dm.load_players_dict()
        print(pd)
        for player in pd:
            if player != "":
                print(dm.read_player_data(pd[player]))
                data = dict(dm.read_player_data(pd[player])).pop('shots')
                for shot in data:
                    shot['player'] = player
                    stats_list.append(shot)

        if args.output:
            file_name = 'DataExports/'+ args.output + '.csv'
        else:
            file_name = 'DataExports/' + 'playerStats.csv'

        with open('DataExports/'+ args.output + '.csv', 'w') as f:
            print(stats_list)
            writer = csv.DictWriter(f, stats_list[0])
            writer.writeheader()
            for i in stats_list:
                writer.writerow(i)
            f.close()



if __name__ == "__main__":
    main()
