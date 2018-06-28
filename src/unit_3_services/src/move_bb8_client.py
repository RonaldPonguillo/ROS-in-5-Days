#!/usr/bin/env python
import rospy
from custom_srv_msg.srv import custom, customRequest

if __name__ == '__main__':
    rospy.init_node('move_bb8_client')
    rospy.wait_for_service('/bb8_service')
    bb8_service = rospy.ServiceProxy('/bb8_service', custom)
    req = customRequest()
    req.repetitions = 2
    result = bb8_service(req)
    print(result)
