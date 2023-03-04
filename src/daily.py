from downloadCsv import downloadPlayerSeasonStats
#from uploadResults import uploadResultsAndStats
from utils import getTodaysDate, getTomorrowsDate
#from predictions import predictSlate, scorePredictions
import sys
from os import path
basepath = path.dirname(__file__)
todays_date = getTodaysDate()
todays_date = todays_date + '.txt'
filepath = path.abspath(path.join(basepath, "..", "data/daily logs", todays_date))
sys.stdout = open(filepath, 'w')

downloadPlayerSeasonStats(today = True, date = None, file_date = None) # downloads team stats file
#uploadResultsAndStats()


sys.stdout.close()