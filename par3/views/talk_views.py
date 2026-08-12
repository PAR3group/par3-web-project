from flask import Blueprint, render_template, request, redirect, url_for, jsonify, g, abort

from par3.models import Post, Comment, User          # [수정] 실제 models.py 경로에 맞게 조정
from par3.views.auth_views import login_required            # [수정] 기존 login_required 재사용
from par3 import db, storage
from par3.utils import get_golf_news_top3

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
    prize_top3, kpga_top3 = get_golf_news_top3()

    return render_template(
        'talk.html',
        posts=posts,
        current_sort=sort,
        current_category=category,
        prize_top3=prize_top3,
        kpga_top3=kpga_top3
    )


@bp.route('/write', methods=['GET', 'POST'])
@login_required  # [추가] 글쓰기는 로그인 필요, 페이지 이동 방식이라 리다이렉트형 사용
def write():
    if request.method == 'GET':
        return render_template('talk-form.html')

    category = request.form.get('category')
    title = request.form.get('title')
    content = request.form.get('content')
    author = request.form.get('author') or '골프인'

    files = request.files.getlist('media')
    image_url = url_for('static', filename='img/PAR3-AMB.png')
    is_video = False

    for file in files:
        if file and file.filename:
            is_video = file.filename.lower().endswith(VIDEO_EXTENSIONS)
            image_url = storage.upload_image(file, 'talk')
            break

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

    post.views = (post.views or 0) + 1
    db.session.commit()

    # 댓글 작성자의 프로필 사진 연결
    for comment in post.comments_list:
        comment_user = User.query.filter_by(
            nickname=comment.author
        ).first()

        comment.profile_img = (
            comment_user.profile_img
            if comment_user and comment_user.profile_img
            else None
        )

        # 대댓글 프로필 사진도 연결
        # for reply in comment.replies:
        #     reply_user = User.query.filter_by(
        #         nickname=reply.author
        #     ).first()

        #     reply.profile_img = (
        #         reply_user.profile_img
        #         if reply_user and reply_user.profile_img
        #         else None
        #     )

    return render_template(
        'talk-detail.html',
        post=post
    )

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)

    # 본인이 작성한 게시글만 수정 가능
    if post.author != g.user.nickname:
        abort(403)

    # 수정 화면 열기
    if request.method == 'GET':
        return render_template('talk-form.html', post=post, edit_mode=True)

    # 수정 내용 저장
    post.category = request.form.get('category')
    post.title = request.form.get('title')
    post.content = request.form.get('content')

    # 새 사진/동영상을 선택했을 경우에만 기존 파일 교체
    file = request.files.get('media')

    if file and file.filename:
        post.is_video = file.filename.lower().endswith(VIDEO_EXTENSIONS)
        post.image_url = storage.upload_image(file, 'talk')

    db.session.commit()

    return redirect(url_for('talk.detail', id=post.id))


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)

    if post.author != g.user.nickname:
        return jsonify({'success': False, 'message': '삭제 권한이 없습니다.'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True})


@bp.route('/<int:id>/like', methods=['POST'])
@api_login_required
def like_post(id):
    post = Post.query.get_or_404(id)
    post.likes = (post.likes or 0) + 1
    db.session.commit()
    return jsonify({'success': True, 'likes': post.likes})


@bp.route('/<int:id>/comment', methods=['POST'])
@api_login_required
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

# ======================================================
# 대댓글 등록
# ======================================================

@bp.route('/<int:id>/comment/<int:parent_id>/reply', methods=['POST'])
@api_login_required
def add_reply(id, parent_id):
    post = Post.query.get_or_404(id)
    parent_comment = Comment.query.get_or_404(parent_id)

    # 다른 게시글의 댓글에 잘못 대댓글이 달리는 것 방지
    if parent_comment.post_id != post.id:
        return jsonify({
            'success': False,
            'message': '잘못된 댓글입니다.'
        }), 400

    data = request.get_json()
    content = data.get('content', '').strip()

    if not content:
        return jsonify({
            'success': False,
            'message': '답글 내용을 입력해 주세요.'
        }), 400

    new_reply = Comment(
        post_id=post.id,
        parent_id=parent_comment.id,
        author=g.user.nickname,
        content=content
    )

    db.session.add(new_reply)
    db.session.commit()

    return jsonify({'success': True})

# 댓글 수정
@bp.route('/comment/<int:comment_id>/edit', methods=['POST'])
@api_login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.author != g.user.nickname:
        return jsonify({
            'success': False,
            'message': '수정 권한이 없습니다.'
        }), 403

    data = request.get_json()
    content = data.get('content', '').strip()

    if not content:
        return jsonify({
            'success': False,
            'message': '댓글 내용을 입력해 주세요.'
        }), 400

    comment.content = content
    db.session.commit()

    return jsonify({'success': True})

# 댓글 삭제
@bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@api_login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.author != g.user.nickname:
        return jsonify({
            'success': False,
            'message': '삭제 권한이 없습니다.'
        }), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'success': True})