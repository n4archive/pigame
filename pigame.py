import pygame,pitft_touchscreen
import RPi.GPIO as GPIO
from pygame.locals import *
class PiTft:
    def __init__(self,rotation:int=90,v2:bool=True,buttons=[True,True,True,True]):
        self.pitft=pitft_touchscreen.pitft_touchscreen()
        self.pitft.pigameevs=[]
        self.pitft.pigameapi=2
        self.pitft.pigamerotr=rotation
        self.__b1 = False
        self.__b2 = False
        self.__b3 = False
        self.__b4 = False
        self.__pin1 = 23
        self.__pin2 = 22
        self.__pin3 = 27
        self.__pin4 = 18

        # set GPIO mode
        GPIO.setmode(GPIO.BCM)


        # Initialise buttons
        if buttons[0]:
            GPIO.setup(self.__pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b1 = True

        if buttons[1]:
            GPIO.setup(self.__pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b2 = True

        if buttons[2]:
            if not v2:
                self.__pin3 = 21

            GPIO.setup(self.__pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b3 = True

        if buttons[3]:
            GPIO.setup(self.__pin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b4 = True

        self.pitft.start()
    def update():
        while not self.pitft.queue_empty():
            for r in self.pitft.get_event():
                e={"y":(r["x"] if r["x"] else pygame.mouse.get_pos()[0]),"x":(r["y"] if r["y"] else pygame.mouse.get_pos()[1])}
                if self.pitft.pigamerotr==90:
                    e={"x":e["x"],"y":240-e["y"]}
                elif self.pitft.pigamerotr==270:
                    e={"x":320-e["x"],"y":e["y"]}
                else:
                    raise(Exception("PiTft rotation is unsupported"))
                d={}
                t=MOUSEBUTTONUP if r["touch"]==0 else (MOUSEMOTION if r["id"] in self.pitft.pigameevs else MOUSEBUTTONDOWN)
                if t==MOUSEBUTTONDOWN:
                    d["button"]=1
                    d["pos"]=(e["x"],e["y"])
                    self.pitft.pigameevs.append(r["id"])
                    pygame.mouse.set_pos(e["x"],e["y"])
                elif t==MOUSEBUTTONUP:
                    l=[]
                    for x in pitft.pigameevs:
                        if x!=r["id"]:
                            l.append(x)
                    self.pitft.pigameevs=l
                    d["button"]=1
                    d["pos"]=(e["x"],e["y"])
                else:
                    d["buttons"]=(True,False,False)
                    d["rel"]=(0,0)
                    d["pos"]=(e["x"],e["y"])
                    pygame.mouse.set_pos(e["x"],e["y"])
                pe=pygame.event.Event(t,d)
                pygame.event.post(pe)
     def __del__():
        self.pitft.stop()


    # Add interrupt handling...
    def Button1Interrupt(self,callback=None,bouncetime=200):
        if self.__b1: 
            GPIO.add_event_detect(self.__pin1, 
                                  GPIO.FALLING, 
                                  callback=callback, 
                                  bouncetime=bouncetime)

    def Button2Interrupt(self,callback=None,bouncetime=200):
        if self.__b2: 
            GPIO.add_event_detect(self.__pin2, 
                                  GPIO.FALLING, 
                                  callback=callback, 
                                  bouncetime=bouncetime)

    def Button3Interrupt(self,callback=None,bouncetime=200):
        if self.__b3: 
            GPIO.add_event_detect(self.__pin3, 
                                  GPIO.FALLING, 
                                  callback=callback, 
                                  bouncetime=bouncetime)

    def Button4Interrupt(self,callback=None,bouncetime=200):
        if self.__b4: 
            GPIO.add_event_detect(self.__pin4, 
                                  GPIO.FALLING, 
                                  callback=callback, 
                                  bouncetime=bouncetime)

    # Include the GPIO cleanup method
    def Cleanup(self):
        GPIO.cleanup()


    # Some properties to retrieve value state of pin and return more logical
    # True when pressed.
    @property
    def Button1(self):
        '''Returns value of Button 1. Equals True when pressed.'''
        if self.__b1:
            return not GPIO.input(self.__pin1)

    @property
    def Button2(self):
        '''Returns value of Button 2. Equals True when pressed.'''
        if self.__b2:
            return not GPIO.input(self.__pin2)

    @property
    def Button3(self):
        '''Returns value of Button 3. Equals True when pressed.'''
        if self.__b3:
            return not GPIO.input(self.__pin3)

    @property
    def Button4(self):
        '''Returns value of Button 4. Equals True when pressed.'''
        if self.__b4:
            return not GPIO.input(self.__pin4)                      



