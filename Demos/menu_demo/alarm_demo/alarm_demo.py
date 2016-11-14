

#
# The MIT License (MIT)
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
import netifaces
import pygame
from pygame.locals import *
from datetime import datetime
import signal
import urllib2
import json
import wget
#from pip._vendor.requests.packages.urllib3.exceptions import LocationParseError
import xmltodict

path = os.path.dirname(os.path.abspath(__file__))
font = path+'/saxmono.ttf'

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
zipCode = '92648'
location = 'Huntington Beach, CA'
weather ='weather' 
windstring = 'windstring'
temp_f = 75
windspeed = 10
winddirection = 'sse'
humidity = '20%'

def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse
    
    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))

def getZip():
	global screen
	global zipCode
	zip1 = int(zipCode[0])
	zip2 = int(zipCode[1])
	zip3 = int(zipCode[2])
	zip4 = int(zipCode[3])
	zip5 = int(zipCode[4])
	screen.fill((0,0,0))	
	bx = 245
	tx = 35
	print 'zipCode is ' + zipCode
	buttons = list()
	screen.blit(buttonP,(bx,0))
	screen.blit(buttonM,(bx,76))
	buttons.append(tx+bx)
	printString(zipCode[0] , (tx+bx,25),(210,150,20),font, 60)
	bx+=110
	screen.blit(buttonP,(bx,0))
	screen.blit(buttonM,(bx,76))
	buttons.append(tx+bx)
	printString(zipCode[1] , (tx+bx,25),(210,150,20),font, 60)	
	bx+=110
	screen.blit(buttonP,(bx,0))
	screen.blit(buttonM,(bx,76))
	buttons.append(tx+bx)
	printString(zipCode[2] , (tx+bx,25),(210,150,20),font, 60)
	bx+=110
	screen.blit(buttonP,(bx,0))
	screen.blit(buttonM,(bx,76))
	buttons.append(tx+bx)	
	printString(zipCode[3] , (tx+bx,25),(210,150,20),font, 60)	
	bx+=110
	screen.blit(buttonP,(bx,0))
	screen.blit(buttonM,(bx,76))
	buttons.append(tx+bx)	
	printString(zipCode[4] , (tx+bx,25),(210,150,20),font, 60)
	bx+=150
	screen.blit(buttonDone,(bx,25))
	print buttons
	while True:
		pygame.display.update()
		for event in pygame.event.get():
			print event.type, QUIT
			x,y = pygame.mouse.get_pos()
			if event.type == 5:
				print( x,y)
				if x > 245 and x < 245+100 and y > 0 and y < 28:
					if zip1 < 9:
						zip1+=1
						screen.fill((0,0,0), ( buttons[0],25, 50,50))
						printString(str(zip1) , (buttons[0],25),(210,150,20),font, 60)
						pygame.display.update()
				if x > 245 and x < 245+100 and y > 72 and y < 100:
					if zip1 > 0 :
						zip1-=1
						screen.fill((0,0,0), ( buttons[0],25, 50,50))
						printString(str(zip1) , (buttons[0],25),(210,150,20),font, 60)
						pygame.display.update()
#
				if x > 110+245 and x < 245+110+100 and y > 0 and y < 28:
					if zip2 < 9:
						zip2+=1
						screen.fill((0,0,0), ( buttons[1],25, 50,50))
						printString(str(zip2) , (buttons[1],25),(210,150,20),font, 60)
						pygame.display.update()
				if x > 110+245 and x < 245+110+100 and y > 72 and y < 100:
					if zip2 > 0 :
						zip2-=1
						screen.fill((0,0,0), ( buttons[1],25, 50,50))
						printString(str(zip2) , (buttons[1],25),(210,150,20),font, 60)
						pygame.display.update()
#
				if x > 220+245 and x < 245+220+100 and y > 0 and y < 28:
					if zip3 < 9:
						zip3+=1
						screen.fill((0,0,0), ( buttons[2],25, 50,50))
						printString(str(zip3) , (buttons[2],25),(210,150,20),font, 60)
						pygame.display.update()
				if x > 220+245 and x < 245+220+100 and y > 72 and y < 100:
					if zip3 > 0 :
						zip3-=1
						screen.fill((0,0,0), ( buttons[2],25, 50,50))
						printString(str(zip3) , (buttons[2],25),(210,150,20),font, 60)
						pygame.display.update()
