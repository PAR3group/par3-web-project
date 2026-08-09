document.addEventListener("DOMContentLoaded", () => {
    // 1. 메뉴 이동 (반응형 상단 고정 오프셋 반영/ 초록색 active 변경 및 우측 독립 스크롤)
    const menuItems = document.querySelectorAll(".menu-item");

    menuItems.forEach(item => {
        item.addEventListener("click", () => {
            // 모든 메뉴에서 active(초록색) 클래스를 떼고, 클릭한 메뉴에만 붙이기
            menuItems.forEach(m => m.classList.remove("active"));
            item.classList.add("active");

            // 오른쪽 스크롤 영역 내부에서 해당 카드로 부드럽게 이동
            const target = item.dataset.target;
            const targetElement = document.querySelector(`#${target}`);

            if (targetElement) {
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - 20;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                
                });
            }
        });
    }); // <-- [중요] 기존 코드에서 빠져있던 닫는 괄호(})를 완벽하게 작성!
        
    // 2. 주소 검색 (Daum API)
    const btnAddress = document.getElementById("btn-search-address");
    if (btnAddress) {
        btnAddress.addEventListener("click", () => {
            new daum.Postcode({
                oncomplete: function(data) {
                    document.getElementById("home_address").value = data.address;
                }
            }).open();
        });
    }

    // 3. 이력관리 모달
    const modal = document.getElementById("detail-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");
    const closeBtn = document.getElementById("btn-modal-close");

    const modalDataMap = {
        posts: { title: "작성한 게시글", items: ["PAR3 이용후기", "드라이버 추천", "주말 라운딩 모집"] },
        join_likes: { title: "골프조인 찜내역", items: ["제주도 골프투어", "강원도 조인"] },
        join_posts: { title: "골프조인 등록글", items: ["9월 10일 조인 모집"] },
        join_participate: { title: "골프조인 참여내역", items: ["남서울CC", "블루원CC"] },
        shop_likes: { title: "쇼핑 찜목록", items: ["타이틀리스트 T200", "오디세이 퍼터"] },
        shop_orders: { title: "주문내역", items: ["드라이버 구매", "골프공 구매"] }
    };

    // [확인] 버튼을 클릭했을 때 모달창 열기
    document.querySelectorAll(".btn-act-check").forEach(btn => {
        btn.addEventListener("click", () => {
            const type = btn.dataset.type;
            const data = modalDataMap[type];

            if (data) {
                modalTitle.textContent = data.title;
                modalBody.innerHTML = data.items.map(item => `<div class="modal-item">${item}</div>`).join("");
                modal.style.display = "flex";
            }
        });
    });
    
    // [닫기] 버튼 누르면 모달창 닫기
    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            modal.style.display = "none";
        });
    }

    // 모달창 밖의 어두운 배경을 눌러도 닫히게 하기
    if (modal) {
        modal.addEventListener("click", e => {
            if (e.target === modal) {
                modal.style.display = "none";
            }
        });
    }
}); // DOMContentLoaded 닫는 괄호
