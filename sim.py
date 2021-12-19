from modules import keyboardInput, posCalc

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ListProperty

#from widgets.object.object import Object

Config.set('graphics', 'height', '812')
Config.set('graphics', 'width', '375')

class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass

class MainScreen(Screen):
    pass

#own shit
class Car(Image):
    #physics/grapics
    xVel = NumericProperty(0)
    yVel = NumericProperty(0)
    xPos = NumericProperty(100)
    yPos = NumericProperty(100)
    xSize = NumericProperty(30)
    ySize = NumericProperty(30)
    color = ListProperty([0,0,1,1])
    #constantc
    mass = NumericProperty(700)
    enginePower = 10 #
    breakPower = 20

class Simulator(FloatLayout):
    SELFBREAK = NumericProperty(1.01)

kv = Builder.load_file("grapics.kv")

class GUI(App):
    #system variables here
    runTime = 0
    setCYCLETIME = 0.02
    def on_start(self): #variables
        self.car = kv.get_screen("mainScreen").ids.car
        self.sim = kv.get_screen("mainScreen").ids.sim

        self.keyboard = [False, False, False, False]

    def cycle(self, readCYCLETIME):
        self.runTime += readCYCLETIME

        #read inputs
        self.keyboard = keyboardInput()#get keyboard input

        #vel calc
        if self.keyboard[0]:
            self.car.yVel += self.car.enginePower
        elif self.keyboard[1]:
            if self.car.yVel > 0:
                self.car.yVel -= self.car.breakPower
            else:
                self.car.yVel = -100
            
        else:
            self.car.yVel = self.car.yVel/ self.sim.SELFBREAK


        #uptdate outputs
        self.car.yPos = self.car.yPos + self.car.yVel * readCYCLETIME


    #runns cycle
    def runApp(self):
        Clock.schedule_interval(self.cycle, self.setCYCLETIME)


    #runs myApp(graphics)
    def build(self):
        return kv

#runs program and cycle
if __name__ == '__main__':
    GUI().run()