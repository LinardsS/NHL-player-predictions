import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os import path
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.api as sm
import pickle
import utils
import math

## Will first train model (skater season totals + 2wk totals)
## Later on: 
    # skater season totals, 
    # skater season totals + 2wk totals + pp totals, 
    # skater season totals + 2wk totals + pp totals + opposing goalie data, 
    # skater season totals + 2wk totals + pp totals + opposing goalie data + opposing team data
    # all goalie models

def trainSkaterSeasonAndTwoWkTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT  twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                            twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                            twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                            twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                            twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                            twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                            twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                            twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                            twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                            sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                            sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                            sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                            sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                            sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                            sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                            sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                            sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                            sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                            sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                            sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                            sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                            sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                            sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                            sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                            sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus
             FROM   games g, skater_game_data sgd, skater_two_wk_totals twowk, skater_season_totals sst
             WHERE  g.id = sgd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    sgd.player_name = sst.player_name
             and    twowk.player_name = sst.player_name
             and    sst.date = DATE(g.date, '-1 day')
             and    twowk.date = sst.date"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    #print(df.describe())
    # aa = df.drop(columns = ['player_name', 'game_id'])
    # string_rows = aa.apply(lambda x: any(isinstance(value, str) for value in x), axis=1)
    # basepath = path.dirname(__file__)
    # filename = utils.getTodaysDate(format = "%Y-%m-%d %H-%M-%S",backdate = None)
    # filename = filename + ".csv"
    # filepath = path.abspath(path.join(basepath, "..", "data", filename))
    # res = df[string_rows]
    # res.to_csv(filepath, index=False)
    # return 0
    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split
    #print(train[['twowk_games_played'] + ['twowk_time_on_ice'] + ['twowk_goals'] + ['twowk_assists'] + ['twowk_first_assists'] + ['twowk_second_assists'] + ['twowk_points'] + ['twowk_ipp'] + ['twowk_shots'] + ['twowk_shooting_pct'] + ['twowk_ixg'] + ['twowk_icf'] + ['twowk_iff'] + ['twowk_iscf'] + ['twowk_ihdcf'] + ['twowk_rush_attempts'] + ['twowk_rebounds_created'] + ['twowk_penalty_minutes'] + ['twowk_penalties_drawn'] + ['twowk_giveaways'] + ['twowk_takeaways'] + ['twowk_hits'] + ['twowk_hits_taken'] + ['twowk_shots_blocked'] + ['twowk_faceoffs_won'] + ['twowk_faceoffs_lost'] + ['twowk_faceoff_pct'] + ['sst_games_played'] + ['sst_time_on_ice'] + ['sst_goals'] + ['sst_assists'] + ['sst_first_assists'] + ['sst_second_assists'] + ['sst_points'] + ['sst_ipp'] + ['sst_shots'] + ['sst_shooting_pct'] + ['sst_ixg'] + ['sst_icf'] + ['sst_iff'] + ['sst_iscf'] + ['sst_ihdcf'] + ['sst_rush_attempts'] + ['sst_rebounds_created'] + ['sst_penalty_minutes'] + ['sst_penalties_drawn'] + ['sst_giveaways'] + ['sst_takeaways'] + ['sst_hits'] + ['sst_hits_taken'] + ['sst_shots_blocked'] + ['sst_faceoffs_won'] + ['sst_faceoffs_lost'] + ['sst_faceoff_pct']])
    
    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print(predict)
    print(r2_score(Y_test,predict))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linear_Regression_' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))

def loadModel(model_name):
    basepath = path.dirname(__file__)
    filename = model_name + ".sav"
    filepath = path.abspath(path.join(basepath, "..", filename))
    loaded_model = pickle.load(open(filepath, 'rb'))
    return loaded_model

