#!/usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped, TransformStamped
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_matrix, quaternion_from_matrix, translation_from_matrix
import tf2_ros

class CameraToBodyOdom:
    def __init__(self):
        rospy.init_node('camera_to_body_odom')

        self.body_T_cam0 = np.array([
            [0.0148655429818, -0.999880929698, 0.00414029679422, -0.0216401454975],
            [0.999557249008, 0.0149672133247, 0.025715529948, -0.064676986768],
            [-0.0257744366974, 0.00375618835797, 0.999660727178, 0.00981073058949],
            [0, 0, 0, 1]
        ])

        self.camera_odom_sub = rospy.Subscriber('/vins_estimator/camera_pose', Odometry, self.camera_odom_callback)

        self.body_odom_pub = rospy.Publisher('/body_odom', Odometry, queue_size=10)

    def camera_odom_callback(self, msg):
        cam_position = np.array([
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            msg.pose.pose.position.z
        ])
        cam_orientation = np.array([
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w
        ])

        cam_T_odom = quaternion_matrix(cam_orientation)
        cam_T_odom[:3, 3] = cam_position

        body_T_odom = np.dot(self.body_T_cam0, cam_T_odom)

        body_position = translation_from_matrix(body_T_odom)
        body_orientation = quaternion_from_matrix(body_T_odom)

        body_odom_msg = Odometry()
        body_odom_msg.header.stamp = msg.header.stamp
        body_odom_msg.header.frame_id = 'body'
        body_odom_msg.pose.pose.position.x = body_position[0]
        body_odom_msg.pose.pose.position.y = body_position[1]
        body_odom_msg.pose.pose.position.z = body_position[2]
        body_odom_msg.pose.pose.orientation.x = body_orientation[0]
        body_odom_msg.pose.pose.orientation.y = body_orientation[1]
        body_odom_msg.pose.pose.orientation.z = body_orientation[2]
        body_odom_msg.pose.pose.orientation.w = body_orientation[3]

        self.body_odom_pub.publish(body_odom_msg)

if __name__ == '__main__':
    try:
        converter = CameraToBodyOdom()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass