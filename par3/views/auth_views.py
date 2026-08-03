from flask import Blueprint, flash, redirect, render_template, url_for
from par3 import db
from par3.models import User
from par3.forms import UserCreateForm
from werkzeug.security import generate_password_hash, check_password_hash


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
        
