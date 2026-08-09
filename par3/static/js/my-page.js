document.addEventListener("DOMContentLoaded", () => {
    // 1. 도메인 선택 이벤트
    // 이메일 도메인 선택 시 입력창 자동 채우기 / 직접입력 처리
    const domainInput = document.getElementById('email-domain');
    const domainSelect = document.getElementById('email-domain-select');

    if (domainSelect && domainInput) {
        domainSelect.addEventListener('change', function() {
            if (this.value === '') {
                domainInput.value = '';
                domainInput.focus();
            } else {
                domainInput.value = this.value;
            }
        });
    }

    // 2. 폼 저장(submit) 시 백엔드로 통합 이메일(par3@kakao.com) 전송
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function () {
            const emailId = document.getElementById('email-id').value.trim();
            const emailDomain = document.getElementById('email-domain').value.trim();
            
            let hiddenEmail = document.getElementById('email-full');
            if (!hiddenEmail) {
                hiddenEmail = document.createElement('input');
                hiddenEmail.type = 'hidden';
                hiddenEmail.id = 'email-full';
                hiddenEmail.name = 'email';
                this.appendChild(hiddenEmail);
            }

            if (emailId && emailDomain) {
                hiddenEmail.value = `${emailId}@${emailDomain}`;
            } else {
                hiddenEmail.value = '';
            }
        });
    }

    // 3-1. 전화번호 국가코드 검색 기능 (TomSelect)
        const countryCodeSelect = document.getElementById('phone-country-code');
        if (countryCodeSelect && typeof TomSelect !== 'undefined') {
            const ts = new TomSelect('#phone-country-code', {
                placeholder: "국가선택",
                allowEmptyOption: true,
                create: false,
                sortField: {
                    field: "text",
                    direction: "asc"
                }
            });
            // ts.on('dropdown_open') 처리 제거 완료
        }

    // 3-2. 휴대전화 번호 하이픈(-) 자동 포맷팅
    const phoneInput = document.getElementById('user-phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            let val = e.target.value.replace(/[^0-9]/g, '');
            if (val.length > 11) val = val.substring(0, 11);

            if (val.length < 4) {
                e.target.value = val;
            } else if (val.length < 8) {
                e.target.value = `${val.substr(0, 3)}-${val.substr(3)}`;
            } else {
                e.target.value = `${val.substr(0, 3)}-${val.substr(3, 4)}-${val.substr(7)}`;
            }
        });
    }

    // 4. 사이드바 메뉴 이동
    const menuItems = document.querySelectorAll(".menu-item");
    menuItems.forEach(item => {
        item.addEventListener("click", () => {
            menuItems.forEach(m => m.classList.remove("active"));
            item.classList.add("active");

            const target = item.dataset.target;
            const targetElement = document.querySelector(`#${target}`);

            if (targetElement) {
                if (target === 'sec-profile') {
                    window.scrollTo({ top: 0, behavior: "smooth" });
                    return;
                }

                const sidebar = document.querySelector('.sidebar');
                let offset = 20;

                if (window.innerWidth <= 768 && sidebar) {
                    offset = sidebar.offsetHeight + 15;
                }

                const bodyRect = document.body.getBoundingClientRect().top;
                const elementRect = targetElement.getBoundingClientRect().top;
                const offsetPosition = (elementRect - bodyRect) - offset;

                window.scrollTo({ top: offsetPosition, behavior: "smooth" });
            }
        });
    });

    // 5. 주소 검색 (Daum Kakao)
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

    // 6. 이력관리 모달
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

    if (closeBtn) {
        closeBtn.addEventListener("click", () => { modal.style.display = "none"; });
    }
    if (modal) {
        modal.addEventListener("click", e => { if (e.target === modal) modal.style.display = "none"; });
    }
});