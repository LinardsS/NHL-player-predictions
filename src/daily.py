from downloadCsv import downloadPlayerSeasonStats, downloadTeamStats
from upload import uploadGameResultsAndTeamStats
from getNHLData import uploadNHLPlayerGameDataToDatabase
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
uploadGameResultsAndTeamStats()
uploadNHLPlayerGameDataToDatabase("main.db")


sys.stdout.close()