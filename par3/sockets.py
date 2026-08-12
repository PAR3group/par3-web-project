# sockets.py
# ============================================
# PAR3 - 조인 채팅 SocketIO 이벤트
# ============================================

from flask import session
from flask_socketio import join_room, leave_room, emit
from par3 import socketio, db
from par3.models import JoinApply, ChatMessage, User

DEFAULT_PROFILE_IMG = "https://raw.githubusercontent.com/feathericons/feather/master/icons/user.svg"


def _get_current_user():
    user_id = session.get('user_id')
    if user_id is None:
        return None
    return User.query.get(user_id)


def _is_participant(join_id, user_id):
    return JoinApply.query.filter_by(
        join_id=join_id, applicant_id=user_id
    ).first() is not None


@socketio.on('join')
def handle_join(data):
    join_id = data.get('join_id')
    user = _get_current_user()
    print(f'[DEBUG] join 이벤트 수신 - join_id={join_id}, user={user}')

    if user is None or not _is_participant(join_id, user.id):
        print('[DEBUG] join 거부됨 - 참여자 아님 또는 로그인 안 됨')
        emit('error', {'msg': '참여자만 입장 가능합니다.'})
        return

    room = f'join_{join_id}'
    join_room(room)
    print(f'[DEBUG] {user.nickname}님이 room={room} 입장 완료')
    emit('system_message', {'msg': f'{user.nickname}님이 입장했습니다.'}, room=room)


@socketio.on('leave')
def handle_leave(data):
    join_id = data.get('join_id')
    user = _get_current_user()
    room = f'join_{join_id}'
    leave_room(room)
    if user:
        emit('system_message', {'msg': f'{user.nickname}님이 퇴장했습니다.'}, room=room)


@socketio.on('send_message')
def handle_send_message(data):
    join_id = data.get('join_id')
    text = (data.get('message') or '').strip()
    user = _get_current_user()
    print(f'[DEBUG] send_message 이벤트 수신 - join_id={join_id}, user={user}, text={text!r}')

    if user is None or not _is_participant(join_id, user.id):
        print('[DEBUG] send_message 거부됨 - 참여자 아님 또는 로그인 안 됨')
        emit('error', {'msg': '참여자만 메시지를 보낼 수 있습니다.'})
        return
    if not text:
        print('[DEBUG] send_message 무시됨 - 빈 텍스트')
        return

    new_message = ChatMessage(join_id=join_id, sender_id=user.id, message=text)
    db.session.add(new_message)
    db.session.commit()

    room = f'join_{join_id}'
    print(f'[DEBUG] room={room}에 receive_message 브로드캐스트')
    emit('receive_message', {
        'sender_id': user.id,
        'sender_nickname': user.nickname,
        'sender_profile_img': user.profile_img or DEFAULT_PROFILE_IMG,
        'message': text,
        'created_at': new_message.created_at.strftime('%H:%M'),
    }, room=room)
