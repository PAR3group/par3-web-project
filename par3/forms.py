from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SelectField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp


class UserCreateForm(FlaskForm):
    user_id = StringField(
        '아이디',
        validators=[
            DataRequired(message='아이디를 입력해주세요.'),
            Length(min=4, max=20, message='4~20자 이내로 입력해주세요.'),
            Regexp(
                r'^[A-Za-z0-9_.]+$',
                message='아이디는 영문, 숫자, _, . 만 사용할 수 있습니다.'
            )
        ]
    )
    username = StringField('이름', validators=[
        DataRequired('이름을 입력해주세요.'), 
        Length(max=20, message='20자 이내로 입력해주세요.'),
        Regexp(r'^[가-힣A-Za-z]+$', message='이름은 한글 또는 영문만 입력할 수 있습니다.')
        ])
    nickname = StringField('닉네임', validators=[DataRequired('닉네임을 입력해주세요.'), Length(min=2, max=20, message='2~20자 이내로 입력해주세요.')])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요.'),
        Length(min=8, message='비밀번호는 최소 8자 이상이어야 합니다.'),
        # 영문, 숫자, 특수기호가 모두 포함되었는지 검사하는 정규식
        Regexp(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+|])[A-Za-z\d!@#$%^&*()\-_=+|]{8,}$',
            message='비밀번호는 영문, 숫자, 특수기호를 포함한 8자 이상이어야 합니다.'
        )
    ])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호를 다시 입력해주세요.'), EqualTo('password1', message='비밀번호가 일치하지 않습니다.')])
    email = EmailField('이메일', validators=[DataRequired('이메일을 입력해주세요.'), Email(message='올바른 이메일 형식을 입력해주세요.')])
    phone1 = SelectField('앞자리', choices=[
        ('010', '010'),
        ('011', '011'),
        ('016', '016'),
        ('017', '017'),
        ('018', '018'),
        ('019', '019')        
    ], validators=[DataRequired()], default='010') 
    phone2 = StringField('가운데', validators=[DataRequired(), Regexp(r'^\d{4}$', message='숫자 4자리를 입력해주세요.')]) 
    phone3 = StringField('뒷자리', validators=[DataRequired(), Regexp(r'^\d{4}$', message='숫자 4자리를 입력해주세요.')])
    user_sex = RadioField('성별', choices=[
        ('M', '남성'),
        ('F', '여성')
    ], validators=[DataRequired()])
    experience_years = SelectField('구력', choices=[
        ("", '선택하세요.'),
        ('0', '1년 이하'),
        ('1', '1년 ~ 2년'),
        ('2', '2년 ~ 5년'),
        ('3', '5년 이상')
    ], validators=[DataRequired('구력을 선택해주세요.')])