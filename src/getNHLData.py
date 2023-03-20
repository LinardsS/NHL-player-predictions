import requests
import sqlite3
from utils import establishDatabaseConnection, setAverageIfNull, getTeamStatsAverages, getTodaysDate, getYesterdaysDate
from os import path
import pandas as pd
import numpy as np
from downloadCsv import daterange
from datetime import date, timedelta


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
    
def uploadNHLPlayerGameDataToDatabase(db_name, from_date = None, to_date = None):    
    # Retrieve all IDs for games that have happened so far
    conn = establishDatabaseConnection(db_name)
    c = conn.cursor()
    if from_date is None:
        from_date= getYesterdaysDate(format = "%Y-%m-%d")
    if to_date is None:
        to_date= getTodaysDate(format = "%Y-%m-%d")

    c.execute("SELECT id, date FROM games where date >= (?) and date < (?) ", (from_date,to_date))
    game_list = c.fetchall()
    print(game_list)
    
    for game in game_list:
        url = "https://statsapi.web.nhl.com/api/v1/game/{}/boxscore".format(game[0])
        print("URL: " + url)
        request = requests.get(url)
        requestJson = request.json()
        home_team = requestJson['teams']['home']['team']['name']
        away_team = requestJson['teams']['away']['team']['name']
        home_team_id = requestJson['teams']['home']['team']['id']
        away_team_id = requestJson['teams']['away']['team']['id']
        # Get list of players that played in the match, then loop through their stats
        
        home_team_goalies = requestJson['teams']['home']['goalies']
        for h_goalie_id in home_team_goalies:
            h_goalie = requestJson['teams']['home']['players']['ID' + str(h_goalie_id)]
            h_goalie_name = h_goalie['person']['fullName']

            h_goalie_stats = h_goalie['stats']['goalieStats']
            h_goalie_toi = h_goalie_stats['timeOnIce']
            h_goalie_goals = h_goalie_stats['goals']     # :)
            h_goalie_assists = h_goalie_stats['assists'] # :)
            h_goalie_pim = h_goalie_stats['pim']
            h_goalie_shots = h_goalie_stats['shots']
            h_goalie_saves = h_goalie_stats['saves']
            h_goalie_pp_saves = h_goalie_stats['powerPlaySaves']
            h_goalie_sh_saves = h_goalie_stats['shortHandedSaves']
            h_goalie_even_saves = h_goalie_stats['evenSaves']
            h_goalie_pp_sa = h_goalie_stats['powerPlayShotsAgainst']
            h_goalie_sh_sa = h_goalie_stats['shortHandedShotsAgainst']
            h_goalie_even_sa = h_goalie_stats['evenShotsAgainst']
            h_goalie_decision = h_goalie_stats['decision']
            if "savePercentage" in h_goalie_stats:
                h_goalie_save_pct = h_goalie_stats['savePercentage']
            else:
                h_goalie_save_pct = None
            if "powerPlaySavePercentage" in h_goalie_stats:
                h_goalie_pp_save_pct = h_goalie_stats['powerPlaySavePercentage']
            else:
                h_goalie_pp_save_pct = None
            if "shortHandedSavePercentage" in h_goalie_stats:
                h_goalie_sh_save_pct = h_goalie_stats['shortHandedSavePercentage']
            else:
                h_goalie_sh_save_pct = None
            if "evenStrengthSavePercentage" in h_goalie_stats:
                h_goalie_even_save_pct = h_goalie_stats['evenStrengthSavePercentage']
            else:
                h_goalie_even_save_pct = None

            h_goalie_tuple = (h_goalie_id, h_goalie_name, game[0], game[1], # game[0] - game_id, game[1] - date
                              home_team, away_team, away_team_id, h_goalie_toi, h_goalie_goals, h_goalie_assists,
                              h_goalie_pim,h_goalie_shots, h_goalie_saves, h_goalie_save_pct, h_goalie_pp_saves,
                              h_goalie_pp_sa, h_goalie_even_saves, h_goalie_even_sa,h_goalie_sh_saves, h_goalie_sh_sa,
                              h_goalie_even_save_pct, h_goalie_pp_save_pct,h_goalie_sh_save_pct, h_goalie_decision)
            query = """INSERT INTO goalie_game_data(
            player_id,
            player_name,
            game_id,
            date,
            home_team,
            away_team,
            opponent_team_id,
            time_on_ice,
            goals,
            assists,
            penalty_minutes,
            shots_faced,
            saves,
            save_pct,
            power_play_saves,
            power_play_shots_faced,
            even_saves,
            even_shots_faced,
            short_handed_saves,
            short_handed_shots_faced,
            even_sv_pct,
            pp_sv_pct,
            sh_sv_pct,
            decision
            )
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            c.execute(query, h_goalie_tuple)


        away_team_goalies = requestJson['teams']['away']['goalies']
        for a_goalie_id in away_team_goalies:
            a_goalie = requestJson['teams']['away']['players']['ID' + str(a_goalie_id)]
            a_goalie_name = a_goalie['person']['fullName']

            a_goalie_stats = a_goalie['stats']['goalieStats']
            a_goalie_toi = a_goalie_stats['timeOnIce']
            a_goalie_goals = a_goalie_stats['goals']     # :)
            a_goalie_assists = a_goalie_stats['assists'] # :)
            a_goalie_pim = a_goalie_stats['pim']
            a_goalie_shots = a_goalie_stats['shots']
            a_goalie_saves = a_goalie_stats['saves']
            a_goalie_pp_saves = a_goalie_stats['powerPlaySaves']
            a_goalie_sh_saves = a_goalie_stats['shortHandedSaves']
            a_goalie_even_saves = a_goalie_stats['evenSaves']
            a_goalie_pp_sa = a_goalie_stats['powerPlayShotsAgainst']
            a_goalie_sh_sa = a_goalie_stats['shortHandedShotsAgainst']
            a_goalie_even_sa = a_goalie_stats['evenShotsAgainst']
            a_goalie_decision = a_goalie_stats['decision']
            if "savePercentage" in a_goalie_stats:
                a_goalie_save_pct = a_goalie_stats['savePercentage']
            else:
                a_goalie_save_pct = None
            if "powerPlaySavePercentage" in a_goalie_stats:
                a_goalie_pp_save_pct = a_goalie_stats['powerPlaySavePercentage']
            else:
                a_goalie_pp_save_pct = None
            if "shortHandedSavePercentage" in a_goalie_stats:
                a_goalie_sh_save_pct = a_goalie_stats['shortHandedSavePercentage']
            else:
                a_goalie_sh_save_pct = None
            if "evenStrengthSavePercentage" in a_goalie_stats:
                a_goalie_even_save_pct = a_goalie_stats['evenStrengthSavePercentage']
            else:
                a_goalie_even_save_pct = None

            a_goalie_tuple = (a_goalie_id, a_goalie_name, game[0], game[1], # game[0] - game_id, game[1] - date
                              home_team, away_team, home_team_id, a_goalie_toi, a_goalie_goals, a_goalie_assists,
                              a_goalie_pim,a_goalie_shots, a_goalie_saves, a_goalie_save_pct, a_goalie_pp_saves,
                              a_goalie_pp_sa, a_goalie_even_saves, a_goalie_even_sa,a_goalie_sh_saves, a_goalie_sh_sa,
                              a_goalie_even_save_pct, a_goalie_pp_save_pct,a_goalie_sh_save_pct, a_goalie_decision)
            query = """INSERT INTO goalie_game_data(
            player_id,
            player_name,
            game_id,
            date,
            home_team,
            away_team,
            opponent_team_id,
            time_on_ice,
            goals,
            assists,
            penalty_minutes,
            shots_faced,
            saves,
            save_pct,
            power_play_saves,
            power_play_shots_faced,
            even_saves,
            even_shots_faced,
            short_handed_saves,
            short_handed_shots_faced,
            even_sv_pct,
            pp_sv_pct,
            sh_sv_pct,
            decision
            )
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            c.execute(query, a_goalie_tuple)

        
        home_team_skaters = requestJson['teams']['home']['skaters']
        home_team_scratches = requestJson['teams']['away']['scratches'] # Players that didn't play
        home_team_skaters = [i for i in home_team_skaters if i not in home_team_scratches]
        for h_skater_id in home_team_skaters:
            h_skater = requestJson['teams']['home']['players']['ID' + str(h_skater_id)]
            h_skater_name = h_skater['person']['fullName']

            h_skater_stats = h_skater['stats']
            if 'skaterStats' in h_skater_stats:
                h_skater_stats = h_skater_stats['skaterStats']
            else:
                continue
            h_skater_toi = h_skater_stats['timeOnIce']
            h_skater_goals = h_skater_stats['goals']
            h_skater_assists = h_skater_stats['assists']
            h_skater_pim = h_skater_stats['penaltyMinutes']
            h_skater_shots = h_skater_stats['shots']
            h_skater_hits = h_skater_stats['hits']
            h_skater_pp_goals = h_skater_stats['powerPlayGoals']
            h_skater_pp_assists = h_skater_stats['powerPlayAssists']
            h_skater_sh_goals = h_skater_stats['shortHandedGoals']
            h_skater_sh_assists = h_skater_stats['shortHandedAssists']
            if "faceOffPct" in h_skater_stats:
                h_skater_faceoff_pct = h_skater_stats['faceOffPct']
            else:
                h_skater_faceoff_pct = None
            h_skater_faceoff_wins = h_skater_stats['faceOffWins']
            h_skater_faceoffs_taken = h_skater_stats['faceoffTaken'] # mind the lowercase 'o'
            h_skater_takeaways = h_skater_stats['takeaways']
            h_skater_giveaways = h_skater_stats['giveaways']
            h_skater_blocked_shots = h_skater_stats['blocked']
            h_skater_plus_minus = h_skater_stats['plusMinus']
            h_skater_ev_toi = h_skater_stats['evenTimeOnIce']
            h_skater_pp_toi = h_skater_stats['powerPlayTimeOnIce']
            h_skater_sh_toi = h_skater_stats['shortHandedTimeOnIce']

            h_skater_tuple = (h_skater_id, h_skater_name, game[0], game[1], home_team, away_team,
                              away_team_id, h_skater_toi, h_skater_goals,h_skater_assists,h_skater_shots,
                              h_skater_hits,h_skater_pp_goals,h_skater_pp_assists, h_skater_pim, 
                              h_skater_faceoff_pct,h_skater_faceoff_wins,h_skater_faceoffs_taken, 
                              h_skater_takeaways, h_skater_giveaways, h_skater_sh_goals, h_skater_sh_assists,
                              h_skater_blocked_shots, h_skater_plus_minus, h_skater_ev_toi,
                              h_skater_pp_toi, h_skater_sh_toi)
            query = """INSERT INTO skater_game_data(
            player_id,
            player_name,
            game_id,
            date,
            home_team,
            away_team,
            opponent_team_id,
            time_on_ice,
            goals,
            assists,
            shots,
            hits,
            power_play_goals,
            power_play_assists,
            penalty_minutes,
            face_off_pct,
            face_off_wins,
            face_offs_taken,
            takeaways,
            giveaways,
            short_handed_goals,
            short_handed_assists,
            blocked_shots,
            plus_minus,
            even_toi,
            pp_toi,
            sh_toi
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            c.execute(query, h_skater_tuple)

        away_team_skaters = requestJson['teams']['away']['skaters']
        away_team_scratches = requestJson['teams']['away']['scratches'] # Players that didn't play
        away_team_skaters = [i for i in away_team_skaters if i not in away_team_scratches]
        for a_skater_id in away_team_skaters:
            a_skater = requestJson['teams']['away']['players']['ID' + str(a_skater_id)]
            a_skater_name = a_skater['person']['fullName']

            a_skater_stats = a_skater['stats']
            if 'skaterStats' in a_skater_stats:
                a_skater_stats = a_skater_stats['skaterStats']
            else:
                continue
            a_skater_toi = a_skater_stats['timeOnIce']
            a_skater_goals = a_skater_stats['goals']
            a_skater_assists = a_skater_stats['assists']
            a_skater_pim = a_skater_stats['penaltyMinutes']
            a_skater_shots = a_skater_stats['shots']
            a_skater_hits = a_skater_stats['hits']
            a_skater_pp_goals = a_skater_stats['powerPlayGoals']
            a_skater_pp_assists = a_skater_stats['powerPlayAssists']
            a_skater_sh_goals = a_skater_stats['shortHandedGoals']
            a_skater_sh_assists = a_skater_stats['shortHandedAssists']
            if "faceOffPct" in a_skater_stats:
                a_skater_faceoff_pct = a_skater_stats['faceOffPct']
            else:
                a_skater_faceoff_pct = None
            a_skater_faceoff_wins = a_skater_stats['faceOffWins']
            a_skater_faceoffs_taken = a_skater_stats['faceoffTaken'] # mind the lowercase 'o'
            a_skater_takeaways = a_skater_stats['takeaways']
            a_skater_giveaways = a_skater_stats['giveaways']
            a_skater_blocked_shots = a_skater_stats['blocked']
            a_skater_plus_minus = a_skater_stats['plusMinus']
            a_skater_ev_toi = a_skater_stats['evenTimeOnIce']
            a_skater_pp_toi = a_skater_stats['powerPlayTimeOnIce']
            a_skater_sh_toi = a_skater_stats['shortHandedTimeOnIce']

            a_skater_tuple = (a_skater_id, a_skater_name, game[0], game[1], home_team, away_team,
                              home_team_id, a_skater_toi, a_skater_goals,a_skater_assists,a_skater_shots,
                              a_skater_hits,a_skater_pp_goals,a_skater_pp_assists, a_skater_pim, 
                              a_skater_faceoff_pct,a_skater_faceoff_wins,a_skater_faceoffs_taken, 
                              a_skater_takeaways, a_skater_giveaways, a_skater_sh_goals, a_skater_sh_assists,
                              a_skater_blocked_shots, a_skater_plus_minus, a_skater_ev_toi,
                              a_skater_pp_toi, a_skater_sh_toi)
            query = """INSERT INTO skater_game_data(
            player_id,
            player_name,
            game_id,
            date,
            home_team,
            away_team,
            opponent_team_id,
            time_on_ice,
            goals,
            assists,
            shots,
            hits,
            power_play_goals,
            power_play_assists,
            penalty_minutes,
            face_off_pct,
            face_off_wins,
            face_offs_taken,
            takeaways,
            giveaways,
            short_handed_goals,
            short_handed_assists,
            blocked_shots,
            plus_minus,
            even_toi,
            pp_toi,
            sh_toi
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            c.execute(query, a_skater_tuple)
    
    #Write changes
    conn.commit()
    conn.close()
        
def uploadNHLPlayerSeasonDataToDatabase(db_name, start_y = None, start_m = None, start_d = None, end_date_y = None, end_date_m = None, end_date_d = None):
    conn = establishDatabaseConnection(db_name)
    if start_y is None: # assume that this param missing indicates the rest are empty as well(only call currently in daily.py)
        start_date = date.today() - timedelta(1)
        end_date = date.today()
    else:
        start_date = date(start_y, start_m, start_d)
        end_date = date(end_date_y, end_date_m, end_date_d)
    FILE_SUFFIX = " - Player Season Totals.csv"
    for single_date in daterange(start_date, end_date):
        basepath = path.dirname(__file__)
        datestring = single_date.strftime("%Y-%m-%d")
        filename = datestring + FILE_SUFFIX
        filepath = path.abspath(path.join(basepath, "..", "data", filename))
        df = pd.read_csv(filepath)
        for index, row in df.iterrows():
            player_id = row[0]
            player_name = row["Player"]
            player_team = row["Team"]
            gp = row["GP"]
            toi = row["TOI"]
            goals = row["Goals"]
            assists = row["Total Assists"]
            first_assists = row["First Assists"]
            second_assists = row["Second Assists"]
            points = row["Total Points"]
            ipp = row["IPP"]
            shots = row["Shots"]
            sh_pct = row["SH%"]
            ixg = row["ixG"]
            icf = row['iCF']
            icf = icf / gp
            iff =  row['iFF']
            iff = iff / gp
            iscf =  row['iSCF']
            iscf = iscf / gp
            ihdcf =  row['iHDCF']
            ihdcf = ihdcf / gp
            rush_attempts = row['Rush Attempts']
            rebounds_created =  row['Rebounds Created']
            penalty_minutes =  row['PIM']
            total_penalties =  row['Total Penalties']
            minor =  row['Minor']
            major =  row['Major']
            misconduct =  row['Misconduct']
            penalties_drawn =  row['Penalties Drawn']
            giveaways =  row['Giveaways']
            takeaways =  row['Takeaways']
            hits =  row['Hits']
            hits_taken =  row['Hits Taken']
            shots_blocked =  row['Shots Blocked']
            faceoffs_won =  row['Faceoffs Won']
            faceoffs_lost =  row['Faceoffs Lost']
            faceoffs_pct =  row['Faceoffs %']

            player_tuple = (player_id, player_name, player_team, datestring, gp, toi, goals, assists, first_assists, second_assists, points,
                            ipp,  shots, sh_pct, ixg,  icf, iff, iscf, ihdcf, rush_attempts, rebounds_created, penalty_minutes,
                            total_penalties, minor, major, misconduct, penalties_drawn, giveaways, takeaways, hits,
                            hits_taken,shots_blocked,faceoffs_won, faceoffs_lost,faceoffs_pct)
            query = """INSERT INTO skater_season_totals(
                nst_player_id,
                player_name,
                team,
                date,
                games_played,
                time_on_ice,
                goals,
                assists,
                first_assists,
                second_assists,
                points,
                ipp,
                shots,
                shooting_pct,
                ixg,
                icf,
                iff,
                iscf,
                ihdcf,
                rush_attempts,
                rebounds_created,
                penalty_minutes,
                total_penalties,
                minor,
                major,
                misconduct,
                penalties_drawn,
                giveaways,
                takeaways,
                hits,
                hits_taken,
                shots_blocked,
                faceoffs_won,
                faceoffs_lost,
                faceoff_pct)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            c = conn.cursor()
            c.execute(query, player_tuple)
        print(filename + " processed")
    
    conn.commit()
def uploadNHLPlayerTwoWkSeasonDataToDatabase(db_name, start_y = None, start_m = None, start_d = None, end_date_y = None, end_date_m = None, end_date_d = None):
    conn = establishDatabaseConnection(db_name)
    if start_y is None: # assume that this param missing indicates the rest are empty as well(only call currently in daily.py)
        start_date = date.today() - timedelta(1)
        end_date = date.today()
    else:
        start_date = date(start_y, start_m, start_d)
        end_date = date(end_date_y, end_date_m, end_date_d)
    FILE_SUFFIX = " - Player 2 Week Totals.csv"
    for single_date in daterange(start_date, end_date):
        basepath = path.dirname(__file__)
        datestring = single_date.strftime("%Y-%m-%d")
        filename = datestring + FILE_SUFFIX
        filepath = path.abspath(path.join(basepath, "..", "data", filename))
        df = pd.read_csv(filepath)
        for index, row in df.iterrows():
            player_id = row[0]
            player_name = row["Player"]
            player_team = row["Team"]
            gp = row["GP"]
            toi = row["TOI"]
            goals = row["Goals"]
            assists = row["Total Assists"]
            first_assists = row["First Assists"]
            second_assists = row["Second Assists"]
            points = row["Total Points"]
            ipp = row["IPP"]
            shots = row["Shots"]
            sh_pct = row["SH%"]
            ixg = row["ixG"]
            icf = row['iCF']
            icf = icf / gp
            iff =  row['iFF']
            iff = iff / gp
            iscf =  row['iSCF']
            iscf = iscf / gp
            ihdcf =  row['iHDCF']
            ihdcf = ihdcf / gp
            rush_attempts = row['Rush Attempts']
            rebounds_created =  row['Rebounds Created']
            penalty_minutes =  row['PIM']
            total_penalties =  row['Total Penalties']
            minor =  row['Minor']
            major =  row['Major']
            misconduct =  row['Misconduct']
            penalties_drawn =  row['Penalties Drawn']
            giveaways =  row['Giveaways']
            takeaways =  row['Takeaways']
            hits =  row['Hits']
            hits_taken =  row['Hits Taken']
            shots_blocked =  row['Shots Blocked']
            faceoffs_won =  row['Faceoffs Won']
            faceoffs_lost =  row['Faceoffs Lost']
            faceoffs_pct =  row['Faceoffs %']

            player_tuple = (player_id, player_name, player_team, datestring, gp, toi, goals, assists, first_assists, second_assists, points,
                            ipp,  shots, sh_pct, ixg,  icf, iff, iscf, ihdcf, rush_attempts, rebounds_created, penalty_minutes,
                            total_penalties, minor, major, misconduct, penalties_drawn, giveaways, takeaways, hits,
                            hits_taken,shots_blocked,faceoffs_won, faceoffs_lost,faceoffs_pct)
            query = """INSERT INTO skater_two_wk_totals(
                nst_player_id,
                player_name,
                team,
                date,
                games_played,
                time_on_ice,
                goals,
                assists,
                first_assists,
                second_assists,
                points,
                ipp,
                shots,
                shooting_pct,
                ixg,
                icf,
                iff,
                iscf,
                ihdcf,
                rush_attempts,
                rebounds_created,
                penalty_minutes,
                total_penalties,
                minor,
                major,
                misconduct,
                penalties_drawn,
                giveaways,
                takeaways,
                hits,
                hits_taken,
                shots_blocked,
                faceoffs_won,
                faceoffs_lost,
                faceoff_pct)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            c = conn.cursor()
            c.execute(query, player_tuple)
        print(filename + " processed")
    
    conn.commit()
#uploadNHLTeamsToDatabase("main.db")
#uploadNHLPlayersToDatabase("main.db")
#uploadNHLGameDataToDatabaseFromFile("main.db")
#######uploadNHLPlayerGameDataToDatabase("main.db", "2022-10-07", "2023-03-08")
####uploadNHLPlayerSeasonDataToDatabase("main.db", 2022, 10, 13, 2023, 3, 12)
##uploadNHLPlayerTwoWkSeasonDataToDatabase("main.db",2023,3,18, 2023,3,19)