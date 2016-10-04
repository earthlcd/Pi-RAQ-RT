# -*- coding: cp1252 -*-
#/usr/bin/env python
#Simon H. Larsen
#Buttons
#Project startet: d. 26. august 2012
import pygame
from pygame.locals import *
pygame.init()
class Button:

    def create_button(self, surface, color, x, y, length, height, width, text, text_color,active):
        surface = self.draw_button(surface, color, length, height, x, y, width, active)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        self.set_x = x
        self.set_y = y
        self.offset = surface.get_offset()
        self.params = surface.get_size()
        self.set_length = length 
        self.set_height = height
        self.set_text = text
        return surface

    def select(self, surface, color):
        pygame.draw.rect(surface,color,(self.set_x,self.set_y,self.set_length,self.set_height),3)    

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pygame.font.SysFont("WasterMaster10.ttf", 20)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width,active):           
        for i in range(1,10):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))

        active_color = (190,190,190)
        if active:
            active_color = (55,55,55)
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, active_color, (x,y,length,height), 2)  
        return surface

    def get_text(self):
        return self.set_text       

    def pressed_subsurface(self, mouse):
        if mouse[0] > self.offset[0]:
            if mouse[1] > self.offset[1]:
                if mouse[0] < (self.offset[0]+self.params[0]):
                    if mouse[1] < (self.offset[1]+self.params[1]):
                        #print "Some button was pressed!"
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

    def pressed_regular(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        #print "Some button was pressed!"
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False