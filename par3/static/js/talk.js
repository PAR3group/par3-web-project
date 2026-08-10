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

    if (!form.keyword.value.trim()) {
        alert('검색어를 입력해 주세요');
        form.keyword.focus();
        return false;
    }

    return true;
}


/* =========================================
   3. TALK 고정영역 + 오른쪽 사이드바
========================================= */
(function () {

    const wrapper = document.querySelector('.content-body-wrapper');
    const sidebar = document.querySelector('.right-sidebar');
    const stickyHeader = document.querySelector('.talk-sticky-header');

    /* 팀장님 헤더 안의 nav */
    const mainNav = document.querySelector('.h_nav');

    if (!wrapper || !sidebar || !stickyHeader) return;


    const EASE = 0.08;

    let current = 0;
    let raf = null;


    /* =========================================
       메인 검은색 헤더의 실제 아래 위치 찾기
    ========================================= */
    function getMainHeaderBottom() {

        if (!mainNav) {
            return 0;
        }

        let element = mainNav;
        let headerBottom = mainNav.getBoundingClientRect().bottom;


        /*
         h_nav의 부모들을 위로 올라가면서
         fixed / sticky 요소가 있으면
         그 요소의 실제 아래 위치를 사용
        */
        while (
            element &&
            element !== document.body
        ) {

            const style =
                window.getComputedStyle(element);

            const rect =
                element.getBoundingClientRect();


            if (
                style.position === 'fixed' ||
                style.position === 'sticky'
            ) {

                headerBottom =
                    Math.max(
                        headerBottom,
                        rect.bottom
                    );
            }

            element = element.parentElement;
        }


        return Math.max(headerBottom, 0);
    }


    /* =========================================
       TALK 고정영역을 메인 헤더 바로 아래에 배치
    ========================================= */
    function syncTalkHeaderPosition() {

        const headerBottom =
            getMainHeaderBottom();

        stickyHeader.style.top =
            `${headerBottom}px`;

        return headerBottom;
    }


    /* =========================================
       화면 크기 확인
    ========================================= */
    function isMobile() {
        return window.innerWidth <= 992;
    }


    /* =========================================
       오른쪽 사이드바 목표 위치 계산
    ========================================= */
    function getTarget() {

        const wrapperTop =
            wrapper.getBoundingClientRect().top
            + window.scrollY;


        const maxTranslate =
            Math.max(
                wrapper.offsetHeight
                - sidebar.offsetHeight,
                0
            );


        /*
         실제 메인 헤더 높이
         +
         TALK 고정영역 높이
         +
         10px 여백
        */
        const mainHeaderBottom =
            syncTalkHeaderPosition();


        const topGap =
            mainHeaderBottom
            + stickyHeader.offsetHeight
            + 10;


        let target =
            window.scrollY
            - wrapperTop
            + topGap;


        return Math.max(
            0,
            Math.min(target, maxTranslate)
        );
    }


    /* =========================================
       오른쪽 사이드바 부드럽게 이동
    ========================================= */
    function tick() {

        /* TALK 위치도 항상 다시 계산 */
        syncTalkHeaderPosition();


        /* 992px 이하에서는 사이드바 이동 해제 */
        if (isMobile()) {

            sidebar.style.transform = 'none';

            current = 0;
            raf = null;

            return;
        }


        const target = getTarget();


        current +=
            (target - current) * EASE;


        if (
            Math.abs(target - current) < 0.5
        ) {
            current = target;
        }


        sidebar.style.transform =
            `translateY(${current}px)`;


        if (
            Math.abs(target - current) > 0.5
        ) {

            raf =
                requestAnimationFrame(tick);

        } else {

            raf = null;
        }
    }


    function requestTick() {

        if (!raf) {
            raf =
                requestAnimationFrame(tick);
        }
    }


    /* =========================================
       스크롤
    ========================================= */
    window.addEventListener(
        'scroll',
        requestTick,
        { passive: true }
    );


    /* =========================================
       화면 크기 변경
    ========================================= */
    window.addEventListener(
        'resize',
        function () {

            syncTalkHeaderPosition();

            if (isMobile()) {

                sidebar.style.transform = 'none';
                current = 0;
            }

            requestTick();
        }
    );


    /* 처음 페이지 열었을 때 */
    syncTalkHeaderPosition();
    requestTick();

})();