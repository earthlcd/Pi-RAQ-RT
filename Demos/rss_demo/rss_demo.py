from pygame.locals import *
import pygame, Buttons, keyboard, rss_error
import os, sys
import xmltodict
import feedparser
import RPi.GPIO as GPIO

class rssDemo:
	def __init__(self):
		self.main()

	def display_init(self):
		pygame.display.init()
		os.putenv('SDL_VIDEODRIVER', 'fbcon')
		os.putenv('SDL_FBDEV'      , '/dev/fb0')
		pygame.font.init()
		pygame.mouse.set_visible(True)
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		self.surface = pygame.display.set_mode(size, pygame.FULLSCREEN)
		self.surface_color = (0,0,0)
		self.surface.fill(self.surface_color)
		self.rss_default_url = "www.reddit.com/r/news/.rss"
		self.rss_font = "saxmono.ttf"
		self.rss_font_size = 50
		self.rss_surface_color = (0,0,0)

	def rss_printString(self,string, position, color, font, size):
		font = pygame.font.Font(font,size)
		fontObj = font.render(string, True, color)
		rectObj = fontObj.get_rect()

		if position[0] == 'C' or position[0] =='c':
			centerH = (pygame.display.Info().current_w /2) - (fontObj.get_width()/2)
			rectObj.topleft = (centerH, position[1])
		else:
			rectObj.topleft = position

		self.rss_surface.blit(fontObj,rectObj)
		

	def rss_init(self,rssurl):
		if(rssurl.startswith("http://") and not rssurl.startswith("http://www.")):
			rssurl = "http://www." + rssurl[len("http://"):len(rssurl)]
		elif(rssurl.startswith("www.")):
			rssurl = "http://" + rssurl
		elif(not rssurl.startswith("http://www.")):
			rssurl = "http://www." + rssurl

		self.parser = feedparser.parse(rssurl)
		if('title' in self.parser.feed):
			self.feedstories = 5 if len(self.parser.entries) > 5 else len(self.parser.entries)
			self.scroll = True
			rss_list_w = []
			rss_list_h = []
			for i in range(0,self.feedstories):
				font = pygame.font.Font(self.rss_font,self.rss_font_size)
				rss_list_w.append(font.size(self.parser.entries[i]['title'])[0])
				rss_list_h.append(font.size(self.parser.entries[i]['title'])[1])

			self.rss_max = max(rss_list_w)
			self.rss_max_height = max(rss_list_h)
		else:
			error = rss_error.rssError()
			self.scroll = False
			self.surface.fill(self.surface_color)
			self.rss_init(self.rss_default_url)	
			# self.control_buttons_init()
			# self.display_control_buttons_init()
		
		#RSS Feed screen 
		self.rss_x = 0
		self.rss_y = (self.surface.get_height()/2)-(self.rss_max_height/2)
		self.rss_w = self.surface.get_width()
		self.rss_h = self.rss_max_height

		self.rss_surface = self.surface.subsurface(self.rss_x,self.rss_y,self.rss_w,self.rss_h)
		self.rss_surface.fill(self.rss_surface_color)
		self.rss_color = (255,255,255)

	def rss_scroll(self,x,entry):
		self.rss_surface.fill(self.rss_surface_color)
		self.rss_printString(self.parser.entries[entry]['title'],(x, 0),self.rss_color,self.rss_font,self.rss_font_size)

	def exit(self):
		pygame.display.quit()
		os._exit(1)

	def button_cmd(self,cmd):
		if(cmd == "Exit"):
			self.exit()	
		elif(cmd == "Change URL"):
			url = self.keyboard_url()
			self.surface.fill(self.surface_color)
			if(url != "#EXIT"):
				self.rss_init(url)
			else:
				self.rss_init(self.rss_default_url)	
			# self.control_buttons_init()
			# self.display_control_buttons_init()

	def display_control_buttons_init(self,dim):
		# Control button config "CHANGE URL/EXIT"

		#Centered 
		self.offset_width = 10
		self.button_w = 150
		self.button_h = 25
		self.start_x = (self.surface.get_width() / 2) - (self.offset_width/2) - self.button_w - 1
		self.start_y = 74


		#Custom, not centered
		# self.start_x = 345
		# self.start_y = 70 
		# self.button_w = 125
		# self.button_h = 25
		# self.offset_width = 5 

		self.keyboard_button = Buttons.Button()
		self.exit_button = Buttons.Button()

		self.keyboard_button_surface = self.surface.subsurface(self.start_x,self.start_y,self.button_w,self.button_h)
		self.exit_button_surface = self.surface.subsurface(self.start_x+self.button_w+self.offset_width,self.start_y,self.button_w,self.button_h)

		background_color = (dim,dim,dim)
		self.keyboard_button_surface.fill(background_color)
		self.exit_button_surface.fill(background_color)

		idle_color = (dim,dim,dim)
		text_color = (0,0,0)

		#Parameters:					  surface,		 color,       x, y,		length, height, width, 		 text,	text_color
		self.keyboard_button.create_button(self.keyboard_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Change URL",text_color,False)
		self.exit_button.create_button(self.exit_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,False)

		if dim == 0:
			self.keyboard_button_surface.fill(background_color)
			self.exit_button_surface.fill(background_color)

		pygame.display.update()

	def display_control_redraw(self,selected,last,active):
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
				elif(last == "Change URL"):
					self.keyboard_button_surface.fill(fill_color)
					self.keyboard_button.create_button(self.keyboard_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Change URL",text_color,not active)
				elif(last == "Exit"):
					self.exit_button_surface.fill(fill_color)
					self.exit_button.create_button(self.exit_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,not active)

				if(selected == "NaN"):
					pass
				elif(selected == "Change URL"):
					self.keyboard_button_surface.fill(fill_color)
					self.keyboard_button.create_button(self.keyboard_button_surface,active_color,0,0,self.button_w,self.button_h,0,"Change URL",text_color,active)
				elif(selected == "Exit"):
					self.exit_button_surface.fill(fill_color)
					self.exit_button.create_button(self.exit_button_surface,active_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,active)
			else:
				if(selected == "NaN"):
					pass
				elif(selected == "Change URL"):
					self.keyboard_button_surface.fill(fill_color)
					self.keyboard_button.create_button(self.keyboard_button_surface,active_color,0,0,self.button_w,self.button_h,0,"Change URL",text_color,active)
				elif(selected == "Exit"):
					self.exit_button_surface.fill(fill_color)
					self.exit_button.create_button(self.exit_button_surface,active_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,active)
		else:
			if(last == "NaN"):
				pass
			elif(last == "Change URL"):
				self.keyboard_button_surface.fill(fill_color)
				self.keyboard_button.create_button(self.keyboard_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Change URL",text_color,not active)
			elif(last == "Exit"):
				self.exit_button_surface.fill(fill_color)
				self.exit_button.create_button(self.exit_button_surface,idle_color,0,0,self.button_w,self.button_h,0,"Exit",text_color,not active)

		pygame.display.update()		

	def keyboard_url(self):
		entry = keyboard.Keyboard()
		url = entry.get_url()
		return url	

	def main(self):
		lastButton = "NaN"
		currentButton = "NaN"
		self.display_init()
		self.rss_init(self.rss_default_url)
		
		dim = 0
		button_control = 0
		scroll_increase = 0

		dir = 0
		if dir == 0:
			input_x = self.rss_w
		else:
			input_x = -self.rss_max

		entry = 0
		while(1):
			for event in pygame.event.get():
				if(event.type == pygame.MOUSEBUTTONDOWN):
					if(button_control == 1 and dim == 250):
						if(self.keyboard_button.pressed_subsurface(pygame.mouse.get_pos())):
							currentButton = "Change URL"
							self.display_control_redraw(currentButton,lastButton,True)
							lastButton = currentButton
						elif(self.exit_button.pressed_subsurface(pygame.mouse.get_pos())):
							currentButton = "Exit"
							self.display_control_redraw(currentButton,lastButton,True)
							lastButton = currentButton
						else:
							currentButton = "NaN"
							self.display_control_redraw(currentButton,lastButton,True)
							lastButton = currentButton 
				elif(event.type == pygame.MOUSEBUTTONUP):
					if(button_control == 1 and dim == 250):	
						if(self.keyboard_button.pressed_subsurface(pygame.mouse.get_pos())):
							currentButton = "Change URL"
							self.display_control_redraw(currentButton,lastButton,False)
							if(currentButton == lastButton):
								self.button_cmd(currentButton)		
							lastButton = currentButton
						elif(self.exit_button.pressed_subsurface(pygame.mouse.get_pos())):
							currentButton = "Exit"
							self.display_control_redraw(currentButton,lastButton,False)
							if(currentButton == lastButton):
								self.button_cmd(currentButton)	
							lastButton = currentButton
						else:
							currentButton = "NaN"
							self.display_control_redraw(currentButton,lastButton,False)
							lastButton = currentButton
					if(button_control == 0 and dim == 0):
						button_control = 1
					elif(button_control == 1 and dim == 250):
						button_control = 0

			if(button_control == 1 and (dim >= 0 and dim < 250)):
				scroll_increase = 1
				dim += 5
				self.display_control_buttons_init(dim)
			elif(button_control == 0 and (dim <= 250 and dim > 0)):
				scroll_increase = 1
				dim -= 5
				self.display_control_buttons_init(dim)
				

			if(self.scroll == True):
				self.rss_scroll(input_x,entry)

				pygame.display.update()	

			if dir == 0:
				if(scroll_increase == 1):
					input_x -= 3
					scroll_increase = 0
				else:
					input_x -=1

				if input_x <= -self.rss_max:
					entry += 1
					if entry == self.feedstories:
						entry = 0
					input_x = self.rss_w
			elif dir == 1:		
				if(scroll_increase == 1):
					input_x += 3
					scroll_increase = 0
				else:
					input_x +=1
					
				if input_x >= self.rss_w + self.rss_max:
					entry += 1
					if entry == self.feedstories:
						entry = 0
					input_x = -self.rss_max

if __name__ == '__main__':
	obj = rssDemo()