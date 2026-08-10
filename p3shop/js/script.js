// ==========================================
// 공통 버튼 & 로고 자동 생성 전용 script.js
// ==========================================
(function() {
    // 1) 버튼 스타일 생성
    if (!document.getElementById('back-btn-style')) {
        const style = document.createElement('style');
        style.id = 'back-btn-style';
        style.textContent = `
            .back-button-wrapper {
                max-width: 1160px;
                margin: 0 auto 15px auto;
                padding: 0 20px;
                display: flex;
                justify-content: flex-start;
            }
            .btn-back-logo {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 14px;
                background-color: #ffffff;
                border: 1px solid #1b4332;
                border-radius: 20px;
                color: #1b4332;
                font-size: 13px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .btn-back-logo:hover {
                background-color: #1b4332;
                color: #ffffff;
            }
        `;
        document.head.appendChild(style);
    }

    // 2) 로고 불러오기 및 버튼 생성
    function initHeader() {
        // 로고(main1111.html) 로드
        const logoContainer = document.getElementById('logoContainer');
        if (logoContainer && logoContainer.children.length === 0) {
            fetch('main1111.html')
                .then(response => response.text())
                .then(data => { logoContainer.innerHTML = data; })
                .catch(err => console.error('로고 로드 실패:', err));
        }

        // 현재 페이지 파일명 확인
        const path = window.location.pathname;

        // 1. 상세 페이지 여부 확인 (detail.html)
        const isDetailPage = path.includes('detail.html');

        // 2. 메인 페이지 여부 확인 (shop.html, index.html 등)
        const isMainPage = path.endsWith('shop.html') || path.endsWith('index.html') || path.endsWith('/');

        // 3. 버튼 생성 로직
        const header = document.querySelector('header');
        if (header && !document.querySelector('.back-button-wrapper')) {
            
            // ★ 상세페이지(detail.html)는 버튼을 아예 만들지 않고 패스!
            if (isDetailPage) {
                return;
            }

            const wrapper = document.createElement('div');
            wrapper.className = 'back-button-wrapper';

            if (isMainPage) {
                // [메인 페이지] -> 나가기 버튼
                // ★ 'main.html' 자리에 나가기 누르면 이동할 페이지명을 넣으세요.
                wrapper.innerHTML = `
                    <button type="button" class="btn-back-logo" onclick="location.href='main.html'">
                        ‹ 나가기
                    </button>
                `;
            } else {
                // [장바구니, 결제창 등 상세페이지/메인이 아닌 모든 곳] -> 뒤로가기 버튼
                wrapper.innerHTML = `
                    <button type="button" class="btn-back-logo" onclick="history.back()">
                        ‹ 뒤로가기
                    </button>
                `;
            }

            header.parentNode.insertBefore(wrapper, header.nextSibling);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHeader);
    } else {
        initHeader();
    }
})();

// ==========================================
// 양옆 세로형 'GOLF SHOP' 배너 및 스크롤 추적 스크립트
// ==========================================
(function() {
    // 1) 스타일 생성
    if (!document.getElementById('side-golf-banner-style')) {
        const style = document.createElement('style');
        style.id = 'side-golf-banner-style';
        style.textContent = `
            .side-banner {
                position: fixed;
                top: 50%;
                transform: translateY(-50%);
                display: flex;
                align-items: center;
                gap: 12px;
                z-index: 999;
                pointer-events: none; /* 마우스 클릭 방해 방지 */
            }
            .side-banner.left {
                left: 30px;
                flex-direction: row-reverse; /* 선이 바깥쪽, 글자가 안쪽 */
            }
            .side-banner.right {
                right: 30px;
                flex-direction: row; /* 글자가 안쪽, 선이 바깥쪽 */
            }
            /* 초록색 선을 '세로' 방향으로 길쭉하게 설정 */
            .side-banner .side-line {
                width: 2px;
                height: 120px;
                background-color: #00c896;
            }
            /* 글자는 기존 그대로 세로로 눕힘 */
            .side-banner .side-text {
                writing-mode: vertical-rl;
                text-orientation: upright;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 5px;
                color: #333;
                text-transform: uppercase;
                font-family: sans-serif;
            }

            /* 화면이 너무 좁아지면 양옆 배너 숨김 */
            @media (max-width: 1400px) {
                .side-banner {
                    display: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // 2) 좌측 및 우측 배너 생성 및 스크롤 연동 함수
    function initSideBanners() {
        if (document.querySelectorAll('.side-banner').length > 0) return;

        // HTML 구조: 세로 초록색 선 + 세로 글자 ("GOLF SHOP")
        const bannerContent = `
            <div class="side-line"></div>
            <div class="side-text">GOLF SHOP</div>
        `;

        // 좌측 배너
        const leftBanner = document.createElement('div');
        leftBanner.className = 'side-banner left';
        leftBanner.innerHTML = bannerContent;
        document.body.appendChild(leftBanner);

        // 우측 배너
        const rightBanner = document.createElement('div');
        rightBanner.className = 'side-banner right';
        rightBanner.innerHTML = bannerContent;
        document.body.appendChild(rightBanner);

        // 스크롤할 때 부드럽게 살짝 반응하는 효과 (선택사항)
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            const move = scrollY * 0.05; // 스크롤 양에 따라 아주 은은하게 움직임
            leftBanner.style.transform = `translateY(calc(-50% + ${move}px))`;
            rightBanner.style.transform = `translateY(calc(-50% + ${move}px))`;
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSideBanners);
    } else {
        initSideBanners();
    }
})();