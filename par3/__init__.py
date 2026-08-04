from flask import Flask, g, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import config

db = SQLAlchemy()
migrate = Migrate()

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

    # 블루프린트 등록
    from .views import main_views, join_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(join_views.bp)

    # 필터 등록


    # 전역 함수 등록

    # g.user 확인 함수
    from .models import User
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User.query.get(user_id)

    return app