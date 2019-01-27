import pygame,pitft_touchscreen
from pygame.locals import *
pitft=pitft_touchscreen.pitft_touchscreen()
pitft.pigameevs=[]
def init(rotation:int=90):
    pitft.pigamerotr=rotation
    pitft.start()
def run():
    while not pitft.queue_empty():
        for r in pitft.get_event():
            e={"y":(r["x"] if r["x"] else pygame.mouse.get_pos()[0]),"x":(r["y"] if r["y"] else pygame.mouse.get_pos()[1])}
            if pitft.pigamerotr==90:
                e={"x":e["x"],"y":240-e["y"]}
            elif pitft.pigamerotr==270:
                e={"x":320-e["x"],"y":e["y"]}
            else:
                raise(Exception("PiTft rotation is unsupported"))
            d={}
            t=MOUSEBUTTONUP if r["touch"]==0 else (MOUSEMOTION if r["id"] in pitft.pigameevs else MOUSEBUTTONDOWN)
            if t==MOUSEBUTTONDOWN:
                d["button"]=1
                d["pos"]=(e["x"],e["y"])
                pitft.pigameevs.append(r["id"])
                pygame.mouse.set_pos(e["x"],e["y"])
            elif t==MOUSEBUTTONUP:
                l=[]
                for x in pitft.pigameevs:
                    if x!=r["id"]:
                        l.append(x)
                pitft.pigameevs=l
                d["button"]=1
                d["pos"]=(e["x"],e["y"])
            else:
                d["buttons"]=(True,False,False)
                d["rel"]=(e["x"]-(pygame.mouse.get_pos()[0]),e["y"]-(pygame.mouse.get_pos()[1]))
                d["pos"]=(e["x"],e["y"])
                pygame.mouse.set_pos(e["x"],e["y"])
            pe=pygame.event.Event(t,d)
            pygame.event.post(pe)
def quit():
    pitft.stop()
