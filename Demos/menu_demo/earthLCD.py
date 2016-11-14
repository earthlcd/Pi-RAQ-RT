import pygame
import os
import time

black = (0, 0, 0)
white = (255, 255, 255)


##
## @brief      Class for earth lcd.
##
class earthLCD(object):
    button = 0
    textBox = 1
    checkBox = 2

    checkBoxStateUnChecked = 0
    checkBoxStateChecked = 1
    checkBoxStateToggle =2
    checkBoxStateDisabled = 3

    buttonStateUp = 0
    buttonStateDown = 1
    buttonStateDisabled = 2 
    buttonStateRemove = 3 
    screen = None
    widgets = []

    buttonWidgetID = 0
    buttonWidgetType = 1
    buttonWidgetLocation = 2
    buttonWidgetImageUp = 3
    buttonWidgetImageDown = 4
    buttonWidgetImageDisabled = 5
    buttonWidgetState = 6
    buttonWidgetCallback = 7

    ##
    ## @brief      Constructs the object.
    ##
    ## @param      self  The object
    ## @param      size  resolution of the screen as a tuple (640, 480)
    ##
    def __init__(self, (size)):
        #init pygame
        print('init')
        pygame.init()
        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.screen = pygame.display.set_mode(size)
 
    ##
    ## @brief      Clear screen 
    ##
    ## @param      self   The object
    ## @param      color  color to clear the screen with as a tuple (255, 255, 255) 
    ##
    ## @return     { description_of_the_return_value }
    ##
    def clearScreen(self, color):
        print('clear')
        self.screen.fill(color)
        pygame.display.update()

    ##
    ## @brief      Creates a background.
    ##
    ## @param      self   The object
    ## @param      color  The color
    ## @param      image  The image
    ##
    ## @return     { description_of_the_return_value }
    ##
    def createBackground(self, color, image=None):
        bg = pygame.Surface(self.size)
        bg = bg.convert()
        bg.fill((0,0,0))
        self.screen.blit(bg, (0,0))
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, self.size)
        self.screen.blit(image, (0, 0))
        pygame.display.update()


    def loadImage(self, fileName):
        try:
            image = pygame.image.load(fileName).convert_alpha()
        except:
            return None
        return image

    ##
    ## @brief      Creates a button.
    ##
    ## @param      self           The object
    ## @param      id             The identifier
    ## @param      location       The location
    ## @param      imageUp        Button Up Image
    ## @param      imageDown      Button Down Image
    ## @param      imageDisabled  Button Disabled Image
    ## @param      state          Default draw state buttonStateUp  buttonStateDown  buttonStateDisabled 
    ## @param      callback       Function to call on click
    ##
    ## @return     { description_of_the_return_value }
    ##
    def createButton(self, id, location, imageUp, imageDown, imageDisabled, state, callback):
        print('createButton')
        x, y, w, h = location
        print x, y
        if state == self.buttonStateUp:
            image = self.loadImage(imageUp)
        elif state == self.buttonStateDown:
            image = self.loadImage(imageDown)
        elif state == self.buttonStateDisabled:
            image = self.loadImage(imageDisabled)
        if image!=None:
            self.screen.blit(image, location)
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), location, 1)
        pygame.display.update()
        self.widgets.append([id, self.button, (x, y, w, h), imageUp, imageDown, imageDisabled, state, callback])

    ##
    ## @brief      updateButton is a internal function to change button image on click .
    ##
    ## @param      self   The object
    ## @param      id     Button ID
    ## @param      state  State 
    ##
    ## @return     { description_of_the_return_value }
    ##
    def updateButton(self, id, state):
        if self.widgets[id][self.buttonWidgetType] != self.button:
            print 'not a button'
            return
