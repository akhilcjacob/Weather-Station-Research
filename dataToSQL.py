#!/usr/bin/python
# -*- coding: utf-8 -*-

# import MySQLdb as db

import datetime
import os
import sys
import string
import time


def main():
    clearData = False
    #filePath ='/home/mccolga/weather_station/'
    filePath = '/Users/Akhil/Desktop/weather_station-master/'
    pathToData = filePath #change if data is in different location
    
    fileName = 'testData.txt' #name of the data file

    fileLoc = pathToData + fileName
    try:
        with open(fileLoc, 'r') as f:
            fileData = f.read()

        # conn = MySQLdb.connect (host = "localhost", user = "username",passwd = "password", db = "db")
        # cur = connection.cursor()
        # cur.execute("CREATE TABLE IF NOT EXISTS WEATHER_DATA (need to put format of table)")
        
        if len(fileData) != 0:
            backupFile(filePath, fileData)
            lines = fileData.split('\n')
            weatherData = lines[3:]
            for x in range(len(weatherData) - 1):
                weatherData[x] = convertToSQL(weatherData[x])
                
            for counter in range(0, len(weatherData) - 1):
                string = 'INSERT INTO weather VALUES(' + str((weatherData[counter])[0:]) + ');'
                # cur.execute(string)
                
            if clearData:
                clearFile(fileLoc)
                
        else:
            errorWriter(filePath, 'EMPTY FILE!!!!')
            sys.exit(1)
            
    except Exception, e:
        errorWriter(filePath, str(e) + '\n' + str(sys.exc_info()[:]))
        pass


##################################################################

def errorWriter(filePath, error):
    string = str(datetime.datetime.now()).split()
    string = string[0] + '_' + string[1]
    if not os.path.exists(filePath + '/ERROR_FILES'):
        os.makedirs(filePath + '/ERROR_FILES')
    errorFile = open(filePath + '/ERROR_FILES/' + string
                     + '_Error_file.txt', 'w')
    errorFile.write(str(datetime.datetime.now()) + '---' + str(error))
    errorFile.close()
    print 'Something went wrong check error file at ' + filePath+ 'ERROR_FILES/' + string + '_Error_file.txt'


def convertToSQL(line):
    line = line.split()
    x = 0
    if len(line) > 0:
        for x in range(len(line) - 1):
            if x == 1:
                line[0] = datetime.datetime.strptime(line[0], '%m/%d/%y').strftime('%Y-%m-%d')
                line[1] = convertTime(line[1])

        line[len(line) - 1] = '\'' + str(line[len(line) - 1]) + '\''
        for x in range(len(line) - 1):
            line[x] = str('\'' + str(line[x]) + '\'')
        line = ','.join(line)
        return line
    else:
        temp = ["\'NULL\'"] * 37
        return temp


def convertTime(time):
    length = len(time)
    timeSet = time[length - 1]
    time = time[0:length - 1]
    if timeSet == 'a':
        timeSet = ' AM'
    elif timeSet == 'p':

        timeSet = ' PM'

    time = datetime.datetime.strptime(time + timeSet, '%I:%M %p'
            ).strftime('%H:%M')
    return time


def clearFile(path):
    open(path, 'w').close()
    print 'Cleared File'


def backupFile(path, lines):
    if not os.path.exists(path + '/Backup_files'):
        os.makedirs(path + '/Backup_files')
    print 'File backed up at ' + path + 'Backup_files'
    file = open(path + 'Backup_files/backupFile.txt', 'a')
    file.write(lines)
    file.close()


if __name__ == '__main__':
    main()

# query = "INSERT INTO weather VALUES( (%s))" % ','.join('?' * len(params))
# cur.execute("INSERT INTO weather VALUES("+str(tempArr)+ " )")
# cur.execute('INSERT INTO table (ColName) VALUES (?);', [','.join(list)])

			
