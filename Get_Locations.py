import datetime
import re
import glob
import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta, MO


# This is used to parse a list, [[Location, Suburb][Location, Suburb]] to [Location, Suburb][Location, Suburb]
# Just a heads up this Isn't my own code stack overflow I believe
def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def write(inWeek, day, dayN):
    inWeek = inWeek[:len(inWeek)-len(".txt")]

    filePath = "./Parsed/" + str(inWeek) + "/"
    directory = os.path.dirname(filePath)

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    filePath = "./Parsed/" + str(inWeek) + "/" + dayN
    directory = os.path.dirname(filePath)

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    f = open(filePath, "w+")

# Starting at 1 as the cops changed the format so that the date appears as date (large space) then the day
    for i in range(1, len(day)):
        f.write(day[i][1] + ",  \t" + day[i][0])
        f.write("\n")

    f.close()
# Re-sorts the file as Location is before Street with the new pre-proccessing
    os.system("sort " + filePath + " -o " + filePath)


# Goes to police website downloads the data, converts .pdf to .txt, and makes a backup of the .txt, and cleans up
def getData():
    today = date.today()
    next_Monday = today + relativedelta(weekday=MO(+1))
    monday = next_Monday.strftime("%d%m20%y")

    raw_date_Monday = datetime.datetime.strptime(monday, "%d%m%Y")
    raw_date_Sunday = raw_date_Monday + datetime.timedelta(days=6)

    holder_Date = raw_date_Sunday
    date_Sunday = holder_Date.strftime('%d%m%Y')

    holder_Date = raw_date_Monday
    date_Monday = holder_Date.strftime('%d%m%Y')

    url = "https://www.police.wa.gov.au/~/media/Files/Police/Traffic/Cameras/Camera-Locations/MediaLocations-" + date_Monday + "-to-" + date_Sunday + ".pdf?la=en"
    r = requests.get(url, stream=True)

# If the size is smaller then the file is empty
    if(len(r.content) > 27580):
        with open("./" + date_Monday + ".pdf", 'wb') as f:
            f.write(r.content)

        os.system("pdftotext -layout ./" + date_Monday + ".pdf")
        os.system("cp ./" + date_Monday + ".txt" + " " + "./Backups")

        os.system("rm -f ./" + date_Monday + ".pdf")

    else:
        print("DATA NOT WRITTEN, TRY AGAIN LATER")


# This Reads all the text files in the dir
def txt():
    os.chdir("./")
    for file in glob.glob("*.txt"):
        main(file)


# reads the data in the text file, parses it, then writes it to a file
def main(inFile):
    inputFile = inFile
    week = []
    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    saturday = []
    sunday = []
    day = 0

    if os.path.isfile(inputFile):
        f = open(inputFile, "r")
        inLines = f.readlines()
        f.close()

        os.system("rm -f " + inputFile)

        raw_Dictionary = {}

# Yes... Its a dictionary, should you use a list, yes. can you. No. I assume it has something to do with the structure of the text.
        for i in range(0, len(inLines)):
            inLines[i] = re.sub(r"[ \t]{2,}", r", ", inLines[i].rstrip())
            raw_Dictionary[i] = inLines[i].split(", ")

        for i in range(0, len(raw_Dictionary)):
            if (len(raw_Dictionary[i]) > 0) and raw_Dictionary[i][0] != "":
                if(len(raw_Dictionary[i][0]) > 0):
                    if(raw_Dictionary[i][0] == "Street Name"):
                        raw_Dictionary[i] = [""]

                    if(raw_Dictionary[i][0] == "Location"):
                        raw_Dictionary[i] = [""]

                    if(len(raw_Dictionary[i]) > 2):
                        if(raw_Dictionary[i][2] == "Location"):
                            raw_Dictionary[i] = [""]

# Crashes if list isn't "declared"
        parsed_List = []
        parsed_List = list(raw_Dictionary.values())

        i = 0
        while i < len(parsed_List):
            if("" in parsed_List[i]):
                del parsed_List[i]
            else:
                i += 1

# Sets a day value based on the last day thats been read
        for i in range(0, len(parsed_List)):
            if("Monday" in parsed_List[i][0]):
                day = 0
            if("Tuesday" in parsed_List[i][0]):
                day = 1
            if("Wednesday" in parsed_List[i][0]):
                day = 2
            if("Thursday" in parsed_List[i][0]):
                day = 3
            if("Friday" in parsed_List[i][0]):
                day = 4
            if("Saturday" in parsed_List[i][0]):
                day = 5
            if("Sunday" in parsed_List[i][0]):
                day = 6

# this converts the, Street, Location, Street, Location into two lines and adds the day variable ie: 1, Street, Location \n 1, Street, Location.
            if(len(parsed_List[i]) > 3):
                holder = split(parsed_List[i], 2)
                holder[0].insert(0, day)
                holder[1].insert(0, day)
                week.insert(i, holder[1])
                week.insert(i, holder[0])

            if(len(parsed_List[i]) == 2):
                parsed_List[i].insert(0, day)
                week.insert(i, parsed_List[i])

# Moves data from week to the specific day
        for i in range(0, len(week)):
            if(week[i][0] == "Location"):
                del week[i]

            if(week[i][0] == 0):
                week[i].pop(0)
                monday.append(week[i])

            if(week[i][0] == 1):
                week[i].pop(0)
                tuesday.append(week[i])

            if(week[i][0] == 2):
                week[i].pop(0)
                wednesday.append(week[i])

            if(week[i][0] == 3):
                week[i].pop(0)
                thursday.append(week[i])

            if(week[i][0] == 4):
                week[i].pop(0)
                friday.append(week[i])

            if(week[i][0] == 5):
                week[i].pop(0)
                saturday.append(week[i])

            if(week[i][0] == 6):
                week[i].pop(0)
                sunday.append(week[i])

# write() prints data to file in dir Parsed
        write(inFile, monday, "Monday")
        write(inFile, tuesday, "Tuesday")
        write(inFile, wednesday, "Wednesday")
        write(inFile, thursday, "Thursday")
        write(inFile, friday, "Friday")
        write(inFile, saturday, "Saturday")
        write(inFile, sunday, "Sunday")


getData()
txt()
