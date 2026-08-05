from flask import Blueprint, flash, redirect, render_template, url_for, session, g, request
from par3 import db
from par3.models import User
from par3.forms import UserCreateForm, UserLoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import functools


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()

    if form.validate_on_submit():
        phonenumber = f"{form.phone1.data}-{form.phone2.data}-{form.phone3.data}"

        # 중복 체크 (아이디 / 닉네임 / 이메일 / 휴대폰번호 모두 unique 컬럼이라 다 확인해야 함)
        if User.query.filter_by(user_id=form.user_id.data).first():
            flash('이미 사용중인 아이디입니다.')
            return render_template('auth/signup.html', form=form)

        if User.query.filter_by(nickname=form.nickname.data).first():
            flash('이미 사용중인 닉네임입니다.')
            return render_template('auth/signup.html', form=form)

        if User.query.filter_by(email=form.email.data).first():
            flash('이미 사용중인 이메일입니다.')
            return render_template('auth/signup.html', form=form)

        if User.query.filter_by(phonenumber=phonenumber).first():
            flash('이미 등록된 휴대폰번호입니다.')
            return render_template('auth/signup.html', form=form)

        user = User()
        user.user_id = form.user_id.data
        user.username = form.username.data
        user.nickname = form.nickname.data
        user.email = form.email.data
        user.user_sex = form.user_sex.data
        user.experience_years = form.experience_years.data
        user.password = generate_password_hash(form.password1.data)
        user.phonenumber = phonenumber

        db.session.add(user)
        db.session.commit()
        flash('회원가입이 완료되었습니다. 로그인해주세요.')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        error = None
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id  # 수정: PK(id)를 저장해야 g.user 조회가 정상 동작함
            # 1. URL에 ?next=... 가 포함되어 있는지 확인
            next_page = request.args.get('next')
            
            # 2. next_page가 존재하면 그쪽으로, 없으면 메인 페이지로 이동
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.inter_par3'))

        flash(error)
    return render_template('auth/login.html', form=form)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.inter_par3'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.path))
        return view(*args, **kwargs)
    return wrapped_view