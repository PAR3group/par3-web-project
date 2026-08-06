import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, g, abort

from par3.models import Post, Comment          # [수정] 실제 models.py 경로에 맞게 조정
from par3.views.auth_views import login_required            # [수정] 기존 login_required 재사용
from par3 import db

bp = Blueprint('talk', __name__, url_prefix='/talk')

VIDEO_EXTENSIONS = ('.mp4', '.webm', '.ogg', '.mov', '.m4v', '.avi')


# [추가] API용 로그인 체크 - fetch로 호출되는 라우트는 리다이렉트 대신 JSON으로 응답해야 함
def api_login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return jsonify({'success': False, 'need_login': True}), 401
        return view(*args, **kwargs)
    return wrapped_view


@bp.route('/')
def list():
    # [참고] 정렬/카테고리/검색 조건 처리
    sort = request.args.get('sort', 'latest')
    category = request.args.get('category')
    keyword = request.args.get('keyword')

    query = Post.query

    if category and category != '전체':
        query = query.filter_by(category=category)

    if keyword:
        query = query.filter(Post.title.contains(keyword) | Post.content.contains(keyword))

    if sort == 'popular':
        query = query.order_by(Post.likes.desc())
    else:
        query = query.order_by(Post.created_at.desc())

    posts = query.all()

    return render_template(
        'talk.html',
        posts=posts,
        current_sort=sort,
        current_category=category
    )


@bp.route('/write', methods=['GET', 'POST'])
@login_required  # [추가] 글쓰기는 로그인 필요, 페이지 이동 방식이라 리다이렉트형 사용
def write():
    if request.method == 'GET':
        return render_template('talk_write.html')

    category = request.form.get('category')
    title = request.form.get('title')
    content = request.form.get('content')
    author = request.form.get('author') or '골프인'

    files = request.files.getlist('media')
    image_url = None
    is_video = False

    # [참고] 여러 파일 첨부 가능하지만, 현재 모델 구조상 대표 이미지 1개만 저장
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1] if '.' in filename else ''
            filename = f"{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join('static', 'uploads', filename)
            file.save(save_path)

            image_url = url_for('static', filename=f'uploads/{filename}')
            is_video = filename.lower().endswith(VIDEO_EXTENSIONS)
            break  # 첫 번째 파일만 대표로 저장

    new_post = Post(
        category=category,
        title=title,
        content=content,
        author=author,
        image_url=image_url,
        is_video=is_video,
        views=0,
        likes=0,
    )
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('talk.list'))


@bp.route('/<int:id>')
def detail(id):
    post = Post.query.get_or_404(id)
    post.views = (post.views or 0) + 1  # [참고] 상세페이지 진입 시 조회수 증가
    db.session.commit()
    return render_template('talk_post.html', post=post)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required  # [추가] 삭제는 로그인 필요
def delete_post(id):
    post = Post.query.get_or_404(id)

    # [추가] 작성자 본인만 삭제 가능
    if post.author != g.user.nickname:
        return jsonify({'success': False, 'message': '삭제 권한이 없습니다.'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True})


@bp.route('/<int:id>/like', methods=['POST'])
@api_login_required  # [추가] 좋아요는 API라 JSON 응답형 사용
def like_post(id):
    post = Post.query.get_or_404(id)
    post.likes = (post.likes or 0) + 1
    db.session.commit()
    return jsonify({'success': True, 'likes': post.likes})


@bp.route('/<int:id>/comment', methods=['POST'])
@api_login_required  # [추가] 댓글도 API라 JSON 응답형 사용
def add_comment(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'success': False, 'message': '댓글 내용을 입력해 주세요.'}), 400

    new_comment = Comment(
        post_id=post.id,
        author=g.user.nickname,
        content=content,
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'success': True})