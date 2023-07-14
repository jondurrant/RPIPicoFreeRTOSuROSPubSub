#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration
from tf_transformations import quaternion_from_euler

class PoseNode(Node):
	def __init__(self):
		super().__init__("Pub_Node")
		self.pose_publisher = self.create_publisher(PoseStamped, "do_pose", 10)
		self.pose_timer = self.create_timer(10.0, self.publish_pose)
		self.poses=[0.0, 3.14/2, 3.14, -3.14/2, 0.0, -3.14/2, 3.14, 3.14/2]
		self.currentPose = 0;

	def publish_pose(self):
		z =self.poses[self.currentPose]
		self.currentPose += 1
		if (self.currentPose >= len(self.poses)):
			self.currentPose = 0
		goal = PoseStamped()
		goal.header.frame_id = "/base_link"
		d = Duration(seconds=5)
		t = self.get_clock().now() + d
		goal.header.stamp = t.to_msg()
		
		(goal.pose.orientation.x,
		goal.pose.orientation.y,
		goal.pose.orientation.z,
		goal.pose.orientation.w) = quaternion_from_euler(0, 0, z)
		self.pose_publisher.publish(goal)

def main(args=None):
	rclpy.init(args=args)
	node = PoseNode()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == "__main__":
	main()