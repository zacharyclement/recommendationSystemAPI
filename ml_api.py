#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:31:47 2018

@author: zachclem
"""

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from io import StringIO
import json

import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route('/data', methods=['GET','POST'])
def data_test():
    if request.method == 'POST':
        data_data = request.data
        print('data data, ', data_data)
        d = json.loads(data_data)
        print('data_data dictionary', d)
        print('type: ', type(d))
        
        testData = StringIO(d)

        df = pd.read_csv(testData)

        print('df = ', df)
        
        
        # d is a string, return jsonified string
        return jsonify(d)
    else:
        dic = {"language": "python",
                "framework": "Flask",
                "name": "Zach",
                "v": {
                        "p" : 3.4,
                        "f" : 12
                 },
                "examples" : ["hi", "hello"],
                "boolean_test" : 'true',
    
                }
        return jsonify(dic)

        
if __name__ == '__main__':
    app.run(debug=True, port=5000)