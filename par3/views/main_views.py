from flask import Blueprint, render_template

bp=Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def inter_par3():
    return render_template('main.html')
