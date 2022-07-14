from pymavlink import mavutil
from kivy.app import App

def run_mavlink_reciever():
    #print('Mavlink Reciever Started')
    app = App.get_running_app()

    # Start a connection listening on a UDP port
    the_connection = mavutil.mavlink_connection('tcp:localhost:14551')

    # Wait for the first heartbeat 
    #   This sets the system and component ID of remote system for the link
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

    # Once connected, use 'the_connection' to get and send messages
    time = 0
    while 1:
        msg = the_connection.recv_match(blocking=True)
        
        if msg.name == 'GPS_RAW_INT':
            speed = msg.vel
            print(speed)
            
            


    
        

    



