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
		self.path = os.path.dirname(os.path.abspath(__file__))
		pygame.display.init()
		os.putenv('SDL_VIDEODRIVER', 'fbcon')
		os.putenv('SDL_FBDEV'      , '/dev/fb0')
		pygame.mouse.set_visible(False)
		pygame.font.init()
		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

		self.surface = pygame.display.set_mode(size, pygame.FULLSCREEN)
		self.surface_color = (0,0,0)
		self.surface.fill(self.surface_color)

		#self.display_font = "saxmono.ttf"
		self.display_font = self.path +"/swiss 721.ttf"
		self.bold = False
		self.font_size = 85
		self.width_sep = 25
		self.top = 10
		self.display_surface_color = (0,0,0)
		self.display_color_pos = (0,255,0)
		self.display_color_neg = (255,0,0)
		self.display_color_unchanged = (62,62,255)
		self.display_color_white = (255,255,255)
		self.img_up = pygame.image.load(self.path+ '/up_filled_trp.png')
		self.img_down = pygame.image.load(self.path +'/down_filled_trp.png')

		self.img_space = self.surface.get_height()-self.get_font_ascent()+1
		self.img_dim = self.surface.get_height() - (2*self.img_space)
		self.img_up = pygame.transform.scale(self.img_up,(self.img_dim,self.img_dim))
		self.img_down = pygame.transform.scale(self.img_down,(self.img_dim,self.img_dim))
		self.updated_list = []
		self.list_indexes = []
		self.surfaces = []
		self.item_infos = []
		self.total_width = 0

		for i in range(0,self.top):
			self.item_infos.append("")

	def get_font_height(self):
		font = pygame.font.Font(self.display_font,self.font_size)
		return font.get_height()

	def get_font_ascent(self):
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

		info_list = []
		for i in index_list:
			info_list.append(self.get_symbol_info(i))

		q.put(info_list)	
		print "finished..."	

	def get_symbol_info(self,symbol):
		yahoo = Share(symbol)
		name = symbol
		string = name + " " + str(yahoo.get_price()) + " " + str(yahoo.get_change())
		symbol_info = []
		symbol_info.append(name)
		symbol_info.append(str(yahoo.get_price()))
		symbol_info.append(str(yahoo.get_change()))
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

	def get_updated_list(self):
		return self.updated_list

	def update_updated_list(self,newlist):
		self.updated_list = newlist	

	def update_item_infos(self,update):
		self.item_infos = update


	def init_infos(self):
		for i in range(0,self.top):
			self.item_infos[i] = ""
			self.item_infos[i] = self.get_symbol_info(self.list_indexes[i])

	def get_item_surface_info(self, symbol_info):
		image_width = 0
		if("+" in symbol_info[2][0] or "-" in symbol_info[2][0]):
			image_width = self.img_dim

		height = self.font_size	
		width = symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep + image_width + symbol_info[2][1][0]

		return (width,height)

	def display_item(self,symbol_info,surface,x,y):
		display_color = self.display_color_unchanged
		if("+" in symbol_info[2][0]):
			display_color = self.display_color_pos
		elif("-" in symbol_info[2][0]):
			display_color = self.display_color_neg

		self.image_width = 0
		if("+" in symbol_info[2][0] or "-" in symbol_info[2][0]):
			self.image_width = self.img_up.get_rect().size[0]

		#top_h = max(symbol_info[0][1][1],symbol_info[1][1][1],symbol_info[2][1][1])
		#self.current_width = symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep + self.image_width + symbol_info[2][1][0]

		self.print_string(surface,symbol_info[0][0],(x,y),self.display_color_white,self.display_font,self.font_size)
		self.print_string(surface,symbol_info[1][0],(x+symbol_info[0][1][0]+self.width_sep,y),display_color,self.display_font,self.font_size)

		image_width = 0
		if("+" in symbol_info[2][0] or "-" in symbol_info[2][0]):
			image_width = self.img_dim
			if("+" in symbol_info[2][0]):
				surface.blit(self.img_up,(x+ symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep,y+self.img_space+1))
			else:
				surface.blit(self.img_down,(x+ symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep,y+self.img_space+1))


		self.print_string(surface,symbol_info[2][0][1:],(x+symbol_info[0][1][0] + self.width_sep + symbol_info[1][1][0] + self.width_sep + image_width,y),display_color,self.display_font,self.font_size)

	def draw_item(self,info,item,x):
		temp_surface = pygame.Surface(self.get_item_surface_info(info))
		self.display_item(info,temp_surface,0,0)
		#self.surface.blit(temp_surface,(x,self.surface.get_height()/2 - self.font_size/2))
		self.surface.blit(temp_surface,(x,self.surface.get_height()/2 - self.get_font_height()/2))

	def get_surface_width(self,item):
		return self.surfaces[item].get_width()

	def check_events(self):
		for event in pygame.event.get():
			if(event.type == pygame.MOUSEBUTTONUP):
				self.exit()

	def get_centered_text_position(self,surface,text,font,size,bold):
		font = pygame.font.Font(font,size)
		font.set_bold(bold)
		x = surface.get_width()/2 - font.size(text)[0]/2
		y = surface.get_height()/2 - font.size(text)[1]/2
		return (x,y)

	def exit(self):
		pygame.display.quit()
		os._exit(1)

	def run(self):

		self.init_display()
		self.surface.fill(self.surface_color)
		self.print_string(self.surface,"Processing Information.",self.get_centered_text_position(self.surface,"Processing Information.",self.display_font,40,self.bold),self.display_color_white,self.display_font,40)
		pygame.display.update()
		self.init_stock_list(self.top)
		self.surface.fill(self.surface_color)
		self.print_string(self.surface,"Processing Information..",self.get_centered_text_position(self.surface,"Processing Information..",self.display_font,40,self.bold),self.display_color_white,self.display_font,40)
		pygame.display.update()
		self.init_infos()
		self.surface.fill(self.surface_color)

		step = 2
		startx = self.surface.get_width()
		item = 0
		item_info = self.item_infos[item]
		width = self.get_item_surface_info(item_info)[0]

		processes = []
		p_start = True
		q = Queue()

		
		while(1):
			if(p_start):
				p_start = False
				p = mp.Process(target=self.update_list,args=(q,self.top))
				processes.append(p)
				processes[0].start()

			j = 0
			while j < width:
				for event in pygame.event.get():
					if(event.type == pygame.MOUSEBUTTONUP):
						return

				self.surface.scroll(-step,0)
				self.draw_item(item_info,item,startx-j)
				pygame.display.update()
				j += step
				
			for x in range(0,self.width_sep):
				for event in pygame.event.get():
					if(event.type == pygame.MOUSEBUTTONUP):
						return


				for i in range(0,40000/(step/2)):
					pass
				self.surface.scroll(-step,0)
				pygame.display.update()

				
			item += 1
			if item == self.top:
				items = q.get()
				processes[0].join()
				newlist = []
				for i in items:
					newlist.append(i)
				self.update_updated_list(newlist)

				processes = []
				p_start = True
				q = Queue()
				item = 0
				self.update_item_infos(self.get_updated_list())

			item_info = self.item_infos[item]
			width = self.get_item_surface_info(item_info)[0]
	

			for event in pygame.event.get():
				if(event.type == pygame.MOUSEBUTTONUP):
					return

if __name__ == '__main__':
	demo = stockDemo()
	demo.run()	