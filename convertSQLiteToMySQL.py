import re, fileinput
from os import path
import sys
from datetime import date,timedelta, datetime

def main():
    basepath = path.dirname(__file__)
    todays_date = getTodaysDate("%Y-%m-%d %H-%M-%S")
    todays_date = todays_date + '.txt'
    sys.stdout = open(todays_date, 'w')
    files = ['main.db.sql']
    fs = fileinput.FileInput(files)
    with fs as opened:
        for line in opened:
            process = False
            for nope in ('BEGIN TRANSACTION','COMMIT',
                        'sqlite_sequence','CREATE UNIQUE INDEX'):
                if nope in line: 
                    break
                else:
                    process = True
            if not process: continue
            m = re.search('CREATE TABLE "([a-z_]*)"(.*)', line)
            if m:
                name, sub = m.groups()
                line = '''DROP TABLE IF EXISTS %(name)s;
        CREATE TABLE IF NOT EXISTS %(name)s%(sub)s
        '''
                line = line % dict(name=name, sub=sub)
            else:
                m = re.search('INSERT INTO "([a-z_]*)"(.*)', line)
                if m:
                    line = 'INSERT INTO %s%s\n' % m.groups()
                    line = line.replace('"', r'\"')
                    line = line.replace('"', "'")
            line = re.sub(r"([^'])'t'(.)", r"\1THIS_IS_TRUE\2", line)
            line = line.replace('THIS_IS_TRUE', '1')
            line = re.sub(r"([^'])'f'(.)", r"\1THIS_IS_FALSE\2", line)
            line = line.replace('THIS_IS_FALSE', '0')
            line = line.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
            print(line)

def getTodaysDate(format = "%Y-%m-%d",backdate = None):
    today = datetime.now()
    if backdate is True:
        today = today - timedelta(days=1)
    return today.strftime(format)

main()