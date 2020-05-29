
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

    def insertRespRec(self, tim, dat):
        conn = self.connect()
        try:
            query1 = """insert cputemp_table 
            (temp_time, temp_data)
            values (%s, %s); """
            cursor = conn.cursor()
            
            cursor.execute(query1, (tim, dat))
                
            conn.commit()    
            
        except Exception as e:
            print("DB Error at insertRespRec", e)
        finally:
            conn.close()

    def insertRespRecList(self, recList):
        conn = self.connect()
        try:
            query1 = """insert resp_table 
            (dev_id, rec_time, resp_data)
            values (%s, %s); """
            cursor = conn.cursor()
            
            for rec in recList:
                tim = rec['rec_time']
                dat = rec['resp_data']
                cursor.execute(query1, (tim, dat))
                
            conn.commit()    
            
        except Exception as e:
            print("DB Error at insertRespRec", e)
        finally:
            conn.close()

    def insertRespRec4All(self, dev, tim, dat):
        conn = self.connect()
        try:
            query1 = """insert resp_table_all 
            (dev_id, rec_time, resp_data)
            values (%s, %s, %s); """
            cursor = conn.cursor()
            
            cursor.execute(query1, (dev, tim, dat))
                
            conn.commit()    
            
        except Exception as e:
            print("DB Error at insertRespRec", e)
        finally:
            conn.close()

    def buildRESPDFFromDB(self):
        conn = self.connect()
        cursor = conn.cursor()
        
        
        df_data = {'date':[], 'RESP':[]}
        query = "select rec_time, resp_data from resp_table "
        cursor.execute(query)
        for row in cursor:
            df_data['date'].append(row[0].strftime("%Y-%m-%d %H:%M:%S.%f"))
            df_data['RESP'].append(float(row[1]))
        
        respdf = pd.DataFrame(data=df_data)
        respdf = respdf.set_index('date')
        return respdf

    def buildRESPAllDFFromDB(self):
        conn = self.connect()
        cursor = conn.cursor()
                
        df_data = {'date':[], 'RESP':[]}
        query = "select rec_time, resp_data from resp_table_all "
        cursor.execute(query)
        for row in cursor:
            df_data['date'].append(row[0].strftime("%Y-%m-%d %H:%M:%S.%f"))
            df_data['RESP'].append(float(row[1]))
        
        respdf = pd.DataFrame(data=df_data)
        respdf = respdf.set_index('date')
        return respdf

    def buildRESPDFFromDBJSON(self):
        conn = self.connect()
        cursor = conn.cursor()
                
        df_data = {'date':[], 'RESP':[]}
        query = "select rec_time, resp_data from resp_table_all "
        cursor.execute(query)
        for row in cursor:
            df_data['date'].append(row[0].strftime("%Y-%m-%d %H:%M:%S.%f"))
            df_data['RESP'].append(float(row[1]))
        
        respdf = pd.DataFrame(data=df_data)
        respdf = respdf.set_index('date')
        return respdf
