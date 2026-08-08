import json
from flask import Blueprint, render_template, redirect, url_for
import os
from par3.models import Post, Join
from par3.utils import get_golf_news_top3

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('intro.html')

@bp.route('/par3/')
@bp.route('/par3/')
def inter_par3():
    prize_top3, kpga_top3 = get_golf_news_top3()
    return render_template('main.html',
                           prize_top3=prize_top3,
                           kpga_top3=kpga_top3,
                           posts=Post.query.order_by(Post.likes.desc()).limit(3).all(),
                           join=Join.query.order_by(Join.create_date.desc()).limit(3).all()
                           )