from downloadCsv import downloadPlayerSeasonStats, downloadTeamStats
from upload import uploadResultsAndStats
from utils import getTodaysDate, getTomorrowsDate
#from predictions import predictSlate, scorePredictions
import sys
from os import path
basepath = path.dirname(__file__)
todays_date = getTodaysDate()
todays_date = todays_date + '.txt'
filepath = path.abspath(path.join(basepath, "..", "data/daily logs", todays_date))
sys.stdout = open(filepath, 'w')

downloadPlayerSeasonStats(today = True, date = None, file_date = None) # downloads player season stats file
downloadTeamStats(today = True, date = None, file_date = None)
uploadResultsAndStats()


sys.stdout.close()