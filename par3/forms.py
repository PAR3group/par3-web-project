from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, EmailField, PasswordField, SelectField, BooleanField, RadioField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange, Optional, Regexp


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
    agree_all = BooleanField('전체 약관 동의하기')  # JS로만 동작 (DB 저장 X)
    agree_service = BooleanField(
        '[필수] 서비스 이용약관 동의',
        validators=[DataRequired(message='서비스 이용약관에 동의해주세요.')]
    )
    agree_privacy = BooleanField(
        '[필수] 개인정보 수집 및 이용 동의',
        validators=[DataRequired(message='개인정보 수집 및 이용에 동의해주세요.')]
    )
    agree_marketing = BooleanField('[선택] 마케팅 정보 수신 동의')

class RecommendForm(FlaskForm):

    # 기본 정보
    gender = SelectField(
        "성별",
        choices=[
            ("male", "남성"),
            ("female", "여성")
        ],
        validators=[DataRequired()]
    )

    user_height = IntegerField(
        "키(cm)",
        validators=[
            DataRequired(),
            NumberRange(min=100, max=250)
            ],
            render_kw={"min": 100, "max": 250, "placeholder": "예: 175"}
    )

    user_weight = IntegerField(
        "몸무게(kg)",
        validators=[
            DataRequired(),
            NumberRange(min=30, max=200)
        ],
        render_kw={"min": 30, "max": 200, "placeholder": "예: 70"}
    )

    # 단위
    distance_unit = SelectField(
        "비거리 단위",
        choices=[
            ("m", "미터(m)"),
            ("yd", "야드(yd)")
        ],
        validators=[DataRequired()]
    )

    speed_unit = SelectField(
        "스윙스피드 단위",
        choices=[
            ("ms", "m/s"),
            ("mph", "mph")
        ],
        validators=[Optional()]
    )

    # 스윙스피드(선택)
    swing_speed = FloatField(
        "드라이버 스윙스피드",
        validators=[Optional()],
        render_kw={"type": "number", "placeholder": "숫자만 작성" }
    )

    #  스윙스피드를 모르는 경우
    swing_speed_unknown = BooleanField("스윙스피드를 모르겠어요")

    # 추천받을 클럽 선택
    driver_selected = BooleanField("드라이버")
    wood5_selected = BooleanField("5번 우드")
    utility4_selected = BooleanField("4번 유틸")
    iron7_selected = BooleanField("7번 아이언")

    # 목표 비거리
    driver_distance = IntegerField(
        "드라이버 목표 비거리",
        validators=[Optional()]
    )

    wood5_distance = IntegerField(
        "5번 우드 목표 비거리",
        validators=[Optional()]
    )

    utility4_distance = IntegerField(
        "4번 유틸 목표 비거리",
        validators=[Optional()]
    )

    iron7_distance = IntegerField(
        "7번 아이언 목표 비거리",
        validators=[Optional()]
    )

    submit = SubmitField("추천받기")    

class UserLoginForm(FlaskForm):
    user_id=StringField('아이디', validators=[DataRequired("아이디를 입력하세요.")])
    password=PasswordField('비밀번호', validators=[DataRequired("비밀번호를 입력하세요.")])  

class FindIdForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired(message='이름을 입력해주세요.')])
    email = EmailField('이메일', validators=[DataRequired(message='이메일을 입력해주세요.'), Email(message='올바른 이메일 형식을 입력해주세요.')])


class FindPasswordForm(FlaskForm):
    user_id = StringField('아이디', validators=[DataRequired(message='아이디를 입력해주세요.')])
    email = EmailField('이메일', validators=[DataRequired(message='이메일을 입력해주세요.'), Email(message='올바른 이메일 형식을 입력해주세요.')])