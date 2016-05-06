#! /usr/bin/env python
# coding=utf-8

import os
from flask import Flask, render_template, request
from model import load

app = Flask(__name__)
app.config.from_object('setting')
app.register_blueprint(load)

port = int(os.getenv("PORT", 9099))

@app.before_request
def require_login():
    # TODO
    pass

@app.route('/test')
def foo():
    v = request.form.get('load_path', '')
    return v


@app.route('/')
def index():
    #from pg import DB
    #db = DB(dbname='postgres',
    #        host='ec2-52-39-229-191.us-west-2.compute.amazonaws.com',
    #        port=5432,user='gpadmin')
    #db.get_tables()
    #v = db.query('select * from t')
    #result = v.getresult()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
