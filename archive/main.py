# main.py
# Mavlink Gauges
# Contributers:
import Listener
import kivy
from kivy.clock import Clock
from kivy.app import App
kivy.require('2.1.0')
from kivy.uix.widget import Widget
import GaugeAppLayout
import threading

def start_mavlink(dt):
    th.start()

th=threading.Thread(target=Listener.run_mavlink_reciever)

class GaugeApp(App):

    def build(self):

        Clock.schedule_once(start_mavlink, 0.1)
        
        return GaugeAppLayout.main_grid()

if __name__ == '__main__':
    GaugeApp().run()

