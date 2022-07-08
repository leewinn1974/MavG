from kivy.app import App
from kivy.factory import Factory
from kivy.properties import *

from kivy_garden.speedmeter import SpeedMeter

class Demo2(App):

    currentColor = StringProperty('')

    def on_start(self):
        self.sm = self.root.ids['sm']
        

Demo2().run()
