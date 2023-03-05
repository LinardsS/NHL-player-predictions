import requests
import sqlite3
from utils import establishDatabaseConnection, setAverageIfNull, getTeamStatsAverages
from os import path
import pandas as pd
import numpy as np


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
            url = "https://statsapi.web.nhl.com/api/v1/teams/{}/roster".format(team_id[0]) ## Team ID x returned in (x,) tuple form
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

def uploadNHLGameDataToDatabaseFromFile(db_name):
    conn = establishDatabaseConnection(db_name)
    avg_dict = getTeamStatsAverages()

    basepath = path.dirname(__file__)
    filename = "NHL 2022-23 Games.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df = pd.read_csv(filepath)
    #print(df)
    for index, row in df.iterrows():
        game_date = row["date"]
        game_id = row["game_id"]
        home_team = row["home_team"]
        away_team = row["away_team"]
        home_team_goals = row["home_team_goals"]
        away_team_goals = row["away_team_goals"]
        result = row['result']
        h_point_pct =  row['h_point%']
        h_point_pct = setAverageIfNull(h_point_pct, avg_dict['h_point%'])
        h_cf_pct =  row['h_cf%']
        h_cf_pct = setAverageIfNull(h_cf_pct, avg_dict['h_cf%'])
        h_ff_pct =  row['h_ff%']
        h_ff_pct = setAverageIfNull(h_ff_pct, avg_dict['h_ff%'])
        h_sf_pct =  row['h_sf%']
        h_sf_pct = setAverageIfNull(h_sf_pct, avg_dict['h_sf%'])
        h_gf_pct =  row['h_gf%']
        h_gf_pct = setAverageIfNull(h_gf_pct, avg_dict['h_gf%'])
        h_xgf_pct =  row['h_xgf%']
        h_xgf_pct = setAverageIfNull(h_xgf_pct, avg_dict['h_xgf%'])
        h_scf_pct =  row['h_scf%']
        h_scf_pct = setAverageIfNull(h_scf_pct, avg_dict['h_scf%'])
        h_scsf_pct =  row['h_scsf%']
        h_scsf_pct = setAverageIfNull(h_scsf_pct, avg_dict['h_scsf%'])
        h_scgf_pct =  row['h_scgf%']
        h_scgf_pct = setAverageIfNull(h_scgf_pct, avg_dict['h_scgf%'])
        h_scsh_pct =  row['h_scsh%']
        h_scsh_pct = setAverageIfNull(h_scsh_pct, avg_dict['h_scsh%'])
        h_scsv_pct =  row['h_scsv%']
        h_scsv_pct = setAverageIfNull(h_scsv_pct, avg_dict['h_scsv%'])
        h_hdsf_pct =  row['h_hdsf%']
        h_hdsf_pct = setAverageIfNull(h_hdsf_pct, avg_dict['h_hdsf%'])
        h_hdgf_pct =  row['h_hdgf%']
        h_hdgf_pct = setAverageIfNull(h_hdgf_pct, avg_dict['h_hdgf%'])
        h_hdsh_pct =  row['h_hdsh%']
        h_hdsh_pct = setAverageIfNull(h_hdsh_pct, avg_dict['h_hdsh%'])
        h_hdsv_pct =  row['h_hdsv%']
        h_hdsv_pct = setAverageIfNull(h_hdsv_pct, avg_dict['h_hdsv%'])
        h_mdsf_pct =  row['h_mdsf%']
        h_mdsf_pct = setAverageIfNull(h_mdsf_pct, avg_dict['h_mdsf%'])
        h_mdgf_pct =  row['h_mdgf%']
        h_mdgf_pct = setAverageIfNull(h_mdgf_pct, avg_dict['h_mdgf%'])
        h_mdsh_pct =  row['h_mdsh%']
        h_mdsh_pct = setAverageIfNull(h_mdsh_pct, avg_dict['h_mdsh%'])
        h_mdsv_pct =  row['h_mdsv%']
        h_mdsv_pct = setAverageIfNull(h_mdsv_pct, avg_dict['h_mdsv%'])
        h_ldsf_pct =  row['h_ldsf%']
        h_ldsf_pct = setAverageIfNull(h_ldsf_pct, avg_dict['h_ldsf%'])
        h_ldgf_pct =  row['h_ldgf%']
        h_ldgf_pct = setAverageIfNull(h_ldgf_pct, avg_dict['h_ldgf%'])
        h_ldsh_pct =  row['h_ldsh%']
        h_ldsh_pct = setAverageIfNull(h_ldsh_pct, avg_dict['h_ldsh%'])
        h_ldsv_pct =  row['h_ldsv%']
        h_ldsv_pct = setAverageIfNull(h_ldsv_pct, avg_dict['h_ldsv%'])
        h_sh_pct =  row['h_sh%']
        h_sh_pct = setAverageIfNull(h_sh_pct, avg_dict['h_sh%'])
        h_sv_pct =  row['h_sv%']
        h_sv_pct = setAverageIfNull(h_sv_pct, avg_dict['h_sv%'])
        h_PDO = row['h_PDO']
        h_PDO = setAverageIfNull(h_PDO, avg_dict['h_PDO'])
        #away team
        a_point_pct =  row['a_point%']
        a_point_pct = setAverageIfNull(a_point_pct, avg_dict['a_point%'])
        a_cf_pct =  row['a_cf%']
        a_cf_pct = setAverageIfNull(a_cf_pct, avg_dict['a_cf%'])
        a_ff_pct =  row['a_ff%']
        a_ff_pct = setAverageIfNull(a_ff_pct, avg_dict['a_ff%'])
        a_sf_pct =  row['a_sf%']
        a_sf_pct = setAverageIfNull(a_sf_pct, avg_dict['a_sf%'])
        a_gf_pct =  row['a_gf%']
        a_gf_pct = setAverageIfNull(a_gf_pct, avg_dict['a_gf%'])
        a_xgf_pct =  row['a_xgf%']
        a_xgf_pct = setAverageIfNull(a_xgf_pct, avg_dict['a_xgf%'])
        a_scf_pct =  row['a_scf%']
        a_scf_pct = setAverageIfNull(a_scf_pct, avg_dict['a_scf%'])
        a_scsf_pct =  row['a_scsf%']
        a_scsf_pct = setAverageIfNull(a_scsf_pct, avg_dict['a_scsf%'])
        a_scgf_pct =  row['a_scgf%']
        a_scgf_pct = setAverageIfNull(a_scgf_pct, avg_dict['a_scgf%'])
        a_scsh_pct =  row['a_scsh%']
        a_scsh_pct = setAverageIfNull(a_scsh_pct, avg_dict['a_scsh%'])
        a_scsv_pct =  row['a_scsv%']
        a_scsv_pct = setAverageIfNull(a_scsv_pct, avg_dict['a_scsv%'])
        a_hdsf_pct =  row['a_hdsf%']
        a_hdsf_pct = setAverageIfNull(a_hdsf_pct, avg_dict['a_hdsf%'])
        a_hdgf_pct =  row['a_hdgf%']
        a_hdgf_pct = setAverageIfNull(a_hdgf_pct, avg_dict['a_hdgf%'])
        a_hdsh_pct =  row['a_hdsh%']
        a_hdsh_pct = setAverageIfNull(a_hdsh_pct, avg_dict['a_hdsh%'])
        a_hdsv_pct =  row['a_hdsv%']
        a_hdsv_pct = setAverageIfNull(a_hdsv_pct, avg_dict['a_hdsv%'])
        a_mdsf_pct =  row['a_mdsf%']
        a_mdsf_pct = setAverageIfNull(a_mdsf_pct, avg_dict['a_mdsf%'])
        a_mdgf_pct =  row['a_mdgf%']
        a_mdgf_pct = setAverageIfNull(a_mdgf_pct, avg_dict['a_mdgf%'])
        a_mdsh_pct =  row['a_mdsh%']
        a_mdsh_pct = setAverageIfNull(a_mdsh_pct, avg_dict['a_mdsh%'])
        a_mdsv_pct =  row['a_mdsv%']
        a_mdsv_pct = setAverageIfNull(a_mdsv_pct, avg_dict['a_mdsv%'])
        a_ldsf_pct =  row['a_ldsf%']
        a_ldsf_pct = setAverageIfNull(a_ldsf_pct, avg_dict['a_ldsf%'])
        a_ldgf_pct =  row['a_ldgf%']
        a_ldgf_pct = setAverageIfNull(a_ldgf_pct, avg_dict['a_ldgf%'])
        a_ldsh_pct =  row['a_ldsh%']
        a_ldsh_pct = setAverageIfNull(a_ldsh_pct, avg_dict['a_ldsh%'])
        a_ldsv_pct =  row['a_ldsv%']
        a_ldsv_pct = setAverageIfNull(a_ldsv_pct, avg_dict['a_ldsv%'])
        a_sh_pct =  row['a_sh%']
        a_sh_pct = setAverageIfNull(a_sh_pct, avg_dict['a_sh%'])
        a_sv_pct =  row['a_sv%']
        a_sv_pct = setAverageIfNull(a_sv_pct, avg_dict['a_sv%'])
        a_PDO = row['a_PDO']
        a_PDO = setAverageIfNull(a_PDO, avg_dict['a_PDO'])

        game_tuple = (game_id, game_date, home_team, away_team, home_team_goals,
                      away_team_goals, result, h_point_pct, h_cf_pct,h_ff_pct,h_sf_pct,
                        h_gf_pct, h_xgf_pct, h_scf_pct,h_scsf_pct,h_scgf_pct,
                        h_scsh_pct,h_scsv_pct,h_hdsf_pct,h_hdgf_pct,h_hdsh_pct,
                        h_hdsv_pct,h_mdsf_pct,h_mdgf_pct,h_mdsh_pct,h_mdsv_pct,
                        h_ldsf_pct,h_ldgf_pct,h_ldsh_pct,h_ldsv_pct,h_sh_pct,h_sv_pct,
                        h_PDO,a_point_pct,a_cf_pct,a_ff_pct, a_sf_pct,a_gf_pct,a_xgf_pct
                        ,a_scf_pct,a_scsf_pct,a_scgf_pct,a_scsh_pct,a_scsv_pct,a_hdsf_pct,
                        a_hdgf_pct,a_hdsh_pct,a_hdsv_pct,a_mdsf_pct,a_mdgf_pct,a_mdsh_pct,
                        a_mdsv_pct,a_ldsf_pct,a_ldgf_pct,a_ldsh_pct,a_ldsv_pct, 
                        a_sh_pct,a_sv_pct,a_PDO)
        query = """INSERT INTO games(id,
            date,
            home_team,
            away_team,
            home_team_goals,
            away_team_goals,
            result,
            h_point_pct,
            h_cf_pct,
            h_ff_pct,
            h_sf_pct,
            h_gf_pct,
            h_xgf_pct,
            h_scf_pct,
            h_scsf_pct,
            h_scgf_pct,
            h_scsh_pct,
            h_scsv_pct,
            h_hdsf_pct,
            h_hdgf_pct,
            h_hdsh_pct,
            h_hdsv_pct,
            h_mdsf_pct,
            h_mdgf_pct,
            h_mdsh_pct,
            h_mdsv_pct,
            h_ldsf_pct,
            h_ldgf_pct,
            h_ldsh_pct,
            h_ldsv_pct,
            h_sh_pct,
            h_sv_pct,
            h_PDO, 
            a_point_pct,
            a_cf_pct,
            a_ff_pct,
            a_sf_pct,
            a_gf_pct,
            a_xgf_pct,
            a_scf_pct,
            a_scsf_pct,
            a_scgf_pct,
            a_scsh_pct,
            a_scsv_pct,
            a_hdsf_pct,
            a_hdgf_pct,
            a_hdsh_pct,
            a_hdsv_pct,
            a_mdsf_pct,
            a_mdgf_pct,
            a_mdsh_pct,
            a_mdsv_pct,
            a_ldsf_pct,
            a_ldgf_pct,
            a_ldsh_pct,
            a_ldsv_pct,
            a_sh_pct,
            a_sv_pct,
            a_PDO)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
        c = conn.cursor()
        c.execute(query, game_tuple)
    
    conn.commit()
    

        

#uploadNHLTeamsToDatabase("main.db")
#uploadNHLPlayersToDatabase("main.db")
uploadNHLGameDataToDatabaseFromFile("main.db")