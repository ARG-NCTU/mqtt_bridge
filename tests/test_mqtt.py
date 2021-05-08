#!/usr/bin/env python3
import paho.mqtt.client as mqtt

def test_mqtt():
    mqtt_ip = "104.199.238.34"
    mqtt_port = int(1883)
    client = mqtt.Client()
    on_connect = client.connect(mqtt_ip, mqtt_port, keepalive=5)
    client.loop_start()
    assert on_connect is not None
    client.disconnect()
    client.loop_stop()

