import os
import util
import traceback
from flask import Blueprint, render_template, request, g
from operator import itemgetter

def foo():
  v = request.form.get('load_path')
  print v
#  cmd = 'ssh -i hawqdemo.pem ec2-user@ec2-52-39-229-191.us-west-2.compute.amazonaws.com "cd /tmpData/; wget %s -O tData"' % v
  cmd = 'ssh -i hawqdemo.pem ec2-user@ec2-52-39-229-191.us-west-2.compute.amazonaws.com "cd /tmpData/; wget %s -O tData"' 
  os.system(cmd % v)

  db = util.db_connect()
  util.createtable(db)
  sql = "copy netflix_sample from '/tmpData/tData' delimiter ','"
  util.db_query(db, sql)

#  print v
#  return v

load = Blueprint('load', __name__, template_folder = 'templates')

@load.route('/load/')
def load_index():
  return render_template('load.html')

@load.route('/load/', methods = ['POST'])
def load_submit():
    load_path = request.form.get('load_path', '')
    foo()
    return load_path
