from dbhelper import DBHelper
import dbconfig

DB = DBHelper(dbconfig.IP_ADDR)
try:
  conn = DB.connect()
  print("DB Connect Successful")
except Exception as e:
  print("DB Error in Connect DB", e)
finally:
  conn.close()

drawDF = DB.buildStatusDFFromDB(10)

print(drawDF)

