from pygame.locals import *
from yahoo_finance import Share
import multiprocessing as mp
from multiprocessing import Queue
import multiprocessing
import stock_indexes
import pygame
import os, sys

class stockDemo():
	def __init__(self):
		pass

	def init_display(self):
		pygame.display.init()
		os.putenv('SDL_VIDEODRIVER', 'fbcon')
		os.putenv('SDL_FBDEV'      , '/dev/fb0')
		pygame.mouse.set_visible(False)
		pygame.font.init()
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

		self.surface = pygame.display.set_mode(size, pygame.FULLSCREEN)
		self.surface_color = (0,0,0)
		self.surface.fill(self.surface_color)

		self.display_font = "saxmono.ttf"
		self.bold = False
		self.font_size = 85
		self.font_size_lower = 0
		self.width_sep = 25
		self.top = 10
		self.display_surface_color = (0,0,0)
		self.display_color_pos = (0,255,0)
		self.display_color_neg = (255,0,0)
		self.display_color_unchanged = (62,62,255)
		self.display_color_white = (255,255,255)
		self.img_up = pygame.image.load('up_trp.png')
		self.img_down = pygame.image.load('down_trp.png')

		img_dim = self.get_img_size()
		self.img_up = pygame.transform.scale(self.img_up,(img_dim,img_dim))
		self.img_down = pygame.transform.scale(self.img_down,(img_dim,img_dim))
		self.updated_list = []
		self.list_indexes = []

	def get_img_size(self):
		font = pygame.font.Font(self.display_font,self.font_size)
		return font.get_ascent()		

	def print_string(self,surface,string,position,color,font,size):
		font = pygame.font.Font(font,size)
		font.set_bold(self.bold)
		fontObj = font.render(string, True, color)
		rectObj = fontObj.get_rect()

		if position[0] == 'C' or position[0] =='c':
			centerH = (pygame.display.Info().current_w /2) - (fontObj.get_width()/2)
			rectObj.topleft = (centerH, position[1])
		else:
			rectObj.topleft = position

		surface.blit(fontObj,rectObj)

	def init_stock_list(self,top):
		stocks = stock_indexes.stockIndexes(top)
		indexes = stocks.get_indexes()
		self.list_indexes = indexes[1]

	def update_list(self,q,top):
		print "running..."
		stocks = stock_indexes.stockIndexes(top)
		indexes = stocks.get_indexes()
		index_list = []
		for i in indexes[1]:
			index_list.append(i)

		q.put(index_list)	
		print "finished..."	

	def get_updated_list(self):
		return self.update_list

	def update_updated_list(self,newlist):
		self.updated_list = newlist	

	def update_list_indexes(self,update):
		self.list_indexes = update

	def init_surface(self):
		display_surface_x = 0
		display_surface_y = (self.surface.get_height()/2) - ((self.font_size)/2)
		display_surface_h = self.font_size
		display_surface_w = self.surface.get_width()

		self.display_surface = self.surface.subsurface(display_surface_x,display_surface_y,display_surface_w,display_surface_h)
		self.display_surface.fill(self.display_surface_color)

	def get_item_info(self,item):
		name = ""
		if(item >= self.top):
			yahoo = Share(self.updated_list[item])
			name = self.updated_list[item]
		else:
			yahoo = Share(self.list_indexes[item])
			name = self.list_indexes[item]
		
		string = name + " " + str(yahoo.get_price()) + " " + str(yahoo.get_change())
		symbol_info = []
		symbol_info.append(name)
		symbol_info.append(str(yahoo.get_price()))
		symbol_info.append(str(yahoo.get_change()))
		symbol_info.append(str(yahoo.get_trade_datetime()))

		if "None" in symbol_info[2]:
			symbol_info[2] = symbol_info[2][:-4]

		for i in range(0,len(symbol_info)):
			if i == 3:
				font = pygame.font.Font(self.display_font,self.font_size_lower)
			else:
				font = pygame.font.Font(self.display_font,self.font_size)

			font.set_bold(self.bold)
			symbol_info[i] = (symbol_info[i],font.size(symbol_info[i]))

		return symbol_info

	def display_item(self,symbol_info,x):
		display_color = self.display_color_unchanged
		if("+" in symbol_info[2][0]):
			display_color = self.display_color_pos
		elif("-" in symbol_info[2][0]):
			display_color = self.display_color_neg



		self.image_width = 0
		if("+" in symbol_info[2][0] or "-" in symbol_info[2][0]):
			self.image_width = self.img_up.get_rect().size[0]

		top_h = max(symbol_info[0][1][1],symbol_info[1][1][1],symbol_info[2][1][1])
		self.current_width = symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep + self.image_width + symbol_info[2][1][0]

		self.print_string(self.display_surface,symbol_info[0][0],(x,0),self.display_color_white,self.display_font,self.font_size)
		self.print_string(self.display_surface,symbol_info[1][0],(x+symbol_info[0][1][0]+self.width_sep,0),display_color,self.display_font,self.font_size)

		if("+" in symbol_info[2][0] or "-" in symbol_info[2][0]):
			if("+" in symbol_info[2][0]):
				self.display_surface.blit(self.img_up,(x+ symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep,0))
			else:
				self.display_surface.blit(self.img_down,(x+ symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep,0))


		self.print_string(self.display_surface,symbol_info[2][0][1:],(x+symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep + self.image_width,0),display_color,self.display_font,self.font_size)
		#self.display_copy = self.display_surface

		
	
	# def item_scroll(self,x):
	# 	self.display_surface.unlock()
	# 	self.surface.blit(self.display_surface,(x,self.display_surface.get_offset()[1]))
	# 	self.display_surface.lock()
	# 	pygame.display.update()

	# def init_surface_info(self,item):
	# 	yahoo = Share(self.list_indexes[item])
	# 	string =  self.list_indexes[item] + " " + str(yahoo.get_price()) + " " + str(yahoo.get_change())
	# 	symbol_info = []
	# 	symbol_info.append(self.list_indexes[item])
	# 	symbol_info.append(str(yahoo.get_price()))
	# 	symbol_info.append(str(yahoo.get_change()))
	# 	symbol_info.append(str(yahoo.get_trade_datetime()))

	# 	if "None" in symbol_info[2]:
	# 		symbol_info[2] = symbol_info[2][:-4]

	# 	for i in range(0,len(symbol_info)):
	# 		if i == 3:
	# 			font = pygame.font.Font(self.display_font,self.font_size_lower)
	# 		else:
	# 			font = pygame.font.Font(self.display_font,self.font_size)

	# 		font.set_bold(self.bold)
	# 		symbol_info[i] = (symbol_info[i],font.size(symbol_info[i]))

	# 	top_h = max(symbol_info[0][1][1],symbol_info[1][1][1],symbol_info[2][1][1])
	# 	border = 0
	# 	bottom_h = 0

	# 	display_surface_x = 0
	# 	display_surface_y = (self.surface.get_height()/2) - ((top_h+border+bottom_h)/2)
	# 	display_surface_h = top_h+border+bottom_h
	# 	display_surface_w = self.surface.get_width()
	# 	self.display_surface = self.surface.subsurface(display_surface_x,display_surface_y,display_surface_w,display_surface_h)
	# 	self.display_surface.fill(self.display_surface_color)
		
	# 	self.image_width = 0
	# 	if("+" in symbol_info[2][0] or "-" in symbol_info[2][0]):
	# 		self.image_width = self.img_up.get_rect().size[0]

		
	# 	self.current_width = symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep + self.image_width + symbol_info[2][1][0]

	# 	return symbol_info

	# def item_display(self,symbol_info,x):
	# 	self.display_surface.fill(self.display_surface_color)
	# 	display_color = self.display_color_unchanged
	# 	if("+" in symbol_info[2][0]):
	# 		display_color = self.display_color_pos
	# 	elif("-" in symbol_info[2][0]):
	# 		display_color = self.display_color_neg

	# 	top_h = max(symbol_info[0][1][1],symbol_info[1][1][1],symbol_info[2][1][1])
	# 	border = 0

	# 	self.print_string(self.display_surface,symbol_info[0][0],(x,0),self.display_color_white,self.display_font,self.font_size)
	# 	self.print_string(self.display_surface,symbol_info[1][0],(x+symbol_info[0][1][0]+self.width_sep,0),display_color,self.display_font,self.font_size)

	# 	image_width = 0
	# 	if("+" in symbol_info[2][0] or "-" in symbol_info[2][0]):
	# 		if("+" in symbol_info[2][0]):
	# 			self.display_surface.blit(self.img_up,(x+ symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep,0))
	# 		else:
	# 			self.display_surface.blit(self.img_down,(x+ symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep,0))


	# 	self.print_string(self.display_surface,symbol_info[2][0][1:],(x+symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep + self.image_width,0),display_color,self.display_font,self.font_size)
	# 	self.print_string(self.display_surface,symbol_info[3][0],(x,top_h+border),self.display_color_white,self.display_font,self.font_size_lower) 

	# 	pygame.display.update()

	def exit(self):
		pygame.display.quit()
		os._exit(1)
	
	def run(self):
		dir = 1
		x1 = 0
		x2 = 0
		item = 0
		processes = []
		info1 = ""
		info2 = ""
		start = True
		first = True
		q = Queue()

		pace = 4
		self.init_display()
		self.init_stock_list(self.top)
		self.init_surface()
		info1 = self.get_item_info(item)
		if dir == 0:
			x1 = -self.current_width
			x2 = -self.current_width
		elif dir == 1:
			x1 = self.surface.get_width()
			x2 = self.surface.get_width()
		# self.item_display(info,x)	
		# self.init_display()
		for i in self.list_indexes:
			print i

		while(1):
			if(first):
				self.surface.fill(self.surface_color)
				self.display_item(info1,x1)
				pygame.display.update()
				if dir == 0:
					x1 += pace
				elif dir == 1:
					x1 -= pace
			else:
				if item+1 == 10:
					items = q.get()
					processes[0].join()
					newlist = []
					for i in items:
						newlist.append(i)
					self.update_updated_list(newlist)

				self.surface.fill(self.surface_color)
				self.display_item(info1,x1)
				self.display_item(info2,x2)
				pygame.display.update()
				if dir == 0:
					x1 += pace
					x2 += pace
				elif dir == 1:
					x1 -= pace
					x2 -= pace


			if start == True:
				start = False
				p = mp.Process(target=self.update_list,args=(q,self.top))
				processes.append(p)
				processes[0].start()

			if(((dir == 0 and x1 == (self.surface.get_width()*3)/4) or  (dir == 1 and x1 == 0))):
				if first:
					first = False
					item += 1
					info2 = self.get_item_info(item)
				else:
					print
					item += 2
					if(item >= self.top):
						processes = []
						start = True
						q = Queue()
						item = 1
						self.update_list_indexes(self.get_updated_list())

					x2 = self.surface.get_width()
					info2 = self.get_item_info(item+1)
			elif(not first and ((dir == 0 and x2 == (self.surface.get_width()*3)/4) or  (dir == 1 and x2 == 0))):
				x1 = self.surface.get_width()
				info1 = self.get_item_info(item)

			for event in pygame.event.get():
				if(event.type == pygame.MOUSEBUTTONUP):
					self.exit()


if __name__ == '__main__':
	demo = stockDemo()
	demo.run()	