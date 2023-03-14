from downloadCsv import downloadPlayerSeasonStats, downloadTeamStats, downloadPlayerLastTwoWkStats
from upload import uploadGameResultsAndTeamStats
from getNHLData import uploadNHLPlayerGameDataToDatabase, uploadNHLPlayerSeasonDataToDatabase
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
uploadGameResultsAndTeamStats()
uploadNHLPlayerGameDataToDatabase("main.db")
uploadNHLPlayerSeasonDataToDatabase("main.db")


sys.stdout.close()