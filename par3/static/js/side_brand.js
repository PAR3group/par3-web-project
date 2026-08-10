// 좌우 세로 GOLF SHOP 텍스트가 스크롤에 살짝 뒤늦게 따라오는(트레일링) 효과
// position: absolute라서 스크롤하면 문서와 함께 자연스럽게 움직이고,
// top 값을 lerp로 늦게 갱신해서 화면 중앙을 조금 늦게 쫓아가도록 만든다.
(function () {
    const els = document.querySelectorAll('.side-brand-text');
    if (!els.length) return;

    function targetTop() {
        return window.scrollY + window.innerHeight / 2;
    }

    let current = targetTop();

    function tick() {
        const target = targetTop();
        current += (target - current) * 0.06;

        els.forEach(el => {
            el.style.top = `${current}px`;
        });

        requestAnimationFrame(tick);
    }

    tick();
})();
