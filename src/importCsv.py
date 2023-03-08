import csv
from os import path
from datetime import date, datetime, timedelta

def getPlayerStats(date, player):
    basepath = path.dirname(__file__)
    FILE_SUFFIX = ' - Player Season Totals'
    if date is None:
        today = date.today()
        date = today.strftime("%Y-%m-%d")
    filename = date + FILE_SUFFIX + '.csv'
    filepath = path.abspath(path.join(basepath, "..", "data", filename))

    if not path.exists(filepath):
        print("Player stats not found for ",date, player)
        return {}

    with open(filepath) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        return_dict = {}
        for row in csv_reader:
            if row['Player'] == player:
                # Add check for players with identical names(Sebastian Aho etc)
                return_dict['player'] = row
        return return_dict

def getTeamsStats(date, home_team, away_team, format = None, backdate = None):
    basepath = path.dirname(__file__)
    FILE_SUFFIX = ' - Team Season Totals'
    if date is None:
        today = date.today()
        date = today.strftime("%Y-%m-%d")
    if backdate is True:
        date = datetime.strptime(date, '%Y-%m-%d')
        date = date-timedelta(days=2)
        date = date.strftime('%Y-%m-%d')
    filename = str(date) + FILE_SUFFIX + '.csv'
    filepath = path.abspath(path.join(basepath, "..", "data", filename))

    if not path.exists(filepath):
        print("Team stats not found for ",date, home_team,away_team)
        return {}

    with open(filepath) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        return_dict = {}
        for row in csv_reader:
            if row['Team'] == home_team:
                return_dict['home_team'] = row
            if row['Team'] == away_team:
                return_dict['away_team'] = row
        return return_dict