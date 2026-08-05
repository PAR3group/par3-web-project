from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('intro.html')

@bp.route('/par3/')
def inter_par3():
    return render_template('main.html')