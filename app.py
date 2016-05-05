#! /usr/bin/env python
# coding=utf-8

import os
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('setting')

@app.before_request
def require_login():
    # TODO
    pass

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
