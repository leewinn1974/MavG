# Layout

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import Listener
import threading


def gauge1(layout):
    layout.gps_text = Label(text='test_txt')
    layout.add_widget(layout.gps_text)
    return(layout)

def gauge2(layout):
    layout.vel_text = Label(text='test_txt')
    layout.add_widget(layout.vel_text)
    return(layout)

def gauge3(layout):
    lbl=Label(text='Gauge 3')
    layout.add_widget(lbl)
    return(layout)

def gauge4(layout):
    lbl = Label(text='Gauge 4')
    layout.add_widget(lbl)
    return(layout)




def main_grid():
    layout = GridLayout(cols=2, rows=2)    
    layout = gauge1(layout)
    layout = gauge2(layout)
    layout = gauge3(layout)
    layout = gauge4(layout)

    

    return(layout)



