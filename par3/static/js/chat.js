document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.c_room');
    if (!container) return;

    const joinId = parseInt(container.dataset.joinId, 10);
    const myUserId = parseInt(container.dataset.userId, 10);
    const messagesEl = document.getElementById('c_messages');
    const form = document.getElementById('c_form');
    const input = document.getElementById('c_input');
    const notice = document.getElementById('c_notice');
    const noticeToggle = document.getElementById('c_notice_toggle');

    const socket = io();

    // 라운드 안내 배너 접기/펴기 (방마다 상태 기억)
    const noticeStorageKey = `c_notice_collapsed_${joinId}`;
    if (notice) {
        if (localStorage.getItem(noticeStorageKey) === '1') {
            notice.classList.add('c_notice--collapsed');
        }
        noticeToggle.addEventListener('click', () => {
            notice.classList.toggle('c_notice--collapsed');
            localStorage.setItem(noticeStorageKey, notice.classList.contains('c_notice--collapsed') ? '1' : '0');
        });
    }

    function appendMessage({ sender_id, sender_nickname, message, created_at }) {
        const div = document.createElement('div');
        div.className = 'c_msg' + (sender_id === myUserId ? ' c_msg--mine' : '');

        const nick = document.createElement('span');
        nick.className = 'c_msg_nick';
        nick.textContent = sender_nickname;

        const row = document.createElement('div');
        row.className = 'c_msg_row';

        const bubble = document.createElement('span');
        bubble.className = 'c_msg_bubble';
        bubble.textContent = message;

        const time = document.createElement('span');
        time.className = 'c_msg_time';
        time.textContent = created_at;

        row.appendChild(bubble);
        row.appendChild(time);
        div.appendChild(nick);
        div.appendChild(row);

        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function appendSystemMessage(text) {
        const div = document.createElement('div');
        div.className = 'c_msg_system';
        div.textContent = text;
        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    // 1) 과거 메시지 로드 (REST)
    fetch(`/join/${joinId}/messages`)
        .then(res => res.json())
        .then(history => {
            if (Array.isArray(history)) {
                history.forEach(appendMessage);
            }
        });

    // 2) 소켓 연결 + 방 입장
    socket.emit('join', { join_id: joinId });

    socket.on('receive_message', appendMessage);
    socket.on('system_message', (data) => appendSystemMessage(data.msg));
    socket.on('error', (data) => alert(data.msg));

    // 3) 메시지 전송
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        socket.emit('send_message', { join_id: joinId, message: text });
        input.value = '';
    });

    // 4) 페이지 이탈 시 방 퇴장
    window.addEventListener('beforeunload', () => {
        socket.emit('leave', { join_id: joinId });
    });
});
