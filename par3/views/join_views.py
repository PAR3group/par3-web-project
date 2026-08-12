# join_views.py
# ============================================
# PAR3 - JOIN (실시간 골프 조인 리스트) 라우트
# 담당: 오지 (feature/join-page)
# 연결 템플릿: templates/join.html
# ============================================

from flask import Blueprint, redirect, render_template, request, url_for,g
from par3.models import Join, JoinApply, User, JoinLike
from par3 import db
from datetime import date, datetime
import random  #추가
from par3.tour_api import search_golf_courses  #추가

# 'join' 이라는 이름의 블루프린트 생성
# url_prefix='/join' → 이 블루프린트 안의 모든 라우트는 앞에 자동으로 /join 이 붙음
bp = Blueprint('join', __name__, url_prefix='/join')


# ------------------------------------------------
# 조인 페이지 (골프 모임 목록 화면)
# 접속 주소: /join/
# ------------------------------------------------
@bp.route('/')
def join_list():
    joins = Join.query.order_by(Join.create_date.desc()).all()

    today = date.today()
    weekday_kr = ['월', '화', '수', '목', '금', '토', '일']
    for j in joins:
        j.dday = (j.round_date - today).days
        j.weekday = weekday_kr[j.round_date.weekday()]
        writer = User.query.get(j.writer_id)
        j.writer_nickname = writer.nickname if writer else '알 수 없음'
        # 이 조인 글에 실제로 신청한 사람들 목록 조회 (JoinApply 테이블에서)
        applies = JoinApply.query.filter_by(join_id=j.id).all()
        j.applicant_initials = [a.applicant_name[0].upper() for a in applies if a.applicant_name]
        # ------------------------------------------------
        # 참여하기 버튼 상태 계산
        # is_owner   : 로그인한 사용자가 이 글의 작성자인지
        # is_applied : 로그인한 사용자가 이미 신청했는지
        # is_full    : 정원이 다 찼는지
        # ------------------------------------------------
        if g.user is not None:
            j.is_owner = (j.writer_id == g.user.id)
            j.is_applied = JoinApply.query.filter_by(join_id=j.id, applicant_id=g.user.id).first() is not None
            # 추가: 로그인 사용자가 이 글에 좋아요를 눌렀는지 확인
            j.is_liked = JoinLike.query.filter_by(join_id=j.id, user_id=g.user.id).first() is not None
        else:
            j.is_owner = False
            j.is_applied = False
            j.is_liked = False

        j.is_full = j.filled_count >= j.recruit_count

    return render_template('join/join.html', joins=joins)

# ------------------------------------------------
# 조인 개설(모집) 폼 페이지
# 접속 주소: /join/create
# ------------------------------------------------
@bp.route('/create', methods=['GET', 'POST'])
def join_create():
    if g.user is None:
        return redirect(url_for('auth.login', next=request.path))

    if request.method == 'POST':
        new_join = Join(
            writer_id=g.user.id,
            course_name=request.form['course_name'],
            region=request.form.get('region', '기타'),
            round_date=datetime.strptime(request.form['round_date'], '%Y-%m-%d').date(),
            tee_time=request.form['tee_time'],
            course_info=request.form['course_info'],
            cost=int(request.form['cost']) if request.form['cost'] else 0,
            recruit_count=int(request.form['recruit_count']) if request.form.get('recruit_count') else 4,
            gender_condition=request.form.get('gender_condition', '무관'),
            title=request.form['title'],
            content=request.form['content'],
            filled_count=1,
            thumb_img=request.form.get('thumb_img_url') or 'golf_replace.png',
        )
        db.session.add(new_join)
        db.session.flush()

        writer_apply = JoinApply(
            join_id=new_join.id,
            applicant_id=g.user.id,
            applicant_name=g.user.nickname,
            applicant_phone=g.user.phonenumber,
            experience_years=g.user.experience_years or '',
            handicap='',
        )
        db.session.add(writer_apply)

        db.session.commit()
        return redirect(url_for('join.join_list'))

    return render_template('join/join_create.html')
# ------------------------------------------------

