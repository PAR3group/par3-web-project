/* =========================================
   1. 게시글 상세페이지 이동
========================================= */
function goDetail(id) {
    location.href = '/talk/' + id;
}


/* =========================================
   2. 검색어 검사
========================================= */
function checkSearch(form) {

    // 공백만 입력했거나 아무것도 입력 안 했을 때 검사
    if (!form.keyword.value.trim()) {
        alert('검색어를 입력해 주세요');
        form.keyword.focus();
        return false;
    }

    return true;
}


/* =========================================
   3. 오른쪽 KLPGA / KPGA 사이드바 따라오기
========================================= */
(function () {

    const wrapper = document.querySelector('.content-body-wrapper');
    const sidebar = document.querySelector('.right-sidebar');
    const stickyHeader = document.querySelector('.talk-sticky-header');

    // 필요한 요소가 없으면 실행하지 않음
    if (!wrapper || !sidebar) return;


    /* 따라오는 움직임 속도 */
    const EASE = 0.08;

    let current = 0;
    let raf = null;


    /* =========================================
       상단 고정 영역의 실제 높이 계산
    ========================================= */
    function getTopGap() {

    if (!stickyHeader) {
        return 90;
    }

    // talk-sticky-header의 top 값(메인 헤더 높이)까지 자동 계산
    const stickyTop =
        parseFloat(
            window.getComputedStyle(stickyHeader).top
        ) || 0;

    return stickyTop + stickyHeader.offsetHeight + 10;
}


    /* =========================================
       992px 이하인지 확인
    ========================================= */
    function isMobile() {
        return window.innerWidth <= 992;
    }


    /* =========================================
       사이드바가 이동할 목표 위치 계산
    ========================================= */
    function getTarget() {

        const wrapperTop =
            wrapper.getBoundingClientRect().top + window.scrollY;

        const maxTranslate =
            Math.max(
                wrapper.offsetHeight - sidebar.offsetHeight,
                0
            );

        const topGap = getTopGap();

        let target =
            window.scrollY - wrapperTop + topGap;

        return Math.max(
            0,
            Math.min(target, maxTranslate)
        );
    }


    /* =========================================
       사이드바 부드럽게 이동
    ========================================= */
    function tick() {

        // 992px 이하에서는 따라다니기 해제
        if (isMobile()) {

            sidebar.style.transform = 'none';

            current = 0;
            raf = null;

            return;
        }


        const target = getTarget();

        // 부드럽게 목표 위치로 이동
        current += (target - current) * EASE;


        // 목표 위치에 거의 도착하면 정확하게 맞춤
        if (Math.abs(target - current) < 0.5) {
            current = target;
        }


        sidebar.style.transform =
            `translateY(${current}px)`;


        // 아직 목표 위치에 도착하지 않았다면 계속 이동
        if (Math.abs(target - current) > 0.5) {

            raf = requestAnimationFrame(tick);

        } else {

            raf = null;
        }
    }


    /* =========================================
       애니메이션 실행 요청
    ========================================= */
    function requestTick() {

        if (!raf) {
            raf = requestAnimationFrame(tick);
        }
    }


    /* =========================================
       스크롤할 때 실행
    ========================================= */
    window.addEventListener(
        'scroll',
        requestTick,
        { passive: true }
    );


    /* =========================================
       화면 크기가 변경될 때 실행
    ========================================= */
    window.addEventListener(
        'resize',
        function () {

            // 992px 이하가 되면 이동 위치 초기화
            if (isMobile()) {

                sidebar.style.transform = 'none';
                current = 0;
            }

            requestTick();
        }
    );


    /* 처음 페이지를 열었을 때 한 번 실행 */
    requestTick();

})();