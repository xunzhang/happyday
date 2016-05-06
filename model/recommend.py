import os
import util
import traceback
from flask import Blueprint, render_template, request, g
from operator import itemgetter

def rec_sim_item(iid):
  sql = "select mid2 from netflix_sample_movie_similarity where mid1 = %s limit 20" % iid
  db = util.db_connect()
  v = util.db_query(db, sql)
  return v

recommend = Blueprint('recommend', __name__, template_folder = 'templates')

@recommend.route('/recommend/')
def recommend_index():
  return render_template('recommend.html')

@recommend.route('/recommend/', methods = ['POST'])
def load_submit():
    v = rec_sim_item(request.form.get('iid'))
    print str(v)
    res = '\n'.join(str(v).strip('mid2').split(' '))
    return res 
