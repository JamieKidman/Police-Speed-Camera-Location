import datetime
import re
import glob
import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta, MO


# This is used to parse a list, [[Location, Suburb][Location, Suburb]] to [Location, Suburb][Location, Suburb]
# Just a heads up this Isn't my own code
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

    filePath = "/home/jamie/Documents/WebBusiness/Police/Parsed/" + str(inWeek) +"/"
    directory = os.path.dirname(filePath)

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    filePath = "/home/jamie/Documents/WebBusiness/Police/Parsed/" + str(inWeek) + "/" + dayN
    directory = os.path.dirname(filePath)

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    f = open(filePath, "w+")

#starting at 1 as the if they changed there format so that the date appears as date (large space) then the day
    for i in range(1, len(day)):
        f.write(day[i][1] + ",  \t" + day[i][0])
        f.write("\n")

    f.close()

    os.system("sort " + filePath + " -o " + filePath)


# Goes to police website downloads the data, converts .pdf to .txt, and makes backups of .txt's, and cleans up
def getData():
    today = date.today()
    nextMonday = today + relativedelta(weekday=MO(+1))
    monday = nextMonday.strftime("%d%m%Y")

    odateMon = datetime.datetime.strptime(monday, "%d%m%Y")
    odateSun = odateMon + datetime.timedelta(days=6)

    dt = odateSun
    dateSun = dt.strftime('%d%m%Y')

    dt = odateMon
    dateMon = dt.strftime('%d%m%Y')

# Fixed it properly so that even if they change the url the program will still run
# Assumes that the first pdf file is the pdf it wants.
    os.system("curl https://www.police.wa.gov.au/Traffic/Cameras/Camera-locations | grep .pdf? > /home/jamie/Documents/WebBusiness/Police/haystack")
    haystack = open("/home/jamie/Documents/WebBusiness/Police/haystack", "r")

    url = "https://www.police.wa.gov.au/" + haystack.read().split("\"")[1]
    r = requests.get(url, stream=True)

    # dateMon = (re.findall(r"[0-9]{6}", url)[0])
    print(dateMon)

    # If the size is less than 27580 then something is wrong found by manual debugging
    if(len(r.content) > 27580):
        with open("/home/jamie/Documents/WebBusiness/Police/" + dateMon + ".pdf", 'wb') as f:
            f.write(r.content)

        #The layout option for pdftotext was used as it made the data easier to parse
        os.system("pdftotext -layout /home/jamie/Documents/WebBusiness/Police/" + dateMon + ".pdf")
        os.system("cp /home/jamie/Documents/WebBusiness/Police/" + dateMon + ".txt" + " " + "/home/jamie/Documents/WebBusiness/Police/Backups")

        os.system("rm -f /home/jamie/Documents/WebBusiness/Police/" + dateMon + ".pdf")
    
    else:
        print("DATA NOT WRITTEN, TRY AGAIN LATER")


# So far this reads all the text files in the dir good for bulk ingest, but could cause issues so NB
def txt():
    os.chdir("/home/jamie/Documents/WebBusiness/Police/")
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

        rawD = {}
        rawL = []


        # This isnt very pythonic and is C and Java like with the for loop indexes. Could also make parsing another function.
        for i in range(0, len(inLines)):
            inLines[i] = re.sub(r"[ \t]{2,}", r", ", inLines[i].rstrip())
            rawD[i] = inLines[i].split(", ")

        for i in range(0, len(rawD)):
            if (len(rawD[i]) > 0) and rawD[i][0] != "":
                if(len(rawD[i][0]) > 0):
                    if(rawD[i][0] == "Street Name"):
                        rawD[i] = [""]

                    if(rawD[i][0] == "Location"):
                        rawD[i] = [""]

                    if(len(rawD[i]) > 2):
                        if(rawD[i][2] == "Location"):
                            rawD[i] = [""]


        rawL = list(rawD.values())

        i = 0
        while i < len(rawL):
            if("" in rawL[i]):
                del rawL[i]
            else:
                i += 1

# Sets a day value based on the last day thats been read
# Could probaby redo this as setting a day variable is likely a bad fix to a bug.
        for i in range(0, len(rawL)):
            if("Monday" in rawL[i][0]):
                day = 0
            if("Tuesday" in rawL[i][0]):
                day = 1
            if("Wednesday" in rawL[i][0]):
                day = 2
            if("Thursday" in rawL[i][0]):
                day = 3
            if("Friday" in rawL[i][0]):
                day = 4
            if("Saturday" in rawL[i][0]):
                day = 5
            if("Sunday" in rawL[i][0]):
                day = 6

            # Multiple locations could be on one line so this splits that up
            if(len(rawL[i]) > 3):
                holder = split(rawL[i], 2)
                holder[0].insert(0, day)
                holder[1].insert(0, day)
                week.insert(i, holder[1])
                week.insert(i, holder[0])

            if(len(rawL[i]) == 2):
                rawL[i].insert(0, day)
                week.insert(i, rawL[i])

# Moves data from weeks to the specific day
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