# ------------------------------------------------
# 조인 참가 신청 폼
# GET  : join_id에 해당하는 조인 글 정보를 화면에 채워서 보여줌
# POST : 신청 데이터 저장 + 해당 Join의 filled_count +1
# ------------------------------------------------
@bp.route('/apply/<int:join_id>', methods=['GET', 'POST'])
def join_apply(join_id):
    if g.user is None:
        return redirect(url_for('auth.login', next=request.path))

    join = Join.query.get_or_404(join_id)
    applicant = g.user   # ← 실제 로그인한 사용자
    # 본인 글이거나 이미 신청했으면 리스트로 돌려보냄
    if join.writer_id == applicant.id:
        return redirect(url_for('join.join_list'))

    already_applied = JoinApply.query.filter_by(join_id=join.id, applicant_id=applicant.id).first()
    if already_applied:
        return redirect(url_for('join.join_list'))

     # 남은 자리 계산 → 동반자 최대 추가 가능 수 (본인 신청분 1자리 제외)
    remaining_slots = join.recruit_count - join.filled_count
    max_companions = max(remaining_slots - 1, 0)

    if request.method == 'POST':
        # ------------------------------------------------
        # 본인 신청 정보 (첫 번째 세트, 이름/연락처는 index 없이 그대로)
        # 동반자 정보는 companion_name_1, companion_phone_1 ... 식으로 넘어옴
        # ------------------------------------------------
        applications_to_add = []

        # 본인
        applications_to_add.append({
            'name': request.form.get('applicant_name', applicant.nickname),
            'phone': request.form.get('applicant_phone', applicant.phonenumber),
            'experience': request.form.get('experience_years', ''),
            'handicap': request.form.get('handicap', ''),
        })

        # 동반자들 (있는 만큼만 순서대로 읽어옴)
        i = 1
        while request.form.get(f'companion_name_{i}') is not None:
            companion_name = request.form.get(f'companion_name_{i}', '').strip()
            if companion_name:   # 이름이 비어있지 않은 경우에만 추가
                applications_to_add.append({
                    'name': companion_name,
                    'phone': request.form.get(f'companion_phone_{i}', ''),
                    'experience': request.form.get(f'companion_experience_{i}', ''),
                    'handicap': request.form.get(f'companion_handicap_{i}', ''),
                })
            i += 1

        # 실제 신청 인원수가 남은 자리를 초과하지 않도록 서버에서도 한 번 더 방어
        applications_to_add = applications_to_add[:remaining_slots]

        for app_data in applications_to_add:
            new_apply = JoinApply(
                join_id=join.id,
                applicant_id=applicant.id,   # 동반자도 신청 주체는 로그인한 본인으로 기록
                applicant_name=app_data['name'],
                applicant_phone=app_data['phone'],
                experience_years=app_data['experience'],
                handicap=app_data['handicap'],
            )
            db.session.add(new_apply)

        # 실제 신청 인원수만큼 filled_count 증가 (정원 초과 방지)
        add_count = len(applications_to_add)
        join.filled_count = min(join.filled_count + add_count, join.recruit_count)

        db.session.commit()
        return redirect(url_for('join.join_list'))

    return render_template(
        'join/join_apply.html',
        join=join,
        applicant=applicant,
        max_companions=max_companions,
    )

from par3.tour_api import search_golf_courses

# ------------------------------------------------
# 골프장 검색 API (region, keyword 둘 다 선택적)
# 접속 주소: /join/api/golf_courses?region=서울&keyword=마이다스
# ------------------------------------------------
@bp.route('/api/golf_courses')
def golf_courses():
    region = request.args.get('region', '').strip()
    keyword = request.args.get('keyword', '').strip()
    results = search_golf_courses(region or None, keyword or None)
    return {'results': results}


