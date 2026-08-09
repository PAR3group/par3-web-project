import re
from flask import Blueprint, g, jsonify, render_template, request, session, url_for

from par3 import db, storage
from par3.models import Join, JoinApply, Post, ShaftRecommend
from par3.views.auth_views import login_required

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
        "posts_count": Post.query.filter_by(author=user.nickname).count(),
        "join_posts_count": Join.query.filter_by(writer_id=user.id).count(),
        "join_participate_count": JoinApply.query.filter_by(applicant_id=user.id).count(),
        "join_likes_count": 0,
        "shop_likes_count": 0,
        "shop_orders_count": 0,
    }


@bp.route('/mypage')
@login_required
def mypage():
    user = g.user
    profile = build_profile(user)
    activity_data = build_activity_data(user)
    equipments = get_recommended_equipments(user)

    return render_template('my-page.html', profile=profile, activity=activity_data, equipments=equipments)


@bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
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


@bp.route('/reset-password')
@login_required
def reset_password():
    return f"<h2>비밀번호 수정 페이지입니다.</h2><a href='{url_for('mypage.mypage')}'>마이페이지로 돌아가기</a>"


@bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    user = g.user
    db.session.delete(user)
    db.session.commit()
    session.clear()

    return f"<script>alert('회원탈퇴가 완료되었습니다.\n\n그동안 PAR3와 함께해 주셔서 감사합니다.\n언제든 새로운 라운드를 시작하고 싶다면 다시 찾아와 주세요.'); location.href='{url_for('main.index')}';</script>"