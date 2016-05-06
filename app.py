#! /usr/bin/env python
# coding=utf-8

import os
from flask import Flask, render_template
from model import load, train, recommend

app = Flask(__name__, static_url_path='', static_folder='images')
app.config.from_object('setting')
app.register_blueprint(load)
app.register_blueprint(train)
app.register_blueprint(recommend)

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
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
