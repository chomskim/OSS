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

import mqconfig_stat as mqconfig

DB_HOST = dbconfig.IP_ADDR
DB = DBHelper(DB_HOST)

MQ_HOST = mqconfig.mq_host
MQ_TOPIC = mqconfig.mq_topic

count = 0
sample_freq = 10 # count of data in 1 sec.
record_freq = 1 # count of data to record in 1 sec.
sample_max = sample_freq / record_freq
sum_data = 0.0

BUF_MAX = 10
rec_buf = []

def pushData2DB(tim, dat):
    try:    
        #print(tim, dat)
        print("{:d} {:s},{:s}".format(count, tim, dat))
        DB.insertStatusRec(tim, dat)
            
    except Exception as e:
        print ("Exception", e)
        
def on_connect(client, userdata, flags, rc):
    try:    
        print("Connect result: {}".format(mqtt.connack_string(rc)))
        client.connected_flag = True
        client.subscribe(MQ_TOPIC, qos=1)
    except Exception as e:
        print ("Exception", e)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))

def on_message(client, userdata, msg):
    global count
    
    try:    
        count +=1
        payload_string = msg.payload.decode('utf-8')
        #print("{:d} Topic: {}. Payload: {}".format(count, msg.topic, payload_string))
        row_data = payload_string.split(',')
        rec_data = ",".join(row_data[1:])
        rec_time = row_data[0]
     
        pushData2DB(rec_time, rec_data)
        
    except Exception as e:
        print ("Exception", e)
       
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

