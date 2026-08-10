function checkSearch(form) {
    // 공백만 입력했거나 아무것도 입력 안 했을 때 검사
    if (!form.keyword.value.trim()) {
        alert('검색어를 입력해 주세요');
        form.keyword.focus();
        return false; // 폼 제출 중단
    }
    return true; // 정상 제출
}

(function () {
    const wrapper = document.querySelector('.content-body-wrapper');
    const sidebar = document.querySelector('.right-sidebar');
    if (!wrapper || !sidebar) return;

    const TOP_GAP = 80;       // 원래 top: 80px 값
    const EASE = 0.08;        // 작을수록 더 느긋하게 따라옴 (0.05~0.15 추천)

    let current = 0;
    let raf = null;

    function update() {
        const wrapperRect = wrapper.getBoundingClientRect();
        const maxTranslate = Math.max(wrapper.offsetHeight - sidebar.offsetHeight, 0);

        // sticky였다면 이 순간 있었을 위치(목표값)
        let target = -wrapperRect.top + TOP_GAP;
        target = Math.max(0, Math.min(target, maxTranslate));

        current += (target - current) * EASE;

        // 목표와 거의 같아지면 스냅해서 미세한 떨림 방지
        if (Math.abs(target - current) < 0.5) current = target;

        sidebar.style.transform = `translateY(${current}px)`;

        raf = requestAnimationFrame(update);
    }

    raf = requestAnimationFrame(update);
})();