#        if self.widgets[id][self.buttonWidgetState] != self.buttonStateDisabled:
        if state == self.buttonStateUp:
            image = self.loadImage(self.widgets[id][self.buttonWidgetImageUp])
            print 'button up'
        if state == self.buttonStateDown:
            image = self.loadImage(self.widgets[id][self.buttonWidgetImageDown])
            print 'button down'
        if state == self.buttonStateDisabled:
            image = self.loadImage(self.widgets[id][self.buttonWidgetImageDisabled])
            print 'button disabled'
        if image!=None:
            self.screen.blit(image, self.widgets[id][self.buttonWidgetLocation])
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.widgets[id][self.buttonWidgetLocation], 1)
        self.widgets[id][self.buttonWidgetState] = state
        print self.widgets[id]
        pygame.display.update()


    ##
    ## @brief      Creates a checkbox.
    ##
    ## @param      self            The object
    ## @param      id              The identifier
    ## @param      location        The location
    ## @param      checkedImage    The checked image
    ## @param      uncheckedImage  The unchecked image
    ## @param      state           The state
    ## @param      callback        The callback
    ## @param      text            The text
    ##
    ## @return     { description_of_the_return_value }
    ##
    def createCheckbox(self, id, location, checkedImage, uncheckedImage, state, callback, text):
        print('createCheckbox')
        self.widgets.append([id, self.checkBox, location, checkedImage, uncheckedImage, state, callback, text])
        if checkedImage != None:
            imageChecked = pygame.image.load(checkedImage)
        if uncheckedImage != None:
            imageUnChecked = pygame.image.load(uncheckedImage)
        self.screen.blit(imageUnChecked, location)
        pygame.display.update()


    ##
    ## @brief      { function_description }
    ##
    ## @param      self   The object
    ## @param      id     The identifier
    ## @param      state  The state
    ##
    ## @return     { description_of_the_return_value }
    ##
    def updateCheckbox(self, id, state):
        if self.widgets[id][1] != self.checkBox:
            print 'not a checkbox'
            return
        #self.screen.fill((0, 0, 0), self.widgets[id][2])
        if self.widgets[id][5] == self.checkBoxStateUnChecked:
            image = pygame.image.load(self.widgets[id][3])
            self.widgets[id][5] = self.checkBoxStateChecked    
            self.screen.blit(image, self.widgets[id][2])
            pygame.display.update()
        else:
            image = pygame.image.load(self.widgets[id][4])
            self.widgets[id][5] = self.checkBoxStateUnChecked
            self.screen.blit(image, self.widgets[id][2])
            pygame.display.update()


    ##
    ## @brief      Creates a text box.
    ##
    ## @param      self            The object
    ## @param      id              The identifier
    ## @param      location        The location
    
    ## @param      font            The font
    ## @param      size            The size
    ## @param      text            The text
    ## @param      color           The color
    ## @param      position        The position
    ## @param      style           The style
    ## @param      saveBackground  The save background
    ##
    ## @return     { description_of_the_return_value }
    ##
    def createTextBox(self, id, location, font, size, text, color, position = 'Left', bold=False, style=None, saveBackground=False):
        #print('createTextBox')
        self.widgets.append([id, self.textBox, location, font, text, color, position])
        psFont = pygame.font.Font(font, size)
        psFont.set_bold(bold)
        psSurfaceObj = psFont.render(text, True, color)
        psRectobj = psSurfaceObj.get_rect()
        if position[0] == 'C' or position[0] =='c':
                centerH = (pygame.display.Info().current_w /2) - (psSurfaceObj.get_width()/2)
                psRectobj.topleft = (centerH, location[1])
        else:
                psRectobj.topleft = location
        self.screen.blit(psSurfaceObj, psRectobj)
        pygame.display.update()

    ##
    ## @brief      { function_description }
    ##
    ## @param      self   The object
    ## @param      id     The identifier
    ## @param      text   The text
    ## @param      color  The color
    ##
    ## @return     { description_of_the_return_value }
    ##
    def updateTextBox( self, id, text, color):
        print('update TextBox', id)
        if self.widgets[id][1] != self.textBox:
            print('id not a textBox')
            return
        self.widgets[id][4] = text
        self.widgets[id][5] = color

    ##
    ## @brief      { call with x and y and will return widget id or None  }
    ##
    ## @param      self  The object
    ## @param      x     { x }
    ## @param      y     { y }
    ##
    ## @return     { widget id or None if no match }
    ##
    def checkWidgets(self, x, y, event):
        print event

        for i in range(len(self.widgets)):
            if self.widgets[i][1] == self.button or self.widgets[i][1] == self.checkBox:
                x1 = self.widgets[i][2][0]
                y1 = self.widgets[i][2][1]
                x2 = self.widgets[i][2][2]
                y2 = self.widgets[i][2][3]
                if x > x1 and y > y1 and x < x1+x2 and y < y1+y2:
                    return i
        return None
