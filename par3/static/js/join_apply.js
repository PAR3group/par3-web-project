// ============================================
// join_apply.js
// PAR3 - JOIN APPLY (조인 참가 신청폼) 페이지 전용 스크립트
// 연결 파일: templates/join/join_apply.html
// 작성자: 오지 (feature/join-page)
//
// 담당 기능:
//   - 폼 제출 시 완료 알림창 표시
// ============================================

document.addEventListener('DOMContentLoaded', function () {

  const form = document.querySelector('.g_form');

  form.addEventListener('submit', function () {
    alert('신청이 정상적으로 완료되었습니다.');
  });

});