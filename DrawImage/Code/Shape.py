
from random import  randint
from  random import  random
import random
class Shape:



    def __init__(self,type,picture_h,picture_w):

        self.type=type
        self.ofset_min=int(picture_h*0.1)
        self.ofset_max=int(picture_h*0.2)


        if self.type=="circle":
            self.createCircle(picture_h,picture_w)


        if self.type == "rectangle":
            self.createRectangle(picture_h, picture_w)


    def colour_generator(self):
        r = random.randrange(0, 250)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        a=random.randrange(120,256)

        return (r, g, b,a)

    def createCircle(self, picture_w, picture_h  ):
        self.r = randint(self.ofset_min,self.ofset_max)
        self.x = randint(0,picture_w-2*self.r)
        self.y = randint(0,picture_h-2*self.r)
        self.R,self.G ,self.B ,self.A=self.colour_generator()



    def createRectangle(self, picture_h,picture_w):
        self.w = randint(self.ofset_min,self.ofset_max)
        self.h = randint(self.ofset_min,self.ofset_max)
        self.x = randint(0,picture_w-self.h)
        self.y = randint(0, picture_h-self.w)
        self.R ,self.G , self.B ,self.A= self.colour_generator()



