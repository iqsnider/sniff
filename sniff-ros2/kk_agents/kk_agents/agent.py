import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
import numpy as np
import time

class Agent(Node):
    """
    """
    def __init__(self):
        super().__init__("agent")

        self.declare_parameter("alpha",1.0)
        self.declare_parameter("x0", 0.0)
        self.declare_parameter("y0", 0.0)
        self.declare_parameter("target_x",1.0)
        self.declare_parameter("target_y",1.0)

        self.alpha = self.get_parameter("alpha").value
        self.pos = np.array([self.get_parameter("x0").value,
                             self.get_parameter("y0").value])
        self.target = np.array([self.get_parameter("target_x").value,
                                self.get_parameter("target_y").value])

        self.pub = self.create_publisher(Point, "position", 10)

        self.last_t = time.time()
        self.timer = self.create_timer(0.01, self.update)

        self.get_logger().info(f"agent starting at {self.pos} -> target {self.target}")

    def update(self):
        t = time.time()
        dt = t - self.last_t
        self.last_t = t

        dp = -self.alpha*(self.pos - self.target)
        self.pos += dp*dt

        msg = Point()
        msg.x, msg.y = float(self.pos[0]), float(self.pos[1])
        msg.z = 0.0

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    mode = Agent()
    rclpy.spin(node)
    rclpy.shutdown()
