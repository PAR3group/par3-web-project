import re

from flask import Blueprint, g, jsonify, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from par3 import db, storage
from par3.models import Join, JoinApply, Post, ShaftRecommend, CartItem
from par3.views.auth_views import login_required
from par3.views.mypage_password_form import ChangePasswordForm

bp = Blueprint('mypage', __name__)

DEFAULT_PROFILE_IMG = "https://raw.githubusercontent.com/feathericons/feather/master/icons/user.svg"

GENDER_DB_TO_LABEL = {'M': '남성', 'F': '여성'}
GENDER_LABEL_TO_DB = {'남성': 'M', '여성': 'F'}

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


def get_recommended_equipments(user):
    recommend = ShaftRecommend.query.filter_by(user_id=user.id).first()
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


def build_recent_activities(user, limit=3):
    events = []

    for post in Post.query.filter_by(author=user.nickname).order_by(Post.created_at.desc()).limit(limit).all():
        events.append((post.created_at, f"📝 '{post.title}' 게시글을 작성했습니다."))

    for join in Join.query.filter_by(writer_id=user.id).order_by(Join.create_date.desc()).limit(limit).all():
        events.append((join.create_date, f"⛳ {join.course_name} 조인 모집 글을 작성했습니다."))

    applies = JoinApply.query.filter_by(applicant_id=user.id).order_by(JoinApply.create_date.desc()).limit(limit).all()
    join_ids = [apply.join_id for apply in applies]
    joins_by_id = {j.id: j for j in Join.query.filter(Join.id.in_(join_ids)).all()} if join_ids else {}
    for apply in applies:
        joined = joins_by_id.get(apply.join_id)
        course_name = joined.course_name if joined else "조인"
        events.append((apply.create_date, f"🤝 '{course_name}' 라운딩 조인 참여 신청을 완료했습니다."))

    events.sort(key=lambda e: e[0], reverse=True)
    return [text for _, text in events[:limit]]


def build_profile(user):
    # 🟢 DB의 phonenumber (+82 010-0000-0000)를 국가코드와 전화번호로 파싱
    country_code = ""
    phone_number = user.phonenumber or ""

    if phone_number.startswith("+"):
        parts = phone_number.split(" ", 1)
        if len(parts) == 2:
            country_code = parts[0]
            phone_number = parts[1]
        else:
            match = re.match(r"^(\+\d{1,3})(.*)$", phone_number)
            if match:
                country_code = match.group(1)
                phone_number = match.group(2).strip()

    return {
        "user_id": user.user_id,
        "email": user.email,
        "nickname": user.nickname,
        "name": user.username,
        "country_code": country_code,  # 🟢 파싱된 국가코드 (+82)
        "phone": phone_number,         # 🟢 파싱된 전화번호 (010-0000-0000)
        "gender": GENDER_DB_TO_LABEL.get(user.user_sex, user.user_sex),
        "golf_experience": GOLF_EXPERIENCE_LABELS.get(user.experience_years, '-'),
        "golf_experience_code": user.experience_years,
        "home_address": user.home_address,
        "profile_img": user.profile_img or DEFAULT_PROFILE_IMG,
        "recent_activities": build_recent_activities(user),
    }


def build_activity_data(user):
    return {
        "posts_count": Post.query.filter_by(
            author=user.nickname
        ).count(),

        "join_posts_count": Join.query.filter_by(
            writer_id=user.id
        ).count(),

        "join_participate_count": JoinApply.query.filter_by(
            applicant_id=user.id
        ).count(),

        # 현재 JOIN에는 찜 저장 기능이 아직 없음
        "join_likes_count": 0,

        # 현재 SHOP에서 사용자별로 저장되는 것은 CartItem
        "shop_likes_count": CartItem.query.filter_by(
            user_id=user.id
        ).count(),

        # 현재 SHOP에는 주문 완료 데이터를 저장하는 모델이 없음
        "shop_orders_count": 0,
    }


@bp.route('/mypage')
@login_required
def mypage():
    user = g.user
    password_form = ChangePasswordForm()
    profile = build_profile(user)
    activity_data = build_activity_data(user)
    equipments = get_recommended_equipments(user)

    # 내 장바구니 목록
    my_cart_items = CartItem.query.filter_by(
        user_id=user.id
        ).all()    

     # 내가 작성한 게시글 목록
    my_posts = Post.query.filter_by(
        author=user.nickname
    ).order_by(
        Post.created_at.desc()
    ).all()

     # 내가 작성한 골프조인 글 목록
    my_join_posts = Join.query.filter_by(
        writer_id=user.id
    ).order_by(
        Join.create_date.desc()
    ).all()

    # 내가 참여한 골프조인 내역
    my_join_applies = JoinApply.query.filter_by(
        applicant_id=user.id
    ).order_by(
        JoinApply.create_date.desc()
    ).all()
    
    my_join_participates = []

    for apply in my_join_applies:
        joined = Join.query.get(apply.join_id)

        if joined:
            my_join_participates.append(joined)

    

    return render_template(
        'my-page.html',
        profile=profile,
        activity=activity_data,
        equipments=equipments,
        my_posts=my_posts,
        my_join_posts=my_join_posts,
        my_join_participates=my_join_participates,
        my_cart_items=my_cart_items,
        password_form=password_form
    )

    
@bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    # 1. 기존 편지 내용(이름, 이메일 등) 읽기
    user = g.user

    email = request.form.get('email')
    nickname = request.form.get('nickname')
    name = request.form.get('name')
    country_code = request.form.get('country_code')  # 🟢 국가코드 (+82)
    phone = request.form.get('phone')                 # 🟢 전화번호 입력값
    gender = request.form.get('gender')
    golf_experience = request.form.get('golf_experience')
    home_address = request.form.get('home_address')

    if email:
        user.email = email
    if nickname:
        user.nickname = nickname
    if name:
        user.username = name
        
    # 🟢 중복 방지 및 국가코드 + 전화번호 정제 저장
    if phone:
        clean_phone = re.sub(r"^\+\d{1,3}\s*", "", phone.strip())  # 기존에 섞여 들어간 +82 등 제거
        if country_code:
            user.phonenumber = f"{country_code} {clean_phone}"
        else:
            user.phonenumber = clean_phone

    if gender:
        user.user_sex = GENDER_LABEL_TO_DB.get(gender, gender)
    if golf_experience in ('0', '1', '2', '3'):
        user.experience_years = int(golf_experience)
    if home_address:
        user.home_address = home_address

    avatar_file = request.files.get('avatar_file')
    if avatar_file and avatar_file.filename:
        try:
            user.profile_img = storage.upload_image(avatar_file, 'avatars')
        except Exception:
            pass

    db.session.commit()

    return f"<script>alert('프로필 정보가 성공적으로 수정되었습니다.'); location.href='{url_for('mypage.mypage')}';</script>"


@bp.route('/update-avatar', methods=['POST'])
@login_required
def update_avatar():
    avatar_file = request.files.get('avatar_file')
    if not avatar_file or not avatar_file.filename:
        return jsonify({'success': False, 'message': '파일이 없습니다.'}), 400

    user = g.user
    try:
        user.profile_img = storage.upload_image(avatar_file, 'avatars')
    except storage.StorageUploadError as e:
        return jsonify({'success': False, 'message': str(e)}), 500

    db.session.commit()

    return jsonify({'success': True, 'profile_img': user.profile_img})


@bp.route('/reset-avatar', methods=['POST'])
@login_required
def reset_avatar():
    user = g.user
    user.profile_img = None
    db.session.commit()

    return jsonify({'success': True, 'profile_img': DEFAULT_PROFILE_IMG})


@bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ChangePasswordForm()
    user = g.user

    if form.validate_on_submit():

        # 1. 현재 비밀번호 확인
        if not check_password_hash(
            user.password,
            form.current_password.data
        ):
            form.current_password.errors.append(
                '현재 비밀번호가 올바르지 않습니다.'
            )

        # 2. 현재 비밀번호와 새 비밀번호가 같은지 확인
        elif check_password_hash(
            user.password,
            form.new_password.data
        ):
            form.new_password.errors.append(
                '현재 비밀번호와 다른 비밀번호를 입력해주세요.'
            )

        else:
            # 3. 새 비밀번호 암호화 저장
            user.password = generate_password_hash(
                form.new_password.data
            )

            db.session.commit()

            return f"""
            <script>
                alert('비밀번호가 성공적으로 변경되었습니다.');
                location.href='{url_for('mypage.mypage')}';
            </script>
            """

    # 비밀번호 오류가 있으면 마이페이지를 다시 보여주고
    # 비밀번호 변경 모달을 자동으로 연다.
    profile = build_profile(user)
    activity_data = build_activity_data(user)
    equipments = get_recommended_equipments(user)

    # 내 장바구니
    my_cart_items = CartItem.query.filter_by(
        user_id=user.id
    ).all()

    # 내가 작성한 게시글
    my_posts = Post.query.filter_by(
        author=user.nickname
    ).order_by(
        Post.created_at.desc()
    ).all()

    # 내가 작성한 골프조인
    my_join_posts = Join.query.filter_by(
        writer_id=user.id
    ).order_by(
        Join.create_date.desc()
    ).all()

    # 내가 참여한 골프조인
    my_join_applies = JoinApply.query.filter_by(
        applicant_id=user.id
    ).order_by(
        JoinApply.create_date.desc()
    ).all()

    my_join_participates = []

    for apply in my_join_applies:
        joined = Join.query.get(apply.join_id)

        if joined:
            my_join_participates.append(joined)

    return render_template(
        'my-page.html',
        profile=profile,
        activity=activity_data,
        equipments=equipments,
        my_posts=my_posts,
        my_join_posts=my_join_posts,
        my_join_participates=my_join_participates,
        my_cart_items=my_cart_items,
        password_form=form,
        open_password_modal=True
    )


@bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    user = g.user
    db.session.delete(user)
    db.session.commit()
    session.clear()

    return f"<script>alert('회원탈퇴가 완료되었습니다.\n\n그동안 PAR3와 함께해 주셔서 감사합니다.\n언제든 새로운 라운드를 시작하고 싶다면 다시 찾아와 주세요.'); location.href='{url_for('main.index')}';</script>"