from par3 import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False, unique=True)
    nickname = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)
    user_sex = db.Column(db.String(1), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)

class ShaftRecommend(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    driver_weight = db.Column(db.Integer)
    wood5_weight = db.Column(db.Integer)
    utility4_weight = db.Column(db.Integer)
    iron7_weight = db.Column(db.Integer)
    driver_flex = db.Column(db.String(5))


# 조인페이지 관련
class Join(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 작성자 - User 테이블과 연결 (팀원 User 모델의 id를 참조)
    writer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    course_name = db.Column(db.String(100), nullable=False)      # 골프장명
    region = db.Column(db.String(20))                              # 지역
    round_date = db.Column(db.Date, nullable=False)                 # 라운드 날짜
    tee_time = db.Column(db.String(10))                              # 티오프 시간
    course_info = db.Column(db.String(100))                           # 코스 이름
    cost = db.Column(db.Integer)                                       # 비용
    recruit_count = db.Column(db.Integer, default=4)                   # 총 모집 인원
    filled_count = db.Column(db.Integer, default=1)                     # 현재 채워진 인원
    gender_condition = db.Column(db.String(20))                         # 성별 조건
    title = db.Column(db.String(200))                                    # 제목
    content = db.Column(db.Text)                                          # 상세 내용
    thumb_img = db.Column(db.String(200), default='no_image.png')         # 썸네일 이미지 파일명
    create_date = db.Column(db.DateTime, default=datetime.now)