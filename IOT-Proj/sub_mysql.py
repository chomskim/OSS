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
sample_freq = 10 # count of data in 1 sec.
record_freq = 1 # count of data to record in 1 sec.
sample_max = sample_freq / record_freq
sum_data = 0.0

buf_max = record_freq
rec_buf = []

def pushData2DB(tim, dat):
    global count
    #print("{:d} {},{:.4f}".format(count, tim.strftime('%Y-%m-%d %H:%M:%S'), dat))
    DB.insertRespRec(tim, dat)

def pushData2List4DB(tim, dat):
    global count
    global rec_buf
    #print(tim, dat)
    print("{:d} {},{:.4f}".format(count, tim.strftime('%Y-%m-%d %H:%M:%S'), dat))
    
    rec = {}
    rec['temp_time'] = tim
    rec['temp_data'] = dat
    rec_buf.append(rec)
    if len(rec_buf) >= buf_max:
        DB.insertRespRecList(rec_buf)
        rec_buf = []

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

    rec_time = datetime.strptime(row_data[0], "%Y-%m-%d %H:%M:%S.%f")
    sub_data = float(row_data[1])
    
    sample_count += 1
    sum_data += sub_data
        
    #print(dev_name, rec_time, sub_data)
         
    if sample_count >= sample_max:
        #print(payload_string)
        avg_data = sum_data / sample_count
        str_data = '{:.1f}'.format(avg_data)
        print(sample_count, rec_time, str_data)
        pushData2DB(rec_time, str_data)
        sample_count = 0
        sum_data = 0
    
if __name__ == "__main__":
    print ("get client")
    client = mqtt.Client("SUB_CPU_TEMP_2_DB")
    client.username_pw_set(mqconfig.mq_user, password=mqconfig.mq_password)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    print ("Try to connect {} ".format(MQ_HOST))
    client.connect(MQ_HOST, 1883, 120)
    print ("connected {} ".format(MQ_HOST))
    client.loop_forever()

