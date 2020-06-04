'''
Created on 2020. 6. 4.

@author: cskim
'''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (8, 4)

import dbconfig
from dbhelper import DBHelper

DB_HOST = dbconfig.IP_ADDR
DB = DBHelper(DB_HOST)

drawDF = DB.buildStatusDFFromDB(10)
drawDF.plot.line()
    
tempSvgFile = 'C:/Temp/iot/plot_1.svg'
plt.savefig(tempSvgFile, format='svg')
