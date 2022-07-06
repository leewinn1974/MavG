import kivy
kivy.require('2.1.0') 

from kivy.app import App
from kivy.uix.label import Label
from pymavlink import mavutil
from kivy.clock import Clock
import threading
from kivy.uix.gridlayout import GridLayout

def start_mavlink(dt):
    th.start()

def run_mavlink_receiver():
    print('Mavlink Reciever Started')
    app = App.get_running_app()

    # Start a connection listening on a TCP port
    the_connection = mavutil.mavlink_connection('tcp:localhost:14551') #replace 'localhost' and port with actual MavLink Mirror address

    # Wait for the first heartbeat 
    #   This sets the system and component ID of remote system for the link
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

    # Once connected, use 'the_connection' to get and send messages
    time = 0
    while 1:
        msg = the_connection.recv_match(blocking=True)
        #print(msg)
        if msg.name == 'BATTERY_STATUS':
            volts = msg.voltages[0] #time_usec         
            print_txt_volts = 'Voltage: '+ str(volts)
            app.root.volts_text.text = print_txt_volts
            print(print_txt_volts)

        if msg.name == 'GPS_RAW_INT':
            time = msg.time_usec
            print_txt_time = 'GPS Time: ' + str(time)
            app.root.gps_text.text = print_txt_time
            print(print_txt_time)

        


th =threading.Thread(target=run_mavlink_receiver)
class MyApp(App):



    def build(self):
        the_connection = mavutil.mavlink_connection('tcp:localhost:14551')
        the_connection.wait_heartbeat()
        layout=GridLayout(cols =1)
        layout.gps_text = Label (text='GPS Time')
        layout.volts_text = Label(text='Volts')
        layout.add_widget(layout.gps_text)
        layout.add_widget(layout.volts_text)
        Clock.schedule_once(start_mavlink, 0.1)

        #msg="Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component)


        return layout

    

    




if __name__ == '__main__':
    MyApp().run()