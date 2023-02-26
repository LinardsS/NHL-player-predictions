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
