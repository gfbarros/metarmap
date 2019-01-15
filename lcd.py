import time
import serial
import urllib.request
import xml.etree.ElementTree as ET

# this assume a 4 line 20 character display

station = "KMSN"

#lcd = serial.Serial (
#	port =' /dev/ttyS0',
#        baudrate = 9600,
#        parity=serial.PARITY_NONE,
#        stopbits=serial.STOPBITS_ONE,
#        bytesize=serial.EIGHTBITS,
#        timeout=1
#)

#url = "https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&hoursBeforeNow=4&mostRecentForEachStation=constraint&stationString=" + station

url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=2&mostRecentForEachStation=true&stationString=" + station

#print(url)
content = urllib.request.urlopen(url).read()
#print(content)

root = ET.fromstring(content)

#print("01234567890123456789")
utctime = time.strftime("%a %d %b %H:%M UTC",time.gmtime())
print(utctime)

rawmetar = root[6][0][0].text
#print(rawmetar)

splitmetar = rawmetar.split()
print(splitmetar[0], splitmetar[1])
print(splitmetar[2], splitmetar[3])
print(splitmetar[4], splitmetar[5])
