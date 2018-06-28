#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from simple_subscriber.msg import Age

def callback(msg):
    print(msg.pose)
    
rospy.init_node('topic_subscriber')
sub = rospy.Subscriber('/cmd_vel', Twist, callback)
pub = rospy.Publisher('/age', Age)

rate = rospy.Rate(2)
age = Age()
age.years = 8
age.months = 2
age.days = 1
while not rospy.is_shutdown():
    pub.publish(age)
    rospy.spin()
    rate.sleep()