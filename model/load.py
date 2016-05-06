import os
import traceback
from flask import Blueprint, render_template, request, g
from operator import itemgetter

def foo():
  v = request.form.get('load_path')
  return v

load = Blueprint('load', __name__, template_folder = 'templates')

@load.route('/load/')
def load_index():
  return render_template('load.html')

@load.route('/load/', methods = ['POST'])
def load_submit():
    load_path = request.form.get('load_path', '')
    return load_path
