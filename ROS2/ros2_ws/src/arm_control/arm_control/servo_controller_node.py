import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from math import degrees

import serial


class ServoController(Node):

    def __init__(self):
        super().__init__('servo_controller')

        self.serial_port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Update this to your Arduino's serial port

        self.joint_command_subscriber = self.create_subscription(
            JointTrajectory,
            'joint_targets',
            self.receive_joint_commands,
            10
        )


    def receive_joint_commands(self, joint_commands):

        names = joint_commands.joint_names
        positions = joint_commands.points[0].positions

        # Match each joint name with its position
        joint_targets = dict(zip(names, positions))

        # Convert ROS radians back to degrees
        base = round(degrees(joint_targets['base_joint']))
        shoulder = round(degrees(joint_targets['shoulder_joint']))
        elbow = round(degrees(joint_targets['elbow_joint']))
        wrist_rotate = round(degrees(joint_targets['wrist_rotate_joint']))
        wrist_pitch = round(degrees(joint_targets['wrist_pitch_joint']))
        gripper = round(degrees(joint_targets['gripper_joint']))

        # Create the command data that will eventually be sent to the Arduino through serial communication. The command is a string of comma-separated values representing the target angles for each joint.
        command = (
            f'{base},'
            f'{shoulder},'
            f'{elbow},'
            f'{wrist_rotate},'
            f'{wrist_pitch},'
            f'{gripper}'
        )

        self.serial_port.write((command + '\n').encode())

        self.get_logger().info(f'Servo command: {command}')
        print()


def main(args=None):

    rclpy.init(args=args)

    node = ServoController()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()