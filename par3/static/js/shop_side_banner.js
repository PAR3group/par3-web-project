// 쇼핑몰 페이지 좌우 세로형 'GOLF SHOP' 배너 + 스크롤 추적 스크립트
(function () {
    if (document.querySelector('.side-banner')) return;

    const style = document.createElement('style');
    style.textContent = `
        .side-banner {
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 999;
            pointer-events: none;
        }
        .side-banner.left {
            left: 30px;
            flex-direction: row-reverse;
        }
        .side-banner.right {
            right: 30px;
            flex-direction: row;
        }
        .side-banner .side-line {
            width: 2px;
            height: 120px;
            background-color: #00c896;
        }
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
        @media (max-width: 1400px) {
            .side-banner {
                display: none;
            }
        }
    `;
    document.head.appendChild(style);

    const bannerContent = `
        <div class="side-line"></div>
        <div class="side-text">GOLF SHOP</div>
    `;

    const leftBanner = document.createElement('div');
    leftBanner.className = 'side-banner left';
    leftBanner.innerHTML = bannerContent;

    const rightBanner = document.createElement('div');
    rightBanner.className = 'side-banner right';
    rightBanner.innerHTML = bannerContent;

    document.body.appendChild(leftBanner);
    document.body.appendChild(rightBanner);

    // 스크롤할 때 은은하게 반응하는 효과
    window.addEventListener('scroll', () => {
        const move = window.scrollY * 0.05;
        leftBanner.style.transform = `translateY(calc(-50% + ${move}px))`;
        rightBanner.style.transform = `translateY(calc(-50% + ${move}px))`;
    });
})();
