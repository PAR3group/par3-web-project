# join_views.py
# ============================================
# PAR3 - JOIN (실시간 골프 조인 리스트) 라우트
# 담당: 오지 (feature/join-page)
# 연결 템플릿: templates/join.html
# ============================================

from flask import Blueprint, render_template

# 'join' 이라는 이름의 블루프린트 생성
# url_prefix='/join' → 이 블루프린트 안의 모든 라우트는 앞에 자동으로 /join 이 붙음
bp = Blueprint('join', __name__, url_prefix='/join')


# ------------------------------------------------
# 조인 페이지 (골프 모임 목록 화면)
# 접속 주소: /join/
# ------------------------------------------------
@bp.route('/')
def join_list():
    # 현재는 정적 데이터로 화면만 구현한 상태
    # ⚠️ TODO: DB 연동 시 models.py에서 Join 데이터 조회해서 join.html에 넘겨줄 예정
    # 예시: joins = Join.query.all()
    #      return render_template('join.html', joins=joins)
    return render_template('join/join.html')

# ------------------------------------------------
# 조인 개설(모집) 폼 페이지
# 접속 주소: /join/create
# ------------------------------------------------
@bp.route('/create')
def join_create():
    return render_template('join/join_create.html')

# ------------------------------------------------
# 조인 참가 신청 폼 페이지
# 접속 주소: /join/apply
# ------------------------------------------------
@bp.route('/apply')
def join_apply():
    return render_template('join/join_apply.html')