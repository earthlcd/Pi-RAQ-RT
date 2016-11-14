from earthLCD import *
from pygame.locals import *
import pygame
import sys, math
import speed_demo.speedDemo as speed
import rss_demo.rss_demo as rss
import stock_demo.stock_demo_scroll as stock
#import alarm_demo.alarm_demo as alarm

img_dir = os.getcwd()+ "/menu_imgs/"
surface_w = 1024
surface_h = 100
button_w = 200
button_h = 30
x_init = 280
y_init = 3
font = "swiss 721.ttf"
font_color = (0,0,0)
gui = earthLCD((surface_w,surface_h))

def get_coords(number):
	button_per_row = 3
	button_per_col = 2
	button_sep_space_w = (surface_w - (button_per_row*button_w))/(button_per_row+1)
	button_sep_space_h = (surface_h - (button_per_col*button_h))/(button_per_col+1)

	space_mult_w = number % button_per_row
	if(space_mult_w == 0):
		space_mult_w = button_per_row

	x = (button_sep_space_w*space_mult_w)+(((number-1)%button_per_row)*button_w)

	button_space_y = number % button_per_row
	if(button_space_y == 0):
		button_space_y = (number / button_per_row) - 1
	else:
		button_space_y = math.floor(float(number)/float(button_per_row))

	y = (button_sep_space_h*math.ceil(float(number)/float(button_per_row)))+(button_space_y*button_h)
	return (x,y)

def create_gui():
    gui = earthLCD((surface_w,surface_h))

    gui.clearScreen((0,0,0))
    #gui.createBackground(0, img_dir+"bg.png")
    gui.createBackground(0, img_dir+"bg-2.bmp")

    # gui.createButton(0, (x_init+get_coords(1)[0], y_init+get_coords(1)[1], button_w, button_h), img_dir+"display_up.png", img_dir+"display_down.png", None, gui.buttonStateUp ,  display_demo_callBack)
    # gui.createButton(1, (x_init+get_coords(2)[0], y_init+get_coords(2)[1],button_w, button_h), img_dir+"rss_up.png", img_dir+"rss_down.png", None, gui.buttonStateUp ,  rss_demo_callBack)
    # gui.createButton(2, (x_init+get_coords(3)[0], y_init+get_coords(3)[1], button_w, button_h), img_dir+"speed_up.png", img_dir+"speed_down.png", None, gui.buttonStateUp ,  speed_demo_callBack)
    # gui.createButton(3, (x_init+get_coords(4)[0], y_init+get_coords(4)[1], button_w, button_h), img_dir+"stock_up.png", img_dir+"stock_down.png", None, gui.buttonStateUp ,  stock_demo_callBack)
    # gui.createButton(4, (x_init+get_coords(5)[0], y_init+get_coords(5)[1], button_w, button_h), img_dir+"exit_up.png", img_dir+"exit_down.png", None, gui.buttonStateUp ,  exit_callBack)
    gui.createButton(0, (x_init, y_init, button_w, button_h), img_dir+"display_2_up.png", img_dir+"display_2_down.png", None, gui.buttonStateUp , display_demo_callBack)
    gui.createButton(1, (x_init+200+25, y_init, button_w, button_h), img_dir+"rss_2_up.png", img_dir+"rss_2_down.png", None, gui.buttonStateUp ,  rss_demo_callBack)
    gui.createButton(2, (x_init+200+25+200+25, y_init, button_w, button_h), img_dir+"speed_2_up.png", img_dir+"speed_2_down.png", None, gui.buttonStateUp ,  speed_demo_callBack)
    gui.createButton(3, (x_init, y_init+33, button_w, button_h), img_dir+"stock_2_up.png", img_dir+"stock_2_down.png", None, gui.buttonStateUp ,  stock_demo_callBack)
    gui.createButton(4, (x_init+200+25, y_init+33, button_w, button_h), img_dir+"exit_2_up.png", img_dir+"exit_2_down.png", None, gui.buttonStateUp ,  exit_callBack)
    

    gui.createTextBox(5, (700, 72), font, 12, '10x1 Demo From EarthLCD', font_color, 'Left',False)
    gui.createTextBox(6, (870, 72), font, 12, '(c)2015 EarthLCD.com', font_color, 'Left',False)

    pygame.mouse.set_visible(True)


if __name__ == '__main__':
    def exit_callBack():
    	pygame.display.quit()
        os._exit(0)

    def display_demo_callBack():
        #alarm()
        print "display demo"
    	create_gui() 

    def speed_demo_callBack():
    	speed.speedDemo()
    	create_gui()

    def rss_demo_callBack():
    	rss.rssDemo()
    	create_gui()

    def stock_demo_callBack():
    	obj = stock.stockDemo()
    	obj.run()
    	create_gui() 
        
    create_gui()    

    while True:
        # Process any events (only mouse events for now).
        for event in pygame.event.get():
            #print event.type
            #print pygame.mouse.get_pos()
            x,y = pygame.mouse.get_pos()
            if event.type == 5:
                id = gui.checkWidgets(x, y, event.type)
                if id !=None:
                    if gui.widgets[id][1] == gui.button :
                        gui.updateButton(id, gui.buttonStateDown)
    #                if gui.widgets[id][1] == gui.checkBox :
    #                    gui.updateCheckbox(id, gui.checkBoxStateToggle)
            if event.type == 6:
                id = gui.checkWidgets(x, y, event.type)
                if id !=None:
                    if gui.widgets[id][1] == gui.button and gui.widgets[id][gui.buttonWidgetState] !=gui.buttonStateDisabled:
                        gui.updateButton(id, gui.buttonStateUp)
                        gui.widgets[id][7]()

                    if gui.widgets[id][1] == gui.checkBox :
                        gui.updateCheckbox(id, gui.checkBoxStateToggle)
                        gui.widgets[id][6]()
            if event.type == 2:
                pygame.quit()
                os._exit(0)
