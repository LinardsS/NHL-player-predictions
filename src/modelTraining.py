import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os import path
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import statsmodels.api as sm
import pickle
import utils
import sqlite3

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
    
    #Save model
    datum = utils.getTodaysDate(format = "%Y-%m-%d %H-%M-%S",backdate = None)
    filename = 'Linear_Regression_' + datum + '.sav'
    pickle.dump(linreg, open(filename, 'wb'))

def loadModel(model_name):
    basepath = path.dirname(__file__)
    filename = model_name + ".sav"
    filepath = path.abspath(path.join(basepath, "..", filename))
    loaded_model = pickle.load(open(filepath, 'rb'))
    return loaded_model

def testModelPrediction():
    model = loadModel("Linear_Regression_2023-04-08 16-41-02")
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
             and    sst.player_name = 'Erik Karlsson'"""
    start_date = "2023-01-01"
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

#trainSkaterSeasonAndTwoWkTotalsModel()
testModelPrediction()