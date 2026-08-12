document.addEventListener('DOMContentLoaded', function () {

  // ------------------------------------------------
  // 신청자 개별 취소 : 확인창 후 서버로 취소 요청 전송
  // ------------------------------------------------
  document.querySelectorAll('.jc_cancel_applicant_bt').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const applyId = btn.dataset.applyId;
      const confirmed = confirm('이 신청자의 참여를 취소하시겠습니까?');
      if (!confirmed) return;

      const form = document.getElementById('jc_cancel_applicant_form');
      form.action = '/join/cancel_applicant/' + applyId;
      form.submit();
    });
  });

  // ------------------------------------------------
  // 글 삭제 : 확인창 후 삭제 요청 전송 (신청자 0명일 때만 버튼이 존재함)
  // ------------------------------------------------
  const deleteBt = document.getElementById('jc_delete_bt');
  if (deleteBt) {
    deleteBt.addEventListener('click', function () {
      const confirmed = confirm('정말 이 조인 글을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.');
      if (!confirmed) return;

      document.getElementById('jc_delete_form').submit();
    });
  }

});