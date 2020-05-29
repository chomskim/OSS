import paho.mqtt.client as mqtt
import time
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import logging
import os
import socket

import dbconfig
from dbhelper import DBHelper

import mqconfig
DB_HOST = dbconfig.IP_ADDR
DB = DBHelper(DB_HOST)

MQ_HOST = mqconfig.mq_host
MQ_TITLE = mqconfig.mq_title

count = 0
sample_count = 0
sample_freq = 250 # count of data in 1 sec.
record_freq = 10 # count of data to record in 1 sec.
sample_max = sample_freq / record_freq
sum_data = 0.0

buf_max = 10
rec_buf = []

def pushData2DB(dev, tim, dat):
    global count
    #print(dev, tim, dat)
    print("{:d} {},{},{:.4f}".format(count, dev, tim.strftime('%Y-%m-%d %H:%M:%S'), dat))
    DB.insertRespRec4All(dev, tim, dat)

def on_connect(client, userdata, flags, rc):
    print("Connect result: {}".format(mqtt.connack_string(rc)))
    client.connected_flag = True
    client.subscribe(MQ_TITLE, qos=1)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))

def on_message(client, userdata, msg):
    global count
    global sample_count
    global sum_data
    
    count +=1
    payload_string = msg.payload.decode('utf-8')
    #print("{:d} Topic: {}. Payload: {}".format(count, msg.topic, payload_string))
    
    row_data = payload_string.split(",")
    #print(row_data)

    dev_name = row_data[0]
    rec_time = datetime.strptime(row_data[1], "%Y-%m-%d %H:%M:%S.%f")
    sub_data = float(row_data[2])
    
    pushData2DB(dev_name, rec_time, sub_data)
    
if __name__ == "__main__":
    print ("get client")
    client = mqtt.Client("SUB01_ALL")
    client.username_pw_set(mqconfig.mq_user, password=mqconfig.mq_password)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    print ("Try to connect {} ".format(MQ_HOST))
    client.connect(MQ_HOST, 1883, 120)
    print ("connected {} ".format(MQ_HOST))
    client.loop_forever()

