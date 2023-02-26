import numpy as np
from datetime import date,timedelta, datetime
import pandas as pd
from os import path

def getTodaysDate(format = "%Y-%m-%d",backdate = None):
    today = date.today()
    if backdate is True:
        today = today - timedelta(days=1)
    return today.strftime(format)

def getYesterdaysDate(format = "%Y-%m-%d"):
    yesterday = date.today() - timedelta(1)
    return yesterday.strftime(format)

def getTomorrowsDate(format = "%Y-%m-%d"):
    tomorrow = date.today() + timedelta(1)
    return tomorrow.strftime(format)