document.addEventListener('DOMContentLoaded', function () {
    const viewport = document.querySelector('.m_shop_card .shop_product_viewport');
    const container = document.querySelector('.m_shop_card .shop_product_container');
    if (!container || !viewport) return;

    const visibleCount = 2;
    const gap = 16;
    const originalCards = Array.from(container.children);

    if (originalCards.length <= visibleCount) return;

    // 앞쪽 카드들을 뒤에 복제해서 붙임 (무한루프용)
    originalCards.slice(0, visibleCount).forEach(function (card) {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        container.appendChild(clone);
    });

    let index = 0;
    const realCount = originalCards.length;

    function getCardWidth() {
        return container.children[0].getBoundingClientRect().width + gap;
    }

    function moveTo(i, withTransition) {
        container.style.transition = withTransition ? 'transform 0.5s ease' : 'none';
        container.style.transform = 'translateX(-' + (i * getCardWidth()) + 'px)';
    }

    // 트랜지션 끝났을 때, 복제본 구간에 도달했으면 원본 위치로 순간 이동
    container.addEventListener('transitionend', function () {
        if (index >= realCount) {
            index = 0;
            moveTo(index, false);
        }
    });

    setInterval(function () {
        index++;
        moveTo(index, true);
    }, 5000);

    // 창 크기 바뀔 때 카드 너비가 달라지므로 현재 위치 재계산
    window.addEventListener('resize', function () {
        moveTo(index, false);
    });
});