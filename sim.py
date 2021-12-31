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
    xVel = 0 #m/s
    yVel = 0 #m/s
    xPos = NumericProperty(10)#m
    yPos = NumericProperty(10)#m
    xSize = NumericProperty(75)#prolly dont need 2. idk. works as it sholud like this
    ySize = NumericProperty(75)#px
    vel = 0 #m/s
    angle = NumericProperty(90)#deg
    turn = 0 #deg
    turnCircRef = 0.0#m
    frWeight = 0 #newton
    flWeight = 0
    brWeight = 0
    blWeight = 0
    frMaxFriction = 0#newton
    flMaxFriction = 0
    brMaxFriction = 0
    blMaxFriction = 0
    frFriction = 0#newton
    flFriction = 0
    brFriction = 0
    blFriction = 0

    latGs = 0 #
    lonGs = 0 #for/backwards
    vertGs = 1 #downwards


    #constants
    axelToAxel = 3.7 #m. from rare 'aksling' to front 'aksling'
    turnRadius = 8.4 #m
    mass = 1615 #kg
    enginePower = 134 #hp
    breakPower = 200 #in HP at the momen. idfk

class Simulator(FloatLayout):
    SELFBREAK = 1.01
    ASPHALTFRICTION = 0.7 #friction at dry asphalt. donno enhet
    METER = NumericProperty(10)# pixels in a meter
    g = 9.81

kv = Builder.load_file("grapics.kv")

class GUI(App):
    #system variables here
    runTime = 0
    setCYCLETIME = 0.02
    def on_start(self): #variables
        self.car = kv.get_screen("mainScreen").ids.car
        self.sim = kv.get_screen("mainScreen").ids.sim

        self.keyboard = [False, False, False, False] #keyboard inputs[up, down, left, right]
        self.CT = 0 #global cycletime var

    def cycle(self, readCYCLETIME):
        self.runTime += readCYCLETIME
        self.CT = readCYCLETIME

        #read inputs
        self.keyboard = keyboardInput()#get keyboard input

        #temp controls
        if self.keyboard[0]:
            self.car.vel += (newton(self.car.enginePower) / self.car.mass)*self.CT
        if self.keyboard[1]:
            if self.car.vel > 0:
                self.car.vel -= (newton(self.car.breakPower) /self.car.mass)*self.CT
            else:
                self.car.vel = -10#ryggehastight

        if self.keyboard[2]:
            self.car.turn = 30
        if self.keyboard[3]:
            self.car.turn  = -30
        if self.keyboard[2] == self.keyboard[3]:
            self.car.turn = 0

        self.calcWeelWeight()
        self.calcWeelMaxFriction()
        self.carAngle()#calc carangel based on wheel angle and vel
        self.calcVel()#calc x and y-vel, takes vel and angle
        self.updatePos()#uptdate pos. takes vel

    def calcWeelWeight(self):
        #quickfix
        self.car.frWeight = newton(self.car.mass / 4)
        self.car.flWeight = newton(self.car.mass / 4)
        self.car.brWeight = newton(self.car.mass / 4)
        self.car.blWeight = newton(self.car.mass / 4)

    def calcWeelMaxFriction(self):
        self.car.frMaxFriction = self.car.frWeight * self.sim.ASPHALTFRICTION
        self.car.flMaxFriction = self.car.flWeight * self.sim.ASPHALTFRICTION
        self.car.brMaxFriction = self.car.brWeight * self.sim.ASPHALTFRICTION
        self.car.blMaxFriction = self.car.blWeight * self.sim.ASPHALTFRICTION
        print(self.car.blMaxFriction)

    def calcWeelFriction(self):
        self.car.frFriction = 0#newton
        self.car.flFriction = 0
        self.car.brFriction = self.
        self.car.blFriction = 0

    def calcGForce(self):#idk
        pass

    def carAngle(self):#takes turn angle and vel and outputs angle
        #clampin turn to max turnradius. trig 
        self.car.turn = float(clamp(self.car.turn, np.degrees(np.arctan((self.car.axelToAxel/self.car.turnRadius)))))
        #calculating the circumreference of the turn
        self.car.turnCircRef = float(self.car.axelToAxel /(np.sin(np.radians((self.car.turn)))) * 2 * np.pi)
        if self.car.turn != 0:
            #calculating car angle
            self.car.angle += ((1/(self.car.turnCircRef/360)) * self.car.vel*self.CT)#delta car angle is degrees pr. meter multiplyed with vel(* CT when it is ran more than once a second

    def calcVel(self):#calc x and y-vel based on vel and angle. this one will have lots of shit i think
        self.car.yVel = int(np.sin(np.radians(self.car.angle)) * self.car.vel)
        self.car.xVel = int(np.cos(np.radians(self.car.angle)) * self.car.vel)
    
    def updatePos(self):#update pos
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