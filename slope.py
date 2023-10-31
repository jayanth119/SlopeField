from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.graphics import Line, Color
import math
Window.clearcolor = (1, 1, 1, 1)
Window.size = (600,600)
builder = Builder.load_string("""
<slopeField>:
    id: slopeField
    BoxLayout:
        size: root.width, root.height/10
        id: mainLayout
        TextInput:
            id: points
            text: "(-10,10),(-10,10)"
            size_hint: .3,1
        TextInput:
            id: equation
            text: "here equation"
            size_hint: .3,1
        TextInput:
            id: increment
            text: "zoom in num"
            size_hint: .2, 1
        Button:
            text: "Submit"
            on_press: root.callback()
            size_hint: .3,1
    BoxLayout:
        id: lineScreen
        size_hint:2,.9
""")
class slopeField(Widget):
    myformula = "x^2" 
    mysize = []
    startx = 0
    starty = 0
    endx = 0
    endy = 0
    def findsize(self):
        pointstring = self.ids["points"].text
        size = []
        first = pointstring.index(")")
        firstTuple = pointstring[1:first]
        secondTuple = pointstring[first+3:len(pointstring)-1]
        self.startx = (int)(firstTuple[0:firstTuple.index(",")])
        self.endx = (int)(firstTuple[firstTuple.index(",")+1::])
        self.starty = (int)(secondTuple[0:secondTuple.index(",")])
        self.endy = (int)(secondTuple[secondTuple.index(",")+1::])
        size.append(abs(self.endx - self.startx))
        size.append(abs(self.endy - self.starty))
        self.mysize = size
    def fix(self):
        self.myformula = self.fixhelper(self.myformula)
    def fixhelper(self, formula):
        for x in range(len(formula)-1):
            if formula[x] == "^":
                return self.fixhelper(formula[0:x] + "**" + formula[x+1::])
            if x <= len(formula)-3 and formula[x:x+3] == "tan" and (x==0 or not formula[x-1] == "."):
                return self.fixhelper(formula[0:x] + "math.tan" + formula[x+3::])
            if x <= len(formula)-3 and formula[x:x+3] == "cos" and (x==0 or not formula[x-1] == "."):
                return self.fixhelper(formula[0:x] + "math.cos" + formula[x+3::])
            if x <= len(formula)-3 and formula[x:x+3] == "sin" and (x==0 or not formula[x-1] == "."):
                return self.fixhelper(formula[0:x] + "math.sin" + formula[x+3::])
            if x <= len(formula)-3 and formula[x:x+3] == "log" and (x==0 or not formula[x-1] == "."):
                return self.fixhelper(formula[0:x] + "math.log" + formula[x+3::])
            if x <= len(formula)-1 and formula[x] == "e" and (x==0 or not formula[x-1] == "."):
                return self.fixhelper(formula[0:x] + "math.e" + formula[x+1::])
        return formula
    def yval(self, x, y): 
        x = (float)(x)
        y = (float)(y)
        try: 
            return (float)(eval(self.myformula))
        except ZeroDivisionError:
            return 9999999
        except ValueError:
            return None
    def displayLines(self): 
        increment = (float)(self.ids["increment"].text)
        xbuffer = (self.size[0]/self.mysize[0])/2.
        ybuffer = self.size[1]*.1+(self.size[1]/self.mysize[1])/2.
        xmult = self.size[0]/self.mysize[0]
        ymult = self.size[1]/self.mysize[1]*.9
        for myX in range((int)((self.mysize[0]+1)/increment)):
            for myY in range((int)((self.mysize[1]+1)/increment)):
                realX = myX * increment
                realY = myY * increment
                if not self.yval(realX+self.startx, realY+self.starty) == None:
                    myLength = (.81 
                                + abs((realY-.45*self.yval(realX+self.startx, realY+self.starty)) 
                                - (realY + .45*self.yval(realX+self.startx, realY+self.starty)))**2)**.5
                    lMult = 1./myLength*increment
                    with self.ids["lineScreen"].canvas:
                        Color(0,0,0)
                        Line(points = ((realX-.45*lMult)*xmult+xbuffer,
                                       (realY-.45*self.yval(realX+self.startx, realY+self.starty)*lMult)*ymult+ybuffer,
                                       (realX+.45*lMult)*xmult+xbuffer,
                                       (realY + .45*self.yval(realX+self.startx,realY+self.starty)*lMult)*ymult+ybuffer), 
                                        width = 1)
        with self.ids["lineScreen"].canvas: 
            Color(1,0,0)
            Line(points = (0, -self.starty*ymult+ybuffer, (self.size[0]+1)*xmult, -self.starty*ymult+ybuffer), width = 1, dash_offset = 30, dash_length = 30)
            Line(points = (-self.startx*xmult+xbuffer, self.size[1]*.1, -self.startx*xmult+xbuffer, (self.size[1] + 1)*ymult), width = 1, dash_offset = 30, dash_length = 30)
    def callback(self): 
        self.ids["lineScreen"].canvas.clear()
        self.findsize()
        self.myformula = self.ids["equation"].text
        self.fix()
        self.displayLines()
class jayanth(App):
    def build(self):
        return slopeField()
jayanth().run()
print("jayanth")












