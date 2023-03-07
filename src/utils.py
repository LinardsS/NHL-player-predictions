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

def setAverageIfNull(value, average):
    if pd.isna(value):
        value = average
    
    return value

def getTeamStatsAverages():
    dict = {
        'h_point%' : 0.550496,
        'h_cf%' : 49.941055,
        'h_ff%' : 49.961178,
        'h_sf%' : 49.993914,
        'h_gf%' : 50.066977,
        'h_xgf%' :   50.017941,
        'h_scf%' :   49.995041,
        'h_scsf%' :  50.105400,
        'h_scgf%' :  50.163279,
        'h_scsh%' :  13.111916,
        'h_scsv%' :  86.841732,
        'h_hdsf%' :  50.117018,
        'h_hdgf%' :  50.397469,
        'h_hdsh%' :  16.938781,
        'h_hdsv%' :  83.127910,
        'h_mdsf%' :  50.084078,
        'h_mdgf%' :  50.666351,
        'h_mdsh%' :  9.383330,
        'h_mdsv%' :  90.484283,
        'h_ldsf%' :  49.884191,
        'h_ldgf%' :  49.910778,
        'h_ldsh%' :  3.088607,
        'h_ldsv%' :  96.897930,
        'h_sh%' : 8.364385,
        'h_sv%' : 91.600133,
        'h_PDO' : 0.999647,
        'a_point%' : 0.552016,
        'a_cf%' : 49.942941,
        'a_ff%' : 49.926814,
        'a_sf%' : 49.898207,
        'a_gf%' : 50.193484,
        'a_xgf%' :   49.843627,
        'a_scf%' :   49.870205,
        'a_scsf%' :  49.786025,
        'a_scgf%' :  50.306967,
        'a_scsh%' :  13.203648,
        'a_scsv%' :  87.045492,
        'a_hdsf%' :  49.770359,
        'a_hdgf%' :  50.180616,
        'a_hdsh%' :  16.860635,
        'a_hdsv%' :  83.282592,
        'a_mdsf%' :  49.826680,
        'a_mdgf%' :  51.604422,
        'a_mdsh%' :   9.624395,
        'a_mdsv%' :  90.769549,
        'a_ldsf%' :  50.007787,
        'a_ldgf%' :  50.330062,
        'a_ldsh%' :   3.067807,
        'a_ldsv%' :  96.899826,
        'a_sh%' :  8.392602,
        'a_sv%' : 91.692623,
        'a_PDO' :  1.000852
    }

    return dict

def convertTimeStringToMinutes(time_string):
    if ':' in time_string:
        m, s = time_string.split(':')
        return int(m) + int(s)/60
    else:
        return time_string