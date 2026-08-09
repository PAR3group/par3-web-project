// ============================================
// join_apply.js
// PAR3 - JOIN APPLY (조인 참가 신청폼) 페이지 전용 스크립트
// 연결 파일: templates/join/join_apply.html
// 작성자: 오지 (feature/join-page)
//
// 담당 기능:
//    1. 연락처 3칸 입력 (010 / 중간4자리 / 마지막4자리)
//      - 숫자만 허용, 자릿수 다 채우면 자동으로 다음 칸 이동
//      - 백스페이스로 빈 칸 지우면 이전 칸으로 이동
//      - 세 칸을 합쳐서 hidden input(applicant_phone)에 000-0000-0000 형식으로 저장
//      - 페이지 로드 시, 기존 저장된 연락처 있으면 세 칸에 나눠서 미리 채워줌
//   2. 폼 제출 시 완료 알림창 표시
// ============================================

// ============================================
// join_apply.js
// PAR3 - JOIN APPLY (조인 참가 신청폼) 페이지 전용 스크립트
// 연결 파일: templates/join/join_apply.html
// 작성자: 오지 (feature/join-page)
//
// 담당 기능:
//   1. 연락처 3칸 입력 (010 / 중간4자리 / 마지막4자리)
//      - 숫자만 허용, 자릿수 다 채우면 자동으로 다음 칸 이동
//      - 백스페이스로 빈 칸 지우면 이전 칸으로 이동
//      - 세 칸을 합쳐서 hidden input(applicant_phone)에 000-0000-0000 형식으로 저장
//      - 페이지 로드 시, 기존 저장된 연락처 있으면 세 칸에 나눠서 미리 채워줌
//   2. 폼 제출 시 완료 알림창 표시
// ============================================

