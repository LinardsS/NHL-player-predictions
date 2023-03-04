import requests
import sqlite3


def uploadNHLTeamsToDatabase(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)

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

#uploadNHLTeamsToDatabase("main.db")