#
				if x > 330+245 and x < 245+330+100 and y > 0 and y < 28:
					if zip4 < 9:
						zip4+=1
						screen.fill((0,0,0), ( buttons[3],25, 50,50))
						printString(str(zip4) , (buttons[3],25),(210,150,20),font, 60)
						pygame.display.update()
				if x > 330+245 and x < 245+330+100 and y > 72 and y < 100:
					if zip4 > 0 :
						zip4-=1
						screen.fill((0,0,0), ( buttons[3],25, 50,50))
						printString(str(zip4) , (buttons[3],25),(210,150,20),font, 60)
						pygame.display.update()
#
				if x > 440+245 and x < 245+440+100 and y > 0 and y < 28:
					if zip5 < 9:
						zip5+=1
						screen.fill((0,0,0), ( buttons[4],25, 50,50))
						printString(str(zip5) , (buttons[4],25),(210,150,20),font, 60)
						pygame.display.update()
				if x > 440+245 and x < 245+440+100 and y > 72 and y < 100:
					if zip5 > 0 :
						zip5-=1
						screen.fill((0,0,0), ( buttons[4],25, 50,50))
						printString(str(zip5) , (buttons[4],25),(210,150,20),font, 60)
						pygame.display.update()
#
				myZip = zip1*10000+zip2*1000+zip3*100+zip4*10+zip5
				print myZip
				if x > 835 and x < 935 and y > 25 and y < 75:
					return str(myZip)


def getWeather(zipCode):
	global location
	global weather 
	global windstring
	global temp_f
	global windspeed
	global winddirection
	global humidity
	url = 'http://api.wunderground.com/api/712ac117097870c0/geolookup/conditions/q/' + zipCode + '.json'
	print url
	try:
		f = urllib2.urlopen(url)
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

	locationSurfaceObj = smallFont.render(location, True, (255,255,255))
	locationRectobj = locationSurfaceObj.get_rect()
	locationRectobj.topleft = (600, 5)

	humiditySurfaceObj = smallFont.render('RH : ' + humidity, True, (255,255,255))
	humidityRectobj = humiditySurfaceObj.get_rect()
	humidityRectobj.topleft = (750, 20)
	
#	temp_f = 75
	tempSurfaceObj = tempFont.render(str(temp_f) + 'F', True, (0,0,255))
	tempRectobj = tempSurfaceObj.get_rect()
	tempRectobj.topleft = (600, 15)
	
	weatherSurfaceObj = smallFont.render('Sky : ' + weather, True, (255,255,255))
	weatherRectobj = weatherSurfaceObj.get_rect()
	weatherRectobj.topleft = (600, 50)

	windSurfaceObj = smallFont.render('Wind : ' + windstring , True, (255,255,255))
	windRectobj = windSurfaceObj.get_rect()
	windRectobj.topleft = (600, 65)

	#wind2SurfaceObj = smallFont.render( 'Speed : ' + str(windspeed) + 'MPH Direction : ' + winddirection, True, (200,150,200))
	#wind2Rectobj = wind2SurfaceObj.get_rect()
	#wind2Rectobj.topleft = (600, 80)


	screen.blit(tempSurfaceObj, tempRectobj)	 
	screen.blit(humiditySurfaceObj, humidityRectobj)	
	screen.blit(weatherSurfaceObj, weatherRectobj)
	screen.blit(windSurfaceObj, windRectobj)
	#screen.blit(wind2SurfaceObj, wind2Rectobj)	
	screen.blit(locationSurfaceObj, locationRectobj)		

#	printString('test print1',(10,0),(255,255,255),'Roboto-Light.ttf',20)	
#	printString('test print2',(10,20),(255,255,255),'Roboto-Black.ttf',20)	
#	printString('test print3',(10,40),(255,255,255),'Roboto-Regular.ttf',20)	
	if eth0ip != None:
		printString('eth0 IP Address ' + eth0ip ,(10,85),(155,155,155),path+'/Roboto-Light.ttf',12)
	if wlan0ip != None:	
		printString('wlan0 IP Address ' + wlan0ip ,(200,85),(15,255,15),path+'/Roboto-Light.ttf',12)		
	printString('EarthLCD Internal DEMO Version DO NOT DISTRIBUTE',(600,80),(0,255,0),path+'/Roboto-Black.ttf',14)

