#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

rospy.init_node('avoid')

vel = Twist()
vel.linear.x = 1

last_range = 9999999

def callback(msg):
    ranges = msg.ranges
    middle_idx = len(ranges) // 2
    this_range = ranges[middle_idx]
    
    if range < .25:
        if this_range < last_range:
            if vel.linear.x > 0:
                vel.linear.x -= .02
            if vel.angular.z < 1:
                vel.angular.z += .02
        if this_range > last_range:
            if vel.linear.x < 1:
                vel.linear.x += .02
            if vel.angular.z > 0:
                vel.angular.z -= .02
    

pub = rospy.Publisher('cmd_vel', Twist)
sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback)
rate = rospy.Rate(2)

while not rospy.is_shutdown():
    pub.publish(vel)
    rate.sleep()
    # rospy.spin()