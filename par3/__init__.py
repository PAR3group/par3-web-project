from flask import Flask, g, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from sqlalchemy import MetaData
import config
from par3.filter import format_datetime, format_markdown, format_timeago


migrate = Migrate()
socketio = SocketIO()

# 네이밍 컨벤션(포린키 네임 오류 방지를 위해 작성)
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

def create_app():
    app=Flask(__name__)
    app.config.from_object(config)

    # ORM초기화
    from . import models
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, async_mode='eventlet', cors_allowed_origins="*")

    # 블루프린트 등록
    from .views import main_views, join_views, auth_views, recommend_views, shop_views, talk_views, mypage_views, admin_views, chat_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(join_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(recommend_views.bp)
    app.register_blueprint(shop_views.bp)
    app.register_blueprint(talk_views.bp)
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(admin_views.bp)
    app.register_blueprint(chat_views.bp)

    # 조인 채팅 소켓 이벤트 핸들러 등록
    from . import sockets

    # 필터 등록
    # datetime_filter
    app.jinja_env.filters['datetime']=format_datetime
    # 2. Flask 앱의 Jinja2 템플릿 필터로 등록합니다. (필터 이름: 'markdown')
    app.jinja_env.filters['markdown']=format_markdown
    app.jinja_env.filters['timeago']=format_timeago

    # 전역 함수 등록
    # g.user 확인 함수
    from .models import User, PageVisit
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            user = User.query.get(user_id)
            # 정지/강제 탈퇴된 회원은 세션을 즉시 무효화
            if user is not None and (user.is_suspended or user.is_withdrawn):
                session.clear()
                user = None
            g.user = user

    # 관리자 페이지 접속 시간대 통계용 방문 로그 (정적 파일/관리자 페이지 자체는 제외)
    @app.before_request
    def log_page_visit():
        if request.method != 'GET' or request.endpoint is None:
            return
        if request.endpoint == 'static' or request.endpoint.startswith('admin.'):
            return
        db.session.add(PageVisit(
            user_id=g.user.id if g.user else None,
            path=request.path,
        ))
        db.session.commit()


    app.config['WTF_CSRF_ENABLED'] = True
    # 개발 단계 동안 CSRF 기능 잠시 끄기
    
    return app
