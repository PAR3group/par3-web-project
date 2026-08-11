# chat_views.py
# ============================================
# PAR3 - 조인 채팅 라우트
# 연결 템플릿: templates/join/chat_rooms.html, templates/join/chat.html
# ============================================

from flask import Blueprint, render_template, jsonify, g, redirect, url_for, flash
from par3.models import Join, JoinApply, ChatMessage, User
from par3 import db

bp = Blueprint('chat', __name__, url_prefix='/join')

DEFAULT_PROFILE_IMG = "https://raw.githubusercontent.com/feathericons/feather/master/icons/user.svg"


def _check_participant(join_id):
    """로그인 + 해당 join 참여자(작성자 포함) 여부 확인"""
    if g.user is None:
        return False
    return JoinApply.query.filter_by(
        join_id=join_id, applicant_id=g.user.id
    ).first() is not None


# ------------------------------------------------
# 내 채팅방 목록 (헤더 드롭다운에서 진입)
# ------------------------------------------------
@bp.route('/chat')
def my_chat_rooms():
    if g.user is None:
        flash('로그인이 필요합니다.')
        return redirect(url_for('auth.login'))

    applied_join_ids = [
        a.join_id for a in JoinApply.query.filter_by(applicant_id=g.user.id).all()
    ]
    rooms = Join.query.filter(Join.id.in_(applied_join_ids)) \
        .order_by(Join.round_date.desc()).all() if applied_join_ids else []

    for room in rooms:
        writer = User.query.get(room.writer_id)
        room.writer_nickname = writer.nickname if writer else '알 수 없음'

    return render_template('join/chat_rooms.html', rooms=rooms)


# ------------------------------------------------
# 채팅방 페이지 (참여자만 접근 가능)
# ------------------------------------------------
@bp.route('/<int:join_id>/chat')
def chat_room(join_id):
    join = Join.query.get_or_404(join_id)

    if not _check_participant(join_id):
        flash('참여자만 채팅방에 입장할 수 있습니다.')
        return redirect(url_for('join.join_list'))

    writer = User.query.get(join.writer_id)
    join.writer_nickname = writer.nickname if writer else '알 수 없음'

    return render_template('join/chat.html', join=join)


# ------------------------------------------------
# 과거 메시지 조회 (페이지 최초 진입시 REST로 로드)
# ------------------------------------------------
@bp.route('/<int:join_id>/messages')
def chat_messages(join_id):
    if not _check_participant(join_id):
        return jsonify({'error': 'forbidden'}), 403

    messages = ChatMessage.query.filter_by(join_id=join_id) \
        .order_by(ChatMessage.created_at.asc()).all()

    return jsonify([{
        'sender_id': m.sender_id,
        'sender_nickname': m.sender.nickname,
        'sender_profile_img': m.sender.profile_img or DEFAULT_PROFILE_IMG,
        'message': m.message,
        'created_at': m.created_at.strftime('%H:%M'),
    } for m in messages])
