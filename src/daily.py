import downloadCsv
from upload import uploadGameResultsAndTeamStats
import getNHLData
from utils import getTodaysDate
#from predictions import predictSlate, scorePredictions
import sys
from os import path, startfile
basepath = path.dirname(__file__)
todays_date = getTodaysDate("%Y-%m-%d %H-%M-%S")
todays_date = todays_date + '.txt'
filepath = path.abspath(path.join(basepath, "..", "data/daily logs", todays_date))
sys.stdout = open(filepath, 'w')

downloadCsv.downloadPlayerSeasonStats(today = True, date = None, file_date = None) # downloads player season stats file
downloadCsv.downloadTeamStats(today = True, date = None, file_date = None)
downloadCsv.downloadPlayerLastTwoWkStats(True, None, None)
downloadCsv.downloadGoalieSeasonStats(True, None, None)
downloadCsv.downloadGoalieLastTwoWkStats(True, None, None)
downloadCsv.downloadPlayerPowerplaySeasonStats(True, None, None)

try:                                                     ## Game results to DB
    uploadGameResultsAndTeamStats()
except Exception as e:
    print("Error in uploadGameResultsAndTeamStats")
    print(e)
try:                                                     ## Player Game Data to DB
    getNHLData.uploadNHLPlayerGameDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerGameDataToDatabase")
    print(e)
try:                                                     ## Player Season Data to DB
    getNHLData.uploadNHLPlayerSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerSeasonDataToDatabase")
    print(e)
try:                                                     ## Player Two Week Season Data to DB
    getNHLData.uploadNHLPlayerTwoWkSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerTwoWkSeasonDataToDatabase")
    print(e)
try:                                                     ## Goalie Season Data to DB
    getNHLData.uploadNHLGoalieSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLGoalieSeasonDataToDatabase")
    print(e)
try:                                                     ## Goalie Two Week Data to DB
    getNHLData.uploadNHLGoalieTwoWkDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLGoalieTwoWkDataToDatabase")
    print(e)
try:                                                     ## Skater PP Season Data to DB
    getNHLData.uploadNHLPlayerPPSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerPPSeasonDataToDatabase")
    print(e)



sys.stdout.close()
startfile(filepath)