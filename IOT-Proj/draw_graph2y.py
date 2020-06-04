'''
Created on 2020. 6. 4.

@author: cskim
'''
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (8, 4)

import dbconfig
from dbhelper import DBHelper

DB_HOST = dbconfig.IP_ADDR
DB = DBHelper(DB_HOST)

drawDF = DB.buildStatusDFFromDB(10)
    
y1 = drawDF['Temp']
y2 = drawDF['CPU']
y3 = drawDF['Mem']

fig,ax1 = plt.subplots()
ax2=ax1.twinx()
ax1.set_ylim([0, 100])
ax2.set_ylim([50, 55])

y1.plot(ax=ax2,style='g')
y2.plot(ax=ax1,style='r')
y3.plot(ax=ax1,style='b')

tempSvgFile = 'C:/Temp/iot/plot_1.svg'
plt.savefig(tempSvgFile, format='svg')

