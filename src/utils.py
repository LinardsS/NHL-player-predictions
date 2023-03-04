import numpy as np
from datetime import date,timedelta, datetime
import pandas as pd
import sqlite3
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

def establishDatabaseConnection(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)

    return conn