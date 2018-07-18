#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:31:47 2018

@author: zachclem
"""

from flask import Flask, render_template, request
from flask_cors import CORS
from sklearn.externals import joblib
import pandas as pd
import pymysql as db
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


@app.route('/recommend/<user_id>', methods=['GET'])
def make_prediction(user_id):
    if request.method=='GET':

        conn = db.connect(host='192.168.2.88', port=3306, user='zach', passwd='1qaz!QAZ', db='old')
        cursor = conn.cursor()
        query_visits = 'SELECT * from old.matomo_log_visit;'
        df_ = pd.read_sql_query(query_visits, conn)
        df = df_[['idvisit', 'idsite', 'idvisitor', 'user_id', 'visitor_count_visits', 'visit_total_actions', 'visitor_days_since_last', 'visit_total_time']]
        df = df.groupby(['user_id', 'idsite']).agg({'user_id': 'count',
                                         'visit_total_actions': 'mean',
                                         'visit_total_time': 'mean',
                                         'visitor_days_since_last': 'mean'}).unstack()
        df = df.rename(columns={'user_id' : 'visit_counts'})
        mi = df.columns
        mi.tolist()
        ind = pd.Index([e[0] + str(e[1]) for e in mi.tolist()])
        df.columns = ind
        #df[['visit_counts1', 'visit_counts4', 'visit_counts5', 'visit_counts6', 'visit_counts7', 'visit_counts8', 'visit_total_actions1', 'visit_total_actions4', 'visit_total_actions5', 'visit_total_actions6', 'visit_total_actions7', 'visit_total_actions8', 'visit_total_time1', 'visit_total_time4', 'visit_total_time5', 'visit_total_time6', 'visit_total_time7', 'visit_total_time8']] = df[['visit_counts1', 'visit_counts4', 'visit_counts5', 'visit_counts6', 'visit_counts7', 'visit_counts8', 'visit_total_actions1', 'visit_total_actions4', 'visit_total_actions5', 'visit_total_actions6', 'visit_total_actions7', 'visit_total_actions8', 'visit_total_time1', 'visit_total_time4', 'visit_total_time5', 'visit_total_time6', 'visit_total_time7', 'visit_total_time8']].fillna(value=0)
        df[['visit_counts4', 'visit_counts5', 'visit_counts6', 'visit_counts7', 'visit_counts8', 'visit_total_actions4', 'visit_total_actions5', 'visit_total_actions6', 'visit_total_actions7', 'visit_total_actions8', 'visit_total_time4', 'visit_total_time5', 'visit_total_time6', 'visit_total_time7', 'visit_total_time8']] = df[['visit_counts4', 'visit_counts5', 'visit_counts6', 'visit_counts7', 'visit_counts8', 'visit_total_actions4', 'visit_total_actions5', 'visit_total_actions6', 'visit_total_actions7', 'visit_total_actions8', 'visit_total_time4', 'visit_total_time5', 'visit_total_time6', 'visit_total_time7', 'visit_total_time8']].fillna(value=0)
        
        #df[['visitor_days_since_last1', 'visitor_days_since_last4', 'visitor_days_since_last5', 'visitor_days_since_last6', 'visitor_days_since_last7', 'visitor_days_since_last8']] = df[['visitor_days_since_last1', 'visitor_days_since_last4', 'visitor_days_since_last5', 'visitor_days_since_last6', 'visitor_days_since_last7', 'visitor_days_since_last8']].fillna(value=999999)
        df[['visitor_days_since_last4', 'visitor_days_since_last5', 'visitor_days_since_last6', 'visitor_days_since_last7', 'visitor_days_since_last8']] = df[['visitor_days_since_last4', 'visitor_days_since_last5', 'visitor_days_since_last6', 'visitor_days_since_last7', 'visitor_days_since_last8']].fillna(value=999999)
        
        #user = df.loc[b'\xa9J\x8f\xe5\xcc\xb1\x9b\xa6', :]
        #user = df.iloc[id_int, :]
        user = df.loc[user_id, :]
        distances, indices = model.kneighbors([user])
        user_look_up = indices[0][1]
        k_neighbor = df.index.values[user_look_up]
        #convert user position back to id or email

        return render_template('index.html', label=('recommended users for ', user_id, 'is', k_neighbor))

if __name__ == '__main__':
    model = joblib.load("knn.pkl")
    app.run(debug=True, port=5000)

