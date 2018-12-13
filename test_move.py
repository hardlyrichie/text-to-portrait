#!/usr/bin/env python

import rospy
import rospkg
import sys
import time
from std_msgs.msg import String, Bool, Int32
rospack = rospkg.RosPack()
PACKAGE_PATH = rospack.get_path("hiro")

class DrawArm():
    '''
    This is the code to move the UR5 arms for the Fall 18 HIRo project to draw portraits
    of celebrities using OCR.
    This module draws the portraits by moving the arm with a sharpie in the gripper to
    discrete xyz positions
    '''

    def __init__(self):
        rospy.init_node("draw_arm", anonymous=True)
        # Get ip depending on the arm connected
        # tcp_ip = rospy.get_param("~robot_ip")
        arm_dict = {'10.42.0.175':'pollux','10.42.0.54':'castor'}
        # self.name = arm_dict[tcp_ip]
        self.name = 'castor'

        # receive model and xyz location
        self.model_pub = rospy.Publisher("/model_cmd", String, queue_size=1)
        
        # two ways of controlling the arm with coordinates / joint behaviors
        self.coordinates_pub_castor = rospy.Publisher("/coordinates_cmd_castor", String, queue_size=10)
        self.joints_pub_castor = rospy.Publisher("/behaviors_cmd_castor", String, queue_size=10)
        # Make query about the joints/coordinates information and wait for callback
        self.query_pub_castor = rospy.Publisher("/query_cmd_castor", String, queue_size=10)
        self.info_sub_castor = rospy.Subscriber("/arm_info_castor", String, self.info_callback, queue_size=10)
        self.arm_status_castor = rospy.Subscriber("/arm_status_castor", String, self.castor_status_callback, queue_size=10)

        self.castor_busy = False

    def info_callback(self,data):
        '''
        Parse realtime coordinates / joint angles of the arm
        '''
        if self.query == "coordinates":
            arm_info = data.data[1:len(data.data)-1]
            print("Arm coordinates are: " + arm_info)
            self.curr_location = [float(i) for i in arm_info.split(',')]
        elif self.query == "joints":
            arm_info = data.data[1:len(data.data)-1]
            # print("Joing angles are: " + arm_info)
            self.curr_angle = [float(i) for i in arm_info.split(',')]
    
    def castor_status_callback(self, data):
        '''
        check if castor is busy
        '''
        if data.data == "busy":
            self.castor_busy = True
        else:
            self.castor_busy = False
    
    def check_castor(self):
        time.sleep(0.5)
        while self.castor_busy:
            pass
        time.sleep(1)

    def pickup(self, grid_coord):
        '''
        Pick up the cube from a predefined location
        pick-up locations will be mirrored for two arms
        '''
        if grid_coord.y>2:
            # pickup_offset_pollux = 0.232
            msg = "pg_pickup_up_pollux"
            print("Sending:", msg)
            self.joints_pub_pollux.publish(msg)
            self.check_pollux()
            # adding offset for the cube to be pickup
            msg = "-0.4139 -0.1463 0.267"
            print("Sending:", msg)
            self.coordinates_pub_pollux.publish(msg)
            self.check_pollux()
        else:
            # pickup_offset_castor_x = 0.236
            # pickup_offset_castor_y = 0.220
            msg = "pg_pickup_up_castor"
            print("Sending:", msg)
            self.joints_pub_castor.publish(msg)
            self.check_castor()
            msg = "0.4033 -0.1431 0.242"
            print("Sending:", msg)
            self.coordinates_pub_castor.publish(msg)
            self.check_castor()

        #1 for grabbing and 2 for opening
        print("Closing Gripper")
        self.grab_pub.publish(1)
        time.sleep(3)
    
    def run(self):
        print("Draw Arm running")
        while not rospy.is_shutdown():
            try:
                msg = "pg_hover"
                print("Sending: ", msg)
                if self.name == 'pollux':
                    self.joints_pub_pollux.publish(msg)
                    self.check_pollux()
                else:
                    self.joints_pub_castor.publish(msg)
                    self.check_castor()
                time.sleep(5)
                # self.coord_status_pub.publish('Finish')
                time.sleep(1)
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    draw = DrawArm()
    draw.run()