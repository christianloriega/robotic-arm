import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from math import degrees

import serial


class ServoController(Node):

    def __init__(self):
        super().__init__('servo_controller')

        # Physical servo angle when each ROS joint is at 0 degrees
        self.home_angles = {
            'base_joint': 135,
            'shoulder_joint': 90,
            'elbow_joint': 135,
            'wrist_rotate_joint': 90,
            'wrist_pitch_joint': 90,
            'gripper_joint': 0
        }

        # Direction of each physical servo TODO: Verify
        self.joint_directions = {
            'base_joint': 1,
            'shoulder_joint': -1,
            'elbow_joint': 1,
            'wrist_rotate_joint': 1,
            'wrist_pitch_joint': 1,
            'gripper_joint': 1
        }

        # Servo Limits
        self.servo_limits = {
            'base_joint': (0, 270),
            'shoulder_joint': (0, 180),
            'elbow_joint': (30, 240),
            'wrist_rotate_joint': (0, 180),
            'wrist_pitch_joint': (0, 180),
            'gripper_joint': (0, 90)
        }
        self.serial_port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Update this to your Arduino's serial port

        self.joint_command_subscriber = self.create_subscription(
            JointTrajectory,
            'joint_targets',
            self.receive_joint_commands,
            10
        )

    def ros_to_servo(self, joint_name, ros_angle_deg):
        home = self.home_angles[joint_name]
        direction= self.joint_directions[joint_name]

        servo_angle = home + direction * ros_angle_deg

        min_angle, max_angle = self.servo_limits[joint_name]

        clamped_angle = max(min_angle, min(max_angle, servo_angle))

        if clamped_angle != servo_angle:
            self.get_logger().warning(
                f'{joint_name} command {servo_angle:.1f} deg '
                f'clamped to {clamped_angle:.1f} deg'
        )

        return round(clamped_angle)

    def receive_joint_commands(self, joint_commands):

        if not joint_commands.points:
            self.get_logger().warning('Received trajectory with no points')
            return

        names = joint_commands.joint_names
        positions = joint_commands.points[0].positions

        # Match each joint name with its position
        joint_targets = dict(zip(names, positions))

        # Convert ROS joint positions from radians to calibrated servo angles
        base = self.ros_to_servo(
            'base_joint',
            degrees(joint_targets['base_joint'])
        )

        shoulder = self.ros_to_servo(
            'shoulder_joint',
            degrees(joint_targets['shoulder_joint'])
        )

        elbow = self.ros_to_servo(
            'elbow_joint',
            degrees(joint_targets['elbow_joint'])
        )

        wrist_rotate = self.ros_to_servo(
            'wrist_rotate_joint',
            degrees(joint_targets['wrist_rotate_joint'])
        )

        wrist_pitch = self.ros_to_servo(
            'wrist_pitch_joint',
            degrees(joint_targets['wrist_pitch_joint'])
        )

        gripper = self.ros_to_servo(
            'gripper_joint',
            degrees(joint_targets['gripper_joint'])
        )

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