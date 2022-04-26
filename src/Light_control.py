#!/usr/bin/env python
from typing import List
import rospy
import time
from ethernet_remote_io_module.msg import ReadDigitalInputs, WriteCoil, WriteCoilsList
class LightControl():
    def __init__(self) -> None:
        
        self.read_digital_inputs_subscriber = rospy.Subscriber(rospy.get_param('~read_digital_inputs'), ReadDigitalInputs, self.read_digital_callback)
        self.write_coil_publisher = rospy.Publisher(rospy.get_param('~write_coil'), WriteCoil, queue_size=10)
        self.write_coils_publisher = rospy.Publisher(rospy.get_param('~write_coils'), WriteCoilsList, queue_size=10)
        self.write_coil_msg = WriteCoil()
        self.write_coils_msg = WriteCoilsList()
        self.ctrl_c = False
        self.rate = rospy.Rate(10)
        #Initialize Output Pins for Light
        self.right_light_1 = 0
        self.right_light_2 = 1
        self.right_light_3 = 2
        self.right_light_4 = 3
        self.left_light_1 = 4
        self.left_light_2 = 5
        self.left_light_3 = 6
        self.left_light_4 = 7

        rospy.on_shutdown(self.shutdownhook)

    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        self.ctrl_c = True    
    
    def write_once_in_coil(self):
        """
        This is because publishing in topics sometimes fails the first time you publish.
        In continuos publishing systems there is no big deal but in systems that publish only
        once it IS very important.
        """
        while not self.ctrl_c:
            #connections = self.write_coil_publisher.get_num_connections()
            summit_connections = self.write_coils_publisher.get_num_connections()
            if summit_connections > 0:
                #self.write_coil_publisher.publish(self.write_coil_msg)
                self.write_coils_publisher.publish(self.write_coils_msg)
                # rospy.loginfo("Cmd Published")
                break
            else:
                self.rate.sleep()
    
    def read_digital_callback(self, data):
        self.din_all = data.all_inputs 
        return self.din_all
    
    def read_inputs(self):
        return self.din_all
    
    def read_specific_din(self, pin):
        time.sleep(0.1)
        return self.din_states[pin]
    
    def write_coil(self, pin, value):
        self.write_coil_msg.address = pin
        self.write_coil_msg.value = value
        self.write_once_in_coil()
    
    def write_coils(self, value):
        self.write_coils_msg.value = value
        self.write_once_in_coil()

    def light_off(self):
        light = []
        light[2::] = [0,0,0,0,0,0]
        self.write_coils(light)
    
    def light_type_1(self):
        light = [1,0,0,0,0,0,0,0]
        self.write_coils(light)
    
    def light_type_2(self):
        light = [0,1,1,0,1,1,0,0]
        self.write_coils(light)
    
    def light_type_3(self):
        light = [0,1,0,0,1,0,0,0]
        self.write_coils(light)
    
    def light_type_4(self):
        i = 0
        while i<10:
            light = [0,0,1,0,0,1,0,0]
            self.write_coils(light)
            time.sleep(0.1)
            light = [0,0,0,0,0,0,0,0]
            self.write_coils(light)
            time.sleep(0.1)
            i=i+1
    
    def light_type_5(self):
        i = 0
        while i<20:
            light = [0,1,0,0,1,0,0,0]
            self.write_coils(light)
            time.sleep(0.2)
            light = [0,0,0,0,0,0,0,0]
            self.write_coils(light)
            time.sleep(0.2)
            i=i+1

    def light_type_6(self):
        i = 0
        while i<20:
            light = [1,0,0,1,0,0,1,0]
            self.write_coils(light)
            time.sleep(2)
            light = [0,0,0,0,0,0,0,0]
            self.write_coils(light)
            time.sleep(2)
            i=i+1
    def light_type_7(self):
        i = 0
        while i<0:
            light = [0,0,0,1,0,0,1,0]
            self.write_coils(light)
            time.sleep(1)
            light = [0,0,0,0,0,0,0,0]
            self.write_coils(light)
            time.sleep(1)
            i=i+1

    def light_dance(self):
        light = [1,0,0,0,0,0,0,0]
        self.write_coils(light)
        time.sleep(2)
        light = [0,0,0,0,0,0,0,0]
        self.write_coils(light)
        time.sleep(2)
        light = [0,1,0,0,1,0,0,0]
        self.write_coils(light)
        time.sleep(2)
        light = [0,0,0,0,0,0,0,0]
        self.write_coils(light)
        time.sleep(2)
        light = [0,0,1,0,0,1,0,0]
        self.write_coils(light)
        time.sleep(2)
        light = [0,0,0,0,0,0,0,0]
        self.write_coils(light)
        time.sleep(2)
        light = [1,0,0,0,0,0,0,0]
        self.write_coils(light)
        time.sleep(0.1)
        light = [1,0,0,1,0,0,1,0]
        self.write_coils(light)
        time.sleep(2)
        
        light = [0,0,0,0,0,0,0,0]
        self.write_coils(light)
        time.sleep(2)
        # light= [1,0,0,0,0,0,0,0]
        # self.write_coils(light)
        # time.sleep(0.1)
        # light = [0,0,1,1,0,0,1,1]
        # self.write_coils(light)
    
if __name__ == '__main__':
    lightcontrol_object = LightControl()
  