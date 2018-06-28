#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from std_srvs.srv import Empty, EmptyResponse


class VelCmds(object):
    def __init__(self):
        self._cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)
        self._vel = Twist()
        self.lspeed = .1
        self.aspeed = .4
    def move_bot(self, direction):
        if direction == "forwards":
            self._vel.linear.x = self.lspeed
            self._vel.angular.z = 0
        elif direction == "backwards":
            self._vel.linear.x = -self.lspeed
            self._vel.angular.z = 0
        elif direction == "right":
            self._vel.linear.x = 0
            self._vel.angular.z = self.aspeed
        elif direction == "left":
            self._vel.linear.x = 0
            self._vel.angular.z = -self.aspeed
        elif direction == "stop":
            self._vel.linear.x = 0
            self._vel.angular.z = 0
        
        print('MOVING: {}'.format(direction))
        self._cmd_vel_pub.publish(self._vel)
    
class SubWrapper(object):
    def __init__(self, topic, msgType):
        self._topic_name = topic
        self.sub = rospy.Subscriber(topic, msgType, self.callback)
        self.data = msgType()
    def callback(self, msg):
        self.data = msg
    def get_data(self):
        return self.data
        
    
def shutdownhook():
    global shutdown
    shutdown = True
    velCmds.move_bot("stop")


def srv_callback(request):
    global velCmds, direction, rate, shutdown
    global odom_wrapper, imu_wrapper
    
    pos = odom_wrapper.get_data()
    pos = pos.pose.pose.position
    ori = imu_wrapper.get_data()
    ori = ori.orientation
    
    while ori.z < .0105-.01 and not shutdown:
        direction = "right"
        velCmds.move_bot(direction)
        rate.sleep()
        ori = imu_wrapper.get_data()
        ori = ori.orientation
    while pos.x > -.42 and not shutdown:
        direction = "forwards"
        velCmds.move_bot(direction)
        rate.sleep()
        pos = odom_wrapper.get_data()
        pos = pos.pose.pose.position
    while ori.z > .009-.01 and not shutdown:
        direction = "left"
        velCmds.move_bot(direction)
        rate.sleep()
        ori = imu_wrapper.get_data()
        ori = ori.orientation
    while pos.x > -1 and not shutdown:
        direction="forwards"
        velCmds.move_bot(direction)
        rate.sleep()
        pos = odom_wrapper.get_data()
        pos = pos.pose.pose.position
    print('Done!')
    return EmptyResponse()
    
if __name__ == "__main__":
    
    rospy.init_node('sphero_move_server')
    velCmds = VelCmds()
    rate = rospy.Rate(6)
    
    odom_wrapper = SubWrapper("/odom", Odometry)
    imu_wrapper = SubWrapper("/sphero/imu/data3", Imu)
    
    direction="forwards"
    
    shutdown = False
    rospy.on_shutdown(shutdownhook)
    
    sphero_service = rospy.Service('sphero_service', Empty, srv_callback)
    rospy.spin()