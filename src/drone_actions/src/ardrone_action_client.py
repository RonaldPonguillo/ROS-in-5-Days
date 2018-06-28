#!/usr/bin/env python
import rospy
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneActionFeedback, ArdroneActionResult
from geometry_msgs.msg import Twist

def action_callback(feedback):
    global nImage
    print('[Feedback] we got image #{}'.format(nImage))
    nImage += 1


if __name__ == '__main__':
    rospy.init_node('ardrone_action_client')
    client = actionlib.SimpleActionClient('/ardrone_action_server', ArdroneAction)
    
    nImage = 0
    rate = rospy.Rate(2)
    vel = Twist()
    vel_pub = rospy.Publisher('/cmd_vel', Twist)
    
    client.wait_for_server()
    goal = ArdroneGoal()
    goal.nseconds = 10
    
    client.send_goal(goal, feedback_cb=action_callback)
    state_result = client.get_state()
    
    while state_result < 2:
        vel.linear.x = .2
        vel_pub.publish(vel)
        rate.sleep()
        state_result = client.get_state()
    vel.linear.x = 0
    vel_pub.publish(vel)
    