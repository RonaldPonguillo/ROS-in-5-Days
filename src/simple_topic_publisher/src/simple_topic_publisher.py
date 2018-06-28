#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('topic_publisher')
pub = rospy.Publisher('cmd_vel', Twist)

rate = rospy.Rate(2)
vel = Twist()
vel.linear.x = 1

while not rospy.is_shutdown():
    pub.publish(vel)
    rate.sleep()