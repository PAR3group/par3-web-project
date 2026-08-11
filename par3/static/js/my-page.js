// ==========================================================
// 프로필 사진 크게 보기 모달
// ==========================================================

function openProfileImageModal(imgSrc) {
    const modal = document.getElementById('image-view-modal');
    const modalImg = document.getElementById('enlarged-profile-img');

    if (modal && modalImg) {
        modalImg.src = imgSrc;
        modal.style.display = 'flex';
    }
}

function closeProfileImageModal() {
    const modal = document.getElementById('image-view-modal');

    if (modal) {
        modal.style.display = 'none';
    }
}


// ==========================================================
// 프로필 비동기 이미지 업로드
// ==========================================================

const avatarInput = document.getElementById('avatar-input');

if (avatarInput) {
    avatarInput.addEventListener('change', function () {
        const file = this.files && this.files[0];

        if (!file) return;

        const preview = document.getElementById('profile-preview');
        const previousSrc = preview.src;

        preview.src = window.URL.createObjectURL(file);

        const formData = new FormData();
        formData.append('avatar_file', file);

        fetch(avatarInput.dataset.uploadUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                preview.src = data.profile_img;
            } else {
                alert(data.message || '프로필 사진 저장에 실패했습니다.');
                preview.src = previousSrc;
            }
        })
        .catch(() => {
            alert('프로필 사진 저장 중 오류가 발생했습니다.');
            preview.src = previousSrc;
        })
        .finally(() => {
            avatarInput.value = '';
        });
    });
}


// ==========================================================
// DOM 로드 후 실행
// ==========================================================

