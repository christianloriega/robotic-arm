import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class ServoController(Node):
    def __init__(self):
        super().__init__('servo_controller') # initialize python class into a ROS2 node
        self.joint_command_subcriber = self.create_subscription(
            Float64MultiArray, 
            'joint_targets', 
            self.receive_joint_commands, 
            10) # subscribe to the 'joint_targets' topic

    def receive_joint_commands(self, joint_commands):
        # This function will be called whenever a new message is received on the 'joint_targets' topic
        angles = joint_commands.data # extract the joint angles from the message
        self.get_logger().info(f'Base: {angles[0]}, '
                               f'Shoulder: {angles[1]}, '
                               f'Elbow: {angles[2]}, '
                               f'Wrist Rotate: {angles[3]}, '
                               f'Wrist Pitch: {angles[4]}, '
                               f'Gripper: {angles[5]}') # log the received joint angles

def main(args=None):
    rclpy.init(args=args) # initialize ROS2 (starts ROS and creates node object)

    node = ServoController() # creates object from class
    rclpy.spin(node) # keeps the node running and processing callbacks

    node.destroy_node()
    rclpy.shutdown() # shuts down ROS2

if __name__ == '__main__':
    main()    