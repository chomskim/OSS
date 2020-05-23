import time
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import os
import re

count = 0

host = "172.30.1.30"
#host = "192.168.43.226"

def on_connect(client, userdata, flags, rc):
    print("Connect result: {}".format(mqtt.connack_string(rc)))
    client.connected_flag = True

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))

def on_message(client, userdata, msg):
    global count
    count +=1
    payload_string = msg.payload.decode('utf-8')
    print("{:d} Topic: {}. Payload: {}".format(count, msg.topic, payload_string))

def pubTempData(client, freq=10, limit=100):
    delta = 1/freq
    
    for i in range(limit*freq):
        ti = datetime.now()
        temp = os.popen("vcgencmd measure_temp").readline()
        da = re.findall(r'\d+\.\d+',temp.rstrip())[0]

        row = "{:s},{:s}".format(ti.strftime("%Y-%m-%d %H:%M:%S.%f"),da)
        client.publish("cpu/temp",payload=row, qos=1)
        if i%freq == 0:
            print (i, row)
        time.sleep(delta)

if __name__ == "__main__":
    print ("get client")
    client = mqtt.Client("CPU_TEMP_PUB01")
    client.username_pw_set('cesan', password='cesan@hufs')
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    print ("Try to connect {} ".format(host))
    client.connect(host, port=1883, keepalive=120)
    print ("connected {} ".format(host))
    client.loop_start()
    pubTempData(client)

    print ("sleep end")
    client.loop_stop()
