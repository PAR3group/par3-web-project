document.addEventListener('DOMContentLoaded', () => {
  const data = window.RECOMMEND_DATA || {};
  const isLoggedIn = data.isLoggedIn;
  const recommendResult = data.result;
  const recommendFlex = data.flex;

  // 실제 저장 API 호출 (공통 함수)
  function doSaveRequest(resultData, flexData, silentSuccess) {
    fetch('/recommend/api/save-recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ result: resultData, flex: flexData })
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          alert(silentSuccess ? '로그인 후 결과가 자동으로 저장되었습니다!' : data.message);
        } else {
          alert(data.message || '저장 실패');
        }
      })
      .catch(err => alert('저장 중 오류가 발생했습니다.'));
  }

  // 버튼 클릭 시 실행되는 함수 (전역으로 등록해야 onclick="saveRecommend()"에서 호출 가능)
  window.saveRecommend = function () {
    if (!isLoggedIn) {
      if (confirm('로그인이 필요한 기능입니다. 로그인 페이지로 이동할까요?')) {
        sessionStorage.setItem('pendingSave', JSON.stringify({
          result: recommendResult,
          flex: recommendFlex
        }));
        location.href = `/auth/login?next=${encodeURIComponent(location.pathname)}`;
      }
      return;
    }

    doSaveRequest(recommendResult, recommendFlex, false);
  };

  // 로그인 후 돌아왔을 때 자동 저장 처리
  const pending = sessionStorage.getItem('pendingSave');
  if (isLoggedIn && pending) {
    sessionStorage.removeItem('pendingSave');
    const parsed = JSON.parse(pending);
    doSaveRequest(parsed.result, parsed.flex, true);
  }

  // ===== 기존 recommend.js에 있던 폼 토글 로직 =====
  const toggles = document.querySelectorAll('.rc_club_toggle');

  function syncBox(toggle) {
    const targetId = toggle.getAttribute('data-target');
    const box = document.getElementById(targetId);
    if (!box) return;

    const input = box.querySelector('input');

    if (toggle.checked) {
      box.classList.add('rc_distance_box--active');
      if (input) input.setAttribute('required', 'required');
    } else {
      box.classList.remove('rc_distance_box--active');
      if (input) {
        input.removeAttribute('required');
        input.value = '';
      }
    }
  }

  toggles.forEach(function (toggle) {
    syncBox(toggle);
    toggle.addEventListener('change', function () {
      syncBox(toggle);
    });
  });

  const unknownCheckbox = document.getElementById('swing-speed-unknown');
  const speedInput = document.getElementById('swing-speed-input');

  function syncSpeedInput() {
    if (!unknownCheckbox || !speedInput) return;

    if (unknownCheckbox.checked) {
      speedInput.value = '';
      speedInput.disabled = true;
    } else {
      speedInput.disabled = false;
    }
  }

  if (unknownCheckbox) {
    syncSpeedInput();
    unknownCheckbox.addEventListener('change', syncSpeedInput);
  }
});