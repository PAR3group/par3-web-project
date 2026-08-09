# join_views.py
# ============================================
# PAR3 - JOIN (실시간 골프 조인 리스트) 라우트
# 담당: 오지 (feature/join-page)
# 연결 템플릿: templates/join.html
# ============================================

from flask import Blueprint, redirect, render_template, request, url_for,g
from par3.models import Join, JoinApply, User
from par3 import db
from datetime import date, datetime

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
        else:
            j.is_owner = False
            j.is_applied = False

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

    if request.method == 'POST':
        new_apply = JoinApply(
            join_id=join.id,
            applicant_id=applicant.id,
            applicant_name=applicant.nickname,
            applicant_phone=applicant.phonenumber,
            experience_years=request.form.get('experience_years', ''),
            handicap=request.form.get('handicap', ''),
        )
        db.session.add(new_apply)

        if join.filled_count < join.recruit_count:
            join.filled_count += 1

        db.session.commit()
        return redirect(url_for('join.join_list'))

    return render_template('join/join_apply.html', join=join, applicant=applicant)

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