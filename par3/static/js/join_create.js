// ============================================
// join_create.js
// PAR3 - JOIN CREATE (조인 개설/모집폼) 페이지 전용 스크립트
// 연결 파일: templates/join/join_create.html
// 작성자: 오지 (feature/join-page)
//
// 담당 기능:
//   1. 엔터 키 입력 시 폼 제출 대신 다음 입력창으로 포커스 이동
//      (단, textarea 안에서는 엔터가 원래대로 줄바꿈으로 동작)
//   2. 지역 선택 드롭다운 열기/닫기 + 선택한 지역명을 버튼 텍스트에 반영
//   3. 폼 제출 시 "폼이 정상적으로 제출되었습니다" 알림창 표시
//      ⚠️ 실제 조인 페이지(join.html)로의 이동은 서버(join_views.py)에서
//         POST 처리 후 redirect(url_for('join.join_list'))로 응답해야 이루어짐.
//         이 파일은 화면 쪽 알림만 담당함.
// ============================================

document.addEventListener('DOMContentLoaded', function () {

  const form = document.querySelector('.g_form');

  // ------------------------------------------------
  // 1. 엔터 키 → 다음 입력창으로 포커스 이동
  // ------------------------------------------------
  const focusableInputs = Array.from(
    form.querySelectorAll('input[type="text"], input[type="date"], input[type="time"], textarea')
  );

  focusableInputs.forEach(function (input, index) {
    input.addEventListener('keydown', function (e) {
      // textarea 안에서는 엔터가 줄바꿈으로 쓰이도록 그대로 둠
      if (e.key === 'Enter' && input.tagName !== 'TEXTAREA') {
        e.preventDefault(); // 폼이 바로 제출되는 기본 동작을 막음
        const next = focusableInputs[index + 1];
        if (next) next.focus();
      }
    });
  });

  // ------------------------------------------------
  // 2. 지역 선택 드롭다운
  // ------------------------------------------------
  const regionSelect = document.getElementById('jc_region_select');

  if (regionSelect) {
    const regionBt = regionSelect.querySelector('.jc_region_bt');
    const regionBtText = regionSelect.querySelector('.jc_region_bt_text');
    const regionOptions = regionSelect.querySelectorAll('input[name="region"]');

    // 버튼 클릭 시 드롭다운 패널 열기/닫기
    regionBt.addEventListener('click', function (e) {
      e.stopPropagation();
      regionSelect.classList.toggle('jc_region_select--open');
    });

    // 드롭다운 바깥을 클릭하면 닫기
    document.addEventListener('click', function () {
      regionSelect.classList.remove('jc_region_select--open');
    });

    // 지역 선택 시 버튼 텍스트를 선택한 지역명으로 바꾸고 드롭다운 닫기
    regionOptions.forEach(function (option) {
      option.addEventListener('change', function () {
        regionBtText.textContent = option.value;
        regionSelect.classList.remove('jc_region_select--open');
      });
    });
  }

  // ------------------------------------------------
  // 3. 폼 제출 시 완료 알림창
  // ------------------------------------------------
  form.addEventListener('submit', function () {
    alert('폼이 정상적으로 제출되었습니다.');
  });

});