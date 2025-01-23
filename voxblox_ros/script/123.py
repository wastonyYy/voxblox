#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped

def odom_to_transform(odom_msg):
    transform = TransformStamped()
    transform.header = odom_msg.header
    transform.header.frame_id = "/world"  
    transform.child_frame_id = "vicon/firefly_sbx/firefly_sbx"  
    transform.transform.translation.x = odom_msg.pose.pose.position.x
    transform.transform.translation.y = odom_msg.pose.pose.position.y
    transform.transform.translation.z = odom_msg.pose.pose.position.z
    transform.transform.rotation = odom_msg.pose.pose.orientation  
    return transform

def callback(odom_msg):
    transform_msg = odom_to_transform(odom_msg)
    pub.publish(transform_msg)

if __name__ == "__main__":
    rospy.init_node("vins_odom_to_vicon_tf")
    pub = rospy.Publisher("/vicon/firefly_sbx/firefly_sbx", TransformStamped, queue_size=10)
    rospy.Subscriber("/body_odom", Odometry, callback)
    rospy.loginfo("Converter is running...")
    rospy.spin()