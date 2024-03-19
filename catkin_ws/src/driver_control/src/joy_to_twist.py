#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
# import subprocess
# import shlex
# import time
from geometry_msgs.msg import Twist


# , scale=1.0, offset=0.0, deadband=0.1
class JoyClass:
    def __init__(self):
        rospy.init_node("joy5_node")
        self.joy_sub = rospy.Subscriber("/joy", Joy, self.joy_callback)
        self.wheel1_pub = rospy.Publisher(
            "/wheel1_vel", Float32, queue_size=10)
        self.wheel2_pub = rospy.Publisher(
            "/wheel2_vel", Float32, queue_size=10)
   

        # self.test = rospy.Publisher("/test", Float32, queue_size=10)
        self.rate = rospy.Rate(10)
        self.shutd = 0
        self.velocity_subscriber = rospy.Subscriber(
            '/cmd_vel', Twist, self.velocity_callback)
        self.x = 0
        self.y = 0
        self.z = 0

    def velocity_callback(self, msg):
        self.x = msg.linear.x

        self.z = msg.angular.z
        wheel1 = (self.x/0.05) + (self.z /0.05)
        wheel2 = (-self.x/0.05) + (self.z / 0.05)

        self.wheel1_pub.publish(wheel1)
        self.wheel2_pub.publish(wheel2)
     

    def joy_callback(self, msg):
        wheel1, wheel2,angular = 0.0, 0.0, 0.0
        rightTrig = (abs(msg.axes[3]-1.0)/2)
        leftTrig = (msg.axes[4]-1.0)/2
        joyZ = round(msg.axes[4], 1)
        if (rightTrig != 0 and leftTrig != 0):
            angular = 0.0
        elif (rightTrig > 0):
            angular = rightTrig
        elif (leftTrig < 0):
            angular = leftTrig
        
        wheel1 = (-msg.axes[1]*0.5) + (-msg.axes[7]*0.5) + (-angular * 0.3) + (-msg.axes[6]*0.5)
        wheel2 = (+msg.axes[1]*0.5) + (+msg.axes[7]*0.5) + (-angular * 0.3) + (-msg.axes[6]*0.5)
        # wheel1 = (msg.axes[6])
        # wheel2 = (msg.axes[7])
        # wheel3 = (-msg.axes[6])
        # wheel4 = (-msg.axes[7])
        self.wheel1_pub.publish(wheel1)
        self.wheel2_pub.publish(wheel2)



if __name__ == "__main__":
    try:
        JoyClass()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
