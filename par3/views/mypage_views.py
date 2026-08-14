import re

from flask import Blueprint, g, jsonify, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from par3 import db, storage
from par3.models import (
    Join,
    JoinApply,
    JoinLike,
    Post,
    Comment,
    ShaftRecommend,
    CartItem,
)
from par3.views.auth_views import login_required
from par3.views.mypage_password_form import ChangePasswordForm


bp = Blueprint('mypage', __name__)


DEFAULT_PROFILE_IMG = (
    "https://raw.githubusercontent.com/feathericons/feather/master/icons/user.svg"
)


GENDER_DB_TO_LABEL = {
    'M': '남성',
    'F': '여성'
}

GENDER_LABEL_TO_DB = {
    '남성': 'M',
    '여성': 'F'
}


GOLF_EXPERIENCE_LABELS = {
    0: '1년 이하',
    1: '1년 ~ 2년',
    2: '2년 ~ 5년',
    3: '5년 이상',
}


CLUB_META = [
    ("driver_weight", "드라이버", "img/rec_D.jpg"),
    ("wood5_weight", "5번 우드", "img/rec_W.jpg"),
    ("utility4_weight", "4번 유틸", "img/rec_U.jpg"),
    ("iron7_weight", "7번 아이언", "img/rec_I.jpg"),
]


# ==========================================================
# 피팅 추천 결과
# ==========================================================

def get_recommended_equipments(user):
    recommend = ShaftRecommend.query.filter_by(
        user_id=user.id
    ).first()

    if recommend is None:
        return []

    equipments = []

    for weight_attr, label, image in CLUB_META:
        weight = getattr(recommend, weight_attr)

        if weight is None:
            continue

        equipments.append({
            "category": label,
            "weight": weight,
            "flex": recommend.driver_flex or "-",
            "image": image,
        })

    return equipments


# ==========================================================
# 최근 활동 내역
# ==========================================================

def build_recent_activities(user, limit=3):
    events = []

    # TALK 작성 게시글
    for post in (
        Post.query
        .filter_by(user_id=user.id)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .all()
    ):
        events.append(
            (
                post.created_at,
                f"📝 '{post.title}' 게시글을 작성했습니다."
            )
        )

    # 내가 작성한 골프조인
    for join in (
        Join.query
        .filter_by(writer_id=user.id)
        .order_by(Join.create_date.desc())
        .limit(limit)
        .all()
    ):
        events.append(
            (
                join.create_date,
                f"⛳ {join.course_name} 조인 모집 글을 작성했습니다."
            )
        )

    # 내가 참여한 골프조인
    applies = (
        JoinApply.query
        .filter_by(applicant_id=user.id)
        .order_by(JoinApply.create_date.desc())
        .limit(limit)
        .all()
    )

    join_ids = [
        apply.join_id
        for apply in applies
    ]

    joins_by_id = (
        {
            join.id: join
            for join in Join.query.filter(
                Join.id.in_(join_ids)
            ).all()
        }
        if join_ids
        else {}
    )

    for apply in applies:
        joined = joins_by_id.get(
            apply.join_id
        )

        course_name = (
            joined.course_name
            if joined
            else "조인"
        )

        events.append(
            (
                apply.create_date,
                f"🤝 '{course_name}' 라운딩 조인 참여 신청을 완료했습니다."
            )
        )

    events.sort(
        key=lambda event: event[0],
        reverse=True
    )

    return [
        text
        for _, text in events[:limit]
    ]


# ==========================================================
# 프로필 데이터
# ==========================================================

def build_profile(user):

    # DB 전화번호
    # 예: +82 010-0000-0000
    # 국가코드와 전화번호를 분리
    country_code = ""
    phone_number = user.phonenumber or ""

    if phone_number.startswith("+"):
        parts = phone_number.split(" ", 1)

        if len(parts) == 2:
            country_code = parts[0]
            phone_number = parts[1]

        else:
            match = re.match(
                r"^(\+\d{1,3})(.*)$",
                phone_number
            )

            if match:
                country_code = match.group(1)
                phone_number = (
                    match.group(2).strip()
                )

    return {
        "user_id": user.user_id,
        "email": user.email,
        "nickname": user.nickname,
        "name": user.username,
        "country_code": country_code,
        "phone": phone_number,
        "gender": GENDER_DB_TO_LABEL.get(
            user.user_sex,
            user.user_sex
        ),
        "golf_experience": (
            GOLF_EXPERIENCE_LABELS.get(
                user.experience_years,
                '-'
            )
        ),
        "golf_experience_code": (
            user.experience_years
        ),
        "home_address": user.home_address,
        "profile_img": (
            user.profile_img
            or DEFAULT_PROFILE_IMG
        ),
        "recent_activities": (
            build_recent_activities(user)
        ),
    }