def testModelPrediction():
    model = loadModel("Linear_Regression_0.242_2023-04-09")
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT  twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                            twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                            twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                            twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                            twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                            twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                            twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                            twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                            twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                            sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                            sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                            sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                            sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                            sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                            sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                            sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                            sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                            sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct
             FROM   skater_two_wk_totals twowk, skater_season_totals sst
             WHERE  twowk.player_name = sst.player_name
             and    sst.date = (?)
             and    twowk.date = sst.date
             and    sst.player_name = 'Connor McDavid'"""
    start_date = "2023-04-05"
    query_params = (start_date,)
    df = pd.read_sql_query(query, conn, params = query_params)
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    prediction = model.predict(df)[0].tolist()
    pred_columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']
    res = {}
    for key in pred_columns:
        for value in prediction:
            res[key] = value
            prediction.remove(value)
            break
    print(res)

def trainSkaterSeasonTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT       sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                            sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                            sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                            sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                            sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                            sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                            sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                            sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                            sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                            sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                            sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                            sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                            sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                            sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                            sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                            sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus
             FROM   games g, skater_game_data sgd, skater_season_totals sst
             WHERE  g.id = sgd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    sgd.player_name = sst.player_name
             and    sst.date = DATE(g.date, '-1 day')"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split

    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print(predict)
    print(r2_score(Y_test,predict))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linreg_OnlySeasonTotals_' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))

def trainSkaterSeasonPPTwoWkTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT  twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                        twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                        twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                        twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                        twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                        twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                        twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                        twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                        twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                        sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                        sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                        sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                        sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                        sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                        sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                        sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                        sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                        sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                        sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                        sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                        sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                        sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                        sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                        sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                        sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus,
                        sppt.games_played as sppt_games_played, sppt.time_on_ice as sppt_time_on_ice, sppt.goals as sppt_goals,
                        sppt.assists as sppt_assists, sppt.first_assists as sppt_first_assists, sppt.second_assists as sppt_second_assists,
                        sppt.points as sppt_points, sppt.ipp as sppt_ipp, sppt.shots as sppt_shots, sppt.shooting_pct as sppt_shooting_pct,
                        sppt.ixg as sppt_ixg, sppt.icf as sppt_icf, sppt.iff as sppt_iff,
                        sppt.iscf as sppt_iscf, sppt.ihdcf as sppt_ihdcf, sppt.rush_attempts as sppt_rush_attempts, sppt.rebounds_created as sppt_rebounds_created, 
                        sppt.penalty_minutes as sppt_penalty_minutes, sppt.penalties_drawn as sppt_penalties_drawn, 
                        sppt.giveaways as sppt_giveaways, sppt.takeaways as sppt_takeaways, sppt.hits as sppt_hits,  
                        sppt.hits_taken as sppt_hits_taken, sppt.shots_blocked as sppt_shots_blocked, sppt.faceoffs_won as sppt_faceoffs_won,
                        sppt.faceoffs_lost as sppt_faceoffs_lost, sppt.faceoff_pct as sppt_faceoff_pct
             FROM   games g, skater_game_data sgd, skater_two_wk_totals twowk, skater_season_totals sst, skater_pp_totals sppt
             WHERE  g.id = sgd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    sgd.player_name = sst.player_name
             and    twowk.player_name = sst.player_name
             and    sppt.player_name = twowk.player_name
             and    sst.date = DATE(g.date, '-1 day')
             and    twowk.date = sst.date
             and    sppt.date = twowk.date"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split

    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print(predict)
    print(r2_score(Y_test,predict))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linreg_SeasonPPTwoWk_' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))

def trainSkaterSeasonPPTwoWkOppGoalieTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT   twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                        twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                        twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                        twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                        twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                        twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                        twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                        twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                        twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                        sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                        sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                        sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                        sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                        sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                        sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                        sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                        sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                        sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                        sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                        sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                        sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                        sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                        sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                        sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                        sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus,
                        gst.gp as gst_gp,gst.toi as gst_toi, gst.shots_against as gst_shots_against, gst.saves as gst_saves,
                        gst.goals_against as gst_goals_against, gst.sv_pct as gst_sv_pct, gst.gaa as gst_gaa, gst.gsaa as gst_gsaa,
                        gst.xg_against as gst_xg_against, gst.hd_shots_against as gst_hd_shots_against,gst.hd_saves as gst_hd_saves,
                        gst.hd_goals_against as gst_hd_goals_against, gst.hdsv_pct as gst_hdsv_pct, gst.hdgaa as gst_hdgaa,
                        gst.hdgsaa as gst_hdgsaa, gst.md_shots_against as gst_md_shots_against, gst.md_saves as gst_md_saves,
                        gst.md_goals_against as gst_md_goals_against, gst.mdsv_pct as gst_mdsv_pct, gst.mdgaa as gst_mdgaa, 
                        gst.mdgsaa as gst_mdgsaa,gst.ld_shots_against as gst_ld_shots_against, gst.ld_saves as gst_ld_saves,
                        gst.ld_goals_against as gst_ld_goals_against, gst.ldsv_pct as gst_ldsv_pct, gst.ldgaa as gst_ldgaa, gst.ldgsaa as gst_ldgsaa,
                        gst.rush_attempts_against as gst_rush_attempts_against, gst.rebound_attempts_against as gst_rebound_attempts_against
             FROM   games g, skater_game_data sgd, skater_two_wk_totals twowk, skater_season_totals sst, goalie_season_totals gst
             WHERE  g.id = sgd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    sgd.player_name = sst.player_name
             and    twowk.player_name = sst.player_name
             and    sst.date = DATE(g.date, '-1 day')
             and    twowk.date = sst.date
             and    gst.player_name = (SELECT  ggd.player_name 
                                        FROM   goalie_game_data ggd, skater_game_data sgd, players p, games g
                                        WHERE  sgd.player_name = sst.player_name
                                        and    sgd.opponent_team_id = p.team_id
                                        and    g.id = sgd.game_id
                                        and    ggd.date = sgd.date
                                        and    ggd.player_name = p.name
                                        order by ggd.time_on_ice desc)
            and     gst.date = twowk.date"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split

    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print(predict)
    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linreg_SeasonPPTwoWkOppGoalie_' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))

def trainSkaterSeasonTwoWkOppGoalieOppTeamTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                    twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                    twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                    twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                    twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                    twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                    twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                    twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                    twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                    sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                    sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                    sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                    sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                    sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                    sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                    sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                    sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                    sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                    sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                    sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                    sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                    sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                    sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                    sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                    sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus,
                    gst.gp as gst_gp,gst.toi as gst_toi, gst.shots_against as gst_shots_against, gst.saves as gst_saves,
                    gst.goals_against as gst_goals_against, gst.sv_pct as gst_sv_pct, gst.gaa as gst_gaa, gst.gsaa as gst_gsaa,
                    gst.xg_against as gst_xg_against, gst.hd_shots_against as gst_hd_shots_against,gst.hd_saves as gst_hd_saves,
                    gst.hd_goals_against as gst_hd_goals_against, gst.hdsv_pct as gst_hdsv_pct, gst.hdgaa as gst_hdgaa,
                    gst.hdgsaa as gst_hdgsaa, gst.md_shots_against as gst_md_shots_against, gst.md_saves as gst_md_saves,
                    gst.md_goals_against as gst_md_goals_against, gst.mdsv_pct as gst_mdsv_pct, gst.mdgaa as gst_mdgaa, 
                    gst.mdgsaa as gst_mdgsaa,gst.ld_shots_against as gst_ld_shots_against, gst.ld_saves as gst_ld_saves,
                    gst.ld_goals_against as gst_ld_goals_against, gst.ldsv_pct as gst_ldsv_pct, gst.ldgaa as gst_ldgaa, gst.ldgsaa as gst_ldgsaa,
                    gst.rush_attempts_against as gst_rush_attempts_against, gst.rebound_attempts_against as gst_rebound_attempts_against,
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_point_pct
                            ELSE g.h_point_pct
                            END AS opp_team_point_pct, 
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_cf_pct
                            ELSE g.h_cf_pct
                            END AS opp_cf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ff_pct
                            ELSE g.h_ff_pct
                            END AS opp_ff_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sf_pct
                            ELSE g.h_sf_pct
                            END AS opp_sf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_gf_pct
                            ELSE g.h_gf_pct
                            END AS opp_gf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_xgf_pct
                            ELSE g.h_xgf_pct
                            END AS opp_xgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scf_pct
                            ELSE g.h_scf_pct
                            END AS opp_scf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsf_pct
                            ELSE g.h_scsf_pct
                            END AS opp_scsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scgf_pct
                            ELSE g.h_scgf_pct
                            END AS opp_scgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsh_pct
                            ELSE g.h_scsh_pct
                            END AS opp_scsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsv_pct
                            ELSE g.h_scsv_pct
                            END AS opp_scsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsf_pct
                            ELSE g.h_hdsf_pct
                            END AS opp_hdsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdgf_pct
                            ELSE g.h_hdgf_pct
                            END AS opp_hdgf_pct,   
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsh_pct
                            ELSE g.h_hdsh_pct
                            END AS opp_hdsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsv_pct
                            ELSE g.h_hdsv_pct
                            END AS opp_hdsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsf_pct
                            ELSE g.h_mdsf_pct
                            END AS opp_mdsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdgf_pct
                            ELSE g.h_mdgf_pct
                            END AS opp_mdgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsh_pct
                            ELSE g.h_mdsh_pct
                            END AS opp_mdsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsv_pct
                            ELSE g.h_mdsv_pct
                            END AS opp_mdsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsf_pct
                            ELSE g.h_ldsf_pct
                            END AS opp_ldsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldgf_pct
                            ELSE g.h_ldgf_pct
                            END AS opp_ldgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsh_pct
                            ELSE g.h_ldsh_pct
                            END AS opp_ldsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsv_pct
                            ELSE g.h_ldsv_pct
                            END AS opp_ldsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sh_pct
                            ELSE g.h_sh_pct
                            END AS opp_sh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sv_pct
                            ELSE g.h_sv_pct
                            END AS opp_sv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_PDO
                            ELSE g.h_PDO
                            END AS opp_PDO
            FROM   games g, skater_game_data sgd, skater_two_wk_totals twowk, skater_season_totals sst, goalie_season_totals gst, teams t
            WHERE  g.id = sgd.game_id
            and    g.date >= (?)
            and    g.date <= (?)
            and    sgd.player_name = sst.player_name
            and    twowk.player_name = sst.player_name
            and    sst.date = DATE(g.date, '-1 day')
            and    twowk.date = sst.date
            and    gst.player_name = (SELECT  ggd.player_name 
                                    FROM   goalie_game_data ggd, skater_game_data sgd, players p, games g
                                    WHERE  sgd.player_name = sst.player_name
                                    and    sgd.opponent_team_id = p.team_id
                                    and    g.id = sgd.game_id
                                    and    ggd.date = sgd.date
                                    and    ggd.player_name = p.name
                                    order by ggd.time_on_ice desc)
            and     gst.date = twowk.date
            and     t.id = sgd.opponent_team_id"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split

    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print(predict)
    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linreg_SeasonTwoWkOppGoalieOppTeam_' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))

def trainSkaterSeasonTwoWkOppGoalieSigOppTeamTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                    twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                    twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                    twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                    twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                    twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                    twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                    twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                    twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                    sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                    sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                    sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                    sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                    sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                    sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                    sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                    sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                    sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                    sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                    sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                    sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                    sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                    sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                    sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                    sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus,
                    gst.gp as gst_gp,gst.toi as gst_toi, gst.shots_against as gst_shots_against, gst.saves as gst_saves,
                    gst.goals_against as gst_goals_against, gst.sv_pct as gst_sv_pct, gst.gaa as gst_gaa, gst.gsaa as gst_gsaa,
                    gst.xg_against as gst_xg_against, gst.hd_shots_against as gst_hd_shots_against,gst.hd_saves as gst_hd_saves,
                    gst.hd_goals_against as gst_hd_goals_against, gst.hdsv_pct as gst_hdsv_pct, gst.hdgaa as gst_hdgaa,
                    gst.hdgsaa as gst_hdgsaa, gst.md_shots_against as gst_md_shots_against, gst.md_saves as gst_md_saves,
                    gst.md_goals_against as gst_md_goals_against, gst.mdsv_pct as gst_mdsv_pct, gst.mdgaa as gst_mdgaa, 
                    gst.mdgsaa as gst_mdgsaa,gst.ld_shots_against as gst_ld_shots_against, gst.ld_saves as gst_ld_saves,
                    gst.ld_goals_against as gst_ld_goals_against, gst.ldsv_pct as gst_ldsv_pct, gst.ldgaa as gst_ldgaa, gst.ldgsaa as gst_ldgsaa,
                    gst.rush_attempts_against as gst_rush_attempts_against, gst.rebound_attempts_against as gst_rebound_attempts_against,
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_point_pct
                            ELSE g.h_point_pct
                            END AS opp_team_point_pct, 
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_cf_pct
                            ELSE g.h_cf_pct
                            END AS opp_cf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ff_pct
                            ELSE g.h_ff_pct
                            END AS opp_ff_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sf_pct
                            ELSE g.h_sf_pct
                            END AS opp_sf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_gf_pct
                            ELSE g.h_gf_pct
                            END AS opp_gf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_xgf_pct
                            ELSE g.h_xgf_pct
                            END AS opp_xgf_pct,
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sv_pct
                            ELSE g.h_sv_pct
                            END AS opp_sv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_PDO
                            ELSE g.h_PDO
                            END AS opp_PDO
            FROM   games g, skater_game_data sgd, skater_two_wk_totals twowk, skater_season_totals sst, goalie_season_totals gst, teams t
            WHERE  g.id = sgd.game_id
            and    g.date >= (?)
            and    g.date <= (?)
            and    sgd.player_name = sst.player_name
            and    twowk.player_name = sst.player_name
            and    sst.date = DATE(g.date, '-1 day')
            and    twowk.date = sst.date
            and    gst.player_name = (SELECT  ggd.player_name 
                                    FROM   goalie_game_data ggd, skater_game_data sgd, players p, games g
                                    WHERE  sgd.player_name = sst.player_name
                                    and    sgd.opponent_team_id = p.team_id
                                    and    g.id = sgd.game_id
                                    and    ggd.date = sgd.date
                                    and    ggd.player_name = p.name
                                    order by ggd.time_on_ice desc)
            and     gst.date = twowk.date
            and     t.id = sgd.opponent_team_id"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split

    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print(predict)
    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linreg_SeasonTwoWkOppGoalieSigOppTeam_' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))

def dtTrainSkaterSeasonAndTwoWkTotalsModel():
    ccp_a = 0.001
    md = 10
    criterion = 'friedman_mse'
    dt = DecisionTreeRegressor(criterion=criterion, max_depth=md, ccp_alpha=ccp_a)
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT  twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                            twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                            twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                            twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                            twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                            twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                            twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                            twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                            twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                            sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                            sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                            sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                            sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                            sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                            sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                            sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                            sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                            sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                            sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                            sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                            sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                            sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                            sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                            sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                            sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus
             FROM   games g, skater_game_data sgd, skater_two_wk_totals twowk, skater_season_totals sst
             WHERE  g.id = sgd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    sgd.player_name = sst.player_name
             and    twowk.player_name = sst.player_name
             and    sst.date = DATE(g.date, '-1 day')
             and    twowk.date = sst.date"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split
    #print(train[['twowk_games_played'] + ['twowk_time_on_ice'] + ['twowk_goals'] + ['twowk_assists'] + ['twowk_first_assists'] + ['twowk_second_assists'] + ['twowk_points'] + ['twowk_ipp'] + ['twowk_shots'] + ['twowk_shooting_pct'] + ['twowk_ixg'] + ['twowk_icf'] + ['twowk_iff'] + ['twowk_iscf'] + ['twowk_ihdcf'] + ['twowk_rush_attempts'] + ['twowk_rebounds_created'] + ['twowk_penalty_minutes'] + ['twowk_penalties_drawn'] + ['twowk_giveaways'] + ['twowk_takeaways'] + ['twowk_hits'] + ['twowk_hits_taken'] + ['twowk_shots_blocked'] + ['twowk_faceoffs_won'] + ['twowk_faceoffs_lost'] + ['twowk_faceoff_pct'] + ['sst_games_played'] + ['sst_time_on_ice'] + ['sst_goals'] + ['sst_assists'] + ['sst_first_assists'] + ['sst_second_assists'] + ['sst_points'] + ['sst_ipp'] + ['sst_shots'] + ['sst_shooting_pct'] + ['sst_ixg'] + ['sst_icf'] + ['sst_iff'] + ['sst_iscf'] + ['sst_ihdcf'] + ['sst_rush_attempts'] + ['sst_rebounds_created'] + ['sst_penalty_minutes'] + ['sst_penalties_drawn'] + ['sst_giveaways'] + ['sst_takeaways'] + ['sst_hits'] + ['sst_hits_taken'] + ['sst_shots_blocked'] + ['sst_faceoffs_won'] + ['sst_faceoffs_lost'] + ['sst_faceoff_pct']])
    
    dt.fit(X_train,Y_train)
    predict = dt.predict(X_test)

    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'DT_' + str(md) + 'MD_FMSE_SeasonTwoWk_' + str(r_sq_score) + '_'+ datum + '.sav'
    print(filename)
    pickle.dump(dt, open(filename, 'wb'))

def plotDecisionTreeRegressor():
    feature_names = ['h_cf%', 'h_ff%', 'h_sf%',
       'h_gf%', 'h_xgf%', 'h_scf%', 'h_scsf%', 'h_scgf%', 'h_scsh%', 'h_scsv%',
       'h_hdsf%', 'h_hdgf%', 'h_hdsh%', 'h_hdsv%', 'h_mdsf%', 'h_mdgf%',
       'h_mdsh%', 'h_mdsv%', 'h_ldsf%', 'h_ldgf%', 'h_ldsh%', 'h_ldsv%',
       'h_sh%', 'h_sv%', 'h_PDO', 'a_cf%', 'a_ff%', 'a_sf%',
       'a_gf%', 'a_xgf%', 'a_scf%', 'a_scsf%', 'a_scgf%', 'a_scsh%', 'a_scsv%',
       'a_hdsf%', 'a_hdgf%', 'a_hdsh%', 'a_hdsv%', 'a_mdsf%', 'a_mdgf%',
       'a_mdsh%', 'a_mdsv%', 'a_ldsf%', 'a_ldgf%', 'a_ldsh%', 'a_ldsv%',
       'a_sh%', 'a_sv%', 'a_PDO']
    feature_importance = pd.DataFrame(dt.feature_importances_, index = feature_names)

    # plot the feature importance
    feature_plot = feature_importance.plot(kind='bar')
    feature_plot.show()

    #plot the tree itself
    fig = plt.figure(figsize=(50,50))
    tree_plot = plot_tree(dt,
                  feature_names = feature_names,
                  filled = True,
                  fontsize = 12)
    plt.show()

def dtTrainSkaterSeasonTotalsModel():
    ccp_a = 0.001
    md = 8
    criterion = 'friedman_mse'
    dt = DecisionTreeRegressor(criterion=criterion, max_depth=md, ccp_alpha=ccp_a)
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT       sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                            sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                            sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                            sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                            sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                            sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                            sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                            sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                            sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                            sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                            sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                            sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                            sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                            sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                            sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                            sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus
             FROM   games g, skater_game_data sgd, skater_season_totals sst
             WHERE  g.id = sgd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    sgd.player_name = sst.player_name
             and    sst.date = DATE(g.date, '-1 day')"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split

    dt.fit(X_train,Y_train)
    predict = dt.predict(X_test)

    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'DT_' + str(md) + 'MD_FMSE_OnlySeasonTotals_' + str(r_sq_score) + '_'+ datum + '.sav'
    print(filename)
    pickle.dump(dt, open(filename, 'wb'))

def dtTrainSkaterSeasonPPTwoWkOppGoalieTotalsModel():
    ccp_a = 0.001
    md = 8
    criterion = 'friedman_mse'
    dt = DecisionTreeRegressor(criterion=criterion, max_depth=md, ccp_alpha=ccp_a)
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT   twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                        twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                        twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                        twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                        twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                        twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                        twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                        twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                        twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                        sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                        sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                        sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                        sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                        sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                        sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                        sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                        sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                        sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                        sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                        sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                        sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                        sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                        sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                        sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                        sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus,
                        gst.gp as gst_gp,gst.toi as gst_toi, gst.shots_against as gst_shots_against, gst.saves as gst_saves,
                        gst.goals_against as gst_goals_against, gst.sv_pct as gst_sv_pct, gst.gaa as gst_gaa, gst.gsaa as gst_gsaa,
                        gst.xg_against as gst_xg_against, gst.hd_shots_against as gst_hd_shots_against,gst.hd_saves as gst_hd_saves,
                        gst.hd_goals_against as gst_hd_goals_against, gst.hdsv_pct as gst_hdsv_pct, gst.hdgaa as gst_hdgaa,
                        gst.hdgsaa as gst_hdgsaa, gst.md_shots_against as gst_md_shots_against, gst.md_saves as gst_md_saves,
                        gst.md_goals_against as gst_md_goals_against, gst.mdsv_pct as gst_mdsv_pct, gst.mdgaa as gst_mdgaa, 
                        gst.mdgsaa as gst_mdgsaa,gst.ld_shots_against as gst_ld_shots_against, gst.ld_saves as gst_ld_saves,
                        gst.ld_goals_against as gst_ld_goals_against, gst.ldsv_pct as gst_ldsv_pct, gst.ldgaa as gst_ldgaa, gst.ldgsaa as gst_ldgsaa,
                        gst.rush_attempts_against as gst_rush_attempts_against, gst.rebound_attempts_against as gst_rebound_attempts_against
             FROM   games g, skater_game_data sgd, skater_two_wk_totals twowk, skater_season_totals sst, goalie_season_totals gst
             WHERE  g.id = sgd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    sgd.player_name = sst.player_name
             and    twowk.player_name = sst.player_name
             and    sst.date = DATE(g.date, '-1 day')
             and    twowk.date = sst.date
             and    gst.player_name = (SELECT  ggd.player_name 
                                        FROM   goalie_game_data ggd, skater_game_data sgd, players p, games g
                                        WHERE  sgd.player_name = sst.player_name
                                        and    sgd.opponent_team_id = p.team_id
                                        and    g.id = sgd.game_id
                                        and    ggd.date = sgd.date
                                        and    ggd.player_name = p.name
                                        order by ggd.time_on_ice desc)
            and     gst.date = twowk.date"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split

    dt.fit(X_train,Y_train)
    predict = dt.predict(X_test)

    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'DT_' + str(md) + 'MD_FMSE_SeasonPPTwoWkOppGoalie_' + str(r_sq_score) + '_'+ datum + '.sav'
    print(filename)
    pickle.dump(dt, open(filename, 'wb'))

def dtTrainSkaterSeasonTwoWkOppGoalieOppTeamTotalsModel():
    ccp_a = 0.001
    md = 8
    criterion = 'friedman_mse'
    dt = DecisionTreeRegressor(criterion=criterion, max_depth=md, ccp_alpha=ccp_a)
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT twowk.games_played as twowk_games_played, twowk.time_on_ice as twowk_time_on_ice, twowk.goals as twowk_goals,
                    twowk.assists as twowk_assists, twowk.first_assists as twowk_first_assists, twowk.second_assists as twowk_second_assists,
                    twowk.points as twowk_points, twowk.ipp as twowk_ipp, twowk.shots as twowk_shots, twowk.shooting_pct as twowk_shooting_pct,
                    twowk.ixg as twowk_ixg, twowk.icf as twowk_icf, twowk.iff as twowk_iff,
                    twowk.iscf as twowk_iscf, twowk.ihdcf as twowk_ihdcf, twowk.rush_attempts as twowk_rush_attempts, twowk.rebounds_created as twowk_rebounds_created, 
                    twowk.penalty_minutes as twowk_penalty_minutes, twowk.penalties_drawn as twowk_penalties_drawn, 
                    twowk.giveaways as twowk_giveaways, twowk.takeaways as twowk_takeaways, twowk.hits as twowk_hits,  
                    twowk.hits_taken as twowk_hits_taken, twowk.shots_blocked as twowk_shots_blocked, twowk.faceoffs_won as twowk_faceoffs_won,
                    twowk.faceoffs_lost as twowk_faceoffs_lost, twowk.faceoff_pct as twowk_faceoff_pct,
                    sst.games_played as sst_games_played, sst.time_on_ice as sst_time_on_ice, sst.goals as sst_goals,
                    sst.assists as sst_assists, sst.first_assists as sst_first_assists, sst.second_assists as sst_second_assists,
                    sst.points as sst_points, sst.ipp as sst_ipp, sst.shots as sst_shots, sst.shooting_pct as sst_shooting_pct,
                    sst.ixg as sst_ixg, sst.icf as sst_icf, sst.iff as sst_iff,
                    sst.iscf as sst_iscf, sst.ihdcf as sst_ihdcf, sst.rush_attempts as sst_rush_attempts, sst.rebounds_created as sst_rebounds_created, 
                    sst.penalty_minutes as sst_penalty_minutes, sst.penalties_drawn as sst_penalties_drawn, 
                    sst.giveaways as sst_giveaways, sst.takeaways as sst_takeaways, sst.hits as sst_hits,  
                    sst.hits_taken as sst_hits_taken, sst.shots_blocked as sst_shots_blocked, sst.faceoffs_won as sst_faceoffs_won,
                    sst.faceoffs_lost as sst_faceoffs_lost, sst.faceoff_pct as sst_faceoff_pct,
                    sgd.time_on_ice as res_time_on_ice, sgd.goals as res_goals, sgd.assists as res_assists,
                    sgd.shots as res_shots, sgd.hits as res_hits, sgd.power_play_goals as res_power_play_goals,
                    sgd.power_play_assists as res_power_play_assists, sgd.penalty_minutes as res_penalty_minutes,
                    sgd.face_off_pct as res_face_off_pct, sgd.face_off_wins as res_face_off_wins,
                    sgd.takeaways as res_takeaways, sgd.giveaways as res_giveaways, 
                    sgd.short_handed_goals as res_short_handed_goals, sgd.short_handed_assists as res_short_handed_assists,
                    sgd.blocked_shots as res_blocked_shots, sgd.plus_minus as res_plus_minus,
                    gst.gp as gst_gp,gst.toi as gst_toi, gst.shots_against as gst_shots_against, gst.saves as gst_saves,
                    gst.goals_against as gst_goals_against, gst.sv_pct as gst_sv_pct, gst.gaa as gst_gaa, gst.gsaa as gst_gsaa,
                    gst.xg_against as gst_xg_against, gst.hd_shots_against as gst_hd_shots_against,gst.hd_saves as gst_hd_saves,
                    gst.hd_goals_against as gst_hd_goals_against, gst.hdsv_pct as gst_hdsv_pct, gst.hdgaa as gst_hdgaa,
                    gst.hdgsaa as gst_hdgsaa, gst.md_shots_against as gst_md_shots_against, gst.md_saves as gst_md_saves,
                    gst.md_goals_against as gst_md_goals_against, gst.mdsv_pct as gst_mdsv_pct, gst.mdgaa as gst_mdgaa, 
                    gst.mdgsaa as gst_mdgsaa,gst.ld_shots_against as gst_ld_shots_against, gst.ld_saves as gst_ld_saves,
                    gst.ld_goals_against as gst_ld_goals_against, gst.ldsv_pct as gst_ldsv_pct, gst.ldgaa as gst_ldgaa, gst.ldgsaa as gst_ldgsaa,
                    gst.rush_attempts_against as gst_rush_attempts_against, gst.rebound_attempts_against as gst_rebound_attempts_against,
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_point_pct
                            ELSE g.h_point_pct
                            END AS opp_team_point_pct, 
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_cf_pct
                            ELSE g.h_cf_pct
                            END AS opp_cf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ff_pct
                            ELSE g.h_ff_pct
                            END AS opp_ff_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sf_pct
                            ELSE g.h_sf_pct
                            END AS opp_sf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_gf_pct
                            ELSE g.h_gf_pct
                            END AS opp_gf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_xgf_pct
                            ELSE g.h_xgf_pct
                            END AS opp_xgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scf_pct
                            ELSE g.h_scf_pct
                            END AS opp_scf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsf_pct
                            ELSE g.h_scsf_pct
                            END AS opp_scsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scgf_pct
                            ELSE g.h_scgf_pct
                            END AS opp_scgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsh_pct
                            ELSE g.h_scsh_pct
                            END AS opp_scsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsv_pct
                            ELSE g.h_scsv_pct
                            END AS opp_scsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsf_pct
                            ELSE g.h_hdsf_pct
                            END AS opp_hdsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdgf_pct
                            ELSE g.h_hdgf_pct
                            END AS opp_hdgf_pct,   
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsh_pct
                            ELSE g.h_hdsh_pct
                            END AS opp_hdsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsv_pct
                            ELSE g.h_hdsv_pct
                            END AS opp_hdsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsf_pct
                            ELSE g.h_mdsf_pct
                            END AS opp_mdsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdgf_pct
                            ELSE g.h_mdgf_pct
                            END AS opp_mdgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsh_pct
                            ELSE g.h_mdsh_pct
                            END AS opp_mdsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsv_pct
                            ELSE g.h_mdsv_pct
                            END AS opp_mdsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsf_pct
                            ELSE g.h_ldsf_pct
                            END AS opp_ldsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldgf_pct
                            ELSE g.h_ldgf_pct
                            END AS opp_ldgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsh_pct
                            ELSE g.h_ldsh_pct
                            END AS opp_ldsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsv_pct
                            ELSE g.h_ldsv_pct
                            END AS opp_ldsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sh_pct
                            ELSE g.h_sh_pct
                            END AS opp_sh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sv_pct
                            ELSE g.h_sv_pct
                            END AS opp_sv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_PDO
                            ELSE g.h_PDO
                            END AS opp_PDO
            FROM   games g, skater_game_data sgd, skater_two_wk_totals twowk, skater_season_totals sst, goalie_season_totals gst, teams t
            WHERE  g.id = sgd.game_id
            and    g.date >= (?)
            and    g.date <= (?)
            and    sgd.player_name = sst.player_name
            and    twowk.player_name = sst.player_name
            and    sst.date = DATE(g.date, '-1 day')
            and    twowk.date = sst.date
            and    gst.player_name = (SELECT  ggd.player_name 
                                    FROM   goalie_game_data ggd, skater_game_data sgd, players p, games g
                                    WHERE  sgd.player_name = sst.player_name
                                    and    sgd.opponent_team_id = p.team_id
                                    and    g.id = sgd.game_id
                                    and    ggd.date = sgd.date
                                    and    ggd.player_name = p.name
                                    order by ggd.time_on_ice desc)
            and     gst.date = twowk.date
            and     t.id = sgd.opponent_team_id"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    # Converts the time string to minutes(float) 
    df['res_time_on_ice'] = df['res_time_on_ice'].apply(utils.convertTimeStringToMinutes)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)

    X = df.drop(columns = ['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus'])
    Y = df[['res_time_on_ice', 'res_goals', 'res_assists', 'res_shots', 'res_hits', 'res_power_play_goals', 'res_power_play_assists', 'res_penalty_minutes', 'res_face_off_pct', 'res_face_off_wins', 'res_takeaways', 'res_giveaways', 'res_short_handed_goals', 'res_short_handed_assists', 'res_blocked_shots', 'res_plus_minus']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split

    dt.fit(X_train,Y_train)
    predict = dt.predict(X_test)

    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'DT_' + str(md) + 'MD_FMSE_SeasonTwoWkOppGoalieOppTeam_' + str(r_sq_score) + '_'+ datum + '.sav'
    print(filename)
    pickle.dump(dt, open(filename, 'wb'))

def trainGoalieSeasonAndTwoWkTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT  twowk.gp as twowk_games_played, twowk.toi as twowk_time_on_ice, (twowk.shots_against / twowk.toi * 60) as twowk_sa_p60,
                        (twowk.saves / twowk.toi * 60) as twowk_saves_p60, twowk.gaa as twowk_gaa, twowk.sv_pct as twowk_sv_pct,
                        twowk.gsaa as twowk_gsaa, (twowk.xg_against / twowk.toi * 60) as twowk_xga_p60, (twowk.hd_shots_against / twowk.toi * 60) as twowk_hdsa_p60,
                        (twowk.hd_saves / twowk.toi * 60) as twowk_hds_p60, twowk.hdsv_pct as twowk_hdsv_pct, twowk.hdgaa as twowk_hdgaa, twowk.hdgsaa as twowk_hdgsaa,
                        (twowk.md_shots_against / twowk.toi * 60) as twowk_mdsa_p60,
                        (twowk.md_saves / twowk.toi * 60) as twowk_mds_p60, twowk.mdsv_pct as twowk_mdsv_pct, twowk.mdgaa as twowk_mdgaa, twowk.mdgsaa as twowk_mdgsaa,
                        (twowk.ld_shots_against / twowk.toi * 60) as twowk_ldsa_p60,
                        (twowk.ld_saves / twowk.toi * 60) as twowk_lds_p60, twowk.ldsv_pct as twowk_ldsv_pct, twowk.ldgaa as twowk_ldgaa, twowk.ldgsaa as twowk_ldgsaa,
                        gst.gp as gst_games_played, gst.toi as gst_time_on_ice, (gst.shots_against / gst.toi * 60) as gst_sa_p60,
                        (gst.saves / gst.toi * 60) as gst_saves_p60, gst.gaa as gst_gaa, gst.sv_pct as gst_sv_pct,
                        gst.gsaa as gst_gsaa, (gst.xg_against / gst.toi * 60) as gst_xga_p60, (gst.hd_shots_against / gst.toi * 60) as gst_hdsa_p60,
                        (gst.hd_saves / gst.toi * 60) as gst_hds_p60, gst.hdsv_pct as gst_hdsv_pct, gst.hdgaa as gst_hdgaa, gst.hdgsaa as gst_hdgsaa,
                        (gst.md_shots_against / gst.toi * 60) as gst_mdsa_p60,
                        (gst.md_saves / gst.toi * 60) as gst_mds_p60, gst.mdsv_pct as gst_mdsv_pct, gst.mdgaa as gst_mdgaa, gst.mdgsaa as gst_mdgsaa,
                        (gst.ld_shots_against / gst.toi * 60) as gst_ldsa_p60,
                        (gst.ld_saves / gst.toi * 60) as gst_lds_p60, gst.ldsv_pct as gst_ldsv_pct, gst.ldgaa as gst_ldgaa, gst.ldgsaa as gst_ldgsaa,
                        ggd.shots_faced as res_shots_faced, ggd.saves as res_saves, ggd.save_pct as res_save_pct,
                        (ggd.shots_faced - ggd.saves) as res_goals_allowed
             FROM   games g, goalie_game_data ggd, goalie_two_wk_totals twowk, goalie_season_totals gst
             WHERE  g.id = ggd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    ggd.player_name = gst.player_name
             and    twowk.player_name = gst.player_name
             and    gst.date = DATE(g.date, '-1 day')
             and    twowk.date = gst.date"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)
    X = df.drop(columns = ['res_shots_faced', 'res_saves', 'res_save_pct', 'res_goals_allowed'])
    Y = df[['res_shots_faced', 'res_saves', 'res_save_pct', 'res_goals_allowed']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split
    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linear_Regression_GoalieSeasonTwoWkTotals' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))

def trainGoalieSeasonTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT   gst.gp as gst_games_played, gst.toi as gst_time_on_ice, (gst.shots_against / gst.toi * 60) as gst_sa_p60,
                        (gst.saves / gst.toi * 60) as gst_saves_p60, gst.gaa as gst_gaa, gst.sv_pct as gst_sv_pct,
                        gst.gsaa as gst_gsaa, (gst.xg_against / gst.toi * 60) as gst_xga_p60, (gst.hd_shots_against / gst.toi * 60) as gst_hdsa_p60,
                        (gst.hd_saves / gst.toi * 60) as gst_hds_p60, gst.hdsv_pct as gst_hdsv_pct, gst.hdgaa as gst_hdgaa, gst.hdgsaa as gst_hdgsaa,
                        (gst.md_shots_against / gst.toi * 60) as gst_mdsa_p60,
                        (gst.md_saves / gst.toi * 60) as gst_mds_p60, gst.mdsv_pct as gst_mdsv_pct, gst.mdgaa as gst_mdgaa, gst.mdgsaa as gst_mdgsaa,
                        (gst.ld_shots_against / gst.toi * 60) as gst_ldsa_p60,
                        (gst.ld_saves / gst.toi * 60) as gst_lds_p60, gst.ldsv_pct as gst_ldsv_pct, gst.ldgaa as gst_ldgaa, gst.ldgsaa as gst_ldgsaa,
                        ggd.shots_faced as res_shots_faced, ggd.saves as res_saves, ggd.save_pct as res_save_pct,
                        (ggd.shots_faced - ggd.saves) as res_goals_allowed
             FROM   games g, goalie_game_data ggd, goalie_season_totals gst
             WHERE  g.id = ggd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    ggd.player_name = gst.player_name
             and    gst.date = DATE(g.date, '-1 day')"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)
    X = df.drop(columns = ['res_shots_faced', 'res_saves', 'res_save_pct', 'res_goals_allowed'])
    Y = df[['res_shots_faced', 'res_saves', 'res_save_pct', 'res_goals_allowed']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split
    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linear_Regression_GoalieSeasonTotals' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))


def trainGoalieSeasonTwoWkOppTeamTotalsModel():
    linreg = LinearRegression()
    conn = utils.establishDatabaseConnection("main.db")

    query = """SELECT  twowk.gp as twowk_games_played, twowk.toi as twowk_time_on_ice, (twowk.shots_against / twowk.toi * 60) as twowk_sa_p60,
                        (twowk.saves / twowk.toi * 60) as twowk_saves_p60, twowk.gaa as twowk_gaa, twowk.sv_pct as twowk_sv_pct,
                        twowk.gsaa as twowk_gsaa, (twowk.xg_against / twowk.toi * 60) as twowk_xga_p60, (twowk.hd_shots_against / twowk.toi * 60) as twowk_hdsa_p60,
                        (twowk.hd_saves / twowk.toi * 60) as twowk_hds_p60, twowk.hdsv_pct as twowk_hdsv_pct, twowk.hdgaa as twowk_hdgaa, twowk.hdgsaa as twowk_hdgsaa,
                        (twowk.md_shots_against / twowk.toi * 60) as twowk_mdsa_p60,
                        (twowk.md_saves / twowk.toi * 60) as twowk_mds_p60, twowk.mdsv_pct as twowk_mdsv_pct, twowk.mdgaa as twowk_mdgaa, twowk.mdgsaa as twowk_mdgsaa,
                        (twowk.ld_shots_against / twowk.toi * 60) as twowk_ldsa_p60,
                        (twowk.ld_saves / twowk.toi * 60) as twowk_lds_p60, twowk.ldsv_pct as twowk_ldsv_pct, twowk.ldgaa as twowk_ldgaa, twowk.ldgsaa as twowk_ldgsaa,
                        gst.gp as gst_games_played, gst.toi as gst_time_on_ice, (gst.shots_against / gst.toi * 60) as gst_sa_p60,
                        (gst.saves / gst.toi * 60) as gst_saves_p60, gst.gaa as gst_gaa, gst.sv_pct as gst_sv_pct,
                        gst.gsaa as gst_gsaa, (gst.xg_against / gst.toi * 60) as gst_xga_p60, (gst.hd_shots_against / gst.toi * 60) as gst_hdsa_p60,
                        (gst.hd_saves / gst.toi * 60) as gst_hds_p60, gst.hdsv_pct as gst_hdsv_pct, gst.hdgaa as gst_hdgaa, gst.hdgsaa as gst_hdgsaa,
                        (gst.md_shots_against / gst.toi * 60) as gst_mdsa_p60,
                        (gst.md_saves / gst.toi * 60) as gst_mds_p60, gst.mdsv_pct as gst_mdsv_pct, gst.mdgaa as gst_mdgaa, gst.mdgsaa as gst_mdgsaa,
                        (gst.ld_shots_against / gst.toi * 60) as gst_ldsa_p60,
                        (gst.ld_saves / gst.toi * 60) as gst_lds_p60, gst.ldsv_pct as gst_ldsv_pct, gst.ldgaa as gst_ldgaa, gst.ldgsaa as gst_ldgsaa,
                        ggd.shots_faced as res_shots_faced, ggd.saves as res_saves, ggd.save_pct as res_save_pct,
                        (ggd.shots_faced - ggd.saves) as res_goals_allowed,
                        
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_point_pct
                            ELSE g.h_point_pct
                            END AS opp_team_point_pct, 
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_cf_pct
                            ELSE g.h_cf_pct
                            END AS opp_cf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ff_pct
                            ELSE g.h_ff_pct
                            END AS opp_ff_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sf_pct
                            ELSE g.h_sf_pct
                            END AS opp_sf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_gf_pct
                            ELSE g.h_gf_pct
                            END AS opp_gf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_xgf_pct
                            ELSE g.h_xgf_pct
                            END AS opp_xgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scf_pct
                            ELSE g.h_scf_pct
                            END AS opp_scf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsf_pct
                            ELSE g.h_scsf_pct
                            END AS opp_scsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scgf_pct
                            ELSE g.h_scgf_pct
                            END AS opp_scgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsh_pct
                            ELSE g.h_scsh_pct
                            END AS opp_scsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_scsv_pct
                            ELSE g.h_scsv_pct
                            END AS opp_scsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsf_pct
                            ELSE g.h_hdsf_pct
                            END AS opp_hdsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdgf_pct
                            ELSE g.h_hdgf_pct
                            END AS opp_hdgf_pct,   
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsh_pct
                            ELSE g.h_hdsh_pct
                            END AS opp_hdsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_hdsv_pct
                            ELSE g.h_hdsv_pct
                            END AS opp_hdsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsf_pct
                            ELSE g.h_mdsf_pct
                            END AS opp_mdsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdgf_pct
                            ELSE g.h_mdgf_pct
                            END AS opp_mdgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsh_pct
                            ELSE g.h_mdsh_pct
                            END AS opp_mdsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_mdsv_pct
                            ELSE g.h_mdsv_pct
                            END AS opp_mdsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsf_pct
                            ELSE g.h_ldsf_pct
                            END AS opp_ldsf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldgf_pct
                            ELSE g.h_ldgf_pct
                            END AS opp_ldgf_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsh_pct
                            ELSE g.h_ldsh_pct
                            END AS opp_ldsh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_ldsv_pct
                            ELSE g.h_ldsv_pct
                            END AS opp_ldsv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sh_pct
                            ELSE g.h_sh_pct
                            END AS opp_sh_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_sv_pct
                            ELSE g.h_sv_pct
                            END AS opp_sv_pct,    
                    CASE WHEN (t.name = g.away_team)
                            THEN g.a_PDO
                            ELSE g.h_PDO
                            END AS opp_PDO
             FROM   games g, goalie_game_data ggd, goalie_two_wk_totals twowk, goalie_season_totals gst, teams t
             WHERE  g.id = ggd.game_id
             and    g.date >= (?)
             and    g.date <= (?)
             and    ggd.player_name = gst.player_name
             and    twowk.player_name = gst.player_name
             and    gst.date = DATE(g.date, '-1 day')
             and    twowk.date = gst.date
             and    t.id = ggd.opponent_team_id"""
    start_date = "2022-10-26"
    end_date = "2023-04-07" 
    query_params = (start_date, end_date)
    df = pd.read_sql_query(query, conn, params = query_params)
    print(df.shape[0])
    # Clean data
    df.replace(to_replace='-', value=0, inplace=True)
    df.replace(to_replace=[None], value=0, inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace('inf', np.nan, inplace=True)
    df.fillna(0,inplace=True)
    X = df.drop(columns = ['res_shots_faced', 'res_saves', 'res_save_pct', 'res_goals_allowed'])
    Y = df[['res_shots_faced', 'res_saves', 'res_save_pct', 'res_goals_allowed']]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=7) # 80%/20% training/test split
    linreg.fit(X_train,Y_train)
    predict = linreg.predict(X_test)

    print("R2:")
    print(r2_score(Y_test,predict))
    print("MSE:")
    print(mean_squared_error(Y_test, predict))
    print("RMSE:")
    print(math.sqrt(mean_squared_error(Y_test, predict)))
    r_sq_score = round(r2_score(Y_test,predict), 3)
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d",backdate = None)
    filename = 'Linear_Regression_GoalieSeasonTwoWkOppTeamTotals' + str(r_sq_score) + '_'+ datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))
#Linear regressions    
#trainSkaterSeasonAndTwoWkTotalsModel()
#testModelPrediction()
#trainSkaterSeasonTotalsModel()
#trainSkaterSeasonPPTwoWkTotalsModel()
#trainSkaterSeasonPPTwoWkOppGoalieTotalsModel()
#trainSkaterSeasonTwoWkOppGoalieOppTeamTotalsModel()
#trainSkaterSeasonTwoWkOppGoalieSigOppTeamTotalsModel()

#Linear regression goalies
#trainGoalieSeasonAndTwoWkTotalsModel()
#trainGoalieSeasonTotalsModel()
#trainGoalieSeasonTwoWkOppTeamTotalsModel()

#Decision trees
# dtTrainSkaterSeasonAndTwoWkTotalsModel()
# dtTrainSkaterSeasonTotalsModel()
# dtTrainSkaterSeasonPPTwoWkOppGoalieTotalsModel()
# dtTrainSkaterSeasonTwoWkOppGoalieOppTeamTotalsModel()