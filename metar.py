import urllib.request
import xml.etree.ElementTree as ET
import time
import board
import neopixel
import sys
import os

# LED strip configuration:
pixel_pin = board.D18
num_pixels = 71
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=True, pixel_order=ORDER)

with open("airports") as f:
    airports = f.readlines()
airports = [x.strip() for x in airports]
#print airports 

mydict = {
	"":""
}

url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=1.5&mostRecentForEachStation=true&stationString="
for airportcode in airports:
	if airportcode == "NULL":
		continue
#	print(airportcode)
	url = url + airportcode + ","

print(url)
content = urllib.request.urlopen(url).read()
#print(content)

root = ET.fromstring(content)

for metar in root.iter('METAR'):
	if airportcode == "NULL":
		continue
	if metar.find('flight_category') is None:
		print("Skipping")
		continue
	stationId = metar.find('station_id').text
	flightCategory = metar.find('flight_category').text
#	print(stationId, " ", flightCategory)
	if stationId in mydict:
		print("duplicate, only save first metar")
	else:
		mydict[stationId] = flightCategory
	
#print(mydict)

i = 0
for airportcode in airports:
	if airportcode == "NULL":
		i = i+1
		continue
	flightCategory = mydict.get(airportcode,"No")
#	print(airportcode, " ", flightCateory)
	if  flightCategory != "No":
		if flightCategory == "VFR":
#			print("VFR")
			pixels[i] = (0,255,0)
		elif flightCategory == "MVFR":
#			print("MVFR")
			pixels[i] = (0,0,255)
		elif flightCategory == "IFR":
#			print("IFR")
			pixels[i] = (255,0,0)
		elif flightCategory == "LIFR":
#			print("LIFR")
			pixels[i] = (255,0,125)
	else:
		pixels[i] = (0,0,0)
		print(airportcode, " N/A")
	print("Setting light ", str(i) , " for " , airportcode , " " , flightCategory)
#	pixels.show()
	i = i+1
print("fin")
