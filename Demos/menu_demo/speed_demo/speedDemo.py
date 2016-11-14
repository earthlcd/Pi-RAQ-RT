import os, sys
import pygame
import RPi.GPIO as GPIO	# handles interfacing with RPi pins
from pygame.locals import *

class speedDemo:
	def __init__(self):
		self.main()

	def init_display(self):
		self.path = os.path.dirname(os.path.abspath(__file__))

		image = pygame.image.load(self.path + "/images/logo000.bmp")
		os.putenv('SDL_VIDEODRIVER', 'fbcon')
		os.putenv('SDL_FBDEV'      , '/dev/fb0')
		pygame.display.init()
		pygame.font.init()
		pygame.mouse.set_visible(False)
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

		GPIO.setwarnings(False)		# disable warnings
		GPIO.setmode(GPIO.BCM)		# refer to pins by Broadcom SOC channel	
		Center = 23					# GPIO pins
		GPIO.setup(Center, 		GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# Center Button

	def main(self):
		self.init_display()

		dir = 1
		image_start = 0
		while True:
			for event in pygame.event.get():
				if((event.type == KEYDOWN and event.key == K_RETURN) or event.type == pygame.MOUSEBUTTONUP):
					return

			if(image_start % 200 == 0):	
				image_num = (5*abs(image_start/200))
				if(image_num >= 100):
					image = pygame.image.load(self.path + "/images/logo" + str(image_num) + ".bmp")
				elif(image_num < 100 and image_num >= 10):
					image = pygame.image.load(self.path + "/images/logo0" + str(image_num) + ".bmp")
				elif(image_num < 10):
					image = pygame.image.load(self.path + "/images/logo00" + str(image_num) + ".bmp")
				self.screen.blit(pygame.transform.flip(image,False,True),(0,0))

			if dir ==1:
				image_start += 1
				if image_start == 5000:
					dir =0
			if dir ==0:
				image_start -= 1
				if image_start == -199:
					dir =1

			pygame.display.update()

if __name__ == "__main__":
	obj = speedDemo()
