#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import actionlib
from actionlib.msg import TestAction, TestFeedback, TestResult

class SquareWrapper(object):
    
    _feedback = TestFeedback()
    _result = TestResult()
    
    def __init__(self):
        self._as = actionlib.SimpleActionServer('drone_square_as', TestAction, self.goal_callback, False)
        self._as.start()
        self._vel = Twist()
        self._vel_pub = rospy.Publisher('/cmd_vel', Twist)
        self._l_speed = .3
        
    def move_drone(self, direction):
        if direction == "forwards":
            self._vel.linear.x = self._l_speed
            self._vel.linear.y = 0
        elif direction == "backwards":
            self._vel.linear.x = -self._l_speed
            self._vel.linear.y = 0
        elif direction == "left":
            self._vel.linear.x = 0
            self._vel.linear.y = self._l_speed
        elif direction == "right":
            self._vel.linear.x = 0
            self._vel.linear.y = -self._l_speed
        elif direction == "stop":
            self._vel.linear.x = 0
            self._vel.linear.y = 0
        self._vel_pub.publish(self._vel)
    
        
    def goal_callback(self, goal):
        
        rate = rospy.Rate(2)
        success = True
        
        for direction in ["forwards", "left", "backwards", "right"]:
            print("Moving", direction)
            if self._as.is_preempt_requested():
                success = False
                self.move_drone("stop")
                break
            i = 0
            while i < 8:
                self.move_drone(direction)
                rate.sleep()
                i += 1
        self.move_drone("stop")
        
        if success:
            self._as.set_succeeded(self._result)

if __name__ == "__main__":
    rospy.init_node('drone_square')
    SquareWrapper()
    rospy.spin()
    # rostopic pub /drone_square_as/goal actionlib/TestActionGoal
    
    