# ==========================================================
# 이력관리 개수
# ==========================================================

def build_activity_data(user):

    return {

        # 작성한 TALK 게시글
        "posts_count": (
            Post.query
            .filter_by(
                user_id=user.id
            )
            .count()
        ),

        # 작성한 골프조인
        "join_posts_count": (
            Join.query
            .filter_by(
                writer_id=user.id
            )
            .count()
        ),

        # 참여한 골프조인
        "join_participate_count": (
            JoinApply.query
            .filter_by(
                applicant_id=user.id
            )
            .count()
        ),

        # 찜한 골프조인
        "join_likes_count": (
            JoinLike.query
            .filter_by(
                user_id=user.id
            )
            .count()
        ),

        # 장바구니
        "shop_likes_count": (
            CartItem.query
            .filter_by(
                user_id=user.id
            )
            .count()
        ),

        # 현재 주문 완료 모델 연결 전
        "shop_orders_count": 0,
    }


# ==========================================================
# MY PAGE
# ==========================================================

@bp.route('/mypage')
@login_required
def mypage():

    user = g.user

    password_form = ChangePasswordForm()

    profile = build_profile(user)

    activity_data = build_activity_data(
        user
    )

    equipments = (
        get_recommended_equipments(
            user
        )
    )



    # ------------------------------------------------------
    # 내 장바구니 목록
    # ------------------------------------------------------

    my_cart_items = (
        CartItem.query
        .filter_by(
            user_id=user.id
        )
        .all()
    )


   # ------------------------------------------------------
   # 내가 작성한 TALK 게시글
    # ------------------------------------------------------

    my_posts = (
        Post.query
        .filter_by(
            user_id=user.id
        )
        .order_by(
            Post.created_at.desc()
        )
        .all()
    )

    # ------------------------------------------------------
    # 내가 찜한 골프조인
    # JoinLike → Join 연결
    # ------------------------------------------------------

    my_join_likes = (
        Join.query
        .join(
            JoinLike,
            JoinLike.join_id == Join.id
        )
        .filter(
            JoinLike.user_id == user.id
        )
        .order_by(
            JoinLike.create_date.desc()
        )
        .all()
    )


    # ------------------------------------------------------
    # 내가 작성한 골프조인
    # ------------------------------------------------------

    my_join_posts = (
        Join.query
        .filter_by(
            writer_id=user.id
        )
        .order_by(
            Join.create_date.desc()
        )
        .all()
    )


    # ------------------------------------------------------
    # 내가 참여한 골프조인 신청내역
    # ------------------------------------------------------

    my_join_applies = (
        JoinApply.query
        .filter_by(
            applicant_id=user.id
        )
        .order_by(
            JoinApply.create_date.desc()
        )
        .all()
    )


    # ------------------------------------------------------
    # JoinApply → 실제 Join 데이터로 변환
    # ------------------------------------------------------

    my_join_participates = []

    for apply in my_join_applies:

        joined = Join.query.get(
            apply.join_id
        )

        if joined:
            my_join_participates.append(
                joined
            )


    # ------------------------------------------------------
    # MY PAGE 템플릿
    # ------------------------------------------------------

    return render_template(
        'my-page.html',
        profile=profile,
        activity=activity_data,
        equipments=equipments,

        my_posts=my_posts,

        # 찜한 골프조인
        my_join_likes=my_join_likes,

        my_join_posts=my_join_posts,
        my_join_participates=my_join_participates,

        my_cart_items=my_cart_items,

        password_form=password_form
    )


# ==========================================================
# 프로필 수정
# ==========================================================

