# Hurdat preprocessing

import nltk.tokenize
import re

stormLevels = {"Extratropical Storm": 1, "Tropical Depression": 1, "Tropical Storm":1,"Hurricane - Category 1":2 ,"Hurricane - Category 2": 3,"Major Hurricane - Category 3":4,  "Major Hurricane - Category 4":5, "Major Hurricane - Category 5":6, }
re_StormTypes = "Tropical Storm|Hurricane - Category 1|Hurricane - Category 2|Major Hurricane - Category 3|Major Hurricane - Category 4|Major Hurricane - Category 5|Topical Storm|Tropical Depression|Extratropical Storm"
re_Ops = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)|(~=)"
re_Storm_Name = "Storm [a-zA-Z]+ *is number *\d+ of the year \d+"
re_astrixs = "\*+"
re_tags = "Month    Day   Hour    Lat\.   Long\.     Dir\.    ----Speed-----   -----Wind------  Pressure  ------------Type-----------"

def strip_Spaces(hFile):
    retFile = []
    for l in hFile:
        if (l.strip() != ''):
            retFile.append(l.strip())
    return retFile

def strip_Comm(hurdat_File):
    hurdat_Sans_Multi_Line_Comm =re.sub("/\*[^*]*\*+(?:[^/*][^*]*\*+)*/","", hurdat_File)
    hurdat_Sans_Snlg_Line_Comm = re.sub("//.*","", hurdat_Sans_Multi_Line_Comm)
    hurdat_Sans_All_Comm = hurdat_Sans_Snlg_Line_Comm
    return hurdat_Sans_All_Comm

def printArray(arr):
    for line in arr:
        print(str(line))

def highestLevelStorm(levels):
    highestStr = ""
    highestInt = 0
    for stormIndex in levels:
        storm = stormIndex[0]
        if stormLevels.get(storm) > highestInt:
            highestStr = storm
            highestInt = stormLevels.get(storm)
    retVal = [highestStr, highestInt]
    return retVal

fileName = "HURDAT.txt"
fileObject = open(fileName, 'r')
HURDAT_file = fileObject.read()

hurdat_strip_com = strip_Comm(HURDAT_file)

hurdat_split = hurdat_strip_com.split('\n')

hurdat_Sans_White_Space = strip_Spaces(hurdat_split)
hurdat_Joined = '\n'.join([str(element) for element in hurdat_Sans_White_Space])
hurdat_lines = hurdat_Joined.split('\n')
hurdat_list = []
for line in hurdat_lines:
    hurdat_list.append(line)

allStorms = []
newStorm = []
maxStormLevel = []

for line in hurdat_lines:
    # print(line)
    if(re.findall(re_Storm_Name,line)):
        if len(newStorm) != 0:
            maxL = highestLevelStorm(maxStormLevel)
            newStorm.append(maxL[0])
            newStorm.append(maxL[1])
            allStorms.append(newStorm)
            newStorm = []
            maxStormLevel = []
        stormInfo = re.findall(re_Storm_Name,line)
        tokens = nltk.wordpunct_tokenize(line)
        newStorm.append(tokens[1])
        newStorm.append(tokens[4])
        newStorm.append(tokens[8])
    elif(re.findall(re_astrixs, line)):
         x = 0
    elif (re.findall(re_tags, line)):
        x = 0
    elif (re.findall(re_StormTypes, line)):
        stormLevel = re.findall(re_StormTypes, line)
        maxStormLevel.append(stormLevel)

maxL = highestLevelStorm(maxStormLevel)
newStorm.append(maxL[0])
newStorm.append(maxL[1])
allStorms.append(newStorm)
newStorm = []
maxStormLevel = []

yearInt = {}
yearCount = {}

for i in range(61):
    yearCount[str(i + 1950)] = 0

for i in range(61):
    yearInt[str(i + 1950)] = 0

for storm in allStorms:
    yearInt[str(storm[2])] += storm[4]
    yearCount[str(storm[2])] += 1

str00 = str(yearInt)
new00 = ""
for i in range(61):
    new00 += str(i+1950) + " " + str(yearInt[str(i + 1950)]) + " " + str(yearInt[str(i + 1950)]*150)    + " " + str(yearCount[str(i + 1950)]) + " " + str(yearCount[str(i + 1950)]*200) +"\n"

print(str(new00))

print(str())
strO = str(allStorms)
newO = ""
prevC = ""
for c in strO:
    if c == "," and prevC == "]":
        newO += "\n"
    elif c == "]":
        prevC = c
    elif c == "[":
        prevC = c
    elif c == ",":
        newO += " "
    elif c == " ":
        prevC = c
    elif c == "'":
        prevC = c
    else:
        newO += c
        prevC = c
    prevC = c

f = open("HURDAT_output.txt", "w")
f.write(str(newO))
f.close()

f = open("HURDAT_meta.txt","w")
f.write(str(new00))
f.close()
