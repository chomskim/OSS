'''
Created on 2018. 11. 18.

@author: cskim
'''
import os
import uuid

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask
from flask import render_template
from flask import session
from flask import jsonify

from dbhelper import DBHelper
import dbconfig

DB = DBHelper(dbconfig.IP_ADDR)

plt.rcParams["figure.figsize"] = (8, 4)

app = Flask(__name__)
app.secret_key = 'qmOdTeca0nM2sq01JEN53DTTHoTlWStk'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/statusplot/<num>")
def statusplot(num):
        
    svg = ''
        
    if not session.get('uid'):
        session['uid'] = uuid.uuid4()
    #print ("session['uid']=%s"%session['uid'])
    num = int(num)
    #print ("<num={}>".format(num))
            
    drawDF = DB.buildStatusDFFromDB(num)
    #print(drawDF)
    
    y1 = drawDF['Temp']
    y2 = drawDF['CPU']
    y3 = drawDF['Mem']
    y1_min = int(y1.min()- 1)
    y1_max = int(y1.max() + 1)

    fig,ax1 = plt.subplots()
    ax2=ax1.twinx()
    ax1.set_ylim([0, 100])
    ax2.set_ylim([y1_min, y1_max])

    y1.plot(ax=ax2,style='g')
    y2.plot(ax=ax1,style='r')
    y3.plot(ax=ax1,style='b')
    
    tempSvgFile = './static/temp/plot_%s.svg' % session['uid']
    plt.savefig(tempSvgFile, format='svg')
    
    with open(tempSvgFile, 'rt', encoding='UTF8') as svgfile:
        svg = svgfile.read()
        #print ({'svg': svg})
    #"""
    try:
        os.remove(tempSvgFile)
    except OSError as e:
        #print ("SVG File Read Error: %s - %s." % (e.filename, e.strerror))
        pass
    #"""
    #return send_file('./static/price_plot.png', mimetype='image/png')
    return jsonify({'svg': svg})
    
    
if __name__ == '__main__':
    app.run(port=5001, debug=False)