@bp.route(
    '/update-profile',
    methods=['POST']
)
@login_required
def update_profile():

    user = g.user

    email = request.form.get(
        'email'
    )

    nickname = request.form.get(
        'nickname'
    )

    name = request.form.get(
        'name'
    )

    country_code = request.form.get(
        'country_code'
    )

    phone = request.form.get(
        'phone'
    )

    gender = request.form.get(
        'gender'
    )

    golf_experience = request.form.get(
        'golf_experience'
    )

    home_address = request.form.get(
        'home_address'
    )


    # 이메일
    if email:
        user.email = email


    # 닉네임
    if nickname:
        user.nickname = nickname


    # 이름
    if name:
        user.username = name


    # ------------------------------------------------------
    # 국가코드 + 전화번호 저장
    # ------------------------------------------------------

    if phone:

        clean_phone = re.sub(
            r"^\+\d{1,3}\s*",
            "",
            phone.strip()
        )

        if country_code:

            user.phonenumber = (
                f"{country_code} "
                f"{clean_phone}"
            )

        else:

            user.phonenumber = (
                clean_phone
            )


    # 성별
    if gender:

        user.user_sex = (
            GENDER_LABEL_TO_DB.get(
                gender,
                gender
            )
        )


    # 구력
    if golf_experience in (
        '0',
        '1',
        '2',
        '3'
    ):

        user.experience_years = int(
            golf_experience
        )


    # 주소
    if home_address:

        user.home_address = (
            home_address
        )


    # ------------------------------------------------------
    # 프로필 이미지
    # ------------------------------------------------------

    avatar_file = request.files.get(
        'avatar_file'
    )

    if (
        avatar_file
        and avatar_file.filename
    ):

        try:

            user.profile_img = (
                storage.upload_image(
                    avatar_file,
                    'avatars'
                )
            )

        except Exception:
            pass


    db.session.commit()


    return (
        f"<script>"
        f"alert('프로필 정보가 성공적으로 수정되었습니다.'); "
        f"location.href='{url_for('mypage.mypage')}';"
        f"</script>"
    )


# ==========================================================
# 프로필 이미지 비동기 변경
# ==========================================================

@bp.route(
    '/update-avatar',
    methods=['POST']
)
@login_required
def update_avatar():

    avatar_file = request.files.get(
        'avatar_file'
    )

    if (
        not avatar_file
        or not avatar_file.filename
    ):

        return jsonify({
            'success': False,
            'message': '파일이 없습니다.'
        }), 400


    user = g.user


    try:

        user.profile_img = (
            storage.upload_image(
                avatar_file,
                'avatars'
            )
        )

    except storage.StorageUploadError as e:

        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


    db.session.commit()


    return jsonify({
        'success': True,
        'profile_img': user.profile_img
    })


# ==========================================================
# 프로필 이미지 초기화
# ==========================================================

@bp.route(
    '/reset-avatar',
    methods=['POST']
)
@login_required
def reset_avatar():

    user = g.user

    user.profile_img = None

    db.session.commit()


    return jsonify({
        'success': True,
        'profile_img': DEFAULT_PROFILE_IMG
    })


# ==========================================================
# 비밀번호 변경
# ==========================================================

