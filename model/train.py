import os
import util
import traceback
from flask import Blueprint, render_template, request, g
from operator import itemgetter

train = Blueprint('train', __name__, template_folder = 'templates')

def mf():
  db = util.db_connect()

  dropmodelsql = "drop table if exists netflix_sample_model"
  util.db_query(db, dropmodelsql)

  kdimv = request.form.get('kdim')
  alphav = request.form.get('alpha')
  iterv = request.form.get('iter')
#sql = "SELECT madlib.lmf_igd_run('netflix_sample_model', 'netflix_sample', 'uid', 'mid', 'rating', 10727, 2244," + kdimv + "," + alphav + ", 0.1 , " + iterv + ", 1e-4);"
  sql = "SELECT madlib.lmf_igd_run('netflix_sample_model', 'netflix_sample', 'uid', 'mid', 'rating', 10727, 2244, %s, %s, 0.1, %s, 1e-4)" % (kdimv, alphav, iterv)
  print sql
  util.db_query(db, sql) 

  dropunfoldsql = "drop table if exists netflix_sample_model_structured"
  util.db_query(db, dropunfoldsql)

  unfoldsql = "create table netflix_sample_model_structured as ( select generate_series(1,2244) as mid, unnest_2d_1d(matrix_u[1:2244][1:%s]) as fac from netflix_sample_model where id = 1)" % iterv
  util.db_query(db, unfoldsql)

def cal_sim():
  db = util.db_connect()

  dropsql = 'drop table if exists netflix_sample_movie_similarity'
  util.db_query(db, dropsql)

  sql = 'CREATE TABLE netflix_sample_movie_similarity AS ( SELECT t1.mid AS mid1, t2.mid As mid2, madlib.cosine_similarity(t1.fac, t2.fac) as sim FROM netflix_sample_model_structured AS t1, netflix_sample_model_structured AS t2 WHERE t1.mid < t2.mid ORDER BY t1.mid, sim DESC, t2.mid)'
  util.db_query(db, sql)

@train.route('/train/')
def train_index():
  return render_template('train.html')

@train.route('/train/', methods = ['POST'])
def train_submit():
    mf()
    return 'Latent Factor Successfully Generated!'

@train.route('/train/sim')
def train_sim_index():
  return render_template('sim.html')

@train.route('/train/sim/', methods = ['POST'])
def train_sim_submit():
    cal_sim()
    return 'Factor Similarities Successfully Generated!'
