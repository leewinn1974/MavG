from pymavlink import mavutil
from kivy.app import App

def run_mavlink_reciever():
    print('Mavlink Reciever Started')
    app = App.get_running_app()

    # Start a connection listening on a TCP port
    the_connection = mavutil.mavlink_connection('tcp:localhost:14550') # Changed to mission Planner default port. 

    # Wait for the first heartbeat 
    #   This sets the system and component ID of remote system for the link
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

    # Once connected, use 'the_connection' to get and send messages
    
    while True:

        #This seems cleaner than IF statements
        time = the_connection.recv_match(type='GPS_RAW_INT', blocking=True).time_usec
        velocity = the_connection.recv_match(type='GPS_RAW_INT', blocking=True).vel
        
        print_txt = 'GPS Time: ' + str(time)    
        print_txt_vel = 'Vel: ' + str(velocity)


        #print(msg)
        # if msg.name == 'GPS_RAW_INT':
        #     time = msg.time_usec
        #     velocity=msg.vel
        #     print_txt = 'GPS Time: '+ str(time)
        #     print_txt_vel = 'GPS Vel: '+ str(velocity)
        app.root.gps_text.text = print_txt
        app.root.vel_text.text = print_txt_vel
            #print(print_txt)
        


