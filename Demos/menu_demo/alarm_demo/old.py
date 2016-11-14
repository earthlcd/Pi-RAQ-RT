

#
# The MIT License (MIT)
#
# Copyright (c) 2014 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os, sys
import time

import pygame
from pygame.locals import *
from datetime import datetime
import signal
import urllib2
import json
import wget
#from pip._vendor.requests.packages.urllib3.exceptions import LocationParseError
import xmltodict


def signal_handler(signal, frame):
	print('\nBYE\n')
	pygame.quit()
	sys.exit(0)
	

MAIN_BG        = (  0,   0,   0) # Black
INPUT_BG       = ( 60, 255, 255) # Cyan-ish
INPUT_FG       = (  0,   0,   0) # Black
CANCEL_BG      = (128,  45,  45) # Dark red
ACCEPT_BG      = ( 45, 128,  45) # Dark green
BUTTON_BG      = ( 60,  60,  60) # Dark gray
BUTTON_FG      = (255, 255, 255) # White
BUTTON_BORDER  = (200, 200, 200) # White/light gray
INSTANT_LINE   = (  0, 255, 128) # Bright yellow green.

location = 'Huntington Beach, CA'
weather ='weather' 
windstring = 'windstring'
temp_f = 75
windspeed = 10
winddirection = 'sse'
humidity = '20%'
def getWeather():
	global location
	global weather 
	global windstring
	global temp_f
	global windspeed
	global winddirection
	global humidity
	try:
		f = urllib2.urlopen('http://api.wunderground.com/api/090b974d8bb3704c/geolookup/conditions/q/CA/Huntington_Beach.json')
		json_string = f.read()
		parsed_json = json.loads(json_string)
		print json_string
		location = parsed_json['location']['city']
		temp_f = parsed_json['current_observation']['temp_f']
		weather = parsed_json['current_observation']['weather']
		windstring = parsed_json['current_observation']['wind_string']		
		windspeed = parsed_json['current_observation']['wind_mph']	
		winddirection = parsed_json['current_observation']['wind_dir']
		humidity = parsed_json['current_observation']['relative_humidity']					
		icon = parsed_json['current_observation']['icon_url']
		iconfile = urllib2.urlopen(icon)
		output = open('icon.gif','wb')
		output.write(iconfile.read())
		output.close()
		#icon_filename = wget.download(icon)
		#print icon_filename
		print "Current temperature in %s is: %s %s %s" % (location, temp_f, weather,windstring)
		f.close()	
		return temp_f
	except:
		print "no network"

def printString(string, position, color, font, size):
	psFont = pygame.font.Font(font, size)	
	psSurfaceObj = psFont.render(string, True, color)
	psRectobj = psSurfaceObj.get_rect()
	if position[0] == 'C' or position[0] =='c':
		centerH = (pygame.display.Info().current_w /2) - (psSurfaceObj.get_width()/2)
		psRectobj.topleft = (centerH, position[1])
	else:
		psRectobj.topleft = position
	screen.blit(psSurfaceObj, psRectobj)
			
def printWeather():
	global weather
	global location 
	global windstring
	global temp_f
	global windspeed
	global winddirection
	global humidity
	locationSurfaceObj = smallFont.render(location, True, (200,150,200))
	locationRectobj = locationSurfaceObj.get_rect()
	locationRectobj.topleft = (700, 5)

	humiditySurfaceObj = smallFont.render('RH : ' + humidity, True, (200,150,200))
	humidityRectobj = humiditySurfaceObj.get_rect()
	humidityRectobj.topleft = (850, 20)
	
	tempSurfaceObj = tempFont.render(str(temp_f) + 'F', True, (0,0,255))
	tempRectobj = tempSurfaceObj.get_rect()
	tempRectobj.topleft = (700, 15)
	
	weatherSurfaceObj = smallFont.render('Sky : ' + weather, True, (200,150,200))
	weatherRectobj = weatherSurfaceObj.get_rect()
	weatherRectobj.topleft = (700, 50)

	windSurfaceObj = smallFont.render('Wind : ' + windstring , True, (200,150,200))
	windRectobj = windSurfaceObj.get_rect()
	windRectobj.topleft = (700, 65)

	#wind2SurfaceObj = smallFont.render( 'Speed : ' + str(windspeed) + 'MPH Direction : ' + winddirection, True, (200,150,200))
	#wind2Rectobj = wind2SurfaceObj.get_rect()
	#wind2Rectobj.topleft = (700, 80)


	screen.blit(tempSurfaceObj, tempRectobj)	 
	screen.blit(humiditySurfaceObj, humidityRectobj)	
	screen.blit(weatherSurfaceObj, weatherRectobj)
	screen.blit(windSurfaceObj, windRectobj)
	#screen.blit(wind2SurfaceObj, wind2Rectobj)	
	screen.blit(locationSurfaceObj, locationRectobj)		
	printString('test print',(10,0),(255,255,255),'Roboto-Light.ttf',20)	
	printString('test print2',(10,20),(255,255,255),'Roboto-Black.ttf',20)	
	printString('test print3',(10,40),(255,255,255),'Roboto-Regular.ttf',20)	
	printString('test print4',(10,60),(255,255,255),'Roboto-Thin.ttf',20)
		
