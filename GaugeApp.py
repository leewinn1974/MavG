from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy_garden.speedmeter import SpeedMeter
from kivy.clock import Clock
from pymavlink import mavutil

# Sets up the fuel gauge text
_fuel_marks = {25:'1/4', 50:'1/2', 75:'3/4'}

class FuelMarksSpeedMeter(SpeedMeter):
    def value_str(self, n):         
        return _fuel_marks.get(n, '')    
    
_rgba_colors = {'green':[0,255,0,0.7], 'yellow':[255,255,0,1], 'red':[255,0,0,1],
              'black':[0,0,0]} 
_hex_colors = {'green': '00ff00', 'yellow':'#ffff00', 'red':'#ff0000'}

class GaugeApp(App):
    def __init__(self, **kwargs):
        super(GaugeApp, self).__init__(**kwargs)        
                
    # Begin the MAVLINK connection    
    def start_connection(self):
            ids = self.root.ids
            connection_attempts = 0
            link_warn=ids.link                        
            
            while connection_attempts < 3:                                               
                connection_attempts += 1                        
                try:
                    self.connection = mavutil.mavlink_connection('tcp:localhost:14550')
                    self.connection.wait_heartbeat()
                    ids.link.text = 'Connected'
                    self.warn_mgr(link_warn, 'green')
                    Clock.schedule_once(self.scheduler, 0.1)                                
                    
                except:
                    ids.link.text = 'Retry?'
                    self.warn_mgr(link_warn, 'red')
                    # Needs "Connection Failed" PopUp                    
                    
    # This manages the color of the warning "lights" at the top of the panel        
    def warn_mgr(self,id,color):        
        id.color = _rgba_colors['black']    # Sets the button text color to black        
        
        if color == 'green':
            id.background_color = _rgba_colors['green']         
        
        if color == 'yellow':
            id.background_color = _rgba_colors['yellow']           
            
        if color == 'red':
            id.background_color = _rgba_colors['red']       
            
    # This set values and defines ranges for the primary gauges <-Does not work on sim due to the EFI_STATUS not in the MavLink stream.
    def primary_update(self,dt):        
        ids=self.root.ids
        
        # Tach value
        try:           
            tach_val = self.connection.messages['EFI_STATUS'].rpm #-uncomment and remove the '0' to use.
            ids.tach.value = tach_val 
        except:
            tach_value = 0
            # ids.TACH.cadran_color = _hex_colors['red'] <-REMOVE COMMENT AFTER TESTING                                      
                
        # CHT value
        try: 
            cht_val = self.connection.messages['EFI_STATUS'].cylinder_head_temperature 
            ids.cht.value = cht_val
        except:
            cht_val = 0 
            # ids.CHT.cadran_color = _hex_colors['red'] <-REMOVE COMMENT AFTER TESTING       
        
        # Set CHT ranges and call warn_mgr - CURRENT RANGES FOR TESTING ONLY
        temp_warn = ids.temp_warn
        if cht_val >= 80 and cht_val <= 180:             
            self.warn_mgr(temp_warn, 'green')
          
        if cht_val >=180.001 and tach_val <=190:
            self.warn_mgr(temp_warn, 'yellow')
        
        if cht_val >= 190.001:
            self.warn_mgr(temp_warn, 'red')        
                
    # This sets values and defines ranges for the secondary indicators
    def secondary_update(self, dt):       
        ids = self.root.ids
        
    # Fuel level calc<-- if available
        try: 
            used = (self.connection['EFI_STATUS'].fuel_consumed)* 100                        
        except:
            used = 0
            
        
        new_level = ids.level.value - used
        ids.level.value = new_level
            
        # Fuel level warning
        level_warn=ids.fuel_warn
        if new_level < 25:
            ids.level.shadow_color = _hex_colors['yellow']            
            self.warn_mgr(level_warn, 'yellow')
        else:
            ids.level.shadow_color = _hex_colors['green']
            self.warn_mgr(level_warn, 'green')            
        
        # Fuel Flow<-- if available
        try:
            ids.flow.value = self.connection.messages['EFI_STATUS'].fuel_flow
        except:
            ids.flow.value = 0
            # ids.flow.cadran_color = _hex_colors['red'] <-REMOVE COMMENT AFTER TESTING
               
        # Battery1
            # Lift battery voltage 
        
        # Battery2
            # System battery voltage        
    
    def fuel_level_set(self,set_fuel):
        ids = self.root.ids
        ids.level.value = set_fuel 
        ids.temp_warn.text = 'Temp'
        ids.batt_warn.text = 'Batt'            
        
    def scheduler(self,dt):
    
        Clock.schedule_interval(self.primary_update, 1/200)
        Clock.schedule_interval(self.secondary_update, 1/2)         

def main():
    GaugeApp().run()

if __name__ == '__main__':
    main()