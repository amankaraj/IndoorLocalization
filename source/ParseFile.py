__author__ = 'Aman'

from os import walk
import re

def readAllFiles(folderPath):
    listOfFiles = []
    for (dirpath, dirnames, filenames) in walk(folderPath):

        listOfFiles.extend(filenames)

    allRows = []
    for fileName in listOfFiles:
        if fileName == 'data.txt':
            file = open(folderPath + fileName)
            listLinesFile = file.readlines()
            foo(listLinesFile,allRows)


    return allRows


def foo(listLinesFile,listRows):

    count = 0
    while count < len(listLinesFile):
        currRow = {}
        count = count + 2
        curr = listLinesFile[count].split(" ")
        currRow["latitude"] = curr[1]
        currRow["longitude"] = curr[2]

        count = count + 1
        curr = listLinesFile[count].split(" ")
        currRow["GSM"] = curr[2]

        count = count + 1
        curr = listLinesFile[count].split(" ")
        currRow["T0"] = curr[3]
        currRow["T0LAC"] = curr[5]
        currRow["T0RSSI"] = curr[7]

        count = count + 1
        curr = listLinesFile[count].split(" ")
        currRow["T1"] = curr[3]
        currRow["T1LAC"] = curr[5]
        currRow["T1RSSI"] = curr[7]

        count = count + 1
        curr = listLinesFile[count].split(" ")
        currRow["T2"] = curr[3]
        currRow["T2LAC"] = curr[5]
        currRow["T2RSSI"] = curr[7]

        count = count + 1
        curr = listLinesFile[count].split(" ")
        currRow["T3"] = curr[3]
        currRow["T3LAC"] = curr[5]
        currRow["T3RSSI"] = curr[7]



        count = count + 1
        curr = listLinesFile[count].split(" ")
        currRow["T4"] = curr[3]
        currRow["T4LAC"] = curr[5]
        currRow["T4RSSI"] = curr[7]

        count = count + 1
        listRows.append(currRow)

    return listRows

# def parseFileToList(listLinesFile):
#
#     print listLinesFile
#     list = []
#     count = 1
#     while count < len(listLinesFile):
#         dictRow = {}
#         while True:
#             line = listLinesFile[count]
#             count = count + 1
#             if line.count('_') == 3:
#                 print line
#                 break
#             splitLine = line.rstrip()
#             if re.search("Loc: ",line):
#                 sp = line.split(":")
#                 dictRow["Loc"] =
#
#         print "------------"
#             #splitLine = line.rstrip()
#             # x = re.findall('^EDGE Cell.*: [0-9.]+', line)
#             # x = re.findall(r'\d+',line)
#             # if len(x) > 0:
#             #     # p = x[0].split(" ")
#             #     # print p
#             #     print x


def getTrainingData():
    allRows = readAllFiles("/Users/Aman/Desktop/Projects/IndoorLocalization/Data/")

    trainingData = []
    for dictR in allRows:
        row = []
        for key in dictR.keys():
            row.append(dictR[key])
        trainingData.append(row)


    return trainingData

getTrainingData()