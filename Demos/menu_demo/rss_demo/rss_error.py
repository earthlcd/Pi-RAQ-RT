from pygame.locals import *
import pygame, Buttons
import os, sys
import xmltodict
import feedparser
import RPi.GPIO as GPIO

class rssError:
	def __init__(self):
		self.main()

	def display_init(self):
		self.path = os.path.dirname(os.path.abspath(__file__))
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		self.surface = pygame.display.set_mode(size, pygame.FULLSCREEN)
		self.surface_color = (0,0,0)
		self.surface.fill(self.surface_color)
		self.error_text = "ERROR: URL is not valid."
		self.font = self.path + "/saxmono.ttf"
		self.font_size = 50

	def printString(self,string, position, color, font, size):
		font = pygame.font.Font(font,size)
		fontObj = font.render(string, True, color)
		rectObj = fontObj.get_rect()

		if position[0] == 'C' or position[0] =='c':
			centerH = (pygame.display.Info().current_w /2) - (fontObj.get_width()/2)
			rectObj.topleft = (centerH, position[1])
		else:
			rectObj.topleft = position

		self.error_surface.blit(fontObj,rectObj)

	def error_surface_init(self):
		font = pygame.font.Font(self.font,self.font_size)
		self.error_w = font.size(self.error_text)[0] 
		self.error_h = font.size(self.error_text)[1] 
		self.error_x = (self.surface.get_width()/2 - self.error_w/2)-1
		self.error_y = (self.surface.get_height()/2 - self.error_h/2)-1

		self.error_surface = self.surface.subsurface(self.error_x,self.error_y,self.error_w,self.error_h)
		self.error_surface.fill(self.surface_color)

		color = (255,255,255)
		self.printString(self.error_text,(0,0),color,self.font,self.font_size)
		#PRINT ERROR


	def init_button(self):
		idle_color = (255,255,255)
		text_color = (0,0,0)

		self.button_w = 125
		self.button_h = 25
		self.start_x = (self.surface.get_width()/2 - self.button_w/2)-1
		self.start_y = 70 
				
		self.exit_button = Buttons.Button()
		self.exit_button_surface = self.surface.subsurface(self.start_x,self.start_y,self.button_w,self.button_h)
		self.exit_button_surface.fill(idle_color)

		#Parameters:					  surface,		 color,       x, y,		length, height, width, 		 text,	text_color
		self.exit_button.create_button(self.exit_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,False)

		pygame.display.update()

	def redraw_button(self,selected,last,active):
		fill_color = (255,255,255)
		idle_color = (255,255,255)
		text_color = (0,0,0)
		
		a_c1 = (200,200,200)
		a_c2 = (154,226,250)
		active_color = a_c2	
		
		if(active):
			if(selected != last):
				if(last == "NaN"):
					pass
				elif(last == "Exit"):
					self.exit_button_surface.fill(fill_color)
					self.exit_button.create_button(self.exit_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,not active)

				if(selected == "NaN"):
					pass
				elif(selected == "Exit"):
					self.exit_button_surface.fill(fill_color)
					self.exit_button.create_button(self.exit_button_surface,active_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,active)
			else:
				if(selected == "NaN"):
					pass
				elif(selected == "Exit"):
					self.exit_button_surface.fill(fill_color)
					self.exit_button.create_button(self.exit_button_surface,active_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,active)
		else:
			if(last == "NaN"):
				pass
			elif(last == "Exit"):
				self.exit_button_surface.fill(fill_color)
				self.exit_button.create_button(self.exit_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,not active)

		pygame.display.update()

	def main(self):
		lastButton = "NaN"
		currentButton = "NaN"
		self.display_init()
		self.error_surface_init()
		self.init_button()
		while(1):
			for event in pygame.event.get():
				if(event.type == pygame.MOUSEBUTTONDOWN):
					if(self.exit_button.pressed_subsurface(pygame.mouse.get_pos())):
						currentButton = "Exit"
						self.redraw_button(currentButton,lastButton,True)
						lastButton = currentButton
					else:
						currentButton = "NaN"
						self.redraw_button(currentButton,lastButton,True)
						lastButton = currentButton 
				elif(event.type == pygame.MOUSEBUTTONUP):
					if(self.exit_button.pressed_subsurface(pygame.mouse.get_pos())):
						currentButton = "Exit"
						self.redraw_button(currentButton,lastButton,False)
						if(currentButton == lastButton):
							return
						lastButton = currentButton
					else:
						currentButton = "NaN"
						self.redraw_button(currentButton,lastButton,False)
						lastButton = currentButton

if __name__ == '__main__':
	obj = rssError()