if __name__ == '__main__':
	#signal.signal(signal.SIGINT, signal_handler)
	x=674
	dir = 1
	#os.environ['SDL_VIDEODRIVER'] = 'fbcon'
	#os.environ["SDL_FBDEV"] = "/dev/fb0"
	#os.environ["SDL_MOUSEDEV"] = "/dev/input/event2"
	#os.environ["SDL_MOUSEDRV"] = "TSLIB"	
	print pygame.get_sdl_version()
	pygame.display.init()
	fpsClock= pygame.time.Clock()
	pygame.font.init()
	pygame.mouse.set_visible(True)
	pygame.event.set_grab(True) 
	# Get size of screen and create main rendering surface.
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

	TimeFont = pygame.font.Font(path+'/whitrabt.ttf', 80)
	tempFont = pygame.font.Font(path+'/Roboto-Black.ttf', 35)	
	smallFont = pygame.font.Font(path+'/Roboto-Light.ttf', 14)
	bgImage = pygame.image.load(path+"/bg.png")		
	logo = pygame.image.load(path+"/earthLCD.png")	
	settings = pygame.image.load(path+"/Setting48.png")	
	buttonP	= pygame.image.load(path+"/button+.png")	
	buttonM	= pygame.image.load(path+"/button-.png")	
	buttonDone	= pygame.image.load(path+"/buttonDone.png")	
	#getWeather()

	#printWeather()

#	file = urllib2.urlopen('http://feeds.foxnews.com/foxnews/latest?format=xml')
#	data = file.read()
#	file.close()

#	data = xmltodict.parse(data)
#	feed = data['rss']['channel']['title']
#	item1 =  data['rss']['channel']['item'][0]['title']

#	feed = 'EarthLCD '
#	item1 = ' Pi-Raq'
	eth0ip = None
	wlan0ip = None

	zipCode = '92648'
	temp_f = getWeather(zipCode)
	while True:
		# Process any events (only mouse events for now).
		for event in pygame.event.get():
			print event.type, QUIT
			print pygame.mouse.get_pos()
			x,y = pygame.mouse.get_pos()
			if event.type == 5:
				print( x,y)
				if x > 0 and x < 48 and y > 0 and y < 48:
					zipCode = getZip()
					temp_f = getWeather(zipCode)	
			if event.type == 2:
				break
				# pygame.quit()
				# sys.exit()
		screen.fill((0,0,0))		
		fill_gradient(screen,  (100, 100, 100), (0, 0,0))
#		screen.blit(bgImage,(0,0))
		#tempSurfaceObj = tempFont.render(str(temp_f), False, (200,150,200))
		#tempRectobj = tempSurfaceObj.get_rect()
		#tempRectobj.topleft = (800, 10)
		#screen.blit(tempSurfaceObj, tempRectobj)	

#		screen.blit(logo,(x,5))
		screen.blit(settings,(0,0))

#		printString(feed + ' ' + item1, (x,75), (0,255,0),'Roboto-Black.ttf',20)	
		CurrentTime = datetime.now().strftime('%l:%M:%S')
		CurrentDate = datetime.now().strftime('%A %B %d %Y Day %j')

		#msgSurfaceObj = TimeFont.render(CurrentTime, True, (32,150,200))
		#msgRectobj = msgSurfaceObj.get_rect()
		#msgRectobj.topleft = (200, 10)
		o = 2
#		printString(CurrentTime , (200-o,5),(250,250,250),'saxmono.ttf', 80)
#		printString(CurrentTime , (200,5-o),(250,250,250),'saxmono.ttf', 80)
		printString(CurrentTime , (200+o,5),(200,200,200),font, 80)
		printString(CurrentTime , (200,5+o),(200,200,200),font, 80)

		printString(CurrentTime , (200,5),(0,0,255),font, 80)

		printString(CurrentDate , (260,75),(200,150,21),font, 14)

		updateWeather = CurrentTime[-5:]
		if updateWeather == '00:00' or updateWeather == '15:00' or updateWeather == '30:00' or updateWeather == '45:00':
			getWeather(zipCode)
			print 'weather updated'
		printWeather()

		iconImage = pygame.image.load(path+"/icon.gif").convert_alpha()
		screen.blit(iconImage,(950,0))
		#oneImage = pygame.image.load("images/5.png").convert_alpha()
		#screen.blit(oneImage,(200,0))				
		#screen.blit(msgSurfaceObj, msgRectobj)	
		#time.sleep(1.0)
		if dir ==1:
			x -=1
			if x ==0:
				dir =0
		if dir ==0:
			x+=1
			if x==674:
				dir =1
		pygame.display.update()
		try:
			eth0ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
		except Exception, e:
			eth0ip = None
		try:
			wlan0ip = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
		except Exception, e:
			wlan0ip = None
		time.sleep(.5)
		fpsClock.tick(30)
