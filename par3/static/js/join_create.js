// ============================================
// join_create.js
// PAR3 - JOIN CREATE (조인 개설/모집폼) 페이지 전용 스크립트
// 연결 파일: templates/join/join_create.html
// 작성자: 오지 (feature/join-page)
//
// 담당 기능:
//   1. 엔터 키 입력 시 폼 제출 대신 다음 입력창으로 포커스 이동
//   2. 지역 선택 + 골프장 검색 (한국관광공사 TourAPI 연동)
//      - 지역만 선택: 그 지역 전체 골프장 목록
//      - 검색어만 입력: 전국에서 키워드 검색
//      - 둘 다: 그 지역 안에서 키워드로 필터링
//   3. 폼 제출 시 완료 알림창 표시
// ============================================

document.addEventListener('DOMContentLoaded', function () {
  // ------------------------------------------------
  // 라운드 날짜 선택 - Flatpickr (placeholder: 2026-08-09 형식 표시,
  // 달력 아이콘은 CSS로 입력창 왼쪽에 배치)
  // ------------------------------------------------
  flatpickr("#round_date_picker", {
    dateFormat: "Y-m-d",   // 저장/전송되는 실제 값 형식 (YYYY-MM-DD)
    minDate: "today",       // 과거 날짜 선택 방지 (선택사항, 필요없으면 이 줄 삭제)
  });
  // ------------------------------------------------
  // 티오프 시간 선택 - Flatpickr (시간 전용 모드)
  // ------------------------------------------------
  flatpickr("#tee_time_picker", {
    enableTime: true,
    noCalendar: true,      // 날짜 달력 없이 시간만
    dateFormat: "h:i K",   // 화면 표시: 오전/오후 형식 (예: 11:30 AM)
    time_24hr: false,        // 12시간제 + AM/PM
  });

  const form = document.querySelector('.g_form');

  // ------------------------------------------------
  // 1. 엔터 키 → 다음 입력창으로 포커스 이동
  // ------------------------------------------------
  const focusableInputs = Array.from(
    form.querySelectorAll('input[type="text"], input[type="date"], input[type="time"], textarea')
  );

  focusableInputs.forEach(function (input, index) {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && input.tagName !== 'TEXTAREA') {
        e.preventDefault();
        const next = focusableInputs[index + 1];
        if (next) next.focus();
      }
    });
  });

  // ------------------------------------------------
  // 2. 지역 선택 + 골프장 검색 (TourAPI 연동)
  // ------------------------------------------------
  const regionSelect = document.getElementById('jc_region_select');
  const courseSearchInput = document.getElementById('jc_course_search_input');
  const coursePanel = document.getElementById('jc_course_panel');
  const courseNameHidden = document.getElementById('jc_course_name_hidden');
  const regionHidden = document.getElementById('jc_region_hidden');
  const thumbImgHidden = document.getElementById('jc_thumb_img_hidden');

  let currentRegion = '';
  let searchTimer = null;

  if (regionSelect) {
    const regionBt = regionSelect.querySelector('.jc_region_bt');
    const regionBtText = regionSelect.querySelector('.jc_region_bt_text');
    const regionOptions = regionSelect.querySelectorAll('input[name="region_radio"]');

    // 지역 드롭다운 열기/닫기
    regionBt.addEventListener('click', function (e) {
      e.stopPropagation();
      regionSelect.classList.toggle('jc_region_select--open');
    });

    // 지역 선택 시 → 즉시 그 지역 전체 골프장 목록 조회
    regionOptions.forEach(function (option) {
      option.addEventListener('change', function () {
        currentRegion = option.value;
        regionBtText.textContent = currentRegion;
        regionHidden.value = currentRegion;
        regionSelect.classList.remove('jc_region_select--open');

        fetchAndShowCourses(currentRegion, courseSearchInput.value.trim());
      });
    });
  }

  if (courseSearchInput) {
    // 검색창 타이핑 → 지역 선택 여부와 무관하게 검색
    courseSearchInput.addEventListener('input', function () {
      // 사용자가 직접 입력한 값도 실시간으로 hidden input에 반영
      // (드롭다운에서 고르면 이 값이 덮어써짐)
      courseNameHidden.value = courseSearchInput.value;
      
      clearTimeout(searchTimer);
      const keyword = courseSearchInput.value.trim();

      // 지역도 없고 키워드도 짧으면 검색 안 함
      if (!currentRegion && keyword.length < 2) {
        coursePanel.classList.remove('jc_course_panel--visible');
        return;
      }

      searchTimer = setTimeout(function () {
        fetchAndShowCourses(currentRegion, keyword);
      }, 300);
    });

    // 검색창 클릭이 바깥 클릭 이벤트로 안 번지게
    courseSearchInput.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  // ------------------------------------------------
  // API 호출 (region, keyword 둘 다 선택적으로 전달)
  // ------------------------------------------------
  function fetchAndShowCourses(region, keyword) {
    coursePanel.innerHTML = '<div class="jc_course_empty">불러오는 중...</div>';
    coursePanel.classList.add('jc_course_panel--visible');

    const params = new URLSearchParams();
    if (region) params.append('region', region);
    if (keyword) params.append('keyword', keyword);

    fetch('/join/api/golf_courses?' + params.toString())
      .then(function (res) { return res.json(); })
      .then(function (data) { renderCourseList(data.results); })
      .catch(function () {
        coursePanel.innerHTML = '<div class="jc_course_empty">불러오기에 실패했습니다</div>';
      });
  }

  // ------------------------------------------------
  // 검색/필터링 결과를 드롭다운 목록으로 렌더링
  // ------------------------------------------------
  function renderCourseList(results) {
    coursePanel.innerHTML = '';

    if (!results || results.length === 0) {
      coursePanel.innerHTML = '<div class="jc_course_empty">골프장을 찾을 수 없습니다</div>';
      return;
    }

    results.forEach(function (course) {
      const item = document.createElement('div');
      item.className = 'jc_course_item';
      item.innerHTML =
        '<img class="jc_course_item_thumb" src="' + (course.image || '/static/img/no_image.png') + '">' +
        '<div class="jc_course_item_info">' +
        '<span class="jc_course_item_name">' + course.name + '</span>' +
        '<span class="jc_course_item_region">' + course.region + '</span>' +
        '</div>';

      item.addEventListener('click', function () {
        courseSearchInput.value = course.name;
        courseNameHidden.value = course.name;
        // 지역이 선택 안 된 상태로 검색해서 고른 경우, 그 골프장의 지역으로 자동 반영
        if (!currentRegion) {
          regionHidden.value = course.region;
        }
        thumbImgHidden.value = course.image || '';
        coursePanel.classList.remove('jc_course_panel--visible');
      });

      coursePanel.appendChild(item);
    });
  }

  // 드롭다운 바깥 클릭 시 지역/골프장 패널 둘 다 닫기
  document.addEventListener('click', function () {
    if (regionSelect) regionSelect.classList.remove('jc_region_select--open');
    coursePanel.classList.remove('jc_course_panel--visible');
  });

  if (regionSelect) {
    regionSelect.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  // ------------------------------------------------
  // 3. 폼 제출 시 완료 알림창
  // ------------------------------------------------
  form.addEventListener('submit', function () {
    alert('폼이 정상적으로 제출되었습니다.');
  });

});