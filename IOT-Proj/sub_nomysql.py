import paho.mqtt.client as mqtt
import time
from datetime import datetime
from datetime import timedelta

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

BUF_MAX = record_freq
rec_buf = []

def pushData2DB(tim, dat):
    global count
    try:    
        print("{:d} {},{}".format(count, tim.strftime('%Y-%m-%d %H:%M:%S'), dat))
        #DB.insertStatusRec(tim, dat)
        
    except Exception as e:
        print ("Exception", e)

def on_connect(client, userdata, flags, rc):
    try:    
        print("Connect result: {}".format(mqtt.connack_string(rc)))
        client.connected_flag = True
        client.subscribe(MQ_TITLE, qos=1)
        
    except Exception as e:
        print ("Exception", e)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))

def on_message(client, userdata, msg):
    global count
    global sample_count
    global sum_data
    global sample_max
    
    try:    
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
            sample_count = 0
            sum_data = 0
            #print(count, sample_count, rec_time, str_data)
            pushData2DB(rec_time, str_data)
    
    except Exception as e:
        print ("Exception", e)

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

