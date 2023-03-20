from downloadCsv import downloadPlayerSeasonStats, downloadTeamStats, downloadPlayerLastTwoWkStats
from upload import uploadGameResultsAndTeamStats
from getNHLData import uploadNHLPlayerGameDataToDatabase, uploadNHLPlayerSeasonDataToDatabase, uploadNHLPlayerTwoWkSeasonDataToDatabase
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
try:
    uploadGameResultsAndTeamStats()
except Exception as e:
    print("Error in uploadGameResultsAndTeamStats")
    print(e)
try:
    uploadNHLPlayerGameDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerGameDataToDatabase")
    print(e)
try:
    uploadNHLPlayerSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerSeasonDataToDatabase")
    print(e)
try:
    uploadNHLPlayerTwoWkSeasonDataToDatabase("main.db")
except Exception as e:
    print("Error in uploadNHLPlayerTwoWkSeasonDataToDatabase")
    print(e)


sys.stdout.close()