# join_views.py
# ============================================
# PAR3 - JOIN (실시간 골프 조인 리스트) 라우트
# 담당: 오지 (feature/join-page)
# 연결 템플릿: templates/join.html
# ============================================

from flask import Blueprint, redirect, render_template, request, url_for
from par3.models import Join, User
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
    joins = Join.query.order_by(Join.round_date.asc()).all()

    today = date.today()
    weekday_kr = ['월', '화', '수', '목', '금', '토', '일']
    for j in joins:
        j.dday = (j.round_date - today).days
        j.weekday = weekday_kr[j.round_date.weekday()]
        writer = User.query.get(j.writer_id)
        j.writer_nickname = writer.nickname if writer else '알 수 없음'

    return render_template('join/join.html', joins=joins)

# ------------------------------------------------
# 조인 개설(모집) 폼 페이지
# 접속 주소: /join/create
# ------------------------------------------------
@bp.route('/create', methods=['GET', 'POST'])
def join_create():
    if request.method == 'POST':
        # ⚠️ TODO: 로그인 기능 연동 후 session에서 실제 로그인한 사용자 id 가져오기
        # 지금은 임시로 첫 번째 회원(id=1)을 작성자로 고정
        temp_user = User.query.first()

        new_join = Join(
            writer_id=temp_user.id if temp_user else 1,
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
        )
        db.session.add(new_join)
        db.session.commit()
        return redirect(url_for('join.join_list'))

    return render_template('join/join_create.html')
# ------------------------------------------------
# 조인 참가 신청 폼 페이지
# 접속 주소: /join/apply
# ------------------------------------------------
@bp.route('/apply')
def join_apply():
    return render_template('join/join_apply.html')