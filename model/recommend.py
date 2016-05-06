import os
import traceback
from flask import Blueprint, render_template, request, g
from operator import itemgetter

recommend = Blueprint('recommend', __name__, template_folder = 'templates')

@recommend.route('/recommend/')
def recommend_index():
  return render_template('recommend.html')

@recommend.route('/recommend/', methods = ['POST'])
def load_submit():
    return 'xxx'
