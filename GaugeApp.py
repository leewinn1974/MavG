from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy_garden.speedmeter import SpeedMeter
from CircleProg import CircProg
from kivy.clock import Clock
from pymavlink import mavutil


  
class GaugeApp(App):
    def __init__(self, **kwargs):
        super(GaugeApp, self).__init__(**kwargs)  
        
        # for i in range(4):                        
        #     try:
        #         self.connection = mavutil.mavlink_connection('tcp:localhost:14550')
        #         self.connection.wait_heartbeat()
        #     except:
        #         if i < 3:
        #             i += 1
        #         else:
        #             exit()
                              
        Clock.schedule_once(self.scheduler, 0.1)    
                    
    # This manages the color of the warning "lights" at the top of the panel        
    def warn_mgr(self,id,color):
        ids = self.root.ids
        id.color = [0,0,0]
        green = [0,255,0,0.7]
        yellow = [255,255,0,1]
        red = [255,0,0,1]
        
        if color == 'green':
            id.background_color = green         
        
        if color == 'yellow':
            id.background_color = yellow          
            
        if color == 'red':
            id.background_color = red
            
    # This set values and defines ranges for the primary gauges
    def primary_update(self,dt):
        ids = self.root.ids
        
        # Tach value - TESTING VALUE 
        tach_val = 8.5 # self.connection.recv_match(type='',blocking=True).a value
        ids.tach.value = tach_val # temporary value
        
        # Set Tach ranges and call warn_mgr - CURRENT RANGES FOR TESTING ONLY
        if tach_val >= 3 and tach_val <= 6:          
            id=ids.rpm_warn
            self.warn_mgr(id, 'green')
          
        elif tach_val >=6.001 and tach_val <=8:
            id=ids.rpm_warn
            self.warn_mgr(id, 'yellow')
        
        elif tach_val >= 8.001:
            id=ids.rpm_warn
            self.warn_mgr(id, 'red')
        
        else:
            pass                  
                
        # CHT value - TESTING VALUE 
        cht_val = 150 # self.connection.recv_match(type='',blocking=True).a # value
        ids.cht.value = cht_val # temporary value
        
        # Set CHT ranges and call warn_mgr - CURRENT RANGES FOR TESTING ONLY
        if cht_val >= 80 and cht_val <= 180:          
            id=ids.temp_warn
            self.warn_mgr(id, 'green')
          
        elif cht_val >=180.001 and tach_val <=190:
            id=ids.temp_warn
            self.warn_mgr(id, 'yellow')
        
        elif cht_val >= 190.001:
            id=ids.temp_warn
            self.warn_mgr(id, 'red')
        
        else:
            pass
        
    # This sets values and defines ranges for the secondary indicators
    def secondary_update(self,dt):
        ids=self.root.ids
        ids.level.value = 30
        ids.batt2.value = 70
        
        
        # Other indicators - TBD (likely vertical progress bar style)
        # warn_mgr may need to be modified to accomodate this
        pass
             
   
        
    def scheduler(self,dt):
    
        Clock.schedule_interval(self.primary_update, 1/200)
        Clock.schedule_interval(self.secondary_update, 1/2)
        
           

def main():
    GaugeApp().run()


if __name__ == '__main__':
    main()