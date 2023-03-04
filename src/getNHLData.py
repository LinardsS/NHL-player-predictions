import requests
import sqlite3
from utils import establishDatabaseConnection


def uploadNHLTeamsToDatabase(db_name):
    conn = establishDatabaseConnection(db_name)

    url = "https://statsapi.web.nhl.com/api/v1/teams"
    request = requests.get(url)
    requestJson = request.json()
    for team in requestJson['teams']:
        team_name = team['name']
        team_id = team['id']
        abbreviation = team['abbreviation']
        conference_id = team['conference']['id']
        division_id = team['division']['id']
        team_tuple = (team_name, team_id, abbreviation, conference_id, division_id)

        query = """INSERT INTO teams(name, id, abbreviation, conference_id, division_id)
                     VALUES(?, ?, ?, ?, ?) """
        c = conn.cursor()
        c.execute(query, team_tuple)
        conn.commit()


def uploadNHLPlayersToDatabase(db_name):
    conn = establishDatabaseConnection(db_name)

    # Get list of team IDs
    c = conn.cursor()
    query = "SELECT id from teams"
    c.execute(query)
    team_list = c.fetchall()
    if team_list is not None:
        for team_id in team_list:
            url = "https://statsapi.web.nhl.com/api/v1/teams/{}/roster".format(team_id[0])
            print("URL: " + url)
            request = requests.get(url)
            requestJson = request.json()
            #print(requestJson)
            for player in requestJson['roster']:
                player_name = player['person']['fullName']
                player_id = player['person']['id']
                position = player['position']['code']
                player_team_id = team_id[0]
                player_tuple = (player_name, player_id, position, player_team_id)

                query = """INSERT INTO players(name, id, position, team_id)
                            VALUES(?, ?, ?, ?) """
                c = conn.cursor()
                c.execute(query, player_tuple)
                conn.commit()
#uploadNHLTeamsToDatabase("main.db")
#uploadNHLPlayersToDatabase("main.db")