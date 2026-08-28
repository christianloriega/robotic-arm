import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__('joint_command_publisher') # turns python class into a ROS2 node
        self.joint_command_publisher = self.create_publisher(Float64MultiArray, 'joint_targets', 10) # topic

        self.timer = self.create_timer(1.0, self.publish_joint_commands) # publish joint commands every second

    def publish_joint_commands(self):
        joint_commands = Float64MultiArray() # ROS message type for sending an array of float64 values
        joint_commands.data = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0] # example joint angles in degrees

        self.joint_command_publisher.publish(joint_commands) # publish the joint commands to the 'joint_targets' topic

def main(args=None):
        rclpy.init(args=args) # initialize ROS2 (starts ROS and creates node object)

        node = JointCommandPublisher() # creates object from class
        rclpy.spin(node) # keeps the node running and processing callbacks

        node.destroy_node()
        rclpy.shutdown() # shuts down ROS2

if __name__ == '__main__':
    main()