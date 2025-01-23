#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped

def odom_callback(msg):
    transform = TransformStamped()
    transform.header = msg.header
    transform.header.frame_id = 'world'  
    transform.child_frame_id = "body"
    transform.transform.translation.x = msg.pose.pose.position.x
    transform.transform.translation.y = msg.pose.pose.position.y
    transform.transform.translation.z = msg.pose.pose.position.z
    transform.transform.rotation = msg.pose.pose.orientation
    pub.publish(transform)

if __name__ == '__main__':
    rospy.init_node('odom_to_transform')
    pub = rospy.Publisher('/vicon/firefly_sbx/firefly_sbx', TransformStamped, queue_size=10)
    sub = rospy.Subscriber('/vins_estimator/camera_pose', Odometry, odom_callback)  
    rospy.spin()