if __name__ == '__main__':
	#signal.signal(signal.SIGINT, signal_handler)
	x=674
	dir = 1
	os.putenv('SDL_VIDEODRIVER', 'fbcon')
	os.putenv('SDL_FBDEV'      , '/dev/fb0')
	pygame.display.init()
	fpsClock= pygame.time.Clock()
	pygame.font.init()
	pygame.mouse.set_visible(False)
	# Get size of screen and create main rendering surface.
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

	TimeFont = pygame.font.Font('whitrabt.ttf', 80)
	tempFont = pygame.font.Font('Zebulon.otf', 35)	
	smallFont = pygame.font.Font('Zebulon.otf', 10)
	bgImage = pygame.image.load("bg.png")		
	logo = pygame.image.load("earthLCD.png")	
	#getWeather()

	#printWeather()

	'''
	file = urllib2.urlopen('http://feeds.foxnews.com/foxnews/latest?format=xml')
	data = file.read()
	file.close()

	data = xmltodict.parse(data)
	feed = data['rss']['channel']['title']
	item1 =  data['rss']['channel']['item'][0]['title']
	'''
	feed = 'EarthLCD '
	item1 = ' Pi-Raq'
	#temp_f = getWeather()
	while True:
		# Process any events (only mouse events for now).
		for event in pygame.event.get():
			print event.type, QUIT
			if event.type == 2:
				pygame.quit()
				sys.exit()
		#screen.fill((240,240,240))		
		screen.blit(bgImage,(0,0))
#		tempSurfaceObj = tempFont.render(str(temp_f), False, (200,150,200))
#		tempRectobj = tempSurfaceObj.get_rect()
#		tempRectobj.topleft = (800, 10)
#		screen.blit(tempSurfaceObj, tempRectobj)	
		screen.blit(logo,(x,5))
		#printString(feed + ' ' + item1, (x,0), (0,255,0),'Roboto-Black.ttf',80)	
		'''	
		CurrentTime = datetime.now().strftime('%l:%M:%S')
		CurrentDate = datetime.now().strftime('%A %B %d %Y Day %j')

#		msgSurfaceObj = TimeFont.render(CurrentTime, True, (32,150,200))
#		msgRectobj = msgSurfaceObj.get_rect()
#		msgRectobj.topleft = (300, 10)
		printString(CurrentTime , (300,10),(21,150,200),'whitrabt.ttf', 80)
		updateWeather = CurrentTime[-5:]
		if updateWeather == '00:00' or updateWeather == '15:00' or updateWeather == '30:00' or updateWeather == '45:00':
			getWeather()
			print 'weather updated'
		printWeather()
#		iconImage = pygame.image.load("icon.gif").convert_alpha()
#		screen.blit(iconImage,(950,0))
		#oneImage = pygame.image.load("images/5.png").convert_alpha()
		#screen.blit(oneImage,(200,0))				
		#screen.blit(msgSurfaceObj, msgRectobj)	
		#time.sleep(1.0)
		'''
		if dir ==1:
			x -=1
			if x ==0:
				dir =0
		if dir ==0:
			x+=1
			if x==674:
				dir =1
		pygame.display.update()
		#fpsClock.tick(120)
