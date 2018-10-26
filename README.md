# Police-Speed-Camera-Location
Downloads and parses a web downlaod with the speed camera locations of Western Australia

To Run, "python3 Get_Locations.py"
Currently it can only runs on Sunday. Which isn't an issue for me as I use crontab to run it (Essentailly auto run for linux).
Uses these imports; datetime, re, glob, os, requests, dateutil.
Only Ran on Linux (Arch and Debian).
Must have pdftotext also.