document.addEventListener("DOMContentLoaded", () => {

    // ======================================================
    // 1. 이메일 도메인 선택
    // ======================================================

    const domainInput = document.getElementById('email-domain');
    const domainSelect = document.getElementById('email-domain-select');

    if (domainSelect && domainInput) {
        domainSelect.addEventListener('change', function () {
            if (this.value === '') {
                domainInput.value = '';
                domainInput.focus();
            } else {
                domainInput.value = this.value;
            }
        });
    }


    // ======================================================
    // 2. 프로필 폼 저장
    // ======================================================

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


    // ======================================================
    // 3-1. 전화번호 국가코드 검색 기능
    // ======================================================

    const countryCodeSelect = document.getElementById('phone-country-code');

    if (countryCodeSelect && typeof TomSelect !== 'undefined') {
        new TomSelect('#phone-country-code', {
            placeholder: "국가선택",
            allowEmptyOption: true,
            create: false,
            sortField: {
                field: "text",
                direction: "asc"
            }
        });
    }


    // ======================================================
    // 3-2. 휴대전화 번호 3칸 입력
    // ======================================================

    const phoneFirst = document.getElementById('phone-first');
    const phoneMiddle = document.getElementById('phone-middle');
    const phoneLast = document.getElementById('phone-last');
    const phoneHidden = document.getElementById('user-phone');

    // DB 전화번호 → 3칸 분리
    if (phoneHidden && phoneHidden.value) {
        const savedPhone = phoneHidden.value.replace(/[^0-9]/g, '');

        if (phoneFirst) {
            phoneFirst.value = savedPhone.substring(0, 3);
        }

        if (phoneMiddle) {
            phoneMiddle.value = savedPhone.substring(3, 7);
        }

        if (phoneLast) {
            phoneLast.value = savedPhone.substring(7, 11);
        }
    }


    // 숫자만 입력 + 다음 칸 자동 이동
    const phoneParts = [phoneFirst, phoneMiddle, phoneLast];

    phoneParts.forEach(input => {
        if (!input) return;

        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9]/g, '');

            if (
                this.value.length === Number(this.maxLength) &&
                this === phoneFirst &&
                phoneMiddle
            ) {
                phoneMiddle.focus();
            }

            if (
                this.value.length === Number(this.maxLength) &&
                this === phoneMiddle &&
                phoneLast
            ) {
                phoneLast.focus();
            }
        });
    });


    // 저장할 때 전화번호 합치기
    if (profileForm) {
        profileForm.addEventListener('submit', function () {
            if (!phoneHidden) return;

            const first = phoneFirst ? phoneFirst.value.trim() : '';
            const middle = phoneMiddle ? phoneMiddle.value.trim() : '';
            const last = phoneLast ? phoneLast.value.trim() : '';

            if (first && middle && last) {
                phoneHidden.value = `${first}-${middle}-${last}`;
            } else {
                phoneHidden.value = '';
            }
        });
    }


    // ======================================================
    // 4. 사이드바 메뉴 이동
    // ======================================================

    const menuItems = document.querySelectorAll(".menu-item");

    menuItems.forEach(item => {
        item.addEventListener("click", () => {
            menuItems.forEach(m => m.classList.remove("active"));
            item.classList.add("active");

            const target = item.dataset.target;
            const targetElement = document.querySelector(`#${target}`);

            if (targetElement) {

                if (target === 'sec-profile') {
                    window.scrollTo({
                        top: 0,
                        behavior: "smooth"
                    });

                    return;
                }

                const sidebar = document.querySelector('.sidebar');
                let offset = 20;

                if (window.innerWidth <= 768 && sidebar) {
                    offset = sidebar.offsetHeight + 15;
                }

                const bodyRect = document.body.getBoundingClientRect().top;
                const elementRect = targetElement.getBoundingClientRect().top;

                const offsetPosition =
                    (elementRect - bodyRect) - offset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });


    // ======================================================
    // 5. 주소 검색
    // ======================================================

    const btnAddress = document.getElementById("btn-search-address");

    if (btnAddress) {
        btnAddress.addEventListener("click", () => {
            new daum.Postcode({
                oncomplete: function (data) {
                    document.getElementById("home_address").value =
                        data.address;
                }
            }).open();
        });
    }


    // ======================================================
    // 6. 이력관리 모달
    // ======================================================

    const modal = document.getElementById("detail-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");
    const closeBtn = document.getElementById("btn-modal-close");


    // ------------------------------------------------------
    // 실제 내가 작성한 TALK 게시글
    // ------------------------------------------------------

    const myPostItems = Array.from(
        document.querySelectorAll('.my-post-data')
    ).map(post => ({
        id: post.dataset.id,
        title: post.dataset.title,
        content: post.dataset.content,
        date: post.dataset.date        
    }));


    // ------------------------------------------------------
    // 실제 내가 작성한 골프조인 글
    // ------------------------------------------------------

    const myJoinPostItems = Array.from(
        document.querySelectorAll('.my-join-post-data')
    ).map(join => ({
        id: join.dataset.id,
        title: join.dataset.title,
        course: join.dataset.course,
        date: join.dataset.date,
        time: join.dataset.time
    }));


    // ------------------------------------------------------
    // 실제 내가 참여한 골프조인
    // ------------------------------------------------------

    const myJoinParticipateItems = Array.from(
        document.querySelectorAll('.my-join-participate-data')
    ).map(join => ({
        id: join.dataset.id,
        title: join.dataset.title,
        course: join.dataset.course,
        date: join.dataset.date,
        time: join.dataset.time,
    }));

    // 실제 장바구니 데이터 읽기
    const myCartItems = Array.from(
        document.querySelectorAll('.my-cart-item-data')
    ).map(item => ({
        id: item.dataset.id,
        title: item.dataset.title,
        brand: item.dataset.brand,
        quantity: item.dataset.quantity
    }));


    // ------------------------------------------------------
    // 이력관리 데이터
    // ------------------------------------------------------

    const modalDataMap = {

        posts: {
            title: "작성한 게시글",
            items: myPostItems
        },

        // 아직 실제 찜 저장 기능 연결 전
        join_likes: {
            title: "골프조인 찜내역",
            items: ["제주도 골프투어", "강원도 조인"]
        },

        join_posts: {
            title: "골프조인 등록글",
            items: myJoinPostItems
        },

        join_participate: {
            title: "골프조인 참여내역",
            items: myJoinParticipateItems
        },

        // 이후 실제 장바구니 DB로 변경 예정
        shop_likes: {
            title: "장바구니",
            items: myCartItems
        },

        // 주문 모델 연결 전
        shop_orders: {
            title: "쇼핑 내역",
            items: ["드라이버 구매", "골프공 구매"]
        }
    };


    // ------------------------------------------------------
    // 이력관리 카드 클릭
    // ------------------------------------------------------

    document.querySelectorAll(".btn-act-check").forEach(btn => {

        btn.addEventListener("click", () => {

            const type = btn.dataset.type;
            const data = modalDataMap[type];

            if (!data || !modal || !modalTitle || !modalBody) {
                return;
            }

            modalTitle.textContent = data.title;


            // ==================================================
            // 작성한 TALK 게시글
            // ==================================================

            if (type === 'posts') {

                if (data.items.length === 0) {
                    modalBody.innerHTML = `
                        <div class="modal-item">
                            작성한 게시글이 없습니다.
                        </div>
                    `;
                } else {
                    modalBody.innerHTML = data.items.map(item => `
                        <div
                            class="modal-item modal-post-item"
                            onclick="goMyPostDetail(${item.id})"
                        >
                            <strong>${item.title}</strong>
                            <div class="my-post-preview">${item.content || ''}</div>
                            <div>${item.date}</div>
                        </div>
                    `).join("");
                }


            // ==================================================
            // 내가 작성한 골프조인
            // ==================================================

            } else if (type === 'join_posts') {

                if (data.items.length === 0) {

                    modalBody.innerHTML = `
                        <div class="modal-item">
                            작성한 골프조인 글이 없습니다.
                        </div>
                    `;

                } else {
                    modalBody.innerHTML = data.items.map(item => `
                        <div
                            class="modal-item modal-post-item"
                            onclick="goMyJoinPost(${item.id})"
                        >
                            <strong>${item.title || '제목 없음'}</strong>

                            <div>
                                ${item.date || ''} · ${item.course || ''} · 티오프 ${item.time || ''}
                            </div>
                        </div>
                    `).join("");
                }
                
            

            // ==================================================
            // 내가 참여한 골프조인
            // ==================================================

            } else if (type === 'join_participate') {

                if (data.items.length === 0) {

                    modalBody.innerHTML = `
                        <div class="modal-item">
                            참여한 골프조인 내역이 없습니다.
                        </div>
                    `;

                } else {

                    modalBody.innerHTML = data.items.map(item => `
                        <div 
                            class="modal-item modal-post-item"
                            onclick="goMyJoinPost(${item.id})"
                        >
                            <strong>${item.title || '제목 없음'}</strong>

                            <div>
                                ${item.date || ''} · ${item.course || ''} · 티오프 ${item.time || ''} 
                            </div>
                        </div>
                    `).join("");

                }


            // ==================================================
            // 나머지 이력
            // ==================================================
            } else if (type === 'shop_likes') {

                if (data.items.length === 0) {
                    modalBody.innerHTML = `
                        <div class="modal-item">
                            장바구니에 담긴 상품이 없습니다.
                        </div>
                    `;
                } else {
                    modalBody.innerHTML = data.items.map(item => `
                        <div
                            class="modal-item modal-post-item"
                            onclick="goMyCart()"
                        >
                            <strong>${item.title}</strong>
                            <div>${item.brand || ''}</div>
                            <div>수량 : ${item.quantity}</div>
                        </div>
                    `).join("");
                }

            } else {

                modalBody.innerHTML = data.items.map(item =>
                    `<div class="modal-item">${item}</div>`
                ).join("");

            }


            // 모달 열기
            modal.style.display = "flex";
        });
    });


    // ------------------------------------------------------
    // 모달 닫기 버튼
    // ------------------------------------------------------

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            modal.style.display = "none";
        });
    }


    // ------------------------------------------------------
    // 모달 바깥 클릭 시 닫기
    // ------------------------------------------------------

    if (modal) {
        modal.addEventListener("click", e => {

            if (e.target === modal) {
                modal.style.display = "none";
            }

        });
    }

}); // DOMContentLoaded 끝


// ==========================================================
// 이력관리 상세페이지 이동
// ==========================================================

// TALK 작성 게시글 → 해당 게시글 상세페이지
function goMyPostDetail(postId) {
    window.location.href = `/talk/${postId}`;
}


// 골프조인 작성글 / 참여내역 → 해당 조인 채팅방
function goMyJoinPost(joinId) {
    window.location.href = `/join/${joinId}/chat`;
}

// 장바구니 상품 → 상품 상세페이지
function goMyCartProduct(productId) {
    window.location.href = `/shop/${productId}`;
};

function goMyCart() {
    window.location.href = '/shop/cart';
}