# ------------------------------------------------
# 조인 글 수정 (작성자 전용)
# GET  : 기존 값 그대로 불러와서 폼에 채워서 보여줌
# POST : 수정 내용 저장
# ------------------------------------------------
@bp.route('/edit/<int:join_id>', methods=['GET', 'POST'])
def join_edit(join_id):
    if g.user is None:
        return redirect(url_for('auth.login', next=request.path))

    join = Join.query.get_or_404(join_id)

    # 작성자 본인이 아니면 접근 불가
    if join.writer_id != g.user.id:
        return redirect(url_for('join.join_list'))

    # 신청자 목록 (취소 버튼과 함께 화면에 표시)
    applies = JoinApply.query.filter_by(join_id=join.id).all()

    if request.method == 'POST':
        new_recruit_count = int(request.form['recruit_count']) if request.form.get('recruit_count') else join.recruit_count

        # 모집 인원을 이미 신청한 인원보다 적게 줄이는 것 방지
        if new_recruit_count < join.filled_count:
            return render_template(
                'join/join_edit.html',
                join=join,
                applies=applies,
                error='이미 신청한 인원(' + str(join.filled_count) + '명)보다 적게 설정할 수 없습니다.'
            )

        join.course_name = request.form['course_name']
        join.region = request.form.get('region', join.region)
        join.round_date = datetime.strptime(request.form['round_date'], '%Y-%m-%d').date()
        join.tee_time = request.form['tee_time']
        join.course_info = request.form['course_info']
        join.cost = int(request.form['cost']) if request.form['cost'] else join.cost
        join.recruit_count = new_recruit_count
        join.gender_condition = request.form.get('gender_condition', join.gender_condition)
        join.title = request.form['title']
        join.content = request.form['content']

        # 새 이미지를 다시 검색해서 선택한 경우에만 갱신 (안 바꿨으면 기존 유지)
        new_thumb = request.form.get('thumb_img_url')
        if new_thumb:
            join.thumb_img = new_thumb

        db.session.commit()
        return redirect(url_for('join.join_list'))

    return render_template('join/join_edit.html', join=join, applies=applies, error=None)


# ------------------------------------------------
# 조인 글 삭제 (작성자 전용, 신청자가 없을 때만 가능)
# ------------------------------------------------
@bp.route('/delete/<int:join_id>', methods=['POST'])
def join_delete(join_id):
    if g.user is None:
        return redirect(url_for('auth.login', next=request.path))

    join = Join.query.get_or_404(join_id)

    if join.writer_id != g.user.id:
        return redirect(url_for('join.join_list'))

    applies_count = JoinApply.query.filter_by(join_id=join.id).count()
    if applies_count > 0:
        # 신청자가 있으면 삭제 불가 (화면에서도 버튼 비활성화하지만, 서버에서도 한 번 더 방어)
        return redirect(url_for('join.join_edit', join_id=join.id))

    db.session.delete(join)
    db.session.commit()
    return redirect(url_for('join.join_list'))


# ------------------------------------------------
# 신청자 개별 취소 (작성자 전용)
# ------------------------------------------------
@bp.route('/cancel_applicant/<int:apply_id>', methods=['POST'])
def cancel_applicant(apply_id):
    if g.user is None:
        return redirect(url_for('auth.login', next=request.path))

    apply_record = JoinApply.query.get_or_404(apply_id)
    join = Join.query.get_or_404(apply_record.join_id)

    # 이 조인 글의 작성자만 취소 가능
    if join.writer_id != g.user.id:
        return redirect(url_for('join.join_list'))

    db.session.delete(apply_record)

    # 참가자 수 다시 계산 (음수 방지)
    if join.filled_count > 0:
        join.filled_count -= 1

    db.session.commit()
    return redirect(url_for('join.join_edit', join_id=join.id))

from par3.models import Join, User, JoinApply, JoinLike

# ------------------------------------------------
# 좋아요(관심목록) 토글 API
# 접속 주소: POST /join/api/toggle_like/<join_id>
# 이미 눌렀으면 취소(삭제), 안 눌렀으면 추가
# ------------------------------------------------
@bp.route('/api/toggle_like/<int:join_id>', methods=['POST'])
def toggle_like(join_id):
    if g.user is None:
        return {'error': '로그인이 필요합니다.'}, 401

    existing = JoinLike.query.filter_by(join_id=join_id, user_id=g.user.id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        return {'liked': False}
    else:
        new_like = JoinLike(join_id=join_id, user_id=g.user.id)
        db.session.add(new_like)
        db.session.commit()
        return {'liked': True}