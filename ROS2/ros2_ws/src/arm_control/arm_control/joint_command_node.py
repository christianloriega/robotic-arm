import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from math import radians

class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__('joint_command_publisher') # turns python class into a ROS2 node
        self.joint_command_publisher = self.create_publisher(JointTrajectory, 'joint_targets', 10) # topic

        self.timer = self.create_timer(1.0, self.publish_joint_commands) # publish joint commands every second

    def publish_joint_commands(self):
        joint_commands = JointTrajectory() # ROS message type for sending joint trajectory commands
        joint_commands.joint_names = [
            'base_joint',
            'shoulder_joint',
            'elbow_joint',
            'wrist_rotate_joint',
            'wrist_pitch_joint',
            'gripper_joint'
        ] 

        point = JointTrajectoryPoint() # ROS message type for a single point in the trajectory
        # Home position in ROS joint coordinates
        point.positions = [
            radians(0),    # base_joint
            radians(0),  # shoulder_joint
            radians(0),   # elbow_joint
            radians(0),    # wrist_rotate_joint
            radians(0),  # wrist_pitch_joint
            radians(0)    # gripper_joint
        ]
        joint_commands.points = [point]

        self.joint_command_publisher.publish(joint_commands) # publish the joint commands to the 'joint_targets' topic

def main(args=None):
        rclpy.init(args=args) # initialize ROS2 (starts ROS and creates node object)

        node = JointCommandPublisher() # creates object from class
        rclpy.spin(node) # keeps the node running and processing callbacks

        node.destroy_node()
        rclpy.shutdown() # shuts down ROS2

if __name__ == '__main__':
    main()