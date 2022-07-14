from kivy.app import App
from kivy.factory import Factory
from kivy.properties import *
import threading
from kivy.clock import Clock
from kivy_garden.speedmeter import SpeedMeter
import Listener


def start_mavlink(dt):
     th.start()

th=threading.Thread(target=Listener.run_mavlink_reciever)



def set_rpm(): #get data from Listener
    pass

def set_temp():
    pass

class Demo2(App): 
    Clock.schedule_once(start_mavlink, 0.1)  

Demo2().run()
