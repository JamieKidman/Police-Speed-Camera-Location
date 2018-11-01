# Police-Speed-Camera-Location
Downloads and parses a web downlaod with the speed camera locations of Western Australia

Get_Locations:
To Run, "python3 Get_Locations.py"
Will print error if the pdf hasn't been uploaded by the police yet for the week. It isn't an issue for me as I use crontab to run it on sunday (Essentailly auto run for linux).
Uses these imports; datetime, re, glob, os, requests, dateutil.
Only Ran on Linux (Arch and Debian).
Must have pdftotext also.

Send_Today_To:
Have to add your own gmail details as its described in the comment in the code. And add a target email in the send_to file.
