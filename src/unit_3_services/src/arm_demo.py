#!/usr/bin/env python

import rospy
import rospkg
from iri_wam_reproduce_trajectory.srv import ExecTraj, ExecTrajRequest
import sys
rospack = rospkg.RosPack()

rospy.init_node('arm_service_client')
rospy.wait_for_service('/execute_trajectory')
trajectory_service = rospy.ServiceProxy('/execute_trajectory', ExecTraj)
ex = ExecTrajRequest()
ex.file = rospack.get_path('iri_wam_reproduce_trajectory') + "/config/get_food.txt"
result=trajectory_service(ex)
print(result)