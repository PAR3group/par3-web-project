from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp


class UserCreateForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired('이름을 입력하세요'), Length(min=1, max=20)])
    nickname = StringField('닉네임', validators=[DataRequired('닉네임을 입력하세요'), Length(min=2, max=20)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요.'),
        Length(min=8, message='비밀번호는 최소 8자 이상이어야 합니다.'),
        # 영문, 숫자, 특수기호가 모두 포함되었는지 검사하는 정규식
        Regexp(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+\\\\|\s]).+$',
            message='비밀번호는 영문, 숫자, 특수기호를 모두 포함해야 합니다.'
        )
    ])
    password2 = 