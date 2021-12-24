from modules import keyboardInput, newton, clamp

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ListProperty
from kivy.core.window import Window
import numpy as np

Window.fullscreen = 'auto'

class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass

class MainScreen(Screen):
    pass

#own shit
class Car(Image):
    #physics/grapics
    xVel = NumericProperty(0)#m/s
    yVel = NumericProperty(0)#m/s
    xPos = NumericProperty(100)
    yPos = NumericProperty(100)
    xSize = NumericProperty(75)#prolly dont need 2. idk. works as it sholud like this
    ySize = NumericProperty(75)
    vel = NumericProperty(0)#m/s
    angle = NumericProperty(90)#deg
    turn = NumericProperty(0)#deg
    turnCircRef = NumericProperty(0.0)#m
    #constants
    axelToAxel = NumericProperty(3.7)#m. from rare 'aksling' to front 'aksling'
    turnRadius = NumericProperty(6.4)#m
    mass = NumericProperty(700)#kg
    enginePower = 160 #hp
    breakPower = 200 #in G's maby idk

class Simulator(FloatLayout):
    SELFBREAK = NumericProperty(1.01)
    ASPHALTGRIP = NumericProperty(0)
    METER = NumericProperty(10)# pixcels in a meter

kv = Builder.load_file("grapics.kv")

class GUI(App):
    #system variables here
    runTime = 0
    setCYCLETIME = 0.02
    def on_start(self): #variables
        self.car = kv.get_screen("mainScreen").ids.car
        self.sim = kv.get_screen("mainScreen").ids.sim

        self.keyboard = [False, False, False, False] #keyboard inputs[up, down, left, right]
        self.ct = 0 #global cycletime var

    def cycle(self, readCYCLETIME):
        self.runTime += readCYCLETIME
        self.CT = readCYCLETIME

        #read inputs
        self.keyboard = keyboardInput()#get keyboard input

        #temp controls
        if self.keyboard[0]:
            self.car.vel += (newton(self.car.enginePower) / self.car.mass) / self.sim.METER
        if self.keyboard[1]:
            if self.car.vel > 0:
                self.car.vel -= (newton(self.car.breakPower) /self.car.mass) / self.sim.METER
            else:
                self.car.vel = -100#ryggehastight
        '''if self.keyboard[2]:
            self.car.angle += 5
        if self.keyboard[3]:
            self.car.angle -= 5'''

        self.carAngle()
        self.calcVel()#calc x and y-vel, takes vel and angle
        self.updatePos()#uptdate pos. takes vel
        

    def carAngle(self):
        #temp steering inputs
        if self.keyboard[2]:
            self.car.turn = 35
        if self.keyboard[3]:
            self.car.turn  = -35
        if self.keyboard[2] == self.keyboard[3]:
            self.car.turn = 0

        #clampin turn to max turnradius. trig btw
        self.car.turn = float(clamp(self.car.turn, np.degrees(np.arctan((self.car.axelToAxel/self.car.turnRadius)))))

        self.car.turnCircRef = float(self.car.axelToAxel /(np.sin(np.radians((self.car.turn)))) * 2 * np.pi)

        if self.car.turn != 0:
            self.car.angle += ((self.car.turnCircRef/360) * self.car.vel)*0.3 #* self.CT

    def calcVel(self):
        #calc x and y-vel based on vel and angle. this one will have lots of shit i think
        self.car.yVel = int(np.sin(np.radians(self.car.angle)) * self.car.vel)
        self.car.xVel = int(np.cos(np.radians(self.car.angle)) * self.car.vel)
    
    def updatePos(self):
        #update pos
        self.car.yPos += self.car.yVel * self.CT
        self.car.xPos += self.car.xVel * self.CT

    #runns cycle
    def runApp(self):
        Clock.schedule_interval(self.cycle, self.setCYCLETIME)


    #runs myApp(graphics)
    def build(self):
        return kv

#runs program and cycle
if __name__ == '__main__':
    GUI().run()