import paho.mqtt.client as mqtt

import time
from datetime import datetime
from datetime import timedelta
import os

host = 'localhost'

count = 0
def on_connect(client, userdata, flags, rc):
    try:    
        print("Connect result: {}".format(mqtt.connack_string(rc)))
        client.connected_flag = True
        client.subscribe("cpu/temp", qos=1)
        
    except Exception as e:
        print ("Exception", e)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))

def on_message(client, userdata, msg):
    global count
    try:    
        count +=1
        payload_string = msg.payload.decode('utf-8')
        print("{:d} Topic: {}. Payload: {}".format(count, msg.topic, payload_string))
        
    except Exception as e:
        print ("Exception", e)

if __name__ == "__main__":
    print ("get client")
    client = mqtt.Client("CPU_TEMP_SUB01")
    client.username_pw_set('cesan', password='cesan@hufs')
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    print ("Try to connect {} ".format(host))
    client.connect(host, 1883, 120)
    print ("connected {} ".format(host))
    client.loop_forever()
