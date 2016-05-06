import os
from flask import Blueprint, render_template, request
from util import PGDB
from load import DATA_TABLE

def mf(kdim, alpha, iterations):
    db = PGDB()
    db.connect_default()
    db.drop_table(DATA_TABLE+'_model')
    M = str(db.execute('SELECT max(uid) from %s' %
                       DATA_TABLE).getresult()[0][0])
    N = str(db.execute('SELECT max(iid) from %s' %
                       DATA_TABLE).getresult()[0][0])
    train_sql = "SELECT madlib.lmd_igd_run(%s, %s, 'uid', 'iid', 'rating', %s, %s, %s, %s, 0.1, %s, 1e-5)"
    db.execute(train_sql % (M, N, kdim, alpha, iterations))
    db.drop_table(DATA_TABLE + '_structured')
    unfold_sql = "CREATE TABLE %s AS (SELECT generate_series(1, %s) AS iid, unnest_2d_1d(matrix_u[1:%s][1:%s]) AS fac from %s WHERE id = 1)" 
    db.execute(unfold_sql % (DATA_TABLE + '_model_structured', M, M,
                             request.form.get('kdim'), DATA_TABLE + '_model'))

def cal_sim():
    db = PGDB()
    db.connect_default()
    db.drop_table(DATA_TABLE+'_item_similarity')
    calsim_sql = 'CREATE TABLE %s AS (SELECT t1.iid AS iid1, t2.iid AS iid2, madlib.cosine_similarity(t1.fac, t2.fac) AS sim FROM %s AS t1, %s AS t2 WHERE t1.iid < t2.iid ORDER BY t1.iid, sim DESC, t2.iid)'
    db.execute(calsim_sql % (DATA_TABLE + '_item_similarity',
                             DATA_TABLE + '_model_structured',
                             DATA_TABLE + '_model_structured'))

train = Blueprint('train', __name__, template_folder = 'templates')

@train.route('/train/')
def train_index():
  return render_template('train.html')

@train.route('/train/', methods = ['POST'])
def train_submit():
    mf(request.form.get('kdim'), request.form.get('alpha'), request.form.get('iter'))
    return 'Latent Factor Successfully Generated!'

@train.route('/train/sim')
def train_sim_index():
  return render_template('sim.html')

@train.route('/train/sim/', methods = ['POST'])
def train_sim_submit():
    cal_sim()
    return 'Factor Similarities Successfully Generated!'
