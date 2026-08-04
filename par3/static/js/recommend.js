document.addEventListener('DOMContentLoaded', function () {
    const toggles = document.querySelectorAll('.rc_club_toggle');

    function syncBox(toggle) {
        const targetId = toggle.getAttribute('data-target');
        const box = document.getElementById(targetId);
        if (!box) return;

        const input = box.querySelector('input');

        if (toggle.checked) {
            box.classList.add('rc_distance_box--active');
            if (input) input.setAttribute('required', 'required');
        } else {
            box.classList.remove('rc_distance_box--active');
            if (input) {
                input.removeAttribute('required');
                input.value = ''; // 체크 해제 시 값도 같이 초기화 (혼동 방지)
            }
        }
    }

    toggles.forEach(function (toggle) {
        syncBox(toggle); // 새로고침/뒤로가기 시 체크 상태 복원 대응
        toggle.addEventListener('change', function () {
            syncBox(toggle);
        });
    });

    // 스윙스피드 모르겠어요 체크박스
    const unknownCheckbox = document.getElementById('swing-speed-unknown');
    const speedInput = document.getElementById('swing-speed-input');

    function syncSpeedInput() {
        if (!unknownCheckbox || !speedInput) return;

        if (unknownCheckbox.checked) {
            speedInput.value = '';
            speedInput.disabled = true;
        } else {
            speedInput.disabled = false;
        }
    }

    if (unknownCheckbox) {
        syncSpeedInput();
        unknownCheckbox.addEventListener('change', syncSpeedInput);
    }
});