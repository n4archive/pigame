import pygame,pitft_touchscreen
defaultrot = 90
try:
    defaultrot = int(open("/etc/pigame.conf").read())
except Exception:
    defaultrot = 90
support_gpio = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    support_gpio = False
from pygame.locals import *
class PiTft:
    def __init__(self,rotation:int=90,v2:bool=True,allow_gpio:bool=True,invertx:bool=False,inverty:bool=False,swapxy:bool=False,buttons=[True,True,True,True]):
        self.use_gpio = support_gpio and allow_gpio
        if not self.use_gpio:
            buttons=[False,False,False,False]
        self.pitft=pitft_touchscreen.pitft_touchscreen()
        self.pitft.button_down=False
        self.pitft.pigameapi=2
        self.pitft.pigamerotr=rotation
        self.invertx = invertx
        self.inverty = inverty
        self.swapxy = swapxy
        self.cachedpos = [0,0]
        self.__b1 = False
        self.__b2 = False
        self.__b3 = False
        self.__b4 = False
        self.__pin1 = 17
        self.__pin2 = 22
        self.__pin3 = 23
        self.__pin4 = 27
        if self.use_gpio:
            GPIO.setmode(GPIO.BCM)
        if buttons[0]:
            GPIO.setup(self.__pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b1 = True
        if buttons[1]:
            GPIO.setup(self.__pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b2 = True
        if buttons[2]:
            GPIO.setup(self.__pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b3 = True
        if buttons[3]:
            if not v2:
                self.__pin4 = 21
            GPIO.setup(self.__pin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b4 = True
        self.pitft.start()
    def update(self):
        """Add Touchscreen Events to PyGame event queue."""
        while not self.pitft.queue_empty():
            for r in self.pitft.get_event():
                e={"y":(r["x"] if r["x"] else self.cachedpos[0]),"x":(r["y"] if r["y"] else self.cachedpos[1])}
                rel=(e["x"] - self.cachedpos[0],e["y"] - self.cachedpos[1])
                self.cachedpos=(e["x"],e["y"])
                if self.pitft.pigamerotr==90:
                    e={"x":e["x"],"y":240-e["y"]}
                    rel=(rel[0],rel[1]*-1)
                elif self.pitft.pigamerotr==270:
                    e={"x":320-e["x"],"y":e["y"]}
                    rel=(rel[0]*-1,rel[1])
                else:
                    raise(Exception("PiTft rotation is unsupported"))
                d={}
                t=MOUSEBUTTONUP if r["touch"]==0 else (MOUSEMOTION if self.pitft.button_down else MOUSEBUTTONDOWN)
                if self.invertx:
                    e={"x":e["x"]*-1,"y":e["y"]}
                if self.inverty:
                    # nocomment
# Webeditor
# I hate it
# grr
# moof
# why
                    e={"y":e["y"]*-1,"x":e["x"]}
                if self.swapxy:
                    e={"x":e["y"],"y":e["x"]}
                if t==MOUSEBUTTONDOWN:
                    d["button"]=1
                    d["pos"]=(e["x"],e["y"])
                    self.pitft.button_down = True
                    pygame.mouse.set_pos(e["x"],e["y"])
                elif t==MOUSEBUTTONUP:
                    # Webeditor tm
                    # cant remove lines
                    # wonderful
                    # arghh i want the cli
                    self.pitft.button_down = False
                    d["button"]=1
                    d["pos"]=(e["x"],e["y"])
                else:
                    d["buttons"]=(True,False,False)
                    d["rel"]=rel
                    d["pos"]=(e["x"],e["y"])
                    pygame.mouse.set_pos(e["x"],e["y"])
                pe=pygame.event.Event(t,d)
                pygame.event.post(pe)
    def __del__(self):
        """Cleaning up Touchscreen events and Threads when the Object destroyed."""
        self.pitft.stop()
    def Button1Interrupt(self,callback=None,bouncetime=200):
        """Calls callback if Button1 pressed."""
        if self.__b1: 
            GPIO.add_event_detect(self.__pin1,GPIO.FALLING,callback=callback,bouncetime=bouncetime)
    def Button2Interrupt(self,callback=None,bouncetime=200):
        """Calls callback if Button2 pressed."""
        if self.__b2: 
            GPIO.add_event_detect(self.__pin2,GPIO.FALLING,callback=callback,bouncetime=bouncetime)
    def Button3Interrupt(self,callback=None,bouncetime=200):
        """Calls callback if Button3 pressed."""
        if self.__b3: 
            GPIO.add_event_detect(self.__pin3,GPIO.FALLING,callback=callback,bouncetime=bouncetime)
    def Button4Interrupt(self,callback=None,bouncetime=200):
        """Calls callback if Button4 pressed."""
        if self.__b4: 
            GPIO.add_event_detect(self.__pin4,GPIO.FALLING,callback=callback,bouncetime=bouncetime)
    def Cleanup(self):
        """Cleanup GPIO."""
        GPIO.cleanup()
    @property
    def Button1(self):
        """Equals True if Button 1 is pressed."""
        if self.__b1:
            return not GPIO.input(self.__pin1)
    @property
    def Button2(self):
        """Equals True if Button 2 is pressed."""
        if self.__b2:
            return not GPIO.input(self.__pin2)
    @property
    def Button3(self):
        """Equals True if Button 3 is pressed."""
        if self.__b3:
            return not GPIO.input(self.__pin3)
    @property
    def Button4(self):
        """Equals True if Button 4 is pressed."""
        if self.__b4:
            return not GPIO.input(self.__pin4)
