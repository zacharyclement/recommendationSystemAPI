#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:31:47 2018

@author: zachclem
"""

from flask import Flask, render_template
from flask_cors import CORS
#from io import StringIO
#import json

#import numpy as np
#import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


#@app.route('/predict', methods=['GET','POST'])
#def make_prediction():
#    if request.method=='POST':
#        return render_template('index.html', label='3')

        
if __name__ == '__main__':
    #model = joblib.load("model.pkl")
    app.run(debug=True, port=5000)