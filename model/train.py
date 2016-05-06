import os
import traceback
from flask import Blueprint, render_template, request, g
from operator import itemgetter

train = Blueprint('train', __name__, template_folder = 'templates')

@train.route('/train/')
def train_index():
  return render_template('train.html')

@train.route('/train/', methods = ['POST'])
def train_submit():
    train_path = request.form.get('alpha', '')
    return train_path

@train.route('/train/sim')
def train_sim_index():
  return render_template('sim.html')

@train.route('/train/sim/', methods = ['POST'])
def train_sim_submit():
    return 'HAHAHA'
