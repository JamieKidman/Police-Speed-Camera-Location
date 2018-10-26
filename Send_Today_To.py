import base64
import datetime
import os
import smtplib
from datetime import date
from dateutil.relativedelta import relativedelta, MO


def emailD():
    today = date.today()
    last_Monday = today + relativedelta(weekday=MO(-1))
    monday = last_Monday.strftime("%d%m20%y")
    today = today.strftime("%d/%m/%y")

    body = "Subject:" + datetime.date.today().strftime("%A") + " - " + today + "\n"

    inputFile = ".//Parsed/" + monday + "/" + datetime.date.today().strftime("%A")
    if os.path.isfile(inputFile):
        f = open(inputFile, "r")
        body += f.read()
        # body += "\nTo Stop these emails Link to a google form"
        print(body)

# email address in plaintext, password in base64 (Just because I didnt like the idea of storing a password in human readable form, still not good)
    gmail_user = ""
    b = b''
    gmail_password = base64.b64decode(b).decode('utf-8')
    sent_from = gmail_user

    inputFile = "./send_to"
    if os.path.isfile(inputFile):
        f = open(inputFile, "r")
        to = f.readlines()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, body)
        server.close()

        print("Email sent!")
    except:
        print("Something went wrong...")


emailD()
