let lastScrollTop = 0;
const delta = 5; // 보정치 (너무 민감하게 반응하지 않도록 설정)
const header = document.querySelector('header'); // 본인 헤더 태그나 클래스 선택자

window.addEventListener('scroll', function() {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
    
    // 스크롤 변화량이 delta 값보다 작으면 무시 (미세한 떨림 방지)
    if (Math.abs(lastScrollTop - currentScroll) <= delta) {
        return;
    }
    
    // 아래로 스크롤 중이고, 페이지 맨 위에 있는 게 아닐 때
    if (currentScroll > lastScrollTop && currentScroll > header.offsetHeight) {
        header.classList.add('hide'); // 숨김
    } else {
        // 위로 스크롤 중일 때
        header.classList.remove('hide'); // 나타남
    }
    
    lastScrollTop = currentScroll;
});