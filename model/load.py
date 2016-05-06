import os
from flask import Blueprint, render_template, request
from util import PGDB
from config import LOGIN_KEY, HOST, TABLE_PREFIX, DELIMITER

DATA_TABLE=''

def load_data(fn):
    tbl = TABLE_PREFIX + fn.split('/')[-1]
    DATA_TABLE = tbl
    cmd = 'ssh -i %s %s "wget %s -O /tmpData/%s"'
    os.system(cmd % (LOGIN_KEY, HOST, fn, 'dat_' + fn.split('/')[-1]))
    db = PGDB()
    db.connect_default()
    db.drop_table(tbl)
    db.create_init_table(tbl)
    db.copy(tbl, '/tmpData/dat_' + fn.split('/')[-1], DELIMITER)

load = Blueprint('load', __name__, template_folder = 'templates')

@load.route('/load/')
def load_index():
  return render_template('load.html')

@load.route('/load/', methods = ['POST'])
def load_submit():
    load_data(request.form.get('load_path'))
    return "Loading Successfully Finished!"
