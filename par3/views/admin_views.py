from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from sqlalchemy import extract, func

from par3 import db
from par3.models import Comment, Join, JoinApply, PageVisit, Post, User
from par3.views.auth_views import admin_required
from par3.views.mypage_views import GOLF_EXPERIENCE_LABELS

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@admin_required
def dashboard():
    rows = (
        db.session.query(
            extract('hour', PageVisit.created_at).label('hour'),
            func.count(PageVisit.id),
        )
        .group_by('hour')
        .all()
    )

    hourly_counts = [0] * 24
    for hour, count in rows:
        if hour is not None:
            hourly_counts[int(hour)] = count

    return render_template('admin/dashboard.html', hourly_counts=hourly_counts)


# ------------------------------------------------
# 회원 관리
# ------------------------------------------------
@bp.route('/members')
@admin_required
def members():
    q = request.args.get('q', '').strip()
    query = User.query
    if q:
        like = f'%{q}%'
        query = query.filter(
            User.nickname.ilike(like)
            | User.user_id.ilike(like)
            | User.username.ilike(like)
            | User.email.ilike(like)
            | User.phonenumber.ilike(like)
        )
    users = query.order_by(User.id.asc()).all()
    for u in users:
        u.experience_label = GOLF_EXPERIENCE_LABELS.get(u.experience_years, f'{u.experience_years}년차')
    return render_template('admin/members.html', users=users, q=q)


@bp.route('/members/<int:id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)

    if user.id == g.user.id:
        flash('본인 계정의 관리자 권한은 변경할 수 없습니다.')
        return redirect(url_for('admin.members'))

    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'{user.nickname}님을 {"관리자로 지정" if user.is_admin else "일반회원으로 변경"}했습니다.')
    return redirect(url_for('admin.members'))


@bp.route('/members/<int:id>/toggle-suspend', methods=['POST'])
@admin_required
def toggle_suspend(id):
    user = User.query.get_or_404(id)

    if user.id == g.user.id:
        flash('본인 계정은 정지할 수 없습니다.')
        return redirect(url_for('admin.members'))

    user.is_suspended = not user.is_suspended
    db.session.commit()
    flash(f'{user.nickname}님을 {"정지" if user.is_suspended else "정지 해제"}했습니다.')
    return redirect(url_for('admin.members'))


@bp.route('/members/<int:id>/toggle-withdraw', methods=['POST'])
@admin_required
def toggle_withdraw(id):
    user = User.query.get_or_404(id)

    if user.id == g.user.id:
        flash('본인 계정은 강제 탈퇴시킬 수 없습니다.')
        return redirect(url_for('admin.members'))

    user.is_withdrawn = not user.is_withdrawn
    db.session.commit()
    flash(f'{user.nickname}님을 {"강제 탈퇴" if user.is_withdrawn else "탈퇴 취소"} 처리했습니다.')
    return redirect(url_for('admin.members'))


# ------------------------------------------------
# 게시글(talk 커뮤니티) 관리
# ------------------------------------------------
@bp.route('/posts')
@admin_required
def posts():
    q = request.args.get('q', '').strip()
    query = Post.query
    if q:
        like = f'%{q}%'
        query = query.filter(
            Post.title.ilike(like)
            | Post.content.ilike(like)
            | Post.author.ilike(like)
        )
    posts = query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts, q=q)


@bp.route('/posts/<int:id>/delete', methods=['POST'])
@admin_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)  # 댓글은 cascade='all, delete-orphan' 으로 함께 삭제됨
    db.session.commit()
    flash('게시글을 삭제했습니다.')
    return redirect(url_for('admin.posts'))


@bp.route('/comments/<int:id>/delete', methods=['POST'])
@admin_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('댓글을 삭제했습니다.')
    return redirect(url_for('admin.posts'))


# ------------------------------------------------
# 조인(골프 조인) 관리
# ------------------------------------------------
@bp.route('/joins')
@admin_required
def joins():
    q = request.args.get('q', '').strip()
    query = Join.query
    if q:
        like = f'%{q}%'
        matched_writer_ids = [
            u.id for u in User.query.filter(User.nickname.ilike(like)).all()
        ]
        query = query.filter(
            Join.title.ilike(like)
            | Join.course_name.ilike(like)
            | Join.region.ilike(like)
            | Join.writer_id.in_(matched_writer_ids)
        )
    joins = query.order_by(Join.create_date.desc()).all()
    writer_ids = {j.writer_id for j in joins}
    writers = {u.id: u for u in User.query.filter(User.id.in_(writer_ids)).all()} if writer_ids else {}
    for j in joins:
        writer = writers.get(j.writer_id)
        j.writer_nickname = writer.nickname if writer else '알 수 없음'
    return render_template('admin/joins.html', joins=joins, q=q)


@bp.route('/joins/<int:id>/delete', methods=['POST'])
@admin_required
def delete_join(id):
    join = Join.query.get_or_404(id)
    JoinApply.query.filter_by(join_id=join.id).delete()
    db.session.delete(join)
    db.session.commit()
    flash('조인 게시글을 삭제했습니다.')
    return redirect(url_for('admin.joins'))
