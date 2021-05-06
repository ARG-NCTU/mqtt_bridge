#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import rospy
import socket

default_topic = 'topic name'

class MQTTpublisher(object):
    def __init__(self):
        rospy.init_node("mqtt_client")

        d = rospy.Duration(float(rospy.get_param('~period', 3)))
        mqtt_ip = rospy.get_param('~mqtt_ip', '104.199.238.34')
        mqtt_port = int(rospy.get_param('~mqtt_port', 1883))
        self.mqtt_topic = rospy.get_param('~mqtt_topic', 'VehState')

        self.hostname = socket.gethostname()

        self.mqtt_client = mqtt.Client("ros_mqtt")
        self.mqtt_client.on_publish = self.on_publish
        self.mqtt_client.on_connect = self.on_connect
        rospy.loginfo("Connecting to mqtt broker...")
        self.mqtt_client.connect(mqtt_ip, mqtt_port)

        self.timer1 = rospy.Timer(d, self.cb_timer1)

    def cb_timer1(self, event):
        #if self.current_msg is not None:
        #Create payload
        payload = self.create_payload()

        #MQTT publish
        ret = self.mqtt_client.publish(self.mqtt_topic ,payload)
        rospy.loginfo("publish " + str(ret.mid))

    def create_payload(self):
        rospy.loginfo("111111")
        return str(self.hostname) + ': ' + str(rospy.get_time())

    def on_connect(self, client, userdata, flags, rc):
        rospy.loginfo("Connected with broker, result: " + mqtt.connack_string(rc))

    def on_publish(self, client, userdata, mid):
        rospy.loginfo("payload published " + str(mid))

    def on_shutdown(self):
        self.mqtt_client.disconnect() 
        rospy.loginfo("Shutting down...")

    def loop(self, timeout = .1):
        self.mqtt_client.loop(timeout)

if __name__ == "__main__":
    mqtt_pub = MQTTpublisher()
    rospy.on_shutdown(mqtt_pub.on_shutdown)
    
    while not rospy.is_shutdown():
        mqtt_pub.loop()


