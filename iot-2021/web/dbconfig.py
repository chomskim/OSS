import os

#IP_ADDR = "172.30.1.6"
IP_ADDR = "172.30.1.7"
#DIR_DATAPATH = os.path.join("D:", r"D:\home\project\medical\data")

db_host = IP_ADDR
db_name = 'iot'
db_user = 'iot'
db_password = 'cesan'

def setHost(host):
    global db_host
    db_host = host
