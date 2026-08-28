import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from math import degrees


class ServoController(Node):

    def __init__(self):
        super().__init__('servo_controller')

        self.joint_command_subscriber = self.create_subscription(
            JointTrajectory,
            'joint_targets',
            self.receive_joint_commands,
            10
        )

    def receive_joint_commands(self, joint_commands):

        names = joint_commands.joint_names
        positions = joint_commands.points[0].positions

        for name, position in zip(names, positions):
            self.get_logger().info(
                f'{name}: {degrees(position):.1f} deg'
            )

        print()


def main(args=None):

    rclpy.init(args=args)

    node = ServoController()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()