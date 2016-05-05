from flask import Blueprint, render_template

load = Blueprint('load', __name__, template_folder = 'templates')

@load.route('/load/')
def load_index():
  return render_template('load.html')