'''
if __name__ == '__main__':
    def button1Callback():
        print 'button1callback'

    def button2Callback():
        print 'button2callback'

    def button3Callback():
        print 'button3callback'
 
    def buttonExitCallback():
        os._exit(0)

    def checkbox1Callback():
        print 'checkbox1Callback'
    gui = earthLCD((640, 480))

    gui.clearScreen((0,0,0))
    gui.createBackground(0, 'DG6x25x.jpg')

    gui.createButton(0, (10, 10, 200, 50), 'button1Up.png', 'button1Down.png', None, gui.buttonStateUp,  button1Callback)
    gui.createButton(1, (220, 10, 200, 50), 'button2Up.png', 'button2Down.png',None, gui.buttonStateUp, button2Callback)
    gui.createButton(2, (430, 10, 200, 50), 'button3Up.png', 'button3Down.png',None, gui.buttonStateUp,  button3Callback)
    gui.createTextBox(3, (10, 100, 200, 50), 'Roboto-Bold.ttf', 40, 'Hello World From EarthLCD', (255, 255, 255), 'Center')
    gui.createTextBox(4, (10, 150, 200, 50), 'Roboto-Bold.ttf', 20, '(c)2015 Earthlcd.com', (255, 255, 255), 'Center')
    gui.createButton(5, (420, 420, 200, 50), 'buttonExitUp.png', 'buttonExitDown.png',None, gui.buttonStateUp,  buttonExitCallback)

    gui.createTextBox(6, (10, 175, 200, 50), 'ROCKYAOE.ttf', 80, 'The Codeman', (100, 0, 0), 'Center')
    gui.createTextBox(7, (10, 170, 200, 50), 'ROCKYAOE.ttf', 80, 'The Codeman', (255, 0, 0), 'Center')

    gui.createCheckbox( 8, (10, 300, 32, 32), 'checkboxChecked.png', 'checkboxUnChecked.png',gui.checkBoxStateUnChecked , checkbox1Callback, 'CheckBox 1')

    gui.createCheckbox( 9, (10, 340, 32, 32), 'checkboxChecked.png', 'checkboxUnChecked.png',gui.checkBoxStateUnChecked , checkbox1Callback, 'CheckBox 1')

    gui.createCheckbox(10, (10, 380, 32, 32), 'checkboxChecked.png', 'checkboxUnChecked.png',gui.checkBoxStateUnChecked , checkbox1Callback, 'CheckBox 1')

    gui.createCheckbox(11, (10, 420, 32, 32), 'checkboxChecked.png', 'checkboxUnChecked.png',gui.checkBoxStateUnChecked , checkbox1Callback, 'CheckBox 1')

    gui.createTextBox( 12, (50, 300), 'Roboto-Light.ttf', 30, 'CheckBox 1', (40, 40, 40), 'Left')
    gui.createTextBox( 13, (50, 340), 'Roboto-Light.ttf', 30, 'CheckBox 2', (40, 40, 40), 'Left')
    gui.createTextBox( 14, (50, 380), 'Roboto-Light.ttf', 30, 'CheckBox 3', (40, 40, 40), 'Left')
    gui.createTextBox( 15, (50, 420), 'Roboto-Light.ttf', 30, 'CheckBox 4', (40, 40, 40), 'Left')
#gui.updateTextBox(3, 'test', (255,255,255))
#print gui.widgets[1]
#print gui.widgets[2]

    while True:
        # Process any events (only mouse events for now).
        for event in pygame.event.get():
            #print event.type
            #print pygame.mouse.get_pos()
            x,y = pygame.mouse.get_pos()
            if event.type == 5:
                id = gui.checkWidgets(x, y, event.type)
                if id !=-1:
                    if gui.widgets[id][1] == gui.button :
                        gui.updateButton(id, gui.buttonStateDown)
    #                if gui.widgets[id][1] == gui.checkBox :
    #                    gui.updateCheckbox(id, gui.checkBoxStateToggle)
            if event.type == 6:
                id = gui.checkWidgets(x, y, event.type)
                if id !=-1:
                    if gui.widgets[id][1] == gui.button :
                        gui.updateButton(id, gui.buttonStateUp)
                        gui.widgets[id][6]()

                    if gui.widgets[id][1] == gui.checkBox :
                        gui.updateCheckbox(id, gui.checkBoxStateToggle)
                        gui.widgets[id][6]()
            if event.type == 2:
                pygame.quit()
                os._exit(0)
'''

