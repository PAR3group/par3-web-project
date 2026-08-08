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
    # 관리자 여부 추가
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    profile_img = db.Column(db.Text)
    home_address = db.Column(db.String(255))
    golf_experience = db.Column(db.String(50))

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

class ShopProduct(db.Model):
    __tablename__ = 'shop_product'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, nullable=False)
    main_img = db.Column(db.String(255))
    detail_img = db.Column(db.String(255))
    features = db.Column(db.JSON, default=list)  
    shipping = db.Column(db.String(50))
    origin = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    reviews = db.relationship('ProductReview', backref='product')


class ProductReview(db.Model):
    __tablename__ = 'product_review'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('shop_product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # 로그인 유저와 연결 가능
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=True)  # 리뷰별 평점 넣을 수 있게
    created_at = db.Column(db.DateTime, default=datetime.now)

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)  # 작성자 닉네임 (g.user.nickname 저장)

    image_url = db.Column(db.String(500))   # 첨부 이미지/동영상 경로
    is_video = db.Column(db.Boolean, default=False)

    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.now)

    # [참고] HTML에서 post.comments_list 로 접근하고 있어서 backref를 comments_list로 지정
    comments_list = db.relationship(
        'Comment',
        backref='post',
        lazy=True,
        cascade='all, delete-orphan'  # 게시글 삭제 시 딸린 댓글도 같이 삭제됨
    )



class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)  # 댓글 작성자 닉네임
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

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
    thumb_img = db.Column(db.String(200), default='golf_replace.png')  # 이미지 없을 때 기본 이미지         # 썸네일 이미지 파일명
    create_date = db.Column(db.DateTime, default=datetime.now)


# 조인페이지 - 조인참여하기 
class JoinApply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    join_id = db.Column(
        db.Integer,
        db.ForeignKey("join.id"),
        nullable=False
    )
    applicant_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    applicant_name = db.Column(db.String(50))
    applicant_phone = db.Column(db.String(20))
    golf_experience = db.Column(db.String(20))
    handicap = db.Column(db.String(20))
    create_date = db.Column(db.DateTime, default=datetime.now)
