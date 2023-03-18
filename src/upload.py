import requests
import pandas as pd
import utils
import importCsv
import sqlite3


def uploadGameResultsAndTeamStats(start_date = None, end_date = None):
    if start_date is None:
        start_date = utils.getYesterdaysDate("%Y-%m-%d")
    if end_date is None:
        end_date = utils.getTodaysDate("%Y-%m-%d") # if date params left null, will retrieve last night's games
    url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}".format(start_date, end_date)
    request = requests.get(url)
    requestJson = request.json()

    conn = utils.establishDatabaseConnection("main.db")
    c = conn.cursor()
    
    for date in requestJson['dates']:
        for game in date['games']:
            if game['gameType'] == "R" or game['gameType'] == "P": # process only regular season or playoff games(no pre-season)
                if game['status']['statusCode'] == "7" or game['status']['statusCode'] == "6": # 7 or 6 - Final, otherwise don't process game as it won't contain scores 
                    game_id = game['gamePk']   # get gameId
                    #pred_row_index = df2.index[df2['game_id'] == game_id] # find game by ID in predictions csv file
                    #update game row with goals for both teams and respective result
                    home_team_goals = game['teams']['home']['score']
                    away_team_goals = game['teams']['away']['score']
                    if home_team_goals > away_team_goals:
                        result = 1
                    else:
                        result = 0
                    

                    #update scores in predictions csv file as well
                    # df2.loc[pred_row_index,"home_team_goals"] = home_team_goals
                    # df2.loc[pred_row_index,"away_team_goals"] = away_team_goals
                    # df2.loc[pred_row_index,"result"] = result
                    # c.execute("SELECT date, home_team, away_team FROM games where id = (?)", (game_id))
                    # game_info = c.fetchall()

                    # game_date = game_info[0]
                    # home_team = game_info[1]
                    # away_team = game_info[2]

                    game_date = date['date']
                    home_team = game['teams']['home']['team']['name']
                    away_team = game['teams']['away']['team']['name']
                    print(game_date,home_team,away_team)
                    # Special é character exception
                    home_team, away_team = utils.handleSpecialCharactersInTeamNames(home_team, away_team)

                    game_dict = importCsv.getTeamsStats(game_date, home_team, away_team, backdate = True)
                    if game_dict == {}:
                        print("Team data missing for: \n")
                        print(game_date,home_team,away_team) # print for debugging purposes
                        continue    # if team stats file not found, don't touch csv rows
                    #2 checks if dictionary present but one team's data is missing
                    if "home_team" not in list(game_dict.keys()):
                        print("{} stats missing from {}".format(home_team,game_date))
                        continue
                    if "away_team" not in list(game_dict.keys()):
                        print("{} stats missing from {}".format(away_team,game_date))
                        continue
                    home_team_dict = game_dict['home_team']
                    away_team_dict = game_dict['away_team']
                    h_point_pct = home_team_dict['Point %']
                    h_cf_pct = home_team_dict['CF%']
                    h_ff_pct = home_team_dict['FF%']
                    h_sf_pct = home_team_dict['SF%']
                    h_gf_pct = home_team_dict['GF%']
                    h_xgf_pct = home_team_dict['xGF%']
                    h_scf_pct= home_team_dict['SCF%']
                    h_scsf_pct = home_team_dict['SCSF%']
                    h_scgf_pct = home_team_dict['SCGF%']
                    h_scsh_pct = home_team_dict['SCSH%']
                    h_scsv_pct = home_team_dict['SCSV%']
                    h_hdsf_pct = home_team_dict['HDSF%']
                    h_hdgf_pct = home_team_dict['HDGF%']
                    h_hdsh_pct = home_team_dict['HDSH%']
                    h_hdsv_pct  = home_team_dict['HDSV%']
                    h_mdsf_pct = home_team_dict['MDSF%']
                    h_mdgf_pct = home_team_dict['MDGF%']
                    h_mdsh_pct = home_team_dict['MDSH%']
                    h_mdsv_pct = home_team_dict['MDSV%']
                    h_ldsf_pct = home_team_dict['LDSF%']
                    h_ldgf_pct = home_team_dict['LDGF%']
                    h_ldsh_pct = home_team_dict['LDSH%']
                    h_ldsv_pct = home_team_dict['LDSV%']
                    h_sh_pct = home_team_dict['SH%']
                    h_sv_pct = home_team_dict['SV%']
                    h_PDO = home_team_dict['PDO']
                    #away team
                    a_point_pct = away_team_dict['Point %']
                    a_cf_pct = away_team_dict['CF%']
                    a_ff_pct = away_team_dict['FF%']
                    a_sf_pct = away_team_dict['SF%']
                    a_gf_pct = away_team_dict['GF%']
                    a_xgf_pct = away_team_dict['xGF%']
                    a_scf_pct= away_team_dict['SCF%']
                    a_scsf_pct = away_team_dict['SCSF%']
                    a_scgf_pct = away_team_dict['SCGF%']
                    a_scsh_pct = away_team_dict['SCSH%']
                    a_scsv_pct = away_team_dict['SCSV%']
                    a_hdsf_pct = away_team_dict['HDSF%']
                    a_hdgf_pct = away_team_dict['HDGF%']
                    a_hdsh_pct = away_team_dict['HDSH%']
                    a_hdsv_pct  = away_team_dict['HDSV%']
                    a_mdsf_pct = away_team_dict['MDSF%']
                    a_mdgf_pct = away_team_dict['MDGF%']
                    a_mdsh_pct = away_team_dict['MDSH%']
                    a_mdsv_pct = away_team_dict['MDSV%']
                    a_ldsf_pct = away_team_dict['LDSF%']
                    a_ldgf_pct = away_team_dict['LDGF%']
                    a_ldsh_pct = away_team_dict['LDSH%']
                    a_ldsv_pct = away_team_dict['LDSV%']
                    a_sh_pct = away_team_dict['SH%']
                    a_sv_pct = away_team_dict['SV%']
                    a_PDO = away_team_dict['PDO']

                    game_tuple = (home_team_goals, away_team_goals, result, h_point_pct, h_cf_pct,h_ff_pct,h_sf_pct,
                        h_gf_pct, h_xgf_pct, h_scf_pct,h_scsf_pct,h_scgf_pct,
                        h_scsh_pct,h_scsv_pct,h_hdsf_pct,h_hdgf_pct,h_hdsh_pct,
                        h_hdsv_pct,h_mdsf_pct,h_mdgf_pct,h_mdsh_pct,h_mdsv_pct,
                        h_ldsf_pct,h_ldgf_pct,h_ldsh_pct,h_ldsv_pct,h_sh_pct,h_sv_pct,
                        h_PDO,a_point_pct,a_cf_pct,a_ff_pct, a_sf_pct,a_gf_pct,a_xgf_pct
                        ,a_scf_pct,a_scsf_pct,a_scgf_pct,a_scsh_pct,a_scsv_pct,a_hdsf_pct,
                        a_hdgf_pct,a_hdsh_pct,a_hdsv_pct,a_mdsf_pct,a_mdgf_pct,a_mdsh_pct,
                        a_mdsv_pct,a_ldsf_pct,a_ldgf_pct,a_ldsh_pct,a_ldsv_pct, 
                        a_sh_pct,a_sv_pct,a_PDO, game_id)
                    query = """UPDATE games SET 
                    home_team_goals = ?,
                    away_team_goals = ?,
                    result = ?,
                    h_point_pct = ?,
                    h_cf_pct = ?,
                    h_ff_pct = ?,
                    h_sf_pct = ?,
                    h_gf_pct = ?,
                    h_xgf_pct = ?,
                    h_scf_pct = ?,
                    h_scsf_pct = ?,
                    h_scgf_pct = ?,
                    h_scsh_pct = ?,
                    h_scsv_pct = ?,
                    h_hdsf_pct = ?,
                    h_hdgf_pct = ?,
                    h_hdsh_pct = ?,
                    h_hdsv_pct = ?,
                    h_mdsf_pct = ?,
                    h_mdgf_pct = ?,
                    h_mdsh_pct = ?,
                    h_mdsv_pct = ?,
                    h_ldsf_pct = ?,
                    h_ldgf_pct = ?,
                    h_ldsh_pct = ?,
                    h_ldsv_pct = ?,
                    h_sh_pct = ?,
                    h_sv_pct = ?,
                    h_PDO = ?, 
                    a_point_pct = ?,
                    a_cf_pct = ?,
                    a_ff_pct = ?,
                    a_sf_pct = ?,
                    a_gf_pct = ?,
                    a_xgf_pct = ?,
                    a_scf_pct = ?,
                    a_scsf_pct = ?,
                    a_scgf_pct = ?,
                    a_scsh_pct = ?,
                    a_scsv_pct = ?,
                    a_hdsf_pct = ?,
                    a_hdgf_pct = ?,
                    a_hdsh_pct = ?,
                    a_hdsv_pct = ?,
                    a_mdsf_pct = ?,
                    a_mdgf_pct = ?,
                    a_mdsh_pct = ?,
                    a_mdsv_pct = ?,
                    a_ldsf_pct = ?,
                    a_ldgf_pct = ?,
                    a_ldsh_pct = ?,
                    a_ldsv_pct = ?,
                    a_sh_pct = ?,
                    a_sv_pct = ?,
                    a_PDO = ?
                    WHERE id = ?"""
                    
                    try: 
                        c.execute(query, game_tuple)
                    except Exception as e:
                        print("c.execute failed with: " + str(e))
                        raise Exception(e)
                    print("Database entry updated for " + game_date + " " + home_team + " vs " + away_team)

    conn.commit()
    conn.close()   