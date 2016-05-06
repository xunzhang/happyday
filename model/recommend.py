import os
from flask import Blueprint, render_template, request
from util import PGDB
from load import DATA_TABLE

def rec_sim_item(iid, ktop):
    db = PGDB()
    db.connect_default()
    sql = 'SELECT iid2 FROM %s WHERE iid1 = %s LIMIT %s'
    return db.execute(sql % (DATA_TABLE + '_item_similarity', iid, ktop))

recommend = Blueprint('recommend', __name__, template_folder = 'templates')

@recommend.route('/recommend/')
def recommend_index():
  return render_template('recommend.html')

@recommend.route('/recommend/', methods = ['POST'])
def load_submit():
    v = rec_sim_item(request.form.get('iid'), request.form.get('ktop'))
    res = '\n'.join(str(v).strip('mid2').split(' '))
    return res
