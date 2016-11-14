from pygame.locals import *
import pygame, Buttons
import os, sys
import xmltodict
import feedparser
import RPi.GPIO as GPIO

class Keyboard:
	def __init__(self):
		self.main()

	def display_init(self):
		self.path = os.path.dirname(os.path.abspath(__file__))
		# Don't REINIT for Demo
		# pygame.display.init()
		# os.putenv('SDL_VIDEODRIVER', 'fbcon')
		# os.putenv('SDL_FBDEV'      , '/dev/fb0')
		# pygame.font.init()
		# pygame.mouse.set_visible(True)
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		self.surface = pygame.display.set_mode(size, pygame.FULLSCREEN)
		self.surface.fill((255,255,255))

		# Keyboard Centered, parameters
		self.board_button_w = 30
		self.board_button_h = 15
		self.board_offset_w = 7
		self.board_offset_h = 1
		self.board_x = (self.surface.get_width()/2)-((((self.board_button_w+self.board_offset_w)*14)+(2*self.board_button_w))/2)-1
		self.board_y = 20

		# 1024 x 10 pixels at the top will be the form entry screen 
		self.text_surface = self.surface.subsurface(self.board_x,0,(((self.board_button_w+self.board_offset_w)*14)+(2*self.board_button_w)),19)
		self.case = "lower"
		self.text_field = "URL: "
		self.shift_on = False

	def get_url(self):
		return self.text_field[len("URL: "):len(self.text_field)]

	def entry_display(self,string):
		self.text_surface.fill((255,255,255))
		message_color = (0,0,0)
		font = pygame.font.Font(self.path +"/WasterMaster10.ttf",20)
		fontObj = font.render(string, True, message_color)
		rectObj = fontObj.get_rect()
		position = (0,0)
		if position[0] == 'C' or position[0] =='c':
			centerH = (pygame.display.Info().current_w /2) - (fontObj.get_width()/2)
			rectObj.topleft = (centerH, position[1])
		else:
			rectObj.topleft = position

		self.text_surface.blit(fontObj,rectObj)
		pygame.display.update()

	def keyboard_button_init(self,lower):
		self.keyboard_button_text_lower_row1 = ["`","1","2","3","4","5","6","7","8","9","0","-","="]
		self.keyboard_button_text_lower_row2 = ["q","w","e","r","t","y","u","i","o","p","{","}"]
		self.keyboard_button_text_lower_row3 = ["a","s","d","f","g","h","j","k","l",":","\'"]
		self.keyboard_button_text_lower_row4 = ["z","x","c","v","b","n","m",",",".","/"]

		self.keyboard_button_text_upper1 = ["~","!","@","#","$","%","^","&","*","(",")","-","+"]
		self.keyboard_button_text_upper2 = ["Q","W","E","R","T","Y","U","I","O","P","{","}"]
		self.keyboard_button_text_upper3 = ["A","S","D","F","G","H","J","K","L",":","\""]
		self.keyboard_button_text_upper4 = ["Z","X","C","V","B","N","M","<",">","?"]

		self.screens = []
		self.buttons = []

		self.esc_button = Buttons.Button()
		self.tab_button = Buttons.Button()
		self.left_shift_button = Buttons.Button()
		self.right_shift_button = Buttons.Button()
		self.fwd_slash_button = Buttons.Button()
		self.caps_button = Buttons.Button()
		self.enter_button = Buttons.Button()
		self.space_button = Buttons.Button()
		self.bckspce_button = Buttons.Button()
		self.clear_button = Buttons.Button()
		self.space_button = Buttons.Button()
		self.com_button = Buttons.Button()
		self.exit_button = Buttons.Button()

		# Custom
		# self.board_button_w = 35
		# self.board_button_h = 14
		# self.board_offset_w = 6
		# self.board_offset_h = 1
		# self.board_x = 200
		# self.board_y = 25

		start_x = self.board_x
		start_y = self.board_y
		width = self.board_button_w
		height = self.board_button_h
		offset_space = self.board_offset_w
		offset_height = self.board_offset_h
		

		self.total_l = len(self.keyboard_button_text_lower_row1) + len(self.keyboard_button_text_lower_row2) + len(self.keyboard_button_text_lower_row3) + len(self.keyboard_button_text_lower_row4)

		self.esc_surface = self.surface.subsurface(start_x,start_y,width,height)
		self.bckspce_surface = self.surface.subsurface(start_x+((len(self.keyboard_button_text_lower_row1)+1)*(offset_space+width)),start_y,width*2,height)

		self.tab_surface = self.surface.subsurface(start_x,start_y+(1*(height+offset_height)), width+offset_space, height)
		self.fwd_surface = self.surface.subsurface(start_x+(width+offset_space+offset_space)+((len(self.keyboard_button_text_lower_row2))*(offset_space+width)),start_y+(height+offset_height), (width*3), height)

		self.caps_surface = self.surface.subsurface(start_x,start_y+(2*(height+offset_height)), (width*2)+offset_space, height)
		self.enter_surface = self.surface.subsurface(start_x+((width*2)+offset_space+offset_space)+((len(self.keyboard_button_text_lower_row3))*(offset_space+width)),start_y+(2*(height+offset_height)), (width*3)+offset_space, height)

		self.lshift_surface = self.surface.subsurface(start_x,start_y+(3*(height+offset_height)), (width*3)+offset_space, height)
		self.rshift_surface = self.surface.subsurface(start_x+((width*3)+offset_space+offset_space)+((len(self.keyboard_button_text_lower_row4))*(offset_space+width)),start_y+(3*(height+offset_height)), (3*width)+(2*offset_space), height)

		self.clear_surface = self.surface.subsurface(start_x, start_y+(4*(height+offset_height)), (width*3)+offset_space, height)
		self.space_surface = self.surface.subsurface(start_x + ((width*3)+offset_space+offset_space), start_y+(4*(height+offset_height)), (width*10)+(offset_space*9), height)
		self.com_surface = self.surface.subsurface(start_x + ((width*10)+(offset_space*9)+offset_space+(width*3)+offset_space+offset_space), start_y+(4*(height+offset_height)), width+offset_space, height)	
		self.exit_surface = self.surface.subsurface(start_x + ((width*10)+(offset_space*9)+offset_space+(width*3)+offset_space+offset_space+width+offset_space+offset_space), start_y+(4*(height+offset_height)), (2*width), height)			

		x = 0
		i = 0
		r = 1
		if(lower):
			while(x < self.total_l):
				if r == 1:
					self.screens.append(self.surface.subsurface(start_x+((i+1)*(offset_space+width)),start_y,width,height))
					self.buttons.append(Buttons.Button())
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_lower_row1):
						i = 0
						r = 2
				elif r == 2:
					self.screens.append(self.surface.subsurface(start_x+(width+offset_space+offset_space)+((i)*(offset_space+width)),start_y+(1*(height+offset_height)),width,height))
					self.buttons.append(Buttons.Button())
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_lower_row2):
						i = 0
						r = 3
				elif r == 3:
					self.screens.append(self.surface.subsurface(start_x+((width*2)+offset_space+offset_space)+((i)*(offset_space+width)),start_y+(2*(height+offset_height)),width,height))
					self.buttons.append(Buttons.Button())
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_lower_row3):
						i = 0
						r = 4 
				elif r == 4:
					self.screens.append(self.surface.subsurface(start_x+((width*3)+offset_space+offset_space)+((i)*(offset_space+width)),start_y+(3*(height+offset_height)),width,height))
					self.buttons.append(Buttons.Button())
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_lower_row4):
						i = 0
		else:
			while(x < self.total_l):
				if r == 1:
					self.screens.append(self.surface.subsurface(start_x+((i+1)*(offset_space+width)),start_y,width,height))
					self.buttons.append(Buttons.Button())
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_upper1):
						i = 0
						r = 2
				elif r == 2:
					self.screens.append(self.surface.subsurface(start_x+(width+offset_space+offset_space)+((i)*(offset_space+width)),start_y+(1*(height+offset_height)),width,height))
					self.buttons.append(Buttons.Button())
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_upper2):
						i = 0
						r = 3
				elif r == 3:
					self.screens.append(self.surface.subsurface(start_x+((width*2)+offset_space+offset_space)+((i)*(offset_space+width)),start_y+(2*(height+offset_height)),width,height))
					self.buttons.append(Buttons.Button())
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_upper3):
						i = 0
						r = 4 
				elif r == 4:
					self.screens.append(self.surface.subsurface(start_x+((width*3)+offset_space+offset_space)+((i)*(offset_space+width)),start_y+(3*(height+offset_height)),width,height))
					self.buttons.append(Buttons.Button())
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_upper4):
						i = 0

		background_color = (255,255,255)
		self.esc_surface.fill(background_color)
		self.tab_surface.fill(background_color)
		self.caps_surface.fill(background_color)
		self.enter_surface.fill(background_color)
		self.lshift_surface.fill(background_color)
		self.rshift_surface.fill(background_color)
		self.clear_surface.fill(background_color)
		self.space_surface.fill(background_color)
		self.com_surface.fill(background_color)
		self.exit_surface.fill(background_color)
		for x in range(0,self.total_l):
			self.screens[x].fill(background_color)		

	def button_cmd(self,cmd):
		shift_switch = False

		if cmd == "Exit":
			self.text_field = "URL: #EXIT"
		elif cmd == "Esc":
			if(self.shift_on):
				shift_switch = True
		elif cmd == "Enter":
			pass
		elif cmd == "CLEAR":
			self.text_field = "URL: "
			self.entry_display(self.text_field)
			if(self.shift_on):
				shift_switch = True
		elif cmd == "LShift":
			if(self.case == "lower"):
				self.case = "upper"
				self.keyboard_button_init(False)
				self.draw_buttons_init(False)
			elif(self.case == "upper"):
				self.case = "lower"
				self.keyboard_button_init(True)
				self.draw_buttons_init(True)
			self.shift_on = not self.shift_on			
		elif cmd == "Caps":
			if(self.case == "lower"):
				self.case = "upper"
				self.keyboard_button_init(False)
				self.draw_buttons_init(False)
			elif(self.case == "upper"):
				self.case = "lower"
				self.keyboard_button_init(True)
				self.draw_buttons_init(True)
		elif cmd == "Bck":
			if(len(self.text_field) > len("URL: ")):
				self.text_field = self.text_field[:-1]				
				self.entry_display(self.text_field)
			if(self.shift_on):
				shift_switch = True	
		elif((len(self.text_field)) + len(cmd) <= 50):	
			if cmd == "Tab":
				self.text_field += "    "
				self.entry_display(self.text_field)
				if(self.shift_on):
					shift_switch = True	
			else:
				self.text_field += cmd
				self.entry_display(self.text_field)
				if(self.shift_on):
					shift_switch = True	

		if(shift_switch):
			self.shift_on = False
			if(self.case == "lower"):
				self.case = "upper"
				self.keyboard_button_init(False)
				self.draw_buttons_init(False)
			elif(self.case == "upper"):
				self.case = "lower"
				self.keyboard_button_init(True)
				self.draw_buttons_init(True)	

	def draw_buttons_init(self,lower):
		idle_color = (255,255,255)
		text_color = (0,0,0)
		width = self.board_button_w
		height = self.board_button_h
		offset_space = self.board_offset_w
		offset_height = self.board_offset_h

		#Parameters:					  surface,		 color,       x, y,		length, height, width, 		 text,	text_color
		#Row 1
		self.esc_button.create_button(self.esc_surface, idle_color, 0, 0, width, height,	0, "Esc", text_color,False)
		self.bckspce_button.create_button(self.bckspce_surface, idle_color, 0,0, width*2, height, 0, "Bck", text_color,False)

		#Row 2
		self.tab_button.create_button(self.tab_surface, idle_color, 0,0, width+offset_space, height,	0, "Tab", text_color,False)
		self.fwd_slash_button.create_button(self.fwd_surface, idle_color, 0,0, (width*3), height, 0, "\\", text_color,False)	

		#Row 3
		self.caps_button.create_button(self.caps_surface, idle_color, 0,0, (width*2)+offset_space, height,0, "Caps", text_color,False)	
		self.enter_button.create_button(self.enter_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "Enter", text_color,False)		

		#Row 4
		self.left_shift_button.create_button(self.lshift_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "LShift", text_color,False)	
		self.right_shift_button.create_button(self.rshift_surface, idle_color, 0,0, (3*width)+(2*offset_space), height, 0, "www.", text_color,False)	

		#Row 5
		self.clear_button.create_button(self.clear_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "CLEAR", text_color,False)
		self.space_button.create_button(self.space_surface, idle_color, 0,0, (width*10)+(offset_space*9), height, 0, " ", text_color,False)
		self.com_button.create_button(self.com_surface, idle_color, 0,0, width+offset_space, height, 0, ".com", text_color,False)
		self.exit_button.create_button(self.exit_surface, idle_color, 0,0, (2*width), height, 0, "Exit", text_color,False)	

		if(lower):
			x = 0
			i = 0
			r = 1
			while(x < self.total_l):
				if r == 1:
					self.buttons[x].create_button(self.screens[x],idle_color,0,0, width, height, 0, self.keyboard_button_text_lower_row1[i], text_color,False)
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_lower_row1):
						i = 0
						r = 2
				elif r == 2:
					self.buttons[x].create_button(self.screens[x],idle_color,0,0, width, height, 0, self.keyboard_button_text_lower_row2[i], text_color,False)
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_lower_row2):
						i = 0
						r = 3
				elif r == 3:
					self.buttons[x].create_button(self.screens[x],idle_color,0,0, width, height, 0, self.keyboard_button_text_lower_row3[i], text_color,False)
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_lower_row3):
						i = 0
						r = 4 
				elif r == 4:
					self.buttons[x].create_button(self.screens[x],idle_color,0,0, width, height, 0, self.keyboard_button_text_lower_row4[i], text_color,False)
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_lower_row4):
						i = 0
						r = 0  
		else:
			x = 0
			i = 0
			r = 1
			while(x < self.total_l):
				if r == 1:
					self.buttons[x].create_button(self.screens[x],idle_color,0,0, width, height, 0, self.keyboard_button_text_upper1[i], text_color,False)
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_upper1):
						i = 0
						r = 2
				elif r == 2:
					self.buttons[x].create_button(self.screens[x],idle_color,0,0, width, height, 0, self.keyboard_button_text_upper2[i], text_color,False)
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_upper2):
						i = 0
						r = 3
				elif r == 3:
					self.buttons[x].create_button(self.screens[x],idle_color,0,0, width, height, 0, self.keyboard_button_text_upper3[i], text_color,False)
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_upper3):
						i = 0
						r = 4 
				elif r == 4:
					self.buttons[x].create_button(self.screens[x],idle_color,0,0, width, height, 0, self.keyboard_button_text_upper4[i], text_color,False)
					x += 1
					i += 1
					if i == len(self.keyboard_button_text_upper4):
						i = 0
						r = 0 

		pygame.display.update()				 				

	def draw_buttons(self,selected,last,active):
		fill_color = (255,255,255)
		idle_color = (255,255,255)
		text_color = (0,0,0)
		selected_color = (117,186,255)
		
		a_c1 = (200,200,200)
		a_c2 = (154,226,250)
		active_color = a_c2

		width = self.board_button_w
		height = self.board_button_h
		offset_space = self.board_offset_w
		offset_height = self.board_offset_h
		
		if(active):
			if(selected != last):
				if(last == "NaN"):
					pass
				elif(last == "Esc"):
					self.esc_surface.fill(fill_color)	
					self.esc_button.create_button(self.esc_surface, idle_color, 0, 0, width, height,	0, "Esc", text_color, not active)
				elif(last == "Bck"):
					self.bckspce_surface.fill(fill_color)	
					self.bckspce_button.create_button(self.bckspce_surface, idle_color, 0,0, width*2, height, 0, "Bck", text_color, not active)		
				elif(last == "Tab"):
					self.tab_surface.fill(fill_color)	
					self.tab_button.create_button(self.tab_surface, idle_color, 0,0, width+offset_space, height,	0, "Tab", text_color, not active)
				elif(last == "\\"):
					self.fwd_surface.fill(fill_color)	
					self.fwd_slash_button.create_button(self.fwd_surface, idle_color, 0,0, (width*3), height, 0, "\\", text_color, not active)	
				elif(last == "Caps"):
					self.caps_surface.fill(fill_color)	
					self.caps_button.create_button(self.caps_surface, idle_color, 0,0, (width*2)+offset_space, height,0, "Caps", text_color, not active)	
				elif(last == "Enter"):
					self.enter_surface.fill(fill_color)	
					self.enter_button.create_button(self.enter_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "Enter", text_color,not active)
				elif(last == "LShift"):
					self.lshift_surface.fill(fill_color)	
					self.left_shift_button.create_button(self.lshift_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "LShift", text_color,not active)	
				elif(last == "www."):
					self.rshift_surface.fill(fill_color)	
					self.right_shift_button.create_button(self.rshift_surface, idle_color, 0,0, (3*width)+(2*offset_space), height, 0, "www.", text_color,not active)
				elif(last == "CLEAR"):
					self.clear_surface.fill(fill_color)	
					self.clear_button.create_button(self.clear_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "CLEAR", text_color,not active)
				elif(last == " "):
					self.space_surface.fill(fill_color)	
					self.space_button.create_button(self.space_surface, idle_color, 0,0, (width*10)+(offset_space*9), height, 0, " ", text_color,not active)
				elif(last == ".com"):
					self.com_surface.fill(fill_color)	
					self.com_button.create_button(self.com_surface, idle_color, 0,0, width+offset_space, height, 0, ".com", text_color,not active)
				elif(last == "Exit"):
					self.exit_surface.fill(fill_color)	
					self.exit_button.create_button(self.exit_surface, idle_color, 0,0, (2*width), height, 0, "Exit", text_color,not active)								
				else:
					self.screens[int(last)].fill(fill_color)
					self.buttons[int(last)].create_button(self.screens[int(last)],idle_color,0,0,width,height,0,self.buttons[int(last)].get_text(),text_color, not active)	

				if(selected == "NaN"):
					pass
				elif(selected == "Esc"):
					self.esc_surface.fill(fill_color)	
					self.esc_button.create_button(self.esc_surface, active_color, 0, 0, width, height,	0, "Esc", text_color, active)
				elif(selected == "Bck"):
					self.bckspce_surface.fill(fill_color)	
					self.bckspce_button.create_button(self.bckspce_surface, active_color, 0,0, width*2, height, 0, "Bck", text_color, active)		
				elif(selected == "Tab"):
					self.tab_surface.fill(fill_color)	
					self.tab_button.create_button(self.tab_surface, active_color, 0,0, width+offset_space, height,	0, "Tab", text_color, active)
				elif(selected == "\\"):
					self.fwd_surface.fill(fill_color)	
					self.fwd_slash_button.create_button(self.fwd_surface, active_color, 0,0, (width*3), height, 0, "\\", text_color, active)	
				elif(selected == "Caps"):
					self.caps_surface.fill(fill_color)	
					self.caps_button.create_button(self.caps_surface, active_color, 0,0, (width*2)+offset_space, height,0, "Caps", text_color, active)	
				elif(selected == "Enter"):
					self.enter_surface.fill(fill_color)	
					self.enter_button.create_button(self.enter_surface, active_color, 0,0, (width*3)+offset_space, height, 0, "Enter", text_color, active)
				elif(selected == "LShift"):
					self.lshift_surface.fill(fill_color)	
					self.left_shift_button.create_button(self.lshift_surface, active_color, 0,0, (width*3)+offset_space, height, 0, "LShift", text_color, active)	
				elif(selected == "www."):
					self.rshift_surface.fill(fill_color)	
					self.right_shift_button.create_button(self.rshift_surface, active_color, 0,0, (3*width)+(2*offset_space), height, 0, "www.", text_color, active)	
				elif(selected == "CLEAR"):
					self.clear_surface.fill(fill_color)	
					self.clear_button.create_button(self.clear_surface, active_color, 0,0, (width*3)+offset_space, height, 0, "CLEAR", text_color,active)
				elif(selected == " "):
					self.space_surface.fill(fill_color)	
					self.space_button.create_button(self.space_surface, active_color, 0,0, (width*10)+(offset_space*9), height, 0, " ", text_color,active)
				elif(selected == ".com"):
					self.com_surface.fill(fill_color)	
					self.com_button.create_button(self.com_surface, active_color, 0,0, width+offset_space, height, 0, ".com", text_color,active)
				elif(selected == "Exit"):
					self.exit_surface.fill(fill_color)	
					self.exit_button.create_button(self.exit_surface, active_color, 0,0, (2*width), height, 0, "Exit", text_color,active)			
				else:
					self.screens[int(selected)].fill(fill_color)
					self.buttons[int(selected)].create_button(self.screens[int(selected)],active_color,0,0,width,height,0,self.buttons[int(selected)].get_text(),text_color, active)
			else:
				if(selected == "NaN"):
					pass
				elif(selected == "Esc"):
					self.esc_surface.fill(fill_color)	
					self.esc_button.create_button(self.esc_surface, active_color, 0, 0, width, height,	0, "Esc", text_color, active)
				elif(selected == "Bck"):
					self.bckspce_surface.fill(fill_color)	
					self.bckspce_button.create_button(self.bckspce_surface, active_color, 0,0, width*2, height, 0, "Bck", text_color, active)		
				elif(selected == "Tab"):
					self.tab_surface.fill(fill_color)	
					self.tab_button.create_button(self.tab_surface, active_color, 0,0, width+offset_space, height,	0, "Tab", text_color, active)
				elif(selected == "\\"):
					self.fwd_surface.fill(fill_color)	
					self.fwd_slash_button.create_button(self.fwd_surface, active_color, 0,0, (width*3), height, 0, "\\", text_color, active)	
				elif(selected == "Caps"):
					self.caps_surface.fill(fill_color)	
					self.caps_button.create_button(self.caps_surface, active_color, 0,0, (width*2)+offset_space, height,0, "Caps", text_color, active)	
				elif(selected == "Enter"):
					self.enter_surface.fill(fill_color)	
					self.enter_button.create_button(self.enter_surface, active_color, 0,0, (width*3)+offset_space, height, 0, "Enter", text_color, active)
				elif(selected == "LShift"):
					self.lshift_surface.fill(fill_color)	
					self.left_shift_button.create_button(self.lshift_surface, active_color, 0,0, (width*3)+offset_space, height, 0, "LShift", text_color, active)	
				elif(selected == "www."):
					self.rshift_surface.fill(fill_color)	
					self.right_shift_button.create_button(self.rshift_surface, active_color, 0,0, (3*width)+(2*offset_space), height, 0, "www.", text_color, active)
				elif(selected == "CLEAR"):
					self.clear_surface.fill(fill_color)	
					self.clear_button.create_button(self.clear_surface, active_color, 0,0, (width*3)+offset_space, height, 0, "CLEAR", text_color, active)
				elif(selected == " "):
					self.space_surface.fill(fill_color)	
					self.space_button.create_button(self.space_surface, active_color, 0,0, (width*10)+(offset_space*9), height, 0, " ", text_color,active)
				elif(selected == ".com"):
					self.com_surface.fill(fill_color)	
					self.com_button.create_button(self.com_surface, active_color, 0,0, width+offset_space, height, 0, ".com", text_color,active)
				elif(selected == "Exit"):
					self.exit_surface.fill(fill_color)	
					self.exit_button.create_button(self.exit_surface, active_color, 0,0, (2*width), height, 0, "Exit", text_color,active)		
				else:
					self.screens[int(selected)].fill(fill_color)
					self.buttons[int(selected)].create_button(self.screens[int(selected)],active_color,0,0,width,height,0,self.buttons[int(selected)].get_text(),text_color, active)
		else:
			if(last == "NaN"):
				pass
			elif(last == "Esc"):
				self.esc_surface.fill(fill_color)	
				self.esc_button.create_button(self.esc_surface, idle_color, 0, 0, width, height,	0, "Esc", text_color, not active)
			elif(last == "Bck"):
				self.bckspce_surface.fill(fill_color)	
				self.bckspce_button.create_button(self.bckspce_surface, idle_color, 0,0, width*2, height, 0, "Bck", text_color, not active)		
			elif(last == "Tab"):
				self.tab_surface.fill(fill_color)	
				self.tab_button.create_button(self.tab_surface, idle_color, 0,0, width+offset_space, height,	0, "Tab", text_color, not active)
			elif(last == "\\"):
				self.fwd_surface.fill(fill_color)	
				self.fwd_slash_button.create_button(self.fwd_surface, idle_color, 0,0, (width*3), height, 0, "\\", text_color, not active)	
			elif(last == "Caps"):
				self.caps_surface.fill(fill_color)	
				self.caps_button.create_button(self.caps_surface, idle_color, 0,0, (width*2)+offset_space, height,0, "Caps", text_color, not active)	
			elif(last == "Enter"):
				self.enter_surface.fill(fill_color)	
				self.enter_button.create_button(self.enter_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "Enter", text_color, not active)
			elif(last == "LShift"):
				self.lshift_surface.fill(fill_color)	
				self.left_shift_button.create_button(self.lshift_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "LShift", text_color, not active)	
			elif(last == "www."):
				self.rshift_surface.fill(fill_color)	
				self.right_shift_button.create_button(self.rshift_surface, idle_color, 0,0, (3*width)+(2*offset_space), height, 0, "www.", text_color, not active)
			elif(last == "CLEAR"):
				self.clear_surface.fill(fill_color)	
				self.clear_button.create_button(self.clear_surface, idle_color, 0,0, (width*3)+offset_space, height, 0, "CLEAR", text_color,not active)
			elif(last == " "):
				self.space_surface.fill(fill_color)	
				self.space_button.create_button(self.space_surface, idle_color, 0,0, (width*10)+(offset_space*9), height, 0, " ", text_color,not active)
			elif(last == ".com"):
				self.com_surface.fill(fill_color)	
				self.com_button.create_button(self.com_surface, idle_color, 0,0, width+offset_space, height, 0, ".com", text_color,not active)
			elif(last == "Exit"):
				self.exit_surface.fill(fill_color)	
				self.exit_button.create_button(self.exit_surface, idle_color, 0,0, (2*width), height, 0, "Exit", text_color,not active)		
			else:
				self.screens[int(last)].fill(fill_color)
				self.buttons[int(last)].create_button(self.screens[int(last)],idle_color,0,0,width,height,0,self.buttons[int(last)].get_text(),text_color, not active)

		pygame.display.update()

	def main(self):
		lower = True
		lastButton = "NaN"
		currentButton = "NaN"
		self.display_init()
		self.keyboard_button_init(lower)
		self.draw_buttons_init(lower)
		self.entry_display(self.text_field)
		
		while(1):
			for event in pygame.event.get():
				if(event.type == pygame.MOUSEBUTTONDOWN):
					if(self.esc_button.pressed_subsurface(pygame.mouse.get_pos())):
						currentButton = "Esc"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.bckspce_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Bck"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.tab_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Tab"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.fwd_slash_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "\\"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.caps_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Caps"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.enter_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Enter"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.left_shift_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "LShift"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.right_shift_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "www."
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.clear_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "CLEAR"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.space_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = " "
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.com_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = ".com"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton
					elif(self.exit_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Exit"
						self.draw_buttons(currentButton,lastButton,True)
						lastButton = currentButton				
					else:
						found = False
						for x in range(0, len(self.buttons)):
							if(self.buttons[x].pressed_subsurface(pygame.mouse.get_pos())):
								currentButton = str(x)
								self.draw_buttons(currentButton,lastButton,True)
								lastButton = currentButton
								found = True
						if(not found):
							currentButton = "NaN"
							self.draw_buttons(currentButton,lastButton,True)
							lastButton = currentButton
				elif(event.type == pygame.MOUSEBUTTONUP):
					if(self.esc_button.pressed_subsurface(pygame.mouse.get_pos())):
						currentButton = "Esc"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)
						lastButton = currentButton
					elif(self.bckspce_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Bck"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)
						lastButton = currentButton
					elif(self.tab_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Tab"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)						
						lastButton = currentButton
					elif(self.fwd_slash_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "\\"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)						
						lastButton = currentButton
					elif(self.caps_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Caps"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)				
						lastButton = currentButton
					elif(self.enter_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Enter"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)
							return	
						lastButton = currentButton
					elif(self.left_shift_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "LShift"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)						
						lastButton = currentButton
					elif(self.right_shift_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "www."
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)						
						lastButton = currentButton
					elif(self.clear_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "CLEAR"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)	
						lastButton = currentButton
					elif(self.space_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = " "
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)	
						lastButton = currentButton
					elif(self.com_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = ".com"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)	
						lastButton = currentButton
					elif(self.exit_button.pressed_subsurface(pygame.mouse.get_pos())):	
						currentButton = "Exit"
						self.draw_buttons(currentButton,lastButton,False)
						if(currentButton == lastButton):
							self.button_cmd(currentButton)
							return	
						lastButton = currentButton			
					else:
						found = False
						for x in range(0, len(self.buttons)):
							if(self.buttons[x].pressed_subsurface(pygame.mouse.get_pos())):
								currentButton = str(x)
								self.draw_buttons(currentButton,lastButton,False)
								if(currentButton == lastButton):
									self.button_cmd(self.buttons[x].get_text())								
								lastButton = currentButton
								found = True
						if(not found):
							currentButton = "NaN"
							self.draw_buttons(currentButton,lastButton,False)
							lastButton = currentButton		
				# else:
				# 	if(self.esc_button.pressed_subsurface(pygame.mouse.get_pos())):
				# 		currentButton = "Esc"
				# 		self.draw_buttons(currentButton,lastButton,False)
				# 		lastButton = currentButton
				# 	elif(self.bckspce_button.pressed_subsurface(pygame.mouse.get_pos())):	
				# 		currentButton = "Bck"
				# 		self.draw_buttons(currentButton,lastButton,False)
				# 		lastButton = currentButton
				# 	elif(self.tab_button.pressed_subsurface(pygame.mouse.get_pos())):	
				# 		currentButton = "Tab"
				# 		self.draw_buttons(currentButton,lastButton,False)
				# 		lastButton = currentButton
				# 	elif(self.fwd_slash_button.pressed_subsurface(pygame.mouse.get_pos())):	
				# 		currentButton = "\\"
				# 		self.draw_buttons(currentButton,lastButton,False)
				# 		lastButton = currentButton
				# 	elif(self.caps_button.pressed_subsurface(pygame.mouse.get_pos())):	
				# 		currentButton = "Caps"
				# 		self.draw_buttons(currentButton,lastButton,False)
				# 		lastButton = currentButton
				# 	elif(self.enter_button.pressed_subsurface(pygame.mouse.get_pos())):	
				# 		currentButton = "Enter"
				# 		self.draw_buttons(currentButton,lastButton,False)
				# 		lastButton = currentButton
				# 	elif(self.left_shift_button.pressed_subsurface(pygame.mouse.get_pos())):	
				# 		currentButton = "LShift"
				# 		self.draw_buttons(currentButton,lastButton,False)
				# 		lastButton = currentButton
				# 	elif(self.right_shift_button.pressed_subsurface(pygame.mouse.get_pos())):	
				# 		currentButton = "RShift"
				# 		self.draw_buttons(currentButton,lastButton,False)
				# 		lastButton = currentButton
				# 	else:
				# 		found = False
				# 		for x in range(0, len(self.buttons)):
				# 			if(self.buttons[x].pressed_subsurface(pygame.mouse.get_pos())):
				# 				currentButton = str(x)
				# 				self.draw_buttons(currentButton,lastButton,False)
				# 				lastButton = currentButton
				# 				found = True
				# 		if(not found):
				# 			currentButton = "NaN"
				# 			self.draw_buttons(currentButton,lastButton,False)
				# 			lastButton = currentButton
if __name__ == '__main__':
	obj = Keyboard()