@bp.route(
    '/reset-password',
    methods=['GET', 'POST']
)
@login_required
def reset_password():

    form = ChangePasswordForm()

    user = g.user


    # ------------------------------------------------------
    # 비밀번호 변경
    # ------------------------------------------------------

    if form.validate_on_submit():


        # 1. 현재 비밀번호 확인
        if not check_password_hash(
            user.password,
            form.current_password.data
        ):

            form.current_password.errors.append(
                '현재 비밀번호가 올바르지 않습니다.'
            )


        # 2. 현재 비밀번호와
        # 새 비밀번호가 같은지 확인
        elif check_password_hash(
            user.password,
            form.new_password.data
        ):

            form.new_password.errors.append(
                '현재 비밀번호와 다른 비밀번호를 입력해주세요.'
            )


        else:

            # 3. 새 비밀번호 암호화 저장
            user.password = (
                generate_password_hash(
                    form.new_password.data
                )
            )

            db.session.commit()


            return f"""
            <script>
                alert(
                    '비밀번호가 성공적으로 변경되었습니다.'
                );
                location.href='{url_for('mypage.mypage')}';
            </script>
            """


    # ======================================================
    # 비밀번호 오류가 있으면
    # MY PAGE 데이터를 다시 전부 불러온다.
    # ======================================================

    profile = build_profile(
        user
    )

    activity_data = (
        build_activity_data(
            user
        )
    )

    equipments = (
        get_recommended_equipments(
            user
        )
    )


    # ------------------------------------------------------
    # 내 장바구니
    # ------------------------------------------------------

    my_cart_items = (
        CartItem.query
        .filter_by(
            user_id=user.id
        )
        .all()
    )


    # ------------------------------------------------------
    # 내가 작성한 게시글
    # ------------------------------------------------------

    my_posts = (
        Post.query
        .filter_by(
            author=user.nickname
        )
        .order_by(
            Post.created_at.desc()
        )
        .all()
    )


    # ------------------------------------------------------
    # 내가 찜한 골프조인
    # ------------------------------------------------------

    my_join_likes = (
        Join.query
        .join(
            JoinLike,
            JoinLike.join_id == Join.id
        )
        .filter(
            JoinLike.user_id == user.id
        )
        .order_by(
            JoinLike.create_date.desc()
        )
        .all()
    )


    # ------------------------------------------------------
    # 내가 작성한 골프조인
    # ------------------------------------------------------

    my_join_posts = (
        Join.query
        .filter_by(
            writer_id=user.id
        )
        .order_by(
            Join.create_date.desc()
        )
        .all()
    )


    # ------------------------------------------------------
    # 내가 참여한 골프조인
    # ------------------------------------------------------

    my_join_applies = (
        JoinApply.query
        .filter_by(
            applicant_id=user.id
        )
        .order_by(
            JoinApply.create_date.desc()
        )
        .all()
    )


    my_join_participates = []


    for apply in my_join_applies:

        joined = Join.query.get(
            apply.join_id
        )

        if joined:

            my_join_participates.append(
                joined
            )


    # ------------------------------------------------------
    # 비밀번호 모달을 연 상태로
    # MY PAGE 다시 출력
    # ------------------------------------------------------

    return render_template(
        'my-page.html',

        profile=profile,
        activity=activity_data,
        equipments=equipments,

        my_posts=my_posts,

        # 찜한 골프조인
        my_join_likes=my_join_likes,

        my_join_posts=my_join_posts,
        my_join_participates=my_join_participates,

        my_cart_items=my_cart_items,

        password_form=form,
        open_password_modal=True
    )


# ==========================================================
# 회원탈퇴
# ==========================================================

@bp.route(
    '/delete-account',
    methods=['POST']
)
@login_required
def delete_account():

    user = g.user


    # ------------------------------------------------------
    # 기존 닉네임 보관
    # ------------------------------------------------------

    old_nickname = user.nickname


    # ======================================================
    # 실제 DB 행 삭제가 아닌
    # 탈퇴 상태 처리
    # ======================================================

    user.is_withdrawn = True

    user.is_suspended = True


    # ------------------------------------------------------
    # UNIQUE 필드 익명화
    # ------------------------------------------------------

    user.user_id = (
        f"withdrawn_{user.id}"
    )

    user.nickname = (
        f"탈퇴회원{user.id}"
    )

    user.email = (
        f"withdrawn_{user.id}@par3.local"
    )

    user.phonenumber = (
        f"withdrawn-{user.id}"
    )


    # ------------------------------------------------------
    # 개인정보 제거
    # ------------------------------------------------------

    user.username = "탈퇴회원"

    user.profile_img = None

    user.home_address = None


    # ------------------------------------------------------
    # 기존 비밀번호로 로그인하지 못하도록 변경
    # ------------------------------------------------------

    user.password = (
        generate_password_hash(
            f"withdrawn-{user.id}-{user.password}"
        )
    )


    # ------------------------------------------------------
    # 기존 TALK 게시글 작성자명 익명화
    # ------------------------------------------------------

    Post.query.filter_by(
        author=old_nickname
    ).update(
        {
            "author": user.nickname
        },
        synchronize_session=False
    )


    # ------------------------------------------------------
    # 기존 TALK 댓글 / 대댓글 작성자명 익명화
    # ------------------------------------------------------

    Comment.query.filter_by(
        author=old_nickname
    ).update(
        {
            "author": user.nickname
        },
        synchronize_session=False
    )


    db.session.commit()


    # ------------------------------------------------------
    # 로그인 세션 제거
    # ------------------------------------------------------

    session.clear()


    return f"""
    <script>
        alert(
            '회원탈퇴가 완료되었습니다.\\n\\n'
            + '그동안 PAR3와 함께해 주셔서 감사합니다.\\n'
            + '언제든 새로운 라운드를 시작하고 싶다면 다시 찾아와 주세요.'
        );

        location.href='{url_for('main.index')}';
    </script>
    """