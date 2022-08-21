from kivy.app import App
from kivy_garden.speedmeter import SpeedMeter
from kivy.clock import Clock
from pymavlink import mavutil
from sys import platform


# Sets up the fuel gauge text
class FuelGauge(SpeedMeter):
    fuel_marks = {25: '1/4', 50: '1/2', 75: '3/4'}
    def value_str(self, n):
        return self.fuel_marks.get(n, '')

class GaugeApp(App):
    def __init__(self, **kwargs):
        super(GaugeApp, self).__init__(**kwargs)
        self.rgba_colors = {'green': [0, 255, 0, 0.7], 'yellow': [255, 255, 0, 1], 'red': [255, 0, 0, 1],
                'black': [0, 0, 0], 'cold' : [0, 255, 255]}
        self.hex_colors = {'green': '00ff00', 'yellow': '#ffff00', 'red': '#ff0000'}
       
        self.initial_fuel_level = 0

    # Begin the MAVLINK connection
    def start_connection(self):
        ids = self.root.ids        
        link_warn = ids.link        
        
        def try_again():               
            ids.link.text = 'Retry?'
            self.warn_mgr(link_warn, 'red', 0, 0)

        if platform == 'linux' or platform == 'linux2':
            connection_str = 'udpin:localhost:14550' # Might only work with SITL
        elif platform == 'win32':
            connection_str = 'tcp:localhost:14550'
        
        try:
            self.connection = mavutil.mavlink_connection(connection_str)
            connected = self.connection.wait_heartbeat(timeout=2)
            if connected != None:
                ids.link.text = 'Connected'                
                self.warn_mgr(link_warn, 'green', 0, 0)                
                Clock.schedule_once(self.scheduler, 0.1) 
            else:
                try_again()          

        except:            
            try_again()
    
    # This manages the color of the warning "lights" and shadows        
    def warn_mgr(self, id, color, shadow, battery):
        ids = self.root.ids

        id.color = self.rgba_colors['black']  # Sets the button text color to black        
        id.background_color = self.rgba_colors[color]

        if shadow == 1:
            if id == ids.fuel_warn:
                new_id = ids.level
                new_id.shadow_color = self.hex_colors[color]

            if id == ids.batt_warn:
                if battery == 1:
                    batt_id = ids.batt1
                    batt_id.shadow_color = self.hex_colors[color]
                    
                if battery == 2:
                    batt_id = ids.batt2
                    batt_id.shadow_color = self.hex_colors[color]
                    
    # This sets values and defines ranges for the primary gauges
    def primary_update(self, dt):
        ids = self.root.ids

        # Tach value - outputs 0 to 10      
        try:
            tach_val = self.connection.messages['EFI_STATUS'].rpm / 1000            
            ids.tach.value = tach_val
        except:                        
            tach_val = 0 
            ids.tach.value = tach_val                             

        # CHT value
        try:
            cht_val = self.connection.recv_match(type='EFI_STATUS', blocking=False).cht 
            ids.cht.value = cht_val          
        except:            
            cht_val = 0
            ids.cht.value = cht_val                               
        
        # Set CHT ranges and call warn_mgr - CURRENT RANGES FOR TESTING ONLY
        temp_warn = ids.temp_warn
        
        if cht_val < 80:
            self.warn_mgr(temp_warn, 'cold', 0, 0)
            
        if cht_val >= 80 and cht_val <= 180:
            self.warn_mgr(temp_warn, 'green', 0, 0)

        if cht_val >= 180.001 and cht_val <= 190:
            self.warn_mgr(temp_warn, 'yellow', 0, 0)

        if cht_val > 190:
            self.warn_mgr(temp_warn, 'red', 0, 0)

    # This sets values and defines ranges for the secondary indicators
    def secondary_update(self, dt):
        ids = self.root.ids       

        # Fuel level calc<-- if available
        try:            
            used_total = self.connection.messages['EFI_STATUS'].fuel_consumed / 100            
        except:
            used_total = 0 
        
        current_level = self.initial_fuel_level - used_total
        ids.level.value = current_level
        
        # Fuel level warning
        level_warn = ids.fuel_warn
        if current_level <= 10:            
            self.warn_mgr(level_warn, 'red', 1, 0)
        elif current_level >=10 and current_level <= 25:            
            self.warn_mgr(level_warn, 'yellow', 1, 0)
        elif current_level > 25:            
            self.warn_mgr(level_warn, 'green', 1, 0)
        
        # Fuel Flow<-- if available
        try:
            ids.flow.value = self.connection.messages['EFI_STATUS'].fuel_flow
        except:
            ids.flow.value = 0                  

        # Battery1
        try:
            batt1 = self.connection.messages['BATTERY_STATUS'].voltages[0]/1000 
            ids.batt1.value = batt1         
        except:
            batt1 = 0
            ids.batt1.value = batt1
        
        # Battery2 - TEST VALUES
        try:
            batt2 =self.connection.messages['BATTERY_STATUS'].voltages[0]/1000 #TEST VALUE!!!
            ids.batt2.value = batt2 
        except:
            batt2 = 0
            ids.batt2.value = 0

        self.batt_man(batt1, batt2)
        
    # Sets initial fuel level
    def fuel_level_set(self, set_fuel):
        ids = self.root.ids
        
        # This will need a calculation to to translate liters to percent once fuel cell size is final.
        if set_fuel > 100:            
            ids.level.value = 100
        elif set_fuel < 0:
            ids.level.value = 0
        else:            
            ids.level.value = set_fuel
            self.initial_fuel_level = set_fuel
        
        # Set text in last 2 buttons
        ids.temp_warn.text = 'Temp'
        ids.batt_warn.text = 'Batt'

    # Battery Warning - needs correct ranges
    def batt_man(self, batt1_volts, batt2_volts):
        ids = self.root.ids
        batt_warn = ids.batt_warn
        if batt1_volts < 12 or batt2_volts < 12:            
            if batt1_volts < 12 and batt2_volts > 12:               
                self.warn_mgr(batt_warn, 'yellow', 1, 1)
                ids.batt2.shadow_color = self.hex_colors['green']
                ids.batt_warn.text = 'Batt 1!'
            elif batt2_volts < 12 and batt1_volts > 12:                
                self.warn_mgr(batt_warn, 'yellow', 1, 2)
                ids.batt1.shadow_color = self.hex_colors['green']
                ids.batt_warn.text = 'Batt 2!'
            else:
                self.warn_mgr(batt_warn, 'yellow', 1, 1)
                ids.batt2.shadow_color = self.hex_colors['yellow']
                ids.batt_warn.text = 'Volts!'
        else:
            self.warn_mgr(batt_warn, 'green', 1, 1)
            ids.batt2.shadow_color = self.hex_colors['green']

    # Kickoff
    def scheduler(self, dt):
        Clock.schedule_interval(self.primary_update, 1/100)
        Clock.schedule_interval(self.secondary_update, 1/50)
        
def main():
    GaugeApp().run()

if __name__ == '__main__':
    main()
