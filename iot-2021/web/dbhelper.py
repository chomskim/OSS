
import mysql.connector
import numpy as np
import pandas as pd

import dbconfig

def floatInf0(fstr):
    fres = float(fstr)
    if np.isinf(fres):
        fres = 0
    return fres

class DBHelper:
    def __init__(self, host='127.0.0.1'):
        dbconfig.setHost(host)

    def connect(self):
        #print ("Getting connection to database")
        return mysql.connector.connect(
            host=dbconfig.db_host, 
            user=dbconfig.db_user, 
            password=dbconfig.db_password,
            database=dbconfig.db_name)

    def insertStatusRec(self, tim, dat):
        conn = self.connect()
        try:
            query1 = """insert cputemp_table 
            (temp_time, temp_data)
            values (%s, %s); """
            cursor = conn.cursor()
            
            cursor.execute(query1, (tim, dat))
                
            conn.commit()    
            
        except Exception as e:
            print("DB Error at insertStatusRec", e)
        finally:
            conn.close()

    def buildStatusDFFromDB(self, num=None):
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT sub.id, sub.stat_time, sub.stat_data FROM (
                SELECT id, stat_time, stat_data FROM status_table ORDER BY id DESC LIMIT %s
            ) sub ORDER BY sub.id ASC
            """
            cursor.execute(query, (num,))
        except Exception as e:
            print("DB Error at buildStatusDFFromDB", e)
        finally:
            conn.close()
        
        df_data = {'time':[], 'Temp':[], 'CPU':[], 'Mem':[]}
        for row in cursor:
            df_data['time'].append(row[1].strftime("%M:%S"))
            stat = row[2].split(",")
            
            df_data['Temp'].append(float(stat[0]))
            df_data['CPU'].append(float(stat[1]))
            df_data['Mem'].append(float(stat[2]))
        
        statdf = pd.DataFrame(data=df_data)
        statdf = statdf.set_index('time')
        statdf = statdf.tail(num)
        return statdf
        