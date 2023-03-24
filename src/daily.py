from downloadCsv import downloadPlayerSeasonStats, downloadTeamStats, downloadPlayerLastTwoWkStats, downloadGoalieSeasonStats
from upload import uploadGameResultsAndTeamStats
from getNHLData import uploadNHLPlayerGameDataToDatabase, uploadNHLPlayerSeasonDataToDatabase, uploadNHLPlayerTwoWkSeasonDataToDatabase, uploadNHLGoalieSeasonDataToDatabase
from utils import getTodaysDate, getTomorrowsDate
#from predictions import predictSlate, scorePredictions
import sys
from os import path
basepath = path.dirname(__file__)
todays_date = getTodaysDate("%Y-%m-%d %H-%M-%S")
todays_date = todays_date + '.txt'
filepath = path.abspath(path.join(basepath, "..", "data/daily logs", todays_date))
sys.stdout = open(filepath, 'w')

downloadPlayerSeasonStats(today = True, date = None, file_date = None) # downloads player season stats file
downloadTeamStats(today = True, date = None, file_date = None)
downloadPlayerLastTwoWkStats(True, None, None)
downloadGoalieSeasonStats(True, None, None)

try:                                                     ## Game results to DB
    uploadGameResultsAndTeamStats()
except Exception as e:
    print("Error in uploadGameResultsAndTeamStats")
    print(e)
try:                                                     ## Player Game Data to DB
    uploadNHLPlayerGameDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerGameDataToDatabase")
    print(e)
try:                                                     ## Player Season Data to DB
    uploadNHLPlayerSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerSeasonDataToDatabase")
    print(e)
try:                                                     ## Player Two Week Season Data to DB
    uploadNHLPlayerTwoWkSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerTwoWkSeasonDataToDatabase")
    print(e)
try:                                                     ## Goalie Season Data to DB
    uploadNHLGoalieSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLGoalieSeasonDataToDatabase")
    print(e)



sys.stdout.close()