document.addEventListener('DOMContentLoaded', function () {

  const form = document.querySelector('.g_form');

  // ------------------------------------------------
  // 모집글 내용(readonly textarea) - 내용 길이만큼 높이 자동 조절
  const contentTextarea = document.querySelector('.g_form_input--textarea[readonly]');
  if (contentTextarea) {
    contentTextarea.style.height = contentTextarea.scrollHeight + 'px';
  }
  // ------------------------------------------------
  // 1. 연락처 3칸 입력
  // ------------------------------------------------
  const phone1 = document.getElementById('phone1');
  const phone2 = document.getElementById('phone2');
  const phone3 = document.getElementById('phone3');
  const phoneHidden = document.getElementById('applicant_phone_hidden');

  function updatePhoneHidden() {
    phoneHidden.value = phone1.value + '-' + phone2.value + '-' + phone3.value;
  }

  if (phone1 && phone2 && phone3) {
    [phone1, phone2, phone3].forEach(function (input, index) {
      // 숫자만 허용 + 자릿수 다 채우면 다음 칸으로 자동 이동
      input.addEventListener('input', function () {
        input.value = input.value.replace(/[^0-9]/g, '');

        if (input.value.length >= input.maxLength) {
          const next = [phone1, phone2, phone3][index + 1];
          if (next) next.focus();
        }

        updatePhoneHidden();
      });

      // 백스페이스로 빈 칸에서 지우면 이전 칸으로 이동
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Backspace' && input.value === '' && index > 0) {
          [phone1, phone2, phone3][index - 1].focus();
        }
      });
    });

    // 페이지 로드 시, hidden input에 이미 들어있는 값(회원가입 시 저장된 연락처)을
    // 세 칸에 나눠서 미리 채워줌
    const existingPhone = phoneHidden.value;
    if (existingPhone && existingPhone.includes('-')) {
      const parts = existingPhone.split('-');
      phone1.value = parts[0] || '';
      phone2.value = parts[1] || '';
      phone3.value = parts[2] || '';
    }
  }

  // ------------------------------------------------
  // 동반자 추가/삭제
  // ------------------------------------------------
  // ------------------------------------------------
  // 인원 추가하기 : 클릭할 때마다 JS 함수로 카드 HTML을 직접 생성해서 추가
  // ------------------------------------------------
  const addBt = document.getElementById('ja_add_companion_bt');
  const applicantList = document.getElementById('ja_applicant_list');
  const maxCompanions = parseInt(form.dataset.maxCompanions || '0', 10);
  let companionCount = 0;

  // 동반자 카드 하나의 HTML을 만들어서 반환하는 함수
  function createCompanionCard(index, displayNumber) {
    const card = document.createElement('div');
    card.className = 'ja_card';
    card.innerHTML =
      '<div class="ja_card_header">' +
      '<span class="ja_card_title">신청자 ' + displayNumber + '</span>' +
      '<span class="ja_remove_bt">삭제</span>' +
      '</div>' +
      '<div class="ja_card_row">' +
      '<div class="ja_card_field">' +
      '<label class="ja_card_label">이름(닉네임)</label>' +
      '<input type="text" class="g_form_input--text" name="companion_name_' + index + '" placeholder="이름이나 닉네임을 입력해주세요">' +
      '</div>' +
      '<div class="ja_card_field">' +
      '<label class="ja_card_label">연락처</label>' +
      '<div class="jc_phone_wrap">' +
          '<input type="text" class="g_form_input--text jc_phone_part companion_phone_part" maxlength="3" placeholder="010">' +
          '<span class="jc_phone_dash">-</span>' +
          '<input type="text" class="g_form_input--text jc_phone_part companion_phone_part" maxlength="4" placeholder="0000">' +
          '<span class="jc_phone_dash">-</span>' +
          '<input type="text" class="g_form_input--text jc_phone_part companion_phone_part" maxlength="4" placeholder="0000">' +
        '</div>' +
        '<input type="hidden" name="companion_phone_' + index + '" class="companion_phone_hidden">' +
      '</div>' +
      '</div>' +
      '<div class="ja_card_row">' +
      '<div class="ja_card_field">' +
      '<label class="ja_card_label">구력</label>' +
      '<input type="text" class="g_form_input--text" name="companion_experience_' + index + '" placeholder="예: 3년차">' +
      '</div>' +
      '<div class="ja_card_field">' +
      '<label class="ja_card_label">평균 스코어(핸디캡)</label>' +
      '<div class="g_form_input--radio">' +
      '<label><input type="radio" name="companion_handicap_' + index + '" value="80대 이하"> 80대 이하</label>' +
      '<label><input type="radio" name="companion_handicap_' + index + '" value="90대"> 90대</label>' +
      '<label><input type="radio" name="companion_handicap_' + index + '" value="100대"> 100대</label>' +
      '<label><input type="radio" name="companion_handicap_' + index + '" value="110 이상"> 110 이상</label>' +
      '</div>' +
      '</div>' +
      '</div>';
    return card;
  }

  if (addBt) {
    addBt.addEventListener('click', function () {
      if (companionCount >= maxCompanions) return;

      companionCount++;
      const displayNumber = companionCount + 1;
      const newCard = createCompanionCard(companionCount, displayNumber);

      newCard.querySelector('.ja_remove_bt').addEventListener('click', function () {
        newCard.remove();
        companionCount--;
        renumberCards();
        toggleAddButton();
      });

      applicantList.appendChild(newCard);
      toggleAddButton();
    });
  }

  function renumberCards() {
    const companionCards = applicantList.querySelectorAll('.ja_card:not(:first-child)');
    companionCards.forEach(function (card, i) {
      card.querySelector('.ja_card_title').textContent = '신청자 ' + (i + 2);
    });
  }

  function toggleAddButton() {
    if (!addBt) return;
    addBt.style.display = (companionCount >= maxCompanions) ? 'none' : 'block';
  }

  // ------------------------------------------------
  // 2. 폼 제출 시 완료 알림창
  // ------------------------------------------------
  form.addEventListener('submit', function () {
    alert('신청이 정상적으로 완료되었습니다.');
  });

});