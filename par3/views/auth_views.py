from flask import Blueprint, flash, redirect, render_template, url_for
from par3 import db
from par3.models import User
from par3.forms import UserCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
import functools


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if not user:
            user = User()
            form.populate_obj(user)
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)
        
# @login_required 할때 반드시 함수명 바로위에 위치해야함
def login_required(view):
    @functools.wraps(view)      # 함수의 이름이 바뀌지 않도록 지켜준다
    def wrapped_view(*args, **kwargs):          # 매개변수로 어떤거든 받겠다.
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped_view