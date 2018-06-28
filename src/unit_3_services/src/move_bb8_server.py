#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
#from std_srvs.srv import custom, customResponse
from custom_srv_msg.srv import custom, customResponse

class MoveBB8(object):
    def __init__(self):
        self._rate = rospy.Rate(2)
        self._vel = Twist()
        self._pub = rospy.Publisher('/cmd_vel', Twist)
        self._lspeed = .2
    
    def moveInDirection(self, direction):
        if direction == "forwards":
            self._vel.linear.x = self._lspeed
            self._vel.linear.y = 0
        elif direction == "backwards":
            self._vel.linear.x = -self._lspeed
            self._vel.linear.y = 0
        elif direction == "left":
            self._vel.linear.x = 0
            self._vel.linear.y = -self._lspeed
        elif direction == "right":
            self._vel.linear.x = 0
            self._vel.linear.y = self._lspeed
        
        self._pub.publish(self._vel)
    
    def go(self):
        for direction in ["forwards", "left", "backwards", "right"]:
            i = 0
            while i < 9:
                self.moveInDirection(direction)
                i += 1
                self._rate.sleep()
                
def bb8_callback(request):
    resp = customResponse()
    resp.success = True
    moveObj = MoveBB8()
    for i in range(request.repetitions):
        moveObj.go()
    return resp

if __name__ == '__main__':
    rospy.logdebug('Initiating bb8 server...')
    rospy.init_node('move_bb8_server')
    bb8_service = rospy.Service('bb8_service', custom, bb8_callback)
    rospy.spin()