import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String, Int32MultiArray
# import numpy as np
import cv2

# TODO: add rtsp streaming using opencv
# TODO: Set url using ros2 parameter, may need a callback or use service client?


class ImageProcNode(Node):
    def __init__(self):
        super().__init__("image_proc_node")

        self.get_logger().info(f"Start image proc")

        # self.color_sub = self.create_subscription(
        #     Int32MultiArray,
        #     'camera/color',
        #     self.color_callback,
        #     1)

        # self.min_hsv = np.array([0, 150, 128])
        # self.max_hsv = np.array([10, 255, 255])

        # Publisher for danger zone notification
        # Lag is not allowed
        self.control_pub = self.create_publisher(
            String,
            'control/motor',
            1)

    # def color_callback(self, msg):
    #     self.max_hsv = np.array([msg.data[0], msg.data[1], msg.data[2]])
    #     self.min_hsv = np.array([msg.data[3], msg.data[4], msg.data[5]])

    # def image_callback(self, msg):
    #     danger = False
    #     cv_image = self.cv_bridge.compressed_imgmsg_to_cv2(msg, 'bgr8')

    #     # ==== Start process frame ====
    #     hsv_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    #     mask_red = cv2.inRange(hsv_img, self.min_hsv, self.max_hsv)
    #     contours, hierarchy = cv2.findContours(
    #         mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    #     for cnt in contours:
    #         if cnt.shape[0] < 100:
    #             continue

    #         (x, y, w, h) = cv2.boundingRect(cnt)
    #         cv2.drawContours(cv_image, [cnt], -1, (0, 255, 0), 2)
    #         cv2.circle(cv_image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)
    #         danger = True
    #     # ==== End process frame ====

    #     notify_msg = String()
    #     notify_msg.data = 'off' if danger else 'on'
    #     self.control_pub.publish(notify_msg)
    #     self.image_pub.publish(
    #         self.cv_bridge.cv2_to_compressed_imgmsg(cv_image, 'jpg'))

    #     self.get_logger().info(f"[Camera] Image Subscribed")


def main(args=None):
    rclpy.init(args=args)

    image_proc_node = ImageProcNode()

    rclpy.spin(image_proc_node)

    image_proc_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
