import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String, Int32MultiArray

# from cv_bridge import CvBridge

from threading import Thread
import time
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
# import asyncio
# import json
# import os
from collections import deque
import cv2
# test
app = Flask(__name__)


class WebControllerNode(Node):
    def __init__(self):
        super().__init__('web_controller_node')

        self.get_logger().info(f"Start web server")
        self.get_logger().info(f"TEST11111")

        HOST_DEFAULT = "0.0.0.0"
        PORT_DEFAULT = "5001"
        self.get_logger().info(
            f"Running the flask server on {HOST_DEFAULT}:{PORT_DEFAULT}")

        self.app_thread = Thread(target=app.run,
                                 daemon=True,
                                 kwargs={
                                     "host": HOST_DEFAULT,
                                     "port": PORT_DEFAULT,
                                     "use_reloader": False,
                                     "threaded": True}
                                 )
        self.app_thread.start()

        # TODO: Gradually speed up and down after holding the key for a while?
        # Maybe increase some speed every 0.5 second?
        # TODO: capture key board control
        # TODO: is it possible to make this modulize, like a general control command button?

        self.__wheel_control_pub = self.create_publisher(String,
                                                         'control/motor',
                                                         1)
        self.__fan_control_pub = self.create_publisher(String,
                                                       'control/fan',
                                                       1)

        self.video_url = "http://192.168.43.196:8889/cam"

    def publish_wheel_control(self, control: str):
        msg = String()
        msg.data = control
        self.__wheel_control_pub.publish(msg)
        self.get_logger().info(f"Wheel: {control}")

    def publish_fan_control(self, control: str):
        msg = String()
        msg.data = control
        self.__fan_control_pub.publish(msg)
        self.get_logger().info(f"Fan: {control}")


@app.route('/')
def index():
    global web_app_node
    video_url = web_app_node.video_url
    web_app_node.get_logger().info(f"URL: {video_url}")
    return render_template('index.html', video_url_string=video_url)


@app.route('/update_video', methods=['POST'])
def update_video():
    global web_app_node
    new_video_url = request.form.get('video_url')
    if new_video_url:
        web_app_node.video_url = new_video_url
    return jsonify({"updated_url": web_app_node.video_url})


# TODO: change API to wheel control only
@app.route('/control', methods=['POST'])
def control():
    global web_app_node
    control_cmd = request.form.get("control")
    web_app_node.get_logger().info(f"Button clicked: {control_cmd}")
    web_app_node.publish_wheel_control(control_cmd)
    return jsonify({"control": control_cmd})


# TODO: publish fan control API and javascript


rclpy.init(args=None)
web_app_node = WebControllerNode()
try:
    executor = MultiThreadedExecutor()
    executor.add_node(web_app_node)
    try:
        executor.spin()
    finally:
        web_app_node.destroy_node()
finally:
    rclpy.shutdown()
